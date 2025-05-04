import copy
import os
# import time

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    raise Exception('PySide import ERROR!  Please install PySide or PySide2')

from .widgets import *
from .ui_tasks_forms import AddToQueueForm, TasksFormCreateOrEdit


class TaskListItem(QWidget):
    def __init__(self, txt_id, txt_schema, txt_user, txt_sequence, txt_shot, txt_take, txt_state, txt_schema_version,
                 txt_queue_version, txt_option, txt_comm):
        super(TaskListItem, self).__init__()
        self.qt_widget = QWidget(self)
        self.qt_lay = QHBoxLayout(self.qt_widget)
        self.qt_lay.setSpacing(0)
        self.qt_lay.setContentsMargins(0, 0, 0, 0)
        self.qt_label_font = QFont()
        self.qt_label_font.setPointSize(8)

        self.qt_label_id = QLabel(txt_id)
        self.qt_label_id.setFont(self.qt_label_font)
        self.qt_label_id.setMinimumWidth(22)
        self.qt_label_id.setMaximumWidth(22)
        self.qt_label_id.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_id)

        self.qt_label_user = QLabel(txt_user)
        self.qt_label_user.setFont(self.qt_label_font)
        self.qt_label_user.setMinimumWidth(22)
        self.qt_label_user.setMaximumWidth(22)
        self.qt_label_user.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_user)

        self.qt_label_schema = QLabel(txt_schema)
        self.qt_label_schema.setStyleSheet("""color:#000;text-align:right;padding-left:4px;""")
        # self.qt_label_schema.setFixedHeight(28)
        self.qt_label_schema.setFont(self.qt_label_font)
        self.qt_label_schema.setMinimumWidth(40)
        self.qt_label_schema.setMaximumWidth(220)

        self.qt_lay.addWidget(self.qt_label_schema)

        self.qt_label_state = QLabel(txt_state)
        self.qt_label_state.setStyleSheet("""color:#000;padding-left:4px;""")
        self.qt_label_state.setFont(self.qt_label_font)
        self.qt_label_state.setMinimumWidth(55)
        self.qt_label_state.setMaximumWidth(55)
        self.qt_lay.addWidget(self.qt_label_state)

        self.qt_label_shot = QLabel(txt_sequence)
        self.qt_label_shot.setFont(self.qt_label_font)
        self.qt_label_shot.setStyleSheet("""color:#000;padding-left:4px;""")
        self.qt_label_shot.setMinimumWidth(33)
        self.qt_label_shot.setMaximumWidth(40)
        self.qt_lay.addWidget(self.qt_label_shot)

        self.qt_label_shot = QLabel(txt_shot)
        self.qt_label_shot.setFont(self.qt_label_font)
        self.qt_label_shot.setStyleSheet("""color:#000;""")
        self.qt_label_shot.setMinimumWidth(33)
        self.qt_label_shot.setMaximumWidth(40)
        self.qt_lay.addWidget(self.qt_label_shot)

        self.qt_label_shot = QLabel(txt_take)
        self.qt_label_shot.setFont(self.qt_label_font)
        self.qt_label_shot.setStyleSheet("""color:#000;""")
        self.qt_label_shot.setMinimumWidth(33)
        self.qt_label_shot.setMaximumWidth(40)
        self.qt_lay.addWidget(self.qt_label_shot)

        self.qt_label_schema_version = QLabel(txt_schema_version)
        self.qt_label_schema_version.setFont(self.qt_label_font)
        self.qt_label_schema_version.setStyleSheet("""color:#000;""")
        self.qt_label_schema_version.setMinimumWidth(28)
        self.qt_label_schema_version.setMaximumWidth(40)
        self.qt_lay.addWidget(self.qt_label_schema_version)

        self.qt_label_queue_version = QLabel(txt_queue_version)
        self.qt_label_queue_version.setFont(self.qt_label_font)
        self.qt_label_queue_version.setStyleSheet("""color:#000;""")
        self.qt_label_queue_version.setMinimumWidth(28)
        self.qt_label_queue_version.setMaximumWidth(40)
        self.qt_lay.addWidget(self.qt_label_queue_version)

        self.qt_label_frame_end = QLabel(txt_option)
        self.qt_label_frame_end.setFont(self.qt_label_font)
        self.qt_label_frame_end.setStyleSheet("""color:#000;""")
        self.qt_label_frame_end.setMinimumWidth(31)
        self.qt_label_frame_end.setMaximumWidth(50)
        self.qt_lay.addWidget(self.qt_label_frame_end)

        self.qt_label_prior = QLabel(txt_comm)
        self.qt_label_prior.setFont(self.qt_label_font)
        self.qt_label_prior.setStyleSheet("""color:#000;""")
        self.qt_label_prior.setMinimumWidth(70)
        self.qt_label_prior.setMaximumWidth(170)
        self.qt_lay.addWidget(self.qt_label_prior)

        self.setLayout(self.qt_lay)


class TasksUI:
    list_tasks = None
    qt_widget_tasks = None

    qt_form_create = None
    qt_form_edit = None
    qt_form_remove = None
    qt_form_add = None

    batch = None
    top_ui = None

    create_form_state = 0
    edit_form_state = 0
    remove_form_state = 0
    add_form_state = 0

    comfun = None

    # widgetsInList = []
    array_visible_tasks_ids = []

    current_list_item_index = None
    last_list_item_index = None

    freeze_list_on_changed = 0
    last_task_list_index = None  # used for list item color change to unselected

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.debug_level = batch.sts.debug_level
        self.top_ui = top
        self.mainw = mainw

        # init GUI
        list_tasks = QListWidget()
        list_tasks.setSelectionMode(QAbstractItemView.NoSelection)
        list_tasks.setFrameShadow(QFrame.Raised)
        list_tasks.currentItemChanged.connect(self.on_current_item_changed)
        list_tasks.setSpacing(1)
        p = list_tasks.sizePolicy()
        p.setVerticalPolicy(QSizePolicy.Policy.Maximum)

        list_tasks.setContextMenuPolicy(Qt.CustomContextMenu)
        list_tasks.customContextMenuRequested.connect(self.on_right_click_show_menu)

        self.list_tasks = list_tasks

        qt_widget_tasks = QWidget()
        self.qt_widget_tasks = qt_widget_tasks
        qt_lay_tasks_main = QVBoxLayout(qt_widget_tasks)
        qt_lay_tasks_main.setContentsMargins(0, 0, 0, 0)

        qt_lay_tasks_list = QHBoxLayout()
        qt_lay_tasks_forms = QVBoxLayout()
        qt_lay_tasks_buttons = QHBoxLayout()

        # CREATE
        # CREATE CREATE
        # CREATE CREATE CREATE
        qt_form_create = TasksFormCreateOrEdit(self.batch, mainw, "create")
        self.qt_form_create = qt_form_create
        qt_form_create.execute_button.button.clicked.connect(
            lambda: self.on_click_add_task(qt_form_create.form_task_item))

        # EDIT
        # EDIT EDIT
        # EDIT EDIT EDIT
        qt_form_edit = TasksFormCreateOrEdit(self.batch, mainw, "edit")
        self.qt_form_edit = qt_form_edit
        qt_form_edit.execute_button.button.clicked.connect(
            lambda: self.on_click_update_task(qt_form_edit.form_task_item))

        # REMOVE
        # REMOVE REMOVE
        # REMOVE REMOVE REMOVE
        qt_form_remove = QWidget()
        self.qt_form_remove = qt_form_remove
        qt_form_remove_layout_ext = QVBoxLayout()
        qt_form_remove.setLayout(qt_form_remove_layout_ext)

        qt_form_remove_layout = QFormLayout()

        wfr_buttons = ButtonWithCheckBoxes("Yes, remove", label_text="Remove selected ?        ")
        wfr_buttons.button.clicked.connect(self.on_click_confirmed_remove_task)

        qt_form_remove_layout.addRow(" ", QLabel("   "))
        qt_form_remove_layout.addRow(" ", wfr_buttons.qt_widget_layout)
        qt_form_remove_layout.addRow(" ", QLabel("   "))

        qt_gb_remove = QGroupBox()
        qt_gb_remove.setLayout(qt_form_remove_layout)
        qt_form_remove_layout_ext.addWidget(qt_gb_remove)

        # QUEUE
        # QUEUE QUEUE
        # QUEUE QUEUE QUEUE
        qt_form_add = AddToQueueForm(self.batch)
        self.qt_form_add = qt_form_add
        qt_form_add.execute_button.clicked.connect(self.on_click_add_to_queue)

        # TAB LAY
        # TAB LAY LAY
        # TAB LAY LAY LAY
        self.comfun.add_widgets(qt_lay_tasks_forms, [qt_form_create, qt_form_edit, qt_form_remove, qt_form_add])

        self.hide_all_forms()

        qt_button_create_task = QPushButton("Create")
        qt_button_edit_task = QPushButton("Edit")
        qt_button_remove_task = QPushButton("Remove")
        qt_button_add_to_queue = QPushButton("Add to Queue")

        qt_button_create_task.clicked.connect(self.on_click_show_create_form)
        qt_button_edit_task.clicked.connect(self.on_click_show_edit_form)
        qt_button_remove_task.clicked.connect(self.on_click_show_remove_form)
        qt_button_add_to_queue.clicked.connect(self.on_click_show_add_to_queue_form)

        qt_lay_tasks_list.addWidget(list_tasks)

        self.comfun.add_widgets(qt_lay_tasks_buttons,
                                [qt_button_create_task, qt_button_edit_task, qt_button_remove_task,
                                 qt_button_add_to_queue])

        self.comfun.add_layouts(qt_lay_tasks_main, [qt_lay_tasks_list, qt_lay_tasks_forms, qt_lay_tasks_buttons])

        self.init_tasks()

    def should_filter_task_pass(self, task, filters):   # TODO filters class !
        if filters[0][0] == 1:
            if task.schema_id == filters[0][1]:
                return True
            else:
                return False
        elif filters[1][0] == 1:
            if task.sequence == filters[1][1]:
                if task.shot == filters[1][2]:
                    if task.take == filters[1][3]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    def init_tasks(self, filters=None):
        widget_list = self.list_tasks
        qt_list_item = QListWidgetItem(widget_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)

        list_item_widget = TaskListItem("ID", "task name", "usr", "seq", "sh", "take", "state", "schV", "queV",
                                        "opts", "desc")

        if self.sts.runtime_env == "Houdini":
            color = self.batch.sts.state_colors_rgb_str[0]
            list_item_widget.setStyleSheet("background-color: rgb(" + color + ");")       # uicolor
        else:
            cur_color = self.sts.state_colors[0].color()
            qt_list_item.setBackground(cur_color)


        widget_list.addItem(qt_list_item)
        widget_list.setItemWidget(qt_list_item, list_item_widget)
        qt_list_item.setSizeHint(QSize(1, 24))
        if self.sts.ui_brightness_mode == 0:
            qt_list_item.setBackground(self.sts.state_colors[0])
        else:
            qt_list_item.setBackground(self.sts.state_colors_up[0])

        for tsk in self.batch.tsk.tasks_data:
            filter_pass = True
            if tsk.project_id == self.batch.prj.current_project_id:
                if filters is not None:
                    filter_pass = self.should_filter_task_pass(tsk, filters)

                if filter_pass:
                    qt_list_item = QListWidgetItem(widget_list)
                    list_item_widget = TaskListItem(str(tsk.id), tsk.task_name, str(tsk.user_id),
                                                    tsk.sequence, tsk.shot, tsk.take, tsk.state,
                                                    str(tsk.schema_ver), str(tsk.queue_ver),
                                                    tsk.options, tsk.description)

                    if self.sts.runtime_env == "Houdini":
                        color = self.batch.sts.state_colors_rgb_str[tsk.state_id]
                        list_item_widget.setStyleSheet("background-color: rgb(" + color + ");")       # uicolor
                    else:
                        cur_color = self.sts.state_colors[tsk.state_id].color()
                        qt_list_item.setBackground(cur_color)

                    widget_list.addItem(qt_list_item)
                    widget_list.setItemWidget(qt_list_item, list_item_widget)
                    qt_list_item.setSizeHint(QSize(130, 26))
                    qt_list_item.setBackground(self.sts.state_colors[tsk.state_id])

    def reset_list(self, filters=None):
        self.freeze_list_on_changed = 1
        index = self.batch.tsk.current_task_index
        self.clear_list(with_freeze=False)
        self.init_tasks(filters)
        self.update_list_of_visible_ids(filters)
        if index is not None and isinstance(index, int):
            self.batch.tsk.update_current_from_index(index)
        self.freeze_list_on_changed = 0

    def reload_tasks_data_and_refresh_list(self, filters=None):
        self.batch.tsk.clear_all_tasks_data()
        self.batch.tsk.load_tasks()
        if filters is None:
            filters = self.mainw.current_filters
        self.reset_list(filters=filters)
        self.update_list_of_visible_ids(filters)

    def _change_current_task_state_and_reset_list(self, state_id, filters=None):
        self.batch.tsk.current_task.state = self.sts.states_visible_names[state_id]
        self.batch.tsk.current_task.state_id = state_id
        self.batch.tsk.save_tasks()
        if filters is None:
            filters = self.mainw.current_filters
        self.reset_list(filters=filters)

    def on_list_tasks_double_clicked(self, item):   # list_schemas.itemDoubleClicked.connect(self.on_list_tasks_double_clicked)
        self.batch.logger.db(("on_list_tasks_double_clicked: ", self.tsk.current_task_id, item))
        self.on_menu_open()

    def on_click_menu_set_init(self):
        self._change_current_task_state_and_reset_list(self.sts.INDEX_STATE_INIT)

    def on_click_menu_set_working(self):
        self._change_current_task_state_and_reset_list(self.sts.INDEX_STATE_WORKING)

    def on_click_menu_set_done(self):
        self._change_current_task_state_and_reset_list(self.sts.INDEX_STATE_DONE)

    def on_click_menu_set_hold(self):
        self._change_current_task_state_and_reset_list(self.sts.INDEX_STATE_HOLD)

    def on_click_menu_remove(self):
        self.on_click_confirmed_remove_task()

    def on_click_menu_sch_ver_from_schema(self):
        cur_sch = self.batch.sch.get_schema_by_id(self.batch.tsk.current_task.schema_id)
        self.batch.tsk.current_task.schema_ver = cur_sch.schema_version
        self.batch.tsk.save_tasks()
        self.reset_list()

    def on_click_menu_schema_version_p1(self):
        self.batch.tsk.current_task.schema_ver = 1 + int(
            self.batch.tsk.current_task.schema_ver)
        self.batch.tsk.save_tasks()
        self.reset_list()

    def on_click_menu_schema_version_m1(self):
        self.batch.tsk.current_task.schema_ver = -1 + int(
            self.batch.tsk.current_task.schema_ver)
        self.batch.tsk.save_tasks()
        self.reset_list()

    def on_click_menu_open_base_setup(self):
        if self.batch.tsk.current_task is not None:
            file_to_load = self.batch.sch.get_base_setup(use_task_id=self.batch.tsk.current_task_id)
            if file_to_load is not False:
                self.batch.logger.inf(("loading file: ", file_to_load))

                if self.comfun.file_exists(file_to_load):
                    if self.batch.dfn.current_interactions is not None:
                        self.batch.dfn.current_interactions.open_setup(file_to_load)   # TODO ret and check is open_setup exist!
                    else:
                        self.batch.logger.err(("Current interactions are not loaded"))
                        self.top_ui.set_top_info("Current interactions are not loaded", 8)
                else:
                    self.batch.logger.wrn(("file_to_load not exist:", file_to_load))
                    self.top_ui.set_top_info("Shot setup not exist! ({})".format(file_to_load), 7)
            else:
                self.batch.logger.wrn(("file_to_load not exist:", file_to_load))

    def on_click_menu_open_shot_setup(self):
        if self.batch.tsk.current_task is not None:
            ver = self.batch.tsk.current_task.queue_ver # task_ver
            file_to_load = self.batch.sio.generate_shot_setup_file_name(tsk_id=self.batch.tsk.current_task_id, ver=ver)
            if file_to_load is not False:
                self.batch.logger.inf(("loading file: ", file_to_load))

                if self.comfun.file_exists(file_to_load):
                    if self.batch.dfn.current_interactions is not None:
                        self.batch.dfn.current_interactions.open_setup(file_to_load)   # TODO ret and check is open_setup exist!
                    else:
                        self.batch.logger.err(("Current interactions are not loaded"))
                        self.top_ui.set_top_info("Current interactions are not loaded", 8)
                else:
                    self.batch.logger.wrn(("file_to_load not exist:", file_to_load))
                    self.top_ui.set_top_info("Shot setup not exist! ({})".format(file_to_load), 7)
            else:
                self.batch.logger.wrn(("file_to_load not exist:", file_to_load))

    @staticmethod
    def on_click_menu_spacer():
        pass

    def on_right_click_show_menu(self, pos):
        global_cursor_pos = self.list_tasks.mapToGlobal(pos)
        qt_right_menu = QMenu()
        qt_right_menu.addAction("Open Base Setup ", self.on_click_menu_open_base_setup)
        qt_right_menu.addAction("Open Shot Setup ", self.on_click_menu_open_shot_setup)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Sch Ver Form Schema", self.on_click_menu_sch_ver_from_schema)
        qt_right_menu.addAction("Sch Ver +1", self.on_click_menu_schema_version_p1)
        qt_right_menu.addAction("Sch Ver -1", self.on_click_menu_schema_version_m1)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Set INIT", self.on_click_menu_set_init)
        qt_right_menu.addAction("Set WORKING", self.on_click_menu_set_working)
        qt_right_menu.addAction("Set DONE", self.on_click_menu_set_done)
        qt_right_menu.addAction("Set HOLD", self.on_click_menu_set_hold)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Remove Task", self.on_click_menu_remove)
        qt_right_menu.exec_(global_cursor_pos)

    def hide_all_forms(self):
        self.qt_form_create.hide()
        self.qt_form_edit.hide()
        self.qt_form_remove.hide()
        self.qt_form_add.hide()
        self.create_form_state = 0
        self.edit_form_state = 0
        self.remove_form_state = 0
        self.add_form_state = 0

    def on_click_show_create_form(self):
        if self.create_form_state == 0:
            self.hide_all_forms()
            if self.batch.tsk.current_task_index is not None and self.batch.tsk.current_task_index >= 0:
                curr_task = self.batch.tsk.tasks_data[self.batch.tsk.current_task_index]
                self.qt_form_create.update_create_ui(curr_task.schema_id)
            elif self.batch.sch.current_schema_index is not None and self.batch.sch.current_schema_index >= 0:
                cur_sch = self.batch.sch.schemas_data[self.batch.sch.current_schema_index]
                self.qt_form_create.update_create_ui(schema_id=cur_sch.id)
            else:
                self.qt_form_create.update_create_ui()
            self.qt_form_create.get_frame_range_from_scene()
            self.qt_form_create.show()
            self.create_form_state = 1
        else:
            self.qt_form_create.hide()
            self.create_form_state = 0

    def on_click_show_edit_form(self):
        if self.edit_form_state == 0:
            self.hide_all_forms()
            if self.batch.tsk.current_task_index is not None:
                self.qt_form_edit.update_edit_ui(self.batch.tsk.current_task)
                self.qt_form_edit.show()
                self.edit_form_state = 1
            else:
                self.batch.logger.wrn("(on_click_show_edit_form) Please Select Task")
                self.top_ui.set_top_info("Please select task first", 7)
        else:
            self.qt_form_edit.hide()
            self.edit_form_state = 0

    def on_click_show_remove_form(self):
        if self.remove_form_state == 0:
            if self.batch.tsk.current_task_id is not None:
                self.hide_all_forms()
                self.qt_form_remove.show()
                self.remove_form_state = 1
            else:
                self.batch.logger.wrn("(on_click_show_remove_form) Please Select Task")
                self.top_ui.set_top_info("Please select task first", 7)
        else:
            self.qt_form_remove.hide()
            self.remove_form_state = 0

    def on_click_show_add_to_queue_form(self):
        if self.add_form_state == 0:
            if self.batch.tsk.current_task_id is not None:
                self.hide_all_forms()
                self.qt_form_add.show()
                self.qt_form_add.update_form()
                self.batch.tsk.update_proxy_task_form_current()
                self.add_form_state = 1
            else:
                self.batch.logger.wrn("(on_click_show_add_to_queue_form) Please Select Task")
                self.top_ui.set_top_info("Please select task first", 7)
        else:
            self.qt_form_add.hide()
            self.add_form_state = 0

    def add_single_task(self, new_task_item):
        new_task_item.id = self.batch.tsk.add_task(new_task_item, do_save=True)
        qt_list_item = QListWidgetItem(self.list_tasks)
        list_item_widget = TaskListItem(str(new_task_item.id), new_task_item.task_name, str(new_task_item.user_id),
                                        new_task_item.sequence, new_task_item.shot, new_task_item.take,
                                        new_task_item.state, str(new_task_item.schema_ver),
                                        str(new_task_item.queue_ver), new_task_item.options, new_task_item.description)

        if self.sts.runtime_env == "Houdini":
            color = self.batch.sts.state_colors_rgb_str[new_task_item.state_id]
            list_item_widget.setStyleSheet("background-color: rgb(" + color + ");")       # uicolor

        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)
        qt_list_item.setSizeHint(QSize(1, 24))
        self.list_tasks.addItem(qt_list_item)
        self.list_tasks.setItemWidget(qt_list_item, list_item_widget)
        return new_task_item.id

    def on_click_add_task(self, new_task_tem):
        if self.batch.prj.current_project_id >= 0:
            if self.qt_form_create.qt_schema_name_combo.currentIndex() >= 0:
                self.qt_form_create.compile_inputs()
                if new_task_tem.schema_id < 0:
                    self.batch.logger.err(("(on_click_add_task) wrong schema_id: ", new_task_tem.schema_id))

                check_task = self.batch.tsk.check_is_task_exist(new_task_tem)
                if check_task is False:
                    new_task_id = self.add_single_task(copy.copy(new_task_tem))
                    self.top_ui.set_top_info(" [INF] Task created, active task: [{}] {}".format(new_task_id,
                                                                                                new_task_tem.task_name))
                    self.qt_form_add.hide()
                    self.add_form_state = 0

                    self.reload_tasks_data_and_refresh_list()

                    self.batch.tsk.update_current_from_id(new_task_id)
                else:
                    self.batch.logger.err("Task exist [{}], nothing added".format(check_task))
                    self.top_ui.set_top_info("Task exist, id:{}. Skiping add!".format(check_task), 7)
            else:
                self.batch.logger.err("(on_click_add_task) PLEASE SELECT SCHEMA ")
                self.top_ui.set_top_info(" [INF] PLEASE SELECT SCHEMA !", 8)
        else:
            self.batch.logger.wrn(("(on_click_add_task) wrong current_project_id: ", self.batch.prj.current_project_id))
            self.top_ui.set_top_info("Please select project first !", 8)

    def on_click_update_task(self, edited_task_item):
        self.qt_form_edit.compile_inputs()

        check_task = self.batch.tsk.check_is_task_exist(edited_task_item)
        if check_task is False:
            self.batch.tsk.update_task(copy.copy(edited_task_item), do_save=True)

            current_list_index = self.list_tasks.currentRow()
            ed_item = self.list_tasks.item(current_list_index)
            list_item_widget = TaskListItem(str(edited_task_item.id), edited_task_item.task_name,
                                            str(edited_task_item.user_id),
                                            edited_task_item.sequence, edited_task_item.shot, edited_task_item.take,
                                            edited_task_item.state, str(edited_task_item.schema_ver),
                                            str(edited_task_item.queue_ver), edited_task_item.options,
                                            edited_task_item.description)

            self.list_tasks.setItemWidget(ed_item, list_item_widget)

            self.qt_form_add.hide()
            self.add_form_state = 0
            self.batch.logger.inf("task updated")
            self.top_ui.set_top_info("Task id:{} updated".format(check_task), 4)
        else:
            self.batch.logger.err("Task exist [{}], skiping update".format(check_task))
            self.top_ui.set_top_info("Task exist, id:{}. Skiping update!".format(check_task), 7)

    def on_click_confirmed_remove_task(self):
        self.batch.logger.db(("remove_task", self.batch.tsk.current_task_index, self.batch.tsk.current_task_id,
                              self.current_list_item_index))
        if self.batch.tsk.current_task_index >= 0:
            take_item_list = self.current_list_item_index + 1
            self.batch.tsk.remove_single_task(index=self.batch.tsk.current_task_index, do_save=True)
            self.last_list_item_index = None
            self.batch.tsk.current_task_index = None
            self.current_list_item_index = None
            self.list_tasks.takeItem(take_item_list)
            self.qt_form_remove.hide()
            self.remove_form_state = 0
        else:
            self.top_ui.set_top_info("Please select task first", 7)

    """
    def print_form_add(self):
        form_add = self.qt_form_add
        self.comfun.print_list(form_add.actionsAllArray)
        for ak in form_add.actions_widgets_array:
            if ak.is_evo == 1:
                self.batch.logger.deepdb((" is_evo:", ak.is_evo,  "   scr:", ak.script_type, ak.script))
            else:
                self.batch.logger.deepdb(("not is_evo:", ak.is_evo, "   scr:", ak.script_type, ak.script))
    """

    """ marker ATQ 010a   on click add   """
    def on_click_add_to_queue(self):    # event from: ui_tasks_form (Add to queue now)
        form_atq = self.qt_form_add
        # self.actions_options.append(self.form_task_item.description)
        # marker ATQ 100
        form_atq.collect_options_from_widgets()
        # current_task_id = self.batch.tsk.current_task_id
        current_task = self.batch.tsk.current_task
        if current_task is not None:
            ret = form_atq.create_directories()  # TODO
            if ret:
                # self.batch.tsk.update_proxy_task_form_current()

                self.batch.tsk.increase_queue_ver()

                self.batch.tsk.proxy_task.queue_ver = self.batch.tsk.current_task.queue_ver
                # marker ATQ 200
                form_queue_items = self.batch.que.generate_queue_items(self.batch.tsk.current_task.id,
                                                                       schema_options=form_atq.schema_options,
                                                                       task_options=form_atq.task_options)
                if form_queue_items is not None and len(form_queue_items) > 0:
                    self.batch.logger.db("{} items generated !".format(len(form_queue_items)))
                    self.batch.que.clear_all_queue_items()
                    self.batch.que.load_queue()
                    self.batch.que.add_to_queue(form_queue_items, do_save=True)
                    self.mainw.que_ui.update_all_queue()
                else:
                    self.batch.logger.wrn(("queue items NOT generated !", self.batch.tsk.current_task.id))
                    self.batch.tsk.current_task.state_id = self.sts.INDEX_STATE_ERROR
                    self.batch.tsk.current_task.state = self.sts.states_visible_names[self.sts.INDEX_STATE_ERROR]
                    self.batch.tsk.save_tasks()

                self.freeze_list_on_changed = 1
                self.last_task_list_index = -1

                filters = self.mainw.current_filters
                self.reset_list(filters=filters)

                self.freeze_list_on_changed = 0
                # self.qt_form_add.update_form()
                # self.batch.tsk.update_proxy_task_form_current()

                if form_queue_items is not None:
                    self.batch.logger.db(" added to queue !!!")
                    self.top_ui.set_top_info(" added to queue ", 2)
                    # self.qt_form_create.update_create_ui(self.batch.tsk.current_task.schema_id)
                    v_zeros = self.batch.prj.current_project.zeros_in_version
                    curr_ver = self.batch.tsk.current_task.queue_ver
                    curr_ver_str = self.comfun.str_with_zeros(curr_ver, v_zeros)
                    next_ver = self.batch.tsk.current_task.queue_ver + 1
                    next_ver_str = self.comfun.str_with_zeros(next_ver, v_zeros)
                    for a in form_atq.actions_widgets_array:
                        atxt = a.qt_edit_line_widget.qt_edit_line.text()
                        if "_v"+curr_ver_str in atxt:
                            updated_atxt = atxt.replace("_v"+curr_ver_str, "_v"+next_ver_str)
                            a.qt_edit_line_widget.qt_edit_line.setText(updated_atxt)
                            print(updated_atxt)
                else:
                    self.top_ui.set_top_info("Items not added to queue !", 9)
            else:
                self.batch.logger.err("Add to queue: can't create output directory !")
                self.top_ui.set_top_info(" ERR: can't create output directory ", 9)
        else:
            self.batch.logger.wrn("Current task undefined! Please select task again.")
            self.top_ui.set_top_info("Please select task ", 7)

    def clear_list(self, with_freeze=True):
        if with_freeze:
            self.freeze_list_on_changed = 1
        while self.list_tasks.count() > 0:
            self.list_tasks.takeItem(0)
        if with_freeze:
            self.freeze_list_on_changed = 0

    def update_all_tasks(self, filters=None):
        self.clear_list()
        self.init_tasks(filters)
        self.update_list_of_visible_ids(filters)

    def update_list_of_visible_ids(self, filters=None):
        array_visible_tasks_ids = []
        for task in self.batch.tsk.tasks_data:
            filter_pass = True
            if task.project_id == self.batch.prj.current_project_id:
                if filters is not None:
                    filter_pass = self.should_filter_task_pass(task, filters)
                if filter_pass:
                    array_visible_tasks_ids.append(task.id)
        self.array_visible_tasks_ids = array_visible_tasks_ids

    def item_set_background(self, item, color_index, up=False):
        if self.sts.runtime_env == "Houdini":

            if up:
                color = self.batch.sts.state_colors_up_rgb_str[color_index]
            else:
                color = self.batch.sts.state_colors_rgb_str[color_index]

            edited_task_item = self.batch.tsk.current_task       #   TODO  huodini list item set background !!!!
            list_item_widget = TaskListItem(str(edited_task_item.id), edited_task_item.task_name,
                                            str(edited_task_item.user_id),
                                            edited_task_item.sequence, edited_task_item.shot, edited_task_item.take,
                                            edited_task_item.state, str(edited_task_item.schema_ver),
                                            str(edited_task_item.queue_ver), edited_task_item.options,
                                            edited_task_item.description)

            list_item_widget.setStyleSheet("background-color: rgb(" + color + ");")        # uicolor
            self.list_tasks.setItemWidget(item, list_item_widget)

        else:
            if up:
                color = self.batch.sts.state_colors_up[color_index].color()
            else:
                color = self.batch.sts.state_colors[color_index].color()
            item.setBackground(color)

    def on_current_item_changed(self, current_task_item):
        if self.freeze_list_on_changed == 1:   # freeze update changes on massive action    i.e  clear_list()
            self.batch.logger.deepdb(("tsk chngd freeze_list_on_changed", self.list_tasks.currentRow()))
        else:
            self.batch.logger.db(("list_task_current_item_changed: ", self.list_tasks.currentRow()))
            self.last_task_list_index = self.current_list_item_index
            current_list_index = self.list_tasks.currentRow() - 1
            self.current_list_item_index = current_list_index

            if self.last_task_list_index is not None:
                if self.last_task_list_index is not None and self.last_task_list_index < len(self.batch.tsk.tasks_data):
                    item = self.list_tasks.item(self.last_task_list_index + 1)
                    if item is not None and self.last_task_list_index < len(self.array_visible_tasks_ids):
                        last_id = self.array_visible_tasks_ids[self.last_task_list_index]
                        last_index = self.batch.tsk.get_index_by_id(last_id)
                        if last_index is not None:
                            color_index = self.batch.tsk.tasks_data[last_index].state_id
                            # item.setBackground(self.batch.sts.state_colors[color_index].color())
                            self.item_set_background(item, color_index)
                else:
                    self.batch.logger.wrn("Wrong last_task_list_index {} vs {} ".format(self.last_task_list_index,
                                                                                        len(self.batch.tsk.tasks_data)))
            else:
                self.batch.logger.db("last_task_list_index is None")

            if len(self.array_visible_tasks_ids) <= current_list_index:
                self.update_list_of_visible_ids()  # TODO move  to init / change list
                if len(self.array_visible_tasks_ids) > current_list_index:
                    self.batch.logger.deepdb(("vis ids FIXED: len(array_visible_tasks_ids):",
                                              len(self.array_visible_tasks_ids),
                                              "vs current_list_index:", current_list_index))
                else:
                    self.batch.logger.err(("vis ids NOT FIXED: len(array_visible_tasks_ids):",
                                           len(self.array_visible_tasks_ids),
                                           "vs current_list_index:", current_list_index))

            if 0 <= current_list_index < len(self.array_visible_tasks_ids):
                current_task_id = self.array_visible_tasks_ids[current_list_index]
                self.batch.tsk.current_task_id = current_task_id
                self.batch.tsk.update_current_from_id(current_task_id)

            current_task_index = self.batch.tsk.current_task_index
            if 0 <= current_task_index < len(self.batch.tsk.tasks_data):
                cur_task = self.batch.tsk.tasks_data[current_task_index]
                if self.top_ui is not None:
                    self.top_ui.set_top_info("[{}]    {}".format(cur_task.id, cur_task.task_name))
                else:
                    self.batch.logger.err("top_ui is None")

                if current_list_index >= 0:
                    item_c = self.list_tasks.item(current_list_index + 1)
                    # cur_color = self.batch.sts.state_colors_up[cur_task.state_id].color()
                    # item_c.setBackground(cur_color)
                    self.item_set_background(item_c, cur_task.state_id, up=True)

                # update SCHEMA
                self.batch.sch.current_schema_id = cur_task.schema_id
                self.batch.sch.update_current_from_id(cur_task.schema_id)

                # update TASK form
                if self.create_form_state == 1:
                    self.qt_form_create.update_create_ui(cur_task.schema_id)   # update create task form
                if self.edit_form_state == 1:
                    self.qt_form_edit.update_edit_ui(cur_task)                 # update edit form
                if self.add_form_state == 1:
                    self.qt_form_add.update_form()                           # update add to queue form
                    self.batch.tsk.update_proxy_task_form_current()
                    # self.list_tasks.scrollTo(current_list_index)
                    # self.list_tasks.scrollTo(current_task_item)
                    # self.list_tasks.scrollToBottom()

                    # self.list_tasks.updateGeometry()
                    # self.list_tasks.scrollToItem(current_task_item)

            else:
                self.batch.logger.err("on chng list task {} < {}".format(current_task_index,
                                                                         len(self.batch.tsk.tasks_data)))
