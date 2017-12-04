try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    print "PySide.QtGui ERR"

from ui_queue import QueueItem
from widgets import *


class AddToQueueForm (QWidget):
    batch = None
    form_atq_local_item = None

    qt_edit_button_frame_from = None
    qt_edit_button_frame_to = None
    qt_edit_button_sim_from = None
    qt_edit_button_sim_to = None
    qt_edit_button_version = None
    qt_edit_button_prior = None

    qt_edit_button_description = None
    FoQuWiEvolve = None
    execute_button = None

    actions_widgets_array = []
    actionsCount = 0

    all_actions_array = [] 
    comfun = None

    def __init__( self, batch):
        QWidget.__init__(self)
        self.form_atq_local_item = QueueItem(0, "", 1, "M", 1, "", "", "", 10, 20, "" ,2 ,"ver" , "evo" ,1 ,"" ,"", 50,
                                             " 1 ", "", 0, "", 1, 3)
        self.batch = batch
        self.s = self.batch.s
        self.comfun = self.batch.comfun
        self.init_ui_elements()

    def init_ui_elements(self):
        qt_form_add_layout = QVBoxLayout()

        qt_action_empty = Action(label_txt="    Select Task")
        qt_lay_actions = QVBoxLayout()
        self.qt_lay_actions = qt_lay_actions
        qt_lay_actions.addWidget(qt_action_empty)
        qt_lay_actions.setSpacing(0)
        qt_lay_actions.setContentsMargins(0, 0, 0, 0)
        qt_gb_actions = QGroupBox()
        qt_gb_actions.setTitle("Actions")
        qt_gb_actions.setLayout(qt_lay_actions)
        qt_form_add_layout.addWidget(qt_gb_actions)
        self.qt_gb_actions = qt_gb_actions

        qt_edit_button_version = EditLineWithButtons("version")
        qt_edit_button_prior = EditLineWithButtons("prior")
        qt_edit_button_sim_from = EditLineWithButtons("sim from")
        qt_edit_button_sim_to = EditLineWithButtons("sim to")
        qt_edit_button_frame_from = EditLineWithButtons("start")
        qt_edit_button_frame_to = EditLineWithButtons("end")

        qt_edit_button_description = EditLineWithButtons("desc", label_minimum_size=60)

        qt_button_cb_add_to_queue = ButtonWithCheckBoxes("Add To Queue Now!", label_text="  pin ?  ")

        qt_widget_group_frame_range = WidgetGroup(
            [qt_edit_button_version, qt_edit_button_prior, qt_edit_button_sim_from, qt_edit_button_sim_to,
             qt_edit_button_frame_from, qt_edit_button_frame_to])

        qt_form_add_layout.addLayout(qt_widget_group_frame_range.qt_widget_layout)
        qt_form_add_layout.addLayout(qt_edit_button_description.qt_widget_layout)
        qt_form_add_layout.addLayout(qt_button_cb_add_to_queue.qt_widget_layout)

        qt_gb_atq = QGroupBox()
        qt_gb_atq.setLayout(qt_form_add_layout)
        self.qt_gb_add_to_queue_now = qt_gb_atq
        qt_form_add_layout.addWidget(qt_gb_atq)

        self.qt_edit_button_sim_from = qt_edit_button_sim_from
        self.qt_edit_button_sim_to = qt_edit_button_sim_to
        self.qt_edit_button_frame_from = qt_edit_button_frame_from
        self.qt_edit_button_frame_to = qt_edit_button_frame_to
        self.qt_edit_button_prior = qt_edit_button_prior
        self.qt_edit_button_version = qt_edit_button_version
        self.qt_edit_button_description = qt_edit_button_description
        self.execute_button = qt_button_cb_add_to_queue.button

        self.setLayout(qt_form_add_layout)
        qt_edit_button_sim_from.qt_edit_line.textChanged.connect(self.on_change_sim_from)
        qt_edit_button_sim_to.qt_edit_line.textChanged.connect(self.on_change_sim_to)
        qt_edit_button_frame_from.qt_edit_line.textChanged.connect(self.on_change_render_from)
        qt_edit_button_frame_to.qt_edit_line.textChanged.connect(self.on_change_render_to)