# -*- coding: utf-8 -*-
'''
Created on 31.08.2011

@author: max
'''

from lxml import etree
import lxml.html
import os


class FB2Creator():
    '''
    Class for FB2 creation.
    '''

    book_dir = 'books'
    scheme = 'docs/FictionBook2.xsd'

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name + '.fb2'
        self.book_name = FB2Creator.book_dir + '/' + self.name
        if not os.path.exists(self.book_dir):
            os.mkdir(self.book_dir)
        self.eoc_sym = None 
        self.gen = None
        self.root = etree.Element('FictionBook')
        self.root.set("xmlns", "http://www.gribuser.ru/xml/fictionbook/2.0") 
        
    def set_end_of_chapter_symbol(self, symbol):
        self.eoc_sym = symbol
        
    def create_file(self):
        '''
        Create fb2 file.
        '''
        self.__create_header()
        self.__create_data()
        self.__write_etree()        
        return self.__isValid()
    
    def set_generator(self, gen):
        self.gen = gen
        
    def set_notifier(self, n):
        self.notifier = n    
    
    def get_file_name(self):
        return self.book_name
    
    def __write_etree(self):
        '''
        Write xml to fb2 file.
        '''
        et = etree.ElementTree(self.root)
        et.write(self.book_name,
                 xml_declaration=True,
                 encoding='utf-8')
        return True
         
        
    def __create_data(self):
        '''
        Create text data from data for fb2.
        '''
        body = etree.SubElement(self.root, 'body')
        title = etree.SubElement(body, 'title')
        etree.SubElement(title, 'p').text = self.name.split('.')[0]
        section = etree.SubElement(body, 'section')
        s = etree.SubElement(section, 'section')
        chap_name = None
        for d in self.gen:
            if d == self.eoc_sym:
                s = etree.SubElement(section, 'section')
                chap_name = None
                self.notifier('chapter')
            else:
                etree.SubElement(s, 'p').text = d
                if not chap_name:
                    chap_name = d
#                    TODO Вставить названия глав для оглавления.
#                    etree.SubElement(s, 'title').text = '<p>' + chap_name + '</p>' 
        
             
    def __create_header(self):
        '''
        Create header for fb2.
        '''
        desc = etree.SubElement(self.root, 'description')
        #title-info
        ti = etree.SubElement(desc, 'title-info')
        etree.SubElement(ti, 'genre').text = 'literature_books'
        author = etree.SubElement(ti, 'author')
        etree.SubElement(author, 'first-name').text = 'Максим'
        etree.SubElement(author, 'last-name').text = 'Митрошин'
        etree.SubElement(ti, 'book-title').text = 'Танцы с драконами'
        etree.SubElement(ti, 'lang').text = 'ru'
        #document-info
        di = etree.SubElement(desc, 'document-info')
        author = etree.SubElement(di, 'author')
        etree.SubElement(author, 'nickname').text = 'rocco66'
        etree.SubElement(di, 'date',
                         value='2002-10-15').text = '15 ноября 2002г., 19:53'
        etree.SubElement(di, 'id').text = 'SuperID'
        etree.SubElement(di, 'version').text = '1.0'
        #publish-info
        pi = etree.SubElement(desc, 'publish-info') 
        
    
    def __isValid(self):
        '''
        Retur True if created fb2 is valid.
        '''
        xmlschema_doc = etree.parse(open(FB2Creator.scheme, mode='r'))
        xmlschema = etree.XMLSchema(xmlschema_doc)
        book = etree.parse(open(self.book_name, mode='r'))
        return xmlschema.validate(book)