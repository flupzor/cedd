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

# http://cedd.oep.hu/images/tmp-res/cedd.e80bee5403bd.png

import urllib
import json
import sys
import os
import time

def imagelist(path):
    rows = json.loads(open(path, "r").read())

    image_list = set()

    for row in rows:
        if len(row) == 0:
            continue
        for column in[11, 12, 13, 14, 15, 16, 17, 18]:
            image_list.add(row[column-1])

    return image_list

def print_usage():
    sys.exit("Usage: %s dir" % (sys.argv[0], ))

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print_usage()
        # NOTREACHED

    cedd_dir = sys.argv[1]

    image_list = set()

    for filename in os.listdir(cedd_dir):
        if not filename.endswith('.json'):
            continue

        image_list.update(imagelist(os.path.join(cedd_dir, filename)))

    i = 0
    for filename in image_list:
        if filename == None:
            continue
        url = "http://cedd.oep.hu" + filename[1:]
        to_filename = filename.replace('./images/tmp-res/', 'cedd_img/')

        if os.path.exists(to_filename):
            print "skipping %d" % i
            i += 1
            continue

        urllib.urlretrieve(url, to_filename)
        print "%d of %d (%d%%)" % (i, len(image_list), i*1.0/len(image_list))
        i += 1
        time.sleep(0.5)
