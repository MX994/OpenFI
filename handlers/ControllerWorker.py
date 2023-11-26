from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from core_devices.DualSense import DualSense
from core_devices import CoreIODevices, PositionMode
from time import sleep

class ControllerWorker(QThread):
    setMinimumXYZ = pyqtSignal()
    setMaximumXYZ = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ds = DualSense()
        self.ds.connect()
        self.accepting_input = True

    @pyqtSlot()
    def enable_input(self):
        self.accepting_input = True
 
    def run(self):
        while True:
            self.ds.update()
            if self.ds.get_r1_pressed():
                CoreIODevices.XY.auto_home()
                continue
            scale = 5 if self.ds.get_l1_pressed() else 1
            pos = [
                self.ds.get_joy_lx_radial() / 12.5, 
                -self.ds.get_joy_ly_radial() / 12.5,
                -self.ds.get_joy_ry_radial() / 50
            ]
            if any(map(lambda k: k != 0, pos)):
                CoreIODevices.XY.set_position_mode(PositionMode.Relative)
                CoreIODevices.XY.move(tuple(map(lambda k: scale * k, pos)))
                self.accepting_input = False
            
            if self.ds.get_joy_l3_pressed():
                self.setMinimumXYZ.emit()
                sleep(0.250)

            if self.ds.get_joy_r3_pressed():
                self.setMaximumXYZ.emit()
                sleep(0.250)