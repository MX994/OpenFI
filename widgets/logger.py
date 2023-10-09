from PyQt6.QtWidgets import (
    QTextEdit,
    QWidget,
    QVBoxLayout
)
from PyQt6.QtCore import *
from PyQt6.QtGui import QTextCursor
from queue import Queue
from handlers import *
import sys

class LoggerWidget(QWidget):
    def __init__(self):
        super(LoggerWidget, self).__init__()

        parent_layout = QVBoxLayout()

        '''
            Define items to be used in the layout.
        '''
        self.line_edit = QTextEdit()
        self.line_edit.setReadOnly(True)
        
        '''
            Construct final layout.
        '''

        parent_layout.addWidget(self.line_edit)
        parent_layout.addStretch()
        self.setLayout(parent_layout)

    def add_line(self, line):
        self.line_edit.moveCursor(QTextCursor.MoveOperation.End)
        self.line_edit.insertPlainText(line)
