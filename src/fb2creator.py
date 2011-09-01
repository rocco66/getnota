'''
Created on 31.08.2011

@author: max
'''

from lxml import etree
import lxml.html


class FB2Creator():
    '''
    Class for FB2 creation.
    '''

    scheme = 'FictionBook2.xsd'

    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name + '.fb2'
        self.data = []
        self.root = etree.Element('FictionBook')
        self.root.set("xmlns", "http://www.gribuser.ru/xml/fictionbook/2.0") 
        
    def add_data(self, data):
        '''
        Add text data for writing in fb2 book.
        '''
        self.data.append(data)
        
    def create(self):
        '''
        Create fb2 file.
        '''
        self.__create_header()
        for d in self.data:
                self.__create_data(d)
        self.__write_etree()        
        return self.__isValid()
        
    def __write_etree(self):
        '''
        Write xml to fb2 file.
        '''
        et = etree.ElementTree(self.root)
        et.write(self.name,
                 xml_declaration=True,
                 encoding='utf-8')
        return True
         
        
    def __create_data(self, data):
        '''
        Create text data from data for fb2.
        '''
        body = etree.SubElement(self.root, 'body')
        #может еще надо применить тэг p к содержимому?
        title = etree.SubElement(body, 'title')
        etree.SubElement(title, 'p').text = self.name.split('.')[0]
        section = etree.SubElement(body, 'section')
        for d in self.data:
            s = etree.SubElement(section, 'section')
            etree.SubElement(s, 'p').text = d
        
             
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
        book = etree.parse(open(self.name, mode='r'))
        return xmlschema.validate(book)