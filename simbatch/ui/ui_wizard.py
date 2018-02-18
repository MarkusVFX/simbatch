try:  # Maya 2016
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        print "PySide import ERROR"

from widgets import *


class WizardUI:
    qt_widget_wizard = None
    qt_lay_wizard_main = None

    batch = None
    top_ui = None
    mainw = None

    comfun = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.comfun = batch.comfun
        self.top_ui = top
        self.mainw = mainw
        self.init_ui()

    def init_ui(self):
        qt_widget_wizard = QWidget()
        qt_widget_wizard.setContentsMargins(20, 20, 20, 20)

        self.qt_widget_wizard = qt_widget_wizard

        qt_lay_wizard_main = QVBoxLayout(qt_widget_wizard)
        qt_lay_wizard_main.setContentsMargins(0, 0, 0, 0)
        self.qt_lay_wizard_main = qt_lay_wizard_main

        qt_lay_wizard_main.addWidget(QLabel("Wizard available in the Pro version !"))
