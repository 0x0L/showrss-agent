#!/usr/bin/env python
"""
An OSX tool to automate downloads from showRSS
"""

from datetime import datetime
from os import path
from subprocess import call
from xml.dom import minidom
from urllib.request import build_opener


URL = """http://showrss.info/user/35118.rss?magnets=true&namespaces=true&name=clean&quality=null&re=no"""

STAMP_FILE = path.join(path.expanduser("~"), ".showrss")


def parse_date(date):
    return


def read_url(url):
    opener = build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    return opener.open(url, timeout=10).read()


def parse_feed(feed):
    get = minidom.parseString(feed).getElementsByTagName
    dates = (
        datetime.strptime(z.firstChild.nodeValue, "%a, %d %b %Y %H:%M:%S %z")
        for z in get("pubDate")
    )
    links = (z.firstChild.nodeValue for z in get("link")[1:])
    return zip(dates, links)


def get_timestamp():
    dt = "2000-01-01 00:00:00+00:00"
    if path.exists(STAMP_FILE):
        with open(STAMP_FILE, "r") as stamp_file:
            dt = stamp_file.read()
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S%z")


def write_timestamp(dt):
    with open(STAMP_FILE, "w") as stamp_file:
        stamp_file.write(str(dt))


if __name__ == "__main__":
    timestamp = get_timestamp()
    all_shows = parse_feed(read_url(URL))
    new_shows = [x for x in all_shows if x[0] > timestamp]

    for _, link in new_shows:
        call(["open", "-g", link])

    if new_shows:
        times, _ = zip(*new_shows)
        write_timestamp(max(times))
