
try:
    from PySide.QtCore  import *
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *


class SimpleLabel():
    qt_widget_layout = None
    def __init__(self, label_text, label_minimum_size=0, labelMaximum=0):
        label = QLabel(label_text)
        if label_minimum_size > 0:
            label.setMinimumWidth(label_minimum_size)
        if labelMaximum > 0:
            label.setMaximumWidth(labelMaximum)

        self.qt_widget_layout = QHBoxLayout()
        self.qt_widget_layout.addWidget(label)


class EditLineWithButtons():
    qt_widget_layout = None
    qt_edit_line = None
    text_on_button_1 = None
    text_on_button_2 = None
    editLineStrValue = ""
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


class ButtonOnLayout ():
    qt_widget_layout = None
    button = None
    def __init__(self, text_on_button,  enabled = True, width=0 ):
        self.qt_widget_layout = QHBoxLayout()
        self.button = QPushButton(text_on_button)
        if enabled is False :
            self.button.setEnabled(False)
        if width > 0 :
            self.button.setFixedWidth(width)
        self.qt_widget_layout.addWidget (self.button)


class ButtonWithCheckBoxes():
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
            self.qt_pin_check_box.setEnabled(False)
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

        if enabled == False:
            self.button.setEnabled(False)
        self.qt_widget_layout.addWidget(self.button)


class CheckBoxes ():
    qt_widget_layout = None
    qt_first_check_box = None
    qt_second_check_box = None
    def __init__(self,   cb1Text = "",  cb2_text = "", label_text = ""  ):
        self.qt_widget_layout = QHBoxLayout()
        if len (cb1Text) > 0 :
            self.qt_first_check_box =  QCheckBox( cb1Text )
            self.qt_widget_layout.addWidget ( self.qt_first_check_box )
        if len (cb2_text) > 0 :
            self.qt_second_check_box =  QCheckBox( cb2_text )
            self.qt_widget_layout.addWidget ( self.qt_second_check_box )
        if len (label_text) > 0 :
            self.qt_widget_layout.addWidget ( QLabel (label_text) )


class RadioButtons():
    qt_widget_layout = None
    currentActive = -1
    qt_radio_butt_1 = None
    qt_radio_butt_2 = None
    qt_radio_butt_3 = None
    qt_radio_butt_4 = None
    qt_radio_butt_5 = None

    def __init__(self, label_text, nameArray, checkedIndex):
        """ MODE """
        qt_lay = QHBoxLayout()
        qt_label_mode = QLabel(label_text)
        qt_lay.addWidget(qt_label_mode)
        qt_radio_group = QButtonGroup()
        qt_radio_group.setExclusive(True)

        if len(nameArray) > 0:
            qt_radio_butt_1 = QRadioButton(nameArray[0])
            self.qt_radio_butt_1 = qt_radio_butt_1
            if checkedIndex == 1:
                qt_radio_butt_1.setChecked(True)
            qt_radio_group.addButton(qt_radio_butt_1, 1)
            qt_lay.addWidget(qt_radio_butt_1)

        if len(nameArray) > 1:
            qt_radio_butt_2 = QRadioButton(nameArray[1])
            self.qt_radio_butt_2 = qt_radio_butt_2
            if checkedIndex == 2:
                qt_radio_butt_2.setChecked(True)
            qt_radio_group.addButton(qt_radio_butt_2, 2)
            qt_lay.addWidget(qt_radio_butt_2)

        if len(nameArray) > 2:
            qt_radio_butt_3 = QRadioButton(nameArray[2])
            self.qt_radio_butt_3 = qt_radio_butt_3
            if checkedIndex == 3:
                qt_radio_butt_3.setChecked(True)
            qt_radio_group.addButton(qt_radio_butt_3, 3)
            qt_lay.addWidget(qt_radio_butt_3)

        if len(nameArray) > 3:
            qt_radio_butt_4 = QRadioButton(nameArray[3])
            self.qt_radio_butt_4 = qt_radio_butt_4
            if checkedIndex == 4:
                qt_radio_butt_4.setChecked(True)
            qt_radio_group.addButton(qt_radio_butt_4, 4)
            qt_lay.addWidget(qt_radio_butt_4)

        if len(nameArray) > 4:
            qt_radio_butt_5 = QRadioButton(nameArray[4])
            self.qt_radio_butt_5 = qt_radio_butt_5
            if checkedIndex == 5:
                qt_radio_butt_5.setChecked(True)
            qt_radio_group.addButton(qt_radio_butt_5, 5)
            qt_lay.addWidget(qt_radio_butt_5)

        self.qt_widget_layout = qt_lay

    def setVisualChecked(self, nr):
        if nr == 1:
            self.qt_radio_butt_1.setChecked(True)
        if nr == 2:
            self.qt_radio_butt_2.setChecked(True)
        if nr == 3:
            self.qt_radio_butt_3.setChecked(True)
        if nr == 4:
            self.qt_radio_butt_4.setChecked(True)
        if nr == 5:
            self.qt_radio_butt_5.setChecked(True)


class WidgetGroup:
    widget_layout = None
    def __init__(self, widgets_list):
        self.widget_layout = QHBoxLayout()
        for wi in widgets_list:
            self.widget_layout.addLayout(wi.widget_layout)
