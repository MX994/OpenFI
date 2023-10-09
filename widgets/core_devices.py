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

class CoreDevicesWidget(QWidget):
    def __init__(self):
        super(CoreDevicesWidget, self).__init__()

        parent_layout = QVBoxLayout()

        '''
            Define items to be used in the layout.
        '''
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

        parent_layout.addWidget(QLabel('Probe Position'))
        parent_layout.addLayout(gantry_layout)

        self.setLayout(parent_layout)