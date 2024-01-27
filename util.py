from api.Harness import Harness

class HarnessWrapper:
    def __init__(self):
        self.Harness = None
        return
    
    def Set(self, harness : Harness):
        self.Harness = harness

    def Get(self) -> Harness:
        return self.Harness