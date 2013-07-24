# -*- coding: utf-8 -*-

import http
import re
import os, sys
import lxml.html
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

def login():
    config = loads(open("conf.json", "r").read())
    user = config["Username"]
    password = config["Password"]
    http.jar.clear_expired_cookies()
    if any(cookie.domain == 'forums.somethingawful.com' and cookie.name == 'bbuserid' for cookie in http.jar):
        if any(cookie.domain == 'forums.somethingawful.com' and cookie.name == 'bbpassword' for cookie in http.jar):
            return
        assert("malformed cookie jar")
    http.get("http://forums.somethingawful.com/account.php", cookies=True, post_data="action=login&username=%s&password=%s" % (user, password))

def get_thread(thread_id):
    login()

### THREAD INFORMATION START ###

    thread_url = "http://forums.somethingawful.com/showthread.php?threadid=%s" % thread_id
    content = http.get_html(thread_url, cookies=True)
    content = clean_html(content)

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
            'locked'      : locked,
            'op'          : original_poster,
            'pages'       : pages,
            'url'         : thread_url
           }

### THREAD INFORMATION END ###

### POST INFORMATION START ###

    new_urls = "http://forums.somethingawful.com/showthread.php?threadid=%s&pagenumber=%d"

    post_list   = []
    id_list     = []
    author_list = []
    reg_list    = []
    date_list   = []
    post_dicts  = []
    post_number = 1

    for j in pages:
        print_r("At page #%d out of #%03d" % (j, pages[-1]))
        
        k = new_urls % (thread_id, j)
        content_from_posts = http.get_html(k, cookies=True)

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

### POST INFORMATION END ###

def create_xml(info, post_data):
    thread_element = http.etree.Element("thread", id="%s" % info['thread_id'])

    doc = http.etree.ElementTree(thread_element)
    root = doc.getroot()
    root.addprevious(http.etree.PI('xml-stylesheet', 'type="text/xsl" href="sheet.xsl"'))

    breadcrumbs_element = http.etree.Element("breadcrumbs")
    thread_element.append(breadcrumbs_element)

    forum_element = http.etree.Element("forum")
    forum_element.text = "%s" % info['forum']
    breadcrumbs_element.append(forum_element)

    board_element = http.etree.Element("board")
    board_element.text = "%s" % info['board']
    breadcrumbs_element.append(board_element)

    subboard_element = http.etree.Element("subboard")
    subboard_element.text = "%s" % info['subboard']
    breadcrumbs_element.append(subboard_element)

    if len(info) == 10:
        subsubboard_element = http.etree.Element("subsubboard")
        subsubboard_element.text = "%s" % info['subsubboard']
        breadcrumbs_element.append(subsubboard_element)

    title_element = http.etree.Element("title")
    title_element.text = "%s" % info['title']
    breadcrumbs_element.append(title_element)

    locked_element = http.etree.Element("locked")
    locked_element.text = "%s" % info['locked']
    thread_element.append(locked_element)

    pages_element = http.etree.Element("pages")
    pages_element.text = "%d" % info['pages'][-1]
    thread_element.append(pages_element)

    url_element = http.etree.Element("url")
    url_element.text = "%s" % info['url']
    thread_element.append(url_element)

    posts_element = http.etree.Element("posts")
    thread_element.append(posts_element)

    for i in range(0, len(post_data)):
        post_element         = http.etree.Element("post", id="%s" % post_data[i]["post_id"])
        posts_element.append(post_element)

        number_element       = http.etree.Element("number")
        number_element.text  = "%d" % post_data[i]['post_number']
        post_element.append(number_element)

        page_element         = http.etree.Element("page")
        page_element.text    = "%s" % post_data[i]['post_page']
        post_element.append(page_element)

        author_element       = http.etree.Element("author")
        author_element.text  = "%s" % post_data[i]['post_author']
        post_element.append(author_element)

        regdate_element      = http.etree.Element("regdate")
        regdate_element.text = "%s" % post_data[i]['post_regdate']
        post_element.append(regdate_element)

        date_element         = http.etree.Element("date")
        date_element.text    = "%s" % post_data[i]['post_date']
        post_element.append(date_element)

        content_text         = str(post_data[i]['post_content']).encode('ascii', 'ignore').replace('&#13;', '')
        content_element      = http.etree.Element("content")
        content_element.text = http.etree.CDATA(content_text)
        post_element.append(content_element)


    file_title = ''.join([x for x in info['title'] if x.isalpha() or x.isdigit() or x is ' '])
    out        = open("output\%s.xml" % file_title, "w")
    doc.write(out, xml_declaration=True, encoding='utf-8', pretty_print=True)
    print '\nDone.'

def main():
    parser = argparse.ArgumentParser(description='Data mine a vBulletin thread,' \
            ' specifically made for SomethingAwful.')
    parser.add_argument('-tid', '--threadid', action='store',
            dest='thread_id', default=None, type=str, help='Set thread id.')
    parser.add_argument('-t', '--threadurl', action='store', dest='thread_url',
            default=None, type=str, help='Set thread url.')
    args = parser.parse_args()
    thread_id = args.thread_id
    thread_url = args.thread_url

    try:
        os.mkdir("output")
    except WindowsError:
        pass

    if thread_id is not None and thread_url is None:
        info, post_data = get_thread(thread_id)
        create_xml(info, post_data)
    if thread_id is None and thread_url is not None:
        thread_id = re.search('(?<=threadid=)\w+', thread_url).group()
        info, post_data = get_thread(thread_id)
        create_xml(info, post_data)

if __name__ == '__main__':
    main()

