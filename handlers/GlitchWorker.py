from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from core_devices.DualSense import DualSense
from core_devices import CoreIODevices, PositionMode
from api.Harness import DeviceHarness
from numpy import arange

class GlitchWorker(QThread):
    glitchSuccess = pyqtSignal(tuple)
    glitchReset = pyqtSignal(tuple)
    glitchStop = pyqtSlot()
    
    def __init__(self):
        super().__init__()
        self.glitch_harness : DeviceHarness = None
        self.configuration = None

    def set_configuration(self, configuration):
        self.configuration = configuration

    def set_harness(self, harness : DeviceHarness):
        self.glitch_harness = harness

    def run(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((0, 20, 0))
        CoreIODevices.XY.auto_home()
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((0, 50, 0))

        while not self.glitch_harness.should_terminate() and self.glitch_harness != None and self.configuration != None:
            for x, y, z, ext_offset, repeat in zip(
                arange(self.configuration['X Min'], self.configuration['X Max'], self.configuration['X Step']),
                arange(self.configuration['Y Min'], self.configuration['Y Max'], self.configuration['Y Step']),
                arange(self.configuration['Z Min'], self.configuration['Z Max'], self.configuration['Z Step']),
                arange(self.configuration['Ext. Offset Min'], self.configuration['Ext. Offset Max'], self.configuration['Ext. Offset Step']),
                arange(self.configuration['Repeat Min'], self.configuration['Repeat Max'], self.configuration['Repeat Step']),
            ):
                
                print(f'Position: ({x}, {y}, {z}) w/ Ext. Offset {ext_offset} and Repeat {repeat}')

                # If EMP XYZ Glitching Mode, move to the location                
                if self.configuration['Mode'] == 'XY':
                    CoreIODevices.XY.move((x, y, z))

                # Configure the GhettoGlitcher
                CoreIODevices.GhettoGlitcher.set_ext_offset(ext_offset)
                CoreIODevices.GhettoGlitcher.set_repeat(repeat)

                # Reset and test
                self.glitch_harness.reset()
                if self.glitch_harness.test():
                    self.glitchSuccess.emit((x, y, z, ext_offset, repeat))
                else:
                    self.glitchReset.emit((x, y, z, ext_offset, repeat))
                        
