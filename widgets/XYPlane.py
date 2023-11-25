from widgets.CoreDevices import *
from core_devices.XYPlane import PositionMode

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
    QGridLayout
)

class XYPlaneWidget(QWidget):
    def __init__(self):
        super(XYPlaneWidget, self).__init__()

        parent_layout = QVBoxLayout()
        
        '''
            Define items to be used in the layout.
        '''
        glitch_parameter_names = [
            'Ext. Offset',
            'Repeat',
            'X',
            'Y',
            'Z',
            'Tries',
        ]

        self.glitch_parameters = [
            [QLabel(e), QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox()] for e in glitch_parameter_names
        ]

        # Gantry controls.
        self.gantry_up_button = QPushButton('▲')
        self.gantry_up_button.clicked.connect(self.gantry_up_clicked)
        self.gantry_down_button = QPushButton('▼')
        self.gantry_down_button.clicked.connect(self.gantry_down_clicked)
        self.gantry_forward_button = QPushButton('↑')
        self.gantry_forward_button.clicked.connect(self.gantry_z_up_clicked)
        self.gantry_backward_button = QPushButton('↓')
        self.gantry_backward_button.clicked.connect(self.gantry_z_down_clicked)
        self.gantry_left_button = QPushButton('←')
        self.gantry_left_button.clicked.connect(self.gantry_left_clicked)
        self.gantry_right_button = QPushButton('→')
        self.gantry_right_button.clicked.connect(self.gantry_right_clicked)
        self.gantry_home_button = QPushButton('⌂')
        self.gantry_home_button.clicked.connect(self.gantry_home_clicked)
        self.gantry_coordinate_spinners = (QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox())
        [x.setMinimum(-235) for x in self.gantry_coordinate_spinners]

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

        '''
            Construct final layout.
        '''        
        parent_layout.addWidget(QLabel('Probe Position'))
        parent_layout.addLayout(gantry_layout)
        
        # Core Device Control
        parameter_layout = QGridLayout()
        for i, e in enumerate(['Minimum', 'Maximum', 'Step']):
            parameter_layout.addWidget(QLabel(e), 0, 1 + i)

        for row, parameter_type in enumerate(self.glitch_parameters):
            for i, e in enumerate(parameter_type):
                parameter_layout.addWidget(e, row + 1, i)
        parent_layout.addLayout(parameter_layout)
        parent_layout.addStretch()

        self.setLayout(parent_layout)

    def gantry_up_clicked(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((0, 0, 1))
        self.update_coordinate_spinners()
    
    def gantry_down_clicked(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((0, 0, -1))
        self.update_coordinate_spinners()
    
    def gantry_left_clicked(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((-1, 0, 0))
        self.update_coordinate_spinners()
    
    def gantry_right_clicked(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((1, 0, 0))
        self.update_coordinate_spinners()
    
    def gantry_z_up_clicked(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((0, 1, 0))
        self.update_coordinate_spinners()

    def gantry_z_down_clicked(self):
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move((0, -1, 0))
        self.update_coordinate_spinners()
    
    def gantry_home_clicked(self):
        CoreIODevices.XY.auto_home()
        self.update_coordinate_spinners()

    def update_coordinate_spinners(self):
        if (coordinates := CoreIODevices.XY.get_projected_position()) != None:
            for coordinate_index, coordinate in enumerate(coordinates):
                self.gantry_coordinate_spinners[coordinate_index].setValue(float(coordinate))

