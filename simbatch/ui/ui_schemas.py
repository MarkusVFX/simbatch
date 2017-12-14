import copy

try:
    from PySide.QtGui import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *
from core.schemas import *
from core.definitions import *



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


class SchemaFormCreateOrEdit(QWidget):
    schema_item_form_object = None
    save_as_base_state = 1

    form_mode = 1  # 1 create    2 edit

    # definitions
    definitions_array = []

    # actions
    actionsCount = 0
    action_widgets = []
    actionsString = ""
    
    # ui
    execute_button = None
    top_ui = None
    qt_bg_schema_top = None
    qt_fae_schema_name_edit = None
    qt_fae_schema_version_edit = None
    qt_fae_schema_description_edit = None
    qt_radio_buttons_fc_software = None
    qt_lay_fae_actions = None
    qt_lay_fae_actions_buttons = None
    active_definition_index = None

    def __init__(self, batch, mode, top):
        QWidget.__init__(self)
        self.definitions_array = []
        self.action_widgets = []
        self.batch = batch
        self.schema_item_form_object = batch.c.get_blank_schema()
        self.s = self.batch.s
        if mode == "edit":
            self.form_mode = 2
        self.init_ui_elements()
        self.add_defined_action_buttons()
        self.top_ui = top

    def init_ui_elements(self):
        qt_lay_outer_schema_form = QVBoxLayout()

        # fae   form add/edit
        qt_fae_schema_name = EditLineWithButtons("Name: ", label_minimum_size=60)
        self.qt_fae_schema_name_edit = qt_fae_schema_name.qt_edit_line
        qt_fae_schema_description = EditLineWithButtons("Description:  ", label_minimum_size=60)
        self.qt_fae_schema_description_edit = qt_fae_schema_description.qt_edit_line
        qt_fae_schema_version = EditLineWithButtons("Version:  ",
                                                    label_minimum_size=55)  # edit_maximum_size, widgetMaximum = 40
        self.qt_fae_schema_version_edit = qt_fae_schema_version.qt_edit_line
        qt_fae_schema_as_base = QCheckBox("Copy Current Scene As Base Setup")
        qt_fae_schema_as_base.setStyleSheet("""padding-left:130px;""")
        if self.form_mode == 2:
            qt_fae_schema_as_base.hide()
        for i, n in enumerate(self.batch.d.definitions_names):
            if n == self.s.runtime_env:
                self.active_definition_index = i
        qt_radio_buttons_fc_software = RadioButtons("Definitons:", self.batch.d.definitions_names,
                                                    self.active_definition_index, self.on_radio_change)

        self.qt_radio_buttons_fc_software = qt_radio_buttons_fc_software

        if self.form_mode == 1:
            schema_form_buttons = ButtonWithCheckBoxes("Create schema", pin_text="pin", cb2_text="Crowd mode",
                                                       cb3_text="Save as base setup", cb3_checked=True)
            schema_form_buttons.third_check_box.stateChanged.connect(self.on_changed_save_as_base_setup)
        else:
            schema_form_buttons = ButtonWithCheckBoxes("Save schema", pin_text="pin", cb2_text="Crowd mode")

        fae_widget_group = WidgetGroup([qt_fae_schema_name, qt_fae_schema_version, qt_fae_schema_description])

        qt_lay_fae = QVBoxLayout()
        qt_lay_fae.addLayout(fae_widget_group.qt_widget_layout)

        qt_bg_schema_top = QGroupBox()
        if self.form_mode == 1:
            qt_bg_schema_top.setTitle("Create Schema :")
        else:
            qt_bg_schema_top.setTitle("Edit Schema :")
        qt_bg_schema_top.setLayout(qt_lay_fae)
        qt_lay_outer_schema_form.addWidget(qt_bg_schema_top)
        self.qt_bg_schema_top = qt_bg_schema_top

        qt_lay_fae_actions = QVBoxLayout()
        self.qt_lay_fae_actions = qt_lay_fae_actions
        qt_lay_fae_actions.setSpacing(0)
        qt_lay_fae_actions.setContentsMargins(0, 10, 0, 10)

        qt_gb_fae_actions = QGroupBox()
        qt_gb_fae_actions.setTitle("Actions")
        qt_gb_fae_actions.setLayout(qt_lay_fae_actions)
        qt_lay_outer_schema_form.addWidget(qt_gb_fae_actions)

        # SOFT BUTTONS
        qt_lay_fae_actions_buttons = QHBoxLayout()
        self.qt_lay_fae_actions_buttons = qt_lay_fae_actions_buttons
        qt_lay_fae_actions_soft = QVBoxLayout()
        qt_lay_fae_actions_soft.addLayout(qt_lay_fae_actions_buttons)
        qt_lay_fae_actions_soft.addLayout(qt_radio_buttons_fc_software.qt_widget_layout)

        qt_gb_fae_add_actions = QGroupBox()
        qt_gb_fae_add_actions.setTitle("Add actions to schema")
        qt_gb_fae_add_actions.setLayout(qt_lay_fae_actions_soft)
        qt_lay_outer_schema_form.addWidget(qt_gb_fae_add_actions)

        qt_lay_fae_save = QVBoxLayout()
        qt_lay_fae_save.addLayout(schema_form_buttons.qt_widget_layout)
        qt_lay_outer_schema_form.addLayout(qt_lay_fae_save)

        qt_fae_schema_name.qt_edit_line.textChanged.connect(self.on_edit_schema_name)
        qt_fae_schema_description.qt_edit_line.textChanged.connect(self.on_edit_schema_description)
        qt_fae_schema_version.qt_edit_line.textChanged.connect(self.on_edit_schema_version)

        self.execute_button = schema_form_buttons
        self.setLayout(qt_lay_outer_schema_form)

    #
    ##
    ### on radio button definition change
    def on_radio_change(self, nr):
        if self.s.debug_level >= 3:
            print " [db] on_radio_change", nr
        self.change_current_definition(nr)

    # clear action and
    def change_current_definition(self, nr=None):
        self.remove_all_action_buttons()
        self.remove_all_defined_action_buttons()
        if nr is None:
            nr = self.active_definition_index
        self.add_defined_action_buttons(nr)

    # def change_current_actions_software__OLD_x(self, runtime_env="", nr=None):
    #     if self.s.debug_level >= 3:
    #         print " [db] (on radio) nr ", nr
    #
    #     self.remove_all_action_buttons()
    #     self.remove_all_defined_action_buttons()
    #
    #     if nr is not None and nr < len(self.batch.d.definitions_array):
    #         for a in self.batch.d.definitions_array[nr]:
    #             b = self.add_software_button(a.action_sub_type)
    #             if self.batch.p.current_project_index >= 0:
    #                 curr_proj = self.batch.p.projects_data[self.batch.p.current_project_index]
    #                 b.button.clicked.connect(
    #                     lambda a=a: self.on_click_add_button(a, self.qt_lay_fae_actions, self.action_widgets,
    #                                                          curr_proj))

    def add_defined_action_button(self, button_txt, disabled=True):
        b = ButtonOnLayout(button_txt)
        self.qt_lay_fae_actions_buttons.addLayout(b.qt_widget_layout)
        if disabled == "disabled":
            b.button.setEnabled(False)
        return b

    # add horizontal row of defined action buttons
    def add_defined_action_buttons(self, nr=None):
        if nr is None:
            nr = self.active_definition_index
        curr_proj = self.batch.p.current_project
        if curr_proj is not None:
            if nr is not None and nr < len(self.batch.d.definitions_array):
                for action in self.batch.d.definitions_array[nr].actions_array:
                    b = self.add_defined_action_button(action.name)
                    b.button.clicked.connect(lambda a=action: self.on_click_defined_action_button(a, curr_proj))
        else:
            if self.s.debug_level >= 2:
                print " [WRN] Current project undefined !"

    # on click one of horizontal button add action widget to vertical list of schema actions
    def on_click_defined_action_button(self, single_or_group_action, curr_proj):  # , force_val=0
        combo_items = []
        combo_val = []

        qt_lay = self.qt_lay_fae_actions
        if isinstance(single_or_group_action, SingleAction):
            button_2 = single_or_group_action.addional_butt_caption
            action_widget = ActionWidget(id=str(single_or_group_action.id) + "  ",
                                         label_txt=single_or_group_action.name,
                                         edit_txt=single_or_group_action.default_value,
                                         text_on_button_1="Get", text_on_button_2=button_2)
        else:  # GroupAction
            for i, a in enumerate(single_or_group_action.actions):
                combo_items.append(a.mode)
                combo_val.append(a.default_value)
            button_2 = single_or_group_action.actions[0].addional_butt_caption
            action_widget = ActionWidget(id=str(single_or_group_action.id), label_txt=single_or_group_action.name,
                                         edit_txt=combo_val[0], text_on_button_1="Get", text_on_button_2=button_2,
                                         combo_items=combo_items, combo_val=combo_val)

        qt_lay.addWidget(action_widget)
        self.action_widgets.append(action_widget)

        action_widget.qt_button_1.clicked.connect(
            lambda: single_or_group_action.get_get_file(single_or_group_action.actionWidget.edit,
                                                        curr_proj.working_directory,
                                                        action_type, QFileDialog)
        )

        if button_2 is not None and len(button_2) > 0:
            action_widget.qt_button_2.clicked.connect(
                lambda: self.on_clicked_button_action_2(single_or_group_action)  # curr_proj.working_directory, action_type)
            )

        if len(combo_items) > 0:
            action_widget.qt_combo.currentIndexChanged.connect(
                lambda: self.on_change_combo_action(action_widget, single_or_group_action, curr_proj)
            )

    def on_clicked_button_action_2(self, act):
        print "   on_clicked_button_action_2  ",  act
        print "   on_clicked_button_action_2  ",  act
        print "   on_clicked_button_action_2  ",  act

    def on_change_combo_action(self, action_widget, software_action, curr_project):
        # action_widget.qt_edit.setText(action_widget.qt_combo.currentText())
        action_widget.qt_edit.setText(software_action.actions[action_widget.qt_combo.currentIndex()].default_value)

        # print "  on_change_combo_action  ", index
        print "  on_change_combo_action  ",  software_action.name
        print "  on_change_combo_actionn  ",
        print "  on_change_combo_actionnn  ",  curr_project





    # def on_change_combo_action_X_old(self, software_action, curr_project):
    #     index = software_action.actionWidget.combo.currentIndex()
    #     if self.s.debug_level >= 4:
    #         print "  [db]  SoftwareAction  comboOnChange : ", index
    #     software_action.actionWidget.action_sub_type = software_action.actionWidget.combo.currentText()
    #     if len(software_action.comboValArr) > index:
    #         if software_action.comboValArr[index] == "<project_cache_dir>":
    #             software_action.comboValArr[index] = "<project_cache_dir>" + "\\" + curr_project.seq_shot_take_pattern
    #         else:
    #             software_action.actionWidget.edit.setText(software_action.comboValArr[index])
    #     else:
    #         print "ERR comboOnChange  ", len(software_action.comboValArr), ">", index

    # clear helper form object (store schema data)
    def clear_vars(self):
        self.schema_item_form_object = self.batch.c.get_blank_schema()

    # remove horizontal row of defined actions buttons
    def remove_all_defined_action_buttons(self):
        while self.qt_lay_fae_actions_buttons.count() > 0:
            b = self.qt_lay_fae_actions_buttons.itemAt(0)
            c = b.takeAt(0)
            c.widget().deleteLater()
            self.qt_lay_fae_actions_buttons.takeAt(0)

    def remove_all_action_buttons(self):
        self.action_widgets = []
        while self.qt_lay_fae_actions.count() > 0:
            b = self.qt_lay_fae_actions.itemAt(0)
            b.widget().deleteLater()
            self.qt_lay_fae_actions.takeAt(0)
        self.actionsCount = 0

    #
    ##
    ###
    def on_edit_schema_name(self, txt):
        self.schema_item_form_object.schema_name = txt
        if self.form_mode == 1:
            self.qt_bg_schema_top.setTitle("Create Schema : " + txt)
        else:
            self.qt_bg_schema_top.setTitle("Edit Schema : " + txt)

    def on_edit_schema_description(self, txt):
        self.schema_item_form_object.description = txt

    def on_edit_schema_version(self, txt):
        self.schema_item_form_object.schemaVersion = int(txt)

    def on_changed_save_as_base_setup(self, state):
        if state:
            self.save_as_base_state = 1
        else:
            self.save_as_base_state = 0

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
    list_visible_schemas_ids = []
    list_visible_schemas_names = []

    # freeze list update on multi change/remove
    freeze_list_on_changed = 0

    # ui
    wfa_copy_schema = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.s = batch.s
        self.c = batch.c
        self.comfun = batch.comfun
        self.top_ui = top
        self.mainw = mainw

        self.init_ui()
        self.init_schemas_list()
        self.on_click_show_form_create()

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
        if self.batch.p.current_project_index >= 0:
            schema_form_create.schema_item_form_object.project_name = self.batch.p.projects_data[
                self.batch.p.current_project_index].project_name
            schema_form_create.schema_item_form_object.projectID = self.batch.p.current_project_id
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

        # wfa   widget form add
        # fa    form add
        wfa_copy_schema = EditLineWithButtons("Copy schema as ... ")
        wfa_target_proj = EditLineWithButtons("Target Proj  (id or name) ... ", text_on_button_1="test")

        wfa_buttons = ButtonWithCheckBoxes("Copy schema", pin_text="pin")

        wfa_target_proj.text_on_button_1.clicked.connect(
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
        wfr_buttons.button.clicked.connect(self.on_click_confirm_remove_project)

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
        if self.s.ui_brightness_mode == 0:
            qt_list_item.setBackground(self.s.state_colors[0])
        else:
            qt_list_item.setBackground(self.s.state_colors_up[0])

        for schema in self.c.schemas_data:
            if schema.project_id == self.batch.p.current_project_id:
                qt_list_item = QListWidgetItem(list_schemas)
                curr_color = self.s.state_colors[schema.state_id].color()
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
        self.update_current_project_schemas()

    def update_current_project_schemas(self):
        list_visible_schemas_names = []
        list_visible_schemas_ids = []
        for schema in self.c.schemas_data:
            if schema.project_id == self.batch.p.current_project_id:
                list_visible_schemas_names.append(schema.schema_name)
                list_visible_schemas_ids.append(schema.id)
        self.list_visible_schemas_names = list_visible_schemas_names
        self.list_visible_schemas_ids = list_visible_schemas_ids

    def clear_list(self):
        self.list_visible_schemas_names = []
        self.list_visible_schemas_ids = []
        while self.list_schemas.count() > 0:
            self.list_schemas.takeItem(0)

    def reset_list(self):
        self.freeze_list_on_changed = 1
        index = self.c.current_schema_index
        self.clear_list()
        self.init_schemas_list()
        if index is not None and index > self.c.total_schemas:
            self.c.current_schema_index = index
            self.c.current_project_id = self.c.schemas_data[self.c.current_schema_index].id
        self.freeze_list_on_changed = 0

    def reload_schemas_data_and_refresh_list(self):
        self.c.clear_all_schemas_data()
        self.c.load_schemas()
        self.reset_list()

    def menu_set_active(self):
        self.batch.p.projects_data[self.batch.p.current_project_index].state = "ACTIVE"
        self.batch.p.projects_data[self.batch.p.current_project_index].state_id = 1  # TODO cnst
        self.batch.p.save_projects()
        self.reset_list()

    def menu_set_hold(self):
        self.batch.p.projects_data[self.batch.p.current_project_index].state = "HOLD"
        self.batch.p.projects_data[self.batch.p.current_project_index].state_id = 21
        self.batch.p.save_projects()
        self.reset_list()

    @staticmethod
    def menu_remove():
        print "  remove "  # TODO

    def menu_open(self):
        current_schema_id = self.c.list_visible_schemas_ids[self.c.current_schema_list_index]
        print "  list_schemas_double_clicked : ", current_schema_id
        sch = self.c.get_schema_by_id(current_schema_id)
        self.load_base_setup(sch.schema_name, sch.schemaVersion)

    def menu_save_as_next_version(self):
        cur_sch_index = self.batch.c.current_schema_index
        self.c.increase_curent_schema_version()

        self.reload_schemas_data_and_refresh_list()

        self.c.current_schema_index = cur_sch_index
        self.c.update_current_from_index(cur_sch_index)

        ret = self.batch.d.getSchemaBaseSetupFile(forceSchemaVersion=True)   # TODO  getSchemaBaseSetupFile PEP8

        cur_schema = self.c.schemas_data[cur_sch_index]
        print " [db] save as :", cur_schema.schema_name, cur_schema.id
        print " [db] save as :", ret
        self.batch.d.soco.save_curent_scene_as(ret[1])

    def menu_locate_base_setup(self):
        import subprocess
        prev_dir = self.batch.d.get_base_setup_dir()
        base_setup_dir = prev_dir[1]
        if self.comfun.path_exists(base_setup_dir, info="Base Setup"):
            subprocess.Popen('explorer "' + base_setup_dir + '"')

    @staticmethod
    def menu_spacer():
        print "  ____  "

    def on_right_click_show_menu(self, pos):
        global_pos = self.list_schemas.mapToGlobal(pos)
        right_menu = QMenu()
        right_menu.addAction("Open", self.menu_open)
        right_menu.addAction("Save current scene as next version", self.menu_save_as_next_version)
        right_menu.addAction("Remove", self.menu_remove)
        right_menu.addAction("________", self.menu_spacer)
        right_menu.addAction("Locate base setup", self.menu_locate_base_setup)
        right_menu.addAction("________", self.menu_spacer)
        right_menu.exec_(global_pos)

    def hide_all_forms(self):
        self.schema_form_create.hide()
        self.schema_form_copy.hide()
        self.schema_form_edit.hide()
        self.schema_form_remove.hide()
        self.create_form_state = 0
        self.copy_form_state = 0
        self.edit_form_state = 0
        self.remove_form_state = 0

    def fill_create_form(self):
        if self.batch.p.current_project_index > -1:
            txt = self.batch.p.projects_data[self.batch.p.current_project_index].project_name
            self.schema_form_create.schema_item_form_object.project_name = txt
            self.schema_form_create.schema_item_form_object.projectID = self.batch.p.current_project_id
            print "[db] (fill_create_form) new : ", txt, "   curr proj index: ", self.batch.p.current_project_index
        else:
            print "[wrn] current_project_index : ", self.batch.p.current_project_index

    def on_click_show_form_create(self):
        if self.create_form_state == 0:
            self.hide_all_forms()
            self.schema_form_create.show()
            self.fill_create_form()
            self.create_form_state = 1
        else:
            self.schema_form_create.hide()
            self.create_form_state = 0

    def on_click_form_edit_fill(self):
        if self.c.current_schema_index >= 0:
            cur_schema = self.c.schemas_data[self.c.current_schema_index]
            self.schema_form_edit.qt_fae_schema_name_edit.setText(cur_schema.schema_name)
            self.schema_form_edit.qt_fae_schema_version_edit.setText(str(cur_schema.schema_version))
            self.schema_form_edit.qt_fae_schema_description_edit.setText(cur_schema.description)

    def on_click_show_form_edit(self):
        if self.edit_form_state == 0:
            self.hide_all_forms()
            self.schema_form_edit.show()
            self.on_click_form_edit_fill()
            if self.c.current_schema_index >= 0:
                cur_schema = self.c.schemas_data[self.c.current_schema_index]
                self.schema_form_edit.update_actions_ui(cur_schema)
            self.edit_form_state = 1
        else:
            self.schema_form_edit.hide()
            self.edit_form_state = 0

    def update_copy_form(self):
        if self.c.current_schema_index >= 0:
            self.wfa_copy_schema.qt_edit_line.setText(
                self.c.schemas_data[self.c.current_schema_index].schema_name)

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
        if self.s.debug_level >= 1:
            print " [INF] on_changed_copy_name ", txt

    def on_changed_copy_target(self, qt_edit_line):
        el_txt = qt_edit_line.text()
        if self.comfun.is_float(el_txt):
            index = self.batch.p.get_index_from_id(int(el_txt))
            if index >= 0:
                qt_edit_line.setText(self.batch.p.projects_data[index].project_name)
            else:
                qt_edit_line.setText("[ERR] Wrong index: " + qt_edit_line.text())

        else:
            self.batch.p.get_index_from_name(qt_edit_line.text(), check_similar=True)
        print qt_edit_line.text()

    def on_clicked_copy_as(self):
        if self.batch.c.current_schema_index >= 0:
            new_name = self.new_name_on_copy
            if len(new_name) > 0:
                curr = self.batch.c.schemas_data[self.batch.c.current_schema_index]
                print "copy sch nAme", curr.project_name
                print "copy sch desc", curr.description
                print "copy sch proj ID", curr.projectID
                copied_schema_item = SchemaItem(0, new_name, curr.state_id, curr.state, curr.schema_version,
                                                curr.project_id, curr.project_name, curr.definition_id,
                                                curr.actions, curr.description)
                self.on_click_add_schema(copied_schema_item)
                self.schema_form_copy.hide()
                self.copy_form_state = 0
            else:
                self.top_ui.set_top_info(" put new name ")
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

    def on_click_confirm_remove_project(self):
        print "on_click_confirm_remove_project", self.c.current_schema_index
        if self.c.current_schema_index >= 0:
            self.c.remove_single_schema(index=self.c.current_schema_index, do_save=True)
            self.list_schemas.takeItem(self.c.current_schema_index + 1)
            self.c.lastSchema = None
            self.c.current_schema_index = None
            self.schema_form_remove.hide()
            self.remove_form_state = 0

    def add_single_schema(self, new_schema_item):
        new_schema_item.id = -1  # TODO check -1
        self.c.add_schema(new_schema_item, do_save=True)
        list_item = QListWidgetItem(self.list_schemas)
        list_item_widget = SchemaListItem(str(new_schema_item.id), new_schema_item.schema_name,
                                          new_schema_item.description, str(new_schema_item.schema_version))
        self.list_schemas.addItem(list_item)
        self.list_schemas.setItemWidget(list_item, list_item_widget)
        print "  [db] add schema DIR ", self.batch.p.current_project_id
        sch_dir = self.batch.p.projects_data[
                     self.batch.p.current_project_index].working_directory_absolute + new_schema_item.schema_name + "\\"
        self.batch.i.create_schema_directory(sch_dir)

    def on_click_add_schema(self, new_schema_item, save_as_base=0):
        if self.s.debug_level >= 4:
            print "  [db] addPRI projectID ", new_schema_item.projectID
            print "  [db] addPRI project_name ", new_schema_item.project_name
            print "  [db] addPRI schema_name ", new_schema_item.schema_name

        self.schema_form_create.compile_actions(new_schema_item.soft_id)
        if new_schema_item is None or len(new_schema_item.schema_name) == 0:
            self.top_ui.set_top_info(" Insert schema name ", 8)
        else:
            new_schema_item.state_id = 22
            new_schema_item.state = "ACTIVE"
            if self.comfun.is_float(new_schema_item.schema_version) is False:
                new_schema_item.schema_version = 1
            self.add_single_schema(copy.copy(new_schema_item))

            if save_as_base == 1:  # save as base setup
                save_as = self.batch.i.generate_tuple_base_setup_file_name(new_schema_item.schema_name)
                if self.s.debug_level >= 4:
                    print "\n  [db] with saveAs: ", save_as
                    print "\n  [db] wit2 saveAs: ", save_as[1]
                self.batch.d.soco.save_curent_scene_as(save_as[1])
            else:
                if self.s.debug_level >= 3:
                    print "\n  [db]  new_schema_item.save_as_base_state : ", save_as_base

            self.top_ui.set_top_info(" schema created, active schema:  " + new_schema_item.schema_name)
            # self.new_schema_item = self.batch.c.get_blank_schema()   # TODO  clear UI !!!  if clear var
            self.schema_form_create.clear_vars()
            self.schema_form_create.hide()
            self.create_form_state = 0
            self.update_current_project_schemas()

            self.mainw.tsk_ui.qt_schema_form_create.update_schema_names_combo(self.c.current_project_schemas_names,
                                                                              self.c.current_project_schemas_ids, 0)
            self.mainw.tsk_ui.qt_form_edit.update_schema_names_combo(self.c.current_project_schemas_names,
                                                                     self.c.current_project_schemas_ids, 0)
            self.reload_schemas_data_and_refresh_list()

    def on_click_update_schema(self, edited_schema_item):
        self.schema_form_edit.compile_actions(edited_schema_item.soft_id)
        if edited_schema_item is None or len(edited_schema_item.schema_name) == 0:
            self.top_ui.set_top_info(" Insert schema name ! ", 8)
            print " [WRN] insert schema name : ", edited_schema_item.schema_name
        else:
            self.c.update_schema(edited_schema_item, do_save=True)

            current_list_index = self.list_schemas.currentRow()
            ed_item = self.list_schemas.item(current_list_index)
            list_item_widget = SchemaListItem(str(edited_schema_item.id), edited_schema_item.schema_name,
                                              edited_schema_item.description, str(edited_schema_item.schema_version))
            self.list_schemas.setItemWidget(ed_item, list_item_widget)

            self.schema_form_edit.hide()
            self.edit_form_state = 0

    def load_base_setup(self, schema_name, version=1):
        file_to_load = self.batch.d.generate_tuple_base_setup_file_name(schema_name,
                                                                        ver=version)
        if file_to_load[0] == 1:
            if self.s.debug_level >= 1:
                print "\n  [INF]   loadFile: ", file_to_load[1]
            self.batch.d.soco.load_scene(file_to_load[1])
        else:
            if self.s.debug_level >= 1:
                print "\n  [ERR]   loadFile: ", file_to_load

    def on_list_schemas_double_clicked(self, item):
        if self.s.debug_level >= 3:
            print " [db] list_schemas_double_clicked ", self.c.current_schema_list_index, item
            if self.s.debug_level >= 7:
                print "    [db]", item
        self.menu_open()

    def on_list_schemas_current_changed(self, current_row):
        if self.freeze_list_on_changed == 0:
            if self.s.debug_level >= 3:
                print " [INF] list_schemas_current_changed ", self.list_schemas.currentRow()
                print " [INF] toolTip ", current_row.toolTip()

            self.last_list_item_nr = self.current_list_item_nr
            self.current_list_item_nr = self.list_schemas.currentRow()

            # update color of last item list
            if self.last_list_item_nr is not None:
                last_schema_id = self.list_visible_schemas_ids[self.last_list_item_nr - 1]
                last_schema_index = self.c.get_index_by_id(last_schema_id)
                last_item = self.list_schemas.item(self.last_list_item_nr)
                color_index = self.c.schemas_data[last_schema_index].state_id
                last_item.setBackground(self.s.state_colors[color_index].color())

            # update color of current item list
            if self.current_list_item_nr >= 0:
                current_schema_index = self.list_visible_schemas_ids[self.current_list_item_nr - 1]
                color_index = self.c.schemas_data[current_schema_index].state_id
                current_row.setBackground(self.s.state_colors_up[color_index].color())

                # update current schema variables and top info
                # if self.current_list_item_nr >= 1:
                current_schema_id = self.list_visible_schemas_ids[self.current_list_item_nr - 1]
                self.c.update_current_from_id(current_schema_id)
                cur_sch_name = self.c.schemas_data[current_schema_index].schema_name

                if self.top_ui is not None:
                    self.top_ui.set_top_info("Current schema:    " + cur_sch_name)
                else:
                    print " [ERR] top_ui undefined ", self.top_ui
            else:
                print " WRN [on sch chng] current_list_item_nr:", self.current_list_item_nr

            if self.edit_form_state == 1:
                cur_schema = self.c.current_schema
                self.schema_form_edit.update_actions_ui(cur_schema)

            if self.copy_form_state == 1:
                self.update_copy_form()
