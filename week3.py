#!usr/bin/env python
# -*- coding: utf-8 -*-
"""Regular Expressions Module"""

import argparse
import urllib2
import csv
import re


def download_data(url):
    """This function download url.
    Args:
        url (str): A string.
    Returns:
        CSV File.
    """
    c_data = urllib2.urlopen(url)
    return c_data


def process_data(content):
    """This function call data.
    Args:
        counts (dict): Count of images and site hits.
        browsers (dict): Browsers and hit times.
    Returns:
        None
    """
    counter = {'imagehit':0,
              'rowcount':0}

    browsers = {'Internet Explorer':0,
                'Firefox':0,
                'Google Chrome':0,
                'Safari':0}

    for row in csv.reader(content):
        counts['rowcount'] += 1
        if r_search(r"jpe?g|JPE?G|GIF|PNG|gif|png", row[0]):
            counter['imagehit'] += 1
        if r_search("MSIE", row[2]):
            browsers['Internet Explorer'] += 1
        elif r_search("Chrome", row[2]):
            browsers['Google Chrome'] += 1
        elif r_search("firefox", row[2], r_I):
            browsers['Firefox'] += 1
        elif r_search("Safari", row[2]) and not r_search("Chrome", row[2]):
            browsers['Safari'] += 1

    image_cal = (float(counts['imagehit'])/ counts['rowcount']) * 100
    top_browsed = [max(b for b in browsers.items())]
    resultname = top_browsed[0][0]
    resultnum = top_browsed[0][1]

    report = ("There's a total of {} page hits today.\n"
              "Images account for {} % percent of all requests.\n"
              "{} is browser top used with {} hits.").format(counts['rowcount'],
                                                             image_cal,
                                                             resultname,
                                                             resultnum)
    print report


def main():
    """
    Args:
        parser (class): Argument parser instance for terminal use.
        args (class): Argument Instance for terminal use.
    Returns:
        None
    Examples:
        >>> main()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="Enter URL Link to CSV File")
    args = parser.parse_args()

    if args.url:
        try:
            inf = download_data(args.url)
            process_data(inf)
        except urllib2.URLError as url_err:
            print 'URL is INVALID'
            raise url_err
    else:
        print 'Please enter a valid URL.'

if __name__ == '__main__':
    main()
