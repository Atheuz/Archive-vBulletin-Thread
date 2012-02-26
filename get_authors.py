# -*- coding: utf-8 -*-

# Filename      get_authors.py
# Author        Lasse Vang Gravesen <gravesenlasse@gmail.com>
# First edited  22-02-2012 14:51
# Last edited   22-02-2012 15:01

import lxml.etree
import os
import argparse

def get_authors(filename):
    content = lxml.etree.fromstring(open(filename, "r").read())
    names = content.xpath('//author/text()')
    print "Total authors: %d, unique authors: %d" % (len(names), len(set(names)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='F', type=str, nargs='+', default=None,
            help='Set files to process')
    args = parser.parse_args()

    os.chdir("output")

    for i in args.filename:
        get_authors(i)

if __name__ == '__main__':
    main()
