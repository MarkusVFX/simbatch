import copy
# import time

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *
from core.tasks import *
from ui_tasks_atqf import AddToQueueForm


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
        self.qt_label_schema.setFixedHeight(28)
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
        self.qt_label_frame_end.setMinimumWidth(26)
        self.qt_label_frame_end.setMaximumWidth(26)
        self.qt_lay.addWidget(self.qt_label_frame_end)

        self.qt_label_prior = QLabel(txt_comm)
        self.qt_label_prior.setFont(self.qt_label_font)
        self.qt_label_prior.setStyleSheet("""color:#000;""")
        self.qt_label_prior.setMinimumWidth(70)
        self.qt_label_prior.setMaximumWidth(170)
        self.qt_lay.addWidget(self.qt_label_prior)

        self.setLayout(self.qt_lay)


class TasksFormCreateOrEdit(QWidget):
    form_mode = 1  # 1 create    2 edit
    form_task_item = None  # store new or edited data as TaskItem

    batch = None
    mainw = None

    schemas_id_array = []

    # GUI QT elements
    qt_fae_schema_description_edit = None
    qt_schema_name_combo = None
    qt_combo_state_names = None

    qt_edit_line_sequence = None
    qt_edit_line_shot = None
    qt_edit_line_take = None
    qt_edit_line_priority = None
    qt_edit_line_version = None

    qt_edit_line_frame_start = None
    qt_edit_line_frame_end = None
    execute_button = None

    # shAQLine = None
    # shBQLine = None
    # shCQLine = None
    # priorQLine = None
    # verQLine = None
    # frStaQLine = None
    # frEndQLine = None

    def __init__(self, batch, mainw, mode):
        QWidget.__init__(self)

        self.batch = batch
        self.mainw = mainw
        self.top_ui = mainw.top_ui
        self.s = batch.s
        if mode == "edit":
            self.form_mode = 2

        self.schemas_id_array = []

        self.form_task_item = TaskItem(0, "def", 1, "NULL", 1, 1, "01", "001", "", 4, 8, 5, 8, 1, 1, 1, "", 1, 50, "")

        self.init_ui_elements(batch.c)
        #self.schemas_id_array = batch.c.schemas_id_array # TODO  visible isd  VS proj's schemas

    def init_ui_elements(self, sch):
        qt_layout_out_form_create = QVBoxLayout()
        qt_layout_form_create = QVBoxLayout()
        qt_layout_combo_form_create = QHBoxLayout()

        qt_combo_schema_name = ComboLabel("", sch.get_schema_names())
        self.qt_schema_name_combo = qt_combo_schema_name.combo
        qt_combo_state = ComboLabel("", ["NULL", "INIT", "WAITING", "HOLD", "QUEUED"])
        self.qt_combo_state_names = qt_combo_state.combo

        qt_edit_buton_sequence = EditLineWithButtons("Sequence ", label_minimum_size=70)
        self.qt_edit_line_sequence = qt_edit_buton_sequence.qt_edit_line
        qt_edit_buton_shot = EditLineWithButtons("Shot ", label_minimum_size=50, align_right=1)
        self.qt_edit_line_shot = qt_edit_buton_shot.qt_edit_line
        qt_edit_buton_take = EditLineWithButtons("Take ", label_minimum_size=50, align_right=1)
        self.qt_edit_line_take = qt_edit_buton_take.qt_edit_line
        qt_edit_buton_prior = EditLineWithButtons("Prior ", label_minimum_size=50, align_right=1)
        self.qt_edit_line_priority = qt_edit_buton_prior.qt_edit_line
        qt_edit_buton_version = EditLineWithButtons("Ver ", label_minimum_size=50, align_right=1)
        self.qt_edit_line_version = qt_edit_buton_version.qt_edit_line

        qt_edit_buton_start = EditLineWithButtons("Start ", label_minimum_size=50, align_right=1)
        self.qt_edit_line_frame_start = qt_edit_buton_start.qt_edit_line
        qt_edit_buton_end = EditLineWithButtons("End ", label_minimum_size=50, align_right=1)
        self.qt_edit_line_frame_end = qt_edit_buton_end.qt_edit_line

        qt_button_lay_detect_framerange = ButtonOnLayout("Detect from cache")
        qt_button_lay_get_framerange = ButtonOnLayout("Get from scene")

        qt_button_lay_detect_framerange.button.clicked.connect(self.get_frame_range_from_cache)
        qt_button_lay_get_framerange.button.clicked.connect(self.get_frame_range_from_scene)

        qt_widget_group_shot = WidgetGroup(
            [qt_edit_buton_sequence, qt_edit_buton_shot, qt_edit_buton_take, qt_edit_buton_prior,
             qt_edit_buton_version])
        qt_widget_group_time_range = WidgetGroup(
            [qt_edit_buton_start, qt_edit_buton_end, qt_button_lay_detect_framerange, qt_button_lay_get_framerange])

        qt_edit_buton_description = EditLineWithButtons("Description ")
        self.qt_fae_schema_description_edit = qt_edit_buton_description.qt_edit_line

        if self.form_mode == 1:
            qt_button_cb_create_save_task = ButtonWithCheckBoxes("Create task", label_text=" ", pin_text="pin")
        else:
            qt_button_cb_create_save_task = ButtonWithCheckBoxes("Save task", label_text=" ")

        qt_layout_combo_form_create.addLayout(qt_combo_schema_name.qt_widget_layout)
        qt_layout_combo_form_create.addLayout(qt_combo_state.qt_widget_layout)

        qt_layout_form_create.addLayout(qt_layout_combo_form_create)

        qt_layout_form_create.addLayout(qt_widget_group_shot.qt_widget_layout)
        qt_layout_form_create.addLayout(qt_widget_group_time_range.qt_widget_layout)

        qt_layout_form_create.addLayout(qt_edit_buton_description.qt_widget_layout)
        qt_layout_form_create.addLayout(qt_button_cb_create_save_task.qt_widget_layout)

        qt_gb_create_edit = QGroupBox()
        if self.form_mode == 1:
            qt_gb_create_edit.setTitle("Create Task")
        else:
            qt_gb_create_edit.setTitle("Edit Task")
        qt_gb_create_edit.setLayout(qt_layout_form_create)
        qt_layout_out_form_create.addWidget(qt_gb_create_edit)

        self.execute_button = qt_button_cb_create_save_task

        self.setLayout(qt_layout_out_form_create)

    def update_create_ui(self, schema_id=-1):
        self.qt_combo_state_names.setCurrentIndex(1)
        print " update ", schema_id
        if schema_id == -1:
            print " ____update ", self.qt_schema_name_combo.count()
            self.qt_schema_name_combo.setCurrentIndex(self.qt_schema_name_combo.count() - 1)
        else:
            arr_index = 0
            for arrEl in self.schemas_id_array:
                if arrEl == schema_id:
                    print " ____set ", arr_index
                    self.qt_schema_name_combo.setCurrentIndex(arr_index)
                arr_index += 1

    def update_edit_ui(self, cur_task):
        self.qt_combo_state_names.setCurrentIndex(self.qt_combo_state_names.findText(cur_task.state))

        arr_index = 0
        for arrEl in self.schemas_id_array:
            if arrEl == cur_task.schema_id:
                print " ____set edit  ", arr_index
                self.qt_schema_name_combo.setCurrentIndex(arr_index)
            arr_index += 1

        self.form_task_item = cur_task
        self.qt_edit_line_sequence.setText(cur_task.shot_A)
        self.qt_edit_line_shot.setText(cur_task.shot_B)
        self.qt_edit_line_take.setText(cur_task.shot_C)

        self.qt_edit_line_frame_start.setText(str(cur_task.frame_from))
        self.qt_edit_line_frame_end.setText(str(cur_task.frame_to))

        self.qt_edit_line_priority.setText(str(cur_task.prior))
        self.qt_edit_line_version.setText(str(cur_task.schema_ver))

        self.qt_fae_schema_description_edit.setText(cur_task.description)

    def update_schemas_id_arr(self, schemas_id_array):  # TODO check is it necessary / remove
        self.schemas_id_array = schemas_id_array

    # update combo box after project change or schema add, rem
    def update_schema_names_combo(self, combo_current_index=None):
        combo_items_arr = self.mainw.sch_ui.current_project_schemas_names
        schemas_id_array = self.mainw.sch_ui.current_project_schemas_ids

        self.qt_schema_name_combo.clear()
        self.update_schemas_id_arr(schemas_id_array)
        for it in combo_items_arr:
            self.qt_schema_name_combo.addItem(it)
        if combo_current_index is not None:
            self.qt_schema_name_combo.setCurrentIndex(combo_current_index)

    def compile_imputs(self):
        self.form_task_item.task_name = self.qt_schema_name_combo.currentText()
        if self.qt_schema_name_combo.currentIndex() >= 0:
            if self.s.debug_level >= 5:
                print "[db sch on tsk a] ", self.qt_schema_name_combo.currentIndex()
                print "[db sch on tsk c] ", self.schemas_id_array
            if len(self.schemas_id_array) > 0:
                if self.s.debug_level >= 5:
                    print "[db sch on tsk b] ", self.schemas_id_array[0], len(self.schemas_id_array)
            if len(self.schemas_id_array) > self.qt_schema_name_combo.currentIndex():
                self.form_task_item.schema_id = self.schemas_id_array[self.qt_schema_name_combo.currentIndex()]
            else:
                if self.s.debug_level >= 1:
                    print "  [ERR74]  compile_imputs   ", len(self.schemas_id_array)
                    print "  [ERR74]  compile_imputs   ", self.qt_schema_name_combo.currentIndex()
        else:
            self.form_task_item.schema_id = -1
            if self.s.debug_level >= 1:
                print "   [WRN] (compile_imputs)  schema_name_combo:", self.qt_schema_name_combo.currentIndex

        if self.batch.c.current_schema_index is None:   # TODO check it
            if self.s.debug_level >= 1:
                print "\n     [ERR] (compile_imputs)  self.sch.curr_schema_index: ", self.batch.c.current_schema_index

        if self.batch.p.current_project_id is not None:
            self.form_task_item.project_id = self.batch.p.current_project_id

        self.form_task_item.state_color = "3478b8"
        self.form_task_item.state = self.qt_combo_state_names.currentText()
        self.form_task_item.state_id = self.qt_combo_state_names.currentIndex()

        self.form_task_item.schema_ver = (self.batch.c.get_schema_by_id(self.form_task_item.schema_id)).schema_version
        self.form_task_item.queue_ver = 0

        self.form_task_item.shot_A = self.qt_edit_line_sequence.text()
        self.form_task_item.shot_B = self.qt_edit_line_shot.text()
        self.form_task_item.shot_C = self.qt_edit_line_take.text()

        self.form_task_item.frame_from = self.batch.comfun.int_or_val(self.qt_edit_line_frame_start.text(), 0)
        self.form_task_item.frame_to = self.batch.comfun.int_or_val(self.qt_edit_line_frame_end.text(), 0)

        if self.qt_edit_line_priority.text().isdigit():
            self.form_task_item.prior = int(self.qt_edit_line_priority.text())
        else:
            self.form_task_item.prior = 50

        self.form_task_item.schema_ver = self.batch.comfun.int_or_val(self.qt_edit_line_version.text(), 1)

        self.form_task_item.description = self.qt_fae_schema_description_edit.text()

    def get_frame_range_from_cache(self):
        hack__a = self.qt_edit_line_sequence.text()
        hack__b = self.qt_edit_line_shot.text()

        curr_proj = self.batch.p.projects_data[self.batch.p.current_project_index]

        pa_seq = self.batch.p.getSeqPattern(curr_proj.seq_shot_take_pattern)
        pa_sh = self.batch.p.getShPattern(curr_proj.seq_shot_take_pattern)

        if len(pa_sh) > 0:
            cut_index = pa_sh.find("<sh")
            pa_sh = pa_sh[cut_index:]

        pa_seq_zeros = pa_seq.count('#')
        pa_sh_zeros = pa_sh.count('#')

        search__b = ""
        if len(hack__a) > 0:
            if self.comfun.is_float(hack__a):
                search__a = self.comfun.str_with_zeros(hack__a, pa_seq_zeros)
                self.qt_edit_line_sequence.setText(search__a)
                if len(hack__b) > 0:
                    if self.comfun.is_float(hack__b):
                        search__b = self.comfun.str_with_zeros(hack__b, pa_sh_zeros)
                        self.qt_edit_line_sh_B.setText(search__b)

                parametric_dir = "<project_cache_dir>" + curr_proj.seq_shot_take_pattern
                ret_imp_dir = self.batch.d.get_import_dir(parametric_dir, hack_frame_range=True, hack_A=search__a,
                                                          hack_B=search__b, hack_C="")
                fr = self.batch.d.get_frame_range_from_dir(ret_imp_dir)

                if fr[0] == 1:
                    self.qt_edit_line_frame_start.setText(str(fr[1]))
                    self.qt_edit_line_frame_end.setText(str(fr[2]))
                    print "   get_frame_range_from_cache  ", fr[1], fr[2]
                    self.top_ui.set_top_info(" Set frame range:  [" + str(fr[1]) + ":" + str(fr[2]) + "]")
                else:
                    print "  cant detect get_frame_range_from_cache  "
                    self.top_ui.set_top_info(" Cant detect frame range ", 7)

    def get_frame_range_from_scene(self):
        # ret = self.batch.o.soft_conn.get_curent_frame_range()
        ret = None  # TODO   .o.  softwares -> definitions
        print "   get_frame_range_from_scene    ", ret
        if ret is not None:
            self.qt_edit_line_frame_start.setText(str(self.comfun.int_or_val(ret[0], 0)))
            self.qt_edit_line_frame_end.setText(str(self.comfun.int_or_val(ret[1], 0)))
            self.top_ui.set_top_info(" Set frame range:  [" + str(ret[0]) + ":" + str(ret[1]) + "]")
        else:
            self.top_ui.set_top_info(" Can't detect frame range ", 7)

    def clear_vars(self):
        self.form_task_item = TaskItem(0, "sample", 1, "NULL", 1, 1, "01", "001", "", 0, 100, 1, 1, 1, "", 1, 50, "")


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

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.s = batch.s
        self.comfun = batch.comfun
        self.debug_level = batch.s.debug_level
        self.top_ui = top
        self.mainw = mainw

        self.array_visible_tasks_ids = []

        # init GUI
        list_tasks = QListWidget()
        list_tasks.setSelectionMode(QAbstractItemView.NoSelection)
        list_tasks.setFrameShadow(QFrame.Raised)
        list_tasks.currentItemChanged.connect(self.on_change_current_list_task)
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
        wfr_buttons.button.clicked.connect(self.on_click_confirm_remove_project)

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
        self.comfun.add_wigdets(qt_lay_tasks_forms, [qt_form_create, qt_form_edit, qt_form_remove, qt_form_add])

        self.hide_all_forms()

        qt_button_create_task = QPushButton("Create  ")
        qt_button_edit_task = QPushButton("Edit  ")
        qt_button_remove_task = QPushButton("Remove  ")
        qt_button_add_to_queue = QPushButton("Add to Queue")

        qt_button_create_task.clicked.connect(self.on_click_show_create)
        qt_button_edit_task.clicked.connect(self.on_click_show_edit)
        qt_button_remove_task.clicked.connect(self.on_click_show_remove)
        qt_button_add_to_queue.clicked.connect(self.on_click_show_add_to_queue)

        qt_lay_tasks_list.addWidget(list_tasks)

        self.comfun.add_wigdets(qt_lay_tasks_buttons,
                                [qt_button_create_task, qt_button_edit_task, qt_button_remove_task,
                                 qt_button_add_to_queue])

        self.comfun.add_layouts(qt_lay_tasks_main, [qt_lay_tasks_list, qt_lay_tasks_forms, qt_lay_tasks_buttons])

        self.init_tasks()

    def init_tasks(self):
        widget_list = self.list_tasks
        qt_list_item = QListWidgetItem(widget_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)

        list_item_widget = TaskListItem("ID", "task name", "user", "seq", "sh", "take", "state", "schV", "queV",
                                        "opts", "descr")

        widget_list.addItem(qt_list_item)
        widget_list.setItemWidget(qt_list_item, list_item_widget)
        qt_list_item.setSizeHint(QSize(1, 24))
        if self.s.ui_brightness_mode == 0:
            qt_list_item.setBackground(self.s.state_colors[0])
        else:
            qt_list_item.setBackground(self.s.state_colors_up[0])

        for tsk in self.batch.t.tasks_data:
            if tsk.project_id == self.batch.p.current_project_id:
                qt_list_item = QListWidgetItem(widget_list)
                if tsk.state_id == 1:
                    color_index = self.s.INDEX_STATE_ACTIVE
                else:
                    color_index = self.s.INDEX_STATE_HOLD
                cur_color = self.s.state_colors[color_index].color()
                qt_list_item.setBackground(cur_color)
                list_item_widget = TaskListItem(str(tsk.id), tsk.task_name, str(tsk.user_id),
                                                tsk.sequence, tsk.shot, tsk.take, tsk.state,
                                                str(tsk.schema_ver), str(tsk.queue_ver),
                                                tsk.options, tsk.description)

                widget_list.addItem(qt_list_item)
                widget_list.setItemWidget(qt_list_item, list_item_widget)
                qt_list_item.setSizeHint(QSize(130, 26))
                qt_list_item.setBackground(self.s.state_colors[tsk.state_id])

    def reset_list(self):
        self.freeze_list_on_changed = 1
        index = self.batch.t.current_task_index
        self.clear_list()
        self.init_tasks()
        self.batch.t.update_current_from_index(index)
        self.freeze_list_on_changed = 0

    def reload_tasks_data_and_refresh_list(self):
        self.batch.t.clear_all_tasks_data()
        self.batch.t.load_tasks()
        self.reset_list()
        self.update_list_of_visible_ids()

    def on_click_menu_set_init(self):
        self.batch.t.current_task.state = "INIT"
        self.batch.t.current_task.state_id = self.s.INDEX_STATE_INIT
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_set_working(self):
        self.batch.t.current_task.state = "WORKING"
        self.batch.t.current_task.state_id = self.s.INDEX_STATE_WORKING
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_set_done(self):
        self.batch.t.current_task.state = "DONE"
        self.batch.t.current_task.state_id = self.s.INDEX_STATE_DONE
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_set_hold(self):
        self.batch.t.current_task.state = "HOLD"
        self.batch.t.current_task.state_id = self.s.INDEX_STATE_HOLD
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_schema_remove(self):
        self.on_click_confirm_remove_project()

    def on_click_menu_sch_ver_from_schema(self):
        cur_sch = self.batch.c.get_schema_by_id(self.batch.t.current_task.schema_id)
        self.batch.t.current_task.schema_ver = cur_sch.schemaVersion
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_schema_version_p1(self):
        self.batch.t.current_task.schema_ver = 1 + int(
            self.batch.t.current_task.schema_ver)
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_schema_version_m1(self):
        self.batch.t.current_task.schema_ver = -1 + int(
            self.batch.t.current_task.schema_ver)
        self.batch.t.save_tasks()
        self.reset_list()

    def on_click_menu_open_base_setup(self):
        sch = self.batch.c.get_schema_by_id(self.batch.t.current_task.schema_id)
        self.batch.schemasUI.loadSchemaFile(sch.schema_name, self.batch.t.current_task.schema_ver)

    def on_click_menu_open_computed(self):
        tsk_id = self.batch.t.current_task.id
        version = self.batch.t.current_task.queue_ver
        evo_nr = -1
        file_to_load = self.batch.d.getComputedSetupFile(tsk_id, version, evo_nr)  # getSchemaBaseSetupFile()
        if file_to_load[0] == 1:
            if self.s.debug_level >= 1:
                print "\n  [INF]   loadFile: ", file_to_load[1]
            self.batch.o.soft_conn.load_scene(file_to_load[1])
        else:
            print "\n  [WRN]   loadFile not exist: ", file_to_load[1]

    @staticmethod
    def on_click_menu_spacer():
        print "  ____  "

    def on_right_click_show_menu(self, pos):
        global_cursor_pos = self.list_tasks.mapToGlobal(pos)
        qt_right_menu = QMenu()
        qt_right_menu.addAction("Open Base Setup ", self.on_click_menu_open_base_setup)
        qt_right_menu.addAction("Open Computed Setup ", self.on_click_menu_open_computed)
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
        qt_right_menu.addAction("Remove Task", self.on_click_menu_schema_remove)
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

    def on_click_show_create(self):
        if self.create_form_state == 0:
            self.hide_all_forms()
            if self.batch.t.current_task_index >= 0:
                curr_task = self.batch.t.tasks_data[self.batch.t.current_task_index]
                self.qt_form_create.update_create_ui(curr_task.schema_id)
            elif self.batch.c.current_schema_index >= 0:
                cur_sch = self.batch.c.schemas_data[self.batch.c.curr_schema_index]
                self.qt_form_create.update_create_ui(schema_id=cur_sch.id)
            else:
                self.qt_form_create.update_create_ui()
            self.qt_form_create.get_frame_range_from_scene()
            self.qt_form_create.show()
            self.create_form_state = 1
        else:
            self.qt_form_create.hide()
            self.create_form_state = 0

    def on_click_show_edit(self):
        if self.edit_form_state == 0:
            self.hide_all_forms()
            if self.batch.t.current_task_index >= 0:
                curr_task = self.batch.t.tasks_data[self.batch.t.current_task_index]
                self.qt_form_edit.update_edit_ui(curr_task)
                self.qt_form_edit.show()
                self.edit_form_state = 1
            else:
                print " [WRN] Please Select Task "
                self.top_ui.set_top_info(" Please Select Task ", 7)
        else:
            self.qt_form_edit.hide()
            self.edit_form_state = 0

    def on_click_show_remove(self):
        if self.remove_form_state == 0:
            self.hide_all_forms()
            self.qt_form_remove.show()
            self.remove_form_state = 1
        else:
            self.qt_form_remove.hide()
            self.remove_form_state = 0

    def on_click_show_add_to_queue(self):
        print " [db] on_click_add_to_queue  proj:  : ", self.batch.p.current_project_id
        if self.add_form_state == 0:
            if self.batch.t.current_task_index >= 0:
                print "[db]  WRN  add2Q CURR TASK ", self.batch.t.current_task_index
            else:
                print "[db]  WRN  add2Q CURR TASK -1 !  !!!\n"
            if self.batch.p.current_project_id >= 0:
                print "[db]  WRN  add2Q CURR PROJ ", self.batch.p.current_project_id
            else:
                print "[db]  WRN  add2Q CURR PROJ -1 !  !!!\n"

            self.hide_all_forms()
            self.qt_form_add.show()
            self.qt_form_add.update_add_ui()
            self.add_form_state = 1
        else:
            self.qt_form_add.hide()
            self.add_form_state = 0

    def add_single_task(self, new_task_item):
        self.batch.t.add_task(new_task_item, do_save=True)
        qt_list_item = QListWidgetItem(self.list_tasks)
        list_item_widget = TaskListItem(str(new_task_item.id), new_task_item.task_name, str(new_task_item.user_id),
                                        new_task_item.sequence, new_task_item.shot, new_task_item.take,
                                        new_task_item.state, str(new_task_item.schema_ver),
                                        str(new_task_item.queue_ver), new_task_item.options, new_task_item.description)
        qt_list_item.setBackground(QBrush(QColor("#ff8555")))   # TODO  settings color !
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)
        qt_list_item.setSizeHint(QSize(1, 24))
        self.list_tasks.addItem(qt_list_item)
        self.list_tasks.setItemWidget(qt_list_item, list_item_widget)

    def on_click_add_task(self, new_task_tem):
        if self.batch.p.current_project_id >= 0:
            if self.qt_form_create.qt_schema_name_combo.currentIndex() >= 0:
                self.qt_form_create.compile_imputs()
                if new_task_tem.schema_id < 0:
                    print "   [ERR]  schema_id  ", new_task_tem.schema_id

                self.add_single_task(copy.copy(new_task_tem))
                self.top_ui.set_top_info(" [INF] Task created, active task:  " + new_task_tem.task_name)

                self.qt_form_add.hide()
                self.add_form_state = 0

                self.reload_tasks_data_and_refresh_list()
            else:
                print " WRN [on_click_add_task] PLEASE SELECT SCHEMA"
                self.top_ui.set_top_info(" [INF] PLEASE SELECT SCHEMA !", 8)
        else:
            print " WRN [on_click_add_task] current_project_id ", self.batch.p.current_project_id
            self.top_ui.set_top_info(" [INF] PLEASE SELECT PROJECT !", 8)

    def on_click_update_task(self, edited_task_item):
        self.qt_form_edit.compile_imputs()
        self.batch.t.update_task(copy.copy(edited_task_item), do_save=True)

        current_list_index = self.list_tasks.currentRow()
        ed_item = self.list_tasks.item(current_list_index)
        list_item_widget = TaskListItem(str(edited_task_item.id), edited_task_item.task_name, edited_task_item.user_id,
                                        edited_task_item.sequence, edited_task_item.shot, edited_task_item.take,
                                        edited_task_item.state, str(edited_task_item.schema_ver),
                                        str(edited_task_item.queue_ver), edited_task_item.options,
                                        edited_task_item.description)

        self.list_tasks.setItemWidget(ed_item, list_item_widget)

        self.qt_form_add.hide()
        self.add_form_state = 0
        if self.s.debug_level >= 1:
            print " [INF] task updated"

    def on_click_confirm_remove_project(self):
        if self.s.debug_level >= 1:
            print "  on_click remove_project  ", self.batch.t.current_task_index, self.batch.t.current_task_list_index
        if self.batch.t.current_task_list_index >= 0:
            take_item_list = self.batch.t.current_task_list_index + 1
            self.batch.t.remove_single_task(index=self.batch.t.current_task_index, do_save=True)
            self.batch.t.last_task_list_index = -1
            self.batch.t.current_task_index = -1
            self.batch.t.current_task_list_index = -1

            print "on_click remove_project B ", self.batch.t.current_task_index, self.batch.t.current_task_list_index
            self.list_tasks.takeItem(take_item_list)

            print "on_click remove_project C ", self.batch.t.current_task_index, self.batch.t.current_task_list_index
            self.qt_form_remove.hide()
            self.remove_form_state = 0

    def print_form_add(self):
        print "\n\n  print_form_add"
        form_add = self.qt_form_add
        print "\n  actionsCount", form_add.actionsCount
        print "\n  actionsAllArray"
        self.comfun.print_list(form_add.actionsAllArray)
        print "\n  actions_widgets_array"
        for ak in form_add.actions_widgets_array:
            if ak.is_evo == 1:
                print " is_evo:", ak.is_evo,  "   scr:", ak.script_type, ak.script
            else:
                print " is_evo:", ak.is_evo, "   scr:", ak.script_type, ak.script
        print ".... "
        print "  print_form_add END\n\n"

    def on_click_add_to_queue(self):
        form_atq = self.qt_form_add
        if self.batch.t.current_task_index > -1:
            ret = form_atq.create_directories()
            if ret:
                self.batch.t.tasks_data[self.batch.t.current_task_index].queue_ver += 1
                self.batch.t.tasks_data[self.batch.t.current_task_index].state = "QUEUED"
                self.batch.t.tasks_data[self.batch.t.current_task_index].state_id = 3
                self.batch.t.save_tasks()

                self.batch.que_ui.add_to_queue_and_update_list(form_atq)

                self.freeze_list_on_changed = 1
                self.batch.t.last_task_list_index = -1
                self.reset_list()

                self.freeze_list_on_changed = 0
                self.qt_form_add.update_add_ui()
            else:
                print " [ERR] Add to queue: cant create directory !"
                self.top_ui.set_top_info(" ERR: cant create directory ", 9)
        else:
            self.top_ui.set_top_info(" Please select task ", 7)

    def clear_list(self):
        self.freeze_list_on_changed = 1
        while self.list_tasks.count() > 0:
            self.list_tasks.takeItem(0)
        self.freeze_list_on_changed = 0

    def update_all_tasks(self):
        self.clear_list()
        self.init_tasks()
        self.update_list_of_visible_ids()

    def update_list_of_visible_ids(self):
        array_visible_tasks_ids = []
        for task in self.batch.t.tasks_data:
            if task.project_id == self.batch.p.current_project_id:
                array_visible_tasks_ids.append(task.id)
        self.array_visible_tasks_ids = array_visible_tasks_ids

    def on_change_current_list_task(self, current_task_item):
        if current_task_item is None:
            print " [db] on_change_current_list_task (current_task_item is None)   ", self.list_tasks.currentRow()
        else:
            print " [db] on_change_current_list_task ", self.list_tasks.currentRow()

        if self.freeze_list_on_changed == 0:  # on massive action    or   refresh
            # self.batch.t.last_task_list_index = self.batch.t.current_task_list_index
            self.last_list_item_index = self.current_list_item_index
            current_list_index = self.list_tasks.currentRow() - 1
            self.current_list_item_index = current_list_index

            if self.last_list_item_index is not None:
                if self.last_list_item_index is not None and self.last_list_item_index < len(self.batch.t.tasks_data):
                    item = self.list_tasks.item(self.last_list_item_index + 1)
                    if self.last_list_item_index < len(self.array_visible_tasks_ids):
                        last_id = self.array_visible_tasks_ids[self.last_list_item_index]
                        last_index = self.batch.t.get_index_by_id(last_id)
                        if item is not None and last_index is not None:
                            color_index = self.batch.t.tasks_data[last_index].state_id
                            item.setBackground(self.batch.s.state_colors[color_index].color())
                else:
                    print " [db] WRONG last_task_list_index {} vs {} ".format(self.last_list_item_index,
                                                                              len(self.batch.t.tasks_data))
            else:
                print " [db] last_task_list_index is None "

            if len(self.array_visible_tasks_ids) <= current_list_index:
                self.update_list_of_visible_ids()  # TODO move  to init / change list
                if len(self.array_visible_tasks_ids) > current_list_index:
                    print " [db] vis ids FIXED: len(array_visible_tasks_ids):{}  vs current_list_index:{}". format(
                        len(self.array_visible_tasks_ids), current_list_index)
                else:
                    print " [ERR] vis ids NOT FIXED: array_visible_tasks_ids[] :{}  vs current_list_index:{}". format(
                        len(self.array_visible_tasks_ids), " vs ", current_list_index)

            if 0 <= current_list_index < len(self.array_visible_tasks_ids):
                current_task_id = self.array_visible_tasks_ids[current_list_index]
                self.batch.t.current_task_id = current_task_id
                self.batch.t.update_current_from_id(current_task_id)

            current_task_index = self.batch.t.current_task_index

            if 0 <= current_task_index < len(self.batch.t.tasks_data):
                cur_task = self.batch.t.tasks_data[current_task_index]
                if self.top_ui is not None:
                    self.top_ui.set_top_info("Current task: [" + str(cur_task.id) + "]    " + cur_task.task_name)
                else:
                    print " [ERR] top_ui None ", self.top_ui

                if current_list_index >= 0:
                    item_c = self.list_tasks.item(current_list_index + 1)
                    cur_color = self.batch.s.state_colors_up[cur_task.state_id].color()
                    item_c.setBackground(cur_color)

                    # update SCHEMA
                self.batch.c.lastSchemaIndex = None  # TODO  check it ui
                self.batch.c.current_schema_id = cur_task.schema_id
                self.batch.c.update_current_from_id(cur_task.schema_id)

                # update PROJECT
                if self.create_form_state == 1:
                    self.qt_form_create.update_create_ui(cur_task.schema_id)
                if self.edit_form_state == 1:
                    self.qt_form_edit.update_edit_ui(cur_task)
                if self.add_form_state == 1:  # add to queue
                    self.qt_form_add.update_add_ui()

            else:
                print "[ERR] on chng curr list task {} < {}   ".format(current_task_index, self.batch.t.tasks_data)
