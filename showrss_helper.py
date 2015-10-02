#!/usr/bin/env python
"""
An OSX tool to automate downloads from showRSS
"""

from time import mktime
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


def update_timestamp(date):
    with open(STAMP_FILE, 'a'):
        timetuple = mktime(date.timetuple())
        utime(STAMP_FILE, (timetuple, timetuple))


def get_timestamp():
    if not path.exists(STAMP_FILE):
        return datetime.fromordinal(1)
    modtime = stat(STAMP_FILE).st_mtime
    return datetime.fromtimestamp(modtime)


if __name__ == '__main__':
    timestamp = utc.localize(get_timestamp())
    all_shows = parse_dates_links(download_feed(RSS_FEED_URL))
    new_shows = filter(lambda x: x[0] > timestamp, all_shows)
    
    if new_shows:
        latest = max(new_shows, key=lambda x: x[0])[0]
        update_timestamp(latest)
        for _, link in new_shows:
            call(['open', '-g', link])
