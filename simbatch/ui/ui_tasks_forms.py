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


class TasksFormCreateOrEdit(QWidget):
    form_mode = 1  # 1 create    2 edit
    form_task_item = None  # store new or edited data as TaskItem

    batch = None
    comfun = None
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

    qt_edit_line_sim_frame_start = None
    qt_edit_line_sim_frame_end = None
    qt_edit_line_prev_frame_start = None
    qt_edit_line_prev_frame_end = None
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
        self.comfun = batch.comfun
        self.mainw = mainw
        self.top_ui = mainw.top_ui
        self.sts = batch.sts
        if mode == "edit":
            self.form_mode = 2

        self.schemas_id_array = []

        self.form_task_item = self.batch.tsk.get_blank_task()

        self.init_ui_elements(batch.sch)

        self.update_schema_names_combo()
        # self.schemas_id_array = batch.sch.schemas_id_array  # TODO  visible isd  VS proj's schemas

    def init_ui_elements(self, sch):
        qt_layout_out_form_create = QVBoxLayout()
        qt_layout_form_create = QVBoxLayout()
        qt_layout_combo_form_create = QHBoxLayout()

        qt_combo_schema_name = ComboLabel("", sch.get_schema_names())
        self.qt_schema_name_combo = qt_combo_schema_name.combo
        qt_combo_state = ComboLabel("", ["NULL", "INIT", "WAITING", "HOLD", "QUEUED", "DONE"])
        self.qt_combo_state_names = qt_combo_state.combo

        qt_edit_buton_sequence = EditLineWithButtons("Seq") #, label_minimum_size=70)
        self.qt_edit_line_sequence = qt_edit_buton_sequence.qt_edit_line
        qt_edit_buton_shot = EditLineWithButtons("Shot") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_shot = qt_edit_buton_shot.qt_edit_line
        qt_edit_buton_take = EditLineWithButtons("Take") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_take = qt_edit_buton_take.qt_edit_line
        qt_edit_buton_prior = EditLineWithButtons("Prior") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_priority = qt_edit_buton_prior.qt_edit_line
        qt_edit_buton_version = EditLineWithButtons("Ver") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_version = qt_edit_buton_version.qt_edit_line

        qt_edit_buton_sim_start = EditLineWithButtons("Sim Range") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_sim_frame_start = qt_edit_buton_sim_start.qt_edit_line
        qt_edit_buton_sim_end = EditLineWithButtons("") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_sim_frame_end = qt_edit_buton_sim_end.qt_edit_line

        qt_edit_buton_prev_start = EditLineWithButtons("Prev Range") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_prev_frame_start = qt_edit_buton_prev_start.qt_edit_line
        qt_edit_buton_prev_end = EditLineWithButtons("") #, label_minimum_size=50, align_right=1)
        self.qt_edit_line_prev_frame_end = qt_edit_buton_prev_end.qt_edit_line

        qt_button_lay_detect_framerange = ButtonOnLayout("From cache", width=70)    # TODO
        qt_button_lay_get_framerange = ButtonOnLayout("Get from scene", width=85)

        qt_button_lay_detect_framerange.button.clicked.connect(self.get_frame_range_from_cache)
        qt_button_lay_get_framerange.button.clicked.connect(self.get_frame_range_from_scene)

        qt_widget_group_shot = WidgetGroup([qt_edit_buton_sequence, qt_edit_buton_shot,
                                            qt_edit_buton_take, qt_edit_buton_prior, qt_edit_buton_version])
        qt_widget_group_time_range = WidgetGroup([qt_edit_buton_sim_start, qt_edit_buton_sim_end,
                                                  qt_edit_buton_prev_start, qt_edit_buton_prev_end,
                                                  # qt_button_lay_detect_framerange,
                                                  qt_button_lay_get_framerange])

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
        self.batch.logger.deepdb(("update_create_ui qt_schema_name_combo.count():", self.qt_schema_name_combo.count()))
        if schema_id == -1:
            self.batch.logger.deepdb(("update current index:", self.qt_schema_name_combo.count() - 1))
            self.qt_schema_name_combo.setCurrentIndex(self.qt_schema_name_combo.count() - 1)
        else:
            arr_index = 0
            for arrEl in self.schemas_id_array:
                if arrEl == schema_id:
                    self.batch.logger.deepdb(("set current index:", arr_index))
                    self.qt_schema_name_combo.setCurrentIndex(arr_index)
                arr_index += 1

    def update_edit_ui(self, cur_task):
        self.qt_combo_state_names.setCurrentIndex(self.qt_combo_state_names.findText(cur_task.state))

        arr_index = 0
        for sch_id in self.schemas_id_array:
            if sch_id == cur_task.schema_id:
                self.qt_schema_name_combo.setCurrentIndex(arr_index)
            arr_index += 1

        self.form_task_item = cur_task
        self.qt_edit_line_sequence.setText(cur_task.sequence)
        self.qt_edit_line_shot.setText(cur_task.shot)
        self.qt_edit_line_take.setText(cur_task.take)

        self.qt_edit_line_sim_frame_start.setText(str(cur_task.sim_frame_start))
        self.qt_edit_line_sim_frame_end.setText(str(cur_task.sim_frame_end))
        self.qt_edit_line_prev_frame_start.setText(str(cur_task.prev_frame_start))
        self.qt_edit_line_prev_frame_end.setText(str(cur_task.prev_frame_end))

        self.qt_edit_line_priority.setText(str(cur_task.priority))
        self.qt_edit_line_version.setText(str(cur_task.schema_ver))

        self.qt_fae_schema_description_edit.setText(cur_task.description)

    def update_schemas_id_arr(self, schemas_id_array):  # TODO check is it necessary / remove
        self.schemas_id_array = schemas_id_array

    # update combo box after project change or schema add, rem
    def update_schema_names_combo(self, combo_current_index=None):
        self.batch.logger.deepdb(("update_schema_names_combo", combo_current_index))
        combo_items_arr = self.mainw.sch_ui.current_project_schemas_names
        schemas_id_array = self.mainw.sch_ui.current_project_schemas_ids

        self.qt_schema_name_combo.clear()
        self.update_schemas_id_arr(schemas_id_array)
        for it in combo_items_arr:
            self.qt_schema_name_combo.addItem(it)
        if combo_current_index is not None:
            self.qt_schema_name_combo.setCurrentIndex(combo_current_index)

    def compile_inputs(self):
        self.form_task_item.task_name = self.qt_schema_name_combo.currentText()
        if self.qt_schema_name_combo.currentIndex() >= 0:
            self.batch.logger.db(("comlpile inputs", self.qt_schema_name_combo.currentIndex(), self.schemas_id_array))
            if len(self.schemas_id_array) > 0:
                self.batch.logger.db(("comlpile ...", self.schemas_id_array[0], len(self.schemas_id_array)))
            if len(self.schemas_id_array) > self.qt_schema_name_combo.currentIndex():
                self.form_task_item.schema_id = self.schemas_id_array[self.qt_schema_name_combo.currentIndex()]
            else:
                if self.sts.debug_level >= 1:
                    self.batch.logger.err(("Comlpile err", len(self.schemas_id_array)))
                    self.batch.logger.err(("Comlpile err", self.qt_schema_name_combo.currentIndex()))

            if self.batch.sch.current_schema_index is None:
                if self.form_task_item.schema_id >= 0:
                    self.batch.sch.update_current_from_id(self.form_task_item.schema_id)

        else:
            self.form_task_item.schema_id = -1
            self.batch.logger.wrn(("Wrong index, schema_name_combo:", self.qt_schema_name_combo.currentIndex()))

        if self.batch.sch.current_schema_index is None:   # TODO check it
            self.batch.logger.err(("Current sch is None! current_schema_index:", self.batch.sch.current_schema_index))

        if self.batch.prj.current_project_id is not None:
            self.form_task_item.project_id = self.batch.prj.current_project_id

        self.form_task_item.state_color = "3478b8"
        self.form_task_item.state = self.qt_combo_state_names.currentText()
        self.form_task_item.state_id = self.qt_combo_state_names.currentIndex()

        self.form_task_item.schema_ver = (self.batch.sch.get_schema_by_id(self.form_task_item.schema_id)).schema_version
        self.form_task_item.queue_ver = 0

        self.form_task_item.sequence = self.qt_edit_line_sequence.text()
        self.form_task_item.shot = self.qt_edit_line_shot.text()
        self.form_task_item.take = self.qt_edit_line_take.text()

        self.form_task_item.sim_frame_start = self.batch.comfun.int_or_val(self.qt_edit_line_sim_frame_start.text(), 0)
        self.form_task_item.sim_frame_end = self.batch.comfun.int_or_val(self.qt_edit_line_sim_frame_end.text(), 0)
        self.form_task_item.prev_frame_start = self.batch.comfun.int_or_val(self.qt_edit_line_prev_frame_start.text(), 0)
        self.form_task_item.prev_frame_end = self.batch.comfun.int_or_val(self.qt_edit_line_prev_frame_end.text(), 0)

        self.form_task_item.priority = self.batch.comfun.int_or_val(self.qt_edit_line_priority.text(), 50)

        self.form_task_item.schema_ver = self.batch.comfun.int_or_val(self.qt_edit_line_version.text(), 1)

        self.form_task_item.description = self.qt_fae_schema_description_edit.text()

    def get_frame_range_from_cache(self):
        curr_proj = self.batch.prj.projects_data[self.batch.prj.current_project_index]

        # pa_seq = self.batch.prj.getSeqPattern(curr_proj.seq_shot_take_pattern)   # TODO
        # pa_sh = self.batch.prj.getShPattern(curr_proj.seq_shot_take_pattern)     # TODO

        #  TODO get frame range from cache or framerange file.

    def get_frame_range_from_scene(self):
        try:
            frame_range = self.batch.dfn.current_interactions.get_curent_frame_range()
        except Exception as e:
            if self.batch.dfn.current_definition is None:
                self.batch.logger.err("Current definition is None, could NOT get current frame range")
            else:
                cdfn = self.batch.dfn.current_definition.name
                self.batch.logger.err(("Could NOT get current frame range. Please check interactions:", cdfn))
                self.batch.logger.err((e))
            self.top_ui.set_top_info(" Can't detect frame range ", 8)
            return False

        self.batch.logger.db(("get_frame_range_from_scene: ", frame_range))
        if frame_range is not None:
            self.qt_edit_line_sim_frame_start.setText(str(self.comfun.int_or_val(frame_range[0], 0)))
            self.qt_edit_line_sim_frame_end.setText(str(self.comfun.int_or_val(frame_range[1], 0)))
            self.qt_edit_line_prev_frame_start.setText(str(self.comfun.int_or_val(frame_range[0], 0)))
            self.qt_edit_line_prev_frame_end.setText(str(self.comfun.int_or_val(frame_range[1], 0)))
            self.top_ui.set_top_info(" Set frame range:  [" + str(frame_range[0]) + ":" + str(frame_range[1]) + "]")
        else:
            self.top_ui.set_top_info(" Can't detect frame range ", 7)

    def clear_vars(self):
        self.form_task_item = self.batch.tsk.get_blank_task()


class AddToQueueForm(QWidget):
    batch = None
    comfun = None
    # actions_options = []       # user inputs for all actions (options with parameters)
    task_options = None          # user inputs (task_proxy)
    schema_options = None        # user inputs (schema_proxy)

    qt_edit_button_frame_from = None
    qt_edit_button_frame_to = None
    qt_edit_button_sim_from = None
    qt_edit_button_sim_to = None
    qt_edit_button_prior = None
    qt_gb_add_to_queue_now = None
    qt_lay_actions = None

    qt_edit_button_description = None
    execute_button = None

    actions_widgets_array = []
    form_actions_count = 0

    # all_actions_array = []   # TODO check, currently not used !!!

    def __init__(self, batch):
        QWidget.__init__(self)
        self.batch = batch
        self.tsk = batch.tsk
        # self.form_atq_local_item = self.batch.que.get_blank_queue_item()
        # self.sts = self.batch.sts
        self.comfun = self.batch.comfun
        self.init_ui_elements()

    def init_ui_elements(self):
        qt_form_add_layout = QVBoxLayout()

        if self.batch.sts.debug_level > 3:  # debug proxy SchemaItem object (used when adding or editing schema)
            db_buttons_group = QGroupBox()
            db_b1 = ButtonOnLayout("basic print", width=140)
            db_b2 = ButtonOnLayout("detailed print", width=170)
            qt_debug_buttons = WidgetGroup([SimpleLabel("debug buttons"), db_b1, db_b2])   # , db_b2
            db_buttons_group.setLayout(qt_debug_buttons.qt_widget_layout)
            qt_form_add_layout.addWidget(db_buttons_group)
            qt_form_add_layout.addItem(QSpacerItem(1, 13))
            db_b1.button.clicked.connect(self.form_basic_db_print)
            db_b2.button.clicked.connect(self.form_detailed_db_print)

        qt_lay_actions = QVBoxLayout()
        self.qt_lay_actions = qt_lay_actions
        qt_lay_actions.setSpacing(0)
        qt_lay_actions.setContentsMargins(0, 0, 0, 0)
        qt_gb_actions = QGroupBox()
        qt_gb_actions.setTitle("Actions")
        qt_gb_actions.setLayout(qt_lay_actions)
        qt_form_add_layout.addWidget(qt_gb_actions)

        qt_edit_button_sim_from = EditLineWithButtons("Sim Range")
        qt_edit_button_sim_to = EditLineWithButtons("")
        qt_edit_button_frame_from = EditLineWithButtons("Prev Range")
        qt_edit_button_frame_to = EditLineWithButtons("")
        qt_edit_button_prior = EditLineWithButtons("Prior")

        qt_edit_button_description = EditLineWithButtons("Desc", label_minimum_size=60)
        qt_edit_button_description.qt_edit_line.textChanged.connect(self.on_edit_desc)

        qt_widget_group_frame_range = WidgetGroup([qt_edit_button_sim_from, qt_edit_button_sim_to,
                                                   qt_edit_button_frame_from, qt_edit_button_frame_to,
                                                   qt_edit_button_prior])
        qt_lay_task_options = QVBoxLayout()
        qt_lay_task_options.addLayout(qt_widget_group_frame_range.qt_widget_layout)
        qt_lay_task_options.addLayout(qt_edit_button_description.qt_widget_layout)

        qt_gb_atq = QGroupBox()
        qt_gb_atq.setTitle("Options")
        qt_gb_atq.setLayout(qt_lay_task_options)
        self.qt_gb_add_to_queue_now = qt_gb_atq
        qt_form_add_layout.addItem(QSpacerItem(1, 13))
        qt_form_add_layout.addWidget(qt_gb_atq)

        qt_button_cb_add_to_queue = ButtonWithCheckBoxes("Add To Queue Now!", pin_text="pin ")
        qt_form_add_layout.addLayout(qt_button_cb_add_to_queue.qt_widget_layout)

        self.qt_edit_button_sim_from = qt_edit_button_sim_from
        self.qt_edit_button_sim_to = qt_edit_button_sim_to
        self.qt_edit_button_frame_from = qt_edit_button_frame_from
        self.qt_edit_button_frame_to = qt_edit_button_frame_to
        self.qt_edit_button_prior = qt_edit_button_prior
        self.qt_edit_button_description = qt_edit_button_description
        self.execute_button = qt_button_cb_add_to_queue.button

        self.setLayout(qt_form_add_layout)
        # qt_edit_button_sim_from.qt_edit_line.textChanged.connect(self.on_change_sim_from)
        # qt_edit_button_sim_to.qt_edit_line.textChanged.connect(self.on_change_sim_to)
        # qt_edit_button_frame_from.qt_edit_line.textChanged.connect(self.on_change_render_from)
        # qt_edit_button_frame_to.qt_edit_line.textChanged.connect(self.on_change_render_to)

    def form_basic_db_print(self):
        print "\n"
        self.collect_options_from_widgets()
        self.tsk.print_task(self.task_options.proxy_task)

    def form_detailed_db_print(self):
        print "\n"
        print_all = True
        self.collect_options_from_widgets()

        if print_all:
            print "\n [INF] PRINT ACTIONS OPTIONS"
            for i, op in enumerate(self.schema_options.proxy_schema.actions_array):
                print i, op
            if self.task_options is not None:
                print "\n [INF] PRINT TASK OPTIONS"
                self.tsk.print_task(self.task_options.proxy_task)
            else:
                print "\n [WRN] task_options undefined!"

        # generate_script_from_actions
        if print_all:
            print "\n [INF] PRINT OPTIONS"
            for i, act in enumerate(self.batch.sch.current_schema.actions_array):
                print act.generate_script_from_action_template(self.batch, act.actual_value, with_new_line=False,
                                                               evo="1")

        print "\n [INF] GENERATE EVO"

        # schema_options.actions_array = self.actions_options
        # self.schema_options.proxy_schema.actions_array.actual_value
        # marker ATQ 302
        proxy_sch = self.schema_options.proxy_schema
        print "_ps: ", proxy_sch
        arr_scripts_params = self.batch.que.get_array_of_scripts_params_val_from_schema_actions(proxy_sch)
        print "_ap: ", arr_scripts_params
        # marker ATQ 303
        all_evo_combinations_array = self.batch.que.do_params_combinations(arr_scripts_params)
        print "_eo: ", all_evo_combinations_array

        print "\n [INF] GENERATE QUEUE ITEMS"
        qi = self.batch.que.generate_queue_items(self.batch.tsk.current_task_id, schema_options=self.schema_options)

        for i, q in enumerate(qi):
            print "gen qi: ", i, q

        print "\n [INF] END"

    def update_form(self):
        current_task = self.tsk.current_task
        self.qt_edit_button_sim_from.qt_edit_line.setText(str(current_task.sim_frame_start))
        self.qt_edit_button_sim_to.qt_edit_line.setText(str(current_task.sim_frame_end))
        self.qt_edit_button_frame_from.qt_edit_line.setText(str(current_task.prev_frame_start))
        self.qt_edit_button_frame_to.qt_edit_line.setText(str(current_task.prev_frame_end))
        self.qt_edit_button_prior.qt_edit_line.setText(str(current_task.priority))
        self.qt_edit_button_description.qt_edit_line.setText(current_task.description)

        self.remove_all_action_widgets()
        current_sch = self.batch.sch.get_schema_by_id(current_task.schema_id)
        current_dfn = self.batch.dfn.current_definition
        if current_dfn is None:
            self.batch.logger.wrn("(on update form) current definition is undefined")
            for act in current_sch.actions_array:
                # gen_script  = action.generate_script(action.scriptActionTemplates, vals, sub_type)
                self.add_action_widget_to_form(act.name, act.actual_value)
        else:
            for act in current_sch.actions_array:
                evolution = None
                mac = current_dfn.get_multiaction_by_name(act.name)
                if act.mode is not None:
                    if len(act.mode) > 0:
                        act_name_sufix = " "+act.mode

                    if mac is not None:
                        action_index = mac.get_action_index_by_mode(act.mode)
                        if action_index is not None:
                            evolution = []
                            if mac.actions[action_index].parameters is not None:
                                for p in mac.actions[action_index].parameters.param_list:
                                    evolution.append(p.abbrev + "   " + p.description)
                else:
                    act_name_sufix = ""

                check_str = str(act.actual_value)
                val_str = self.batch.sio.predefined.convert_predefined_variables_to_values(check_str, param="[evo]", option=str(current_task.id))

                if val_str is None:
                    val_str = "None"

                self.add_action_widget_to_form(act.name+act_name_sufix, edit_txt=val_str, evo=evolution)

    def add_action_widget_to_form(self, info, edit_txt=None, evo=None):
        if edit_txt is None and evo is None:
            wi = SimpleLabel(info)
        else:
            if evo is not None:
                if len(evo) <= 1:
                    wi = ActionWidgetATQ(self.batch, info, edit_txt)
                else:
                    wi = ActionWidgetATQ(self.batch, info, edit_txt,  combo_label="    with evolutions:", combo_items=evo)
            else:
                wi = ActionWidgetATQ(self.batch, info, edit_txt)

        qt_widget = QWidget()
        qt_widget.setLayout(wi.qt_widget_layout)
        self.qt_lay_actions.addWidget(qt_widget)
        self.actions_widgets_array.append(wi)

    def remove_all_action_widgets(self):
        del self.actions_widgets_array[:]
        # del self.all_actions_array[:]
        self.form_actions_count = 0
        while self.qt_lay_actions.count() > 0:
            b = self.qt_lay_actions.itemAt(0)
            b.widget().deleteLater()
            # b.deleteLater()
            self.qt_lay_actions.takeAt(0)
        # self.actionsCount = 0

    def create_directories(self):
        # TODO
        return True

    # def add_evo_to_line(self):
    #     evoAbbreviation = self.CMB.combo.currentText()[:3]
    #     el= self.ELWB.editLine
    #
    #     exist = el.text().find( evoAbbreviation )
    #     if exist >= 0 :
    #         el.setText( el.text()[:exist+4] +"_"+ el.text()[exist+4:] )
    #     else:
    #         if len(el.text()) < 3:
    #             el.setText( evoAbbreviation + "  " )
    #         else:
    #             el.setText( el.text()+ "; "+ evoAbbreviation + "  " )
    #
    #     self.checkEvos()

    def on_edit_desc(self, txt):
        if self.batch.tsk.proxy_task is not None:
            self.batch.tsk.proxy_task.description = txt

    """ marker ATQ 100   collect options   """
    def collect_options_from_widgets(self):
        self.batch.logger.db("colecting user options from widgets ...")
        # del self.actions_options[:]
        self.schema_options = self.collect_options_from_action_widgets()
        self.task_options = self.collect_options_from_task_widgets()
        self.batch.tsk.proxy_task = self.task_options.proxy_task

    def collect_options_from_action_widgets(self):
        so = self.batch.sch.create_schema_options_object()
        for i, wa in enumerate(self.actions_widgets_array):
            opt = wa.qt_edit_line_widget.qt_edit_line.text()
            evo = ""
            if wa.qt_combo_param is not None:
                evo = wa.qt_evo_edit_line_widget.qt_edit_line.text()
            '''
            if len(evo) > 4:   # TODO check is it evo or random string !
                #self.actions_options.append([opt, evo])
                so.proxy_schema.actions_array[i].actual_value = opt+""+evo
                # TODO lose opt !!!!
            else:
                #self.actions_options.append([opt])
                so.proxy_schema.actions_array[i].actual_value = opt+""+evo
            '''
            so.proxy_schema.actions_array[i].actual_value = opt+"^"+evo
        return so

    def collect_options_from_task_widgets(self):
        task_options = self.tsk.create_task_options_object()

        check_val = self.qt_edit_button_sim_from.qt_edit_line.text()
        if self.comfun.can_get_int(check_val):
            task_options.set_task_value("sim_frame_start", int(check_val))

        check_val = self.qt_edit_button_sim_to.qt_edit_line.text()
        if self.comfun.can_get_int(check_val):
            task_options.set_task_value("sim_frame_end", int(check_val))

        check_val = self.qt_edit_button_frame_from.qt_edit_line.text()
        if self.comfun.can_get_int(check_val):
            task_options.set_task_value("prev_frame_start", int(check_val))

        check_val = self.qt_edit_button_frame_to.qt_edit_line.text()
        if self.comfun.can_get_int(check_val):
            task_options.set_task_value("prev_frame_end", int(check_val))

        check_val = self.qt_edit_button_prior.qt_edit_line.text()
        if self.comfun.can_get_int(check_val):
            task_options.set_task_value("priority", int(check_val))

        task_options.set_task_value("description", self.qt_edit_button_description.qt_edit_line.text())

        # task_options.set_task_value("user options", 22)   # PRO version
        # task_options.set_task_value("user_id", 1)   # PRO version

        return task_options

