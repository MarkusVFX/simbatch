
try:
    from PySide.QtCore  import *
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *


class SimpleLabel():
    qt_widget_layout = None
    def __init__(self, label_text, label_minimum_size=0, label_maximum=0):
        label = QLabel(label_text)
        if label_minimum_size > 0:
            label.setMinimumWidth(label_minimum_size)
        if label_maximum > 0:
            label.setMaximumWidth(label_maximum)

        self.qt_widget_layout = QHBoxLayout()
        self.qt_widget_layout.addWidget(label)


class ComboLabel():
    qt_widget_layout = None
    combo = None
    text_on_button_1 = None

    def __init__(self, label_text, combo_items_arr, combo_current_index=0, label_minimum_size=0, text_on_button_1="",
                 buttonSize=0):
        self.qt_widget_layout = QHBoxLayout()
        if len(label_text) > 0:
            label = QLabel(label_text)
            if label_minimum_size > 0:
                label.setMinimumWidth(label_minimum_size)
            self.qt_widget_layout.addWidget(label)

        combo = QComboBox()
        for it in combo_items_arr:
            combo.addItem(it)
        combo.setCurrentIndex(combo_current_index)
        self.qt_widget_layout.addWidget(combo)
        self.combo = combo

        if len(text_on_button_1) > 0:
            self.text_on_button_1 = QPushButton(text_on_button_1)
            self.qt_widget_layout.addWidget(self.text_on_button_1)
            if buttonSize > 0:
                self.text_on_button_1.setMaximumWidth(buttonSize)



class EditLineWithButtons:
    qt_widget_layout = None
    qt_edit_line = None
    text_on_button_1 = None
    text_on_button_2 = None
    label = None

    def __init__(self, label_text, edit_text_string="", label_minimum_size=0, text_on_button_1="", text_on_button_2="",
                 button_width=0, align_right=0, edit_minimum_size=0, edit_maximum_size=0):
        self.qt_widget_layout = QHBoxLayout()
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
        self.qt_widget_layout.addWidget(self.qt_edit_line)

        if len(text_on_button_1) > 0:
            self.text_on_button_1 = QPushButton(text_on_button_1)
            self.qt_widget_layout.addWidget(self.text_on_button_1)
            if button_width > 0:
                self.text_on_button_1.setFixedWidth(button_width)
        if len(text_on_button_2) > 0:
            self.text_on_button_2 = QPushButton(text_on_button_2)
            self.qt_widget_layout.addWidget(self.text_on_button_2)
            if button_width > 0:
                self.text_on_button_2.setFixedWidth(button_width)


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
    third_check_box = None

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
            self.third_check_box = QCheckBox(cb3_text)
            self.qt_widget_layout.addWidget(self.third_check_box)
            if cb3_checked:
                self.third_check_box.setChecked(True)
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
            qt_radio_butt.clicked.connect(lambda i=i: on_radio_change(i))

        if checked_index is not None and checked_index < len(self.qt_radio_butt_arr):
            self.qt_radio_butt_arr[checked_index].setChecked(True)

        self.qt_widget_layout = qt_lay

    # def set_visual_checkeds(self, nr):
    #         self.qt_radio_butt_arr[nr-1].setChecked(True)


class ActionWidget(QWidget):
    # action_name = ""
    # action_sub_mode = ""
    action_data = None  # SingleAction   or  GroupAction
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

    def __init__(self, action_data, action_id="", label_txt="", edit_txt="", combo_items="", combo_val="", cb1="", cb2="",
                 cb3="", text_on_button_1="", text_on_button_2="", enabled1=True, enabled2=True):
        QWidget.__init__(self)
        # self.action_name = action_name
        self.action_data = action_data
        qt_widget_layout = QHBoxLayout()
        qt_widget_layout.setSpacing(2)
        self.setMaximumHeight(70)
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.qt_layout = qt_widget_layout  # TODO check this

        if len(action_id) > 0:
            self.qt_id = QLabel(action_id)

        if len(label_txt) > 0:
            self.qt_label = QLabel(label_txt)
            qt_widget_layout.addWidget(self.qt_label)

        if len(edit_txt) > 0:
            if edit_txt == " ":
                edit_txt = ""
            self.qt_edit = QLineEdit(edit_txt)
            self.edit_val = edit_txt
            qt_widget_layout.addWidget(self.qt_edit)
            self.qt_edit.textChanged.connect(self.on_change_line_edit)

        if text_on_button_2 is not None and len(text_on_button_2) > 0:
            self.qt_button_2 = QPushButton(text_on_button_2)
            if enabled2 is False:
                self.qt_button_2.setEnabled(False)
            self.qt_layout.addWidget(self.qt_button_2)

        if len(combo_items) > 0:
            self.qt_combo = QComboBox()
            # combo_items_arr = combo_items.split(",")
            counter = 0
            set_index = 0
            for it in combo_items:
                if len(combo_val) > 0 and it == combo_val:
                    set_index = counter
                    if self.s.debug_level >= 4:
                        print " [db] combo val ", set_index, "___", combo_val
                self.qt_combo.addItem(it)
                counter += 1

            self.qt_combo.setCurrentIndex(set_index)
            # self.action_sub_mode = combo_items_arr[0]
            # print " init action subtype : ", combo_items_arr[0]
            qt_widget_layout.addWidget(self.qt_combo)
            self.qt_combo.currentIndexChanged.connect(self.on_change_combo)

        if len(cb1) > 0:
            self.cb1 = QCheckBox(cb1, self)
            qt_widget_layout.addWidget(self.cb1)

        if len(cb2) > 0:
            self.cb2 = QCheckBox(cb2, self)
            qt_widget_layout.addWidget(self.cb2)

        if len(cb3) > 0:
            self.cb3 = QCheckBox(cb3, self)
            qt_widget_layout.addWidget(self.cb3)

        if len(text_on_button_1) > 0:
            self.qt_button_1 = QPushButton(text_on_button_1)
            if enabled1 is False:
                self.qt_button_1.setEnabled(False)
            self.qt_layout.addWidget(self.qt_button_1)

        self.setLayout(qt_widget_layout)

    def on_change_line_edit(self, txt):
        if self.s.debug_level >= 4:
            print "  [db] Action edit chngd: ", txt
        self.edit_val = txt

    def on_change_combo(self, index):
        if self.s.debug_level >= 4:
            print "  [db] Action combo chngd: ", index, "  ", self.combo.currentText()


class WidgetGroup:
    qt_widget_layout = None

    def __init__(self, widgets_list):
        self.qt_widget_layout = QHBoxLayout()
        for wi in widgets_list:
            self.qt_widget_layout.addLayout(wi.qt_widget_layout)
