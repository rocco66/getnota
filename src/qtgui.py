# -*- coding: utf-8 -*-
'''
Created on 05.09.2011

@author: max
'''

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
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
    CANCEL_BUTTON_TEXT = 'Cancel creation'

    chapter_proc = QtCore.pyqtSignal(int)

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.initUI()
        
    def initUI(self):
        '''
        Init all GUI elements.
        '''
        self.setWindowTitle(QTGUI.TITLE)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum)) 
        main_box = self.__search_area_init()
        out_box = self.__output_area_init()
        main_box.addLayout(out_box)
        self.setLayout(main_box)
        self.__go_to_base_state()
    
    def __search_area_init(self):
        '''
        Init search area of form. 
        '''
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
    
    @pyqtSlot(bool)
    def __spec_out(self, b):
        '''
        Slot of book search type changed. 
        '''
        if b:
            self.file_name_value.setEnabled(True)
        else:
            self.file_name_value.setEnabled(False)
    
    def __output_area_init(self):
        '''
        Init output area of form. 
        '''  
        out_box = QtGui.QVBoxLayout()
        self.file_name_spec = QtGui.QCheckBox(QTGUI.SPEC_DILE_NAME_TEXT, self)
        self.file_name_value = QtGui.QLineEdit(self)
        self.file_name_spec.toggled.connect(self.__spec_out)
        out_box.addWidget(self.file_name_spec)
        out_box.addWidget(self.file_name_value)
        create_button = QtGui.QPushButton(QTGUI.CREATE_BUTTON_TEXT, self)
        create_button.clicked.connect(self.__create_book)
        out_box.addWidget(create_button)
        self.create_button = create_button
        progress = QtGui.QProgressBar(self)
        out_box.addWidget(progress)
        self.progress = progress
        cancel_button = QtGui.QPushButton(QTGUI.CANCEL_BUTTON_TEXT, self)
        cancel_button.clicked.connect(self.__cancel_book)
        self.cancel_button = cancel_button
        out_box.addWidget(self.cancel_button)
        return out_box 
    
    @pyqtSlot(bool)    
    def __cancel_book(self, b):
        '''
        Cancel book generation. 
        '''
        self.gbt.terminate()
        self.__go_to_base_state()
        
    def __go_to_base_state(self):
        '''
        All GUI elements base state. 
        '''
        wlist = self.children()
        wlist.remove(self.progress)
        for w in wlist: 
            if issubclass(type(w), QtGui.QWidget):
                w.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress.setValue(self.progress.minimum())
        self.__spec_out(self.file_name_spec.isChecked())
        
    @pyqtSlot(bool)
    def __create_book(self, b):
        '''
        Create book by parameters. 
        '''
        
        class GetBookThread(QtCore.QThread):
            '''
            Create book thread. 
            '''
            def run(self):
                self.nb.generate()
        
        if self.search_id.isChecked():
            nb = Notabenoid2FB2(self.search_field.text())
            nb.set_notifier(self.__notifier)
            self.current_progress = 0
            self.progress.setMaximum(nb.get_chapter_number())
            self.chapter_proc.connect(self.progress.setValue)
            self.repaint()
            self.__go_to_progress_state()
            self.gbt = GetBookThread()
            self.gbt.nb = nb
            self.gbt.start()
        else:
            pass
        
    def __notifier(self, s):
        '''
        Called by each chapter generated. 
        '''
        self.current_progress += 1
        self.chapter_proc.emit(self.current_progress)
    
    def __go_to_progress_state(self):
        '''
        All GUI elements book generate state. 
        '''
        wlist = self.children()
        wlist.remove(self.progress)
        for w in wlist: 
            if issubclass(type(w), QtGui.QWidget):
                w.setEnabled(False)
        self.cancel_button.setEnabled(True)
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = QTGUI()
    ex.show()
    sys.exit(app.exec_())