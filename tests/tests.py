'''
Created on 26.08.2011

@author: max
'''
import unittest
from notabenoid import Notabenoid


class Test(unittest.TestCase):

    def testGetBookInfoByID(self):
        nb = Notabenoid('19980')
        self.assertEqual(nb.get_book_name(), 
                         'A DANCE WITH DRAGONS / ТАНЕЦ С ДРАКОНАМИ',
                         'wrong book name receive')
        self.assertEqual(nb.get_book_img(), 
                         'http://notabenoid.com/i//book/1/19980-45199.jpg',
                         'wrong book image url receive')
        
    def testGetChapter(self):
        nb = Notabenoid('19980')
        gen = nb.chapters_links()
        self.assertEqual(gen.__next__(),
                         '/book/19980/65224/ready',
                         'wrong chapters link receive')
        
    def testGetFirstLine(self):
        nb = Notabenoid('19980')
        self.assertEqual(nb.content().__next__(), 
                         'A DANCE WITH DRAGONS / ТАНЕЦ С ДРАКОНАМИ A CAVIL ON CHRONOLOGY',
                         'wrong first book line')
    
    def testGetFirstChapter(self):
        nb = Notabenoid('19980')
        for line in nb.content():
            if not line:
                break
            else:
                last_line = line
        self.assertEqual(last_line, 
                         '—Джордж Р. Р. Мартин Апрель 2011',
                         'wrong first chapter')
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()