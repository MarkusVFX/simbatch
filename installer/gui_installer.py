if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from simbatch.core.lib.logger import Logger
from simbatch.core.lib.common import CommonFunctions


try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        raise Exception('PySide import ERROR!  Please install PySide or PySide2')

env_maya = False

try:
    import maya.OpenMayaUI as mui
    env_maya = True
except ImportError:
    print('OpenMayaUI import ERROR! Run this script from Maya')
    pass


def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)

try:    # Maya 2016
    import shiboken
except:
    try:  # Maya 2017
        import shiboken2 as shiboken
    except:
        print "shiboken import ERROR"
        pass


class AnimatedBar:
    qt_lay_animated_bar = None

    def __init__(self):
        self.qt_lay_animated_bar = QHBoxLayout()

        qt_font = QFont()
        qt_font.setPointSize(10)
        qt_font.setBold(True)
        qt_font.setFamily("Veranda")
        qt_lbl_info = QLabel("info")
        qt_lbl_info.setFont(qt_font)
        self.qt_lay_animated_bar.addWidget(qt_lbl_info)


class InstallerWindow(QMainWindow):
    top_ui = None
    qt_tab_widget = None
    window_height = 220
    window_width = 400

    animated_bar = None
    comfun = None

    def __init__(self):
        super(InstallerWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.logger = Logger(log_level=0, console_level=3)
        self.comfun = CommonFunctions(self.logger)
        self.setMinimumHeight(self.window_height)
        self.setMinimumWidth(self.window_width)

        self.animated_bar = AnimatedBar()

        qt_central_widget = QWidget(self)
        qt_lay_central = QVBoxLayout()
        qt_lay_central.setContentsMargins(0, 0, 0, 0)
        qt_central_widget.setLayout(qt_lay_central)

        qt_lay_paths = QVBoxLayout()
        qt_gbox_paths = QGroupBox()
        qt_gbox_paths.setLayout(qt_lay_paths)
        """ SOURCE """
        qt_lay_path_source = QHBoxLayout()
        qt_path_source_label = QLabel("Source directory : ")
        qt_path_source_edit = QLineEdit("")
        qt_path_source_button = QPushButton("Get")
        qt_path_source_button.setToolTip('Select directory')
        qt_path_source_button.clicked.connect(self.on_click_get_source_dir)
        qt_lay_path_source.addWidget(qt_path_source_label)
        qt_lay_path_source.addWidget(qt_path_source_edit)
        qt_lay_path_source.addWidget(qt_path_source_button)

        """ DEST """
        qt_lay_path_destination = QHBoxLayout()
        qt_path_destination_label = QLabel("Destination directory : ")
        qt_path_destination_edit = QLineEdit("")
        qt_path_destination_button = QPushButton("Get")
        qt_path_destination_button.setToolTip('Select directory')
        qt_path_destination_button.clicked.connect(self.on_click_get_source_dir)
        qt_lay_path_destination.addWidget(qt_path_destination_label)
        qt_lay_path_destination.addWidget(qt_path_destination_edit)
        qt_lay_path_destination.addWidget(qt_path_destination_button)

        """  ADD PATHS  (SRC DEST)  """
        qt_lay_paths.addLayout(qt_lay_path_source)
        # qt_lay_paths.addSpacerItem(QSpacerItem(20,20))
        qt_lay_paths.addLayout(qt_lay_path_destination)


        qt_lay_buttons = QHBoxLayout()
        qt_info_button = QPushButton("Info")
        qt_check_button = QPushButton("Check")
        qt_install_button = QPushButton("Install")

        qt_lay_buttons.addWidget(qt_info_button)
        qt_lay_buttons.addWidget(qt_check_button)
        qt_lay_buttons.addWidget(qt_install_button)

        """  ADD TO CENTRAL  """
        qt_lay_central.addLayout(self.animated_bar.qt_lay_animated_bar)
        # qt_lay_central.addLayout(qt_lay_paths)
        qt_lay_central.addWidget(qt_gbox_paths)
        qt_lay_central.addLayout(qt_lay_buttons)
        self.setCentralWidget(qt_central_widget)


    def on_click_get_source_dir(self):
        self.comfun.get_dialog_directory(self.qt_settings_data_directory_edit, QFileDialog,
                                         dir_separator=self.settings.dir_separator)



if __name__ == "__main__":
    if env_maya:
        main_window = InstallerWindow()
        main_window.show()
    else:
        app = QApplication([])
        main_window = InstallerWindow()
        main_window.show()
        app.exec_()

    print ("env_maya", env_maya)
