from .XYPlane import *
from .GhettoGlitcher import *
from .PicoEMP import *
class Devices:
    def __init__(self):
        self.XY = XYPlane()
        self.GhettoGlitcher = GhettoGlitcher()
        self.PicoEMP = ChipShouterPicoEMP()
        return
    
CoreIODevices = Devices()