'''
Created on 01.09.2011

@author: max
'''

from notabenoid import Notabenoid
from fb2creator import FB2Creator
import sys


class Notabenoid2FB2():
    '''
    Class for creation FB2 from Motabenoid.
    '''

    def __init__(self, book_id):
        '''
        Constructor
        '''
        nb = Notabenoid(book_id)
        name = nb.get_book_name()
        name = name.split('/')[0]
        name = name.strip()
        name = name.replace(' ', '_')
        name = name.lower()
        fb2 = FB2Creator(name)
        fb2.set_generator(nb.content())
        fb2.set_notifier(self.print_chapter)
        fb2.set_end_of_chapter_symbol(nb.end_of_chapter())
        fb2.create_file()
    
    def print_chapter(self, s):
        print(s)
    
    
if __name__ == '__main__':
    n2fb2 = Notabenoid2FB2(sys.argv[1])