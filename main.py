# -*- coding: utf-8 -*-

import requests
import re
import os, sys
import lxml.html
import lxml.etree
from lxml.html.clean import clean_html
from lxml.html.clean import Cleaner
from json import loads
from StringIO import StringIO
import argparse

# Convenience functions.

html_escape_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
    '"': "&quot;"
}

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def print_r(s):
    sys.stdout.write("%s \r" % (" " * 50))
    sys.stdout.write("%s \r" % s)
    sys.stdout.flush()
    
def get_html(session, url):
    return lxml.html.fromstring(session.get(url).text)

def login(session):
    config = loads(open("conf.json", "r").read())
    payload = {"action":"login", "username":config["Username"], "password":config["Password"]}
    session.post("http://forums.somethingawful.com/account.php", data=payload)
    
def get_thread_information(session, thread_id):
    thread_url = "http://forums.somethingawful.com/showthread.php?threadid=%s" % thread_id
    content = clean_html( get_html(session, thread_url) )

    breadcrumbs = content.xpath('///div[@class="breadcrumbs"][1]//span[@class="mainbodytextlarge"]//a')
    if len(breadcrumbs) == 4:
        forum, board, subboard, title = [x.text_content() for x in breadcrumbs]
        subsubboard = None
    elif len(breadcrumbs) == 5:
        forum, board, subboard, subsubboard, title = [x.text_content() for x in breadcrumbs]

    locked = 'closed' in content.xpath('//ul[@class="postbuttons"]/li[2]/a/img/@src')[0]

    original_poster = content.xpath('//dt[contains(@class, "author")]')[0].text_content()

    try:
        pages = content.xpath('//div[@class="pages top"]/a[last()]')[0].text_content()
        pages = pages.encode('utf-8', 'ignore')
        pages = re.search("\d+", pages).group()
        pages = range(1,int(pages)+1)
    except (AttributeError, IndexError):
        pages = [1]

    data = {'thread_id'   : thread_id,
            'forum'       : forum,
            'board'       : board,
            'subboard'    : subboard,
            'subsubboard' : subsubboard,
            'title'       : title,
            'file_title'  : ''.join([x for x in title if x.isalpha() or x.isdigit() or x is ' ']),
            'locked'      : locked,
            'op'          : original_poster,
            'pages'       : pages,
            'url'         : thread_url
           }
    
    return pages, data
    
def get_post_information(session, thread_id, pages, data):
    new_url = "http://forums.somethingawful.com/showthread.php?threadid=%s&pagenumber=%d"

    post_list   = []
    id_list     = []
    author_list = []
    reg_list    = []
    date_list   = []
    post_dicts  = []
    post_number = 1

    for j in pages:
        print_r("At page #%d out of #%03d" % (j, pages[-1]))
        
        k = new_url % (thread_id, j)
        content_from_posts = get_html(session, k)

        for i in content_from_posts.xpath('//td[@class="postbody"]'):
            cleaner      = Cleaner(style=True, comments=True, scripts=True,
                                   javascript=True, page_structure=True, links=True)
            i            = cleaner.clean_html(i)
            current_post = lxml.html.tostring(i)
            current_post = current_post.strip() \
                                       .encode('ascii', 'ignore') \
                                       .replace('\n', ' ') \
                                       .replace('\r', ' ') \
                                       .replace('\x00', '') \
                                       .replace('<td class="postbody">','') \
                                       .replace('</td>','') \
                                       .strip()
            result       = ' '.join(current_post.split())

            post_list.append(result)

        id_list     = [re.search('(?<=#post)\w+', x).group()                  for x in content_from_posts.xpath('//td[@class="postdate"]/a[1]/@href')]
        author_list = [x.text_content().strip()                               for x in content_from_posts.xpath('//dl[@class="userinfo"]/dt')]
        date_list   = [re.search('\w{3}.+', x.text_content().strip()).group() for x in content_from_posts.xpath('//td[@class="postdate"]')]
        reg_list    = [x.text_content().strip()                               for x in content_from_posts.xpath('//dl[@class="userinfo"]/dd[@class="registered"]')]


        for i in range(0, len(post_list)):
            post_dicts.append({'post_content' :  post_list[i],
                               'post_id'      :  id_list[i],
                               'post_author'  :  author_list[i],
                               'post_regdate' :  reg_list[i],
                               'post_date'    :  date_list[i],
                               'post_page'    :  j,
                               'post_number'  :  post_number
                              })
            post_number += 1

        post_list   = []
        id_list     = []
        author_list = []
        reg_list    = []
        date_list   = []
        
    return data, post_dicts

def get_thread(thread_id, update=False):
    session = requests.Session()
    login(session)

    pages, data = get_thread_information(session, thread_id)
    
    if update:
        content = lxml.etree.fromstring(open("output\%s.xml" % data["file_title"], "r").read())
        last_post    = content.xpath('//post[position()=last()]/@post_thread_page')[0]
        last_post_id = content.xpath('//post[position()=last()]/@post_id')[0]
        #print last_post, last_post_id
    return get_post_information(session, thread_id, pages, data)

def create_xml(info, post_data):
    thread_element = lxml.etree.Element("thread", thread_id         = "%s" % info['thread_id'],
                                                  thread_locked     = "%s" % info['locked'],
                                                  thread_page_count = "%d" % info['pages'][-1],
                                                  thread_url        = "%s" % info['url'])

    doc = lxml.etree.ElementTree(thread_element)
    root = doc.getroot()
    root.addprevious(lxml.etree.PI('xml-stylesheet', 'type="text/xsl" href="sheet.xsl"'))

    breadcrumbs_element = lxml.etree.Element("breadcrumbs", thread_forum       = "%s" % info['forum'],
                                                            thread_board       = "%s" % info['board'],
                                                            thread_subboard    = "%s" % info['subboard'],
                                                            thread_subsubboard = "%s" % info['subsubboard'],
                                                            thread_title       = "%s" % info['title'])
    thread_element.append(breadcrumbs_element)

    posts_element = lxml.etree.Element("posts")
    thread_element.append(posts_element)

    for i in range(0, len(post_data)):
        post_element         = lxml.etree.Element("post", post_id             = "%s" % post_data[i]["post_id"],
                                                          post_thread_number  = "%d" % post_data[i]['post_number'],
                                                          post_thread_page    = "%d" % post_data[i]['post_page'],
                                                          post_author         = "%s" % post_data[i]['post_author'],
                                                          post_author_regdate = "%s" % post_data[i]['post_regdate'],
                                                          post_date           = "%s" % post_data[i]['post_date'])
        posts_element.append(post_element)

        content_text         = str(post_data[i]['post_content']).encode('ascii', 'ignore').replace('&#13;', '')
        content_element      = lxml.etree.Element("content")
        content_element.text = lxml.etree.CDATA(content_text)
        post_element.append(content_element)

    out        = open("output\%s.xml" % info['file_title'], "w")
    doc.write(out, xml_declaration=True, encoding='utf-8', pretty_print=True)
    print '\nDone.'

def main():
    parser = argparse.ArgumentParser(description='Data mine a vBulletin thread,' \
            ' specifically made for SomethingAwful.')
    thread_group = parser.add_mutually_exclusive_group()
    thread_group.add_argument('-tid', '--threadid', action='store',
            dest='thread_id', default=None, type=str, help='Set thread id.')
    thread_group.add_argument('-t', '--threadurl', action='store', dest='thread_url',
            default=None, type=str, help='Set thread url.')
    parser.add_argument('-u', '--update', action='store_true', dest='update', 
            default=False, help='Set to update')
    args = parser.parse_args()

    try:
        os.mkdir("output")
    except WindowsError:
        pass
        
    input_id = args.thread_id if args.thread_id else re.search('(?<=threadid=)\w+', args.thread_url).group()

    info, post_data = get_thread(input_id, update=args.update)
    create_xml(info, post_data)

if __name__ == '__main__':
    main()

