#!/usr/bin/env python

# Copyright (c) 2013 Alexander Schrijver <alex@flupzor.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Poor man's character recognition which compares vertical lines to a list of
# pre-defined characters. If one character is found which completely matches the
# character in the image, the character is cut off of the image and the
# process runs again until nothing is left (all characters have been found).

import os

from PIL import Image

DEBUG=False

class CustomImage:
    def __init__(self, img):
        # always convert to RGBA, so img.getpixels returns the type.
        new_img = img.convert('RGBA')

        self._img = new_img

    def vline(self, x):
        l = []
        width, height = self.size

        for i in range(height):
            color = self.getpixel((x, i))
            l.append(color)

        return l

    def match_vline(self, img, x):
        if DEBUG:
            print "Matching the following two lines:"
            print self.vline(x)
            print img.vline(x)
        return self.vline(x) == img.vline(x)

    def cutoff(self, x):
        return CustomImage(self.crop((x, 0, self.width, self.height)))

    @property
    def width(self):
        width, height = self.size
        return width

    @property
    def height(self):
        width, height = self.size
        return height

    def __getattr__(self, name):
        return getattr(self._img, name)

def openimg(filename):
    return CustomImage(Image.open(filename))

def cropimg(filename, start_x, end_x):
    img = openimg(filename)

    return CustomImage(img.crop((start_x, 0, end_x, img.height)))

def _match_to_characters(img, matches, line):
    new_matches = {}

    if DEBUG:
        print "Image width: %d" % (img.width, )
        print "Matching line: %d" % (line, )

    for char, char_img in matches.items():

        if line < char_img.width and img.match_vline(char_img, line):
            if DEBUG:
                print "Line %d matches %s" % (line, char)
            new_matches[char] = char_img

    largest_width = 0
    for char, char_img in new_matches.items():
        if char_img.width > largest_width:
            largest_width = char_img.width

    if line < largest_width-1:
        return _match_to_characters(img, new_matches, line+1)

    return new_matches

characters = {
    "0": cropimg("templates/0_33.png", 0, 5),
    "1": cropimg("templates/1_64.png", 0, 5),
    "2": cropimg("templates/2_19.png", 0, 5),
    "3": cropimg("templates/3_66.png", 0, 5),
    "4": cropimg("templates/4_70.png", 0, 5),
    "5": cropimg("templates/59_50.png", 0, 5),
    "6": cropimg("templates/6_05.png", 0, 5),
    "7": cropimg("templates/7.75.png", 0, 4),
    "8": cropimg("templates/850_05.png", 0, 5),
    "9": cropimg("templates/907_85.png", 0, 5),
    ".": cropimg("templates/0_33.png", 5, 8),
    "EUR": cropimg("templates/0_33.png", 18, 27),
}

def match_character(img):
    if img.width == 0:
        return None

    matches = _match_to_characters(img, characters, 0)
    if len(matches) > 1:
        raise Exception("Too many results returned")

    if len(matches) == 0:
        return None

    return matches.items()[0]

def match_characters(img):
    characters_found = ''
    while True:
        match = match_character(img)
        if match == None:
            break;

        characters_found += (match[0])

        img = img.cutoff(match[1].width)
        img.load()

    if img.width != 0:
        raise Exception("Not all characters where recognized.")

    return characters_found

img = CustomImage(Image.open("cedd.45ffa7e9a450.png"))
characters_found = match_characters(img)

if characters_found.find("EUR") != -1:
    price = float(characters_found[:characters_found.find("EUR")])

    print price
