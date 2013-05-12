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

import mechanize
import time
import urllib
from urlparse import urlparse, parse_qs, urlunparse

countries = {
    "AT": "AUSTRIA",
    "CZ": "CZECH REPUBLIC",
    "FI": "FINLAND",
    "HU": "HUNGARY",
    "IE": "IRELAND",
    "LV": "LATVIA",
    "LT": "LITHUANIA",
    "NO": "NORWAY",
    "PL": "POLAND",
    "SK": "SLOVAKIA",
    "SI": "SLOVENIA",
}

def build_url(path, query):
    return path + '?' + query

def retrieve_country(country):
    br = mechanize.Browser()
    # Fuck robots.txt. Yes, we're fuckin' rebels.
    br.set_handle_robots(False)

    # The order of the querystring matters. That's why we can't use a
    # dictionary.
    params = (
        ('s', 'drug-database'),
        ('mode', 'country'),
        ('actualcountry', country),
        # We request all data (i.e. medicine prefixed with "all" characters)
        ('%s_currentletter' % (country,), 'all'),
        # Divide into pages of 60 items.
        ('pages', '60')
    )

    querystring = '&'.join(["%s=%s" % i for i in params])
    url = 'http://cedd.oep.hu/content.php?' + querystring

    print "Opening url: %s" % (url, )

    resp = br.open(url)
    data = resp.read()

    # Redirect, if needed.
    if data.find("The requested dataset is empty."):
        redirect_link = None
        for link in br.links():
            if link.url.startswith("./drugs.tib?s=drug-database&mode=country&actualcountry="):
                redirect_link = link
                break

        resp = br.follow_link(redirect_link)
        data = resp.read()

    # Make sure all columns are printed.
    milliseconds_since_epoch = int(time.time() * 1000)

    ajax_req = (
        ('xjxfun', 'applycols'),
        ('xjxr', str(milliseconds_since_epoch)),
        ('xjxargs[]', '<![CDATA[true|true|true|true|true|true|true|true|true|true|true|true|true|true|true|true|true|true|]]>')
    )

    # XXX: use the same function as above.
    data = urllib.urlencode(ajax_req)

    r = br.open("/drugs.tib?s=drug-database&mode=country&f=cedddrug1&portallang=en", data)

    br.back()

    # Find all pages.

    for link in br.links(text=">>|"):
        page = last_page = urlparse(link.url)
        break;

    # XXX: do a shallow copy.
    page_qs = last_page_qs = parse_qs(last_page.query)
    last_page_nr = int(last_page_qs['opage'][0])

    for page_nr in range(1, last_page_nr+1):
        page_qs['opage'][0] = str(page_nr)

        querystring = '&'.join(["%s=%s" % (key, value[0]) for key, value in page_qs.items()])

        resp = br.open(build_url(page.path, querystring))
        data = resp.read()

        filename = "cedd_files/%s_%s.html" % (country, str(page_nr),)
        print "Writing: %s" % filename
        f = open(filename, "w")
        f.write(data)

if __name__ == "__main__":
    for country in countries:
        retrieve_country(country)
