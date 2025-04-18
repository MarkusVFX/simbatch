try:  # Maya 2016
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        raise Exception('PySide import ERROR!  Please install PySide or PySide2')

from .widgets import *


class QueueFormEdit(QWidget):
    batch = None
    mainw = None

    qt_edit_fe_name = None
    qt_edit_fe_prior = None
    qt_edit_fe_state = None
    qt_fe_description = None
    qt_edit_button_fe_comm = None

    def __init__(self, batch, mainw):
        QWidget.__init__(self)
        # super(QueueFormEdit, self).__init__()
        self.batch = batch
        self.mainw = mainw
        self.comfun = batch.comfun
        self.init_ui_elements()

    def init_ui_elements(self):
        qt_form_edit_layout_ext = QVBoxLayout()
        self.setLayout(qt_form_edit_layout_ext)

        qt_form_edit_layout = QVBoxLayout()

        # fe   form edit
        qt_edit_button_fe_name = EditLineWithButtons("Queue item name: ")
        qt_edit_button_fe_prior = EditLineWithButtons("Priority: ", label_minimum_size=65)
        qt_edit_button_fe_state = EditLineWithButtons("State: ", label_minimum_size=65)
        qt_edit_button_fe_descr = EditLineWithButtons("Description:  ", label_minimum_size=65)
        qt_edit_button_fe_comm = QTextEdit()
        qt_lay_command = QVBoxLayout()
        qt_lay_command.addWidget(qt_edit_button_fe_comm)
        self.qt_edit_fe_name = qt_edit_button_fe_name.qt_edit_line
        self.qt_edit_fe_prior = qt_edit_button_fe_prior.qt_edit_line
        self.qt_edit_fe_state = qt_edit_button_fe_state.qt_edit_line
        self.qt_fe_description = qt_edit_button_fe_descr.qt_edit_line
        self.qt_edit_button_fe_comm = qt_edit_button_fe_comm

        qt_cb_button_save = ButtonWithCheckBoxes("Save changes", pin_text="pin")
        qt_cb_button_save.button.clicked.connect(
            lambda: self.on_click_save_changes(qt_edit_button_fe_name.get_txt(), qt_edit_button_fe_prior.get_txt(),
                                               qt_edit_button_fe_state.get_txt(), qt_edit_button_fe_descr.get_txt()))

        # TODO  qt_cb_button_save !!!
        qt_cb_button_save.button.setEnabled(False)

        self.comfun.add_layouts(qt_form_edit_layout, [qt_edit_button_fe_name.qt_widget_layout,
                                                      qt_edit_button_fe_prior.qt_widget_layout,
                                                      qt_edit_button_fe_state.qt_widget_layout,
                                                      qt_edit_button_fe_descr.qt_widget_layout,
                                                      qt_lay_command,
                                                      qt_cb_button_save.qt_widget_layout])

        qt_gb_edit = QGroupBox()
        qt_gb_edit.setLayout(qt_form_edit_layout)
        qt_form_edit_layout_ext.addWidget(qt_gb_edit)

    def update_edit_ui(self, que=None):
        if que is None:
            if self.batch.que.current_queue_index >= 0:
                que = self.batch.que.current_queue
            else:
                self.batch.logger.wrn("Please Select Queue Item")
                self.mainw.top_ui.set_top_info(" Please Select Queue Item", 7)

        if que is not None:
            self.qt_edit_fe_name.setText(que.queue_item_name)
            self.qt_edit_fe_prior.setText(str(que.prior))
            self.qt_edit_fe_state.setText(que.state)
            self.qt_fe_description.setText(que.description)
            self.qt_edit_button_fe_comm.setText(que.evolution_script.replace(";", ";\n\n"))

    def on_click_save_changes(self, updated_queue_name, updated_prior, updated_state, updated_description):
        # TODO  qt_cb_button_save !!!
        pass


class QueueFormRemove(QWidget):
    batch = None
    mainw = None

    def __init__(self, batch, mainw):
        QWidget.__init__(self)
        # super(QueueFormRemove, self).__init__()
        self.batch = batch
        self.mainw = mainw

        self.init_ui_elements()

    def init_ui_elements(self):
        qt_form_remove_layout_ext = QVBoxLayout()
        self.setLayout(qt_form_remove_layout_ext)

        qt_form_remove_layout = QFormLayout()

        qt_cb_button_remove = ButtonWithCheckBoxes("Yes, remove", label_text="Remove selected ?        ")

        qt_form_remove_layout.addRow(" ", QLabel("   "))
        qt_form_remove_layout.addRow(" ", qt_cb_button_remove.qt_widget_layout)
        qt_form_remove_layout.addRow(" ", QLabel("   "))
        qt_cb_button_remove.button.clicked.connect(self.on_click_remove)

        qt_gb_remove = QGroupBox()
        qt_gb_remove.setLayout(qt_form_remove_layout)
        qt_form_remove_layout_ext.addWidget(qt_gb_remove)

    def on_click_remove(self):
        self.mainw.que_ui.on_click_confirmed_remove_queue_item()

