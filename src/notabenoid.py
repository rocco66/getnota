'''
Created on 26.08.2011

@author: max
'''

from urllib import request
import lxml.html


class Notabenoid(object):
    '''
    classdocs
    '''

    NB_URL = 'http://notabenoid.com/book/'
    XPATH_BOOK_NAME = '/html/body/div/div[2]/div/div/div/h1'

    def __init__(self, id):
        '''
        Constructor
        '''
        self.id = id
        url = Notabenoid.NB_URL + id
        self.main_page = request.urlopen(url).read().decode()
        self.main_page = lxml.html.document_fromstring(self.main_page)
        
        
    def get_book_name(self):
        #сделать по id='Info'
        return self.main_page.xpath(Notabenoid.XPATH_BOOK_NAME)[0].text
        