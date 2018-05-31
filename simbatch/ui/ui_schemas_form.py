import copy

try:  # Maya 2016
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        print "PySide import ERROR"

from widgets import *
# from core.schemas import SingleAction
from simbatch.core.actions import MultiAction, SingleAction


class SchemaFormCreateOrEdit(QWidget):
    schema_item_form_object = None
    save_as_base_state = 1

    form_mode = 1  # 1 create    2 edit

    # actions
    form_actions_count = 0
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
    schema_form_buttons = None

    def __init__(self, batch, mode, top):
        QWidget.__init__(self)
        # self.actions_array = []
        self.action_widgets = []
        self.batch = batch
        self.schema_item_form_object = batch.sch.get_blank_schema()
        self.sts = self.batch.sts
        if mode == "edit":
            self.form_mode = 2
        self.init_ui_elements()
        self.top_ui = top

    def form_basic_print(self):
        self.batch.logger.raw("\n schema_item_form_object:")
        self.schema_item_form_object.basic_print()
        self.batch.logger.raw("\n form action_widgets count: {}".format(len(self.action_widgets)))
        for i, aw in enumerate(self.action_widgets):
            self.batch.logger.raw(" action_widget {}  {}".format(i, aw.qt_label.text()))

    def form_detailed_print(self):
        self.batch.logger.raw("\nschema_item_form_object:")
        self.schema_item_form_object.detailed_print()
        self.batch.logger.raw("\nform action_widgets count:  {}".format(len(self.action_widgets)))
        for i, aw in enumerate(self.action_widgets):
            self.batch.logger.raw(" action_widget {}  id:{}  label:{}  edit_val:{}".format(i, aw.widget_id,
                                                                                           aw.qt_label.text(),
                                                                                           aw.edit_val, aw.ui_info))
        self.batch.logger.raw("forms action_array count:  {}".format(len(self.schema_item_form_object.actions_array)))
        for a in self.schema_item_form_object.actions_array:
            self.batch.logger.raw("action: {}   {}  {}".format(a.name, a.default_value, a.actual_value))

    def init_ui_elements(self):
        qt_lay_outer_schema_form = QVBoxLayout()

        if self.sts.debug_level > 3:  # debug proxy SchemaItem object (used when adding or editing schema)
            db_buttons_group = QGroupBox()
            db_b1 = ButtonOnLayout("basic print", width=140)
            db_b2 = ButtonOnLayout("detailed print", width=170)
            qt_debug_buttons = WidgetGroup([SimpleLabel("debug buttons"), db_b1, db_b2])
            db_buttons_group.setLayout(qt_debug_buttons.qt_widget_layout)
            qt_lay_outer_schema_form.addWidget(db_buttons_group)
            db_b1.button.clicked.connect(self.form_basic_print)
            db_b2.button.clicked.connect(self.form_detailed_print)

        # fae   form add/edit
        qt_fae_schema_name = EditLineWithButtons("Name: ", label_minimum_size=60)
        self.qt_fae_schema_name_edit = qt_fae_schema_name.qt_edit_line
        qt_fae_schema_description = EditLineWithButtons("Description:  ", label_minimum_size=60)
        self.qt_fae_schema_description_edit = qt_fae_schema_description.qt_edit_line
        qt_fae_schema_version = EditLineWithButtons("Version:  ", label_minimum_size=55)
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
            schema_form_buttons.qt_third_check_box.stateChanged.connect(self.on_changed_save_as_base_setup)
        else:
            schema_form_buttons = ButtonWithCheckBoxes("Save schema", pin_text="pin", cb2_text="Crowd mode")

        self.schema_form_buttons = schema_form_buttons
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

        if schema_form_buttons.qt_second_check_box is not None:
            schema_form_buttons.qt_second_check_box.setEnabled(False)    # TODO crowd mode

        if self.batch.dfn.current_definition_index is not None:
            self.change_current_definition(self.batch.dfn.current_definition_index)
            if self.batch.dfn.current_definition_name == "Stand-alone":
                if schema_form_buttons.qt_third_check_box is not None:
                    schema_form_buttons.qt_third_check_box.setChecked(False)
                    schema_form_buttons.qt_third_check_box.setEnabled(False)

    #
    ##
    ###
    # DEFINITIONS
    # DEFINITIONS
    # DEFINITIONS
    def change_current_definition(self, nr=None):
        self.batch.logger.deepdb(("change_current_definition ", nr))
        self.remove_all_action_widgets()
        self.remove_all_defined_action_buttons()
        if nr is None:
            nr = self.batch.dfn.current_definition_index
        else:
            self.batch.dfn.current_definition_index = nr
        self.add_defined_action_buttons(nr)
        self.batch.dfn.update_current_definition(nr)

    def on_radio_change(self, nr):  # on click definition change
        self.batch.logger.db(("on_radio_change definition", nr))
        self.change_current_definition(nr=nr)
        if self.batch.dfn.current_definition_name == "Stand-alone":
            if self.schema_form_buttons.qt_third_check_box is not None:
                self.schema_form_buttons.qt_third_check_box.setChecked(False)
                self.schema_form_buttons.qt_third_check_box.setEnabled(False)
        else:
            if self.schema_form_buttons.qt_third_check_box is not None:
                self.schema_form_buttons.qt_third_check_box.setEnabled(True)

    def add_defined_action_button(self, button_txt, disabled=False):
        b = ButtonOnLayout(button_txt)
        self.qt_lay_fae_actions_buttons.addLayout(b.qt_widget_layout)
        if disabled:
            b.button.setEnabled(False)
        return b

    # add horizontal row of defined action buttons
    def add_defined_action_buttons(self, nr=None):
        self.batch.logger.deepdb(("add act but, dfn idx:", nr))
        if nr is None:
            nr = self.batch.dfn.current_definition_index
        curr_proj = self.batch.prj.current_project
        if curr_proj is not None:
            if nr is not None and nr < len(self.batch.dfn.definitions_array):
                for multi_action in self.batch.dfn.definitions_array[nr].multi_actions_array:
                    b = self.add_defined_action_button(multi_action.name)
                    b.button.clicked.connect(lambda a=multi_action: self.on_click_defined_action_button(a))
            else:
                if nr is None:
                    self.batch.logger.wrn("add act but nr is None !")
                else:
                    self.batch.logger.wrn(("add act but nr < definitions count ___ ", nr, "  < ",
                                           len(self.batch.dfn.definitions_array)))
        else:
            self.batch.logger.wrn("Current project undefined !")


    def add_action_widget_to_form(self, multi_action):
        combo_items = []
        qt_lay = self.qt_lay_fae_actions
        button_1_caption = None
        button_2_caption = None
        button_1_function_str = None
        button_2_function_str = None
        if len(multi_action.actions) > 0:
            if multi_action.actions[0].ui is not None:
                if len(multi_action.actions[0].ui) > 0:
                    button_1_caption = multi_action.actions[0].ui[0][0]
                    button_1_function_str = multi_action.actions[0].ui[0][1]
                if len(multi_action.actions[0].ui) > 1:
                    button_2_caption = multi_action.actions[0].ui[1][0]
                    button_2_function_str = multi_action.actions[0].ui[1][1]

        batch = self.batch   # share logger and interaction from definition
        top = self.top_ui
        if multi_action.actions_count == 0:   # incorrectly defined action
            action_widget = ActionWidget(batch, top, -1, "incorrectly defined action", MultiAction(-1, "empty action"))
            single_action = SingleAction(multi_action.name, "err", "incorrectly defined action", "null")

        else:
            single_action = SingleAction(multi_action.actions[0].name, multi_action.actions[0].description,
                                         multi_action.actions[0].default_value, multi_action.actions[0].template)

            if multi_action.actions_count == 1:   # single action, no combo
                action_widget = ActionWidget(batch, top, self.form_actions_count+1, multi_action.actions[0].name,
                                             multi_action,
                                             button_1_caption=button_1_caption, button_1_fun_str=button_1_function_str,
                                             button_2_caption=button_2_caption, button_2_fun_str=button_2_function_str)

            else:            # multi action :  import ANI, CAM, ENV
                for i, a in enumerate(multi_action.actions):
                    combo_items.append(a.mode)
                action_widget = ActionWidget(batch, top, self.form_actions_count+1, multi_action.name, multi_action,
                                             button_1_caption=button_1_caption, button_1_fun_str=button_1_function_str,
                                             button_2_caption=button_2_caption, button_2_fun_str=button_2_function_str,
                                             combo_items=combo_items)

        qt_lay.addWidget(action_widget)
        self.action_widgets.append(action_widget)
        self.schema_item_form_object.actions_array.append(single_action)
        self.form_actions_count += 1

    # on click one of horizontal button:
    # ADD action widget to vertical list of schema's actions
    def on_click_defined_action_button(self, multi_action):
        self.add_action_widget_to_form(multi_action)

    # ACTIONS
    # ACTIONS
    # ACTIONS
    def compile_actions(self):
        del self.schema_item_form_object.actions_array[:]
        for a_wi in self.action_widgets:
            if len(a_wi.multi_action.actions) > a_wi.current_action_index:
                self.schema_item_form_object.actions_array.append(a_wi.multi_action.actions[a_wi.current_action_index])

    # remove horizontal row of defined actions buttons
    def remove_all_defined_action_buttons(self):
        while self.qt_lay_fae_actions_buttons.count() > 0:
            b = self.qt_lay_fae_actions_buttons.itemAt(0)
            c = b.takeAt(0)
            c.widget().deleteLater()
            self.qt_lay_fae_actions_buttons.takeAt(0)

    def remove_all_action_widgets(self):
        del self.action_widgets[:]
        while self.qt_lay_fae_actions.count() > 0:
            b = self.qt_lay_fae_actions.itemAt(0)
            b.widget().deleteLater()
            self.qt_lay_fae_actions.takeAt(0)
        self.form_actions_count = 0

    def refresh_actions_ui(self):
        cur_index = self.batch.dfn.current_definition_index
        self.remove_all_defined_action_buttons()
        self.remove_all_action_widgets()
        self.batch.dfn.current_definition_index = cur_index
        self.add_defined_action_buttons(nr=cur_index)

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
        self.schema_item_form_object.based_on_definition = schema_item.based_on_definition
        self.qt_fae_schema_name_edit.setText(schema_item.schema_name)
        self.qt_fae_schema_version_edit.setText(str(schema_item.schema_version))
        self.qt_fae_schema_description_edit.setText(schema_item.description)
        self.schema_item_form_object.actions_array = copy.deepcopy(schema_item.actions_array)

        self.remove_all_action_widgets()
        for i, ac in enumerate(copy.deepcopy(self.schema_item_form_object.actions_array)):
            #if isinstance(ac, SingleAction):
            print "TODO SingleAction ", ac.name, len(self.schema_item_form_object.actions_array)  # TODO
            mac = MultiAction(i, ac.name)
            mac.add_single_action(copy.deepcopy(ac))
            self.add_action_widget_to_form(mac)
            # else:
                # self.add_action_widget_to_form(ac)