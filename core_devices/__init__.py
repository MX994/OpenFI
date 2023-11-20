from .XYPlane import *
from .GhettoGlitcher import *

class Devices:
    def __init__(self):
        self.XY = XYPlane()
        self.GhettoGlitcher = GhettoGlitcher()
        return
    
CoreIODevices = Devices()