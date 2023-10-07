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

class CameraWidget(QWidget):
    def __init__(self):
        super(CameraWidget, self).__init__()

        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel('Camera'))

        self.setLayout(parent_layout)