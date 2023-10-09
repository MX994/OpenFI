
from widgets.camera import *
from widgets.core_devices import *
from widgets.logger import *
from widgets.parameters import *

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

        parent_layout = QGridLayout()

        # Core Device Control
        self.core_device_widget = CoreDevicesWidget()
        
        # Parameter Control
        self.glitch_parameter_widget = XYGlitchParametersWidget()

        # Logger Control
        self.logger_widget = LoggerWidget()

        
        parent_layout.addWidget(self.logger_widget, 1, 0)
        parent_layout.addWidget(self.core_device_widget, 0, 1)
        parent_layout.addWidget(self.glitch_parameter_widget, 1, 1)

        self.setLayout(parent_layout)

class CrowbarWidget(QWidget):
    def __init__(self):
        super(CrowbarWidget, self).__init__()

        parent_layout = QGridLayout()

        # Logger Control
        self.logger_widget = LoggerWidget()

        # Parameter Control
        self.glitch_parameter_widget = CrowbarGlitchParametersWidget()
        
        parent_layout.addWidget(self.logger_widget, 0, 0)
        parent_layout.addWidget(self.glitch_parameter_widget, 0, 1)
        
        self.setLayout(parent_layout)