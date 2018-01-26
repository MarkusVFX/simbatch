try:
    from PySide.QtGui import *
except ImportError:
    print "PySide.QtGui ERR"

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

        qt_lay_wizard_form = QVBoxLayout()
        # qt_lay_wizard_buttons = QVBoxLayout()

        ###   STEP 1
        qt_lay_step_1a = QVBoxLayout()
        wizard_step_1a = EditLineWithButtons("Project Name:", label_minimum_size=94)
        wizard_step_1b = EditLineWithButtons("Project Directory:", text_on_button_1="Get", label_minimum_size=94,
                                             button_width=50)
        wizard_step_1bb = EditLineWithButtons("Working Directory:", text_on_button_1="Get", label_minimum_size=94,
                                              button_width=50)
        wizard_step_1c = EditLineWithButtons("Initial File or Path:", text_on_button_1="Test", text_on_button_2="Get",
                                             label_minimum_size=94, button_width=50)
        wizard_step_1d = EditLineWithButtons("Description:")
        wizard_but_use_cur_scene = ButtonWithCheckBoxes("Get from current scene", cb2_text="Use current scene",
                                                        cb2_checked=True,
                                                        button_width=150)  # , label_text = "Use label_text"
        wizard_step_create_project = ButtonOnLayout("Create Project", width=180)
        wizard_step_use_curr_scene = ButtonOnLayout("Use Current Project", width=180)
        qt_lay_step_1b = QHBoxLayout()
        self.comfun.add_layouts(qt_lay_step_1b, [wizard_step_create_project.qt_widget_layout,
                                                 SimpleLabel("or", label_maximum=10).qt_widget_layout,
                                                 wizard_step_use_curr_scene.qt_widget_layout])

        ### self s1
        self.s1projNameEL = wizard_step_1a.qt_edit_line
        self.s1projDirEL = wizard_step_1b.qt_edit_line
        self.s1workingDirEL = wizard_step_1bb.qt_edit_line
        self.s1initFileEL = wizard_step_1c.qt_edit_line
        self.s1projDescEL = wizard_step_1d.qt_edit_line
        self.s1CurrentSceneCB = wizard_but_use_cur_scene.qt_second_check_box
        self.comfun.add_layouts(qt_lay_step_1a, [wizard_step_1a.qt_widget_layout, wizard_step_1b.qt_widget_layout,
                                                 wizard_step_1bb.qt_widget_layout, wizard_step_1c.qt_widget_layout,
                                                 wizard_step_1d.qt_widget_layout,
                                                 wizard_but_use_cur_scene.qt_widget_layout, qt_lay_step_1b])

        qt_group_box_step_1 = QGroupBox()
        qt_group_box_step_1.setTitle("1 ) Create  Project")
        qt_group_box_step_1.setLayout(qt_lay_step_1a)
        qt_lay_wizard_form.addWidget(qt_group_box_step_1)

        qt_lay_wizard_main.addWidget(QLabel("Wizard under refactoring !"))
