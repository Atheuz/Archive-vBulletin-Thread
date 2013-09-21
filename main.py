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
from util import convenience

class SAThreadArchive(object):
    def __init__(self, thread_id, update=False):
        self.thread_id   = thread_id
        self.thread_url  = "http://forums.somethingawful.com/showthread.php?threadid=%s" % thread_id
        self.session     = requests.Session()
        self.update      = update
        self.config      = loads(open("conf.json", "r").read())
        
        self.breadcrumbs     = {"forum":None,
                                "board":None,
                                "subboard":None,
                                "subsubboard":None,
                                "title":None}
        self.locked          = None
        self.original_poster = None
        self.pages           = None
        self.file_title      = None
        self.post_number     = 1
        self.post_dicts      = []
        
        
    def get_thread(self):
        self.login()
        self.get_thread_information()
        
        if self.update:
            content      = lxml.etree.fromstring(open("output\%s.xml" % self.file_title, "r").read())
            last_post    = content.xpath('//post[position()=last()]')[0]
            self.get_post_information(continue_from=last_post)
        else:
            self.get_post_information()
        
    def login(self):
        """Login to SomethingAwful using details in the self.config variable"""
        payload = {"action": "login",
                   "username": self.config["Username"],
                   "password": self.config["Password"]}
        self.session.post("http://forums.somethingawful.com/account.php", data=payload)
        
    def get_thread_information(self):
        content = clean_html(lxml.html.fromstring(self.session.get(self.thread_url).text))
        breadcrumbs_tmp = [x.text_content() for x in content.xpath('///div[@class="breadcrumbs"][1]//span[@class="mainbodytextlarge"]//a')]
        if len(breadcrumbs_tmp) == 4:
            self.breadcrumbs["forum"], self.breadcrumbs["board"], self.breadcrumbs["subboard"], self.breadcrumbs["title"] = breadcrumbs_tmp
        elif len(breadcrumbs_tmp) == 5:
            self.breadcrumbs["forum"], self.breadcrumbs["board"], self.breadcrumbs["subboard"], self.breadcrumbs["subsubboard"], self.breadcrumbs["title"] = breadcrumbs_tmp
        

        self.locked = 'closed' in content.xpath('//ul[@class="postbuttons"]/li[2]/a/img/@src')[0]
        self.original_poster = content.xpath('//dt[contains(@class, "author")]')[0].text_content()
        try:
            self.pages = content.xpath('//div[@class="pages top"]/a[last()]')[0].text_content()
            self.pages = self.pages.encode('utf-8', 'ignore')
            self.pages = re.search("\d+", self.pages).group()
            self.pages = range(1,int(self.pages)+1)
        except (AttributeError, IndexError):
            self.pages = [1]
        self.file_title = ''.join([x for x in self.breadcrumbs["title"] if x.isalpha() or x.isdigit() or x is ' '])
        
    def get_post_information(self, continue_from=None):
        page_url = "http://forums.somethingawful.com/showthread.php?threadid=%s&pagenumber=%d"
        
        post_list   = []
        id_list     = []
        author_list = []
        reg_list    = []
        date_list   = []
        
        if continue_from is not None:
            print "Updating from page %s, post id %s" % (continue_from.xpath('./@post_thread_page')[0], continue_from.xpath('./@post_id')[0])
            self.pages = self.pages[self.pages.index(int(continue_from.xpath('./@post_thread_page')[0])):]
        
        for p in self.pages:
            convenience.print_r("At page #%d out of #%03d" % (p, self.pages[-1]))
            current_url = page_url % (self.thread_id, p)
            content_from_posts = lxml.html.fromstring(self.session.get(current_url).text)
            for pb in content_from_posts.xpath('//td[@class="postbody"]'):
                result = ' '.join(self.clean_post(pb).split())
                post_list.append(result)
            id_list     = [re.search('(?<=#post)\w+', x).group()                  for x in content_from_posts.xpath('//td[@class="postdate"]/a[1]/@href')]
            author_list = [x.text_content().strip()                               for x in content_from_posts.xpath('//dl[@class="userinfo"]/dt')]
            date_list   = [re.search('\w{3}.+', x.text_content().strip()).group() for x in content_from_posts.xpath('//td[@class="postdate"]')]
            reg_list    = [x.text_content().strip()                               for x in content_from_posts.xpath('//dl[@class="userinfo"]/dd[@class="registered"]')]
            
            for i in range(0, len(post_list)):
                self.post_dicts.append({'post_content' :  post_list[i],
                                   'post_id'      :  id_list[i],
                                   'post_author'  :  author_list[i],
                                   'post_regdate' :  reg_list[i],
                                   'post_date'    :  date_list[i],
                                   'post_page'    :  p,
                                   'post_number'  :  self.post_number
                                  })
                self.post_number += 1
                
            post_list   = []
            id_list     = []
            author_list = []
            reg_list    = []
            date_list   = []

    def clean_post(self, p):
        cleaner      = Cleaner(style=True, comments=True, scripts=True,
                               javascript=True, page_structure=True, links=True)
        p            = cleaner.clean_html(p)
        current_post = lxml.html.tostring(p)
        current_post = current_post.strip() \
                                   .encode('ascii', 'ignore') \
                                   .replace('\n', ' ') \
                                   .replace('\r', ' ') \
                                   .replace('\x00', '') \
                                   .replace('<td class="postbody">','') \
                                   .replace('</td>','') \
                                   .strip()
        return current_post
    
    def create_xml(self):
        if self.update:
            parser = lxml.etree.XMLParser(remove_blank_text=True)
            thread_content = lxml.etree.parse("output\%s.xml" % self.file_title, parser)
            last_post = thread_content.xpath('//post[position()=last()]')[0]
            post_data = [self.create_post_xml(x) for x in self.post_dicts if x["post_number"] > int(last_post.xpath('./@post_thread_number')[0])]
            posts = thread_content.xpath('//posts')[0]
            for i in post_data:
                posts.append(i)
            out = open("output\%s.xml" % self.file_title, "w")
            thread_content.write(out, xml_declaration=True, encoding='utf-8', pretty_print=True)
        else:
            thread_element = lxml.etree.Element("thread", thread_id         = "%s" % self.thread_id,
                                                          thread_locked     = "%s" % self.locked,
                                                          thread_page_count = "%d" % self.pages[-1],
                                                          thread_url        = "%s" % self.thread_url)
            doc = lxml.etree.ElementTree(thread_element)
            root = doc.getroot()
            root.addprevious(lxml.etree.PI('xml-stylesheet', 'type="text/xsl" href="sheet.xsl"'))
            breadcrumbs_element = lxml.etree.Element("breadcrumbs", thread_forum       = "%s" % self.breadcrumbs['forum'],
                                                                    thread_board       = "%s" % self.breadcrumbs['board'],
                                                                    thread_subboard    = "%s" % self.breadcrumbs['subboard'],
                                                                    thread_subsubboard = "%s" % self.breadcrumbs['subsubboard'],
                                                                    thread_title       = "%s" % self.breadcrumbs['title'])
            thread_element.append(breadcrumbs_element)
            
            posts_element = lxml.etree.Element("posts")
            thread_element.append(posts_element)
            
            for p in self.post_dicts:
                post_element = self.create_post_xml(p)
                posts_element.append(post_element)
            out = open("output\%s.xml" % self.file_title, "w")
            doc.write(out, xml_declaration=True, encoding='utf-8', pretty_print=True)
        print '\nDone.'
        
        
    def create_post_xml(self, post):
        p = lxml.etree.Element("post", post_id             = "%s" % post["post_id"],
                                       post_thread_number  = "%d" % post['post_number'],
                                       post_thread_page    = "%d" % post['post_page'],
                                       post_author         = "%s" % post['post_author'],
                                       post_author_regdate = "%s" % post['post_regdate'],
                                       post_date           = "%s" % post['post_date'])
        content_text         = str(post['post_content']).encode('ascii', 'ignore').replace('&#13;', '')
        content_element      = lxml.etree.Element("content")
        content_element.text = lxml.etree.CDATA(content_text)
        p.append(content_element)
        return p

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
    archive = SAThreadArchive(input_id, update=args.update)
    archive.get_thread()
    archive.create_xml()

if __name__ == '__main__':
    main()

