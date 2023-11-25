import sys
from core_devices import CoreIODevices, PositionMode
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from widgets import XYPlane, Crowbar, CoreDevices
from handlers import *
import importlib
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("OpenFI")

        self.harness_path = Path('./harnesses')
        self.current_harness = None

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
        
        # Run Glitch
        self.run_glitch_action = QAction(QIcon("assets/play.png"), "&Run Glitch", self)
        self.run_glitch_action.setStatusTip('Start a glitch sequence with the specified parameters.')
        self.run_glitch_action.triggered.connect(self.onRunGlitch)

        # Stop Glitch
        self.stop_glitch_action = QAction(QIcon("assets/stop.png"), "&Stop Glitch", self)
        self.stop_glitch_action.setStatusTip('Stop the current glitch sequence.')
        self.stop_glitch_action.triggered.connect(self.onStopGlitch)

        # Refresh Harness List
        self.refresh_harness_list = QAction(QIcon("assets/refresh.png"), "&Refresh Harness List", self)
        self.refresh_harness_list.setStatusTip('Get all possible harnesses.')
        self.refresh_harness_list.triggered.connect(self.onHarnessRefresh)

        # Load Harness
        self.load_harness = QAction(QIcon("assets/load.png"), "&Load Harness", self)
        self.load_harness.setStatusTip('Load the selected harness.')
        self.load_harness.triggered.connect(self.onHarnessLoad)

        # Harness List
        self.harness_list = QComboBox()
        self.harness_list.setStatusTip('Selects the harness configuration to execute.')
        self.harness_list.setFixedWidth(128)

        self.harness_spacer = QWidget()
        self.harness_spacer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.harness_spacer.setFixedWidth(16)

        self.tab_control = QTabWidget(self)

        '''
            Construct final layout.
        '''
        layout = QHBoxLayout()
        
        # Build toolbar.
        toolbar.addSeparator()
        
        # Add harness list.
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)

        # Glitch controller buttons.
        toolbar.addActions([
            self.run_glitch_action,
            self.stop_glitch_action,
            self.refresh_harness_list,
            self.load_harness
        ])
        toolbar.addWidget(QLabel("Selected Harness"))
        toolbar.addWidget(self.harness_spacer)
        toolbar.addWidget(self.harness_list)
        self.addToolBar(toolbar)

        # Add subwindows.
        self.tab_control.addTab(self.crowbar_widget, 'Crowbar')
        self.tab_control.addTab(self.xy_widget, 'XY')
        self.tab_control.addTab(self.core_devices_widget, 'Core Devices')
        
        layout.addWidget(self.tab_control)
        self.setStatusBar(QStatusBar(self))
        
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

    def onHarnessLoad(self, s):
        # Load harness.
        if self.harness_list.currentText() not in [None, '']:
            module_name = f'{self.harness_list.currentText()}.harness'
            module_path = self.harness_path / self.harness_list.currentText() / 'harness.py'
            if not module_path.exists():
                return
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            self.current_harness = module.Harness()
    def onHarnessRefresh(self, s):
        self.harness_list.clear()
        self.harness_list.addItems([x.stem for x in self.harness_path.glob('*') if x.is_dir()])
        
def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
