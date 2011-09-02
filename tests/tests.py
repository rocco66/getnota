'''
Created on 26.08.2011

@author: max
'''
import unittest
from notabenoid import Notabenoid
from fb2creator import FB2Creator


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
        links = nb.get_chapters_links()
        self.assertEqual(links[0],
                         '/book/19980/65224/ready',
                         'wrong chapters link receive')
        
    def testGetFirstLine(self):
        nb = Notabenoid('19980')
        self.assertEqual(nb.content().__next__(), 
                         'A DANCE WITH DRAGONS / ТАНЕЦ С ДРАКОНАМИ A CAVIL ON CHRONOLOGY',
                         'wrong first book line')
    
    def testGetThirdChapter(self):
        nb = Notabenoid('19980')
        for l in nb.get_chapter(3):
            pass
        self.assertEqual(l, 
                         '.',
                         'wrong first chapter')
        
    def testGetChapterNumber(self):
        nb = Notabenoid('19980')
        self.assertEqual(nb.get_chapter_number(), 
                         75,
                         'wrong chapter number')
        
    def testCreateFB2(self):
        creator = FB2Creator('test')
        creator.add_data('12345')
        self.assertEqual(creator.create(), 
                         True,
                         "Can't create FB2 file")

        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()