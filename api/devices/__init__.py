from .XYPlane import *
from .GhettoGlitcher import *
from .PicoEMP import *

class Devices:
    def __init__(self):
        self.XY = XYPlane()
        self.GhettoGlitcher = GhettoGlitcher()
        self.PicoEMP = ChipShouterPicoEMP()
        self.Initialized = False
        return
    
    def Init(self):
        if not self.Initialized:
            self.XY.connect('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
            self.PicoEMP.connect('/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6616408438E5026-if00')
            self.GhettoGlitcher.connect('/dev/serial/by-id/usb-Unexpected_Maker_FeatherS2_Neo_d4:f9:8d:70:ef:f8-if00')
            self.Initialized = True