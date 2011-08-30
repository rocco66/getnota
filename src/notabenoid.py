'''
Created on 26.08.2011

@author: max
'''

from urllib import request
from datetime import datetime
import lxml.html


class Notabenoid(object):
    '''
    Class for receiving book from notabenoid.com.
    '''

    NB_URL = 'http://notabenoid.com'
    BOOK_INFO_ID = 'Info'
    CHAP_LIST_ID = 'ChapList'
    CONTENT_ID = 'content'
    END_OF_CHAPTER = 'Переведено на сайте www.notabenoid.com'

    def __init__(self, book_id):
        '''
        Constructor
        id  - book id from notabenoid.com.
        '''
        self.id = book_id
        url = Notabenoid.NB_URL + '/book/' + book_id
        self.main_page = request.urlopen(url).read().decode()
        self.main_page = lxml.html.document_fromstring(self.main_page)
        info = self.main_page.get_element_by_id(Notabenoid.BOOK_INFO_ID)
        self.book_name = info.find('h1').text
        self.img_url = info.find('img').attrib['src']
        
        
    def get_book_name(self):
        '''
        Return book name.
        '''
        return self.book_name
    
    def get_book_img(self):
        '''
        Return book image url.
        '''
        return self.img_url
    
    def get_date(self):
        '''
        Return date of book receiving.
        '''
        return datetime.now()
    
    def chapters_links(self):
        '''
        Generator for chapter links.
        '''
        chap_table = self.main_page.get_element_by_id(Notabenoid.CHAP_LIST_ID)
        for tr in chap_table:
            res = tr.attrib.get('id')
            if res:
                td = tr[-1]
                a = td[0]
                yield a.attrib['href']
             
    def end_of_chapter(self):
        return None     
        
    def content(self):
        '''
        Generator for lines from book.
        '''
        for cl in self.chapters_links():
            url = Notabenoid.NB_URL + cl
            page = lxml.html.parse(url).getroot()
            form = page.forms[-1]
            page = lxml.html.parse(lxml.html.submit_form(form)).getroot()
            content = page.get_element_by_id(Notabenoid.CONTENT_ID)
            for p in content:
                if Notabenoid.END_OF_CHAPTER == p.text:
                    yield self.end_of_chapter()
                yield p.text

        
        