from serial import Serial

class GhettoGlitcher():
    def __init__(self):
        self.socket = None

    def connect(self, path : str):
        self.socket = Serial(path)

    def ping(self):
        self.socket.write(f'ping\n'.encode())
        self.print_response()

    def arm(self):
        self.socket.write(f'arm\n'.encode())
        self.print_response()

    def disarm(self):
        self.socket.write(f'disarm\n'.encode())
        self.print_response()

    def baud_rate(self, baud_rate : int):
        self.socket.write(f'baud {baud_rate}\n'.encode())
        self.print_response()

    def pattern(self, pattern):
        self.socket.write(f'pattern {pattern}\n'.encode())
        self.print_response()

    def trigger_type(self, type):
        self.socket.write(f'trigger_type {type}\n'.encode())
        self.print_response()

    def print_response(self):
        while (line := self.socket.readline()) != '': 
            print(line)