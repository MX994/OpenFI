from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from core_devices.DualSense import DualSense
from core_devices import CoreIODevices, PositionMode
from api.Harness import DeviceHarness

class GlitchWorker(QThread):
    glitchSuccess = pyqtSignal(tuple)
    glitchReset = pyqtSignal(tuple)
    glitchStop = pyqtSlot()
    
    def __init__(self):
        super().__init__()
        self.glitch_harness : DeviceHarness = None
        self.configuration = None

    def set_glitch_type(self, configuration):
        self.configuration = configuration

    def set_harness(self, harness : DeviceHarness):
        self.glitch_harness = harness

    def run(self):
        while not self.glitch_harness.should_terminate() and self.glitch_harness != None and self.configuration != None:
            for x, y, z, ext_offset, repeat in zip(
                range(self.configuration['X Min'], self.configuration['X Max'], self.configuration['X Step']),
                range(self.configuration['Y Min'], self.configuration['Y Max'], self.configuration['Y Step']),
                range(self.configuration['Z Min'], self.configuration['Z Max'], self.configuration['Z Step']),
                range(self.configuration['Ext. Offset Min'], self.configuration['Ext. Offset Max'], self.configuration['Ext. Offset Step']),
                range(self.configuration['Repeat Min'], self.configuration['Repeat Max'], self.configuration['Repeat Step']),
            ):

                # If EMP XYZ Glitching Mode, move to the location                
                if self.configuration['Mode'] == 'XY':
                    CoreIODevices.XY.move((x, y, z))

                # Configure the GhettoGlitcher
                CoreIODevices.GhettoGlitcher.set_ext_offset(ext_offset)
                CoreIODevices.GhettoGlitcher.set_repeat(repeat)
                CoreIODevices.GhettoGlitcher.arm()

                # Reset and test
                self.glitch_harness.reset()
                if self.glitch_harness.test():
                    self.glitchSuccess.emit((x, y, z, ext_offset, repeat))
                else:
                    self.glitchReset.emit((x, y, z, ext_offset, repeat))
                        
