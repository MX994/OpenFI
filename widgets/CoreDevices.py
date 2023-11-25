from PyQt6.QtWidgets import *
from core_devices import CoreIODevices
import serial.tools.list_ports

class CoreDevicesWidget(QWidget):
    def __init__(self):
        super(CoreDevicesWidget, self).__init__()

        parent_layout = QVBoxLayout()

        '''
            Define items to be used in the layout.
        '''

        # Getting UART devices
        self.gantry_uart_connections = QComboBox()
        self.gantry_uart_connect = QPushButton('Connect')
        self.gantry_uart_connect.clicked.connect(self.connect_to_xy_plane)
        self.gantry_uart_refresh = QPushButton('Refresh Devices')
        self.gantry_uart_refresh.clicked.connect(self.get_uart_devices_gantry)

        self.emp_uart_connections = QComboBox()
        self.emp_uart_connect = QPushButton('Connect')
        self.emp_uart_connect.clicked.connect(self.connect_to_emp)
        self.emp_uart_refresh = QPushButton('Refresh Devices')
        self.emp_uart_refresh.clicked.connect(self.get_uart_devices_emp)

        '''
            Construct final layout.
        '''
        # XYPlane UART
        gantry_uart_conn_layout = QGridLayout()
        gantry_uart_conn_layout.addWidget(self.gantry_uart_connections, 0, 0)
        gantry_uart_conn_layout.addWidget(self.gantry_uart_connect, 0, 1)
        gantry_uart_conn_layout.addWidget(self.gantry_uart_refresh, 0, 2)

        # EMP
        emp_uart_conn_layout = QGridLayout()
        emp_uart_conn_layout.addWidget(self.emp_uart_connections, 0, 0)
        emp_uart_conn_layout.addWidget(self.emp_uart_connect, 0, 1)
        emp_uart_conn_layout.addWidget(self.emp_uart_refresh, 0, 2)

        parent_layout.addWidget(QLabel('Device Connections'))
        parent_layout.addWidget(QLabel('XY Plane'))
        parent_layout.addLayout(gantry_uart_conn_layout)
        parent_layout.addWidget(QLabel('EMP'))
        parent_layout.addLayout(emp_uart_conn_layout)
        parent_layout.addStretch()
        
        self.setLayout(parent_layout)


    def get_uart_devices_gantry(self):
        self.gantry_uart_connections.clear()
        self.gantry_uart_connections.addItems([e.name for e in serial.tools.list_ports.comports()])
    
    def get_uart_devices_emp(self):
        self.emp_uart_connections.clear()
        self.emp_uart_connections.addItems([e.name for e in serial.tools.list_ports.comports()])

    def connect_to_xy_plane(self):
        # CoreIODevices.XY.connect('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
        print(self.gantry_uart_connections.currentText())
        CoreIODevices.XY.connect(self.gantry_uart_connections.currentText())
        CoreIODevices.XY.set_stepper_steps(X=200, Y=200, Z=800)
        CoreIODevices.XY.set_message('OpenEMP loaded.')
        CoreIODevices.XY.beep()

        # self.controller_worker = ControllerWorker()
        # self.movement_worker = MovementWorker()

    def connect_to_emp(self):
        ...