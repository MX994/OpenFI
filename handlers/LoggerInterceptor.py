from PyQt6.QtCore import *
from PyQt6.QtGui import *
from queue import Queue


class LoggerHook(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        ...

class LoggerReceiver(QObject):
    textReceived = pyqtSignal(str)

    def __init__(self, queue):
        super(QObject, self).__init__()
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.textReceived.emit(text)
