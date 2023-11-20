from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from api.Harness import *

class GlitchWorker(QThread):
    def __init__(self, glitch_parameters, harness):
        super().__init__()
        self.harness : DeviceHarness = harness
        self.glitch_parameters = glitch_parameters
 
    def run(self):
        while not self.harness.should_terminate():
            self.harness.reset()
            self.harness.test()
    