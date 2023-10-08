from PyQt6.QtCore import QThread, QObject
from core_devices.dualsense import DualSense
from core_devices import CoreIODevices, PositionMode

class ControllerWorker(QThread):
    def __init__(self):
        super().__init__()
        self.ds = DualSense()
        self.ds.connect()

    def run(self):
        while True:            
            scale = 1
            self.ds.update()
            if self.ds.get_l1_pressed():
                scale *= 5
            pos = [
                self.ds.get_joy_lx_radial() / 12.5, 
                -self.ds.get_joy_ly_radial() / 12.5,
                -self.ds.get_joy_ry_radial() / 50
            ]
            if any(map(lambda k: k != 0, pos)):
                CoreIODevices.XY.set_position_mode(PositionMode.Relative)
                CoreIODevices.XY.move(list(map(lambda k: scale * k, pos)))