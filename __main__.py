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
from widgets import ParentWidget
from handlers import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("OpenFI")

        '''
            Define components to be placed in the view.
        '''

        # CoreIODevices.XY.connect('/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
        CoreIODevices.XY.connect('COM9')

        self.controller_worker = ControllerWorker()
        self.movement_worker = MovementWorker()
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
        self.setCentralWidget(ParentWidget())
        self.setStatusBar(QStatusBar(self))
        
        self.controller_worker.doAutoHome.connect(self.movement_worker.do_auto_home)
        self.controller_worker.doRelativeMove.connect(self.movement_worker.do_move_relative)
        self.movement_worker.movementFinished.connect(self.controller_worker.enable_input)
        self.controller_worker.start()
    
    def onRunGlitchClicked(self, s):
        print("click", s)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
