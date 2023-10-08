from PyQt6.QtCore import QThread
import hid
import enum

class Special(enum.Enum):
    L1 = 1
    R1 = (1 << 1)
    L2 = (1 << 2)
    R2 = (1 << 3)
    SHARE = (1 << 4)
    OPTIONS = (1 << 5)
    L3 = (1 << 6)
    R3 = (1 << 7)

class DualSense:
    def __init__(self) -> None:
        self.dualsense = hid.device()
        self.frame = DualSenseFrame()
        self.deadzone = 20
        self.joy_center = 128
    
    def connect(self):
        self.dualsense.open(0x054C, 0x0CE6)
        self.dualsense.set_nonblocking(True)

    def update(self):
        if (data := self.dualsense.read(0x40)):
            self.frame = DualSenseFrame(data)

    def get_joy_lx(self):
        return self.frame.lx
    
    def get_joy_lx_radial(self):
        return self.__linear_to_radial(self.get_joy_lx(), self.joy_center)
    
    def get_joy_ly(self):
        return self.frame.ly
    
    def get_joy_ly_radial(self):
        return self.__linear_to_radial(self.get_joy_ly(), self.joy_center)
    
    def get_joy_rx(self):
        return self.frame.rx
    
    def get_joy_rx_radial(self):
        return self.__linear_to_radial(self.get_joy_rx(), self.joy_center)
    
    def get_joy_ry(self):
        return self.frame.ry
    
    def get_joy_ry_radial(self):
        return self.__linear_to_radial(self.get_joy_ry(), self.joy_center)

    def get_l1_pressed(self):
        return self.frame.special & Special.L1.value
    
    def get_l2_pressed(self):
        return self.frame.special & Special.L2.value
    
    def get_r2_pressed(self):
        return self.frame.special & Special.R2.value
    
    def get_l2_analog(self):
        return self.frame.l2_analog
    
    def __linear_to_radial(self, n, center):
        rebase = n - center
        if abs(rebase) < self.deadzone:
            return 0
        # Center @ 128, w/ deadzone
        return rebase / center
    
    def get_r2_analog(self):
        return self.frame.r2_analog
    
    def get_joy_l3_pressed(self):
        return self.frame.special & Special.L3.value
    
    def get_joy_r3_pressed(self):
        return self.frame.special & Special.R3

class DualSenseFrame:
    def __init__(self, buffer=None):
        if buffer != None:
            self.connection_mode = buffer[0]
            self.lx = buffer[1]
            self.ly = buffer[2]
            self.rx = buffer[3]
            self.ry = buffer[4]
            self.l2_analog = buffer[5]
            self.r2_analog = buffer[6]
            self.unknown_counter = buffer[7]
            self.dpad_shapes = buffer[8]
            self.special = buffer[9]
            self.home_button = buffer[10]
        else:
            self.connection_mode = 0
            self.lx = 0
            self.ly = 0
            self.rx = 0
            self.ry = 0
            self.l2_analog = 0
            self.r2_analog = 0
            self.unknown_counter = 0
            self.dpad_shapes = 0
            self.special = 0
            self.home_button = 0  