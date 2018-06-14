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

    def __init__(self):
        super(InstallerWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setMinimumHeight(self.window_height)
        self.setMinimumWidth(self.window_width)

        self.animated_bar = AnimatedBar()

        # self.addLayout(self.animated_bar.qt_lay_animated_bar)
        qt_central_widget = QWidget(self)
        qt_central_widget.setLayout(self.animated_bar.qt_lay_animated_bar)
        self.setCentralWidget(qt_central_widget)



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
