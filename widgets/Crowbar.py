from widgets.Camera import *
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

class CrowbarWidget(QWidget):
    def __init__(self):
        super(CrowbarWidget, self).__init__()

        parent_layout = QVBoxLayout()

        glitch_parameter_names = [
            'Ext. Offset',
            'Repeat',
            'Tries',
        ]

        self.glitch_parameters = [
            [QLabel(e), QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox()] for e in glitch_parameter_names
        ]

        '''
            Construct final layout.
        '''
        parameter_layout = QGridLayout()
        for i, e in enumerate(['Minimum', 'Maximum', 'Step']):
            parameter_layout.addWidget(QLabel(e), 0, 1 + i)

        for row, parameter_type in enumerate(self.glitch_parameters):
            for i, e in enumerate(parameter_type):
                parameter_layout.addWidget(e, row + 1, i)
        parent_layout.addLayout(parameter_layout)
        parent_layout.addStretch()
        self.setLayout(parent_layout)