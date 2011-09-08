# -*- coding: utf-8 -*-
'''
Created on 01.09.2011

@author: max
'''

from notabenoid import Notabenoid
from fb2creator import FB2Creator
import sys


class Notabenoid2FB2():
    '''
    Class for creation FB2 from Notabenoid.
    '''

    def __init__(self, book_id):
        '''
        Constructor
        '''
        self.nb = Notabenoid(book_id)
        name = self.nb.get_book_name()
        name = name.split('/')[0]
        name = name.strip()
        name = name.replace(' ', '_')
        name = name.lower()
        self.file_name = name 
        fb2 = FB2Creator(name)
        fb2.set_generator(self.nb.content())
        fb2.set_notifier(self.print_chapter)
        fb2.set_end_of_chapter_symbol(self.nb.end_of_chapter())
        self.fb2 = fb2
        self.current_chapter = 0
    
    def print_chapter(self, s):
        self.current_chapter += 1
        print(s + ' ' + str(self.current_chapter))
        
    def get_file_name(self):
        return self.fb2.get_file_name()
    
    def generate(self):
        self.fb2.create_file()
        
    def get_chapter_number(self):
        '''
        Return number of chapter in book.
        '''
        return self.nb.get_chapter_number()
    
    def set_notifier(self, n):
        self.fb2.set_notifier(n)
        
    
if __name__ == '__main__':
    n2fb2 = Notabenoid2FB2(sys.argv[1])
    n2fb2.generate()