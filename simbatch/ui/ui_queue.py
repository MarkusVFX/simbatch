# import copy
import subprocess

try:
    from PySide.QtGui import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *
from core.queue import *

class QueueUI():
    list_queue = None
    qt_widget_queue = None

    batch = None
    top_ui = None

    qt_form_edit = None
    qt_form_remove = None

    edit_form_state = 0
    remove_form_state = 0

    qt_edit_fe_name = None
    qt_edit_fe_pror = None
    qt_edit_fe_state = None
    qt_fe_description = None

    freeze_list_on_changed = 0

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.s = batch.s
        self.q = batch.q
        self.comfun = batch.comfun
        self.top_ui = top
        self.mainw = mainw

        list_queue = QListWidget()
        list_queue.setSelectionMode(QAbstractItemView.NoSelection)

        list_queue.setFrameShadow(QFrame.Raised)
        list_queue.currentItemChanged.connect(self.list_queue_current_changed)
        list_queue.setSpacing(1)
        p = list_queue.sizePolicy()
        p.setVerticalPolicy(QSizePolicy.Policy.Maximum)

        list_queue.setContextMenuPolicy(Qt.CustomContextMenu)
        list_queue.customContextMenuRequested.connect(self.on_right_click_show_menu)

        self.list_queue = list_queue

        qt_widget_queue = QWidget()
        self.qt_widget_queue = qt_widget_queue
        qt_lay_queue_main = QVBoxLayout(qt_widget_queue)
        qt_lay_queue_main.setContentsMargins(0, 0, 0, 0);

        qt_lay_queue_list = QHBoxLayout()
        qt_lay_forms = QVBoxLayout()
        qt_lay_queue_buttons = QHBoxLayout()

        # EDIT
        # EDIT EDIT
        # EDIT EDIT EDIT
        qt_form_edit = QWidget()
        self.qt_form_edit = qt_form_edit
        qt_form_edit_layout = QVBoxLayout()
        qt_form_edit.setLayout(qt_form_edit_layout)

        qt_form_edit_layout = QVBoxLayout()

        # fe   form edit
        qt_edit_button_fe_name = EditLineWithButtons("Queue item name: ")
        qt_edit_button_fe_prior = EditLineWithButtons("Priority: ", label_minimum_size=65)
        qt_edit_button_fe_state = EditLineWithButtons("State: ", label_minimum_size=65)
        qt_edit_button_fe_descr = EditLineWithButtons("Description:  ", label_minimum_size=65)
        self.qt_edit_fe_name = qt_edit_button_fe_name.qt_edit_line
        self.qt_edit_fe_pror = qt_edit_button_fe_prior.qt_edit_line
        self.qt_edit_fe_state = qt_edit_button_fe_state.qt_edit_line
        self.qt_fe_description = qt_edit_button_fe_descr.qt_edit_line

        qt_cb_button_save = ButtonWithCheckBoxes("Save changes", pin_text="pin")
        qt_cb_button_save.button.clicked.connect(
            lambda: self.on_click_save_changes(qt_edit_button_fe_name.get_txt(), qt_edit_button_fe_prior.get_txt(),
                                               qt_edit_button_fe_state.get_txt(), qt_edit_button_fe_descr.get_txt()))

        qt_form_edit_layout.addLayout(qt_edit_button_fe_name.qt_widget_layout)
        qt_form_edit_layout.addLayout(qt_edit_button_fe_prior.qt_widget_layout)
        qt_form_edit_layout.addLayout(qt_edit_button_fe_state.qt_widget_layout)
        qt_form_edit_layout.addLayout(qt_edit_button_fe_descr.qt_widget_layout)
        qt_form_edit_layout.addLayout(qt_cb_button_save.qt_widget_layout)

        # TODO
        # qt_gb_edit = QGroupBox()
        # qt_gb_edit.setLayout(qt_form_edit_layout)
        # qt_form_edit_layout.addWidget(qt_gb_edit)

        # REMOVE
        # REMOVE REMOVE
        # REMOVE REMOVE REMOVE
        qt_form_remove = QWidget()
        self.qt_form_remove = qt_form_remove
        qt_form_remove_layout_ext = QVBoxLayout()
        qt_form_remove.setLayout(qt_form_remove_layout_ext)

        qt_form_remove_layout = QFormLayout()

        qt_cb_button_remove = ButtonWithCheckBoxes("Yes, remove", label_text="Remove selected ?        ")

        qt_form_remove_layout.addRow(" ", QLabel("   "))
        qt_form_remove_layout.addRow(" ", qt_cb_button_remove.qt_widget_layout)
        qt_form_remove_layout.addRow(" ", QLabel("   "))
        qt_cb_button_remove.button.clicked.connect(self.on_click_confirm_remove_project)

        qt_gb_remove = QGroupBox()
        qt_gb_remove.setLayout(qt_form_remove_layout)
        qt_form_remove_layout_ext.addWidget(qt_gb_remove)


        self.comfun.add_wigdets(qt_lay_forms, [qt_form_edit, qt_form_remove])

        self.hide_all_forms()

        qt_button_sim_one = QPushButton("Simulate One")
        qt_button_sim_all = QPushButton("Simulate All")
        qt_button_queue_edit = QPushButton("Edit")
        qt_button_queue_remove = QPushButton("Remove from Queue")

        qt_button_sim_one.clicked.connect(self.on_click_sim_one)
        qt_button_sim_all.clicked.connect(self.on_click_sim_all)
        qt_button_queue_edit.clicked.connect(self.on_click_edit)
        qt_button_queue_remove.clicked.connect(self.on_click_remove)

        qt_lay_queue_list.addWidget(list_queue)
        self.comfun.add_wigdets(qt_lay_queue_buttons,
                                [qt_button_sim_one, qt_button_sim_all, qt_button_queue_edit, qt_button_queue_remove])
        self.comfun.add_layouts(qt_lay_queue_main, [qt_lay_queue_list, qt_lay_forms, qt_lay_queue_buttons])

    def reset_list(self):
        self.freeze_list_on_changed = 1
        index = self.batch.q.current_queue_index
        self.clear_list()
        self.batch.init_queue(self.list_queue)
        self.batch.q.current_queue_index = index
        self.batch.q.current_queue_id = self.batch.q.queue_data[self.batch.q.current_queue_index].id
        self.freeze_list_on_changed = 0

    def on_click_menu_set_init(self):
        self.batch.q.queue_data[self.batch.q.current_queue_index].state = "INIT"
        self.batch.q.queue_data[self.batch.q.current_queue_index].state_id = 1  ###  TODO const !
        self.batch.q.save_queue()
        self.reset_list()

    def on_click_menu_set_working(self):
        self.batch.q.queue_data[self.batch.q.current_queue_index].state = "WORKING"
        self.batch.q.queue_data[self.batch.q.current_queue_index].state_id = 4  ###  TODO const !
        self.batch.q.save_queue()
        self.reset_list()

    def on_click_menu_set_done(self):
        self.batch.q.queue_data[self.batch.q.current_queue_index].state = "DONE"
        self.batch.q.queue_data[self.batch.q.current_queue_index].state_id = 11  ###  TODO const !
        self.batch.q.save_queue()
        self.reset_list()

    def on_click_menu_set_hold(self):
        self.batch.q.queue_data[self.batch.q.current_queue_index].state = "HOLD"
        self.batch.q.queue_data[self.batch.q.current_queue_index].state_id = 21  ###  TODO const !
        self.batch.q.save_queue()
        self.reset_list()

    def on_menu_locate_prev(self):
        cur_queue_item = self.batch.q.queue_data[self.batch.q.current_queue_index]
        proj_id = cur_queue_item.proj_id
        task_id = cur_queue_item.task_id
        evo_nr = cur_queue_item.evolution_nr
        version = cur_queue_item.version
        prev_dir = self.batch.d.get_task_prev_dir(forceProjID=proj_id, forceTaskID=task_id, evolution_nr=evo_nr,
                                                  forceQueueVersion=version)

        if self.s.debug_level >= 3:
            print "  [db] DIR : ", task_id, prev_dir

        prev_dir = prev_dir + "\\"
        if self.comfun.path_exists(prev_dir, " prev open "):
            subprocess.Popen('explorer "' + prev_dir + '"')

    def on_menu_open_computed_scene(self):
        cur_queue_item = self.batch.q.queue_data[self.batch.q.current_queue_index]
        proj_id = cur_queue_item.proj_id
        task_id = cur_queue_item.task_id
        evo_nr = cur_queue_item.evolution_nr
        version = cur_queue_item.version

        file_to_load = self.batch.d.get_computed_setup_file(task_id, version, evo_nr)
        if file_to_load[0] == 1:
            if self.s.debug_level >= 1:
                print "\n  [INF]   file_to_load: ", file_to_load[1]
            self.batch.o.soft_conn.load_scene(file_to_load[1])
        else:
            print "\n  [WRN]   file_to_load not exist: ", file_to_load[1]

    def on_click_menu_schema_remove(self):
        self.batch.q.removeQueueItem(index=self.batch.q.current_queue_index, do_save=True)
        self.reset_list()
        print "  remove "

    def on_click_menu_spacer(self):
        print "  ____  "

    def on_right_click_show_menu(self, pos):
        global_cursor_pos = self.list_queue.mapToGlobal(pos)
        qt_right_menu = QMenu()
        qt_right_menu.addAction("Set INIT", self.on_click_menu_set_init)
        qt_right_menu.addAction("Set WORKING", self.on_click_menu_set_working)
        qt_right_menu.addAction("Set DONE", self.on_click_menu_set_done)
        qt_right_menu.addAction("Set HOLD", self.on_click_menu_set_hold)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Locate prev", self.on_menu_locate_prev)
        qt_right_menu.addAction("Open computed scene", self.on_menu_open_computed_scene)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Remove", self.on_click_menu_schema_remove)
        qt_right_menu.exec_(global_cursor_pos)

    def hide_all_forms(self):
        self.qt_form_edit.hide()
        self.qt_form_remove.hide()
        self.edit_form_state = 0
        self.remove_form_state = 0

    def on_click_sim_one(self):
        pass

    def on_click_sim_all(self):
        pass

    def on_click_edit(self):
        if self.edit_form_state == 0:
            self.hide_all_forms()
            self.qt_form_edit.show()
            self.on_click_form_edit_fill()
            self.edit_form_state = 1
        else:
            self.qt_form_edit.hide()
            self.edit_form_state = 0

    def on_click_form_edit_fill(self):
        if self.batch.q.current_queue_index >= 0:
            currQueueItem = self.batch.q.queue_data[self.batch.q.current_queue_index]
            self.qt_edit_fe_name.setText(currQueueItem.queue_item_name)
            self.qt_edit_fe_pror.setText(str(currQueueItem.prior))
            self.qt_edit_fe_state.setText(currQueueItem.state)
            self.qt_fe_description.setText(currQueueItem.description)
        else:
            print " [WRN] Please Select Queue Item"
            self.top_ui.set_top_info(" Please Select Queue Item", 7)

    def add_queue_item_to_list(self, newQueueItem):
        pass

    def add_to_queue_and_update_list(self, formATQ):
        pass

    def on_click_save_changes(self, updatedQueueName, updatedPrior, updatedState, updatedDescription):
        pass

    def on_click_remove(self):
        pass

    def on_click_confirm_remove_project(self):
        pass

    def clear_list(self):
        pass

    def list_queue_current_changed(self, x):
        pass
