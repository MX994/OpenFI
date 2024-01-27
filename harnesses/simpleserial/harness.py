from api.Harness import *
from time import sleep

class DeviceHarness(Harness):
    def __init__(self, devices):
        # super().__init__(devices)
        self.devices = devices
        self.count = 0
        return
    
    def configure(self) -> None:
        print('LFG!')
        return
    
    def reset(self) -> None:
        return
        
    def should_terminate(self) -> bool:
        return self.count == 10
    
    def test(self) -> bool:
        self.count += 1
        sleep(0.25)
        return True