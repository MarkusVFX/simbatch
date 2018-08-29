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


class SimpleLabel:
    qt_widget_layout = None
    label = None

    def __init__(self, label_text, label_minimum_size=0, label_maximum=0):
        label = QLabel(label_text)
        self.label = label
        if label_minimum_size > 0:
            label.setMinimumWidth(label_minimum_size)
        if label_maximum > 0:
            label.setMaximumWidth(label_maximum)

        self.qt_widget_layout = QHBoxLayout()
        self.qt_widget_layout.addWidget(label)

    def hide(self):
        self.label.setVisible(False)

    def show(self, txt=None):
        if txt is not None:
            self.label.setText(txt)
        self.label.setVisible(True)


class ComboLabel:
    qt_widget_layout = None
    combo = None
    text_on_button_1 = None

    def __init__(self, label_text, combo_items_arr, combo_current_index=0, label_minimum_size=0, text_on_button_1="",
                 button_size=0):
        self.qt_widget_layout = QHBoxLayout()
        if label_text is not None and len(label_text) > 0:
            label = QLabel(label_text)
            if label_minimum_size > 0:
                label.setMinimumWidth(label_minimum_size)
            self.qt_widget_layout.addWidget(label)

        combo = QComboBox()
        if combo_items_arr is not None:
            for it in combo_items_arr:
                combo.addItem(it)
            combo.setCurrentIndex(combo_current_index)
        self.qt_widget_layout.addWidget(combo)
        self.combo = combo

        if len(text_on_button_1) > 0:
            self.button_1 = QPushButton(text_on_button_1)
            self.qt_widget_layout.addWidget(self.button_1)
            if button_size > 0:
                self.button_1.setMaximumWidth(button_size)


class EditLineWithButtons:
    qt_widget_layout = None
    qt_edit_line = None
    button_1 = None
    button_2 = None
    label = None

    def __init__(self, label_text, edit_text_string="", label_minimum_size=0, text_on_button_1="", text_on_button_2="",
                 button_width=0, align_right=0, edit_minimum_size=0, edit_maximum_size=0):
        self.qt_widget_layout = QHBoxLayout()
        if edit_text_string is not None:
            self.qt_edit_line = QLineEdit(edit_text_string)
            if edit_minimum_size > 0:
                self.qt_edit_line.setMinimumWidth(edit_minimum_size)
            if edit_maximum_size > 0:
                self.qt_edit_line.setMaximumWidth(edit_maximum_size)

        if len(label_text) > 0:
            label = QLabel(label_text)
            self.label = label
            if label_minimum_size > 0:
                label.setMinimumWidth(label_minimum_size)
            if align_right == 1:
                label.setAlignment(Qt.AlignRight)
            self.qt_widget_layout.addWidget(label)
        if edit_text_string is not None:
            self.qt_widget_layout.addWidget(self.qt_edit_line)

        if len(text_on_button_1) > 0:
            self.button_1 = QPushButton(text_on_button_1)
            self.qt_widget_layout.addWidget(self.button_1)
            if button_width > 0:
                self.button_1.setFixedWidth(button_width)
        if len(text_on_button_2) > 0:
            self.button_2 = QPushButton(text_on_button_2)
            self.qt_widget_layout.addWidget(self.button_2)
            if button_width > 0:
                self.button_2.setFixedWidth(button_width)

    def get_txt(self):
        return self.qt_edit_line.text()


class ButtonOnLayout:
    qt_widget_layout = None
    button = None

    def __init__(self, text_on_button, enabled=True, width=0):
        self.qt_widget_layout = QHBoxLayout()
        self.button = QPushButton(text_on_button)
        if enabled is False:
            self.button.setEnabled(False)
        if width > 0:
            self.button.setFixedWidth(width)
        self.qt_widget_layout.addWidget(self.button)


class ButtonWithCheckBoxes:
    qt_widget_layout = None
    button = None
    qt_pin_check_box = None
    qt_second_check_box = None
    qt_third_check_box = None

    def __init__(self, text_on_button, pin_text="", cb2_text="", cb3_text="", label_text="", enabled=True,
                 button_width=0, cb2_checked=False, cb3_checked=False):
        self.qt_widget_layout = QHBoxLayout()
        if len(pin_text) > 0:
            self.qt_pin_check_box = QCheckBox(pin_text)
            self.qt_widget_layout.addWidget(self.qt_pin_check_box)
        if len(cb2_text) > 0:
            self.qt_second_check_box = QCheckBox(cb2_text)
            self.qt_widget_layout.addWidget(self.qt_second_check_box)
            if cb2_checked:
                self.qt_second_check_box.setChecked(True)
        if len(cb3_text) > 0:
            self.qt_third_check_box = QCheckBox(cb3_text)
            self.qt_widget_layout.addWidget(self.qt_third_check_box)
            if cb3_checked:
                self.qt_third_check_box.setChecked(True)
        if len(label_text) > 0:
            self.qt_widget_layout.addWidget(QLabel(label_text))
        self.button = QPushButton(text_on_button)
        if button_width > 0:
            self.button.setFixedWidth(button_width)

        if enabled is False:
            self.button.setEnabled(False)
        self.qt_widget_layout.addWidget(self.button)


class CheckBoxes:
    qt_widget_layout = None
    qt_first_check_box = None
    qt_second_check_box = None

    def __init__(self, cb1_text="", cb2_text="", label_text=""):
        self.qt_widget_layout = QHBoxLayout()
        if len(cb1_text) > 0:
            self.qt_first_check_box = QCheckBox(cb1_text)
            self.qt_widget_layout.addWidget(self.qt_first_check_box)
        if len(cb2_text) > 0:
            self.qt_second_check_box = QCheckBox(cb2_text)
            self.qt_widget_layout.addWidget(self.qt_second_check_box)
        if len(label_text) > 0:
            self.qt_widget_layout.addWidget(QLabel(label_text))


class RadioButtons:
    qt_widget_layout = None
    currentActive = None
    qt_radio_butt_arr = []

    def __init__(self, label_text, names_array, checked_index, on_radio_change):
        self.qt_radio_butt_arr = []
        qt_lay = QHBoxLayout()
        qt_label_mode = QLabel(label_text)
        qt_lay.addWidget(qt_label_mode)
        qt_radio_group = QButtonGroup()
        qt_radio_group.setExclusive(True)

        for i, el in enumerate(names_array):
            qt_radio_butt = QRadioButton(el)
            # if checked_index == i:
            #     qt_radio_butt.setChecked(True)
            qt_radio_group.addButton(qt_radio_butt, i)
            qt_lay.addWidget(qt_radio_butt)
            self.qt_radio_butt_arr.append(qt_radio_butt)
            qt_radio_butt.clicked.connect(lambda ii=i: on_radio_change(ii))

        if checked_index is not None and checked_index < len(self.qt_radio_butt_arr):
            self.qt_radio_butt_arr[checked_index].setChecked(True)

        self.qt_widget_layout = qt_lay

    # def set_visual_checkeds(self, nr):
    #         self.qt_radio_butt_arr[nr-1].setChecked(True)


class ActionWidget(QWidget):    # used for add schema,  edit schema  form.    For add to queue use: ActionWidgetATQ
    # action_name = ""
    # action_sub_mode = ""
    multi_action = None  # MultiAction  # GroupAction
    qt_id = None
    qt_layout = None
    qt_label = None
    qt_edit = None
    qt_combo = None
    qt_button_1 = None
    qt_button_2 = None
    edit_val = ""
    cb1 = None
    cb2 = None
    cb3 = None

    widget_id = None

    current_action_index = 0   # current index from GroupAction;  0 for single action

    batch = None
    logger = None
    interactions = None

    def __init__(self, batch, top_ui, widget_id, label_txt, multi_action, edit_txt=None, combo_items="",
                 combo_def_val="", button_1_caption=None, button_1_fun_str=None,
                 button_2_caption=None, button_2_fun_str=None, enabled1=True, enabled2=True):

        QWidget.__init__(self)
        self.batch = batch
        self.top_ui = top_ui
        self.logger = batch.logger
        self.interactions = batch.dfn.current_interactions      # connect  qt_button_1   or and   qt_button_1
        self.widget_id = widget_id
        self.multi_action = multi_action

        qt_widget_layout = QHBoxLayout()
        qt_widget_layout.setSpacing(2)
        self.setMaximumHeight(70)
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.qt_layout = qt_widget_layout  # TODO check this

        self.ui_info = (button_1_caption, button_1_fun_str, button_2_caption, button_2_fun_str)  # only for print

        self.qt_label = QLabel(label_txt)
        qt_widget_layout.addWidget(self.qt_label)

        if edit_txt is None:
            if len(multi_action.actions) > 0:
                if len(multi_action.actions[0].actual_value) > 0:
                    edit_txt = multi_action.actions[0].actual_value
                else:
                    # edit_txt = multi_action.actions[0].default_value
                    edit_txt = multi_action.actions[0].ui[0]

        if edit_txt is not False:
            if edit_txt == " ":
                edit_txt = ""
            self.edit_val = str(edit_txt)
            self.qt_edit = QLineEdit(self.edit_val)
            qt_widget_layout.addWidget(self.qt_edit)
            self.qt_edit.textChanged.connect(self.on_change_line_edit)

        if button_1_caption is not None and len(button_1_caption) > 0:
            self.qt_button_1 = QPushButton(button_1_caption)
            if enabled1 is False:
                self.qt_button_1.setEnabled(False)
            self.qt_layout.addWidget(self.qt_button_1)

            self.qt_button_1.clicked.connect(lambda: self.eval_button_fun(self.qt_edit, button_1_fun_str))
            # predefined function from definition !!!!

        if button_2_caption is not None and len(button_2_caption) > 0:
            self.qt_button_2 = QPushButton(button_2_caption)
            if enabled2 is False:
                self.qt_button_2.setEnabled(False)
            self.qt_layout.addWidget(self.qt_button_2)

            self.qt_button_2.clicked.connect(lambda: self.eval_button_fun(self.qt_edit, button_2_fun_str))
            # predefined function from definition !!!!

        if len(combo_items) > 0:
            self.qt_combo = QComboBox()
            # combo_items_arr = combo_items.split(",")
            set_index = 0
            for counter, it in enumerate(combo_items):
                if len(combo_def_val) > 0 and it == combo_def_val:
                    set_index = counter
                    self.logger.deepdb(("new combo val ", set_index, "___", combo_def_val))
                self.qt_combo.addItem(it)
                # self.sub_action_data.append([counter, combo_val, x])

            self.qt_combo.setCurrentIndex(set_index)
            qt_widget_layout.addWidget(self.qt_combo)
            self.qt_combo.currentIndexChanged.connect(self.on_change_combo)
        self.setLayout(qt_widget_layout)

    def eval_button_fun(self, edit, button_fun_str):
        self.logger.deepdb(("eval_button_fun", button_fun_str))
        if button_fun_str[0] == "[":
            button_fun_str = button_fun_str[1:-1]
            script_function_splitted = button_fun_str.split("|")
            if len(script_function_splitted) > 1:
                function_to_eval = "self.defined_button_{}(\"{}\")".format(script_function_splitted[0],
                                                                           script_function_splitted[1])
            else:
                function_to_eval = "self.defined_button_"+script_function_splitted[0]+"()"
        else:
            function_to_eval = "self."+button_fun_str+"()"

        if function_to_eval is not None:
            eval_ret = eval(function_to_eval)
            edit.setText(eval_ret)
        else:
            self.batch.logger.wrn("Dynamic button clicked connect is EMPTY")

    @staticmethod
    def eval_str(str_to_eval):
        eval(str_to_eval)

    def defined_button_get_file(self):                # QFileDialog - protect common function to be independent library
        ret_file = self.batch.comfun.file_dialog_to_edit_line(self.qt_edit, QFileDialog,
                                                              self.batch.prj.current_project.project_directory)
        return ret_file

    def defined_button_get_directory(self):           # QFileDialog - protect common function to be independent library
        ret_dir = self.batch.comfun.get_dialog_directory(self.qt_edit, QFileDialog,
                                                         force_start_dir=self.batch.prj.current_project.project_directory,
                                                         dir_separator=self.sts.dir_separator)
        return ret_dir

    def defined_button_show_info(self, info):
        self.top_ui.set_top_info(info, 4)

    def get_current_action(self):
        for i, a in enumerate(self.multi_action.actions):
            if i == self.current_action_index:
                return a
        return None

    def on_change_line_edit(self, txt):
        self.logger.deepdb(("Action edit chngd: ", txt))
        self.edit_val = txt
        self.multi_action.actions[self.current_action_index].actual_value = txt

    def on_change_combo(self, index):
        self.logger.deepdb(("Action combo chngd: ", index, "  ", self.qt_combo.currentText()))
        self.current_action_index = index
        sub_a = self.multi_action.actions[index]
        if len(sub_a.actual_value) > 0:
            self.qt_edit.setText(sub_a.actual_value)
        else:
            # self.qt_edit.setText(sub_a.default_value)
            self.qt_edit.setText(sub_a.ui[0])
        if sub_a.ui is not None:
            if len(sub_a.ui) > 1:
                button_1_caption = sub_a.ui[1][0]   # TODO  sub_a as object
                button_1_fun_str = sub_a.ui[1][1]   # TODO  sub_a as object
                self.qt_button_1.setText(button_1_caption)
                self.qt_button_1.clicked.disconnect()
                self.qt_button_1.clicked.connect(lambda: self.eval_button_fun(self.qt_edit, button_1_fun_str))

            if len(sub_a.ui) > 2:
                button_2_caption = sub_a.ui[2][0]   # TODO  sub_a as object
                button_2_fun_str = sub_a.ui[2][1]   # TODO  sub_a as object
                self.qt_button_2.setText(button_2_caption)
                self.qt_button_2.clicked.disconnect()
                self.qt_button_2.clicked.connect(lambda: self.eval_button_fun(self.qt_edit, button_2_fun_str))


class ActionWidgetATQ(QWidget):  # QWidget
    qt_widget_layout = None
    qt_combo_param = None   # ComboLabel
    qt_edit_line_widget = None  # EditLineWithButtons

    batch = None

    evos_array = None
    evos_count = None

    def __init__(self, batch, text_label, text_edit, combo_label=None, combo_items=None):
        super(ActionWidgetATQ, self).__init__()
        # QWidget.__init__(self)
        self.batch = batch
        self.qt_widget_layout = QVBoxLayout()
        correct_button_caption = ""
        if combo_label is not None:
            self.qt_combo_param = ComboLabel(combo_label+" "+text_edit, combo_items, text_on_button_1="Add evo",
                                             button_size=70)
            self.qt_widget_layout.addLayout(self.qt_combo_param.qt_widget_layout)
            correct_button_caption = "Correct"

            self.qt_edit_line_widget = EditLineWithButtons(text_label, "", text_on_button_1=correct_button_caption,
                                                           button_width=70)
            if self.qt_combo_param is not None:
                self.qt_combo_param.button_1.clicked.connect(lambda: self.add_evo_to_line())

            if self.qt_edit_line_widget.button_1 is not None:
                self.qt_edit_line_widget.button_1.clicked.connect(lambda: self.correct_params())
                self.qt_edit_line_widget.qt_edit_line.textChanged.connect(lambda: self.check_evos())

        else:
            self.qt_edit_line_widget = EditLineWithButtons(text_label, text_edit,
                                                           text_on_button_1=correct_button_caption, button_width=70)
        self.qt_widget_layout.addLayout(self.qt_edit_line_widget.qt_widget_layout)

    def __str__(self):
        return "ActionWidgetATQ   evos_count:" + str(self.evos_count)

    def add_evo_to_line(self):
        evo_abbreviation = self.qt_combo_param.combo.currentText()[:3]
        el = self.qt_edit_line_widget.qt_edit_line

        # print "[DB] add_evo_to_line: ", evo_abbreviation

        exist = el.text().find(evo_abbreviation)
        if exist >= 0:
            el.setText(el.text()[:exist+4] + "_" + el.text()[exist+4:])
        else:
            if len(el.text()) < 3:
                el.setText(evo_abbreviation + "  ")
            else:
                el.setText(el.text() + "; " + evo_abbreviation + "  ")
        self.check_evos()

    def check_evos(self):
        ret = self.batch.pat.get_evolutions_from_string(self.qt_edit_line_widget.qt_edit_line.text())

        self.evos_array = ret[1]
        self.show_number_evolutions(ret[0])
        self.evos_count = ret[0]

    def show_number_evolutions(self, nr):
        if nr <= 1:
            self.qt_edit_line_widget.label.setText("    {} evolution: ".format(nr))
        else:
            self.qt_edit_line_widget.label.setText("    {} evolutions:".format(nr))

    def correct_params(self):
        self.check_evos()
        ee = []
        for e in self.evos_array:
            ee.append("  ".join(e))
        self.qt_edit_line_widget.qt_edit_line.setText(" ;  ".join(ee))


class WidgetGroup:
    qt_widget_layout = None

    def __init__(self, widgets_list):
        self.qt_widget_layout = QHBoxLayout()
        for wi in widgets_list:
            self.qt_widget_layout.addLayout(wi.qt_widget_layout)
