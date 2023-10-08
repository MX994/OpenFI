from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from core_devices.dualsense import DualSense
from core_devices import CoreIODevices, PositionMode

class MovementWorker(QThread):
    movementFinished = pyqtSignal()
    def __init__(self):
        super().__init__()
    
    def run(self):
        return
    
    @pyqtSlot()
    def do_auto_home(self):
        CoreIODevices.XY.auto_home()
        self.movementFinished.emit()

    @pyqtSlot(tuple)
    def do_move_absolute(self, coordinates):
        CoreIODevices.XY.set_position_mode(PositionMode.Absolute)
        CoreIODevices.XY.move(coordinates)
        self.movementFinished.emit()

    @pyqtSlot(tuple)
    def do_move_relative(self, coordinates):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move(coordinates)
        self.movementFinished.emit()
    