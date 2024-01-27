class Harness:
    def __init__(self, devices):
        self.devices = devices
        return
    
    def configure(self) -> None:
        return
    
    def reset(self) -> None:
        return
        
    def should_terminate(self) -> bool:
        return True
    
    def test(self) -> bool:
        return False