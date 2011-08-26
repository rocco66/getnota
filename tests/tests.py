'''
Created on 26.08.2011

@author: max
'''
import unittest
from notabenoid import Notabenoid


class Test(unittest.TestCase):

    def testGetBookNameByID(self):
        nb = Notabenoid('19980')
        self.assertEqual(nb.get_book_name(), 
                         'A DANCE WITH DRAGONS / ТАНЕЦ С ДРАКОНАМИ',
                         'wrong book name receive')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()