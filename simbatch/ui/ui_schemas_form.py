try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *
# from core.schemas import SingleAction

class SchemaFormCreateOrEdit(QWidget):
    schema_item_form_object = None
    save_as_base_state = 1

    form_mode = 1  # 1 create    2 edit

    # actions
    actionsCount = 0
    actions_array = []
    action_widgets = []
    actions_string = ""

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

    def __init__(self, batch, mode, top):
        QWidget.__init__(self)
        self.actions_array = []
        self.action_widgets = []
        self.batch = batch
        self.schema_item_form_object = batch.sch.get_blank_schema()
        self.sts = self.batch.sts
        if mode == "edit":
            self.form_mode = 2
        self.init_ui_elements()
        self.add_defined_action_buttons()
        self.top_ui = top

    def proxy_basic_print(self):
        self.schema_item_form_object.basic_print()

    def proxy_detailed_print(self):
        self.schema_item_form_object.detailed_print()

    def init_ui_elements(self):
        qt_lay_outer_schema_form = QVBoxLayout()

        if self.sts.debug_level > 3:  # debug proxy SchemaItem object (used when adding or editing schema)
            db_buttons_group = QGroupBox()
            db_b1 = ButtonOnLayout("basic print", width=140)
            db_b2 = ButtonOnLayout("detailed print", width=170)
            qt_debug_buttons = WidgetGroup([SimpleLabel("debug buttons"), db_b1, db_b2])
            db_buttons_group.setLayout(qt_debug_buttons.qt_widget_layout)
            qt_lay_outer_schema_form.addWidget(db_buttons_group)
            db_b1.button.clicked.connect(self.proxy_basic_print)
            db_b2.button.clicked.connect(self.proxy_detailed_print)

        # fae   form add/edit
        qt_fae_schema_name = EditLineWithButtons("Name: ", label_minimum_size=60)
        self.qt_fae_schema_name_edit = qt_fae_schema_name.qt_edit_line
        qt_fae_schema_description = EditLineWithButtons("Description:  ", label_minimum_size=60)
        self.qt_fae_schema_description_edit = qt_fae_schema_description.qt_edit_line
        qt_fae_schema_version = EditLineWithButtons("Version:  ", label_minimum_size=55)
                                                        # , edit_maximum_size=70 ,  widgetMaximum = 40)
        self.qt_fae_schema_version_edit = qt_fae_schema_version.qt_edit_line
        qt_fae_schema_as_base = QCheckBox("Copy Current Scene As Base Setup")
        qt_fae_schema_as_base.setStyleSheet("""padding-left:130px;""")
        if self.form_mode == 2:
            qt_fae_schema_as_base.hide()

        qt_radio_buttons_fc_software = RadioButtons("Definitons:", self.batch.dfn.definitions_names,
                                                    self.batch.dfn.current_definition_index, self.on_radio_change)
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
        # qt_bg_schema_top.clicked.connect(self.schema_item_form_object.basic_print)

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

        if self.batch.dfn.current_definition_index is not None:
            self.change_current_definition(self.batch.dfn.current_definition_index)

    #
    ##
    ###
    # DEFINITIONS
    # DEFINITIONS
    # DEFINITIONS
    def change_current_definition(self, nr=None):
        self.remove_all_action_widgets()
        self.remove_all_defined_action_buttons()
        if nr is None:
            nr = self.batch.dfn.current_definition
        self.add_defined_action_buttons(nr)

    def on_radio_change(self, nr):  # on click definition change
        self.batch.logger.db(("on_radio_change definition", nr))
        self.change_current_definition(nr)

    # ACTIONS
    # ACTIONS
    # ACTIONS
    def compile_actions(self):
        self.actions_array = []
        for i, action_widget in enumerate(self.action_widgets):
            single_action = action_widget.get_current_action()
            if single_action is not None:
                self.actions_array.append(single_action)
                # TODO  compile acttion
                self.batch.logger.deepdb(("COMPILE ACTION", single_action))
            else:
                self.batch.logger.wrn(("(compile_actions)  None ACTION : ", i))

    def add_defined_action_button(self, button_txt, disabled=False):
        b = ButtonOnLayout(button_txt)
        self.qt_lay_fae_actions_buttons.addLayout(b.qt_widget_layout)
        if disabled:
            b.button.setEnabled(False)
        return b

    # add horizontal row of defined action buttons
    def add_defined_action_buttons(self, nr=None):
        if nr is None:
            nr = self.batch.dfn.current_definition
        curr_proj = self.batch.prj.current_project
        if curr_proj is not None:
            if nr is not None and nr < len(self.batch.dfn.definitions_array):
                for action_group in self.batch.dfn.definitions_array[nr].grouped_actions_array:
                    b = self.add_defined_action_button(action_group.name)
                    b.button.clicked.connect(lambda a=action_group: self.on_click_defined_action_button(a, curr_proj))
        else:
            self.batch.logger.wrn("Current project undefined !")

    # on click one of horizontal button add action widget to vertical list of schema actions
    def on_click_defined_action_button(self, group_of_actions, curr_proj):  # , force_val=0
        combo_items = []
        combo_val = []

        qt_lay = self.qt_lay_fae_actions
        button_2 = group_of_actions.actions[0].addional_butt_caption
        if group_of_actions.actions_count == 1:   # single action, no combo
            action_widget = ActionWidget(group_of_actions.group_id, group_of_actions.name, group_of_actions,
                                         text_on_button_2=button_2)
        else:  # grouped actions :  import ANI,CAM,ENV
            for i, a in enumerate(group_of_actions.actions):
                combo_items.append(a.mode)
                combo_val.append(a.default_value)
            action_widget = ActionWidget(group_of_actions.group_id, group_of_actions.name, group_of_actions,
                                         text_on_button_2=button_2,
                                         edit_txt=combo_val[0], combo_items=combo_items, combo_val=combo_val)

        qt_lay.addWidget(action_widget)
        self.action_widgets.append(action_widget)

        # action_widget.qt_button_1.clicked.connect(
        #     lambda: group_of_actions.get_get_file(group_of_actions.actionWidget.edit,
        #                                           curr_proj.working_directory,
        #                                           action_type, QFileDialog)
        # )

        # if button_2 is not None and len(button_2) > 0:
        #     action_widget.qt_button_2.clicked.connect(
        #         lambda: self.on_clicked_addional_action_button(group_of_actions)
        #     )

        # if len(combo_items) > 0:
        #     action_widget.qt_combo.currentIndexChanged.connect(
        #         lambda: self.on_change_combo_action(action_widget, group_of_actions)
        #     )

    def on_clicked_addional_action_button(self, act):
        self.batch.logger.db(("on_clicked_addional_action_button", act))
        # TODO

    # @staticmethod
    # def on_change_combo_action(action_widget, software_action):
    #     action_widget.qt_edit.setText(software_action.actions[action_widget.qt_combo.currentIndex()].default_value)
    #     action_widget.action_data.current_sub_action_index = action_widget.qt_combo.currentIndex()


    # remove horizontal row of defined actions buttons
    def remove_all_defined_action_buttons(self):
        while self.qt_lay_fae_actions_buttons.count() > 0:
            b = self.qt_lay_fae_actions_buttons.itemAt(0)
            c = b.takeAt(0)
            c.widget().deleteLater()
            self.qt_lay_fae_actions_buttons.takeAt(0)

    def remove_all_action_widgets(self):
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


    # SCHEMA PROXY OBJECT
    # SCHEMA PROXY OBJECT
    # SCHEMA PROXY OBJECT

    # clear helper form object (store schema data)
    def clear_vars(self):
        self.schema_item_form_object = self.batch.sch.get_blank_schema()

    def update_form_data(self, schema_item):   # old update_actions_ui
        self.clear_vars()
        self.schema_item_form_object.project_id = schema_item.project_id
        self.schema_item_form_object.definition_name = schema_item.definition_name
