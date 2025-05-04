from typing import List, Optional, Any
import copy


try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    raise Exception('PySide import ERROR!  Please install PySide or PySide2')

from .widgets import *


class SchemaFormCreateOrEdit(QWidget):
    """A form widget for creating or editing schema items.
    
    This class handles the UI and logic for creating new schemas or editing existing ones.
    It manages action widgets and their interactions with the schema definition system.
    """
    
    local_schema_item: Optional[Any] = None
    save_as_base_state: int = 1
    form_mode: int = 1  # 1 create, 2 edit
    form_actions_count: int = 0
    action_widgets: List[Any] = []
    actions_string: str = ""

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

    def __init__(self, batch: Any, mode: str, top: Any) -> None:
        """Initialize the schema form.
        
        Args:
            batch: The main batch object containing core functionality
            mode: The form mode ("create" or "edit")
            top: The top-level UI object
        """
        super().__init__()
        self.action_widgets = []
        self.batch = batch
        self.local_schema_item = batch.sch.get_blank_schema()
        self.sts = self.batch.sts
        if mode == "edit":
            self.form_mode = 2
        self.init_ui_elements()
        self.top_ui = top

    def form_basic_print(self):
        self.batch.logger.raw("\n__schema item FORM object__")
        self.local_schema_item.basic_print()
        self.batch.logger.raw("\n\n form action_widgets count: {}".format(len(self.action_widgets)))
        for i, aw in enumerate(self.action_widgets):
            self.batch.logger.raw(" action_widget {}  {}".format(i, aw.qt_label.text()))

    def form_detailed_print(self):
        self.batch.logger.raw("\n__schema item FORM object__")
        self.local_schema_item.detailed_print()
        self.batch.logger.raw("\n\nform action_widgets count:  {}".format(len(self.action_widgets)))
        for i, aw in enumerate(self.action_widgets):
            self.batch.logger.raw(" action_widget {}  id:{}  label:{}  edit_val:{}".format(i, aw.widget_id,
                                                                                           aw.qt_label.text(),
                                                                                           aw.edit_val, aw.ui_info))
        self.batch.logger.raw("\nforms action_array count:  {}".format(len(self.local_schema_item.actions_array)))
        for a in self.local_schema_item.actions_array:
            self.batch.logger.raw("action: {}  def_val:{}  act_val:{}  mode:{}".format(a.name, a.ui[0],
                                                                                       # a.default_value
                                                                                       a.actual_value, a.mode))

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
        self.qt_fae_schema_name_edit = qt_fae_schema_name    # if sch name exist -> color RED
        self.qt_fae_schema_name_edit.qt_edit_line.textChanged.connect(lambda: self.on_change_sch_name(
            self.qt_fae_schema_name_edit.get_txt(), self.form_mode))
        qt_fae_schema_description = EditLineWithButtons("Description:  ", label_minimum_size=60)
        self.qt_fae_schema_description_edit = qt_fae_schema_description.qt_edit_line
        qt_fae_schema_version = EditLineWithButtons("Version:  ", label_minimum_size=55)
        self.qt_fae_schema_version_edit = qt_fae_schema_version.qt_edit_line
        qt_fae_schema_as_base = QCheckBox("Copy Current Scene As Base Setup")
        qt_fae_schema_as_base.setStyleSheet("""padding-left:130px;""")
        if self.form_mode == 2:
            qt_fae_schema_as_base.hide()

        qt_radio_buttons_fc_software = RadioButtons("Definitions:", self.batch.dfn.definitions_names,
                                                    self.batch.dfn.current_definition_index, self.on_radio_change)
        if len(self.batch.dfn.definitions_names) == 1:
            self.batch.dfn.current_definition_index = 0

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
        self.local_schema_item.based_on_definition = self.batch.dfn.current_definition.name

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

    def add_defined_action_buttons(self, nr: Optional[int] = None) -> None:
        """Add action buttons based on the current definition.
        
        Args:
            nr: Optional index of the definition to use. If None, uses current definition.
        """
        self.batch.logger.deepdb(f"Adding action buttons for definition index: {nr}")
        
        if nr is None:
            nr = self.batch.dfn.current_definition_index
            
        curr_proj = self.batch.prj.current_project
        if curr_proj is None:
            self.batch.logger.wrn("Current project undefined!")
            return
            
        if nr is None:
            self.batch.logger.wrn("Definition index is None!")
            return
            
        if nr >= len(self.batch.dfn.definitions_array):
            self.batch.logger.wrn(f"Definition index {nr} out of range (max: {len(self.batch.dfn.definitions_array)})")
            return
            
        try:
            for multi_action in self.batch.dfn.definitions_array[nr].multi_actions_array:
                if not hasattr(multi_action, 'name'):
                    self.batch.logger.err(f"Invalid multi_action object: {multi_action}")
                    continue
                    
                b = self.add_defined_action_button(multi_action.name)
                def create_click_handler(action):
                    return lambda: self.on_click_defined_action_button(action)
                b.button.clicked.connect(create_click_handler(multi_action))
        except Exception as e:
            self.batch.logger.err(f"Error adding action buttons: {str(e)}")

    def create_action_widget(self, multi_action: Any) -> Any:
        """Create a widget for a multi-action.
        
        Args:
            multi_action: The multi-action object to create a widget for
            
        Returns:
            An ActionWidget instance for the given multi-action
        """
        if not hasattr(multi_action, 'actions'):
            self.batch.logger.err(f"Invalid multi_action object: {multi_action}")
            dummy_multiaction = self.batch.dfn.create_multiaction(-1, "empty action")
            return ActionWidget(self.batch, self.top_ui, self, "incorrectly defined action", dummy_multiaction)
            
        combo_items = []
        button_1_caption = None
        button_2_caption = None
        button_1_function_str = None
        button_2_function_str = None
        
        if len(multi_action.actions) > 0 and hasattr(multi_action.actions[0], 'ui'):
            if len(multi_action.actions[0].ui) > 1:
                button_1_caption = multi_action.actions[0].ui[1][0]
                button_1_function_str = multi_action.actions[0].ui[1][1]
            if len(multi_action.actions[0].ui) > 2:
                button_2_caption = multi_action.actions[0].ui[2][0]
                button_2_function_str = multi_action.actions[0].ui[2][1]

        if multi_action.actions_count == 0:
            self.batch.logger.wrn("Creating widget for empty multi_action")
            dummy_multiaction = self.batch.dfn.create_multiaction(-1, "empty action")
            return ActionWidget(self.batch, self.top_ui, self, "incorrectly defined action", dummy_multiaction)

        # Single action, no combo    
        if multi_action.actions_count == 1:
            if len(multi_action.actions[0].actual_value) == 0:
                multi_action.actions[0].actual_value = multi_action.actions[0].ui[0]
            return ActionWidget(
                self.batch, self.top_ui, self, 
                multi_action.actions[0].name,
                copy.deepcopy(multi_action),
                button_1_caption=button_1_caption,
                button_1_fun_str=button_1_function_str,
                button_2_caption=button_2_caption,
                button_2_fun_str=button_2_function_str
            )
            
        # Multi-action case
        for action in multi_action.actions:
            combo_items.append(action.mode)
            action.actual_value = action.ui[0]
            
        return ActionWidget(
            self.batch, self.top_ui, self,
            multi_action.name,
            copy.deepcopy(multi_action),
            button_1_caption=button_1_caption,
            button_1_fun_str=button_1_function_str,
            button_2_caption=button_2_caption,
            button_2_fun_str=button_2_function_str,
            combo_items=combo_items
        )

    def add_action_widget_to_form(self, multi_action: Any) -> None:
        try:
            new_widget = self.create_action_widget(multi_action)
            self.qt_lay_fae_actions.addWidget(new_widget)
            self.action_widgets.append(new_widget)
            current_action = new_widget.get_current_action()
            if current_action is not None:
                self.local_schema_item.actions_array.append(current_action)
            self.form_actions_count += 1
        except Exception as e:
            self.batch.logger.err(f"Error adding action widget: {str(e)}")

    def on_click_defined_action_button(self, multi_action: Any) -> None:
        """ on click one of horizontal button """
        """ ADD action widget to vertical list of schema's actions """
        try:
            if not hasattr(multi_action, 'actions'):
                self.batch.logger.err(f"Invalid multi_action object: {multi_action}")
                return
            self.add_action_widget_to_form(copy.deepcopy(multi_action))
        except Exception as e:
            self.batch.logger.err(f"Error handling action button click: {str(e)}")

    # ACTIONS
    # ACTIONS
    # ACTIONS
    """   create/update SCHEMA actions from current widgets """
    def compile_actions(self):
        del self.local_schema_item.actions_array[:]
        for a_wi in self.action_widgets:
            if len(a_wi.multi_action.actions) > a_wi.current_action_index:
                self.local_schema_item.actions_array.append(a_wi.multi_action.actions[a_wi.current_action_index])

    """ remove horizontal row of defined actions buttons """
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

    def remove_action_widget_from_form(self, index):
        # reset id for older widgets
        for i, aw in enumerate(self.action_widgets):
            if i > index-1:
                aw.widget_id -= 1
        del self.action_widgets[index-1]
        self.form_actions_count -= 1

    def move_action_widget_up(self, index):
        awa = self.action_widgets  # action widets array

        if index > 1:
            self.batch.logger.deepdb(" move up " + str(index)  +"    id:"+  str(awa[index-1].widget_id)  )
            for i, aw in enumerate(awa):
                if i >= index - 2:
                    self.qt_lay_fae_actions.removeWidget(awa[i])

            awa[index - 1], awa[index-2] = awa[index-2], awa[index - 1]
            awa[index - 1].widget_id, awa[index-2].widget_id = awa[index-2].widget_id, awa[index - 1].widget_id

            for i, aw in enumerate(awa):
                if i >= index - 2:
                    self.qt_lay_fae_actions.addWidget(awa[i])
        else:
            self.batch.logger.inf("First element, cant be moved up ")

    def move_action_widget_dwn(self, index):
        awa = self.action_widgets   # action widets array

        if index < len(awa):
            self.batch.logger.deepdb(" move dwn " + str(index)  +"    id:"+  str(awa[index-1].widget_id)  )
            for i, aw in enumerate(awa):
                if i >= index -1:
                    self.qt_lay_fae_actions.removeWidget(awa[i])

            awa[index-1], awa[index] = awa[index], awa[index-1]
            awa[index-1].widget_id, awa[index].widget_id = awa[index].widget_id, awa[index-1].widget_id

            for i, aw in enumerate(awa):
                if i >= index -1:
                    self.qt_lay_fae_actions.addWidget(awa[i])
        else:
            self.batch.logger.inf("Last element, cant be moved down ")

    def refresh_actions_ui(self):
        cur_index = self.batch.dfn.current_definition_index
        self.remove_all_defined_action_buttons()
        self.remove_all_action_widgets()
        self.batch.dfn.update_current_definition(cur_index)
        self.add_defined_action_buttons(nr=cur_index)

    #
    ##
    ###
    def on_edit_schema_name(self, txt):
        self.local_schema_item.schema_name = txt
        if self.form_mode == 1:
            self.qt_bg_schema_top.setTitle("Create Schema : " + txt)
        else:
            self.qt_bg_schema_top.setTitle("Edit Schema : " + txt)

    def on_change_sch_name(self, name, mode):
        for s in self.batch.sch.schemas_data:
            show_red = False
            if mode == 1:    # mode create
                if name == s.schema_name:
                    show_red = True
            else:            # mode edit
                if name == s.schema_name and self.batch.sch.current_schema.id != s.id:
                    show_red = True

            if show_red:
                self.qt_fae_schema_name_edit.label.setText("Name !")
                self.qt_fae_schema_name_edit.label.setStyleSheet("""color:#FF0000;font-weight: bold;""")
                return True

        self.qt_fae_schema_name_edit.label.setText("Name")
        self.qt_fae_schema_name_edit.label.setStyleSheet("""color:#000000""")

    def on_edit_schema_description(self, txt):
        self.local_schema_item.description = txt

    def on_edit_schema_version(self, txt):
        self.local_schema_item.schema_version = int(txt)

    def on_changed_save_as_base_setup(self, state):
        if state:
            self.save_as_base_state = 1
        else:
            self.save_as_base_state = 0

    # SCHEMA ITEM : local form object
    # clear
    def clear_vars(self):
        self.local_schema_item = self.batch.sch.get_blank_schema()

    def update_widgets(self, schema_item):
        pass

    """  on show form create / edit / change item """
    def update_local_schema_item(self, schema_item):
        self.qt_fae_schema_name_edit.qt_edit_line.setText(schema_item.schema_name)
        self.qt_fae_schema_version_edit.setText(str(schema_item.schema_version))
        self.qt_fae_schema_description_edit.setText(schema_item.description)
        self.local_schema_item = copy.deepcopy(schema_item)
        self.local_schema_item.id = 0

    def create_widgets(self, schema_item):
        schema_definition = self.batch.dfn.get_definition_by_name(schema_item.based_on_definition)
        if schema_definition is None:
            self.batch.logger.err(("definition", schema_item.based_on_definition, "not exist"))
        else:
            for act in schema_item.actions_array:
                mac = schema_definition.get_multiaction_by_name(act.name)
                if mac is not None:
                    self.add_action_widget_to_form(mac)
                else:
                    self.batch.logger.err(("multiaction:", act.name, "in definition:", schema_item.based_on_definition,
                                           "not exist"))

    def setup_widgets(self, schema_item):
        for i, wi in enumerate(self.action_widgets):
            if wi.qt_combo is not None:
                act = schema_item.actions_array[i]
                ret = wi.qt_combo.findText(act.mode)
                wi.qt_combo.setCurrentIndex(ret)
                wi.qt_edit.setText(act.actual_value)
            else:
                act = schema_item.actions_array[i]
                wi.qt_edit.setText(act.actual_value)

    """ on change schema item and show form """
    def update_form(self, schema_item):
        self.clear_vars()
        self.remove_all_action_widgets()
        self.create_widgets(schema_item)
        self.setup_widgets(schema_item)
        self.update_local_schema_item(schema_item)
