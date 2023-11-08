import sys
from core_devices import CoreIODevices, PositionMode
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from widgets import XYPlane, Crowbar, CoreDevices
from handlers import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("OpenFI")

        '''
            Define components to be placed in the view.
        '''
        self.tab_control = QTabWidget(self)
        self.crowbar_widget = Crowbar.CrowbarWidget()
        self.xy_widget = XYPlane.XYPlaneWidget()
        self.core_devices_widget = CoreDevices.CoreDevicesWidget()
        
        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        # self.addToolBar(toolbar)

        # Run Glitch
        self.run_glitch_action = QAction(QIcon("assets/play.png"), "&Run Glitch", self)
        self.run_glitch_action.setStatusTip('Start a glitch sequence with the specified parameters.')
        self.run_glitch_action.triggered.connect(self.onRunGlitch)
        self.run_glitch_action.setCheckable(True)

        # Stop Glitch
        self.stop_glitch_action = QAction(QIcon("assets/stop.png"), "&Stop Glitch", self)
        self.stop_glitch_action.setStatusTip('Stop the current glitch sequence.')
        self.stop_glitch_action.triggered.connect(self.onStopGlitch)
        self.stop_glitch_action.setCheckable(True)

        # Harness List
        self.harness_list = QComboBox()
        self.harness_list.setStatusTip('Selects the harness configuration to execute.')

        self.harness_spacer = QWidget()
        self.harness_spacer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.harness_spacer.setFixedWidth(8)

        self.tab_control = QTabWidget(self)

        '''
            Construct final layout.
        '''
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Add glitch controller buttons.
        toolbar.addActions([
            self.run_glitch_action,
            self.stop_glitch_action
        ])
        toolbar.addSeparator()
        
        # Add harness list.
        toolbar.addWidget(QLabel("Selected Harness"))
        toolbar.addWidget(self.harness_spacer)
        toolbar.addWidget(self.harness_list)

        # Add subwindows.
        self.tab_control.addTab(self.crowbar_widget, 'Crowbar')
        self.tab_control.addTab(self.xy_widget, 'XY')
        self.tab_control.addTab(self.core_devices_widget, 'Core Devices')
        
        layout.addWidget(self.tab_control)
        self.setStatusBar(QStatusBar(self))
        
        # Replace stdout.
        self.queue = Queue()
        sys.stdout = LoggerHook(self.queue)
        
        # # Start receiver thread.
        # self.logger_receiver_thread = QThread()
        # self.logger_receiver = LoggerReceiver(self.queue)
        # self.logger_receiver.textReceived.connect(self.crowbar_widget.logger_widget.add_line)
        # self.logger_receiver.textReceived.connect(self.xy_widget.logger_widget.add_line)
        # self.logger_receiver.moveToThread(self.logger_receiver_thread)
        # self.logger_receiver_thread.started.connect(self.logger_receiver.run)
        # self.logger_receiver_thread.start()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)
         
    def onRunGlitch(self, s):
        print("click", s)

    def onStopGlitch(self, s):
        print("click", s)
        
def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
