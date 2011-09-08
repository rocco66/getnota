# -*- coding: utf-8 -*-
'''
Created on 05.09.2011

@author: max
'''

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QSizePolicy
from notabenoid2fb2 import Notabenoid2FB2
import sys


class QTGUI(QtGui.QWidget):
    '''
    Qt GUI for notabenoid2fb2
    '''

    TITLE = 'Notabenoid2fb2'
    SEARCH_BY_ID_TEXT = 'Search by ID'
    SEARCH_BY_ID_NAME = 'Search by Name'
    SPEC_DILE_NAME_TEXT = 'Specify file name'
    CREATE_BUTTON_TEXT = 'Create book'

    chapter_proc = QtCore.pyqtSignal(int)

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(QTGUI.TITLE)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum)) 
        main_box = self.__search_area_init()
        out_box = self.__output_area_init()
        main_box.addLayout(out_box)
        self.setLayout(main_box)
    
    def __search_area_init(self):
        self.search_field = QtGui.QLineEdit(self)
        self.search_id = QtGui.QRadioButton(QTGUI.SEARCH_BY_ID_TEXT, self)
        self.search_id.toggle()
        self.search_name = QtGui.QRadioButton(QTGUI.SEARCH_BY_ID_NAME, self)
        search_box = QtGui.QVBoxLayout()
        head = QtGui.QHBoxLayout()
        head.addWidget(self.search_id)
        head.addWidget(self.search_name)
        search_box.addLayout(head)
        search_box.addWidget(self.search_field)
        return search_box
    
    def __output_area_init(self):
        
        @pyqtSlot(bool)
        def __spec_out(b):
            if b:
                self.file_name_value.show()
            else:
                self.file_name_value.hide()
    
        out_box = QtGui.QVBoxLayout()
        self.file_name_spec = QtGui.QCheckBox(QTGUI.SPEC_DILE_NAME_TEXT, self)
        self.file_name_value = QtGui.QLineEdit(self)
        self.file_name_spec.toggled.connect(__spec_out)
        self.file_name_value.hide()
        out_box.addWidget(self.file_name_spec)
        out_box.addWidget(self.file_name_value)
        create_button = QtGui.QPushButton(QTGUI.CREATE_BUTTON_TEXT, self)
        create_button.clicked.connect(self.__create_book)
        out_box.addWidget(create_button)
        return out_box 
        
    @pyqtSlot(bool)
    def __create_book(self, b):
        
        class GetBookThread(QtCore.QThread):
            def run(self):
                self.nb.generate()
        
        if self.search_id.isChecked():
            nb = Notabenoid2FB2(self.search_field.text())
            nb.set_notifier(self.__notifier)
            progress = QtGui.QProgressBar(self)
            progress.setMaximum(nb.get_chapter_number())
            self.layout().addWidget(progress)
            self.progress = progress
            self.current_progress = 0
            self.chapter_proc.connect(self.progress.setValue)
            self.repaint()
            gbt = GetBookThread()
            gbt.nb = nb
            gbt.start()
        else:
            pass
        
    def __notifier(self, s):
        self.current_progress += 1
        self.chapter_proc.emit(self.current_progress)
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = QTGUI()
    ex.show()
    sys.exit(app.exec_())