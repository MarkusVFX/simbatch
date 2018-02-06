import copy

try:
    from PySide.QtGui import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *
from core.schemas import *
from core.definitions import *

from ui_schemas_form import SchemaFormCreateOrEdit


class SchemaListItem(QWidget):
    def __init__(self, txt_id, txt_name, txt_desc, txt_schema_version):
        super(SchemaListItem, self).__init__()
        self.qt_widget = QWidget(self)
        self.qt_label_font = QFont()
        self.qt_label_font.setPointSize(8)
        self.qt_lay = QHBoxLayout(self.qt_widget)
        self.qt_lay.setSpacing(0)
        self.qt_lay.setContentsMargins(0, 0, 0, 0)
        self.qt_label_id = QLabel(txt_id)
        self.qt_label_id.setFont(self.qt_label_font)
        self.qt_label_id.setStyleSheet("""color:#000;padding-left:4px;""")
        self.qt_label_id.setMinimumWidth(140)
        self.qt_label_id.setMaximumWidth(170)
        self.qt_label_id.setFixedHeight(15)
        self.qt_lay.addWidget(self.qt_label_id)

        self.qt_label_name = QLabel(txt_name)
        self.qt_label_name.setFont(self.qt_label_font)
        self.qt_label_name.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_name)

        self.qt_label_version = QLabel(txt_schema_version)
        self.qt_label_version.setMinimumWidth(22)
        self.qt_label_version.setMaximumWidth(30)
        self.qt_label_version.setFont(self.qt_label_font)
        self.qt_label_version.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_version)

        self.qt_label_desc = QLabel(txt_desc)
        self.qt_label_desc.setStyleSheet("""color:#000;padding-left:4px;""")
        self.qt_lay.addWidget(self.qt_label_desc)

        self.setLayout(self.qt_lay)


class SchemasUI:
    list_schemas = None
    qt_widget_schema = None
    qt_lay_schema_main = None

    batch = None
    top_ui = None
    mainw = None

    create_form_state = 0
    copy_form_state = 0
    edit_form_state = 0
    remove_form_state = 0

    schema_form_create = None
    schema_form_copy = None
    schema_form_edit = None
    schema_form_remove = None

    new_name_on_copy = ""  # form copied schema

    comfun = None

    FormActions = None
    qt_lay_fae_actions_buttons = None
    qt_lay_fae_actions = None

    #  schema list
    current_list_item_nr = None
    last_list_item_nr = None
    list_visible_schemas_ids = []        # according with list filters
    list_visible_schemas_names = []      # according with list filters
    current_project_schemas_ids = []     # used for combo cox (add task)
    current_project_schemas_names = []   # used for combo cox (add task)

    # freeze list update on multi change/remove
    freeze_list_on_changed = 0

    # ui
    wfa_copy_schema = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.sts = batch.sts
        self.sch = batch.sch
        self.comfun = batch.comfun
        self.top_ui = top
        self.mainw = mainw

        self.visible_project_schemas_ids = []
        self.visible_project_schemas_names = []

        self.init_ui()
        self.init_schemas_list()
        # self.on_click_show_form_create()

    def init_ui(self):
        list_schemas = QListWidget()
        list_schemas.setSelectionMode(QAbstractItemView.NoSelection)
        list_schemas.setFrameShadow(QFrame.Raised)
        list_schemas.currentItemChanged.connect(self.on_list_schemas_current_changed)
        list_schemas.itemDoubleClicked.connect(self.on_list_schemas_double_clicked)
        list_schemas.setSpacing(1)
        p = list_schemas.sizePolicy()
        p.setVerticalPolicy(QSizePolicy.Policy.Maximum)

        list_schemas.setContextMenuPolicy(Qt.CustomContextMenu)
        list_schemas.customContextMenuRequested.connect(self.on_right_click_show_menu)

        self.list_schemas = list_schemas

        qt_widget_schema = QWidget()
        self.qt_widget_schema = qt_widget_schema
        qt_lay_schema_main = QVBoxLayout(qt_widget_schema)
        qt_lay_schema_main.setContentsMargins(0, 0, 0, 0)
        self.qt_lay_schema_main = qt_lay_schema_main

        qt_lay_schema_list = QHBoxLayout()
        qt_lay_schema_forms = QVBoxLayout()
        qt_lay_schema_buttons = QHBoxLayout()

        # CREATE
        # CREATE CREATE
        # CREATE CREATE CREATE
        schema_form_create = SchemaFormCreateOrEdit(self.batch, "create", self.top_ui)
        self.schema_form_create = schema_form_create
        if self.batch.prj.current_project_index >= 0:
            schema_form_create.schema_item_form_object.project_name = self.batch.prj.projects_data[
                self.batch.prj.current_project_index].project_name
            schema_form_create.schema_item_form_object.projectID = self.batch.prj.current_project_id
        schema_form_create.execute_button.button.clicked.connect(
            lambda: self.on_click_add_schema(schema_form_create.schema_item_form_object,
                                             save_as_base=schema_form_create.save_as_base_state))

        # COPY
        # COPY COPY
        # COPY COPY COPY
        schema_form_copy = QWidget()
        self.schema_form_copy = schema_form_copy
        qt_lay_outer_form_copy = QFormLayout()
        schema_form_copy.setLayout(qt_lay_outer_form_copy)
        qt_lay_form_copy = QVBoxLayout()

        # wfa -  widget form add
        # fa  -  form add
        wfa_copy_schema = EditLineWithButtons("Copy schema as ... ")
        wfa_target_proj = EditLineWithButtons("Target Proj  (id or name) ... ", text_on_button_1="test")
        wfa_buttons = ButtonWithCheckBoxes("Copy schema", pin_text="pin")

        wfa_target_proj.button_1.clicked.connect(
            lambda: self.on_changed_copy_target(wfa_target_proj.qt_edit_line))
        wfa_buttons.button.clicked.connect(self.on_clicked_copy_as)
        wfa_copy_schema.qt_edit_line.textChanged.connect(self.on_changed_copy_name)

        qt_lay_form_copy.addLayout(wfa_copy_schema.qt_widget_layout)
        qt_lay_form_copy.addLayout(wfa_target_proj.qt_widget_layout)
        qt_lay_form_copy.addLayout(wfa_buttons.qt_widget_layout)
        self.wfa_copy_schema = wfa_copy_schema

        qt_gb_copy = QGroupBox()
        qt_gb_copy.setLayout(qt_lay_form_copy)
        qt_lay_outer_form_copy.addWidget(qt_gb_copy)

        # EDIT
        # EDIT EDIT
        # EDIT EDIT EDIT
        schema_form_edit = SchemaFormCreateOrEdit(self.batch, "edit", self.top_ui)
        self.schema_form_edit = schema_form_edit
        schema_form_edit.execute_button.button.clicked.connect(
            lambda: self.on_click_update_schema(schema_form_edit.schema_item_form_object))

        # REMOVE
        # REMOVE REMOVE
        # REMOVE REMOVE REMOVE
        schema_form_remove = QWidget()
        self.schema_form_remove = schema_form_remove
        qt_form_remove_layout_ext = QVBoxLayout()
        schema_form_remove.setLayout(qt_form_remove_layout_ext)

        qt_form_remove_layout = QFormLayout()

        wfr_buttons = ButtonWithCheckBoxes("Yes, remove", label_text="Remove selected ?")

        qt_form_remove_layout.addRow(" ", QLabel("   "))
        qt_form_remove_layout.addRow(" ", wfr_buttons.qt_widget_layout)
        qt_form_remove_layout.addRow(" ", QLabel("   "))
        wfr_buttons.button.clicked.connect(self.on_click_confirm_remove_schema)

        qt_gb_remove = QGroupBox()
        qt_gb_remove.setLayout(qt_form_remove_layout)
        qt_form_remove_layout_ext.addWidget(qt_gb_remove)

        ###
        ######
        #########
        self.comfun.add_wigdets(qt_lay_schema_forms, [schema_form_create, schema_form_copy, schema_form_edit,
                                                      schema_form_remove])  # , FormTask] )

        self.hide_all_forms()

        qt_button_schema_create = QPushButton("Create")
        qt_button_schema_copy = QPushButton("Copy")
        qt_button_schema_edit = QPushButton("Edit")
        qt_button_schema_remove = QPushButton("Remove")

        qt_button_schema_create.clicked.connect(self.on_click_show_form_create)
        qt_button_schema_copy.clicked.connect(self.on_click_show_form_copy)
        qt_button_schema_edit.clicked.connect(self.on_click_show_form_edit)
        qt_button_schema_remove.clicked.connect(self.on_click_show_form_remove)

        qt_lay_schema_list.addWidget(list_schemas)

        self.comfun.add_wigdets(qt_lay_schema_buttons,
                                [qt_button_schema_create, qt_button_schema_edit, qt_button_schema_copy,
                                 qt_button_schema_remove])

        self.comfun.add_layouts(qt_lay_schema_main, [qt_lay_schema_list, qt_lay_schema_forms, qt_lay_schema_buttons])

    #
    # #
    # # #
    def init_schemas_list(self):
        list_schemas = self.list_schemas
        if list_schemas.count() > 0:
            list_schemas.clear()

        qt_list_item = QListWidgetItem(list_schemas)
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)
        list_item_widget = SchemaListItem("ID", "schema name", "description", "schV")

        list_schemas.addItem(qt_list_item)
        list_schemas.setItemWidget(qt_list_item, list_item_widget)
        qt_list_item.setSizeHint(QSize(1, 24))
        if self.sts.ui_brightness_mode == 0:
            qt_list_item.setBackground(self.sts.state_colors[0])
        else:
            qt_list_item.setBackground(self.sts.state_colors_up[0])

        for schema in self.sch.schemas_data:
            if schema.project_id == self.batch.prj.current_project_id:
                qt_list_item = QListWidgetItem(list_schemas)
                curr_color = self.sts.state_colors[schema.state_id].color()
                qt_list_item.setBackground(curr_color)
                list_item_widget = SchemaListItem(str(schema.id), schema.schema_name,
                                                  schema.description, str(schema.schema_version))
                list_schemas.addItem(qt_list_item)
                list_schemas.setItemWidget(qt_list_item, list_item_widget)
                qt_list_item.setSizeHint(QSize(1, 24))

                self.list_visible_schemas_names.append(schema.schema_name)
                self.list_visible_schemas_ids.append(schema.id)

    def update_schemas_list(self):
        self.init_schemas_list()

    # at this moment with no filters supported   update_visible_schemas_ids === update_current_project_schemas
    def update_visible_schemas_ids(self):        # TODO list filters
        # self.list_visible_schemas_names = []
        # self.list_visible_schemas_ids = []
        # for schema in self.sch.schemas_data:
        #     if schema.project_id == self.batch.prj.current_project_id:
        #         self.list_visible_schemas_names.append(schema.schema_name)
        #         self.list_visible_schemas_ids.append(schema.id)
        self.update_current_project_schemas()

    def update_current_project_schemas(self):  # all current project's schemas used for drop box in create task form
        self.current_project_schemas_ids = []
        self.current_project_schemas_names = []
        for schema in self.batch.sch.schemas_data:
            if schema.project_id == self.batch.prj.current_project_id:
                self.current_project_schemas_names.append(schema.schema_name)
                self.current_project_schemas_ids.append(schema.id)

    def clear_list(self):
        self.list_visible_schemas_names = []
        self.list_visible_schemas_ids = []
        while self.list_schemas.count() > 0:
            self.list_schemas.takeItem(0)

    def reset_list(self):
        self.freeze_list_on_changed = 1
        index = self.sch.current_schema_index
        self.clear_list()
        self.init_schemas_list()
        if index is not None and index > self.sch.total_schemas:
            self.sch.current_schema_index = index
            self.sch.current_project_id = self.sch.current_schema.id
        self.freeze_list_on_changed = 0

    def reload_schemas_data_and_refresh_list(self):
        self.sch.clear_all_schemas_data()
        self.sch.load_schemas()
        self.reset_list()
        self.update_visible_schemas_ids()

    def on_menu_open(self):
        current_schema_id = self.sch.list_visible_schemas_ids[self.sch.current_schema_list_index]
        self.batch.logger.db(("list_schemas_double_clicked :", current_schema_id))
        sch = self.sch.get_schema_by_id(current_schema_id)
        self.load_base_setup(sch.schema_name, sch.schemaVersion)

    def on_menu_save_as_next_version(self):
        cur_sch_index = self.batch.sch.current_schema_index
        self.sch.increase_current_schema_version()

        self.reload_schemas_data_and_refresh_list()

        self.sch.current_schema_index = cur_sch_index
        self.sch.update_current_from_index(cur_sch_index)

        ret = self.batch.dfn.get_schema_base_setup_file(forceSchemaVersion=True)

        cur_schema = self.sch.schemas_data[cur_sch_index]
        self.batch.logger.db(("save as :", cur_schema.schema_name, cur_schema.id))
        self.batch.dfn.soco.save_curent_scene_as(ret[1])

    def on_menu_locate_base_setup(self):
        import subprocess
        prev_dir = self.batch.dfn.get_base_setup_dir()
        base_setup_dir = prev_dir[1]
        if self.sts.current_os == 2:
            if self.comfun.path_exists(base_setup_dir, info="Base Setup"):
                subprocess.Popen('explorer "' + base_setup_dir + '"')

    def on_menu_remove(self):
        self.on_click_confirm_remove_schema()

    @staticmethod
    def on_menu_spacer():
        pass

    def _change_current_schema_state_and_reset_list(self, state_id):
        self.batch.sch.current_schema.state = self.sts.states_visible_names[state_id]
        self.batch.sch.current_schema.state_id = state_id
        self.batch.sch.save_schemas()
        self.reset_list()

    def on_menu_set_active(self):
        self._change_current_schema_state_and_reset_list(self.sts.INDEX_STATE_ACTIVE)

    def on_menu_set_suspended(self):
        self._change_current_schema_state_and_reset_list(self.sts.INDEX_STATE_SUSPEND)

    def on_menu_set_hold(self):
        self._change_current_schema_state_and_reset_list(self.sts.INDEX_STATE_HOLD)

    def on_right_click_show_menu(self, pos):
        global_pos = self.list_schemas.mapToGlobal(pos)
        qt_menu_right = QMenu()
        qt_menu_right.addAction("Open base schema", self.on_menu_open)
        qt_menu_right.addAction("Save current scene as next version", self.on_menu_save_as_next_version)
        qt_menu_right.addAction("________", self.on_menu_spacer)
        qt_menu_right.addAction("Locate base setup", self.on_menu_locate_base_setup)
        qt_menu_right.addAction("________", self.on_menu_spacer)
        qt_menu_right.addAction("Set ACTIVE", self.on_menu_set_active)
        qt_menu_right.addAction("Set SUSPEND", self.on_menu_set_suspended)
        qt_menu_right.addAction("Set HOLD", self.on_menu_set_hold)
        qt_menu_right.addAction("________", self.on_menu_spacer)
        qt_menu_right.addAction("Remove", self.on_menu_remove)
        qt_menu_right.exec_(global_pos)

    def hide_all_forms(self):
        self.schema_form_create.hide()
        self.schema_form_copy.hide()
        self.schema_form_edit.hide()
        self.schema_form_remove.hide()
        self.create_form_state = 0
        self.copy_form_state = 0
        self.edit_form_state = 0
        self.remove_form_state = 0

    def update_form_create(self):
        if self.batch.prj.current_project_index >= 0:
            # txt = self.batch.prj.projects_data[self.batch.prj.current_project_index].project_name
            # self.schema_form_create.schema_item_form_object.project_name = txt
            # self.schema_form_create.schema_item_form_object.projectID = self.batch.prj.current_project_id
            new_schema = self.sch.get_blank_schema()
            new_schema.project_id = self.batch.prj.current_project_id

            new_schema.definition_name = self.batch.dfn.current_definition_name
            self.schema_form_create.update_form_data(new_schema)
        else:
            self.batch.logger.wrn(("Wrong current project index", self.batch.prj.current_project_index))

    def on_click_show_form_create(self):
        if self.create_form_state == 0:
            self.hide_all_forms()
            self.schema_form_create.show()
            self.update_form_create()
            self.create_form_state = 1
        else:
            self.schema_form_create.hide()
            self.create_form_state = 0

    def form_edit_update_ui(self):
        if self.sch.current_schema_index >= 0:
            cur_schema = self.sch.current_schema
            self.schema_form_edit.qt_fae_schema_name_edit.setText(cur_schema.schema_name)
            self.schema_form_edit.qt_fae_schema_version_edit.setText(str(cur_schema.schema_version))
            self.schema_form_edit.qt_fae_schema_description_edit.setText(cur_schema.description)

    def on_click_show_form_edit(self):
        if self.edit_form_state == 0:
            self.hide_all_forms()
            self.schema_form_edit.show()
            self.form_edit_update_ui()

            if self.sch.current_schema_index >= 0:
                self.schema_form_edit.update_form_data(self.sch.current_schema)
            self.edit_form_state = 1
        else:
            self.schema_form_edit.hide()
            self.edit_form_state = 0

    def update_copy_form(self):
        if self.sch.current_schema_index >= 0:
            self.wfa_copy_schema.qt_edit_line.setText(
                self.sch.schemas_data[self.sch.current_schema_index].schema_name)

    def on_click_show_form_copy(self):
        if self.copy_form_state == 0:
            self.hide_all_forms()
            self.update_copy_form()
            self.schema_form_copy.show()
            self.copy_form_state = 1
        else:
            self.schema_form_copy.hide()
            self.copy_form_state = 0

    def on_changed_copy_name(self, txt):
        self.new_name_on_copy = txt
        # TODO !!! copy schema
        self.batch.logger.db(("on_changed_copy_name", txt))

    def on_changed_copy_target(self, qt_edit_line):
        el_txt = qt_edit_line.text()
        if self.comfun.is_float(el_txt):
            index = self.batch.prj.get_index_from_id(int(el_txt))
            if index >= 0:
                qt_edit_line.setText(self.batch.prj.projects_data[index].project_name)
            else:
                qt_edit_line.setText("[ERR] Wrong index: " + qt_edit_line.text())

        else:
            self.batch.prj.get_index_from_name(qt_edit_line.text(), check_similar=True)
        self.batch.logger.db(("qt_edit_line.text() : ", qt_edit_line.text()))

    def on_clicked_copy_as(self):
        if self.batch.sch.current_schema_index >= 0:
            new_name = self.new_name_on_copy
            if len(new_name) > 0:
                curr = self.batch.sch.schemas_data[self.batch.sch.current_schema_index]
                copied_schema_item = SchemaItem(0, new_name, curr.state_id, curr.state, curr.schema_version,
                                                curr.project_id, curr.project_name, curr.definition_id,
                                                curr.actions, curr.description)
                self.on_click_add_schema(copied_schema_item)
                self.schema_form_copy.hide()
                self.copy_form_state = 0
            else:
                self.top_ui.set_top_info(" please, input a new name ")
        else:
            self.top_ui.set_top_info(" select schema to copy ! ")

    def on_click_show_form_remove(self):
        if self.remove_form_state == 0:
            self.hide_all_forms()
            self.schema_form_remove.show()
            self.remove_form_state = 1
        else:
            self.schema_form_remove.hide()
            self.remove_form_state = 0

    def on_click_confirm_remove_schema(self):
        self.batch.logger.db(("on_click_confirm_remove_schema index:", self.sch.current_schema_index))
        if self.sch.current_schema_index >= 0:
            remove_index = self.sch.current_schema_index
            self.sch.lastSchema = None
            self.sch.current_schema_id = None
            self.sch.current_schema_index = None
            self.sch.remove_single_schema(index=remove_index, do_save=True)
            # self.list_schemas.takeItem(remove_index + 1)
            self.update_visible_schemas_ids()
            self.reset_list()
            # list_visible_schemas_ids
            self.schema_form_remove.hide()
            self.remove_form_state = 0

    def add_single_schema(self, new_schema_item):
        new_schema_item.id = -1  # TODO check -1
        self.sch.add_schema(new_schema_item, do_save=True)
        list_item = QListWidgetItem(self.list_schemas)
        list_item_widget = SchemaListItem(str(new_schema_item.id), new_schema_item.schema_name,
                                          new_schema_item.description, str(new_schema_item.schema_version))
        self.list_schemas.addItem(list_item)
        self.list_schemas.setItemWidget(list_item, list_item_widget)
        self.batch.logger.db(("add schema:", new_schema_item.schema_name,
                              "   to proj :", self.batch.prj.current_project_id))
        sch_dir = self.batch.prj.current_project.working_directory_absolute + new_schema_item.schema_name + "\\"
        self.batch.sio.create_schema_directory(sch_dir)

    def on_click_add_schema(self, new_schema_item, save_as_base=0):
        self.batch.logger.db(("adding schema with name: ", new_schema_item.schema_name))

        self.schema_form_create.compile_actions()
        if new_schema_item is None or len(new_schema_item.schema_name) == 0:
            self.top_ui.set_top_info(" Insert schema name ", 8)
        else:
            new_schema_item.state_id = self.sts.INDEX_STATE_ACTIVE
            new_schema_item.state = "ACTIVE"
            if self.comfun.is_float(new_schema_item.schema_version) is False:
                new_schema_item.schema_version = 1
            self.add_single_schema(copy.copy(new_schema_item))

            if save_as_base == 1:  # save as base setup
                save_as = self.batch.sio.generate_base_setup_file_name(new_schema_item.schema_name)
                self.batch.logger.deepdb(("with saveAs:  ", save_as))
                if self.batch.dfn.current_interaction is not None:
                    self.batch.dfn.current_interaction.save_curent_scene_as(save_as[1])
            else:
                self.batch.logger.deepdb(("with save_as_base_state:", save_as_base))

            self.top_ui.set_top_info("schema created, active schema:  " + new_schema_item.schema_name)
            # self.new_schema_item = self.batch.sch.get_blank_schema()   # TODO  clear UI !!!  if clear var
            self.schema_form_create.clear_vars()
            self.schema_form_create.hide()
            self.create_form_state = 0
            self.update_current_project_schemas()

            self.mainw.tsk_ui.qt_form_create.update_schema_names_combo()
            # self.current_project_schemas_names,              self.current_project_schemas_ids, 0)
            self.mainw.tsk_ui.qt_form_edit.update_schema_names_combo()
            # self.current_project_schemas_names,          self.current_project_schemas_ids, 0)
            self.reload_schemas_data_and_refresh_list()

    def on_click_update_schema(self, edited_schema_item):
        self.schema_form_edit.compile_actions()
        if edited_schema_item is None or len(edited_schema_item.schema_name) == 0:
            self.top_ui.set_top_info(" Insert schema name ! ", 8)
            self.batch.logger.wrn("insert schema name ! ")
        else:
            self.sch.update_schema(edited_schema_item, do_save=True)

            current_list_index = self.list_schemas.currentRow()
            ed_item = self.list_schemas.item(current_list_index)
            list_item_widget = SchemaListItem(str(edited_schema_item.id), edited_schema_item.schema_name,
                                              edited_schema_item.description, str(edited_schema_item.schema_version))
            self.list_schemas.setItemWidget(ed_item, list_item_widget)

            self.schema_form_edit.hide()
            self.edit_form_state = 0

    def load_base_setup(self, schema_name, version=1):
        file_to_load = self.batch.dfn.generate_tuple_base_setup_file_name(schema_name, ver=version)
        if file_to_load[0] == 1:
            self.batch.logger.inf(("loadFile: ", file_to_load[1]))
            self.batch.dfn.soco.load_scene(file_to_load[1])
        else:
            self.batch.logger.err(("loadFile: ", file_to_load))

    def on_list_schemas_double_clicked(self, item):
        self.batch.logger.db(("list_schemas_double_clicked: ", self.sch.current_schema_list_index, item))
        self.on_menu_open()

    def on_list_schemas_current_changed(self, current_row):
        if self.freeze_list_on_changed == 0:
            self.batch.logger.inf(("list_schemas_current_changed: ", self.list_schemas.currentRow()))

            self.last_list_item_nr = self.current_list_item_nr
            self.current_list_item_nr = self.list_schemas.currentRow()

            # update color of last item list
            if self.last_list_item_nr is not None:
                last_schema_id = self.list_visible_schemas_ids[self.last_list_item_nr - 1]
                last_schema_index = self.sch.get_index_by_id(last_schema_id)
                last_item = self.list_schemas.item(self.last_list_item_nr)
                color_index = self.sch.schemas_data[last_schema_index].state_id
                last_item.setBackground(self.sts.state_colors[color_index].color())

            # update color of current item list
            if self.current_list_item_nr >= 0:
                self.batch.logger.deepdb(("current_list_item_nr: ", self.current_list_item_nr))

                current_schema_id = self.list_visible_schemas_ids[self.current_list_item_nr - 1]
                self.sch.update_current_from_id(current_schema_id)
                color_index = self.sch.current_schema.state_id
                current_row.setBackground(self.sts.state_colors_up[color_index].color())

                # update current schema variables and top info
                cur_sch_name = self.sch.current_schema.schema_name
                if self.top_ui is not None:
                    self.top_ui.set_top_info("Current schema:    " + cur_sch_name)
                else:
                    self.batch.logger.err("top_ui undefined !")
            else:
                self.batch.logger.wrn(("(on sch chng) current_list_item_nr:", self.current_list_item_nr))

            if self.edit_form_state == 1:
                self.form_edit_update_ui()
                self.schema_form_edit.update_form_data(self.sch.current_schema)
                self.batch.logger.db(("update edit form: ", self.sch.current_schema.schema_name))

            if self.copy_form_state == 1:
                self.update_copy_form()
