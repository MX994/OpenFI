import serial
import enum

class PositionMode(enum.Enum):
    Absolute = 0
    Relative = 1

class XYPlane:
    def __init__(self):
        self.serial = None
        self.position_mode = None

    def connect(self, port: str, baud: int = 115200):
        if self.serial == None:
            try:
                self.serial = serial.Serial(port, baud)
                print('[+] Connected to XYZ-Plane!')
            except serial.SerialException as e:
                print(f'[-] Error when connecting XYZ-Plane: {e}')
            except ValueError as e:
                print(f'[-] Error when connecting XYZ-Plane: {e}')

    def send_command(self, command : str):
        response = []
        if self.serial != None:
            print(f'[+] Sending {command}...')
            self.serial.write(f'{command}\n'.encode())
            # Wait for response.
            while (current := self.serial.readline().decode('utf-8').strip('\n')) != 'ok':
                response.append(current)
                print(f'[-] {current}')
            print(f'[-] {current}')
        return response

    def auto_home(self) -> bool:
        self.send_command('G28')

    def beep(self):
        self.send_command('M300 P50')
        
    def get_projected_position(self):
        response = self.send_command('M114R')
        tokens = [x.split(':') for x in response[0].split(' ')]
        return (tokens[0][1], tokens[1][1], tokens[2][1])

    def set_stepper_steps(self, X=None, Y=None, Z=None, E=None):
        self.send_command(f'M092 {f"X{X}" if X != None else ""} {f"Y{Y}" if Y != None else ""} {f"Z{Z}" if Z != None else ""}')

    def set_message(self, msg):
        self.send_command(f'M117 {msg}')

    def get_position_mode(self) -> PositionMode:
        return self.position_mode
    
    def move(self, position: tuple, speed: int = 9600):
        # Move XY, then Z, to avoid collisions.
        self.send_command(f'G0 X{position[0]} Y{position[1]} Z{position[2]} F{speed}')
    
    def set_position_mode(self, requested_position: PositionMode) -> bool:
        self.position_mode = requested_position
        self.send_command(f'G9{requested_position.value}')
