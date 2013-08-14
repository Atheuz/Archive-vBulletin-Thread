# -*- coding: utf-8 -*-

# Filename      get_authors.py
# Author        Lasse Vang Gravesen <gravesenlasse@gmail.com>
# First edited  22-02-2012 14:51
# Last edited   22-02-2012 15:01

import lxml.etree
import os
from collections import Counter
import argparse

def get_authors(filename):
    content = lxml.etree.fromstring(open(filename, "r").read())
    names = content.xpath('//author/text()')
    print "Total authors: %d, unique authors: %d" % (len(names), len(set(names)))

def get_regdates(filename):
    content = lxml.etree.fromstring(open(filename, "r").read())
    names = content.xpath('//author/text()')
    dates = content.xpath('//regdate/text()')
    com = set(zip(names,dates))
    dates = [x[1] for x in com]
    years = [int(x[-4::]) for x in dates]
    #print sorted(years, key=lambda x: x)
    s = 0
    for i in Counter(years).most_common(10):
        print i[0],i[1]
        s += i[1]
    #print "Total: %d" % s

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='F', type=str, nargs='+', default=None,
            help='Set files to process')
    args = parser.parse_args()

    os.chdir("output")

    for i in args.filename:
        get_authors(i)
        get_regdates(i)

if __name__ == '__main__':
    main()
