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


class DefinitionsUI:
    qt_widget_definitions = None
    qt_lay_definitions_main = None

    batch = None
    top_ui = None
    mainw = None

    comfun = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.comfun = batch.comfun

        self.dfn = batch.dfn
        self.sts = batch.sts

        self.top_ui = top
        self.mainw = mainw
        self.init_ui()

    def init_ui(self):
        qt_widget_definitions = QWidget()
        qt_widget_definitions.setContentsMargins(20, 20, 20, 20)

        self.qt_widget_definitions = qt_widget_definitions

        lay_definitions_main = QVBoxLayout(qt_widget_definitions)
        lay_definitions_main.setContentsMargins(0, 0, 0, 0)
        self.qt_lay_definitions_main = lay_definitions_main

        prnt_lay = QVBoxLayout()
        current_name = EditLineWithButtons("Project Name:", label_minimum_size=94)

        print_base = ButtonOnLayout("Print Base", width=180)
        print_current = ButtonOnLayout("Print Current", width=180)
        print_all = ButtonOnLayout("Print ALL", width=180)

        print_base.button.clicked.connect(self.on_click_print_base)
        print_current.button.clicked.connect(self.on_click_sprint_current)
        print_all.button.clicked.connect(self.on_click_print_all)

        self.comfun.add_layouts(prnt_lay, [current_name.qt_widget_layout,
                                           print_base.qt_widget_layout,
                                           print_current.qt_widget_layout,
                                           print_all.qt_widget_layout])

        self.comfun.add_layouts(lay_definitions_main, [prnt_lay])

    def on_click_print_base(self):
        logger_raw = self.batch.logger.raw
        if self.dfn.current_definition_name is None:
            logger_raw("\n\n total_definitions:{} current:None".format(self.dfn.total_definitions))
        else:
            logger_raw("\n\n total_definitions:{} current:{}".format(self.dfn.total_definitions,
                                                                     self.dfn.current_definition_name))
            logger_raw(" dfn count:{} dfn names count:{}".format(len(self.dfn.definitions_array),
                                                                 len(self.dfn.definitions_names)))
        for d in self.dfn.definitions_array:
            logger_raw(" _name:{} total_actions:{} names count:{}".format(d.name, d.total_actions, len(d.action_names)))

    def on_click_sprint_current(self):
        self.batch.logger.raw(str(self.dfn.current_definition_name))
        for d in self.dfn.definitions_array:
            if d.name == self.dfn.current_definition_name:
                # self.print_single_dfn(d)
                d.print_single()

    def on_click_print_all(self):
        for d in self.dfn.definitions_array:
            d.print_single()
