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

class GlitchParametersWidget(QWidget):
    def __init__(self):
        super(GlitchParametersWidget, self).__init__()

        parent_layout = QVBoxLayout()

        '''
            Define items to be used in the layout.
        '''
        glitch_parameter_names = [
            'Ext. Offset',
            'Repeat',
            'X',
            'Y',
            'Z'
        ]

        self.glitch_parameters = [
            [QLabel(e), QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox()] for e in glitch_parameter_names
        ]

        '''
            Construct final layout.
        '''
        parameter_layout = QGridLayout()
        for row, parameter_type in enumerate(self.glitch_parameters):
            for i, e in enumerate(parameter_type):
                parameter_layout.addWidget(e, row, i)
        parent_layout.addLayout(parameter_layout)
        self.setLayout(parent_layout)