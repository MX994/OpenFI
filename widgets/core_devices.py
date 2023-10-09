from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QDoubleSpinBox
)
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
        self.gantry_uart_refresh = QPushButton('Refresh Devices')
        self.gantry_uart_refresh.clicked.connect(self.get_uart_devices_gantry)

        self.emp_uart_connections = QComboBox()
        self.emp_uart_connect = QPushButton('Connect')
        self.emp_uart_refresh = QPushButton('Refresh Devices')
        self.emp_uart_refresh.clicked.connect(self.get_uart_devices_emp)

        # Gantry controls.
        self.gantry_up_button = QPushButton('▲')
        self.gantry_down_button = QPushButton('▼')
        self.gantry_forward_button = QPushButton('↑')
        self.gantry_backward_button = QPushButton('↓')
        self.gantry_left_button = QPushButton('←')
        self.gantry_right_button = QPushButton('→')
        self.gantry_home_button = QPushButton('⌂')
        self.gantry_coordinate_spinners = (QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox())

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

        # Gantry controls
        gantry_layout = QGridLayout()

        # Up and Down
        gantry_up_down_layout = QGridLayout()
        gantry_up_down_layout.addWidget(self.gantry_up_button, 0, 0)
        gantry_up_down_layout.addWidget(self.gantry_down_button, 1, 0)

        # Forward/Backward/Left/Right
        gantry_arrow_layout = QGridLayout()
        gantry_arrow_layout.setRowStretch(0, 0)
        gantry_arrow_layout.addWidget(self.gantry_forward_button, 0, 1)
        gantry_arrow_layout.addWidget(self.gantry_backward_button, 2, 1)
        gantry_arrow_layout.addWidget(self.gantry_left_button, 1, 0)
        gantry_arrow_layout.addWidget(self.gantry_right_button, 1, 2)
        gantry_arrow_layout.addWidget(self.gantry_home_button, 1, 1)

        # XYZ
        gantry_position_layout = QGridLayout()
        gantry_position_layout.addWidget(self.gantry_coordinate_spinners[0], 0, 0)
        gantry_position_layout.addWidget(self.gantry_coordinate_spinners[1], 0, 1)
        gantry_position_layout.addWidget(self.gantry_coordinate_spinners[2], 0, 2)

        gantry_layout.addLayout(gantry_arrow_layout, 0, 0)
        gantry_layout.addLayout(gantry_up_down_layout, 0, 1)
        gantry_layout.addLayout(gantry_position_layout, 1, 0, 1, 2)

        parent_layout.addWidget(QLabel('Device Connections'))

        parent_layout.addWidget(QLabel('XY Plane'))
        parent_layout.addLayout(gantry_uart_conn_layout)

        parent_layout.addWidget(QLabel('EMP'))
        parent_layout.addLayout(emp_uart_conn_layout)

        parent_layout.addWidget(QLabel('Probe Position'))
        parent_layout.addLayout(gantry_layout)
        
        self.setLayout(parent_layout)


    def get_uart_devices_gantry(self):
        self.gantry_uart_connections.clear()
        self.gantry_uart_connections.addItems([e.name for e in serial.tools.list_ports.comports()])
    
    def get_uart_devices_emp(self):
        self.emp_uart_connections.clear()
        self.emp_uart_connections.addItems([e.name for e in serial.tools.list_ports.comports()])

    def connect_to_xy_plane(self):
        # CoreIODevices.XY.connect('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
        CoreIODevices.XY.connect('COM9')
        CoreIODevices.XY.set_stepper_steps(X=200, Y=200, Z=800)
        CoreIODevices.XY.set_message('OpenEMP loaded.')

        # self.controller_worker = ControllerWorker()
        # self.movement_worker = MovementWorker()

    def connect_to_emp(self):
        ...