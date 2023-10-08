import sys
from core_devices import CoreIODevices, PositionMode
from PyQt6.QtGui import QAction, QIcon, QKeyEvent
from PyQt6.QtCore import QEvent, QObject, Qt, QSize
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
    QGridLayout
)
from widgets.core_devices import *
from core_devices.dualsense import DualSense
from handlers.controller import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("OpenEMP")

        '''
            Define components to be placed in the view.
        '''
        CoreIODevices.XY.connect('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Run Glitch
        self.run_glitch_action = QAction(QIcon("bug.png"), "&Run Glitch", self)
        self.run_glitch_action.setStatusTip('Start a glitch sequence with the specified parameters.')
        self.run_glitch_action.triggered.connect(self.onRunGlitchClicked)
        self.run_glitch_action.setCheckable(True)

        # Stop Glitch
        self.stop_glitch_action = QAction(QIcon("bug.png"), "&Stop Glitch", self)
        self.stop_glitch_action.setStatusTip('Stop the current glitch sequence.')
        self.stop_glitch_action.triggered.connect(self.onRunGlitchClicked)
        self.stop_glitch_action.setCheckable(True)

        # Harness List
        self.harness_list = QComboBox()
        self.harness_list.setStatusTip('Selects the harness configuration to execute.')

        '''
            Construct final layout.
        '''

        layout = QGridLayout()
        
        # Add glitch controller buttons.
        toolbar.addActions([
            self.run_glitch_action,
            self.stop_glitch_action
        ])
        toolbar.addSeparator()
        
        # Add harness list.
        toolbar.addWidget(QLabel("Selected Harness"))
        toolbar.addWidget(self.harness_list)
        toolbar.addSeparator()

        CoreIODevices.XY.set_stepper_steps(X=200, Y=200, Z=800)
        CoreIODevices.XY.set_message('OpenEMP loaded.')

        # Add subwindows.
        self.setCentralWidget(CoreDevicesWidget())
        self.setStatusBar(QStatusBar(self))

        self.controller_worker = ControllerWorker()
        self.controller_worker.start()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        delta_position = [0, 0, 0]
        match event.key():
            case Qt.Key.Key_W:
                delta_position[1] = 0.5
            case Qt.Key.Key_S:
                delta_position[1] = -0.5
            case Qt.Key.Key_A:
                delta_position[0] = -0.5
            case Qt.Key.Key_D:
                delta_position[0] = 0.5
            case Qt.Key.Key_Q:
                delta_position[2] = -0.25
            case Qt.Key.Key_E:
                delta_position[2] = 0.25
        CoreIODevices.XY.set_position_mode(PositionMode.Relative)
        CoreIODevices.XY.move(delta_position)
        return super().keyPressEvent(event)
    
    def onRunGlitchClicked(self, s):
        print("click", s)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
