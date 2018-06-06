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

from widgets import *
from simbatch.core.queue import QueueItem


class AddToQueueForm (QWidget):
    batch = None
    form_atq_local_item = None    # obsolete
    options = []                  # all inputted user's options with parameters

    qt_edit_button_frame_from = None
    qt_edit_button_frame_to = None
    qt_edit_button_sim_from = None
    qt_edit_button_sim_to = None
    qt_edit_button_version = None
    qt_edit_button_prior = None
    qt_gb_add_to_queue_now = None
    qt_lay_actions = None

    qt_edit_button_description = None
    FoQuWiEvolve = None
    execute_button = None

    actions_widgets_array = []
    form_actions_count = 0

    all_actions_array = []
    comfun = None

    def __init__(self, batch):
        QWidget.__init__(self)
        self.batch = batch
        self.form_atq_local_item = self.batch.que.get_blank_queue_item()
        # self.sts = self.batch.sts
        # self.comfun = self.batch.comfun
        self.init_ui_elements()

    def init_ui_elements(self):
        qt_form_add_layout = QVBoxLayout()

        # qt_action_empty = ActionWidget(None, label_txt="    Select Task")
        qt_lay_actions = QVBoxLayout()
        self.qt_lay_actions = qt_lay_actions
        # qt_lay_actions.addWidget(qt_action_empty)
        qt_lay_actions.setSpacing(0)
        qt_lay_actions.setContentsMargins(0, 0, 0, 0)
        qt_gb_actions = QGroupBox()
        qt_gb_actions.setTitle("Actions")
        qt_gb_actions.setLayout(qt_lay_actions)
        qt_form_add_layout.addWidget(qt_gb_actions)

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
        # qt_gb_atq.setLayout(qt_form_add_layout)
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
        # qt_edit_button_sim_from.qt_edit_line.textChanged.connect(self.on_change_sim_from)
        # qt_edit_button_sim_to.qt_edit_line.textChanged.connect(self.on_change_sim_to)
        # qt_edit_button_frame_from.qt_edit_line.textChanged.connect(self.on_change_render_from)
        # qt_edit_button_frame_to.qt_edit_line.textChanged.connect(self.on_change_render_to)

    def update_add_ui(self):
        current_task = self.batch.tsk.current_task
        self.qt_edit_button_sim_from.qt_edit_line.setText(str(current_task.sim_frame_start))
        self.qt_edit_button_sim_to.qt_edit_line.setText(str(current_task.sim_frame_end))
        self.qt_edit_button_frame_from.qt_edit_line.setText(str(current_task.prev_frame_start))
        self.qt_edit_button_frame_to.qt_edit_line.setText(str(current_task.prev_frame_end))
        self.qt_edit_button_prior.qt_edit_line.setText(str(current_task.priority))
        self.qt_edit_button_version.qt_edit_line.setText(str(current_task.task_ver))
        self.qt_edit_button_description.qt_edit_line.setText(current_task.description)

        self.remove_all_action_widgets()
        current_sch = self.batch.sch.get_schema_by_id(current_task.schema_id)
        for act in current_sch.actions_array:
            self.add_action_to_form(act.name, act.actual_value)

    def add_action_to_form(self, info, edit_txt=None, evo=None):
        if edit_txt is None and evo is None:
            wi = SimpleLabel(info)
        else:
            if edit_txt is not None:
                wi = EditLineWithButtons(info, edit_txt)
            else:
                wi = ActionWidgetATQ()
        qt_widget = QWidget()
        qt_widget.setLayout(wi.qt_widget_layout)
        self.qt_lay_actions.addWidget(qt_widget)
        # self.qt_lay_actions.addLayout(wi.qt_widget_layout)

    def remove_all_action_widgets(self):
        # self.actionsWidgetasArray = []
        # self.actionsAllArray = []
        while self.qt_lay_actions.count() > 0:
            b = self.qt_lay_actions.itemAt(0)
            b.widget().deleteLater()
            # b.deleteLater()
            self.qt_lay_actions.takeAt(0)
        # self.actionsCount = 0

    def create_directories(self):
        # TODO
        return True
