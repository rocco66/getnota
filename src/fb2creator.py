'''
Created on 31.08.2011

@author: max
'''

import lxml.etree
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
        self.name = name
        self.data = []
        
    def add_data(self, data):
        '''
        Add text data for writing in fb2 book.
        '''
        self.data.append(data)
        
    def create(self):
        '''
        Create fb2 file.
        '''
        try:
            self.file = open(self.name + '.fb2', mode='w')
            self.__write_header()
            for d in self.data:
                self.__write_data(d)
        finally:
            self.file.close()
        return self.__isValid()
        
    def __write_data(self, data):
        '''
        Write text data from data to fb2 file.
        '''
        pass
             
    def __write_header(self):
        '''
        Write header to fb2 file.
        '''
        pass
    
    def __isValid(self):
        '''
        Retur True if created fb2 is valid.
        '''
        """
        f = StringIO('''\
... <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
... <xsd:element name="a" type="AType"/>
... <xsd:complexType name="AType">
...   <xsd:sequence>
...     <xsd:element name="b" type="xsd:string" />
...   </xsd:sequence>
... </xsd:complexType>
... </xsd:schema>
... ''')
>>> xmlschema_doc = etree.parse(f)
>>> xmlschema = etree.XMLSchema(xmlschema_doc)

>>> valid = StringIO('<a><b></b></a>')
>>> doc = etree.parse(valid)
>>> xmlschema.validate(doc)
True
        """