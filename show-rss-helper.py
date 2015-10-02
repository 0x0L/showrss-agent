#!/usr/bin/env python

"""
    An OSX tool to automate downloads from showRSS
"""

from datetime import datetime
from dateutil import parser
from os import path, stat, utime
from pytz import utc
from subprocess import call
from urllib import urlencode
from urllib2 import build_opener
from xml.dom import minidom

CONFIGURATION = {
    # Show RSS user id
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

STAMP_FILE = path.join(path.expanduser("~"), '.show-rss')
RSS_FEED_URL = 'http://showrss.info/rss.php?' + urlencode(CONFIGURATION)


def update_timestamp():
    with open(STAMP_FILE, 'a'):
        utime(STAMP_FILE, None)

def get_timestamp():
    if not path.exists(STAMP_FILE):
        update_timestamp()
        return None
    modtime = stat(STAMP_FILE).st_mtime
    date = utc.localize(datetime.fromtimestamp(modtime))
    update_timestamp()
    return date


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


if __name__ == '__main__':
    timestamp = get_timestamp()
    feed = download_feed(RSS_FEED_URL)

    for date, link in parse_dates_links(feed):
        # print link, date
        if timestamp is None or date > timestamp:
            call(['open', '-g', link])
