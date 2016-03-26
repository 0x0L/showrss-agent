#!/usr/bin/env python
"""
An OSX tool to automate downloads from showRSS
"""

from dateutil import parser
from os import path
from subprocess import call
from xml.dom import minidom

try:
    from urllib2 import build_opener
except ImportError:
    from urllib.request import build_opener


RSS_FEED_URL = """FEED_URL_CONFIG"""

STAMP_FILE = path.join(path.expanduser("~"), '.showrss')


def read_url(url):
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(url, timeout=10).read()


def parse_feed(feed):
    get = minidom.parseString(feed).getElementsByTagName
    dates = (parser.parse(z.firstChild.nodeValue) for z in get('pubDate'))
    links = (z.firstChild.nodeValue for z in get('link')[1:])
    return zip(dates, links)


def get_timestamp():
    dt = '2000-01-01 00:00:00+00:00'
    if path.exists(STAMP_FILE):
        with open(STAMP_FILE, 'r') as stamp_file:
            dt = stamp_file.read()
    return parser.parse(dt)


def write_timestamp(dt):
    with open(STAMP_FILE, 'w') as stamp_file:
        stamp_file.write(str(dt))


if __name__ == '__main__':
    timestamp = get_timestamp()
    all_shows = parse_feed(read_url(RSS_FEED_URL))
    new_shows = [x for x in all_shows if x[0] > timestamp]

    for _, link in new_shows:
        call(['open', '-g', link])

    if new_shows:
        times, _ = zip(*new_shows)
        write_timestamp(max(times))
