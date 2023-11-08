from widgets.CoreDevices import *

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
        self.gantry_down_button = QPushButton('▼')
        self.gantry_forward_button = QPushButton('↑')
        self.gantry_backward_button = QPushButton('↓')
        self.gantry_left_button = QPushButton('←')
        self.gantry_right_button = QPushButton('→')
        self.gantry_home_button = QPushButton('⌂')
        self.gantry_coordinate_spinners = (QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox())

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
