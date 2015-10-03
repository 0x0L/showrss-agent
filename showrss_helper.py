#!/usr/bin/env python
"""
An OSX tool to automate downloads from showRSS
"""

from dateutil import parser
from os import path
from subprocess import call
from xml.dom import minidom

try:
    from urllib import urlencode
    from urllib2 import build_opener
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import build_opener

CONFIGURATION = {
    # Show RSS user id
    # 'user_id': 17065,
    'user_id': USER_ID,

    # 'null'  Per show settings,
    # 0       Only standard torrents,
    # 1       Only 720p HD
    # 2       Both types of torrents
    'hd': 'null',

    # 'null'  Per show settings,
    # 0       Skip proper/repack
    # 1       Include proper/repack
    'proper': 'null',

    # Uncomment this line to use torrent files instead of the magnet protocol
    # 'magnets': 'false',

    # For reference
    # 'namespaces': 'false',
    # 'raw': 'false',
}

STAMP_FILE = path.join(path.expanduser("~"), '.showrss')
RSS_FEED_URL = 'http://showrss.info/rss.php?' + urlencode(CONFIGURATION)


def download_feed(url):
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(url, timeout=10).read()


def parse_dates_links(feed):
    xml = minidom.parseString(feed)

    links = [z.firstChild.nodeValue
             for z in xml.getElementsByTagName('link')[1:]]

    dates = [parser.parse(z.firstChild.nodeValue)
             for z in xml.getElementsByTagName('pubDate')]

    assert(len(links) == len(dates))
    return zip(dates, links)


def get_timestamp():
    dt = '2000-01-01 00:00:00+00:00'
    if path.exists(STAMP_FILE):
        with open(STAMP_FILE, 'r') as stamp_file:
            dt = stamp_file.read()
    return parser.parse(dt)


if __name__ == '__main__':
    timestamp = get_timestamp()
    all_shows = parse_dates_links(download_feed(RSS_FEED_URL))
    new_shows = list(filter(lambda x: x[0] > timestamp, all_shows))

    if new_shows:
        latest_dt = max(new_shows, key=lambda x: x[0])[0]
        with open(STAMP_FILE, 'w') as stamp_file:
            stamp_file.write(str(latest_dt))

        for _, link in new_shows:
            call(['open', '-g', link])
