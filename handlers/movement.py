from PyQt6.QtCore import QThread, QObject, pyqtSlot
from core_devices.dualsense import DualSense
from core_devices import CoreIODevices, PositionMode

class MovementWorker(QThread):
    def __init__(self):
        super().__init__()
        
        return
    
    def run(self):
        return
    
    @pyqtSlot()
    def auto_home(self):
        CoreIODevices.XY.auto_home()

    @pyqtSlot(tuple)
    def move(self, coordinates):
        CoreIODevices.XY.set_position_mode(PositionMode.Absolute)
        CoreIODevices.XY.move(coordinates)

    