from api.Harness import *

class Harness(DeviceHarness):
    def __init__(self):
        return
    
    def configure(self) -> None:
        print('LFG!')
        return
    
    def reset(self) -> None:
        return
        
    def should_terminate(self) -> bool:
        return True
    
    def test(self) -> bool:
        return False