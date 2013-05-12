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

import sys
import os
import json

from bs4 import BeautifulSoup

mapping = {
    1: "number",
    2: "product name",
    3: "date beginning",
    4: "date ending",
    5: "country",
    6: "package size",
    7: "ATC Code",
    8: "Route of administration",
    9: "Strength",
    10: "Unit",
    11: "Manufacturer price",
    12: "Wholesale price",
    13: "Net Retail price",
    14: "Gross Retail price",
    15: "Manufacturer price/unit of package",
    16: "Wholesale price/unit of package",
    17: "Net Retail price/unit of package",
    18: "Gross Retail price/unit of pacakge",
}

def get_page(data):
    b = BeautifulSoup(data)

    contents = b.find("div", {"id": "qm1", }).table

    rows = []

    for tr in contents:
        column = 1
        row = []
        for td in tr:
            if not td.has_key('class'):
                continue
            if 'hd1' in td['class'] or 'hd2' in td['class']:
                continue

#            if not 'cel1' in td['class'] and not 'cel2' in td['class']:
#                print td['class']

            if column in range(1, 10+1):
                row.append(td.getText())

            if column in [11, 12, 13, 14, 15, 16, 17, 18]:
                if td.getText() != '-':
                    row.append(td.img['src'])
                else:
                    row.append(None)

            column += 1
        rows.append(row)

    return rows

def print_usage():
    sys.exit("Usage: %s dir" % (sys.argv[0], ))

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print_usage()
        # NOTREACHED

    octrooi_dir = sys.argv[1]

    for filename in os.listdir(octrooi_dir):
        if not filename.endswith('.html'):
            continue

        filedescr = open(os.path.join(octrooi_dir, filename), 'r')
        file_data = filedescr.read()

        json_filename = filename + '.json'
        json_filedescr = open(os.path.join(octrooi_dir, json_filename), 'w')

        rows = get_page(file_data)

        json_filedescr.write(json.dumps(rows))
