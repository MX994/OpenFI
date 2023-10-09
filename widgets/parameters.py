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

class XYGlitchParametersWidget(QWidget):
    def __init__(self):
        super(XYGlitchParametersWidget, self).__init__()

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
        for i, e in enumerate(['Minimum', 'Maximum', 'Step']):
            parameter_layout.addWidget(QLabel(e), 0, 1 + i)

        for row, parameter_type in enumerate(self.glitch_parameters):
            for i, e in enumerate(parameter_type):
                parameter_layout.addWidget(e, row + 1, i)
                
        parent_layout.addLayout(parameter_layout)
        self.setLayout(parent_layout)
        

class CrowbarGlitchParametersWidget(QWidget):
    def __init__(self):
        super(CrowbarGlitchParametersWidget, self).__init__()

        parent_layout = QVBoxLayout()

        '''
            Define items to be used in the layout.
        '''
        glitch_parameter_names = [
            'Ext. Offset',
            'Repeat',
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
        self.setLayout(parent_layout)