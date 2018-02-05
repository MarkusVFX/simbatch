try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *
from core.projects import *


class ProjectListItem(QWidget):
    def __init__(self, txt_id, txt_name, working_directory, txt_description, parent=None):
        super(ProjectListItem, self).__init__(parent)
        self.qt_widget = QWidget(self)
        self.qt_label_font = QFont()
        self.qt_label_font.setPointSize(8)

        self.qt_lay = QHBoxLayout(self.qt_widget)
        self.qt_lay.setSpacing(0)
        self.qt_lay.setContentsMargins(0, 0, 0, 0)

        self.qt_label_id = QLabel(txt_id)
        self.qt_label_id.setFont(self.qt_label_font)
        self.qt_label_id.setMinimumWidth(22)
        self.qt_label_id.setMaximumWidth(22)
        self.qt_lay.addWidget(self.qt_label_id)

        self.qt_label_name = QLabel(txt_name)
        self.qt_label_name.setStyleSheet("""padding-left:4px;""")
        self.qt_label_name.setFont(self.qt_label_font)
        self.qt_lay.addWidget(self.qt_label_name)
        self.qt_label_directory = QLabel(working_directory)
        self.qt_label_directory.setFont(self.qt_label_font)
        self.qt_lay.addWidget(self.qt_label_directory)
        self.qt_label_description = QLabel(txt_description)
        self.qt_label_description.setFont(self.qt_label_font)
        self.qt_lay.addWidget(self.qt_label_description)

        self.setLayout(self.qt_lay)


class ProjectsUI:
    qt_list_projects = None
    qt_widget_projects = None

    batch = None
    top_ui = None
    mainw = None

    qt_form_add = None
    qt_form_edit = None
    qt_form_remove = None

    add_form_state = 0      # 0 hidden form, 1 showed form
    edit_form_state = 0     # 0 hidden form,  1 showed form
    remove_form_state = 0   # 0 hidden form,  1 showed form

    comfun = None
    debug_level = None

    freeze_list_on_changed = 0
    last_project_index = None    # used for list item color change to unselected

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.prj = batch.prj
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.debug_level = batch.sts.debug_level
        self.top_ui = top
        self.mainw = mainw

        qt_list_projects = QListWidget()
        # qt_list_projects.setSelectionMode(QAbstractItemView.MultiSelection)   TODO multiselect list item
        qt_list_projects.setSelectionMode(QAbstractItemView.NoSelection)
        qt_list_projects.currentItemChanged.connect(self.on_list_current_changed)
        qt_list_projects.setContextMenuPolicy(Qt.CustomContextMenu)
        qt_list_projects.customContextMenuRequested.connect(self.on_right_click_show_menu)

        qt_list_projects.setFrameShadow(QFrame.Raised)
        qt_list_projects.setSpacing(1)
        p = qt_list_projects.sizePolicy()
        p.setVerticalPolicy(QSizePolicy.Policy.Maximum)

        self.qt_list_projects = qt_list_projects

        qt_widget_projects = QWidget()
        self.qt_widget_projects = qt_widget_projects
        qt_project_main_layout = QVBoxLayout(qt_widget_projects)
        qt_project_main_layout.setContentsMargins(0, 0, 0, 0)

        qt_lay_projects_lists = QHBoxLayout()
        qt_lay_projects_forms = QHBoxLayout()
        qt_lay_projects_buttons = QHBoxLayout()

        # ADD
        # ADD ADD
        # ADD ADD ADD
        qt_form_add = QWidget()
        qt_form_add_layout_ext = QVBoxLayout()
        qt_form_add.setLayout(qt_form_add_layout_ext)

        qt_form_add_layout = QVBoxLayout()
        self.qt_form_add = qt_form_add

        # wfa :  element belongs to widget form add
        wfa_proj_name_label = SimpleLabel("New project name: ")
        wfa_project_name_edit = EditLineWithButtons(" ", label_minimum_size=7)
        self.wfa_project_name_edit = wfa_project_name_edit
        wfa_project_dir_label = SimpleLabel("Project directory: ")
        wfa_project_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        self.wfa_project_dir_edit = wfa_project_dir_edit
        wfa_working_dir_label = SimpleLabel("Working directory: ")
        wfa_working_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        self.wfa_working_dir_edit = wfa_working_dir_edit
        wfa_cam_dir_label = SimpleLabel("Cameras directory: ")
        wfa_cam_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        self.wfa_cam_dir_edit = wfa_cam_dir_edit
        wfa_ani_dir_label = SimpleLabel("Animation cache directory: ")
        wfa_ani_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        self.wfa_ani_dir_edit = wfa_ani_dir_edit
        wfa_descr_edit = EditLineWithButtons("Description: ", label_minimum_size=80)
        self.wfa_descr_edit = wfa_descr_edit

        wfa_buttons = ButtonWithCheckBoxes("Add project", pin_text="pin", cb2_text="Set as default project")
        wfa_project_dir_edit.button_1.clicked.connect(
            lambda: self.fa_get_project_directory(wfa_project_dir_edit.qt_edit_line))
        wfa_working_dir_edit.button_1.clicked.connect(
            lambda: self.fa_get_working_directory(wfa_working_dir_edit.qt_edit_line))
        wfa_cam_dir_edit.button_1.clicked.connect(
            lambda: self.fa_get_cam_directory(wfa_cam_dir_edit.qt_edit_line))
        wfa_ani_dir_edit.button_1.clicked.connect(
            lambda: self.fa_get_cache_directory(wfa_ani_dir_edit.qt_edit_line))
        wfa_buttons.button.clicked.connect(
            lambda: self.on_click_add_project(wfa_project_name_edit.get_txt(), wfa_project_dir_edit.get_txt(),
                                              wfa_working_dir_edit.get_txt(), wfa_cam_dir_edit.get_txt(),
                                              wfa_ani_dir_edit.get_txt(), wfa_descr_edit.get_txt(),
                                              wfa_buttons.qt_pin_check_box.isChecked()))

        qt_form_add_layout.addLayout(wfa_proj_name_label.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_project_name_edit.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_project_dir_label.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_project_dir_edit.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_working_dir_label.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_working_dir_edit.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_cam_dir_label.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_cam_dir_edit.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_ani_dir_label.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_ani_dir_edit.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_descr_edit.qt_widget_layout)
        qt_form_add_layout.addLayout(wfa_buttons.qt_widget_layout)

        qt_gb_add = QGroupBox()
        qt_gb_add.setLayout(qt_form_add_layout)
        qt_form_add_layout_ext.addWidget(qt_gb_add)

        # EDIT
        # EDIT EDIT
        # EDIT EDIT EDIT
        qt_form_edit = QWidget()
        qt_form_edit_layout_ext = QVBoxLayout()
        qt_form_edit.setLayout(qt_form_edit_layout_ext)

        qt_form_edit_layout = QVBoxLayout()
        self.qt_form_edit = qt_form_edit

        wfe_project_name_label = SimpleLabel("Project name: ")
        wfe_project_name_edit = EditLineWithButtons(" ", label_minimum_size=7)

        wfe_project_dir_label = SimpleLabel("Project directory: ")
        wfe_project_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        wfe_project_working_dir_label = SimpleLabel("Working directory: ")
        wfe_project_working_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        wfe_project_cam_dir_label = SimpleLabel("Cameras directory: ")
        wfe_project_cam_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        wfe_project_anicache_dir_label = SimpleLabel("Animation cache directory: ")
        wfe_project_anicache_dir_edit = EditLineWithButtons(" ", text_on_button_1="Get", label_minimum_size=7)
        wfe_project_description_edit = EditLineWithButtons("Description: ", label_minimum_size=80)

        wfe_buttons = ButtonWithCheckBoxes("Save changes", pin_text="pin", cb2_text="Set as default project")

        self.qt_fe_task_name = wfe_project_name_edit.qt_edit_line

        self.qt_fe_proj_dir = wfe_project_dir_edit.qt_edit_line
        wfe_project_dir_edit.button_1.clicked.connect(
            lambda: self.get_dialog_project_directory(wfe_project_dir_edit.qt_edit_line))
        self.qt_fe_working_dir = wfe_project_working_dir_edit.qt_edit_line
        wfe_project_working_dir_edit.button_1.clicked.connect(
            lambda: self.get_dialog_working_directory(wfe_project_working_dir_edit.qt_edit_line))
        self.qt_fe_cam_dir = wfe_project_cam_dir_edit.qt_edit_line
        wfe_project_cam_dir_edit.button_1.clicked.connect(
            lambda: self.get_dialog_cam_directory(wfe_project_cam_dir_edit.qt_edit_line))
        self.qt_fe_anicache_dir = wfe_project_anicache_dir_edit.qt_edit_line
        wfe_project_anicache_dir_edit.button_1.clicked.connect(
            lambda: self.get_dialog_anicache_directory(wfe_project_anicache_dir_edit.qt_edit_line))
        wfe_buttons.button.clicked.connect(
            lambda: self.save_project_changes(wfe_project_name_edit.get_txt(), wfe_project_dir_edit.get_txt(),
                                              wfe_project_working_dir_edit.get_txt(),
                                              wfe_project_cam_dir_edit.get_txt(),
                                              wfe_project_anicache_dir_edit.get_txt(),
                                              wfe_buttons.qt_second_check_box.isChecked(),
                                              wfe_project_description_edit.get_txt(),
                                              wfe_buttons.qt_pin_check_box.isChecked()
                                              ))
        self.qt_fe_description = wfe_project_description_edit.qt_edit_line
        self.qtcb_fe_default_proj = wfe_buttons.qt_second_check_box

        qt_form_edit_layout.addLayout(wfe_project_name_label.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_name_edit.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_dir_label.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_dir_edit.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_working_dir_label.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_working_dir_edit.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_cam_dir_label.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_cam_dir_edit.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_anicache_dir_label.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_anicache_dir_edit.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_project_description_edit.qt_widget_layout)
        qt_form_edit_layout.addLayout(wfe_buttons.qt_widget_layout)

        qt_gb_edit = QGroupBox()
        qt_gb_edit.setLayout(qt_form_edit_layout)
        qt_form_edit_layout_ext.addWidget(qt_gb_edit)

        # REMOVE
        # REMOVE REMOVE
        # REMOVE REMOVE REMOVE
        qt_form_remove = QWidget()
        self.qt_form_remove = qt_form_remove
        qt_form_remove_layout_ext = QVBoxLayout()
        qt_form_remove.setLayout(qt_form_remove_layout_ext)

        qt_form_remove_layout = QFormLayout()

        wfr_buttons = ButtonWithCheckBoxes("Yes, remove", label_text="Remove selected ?")
        wfr_buttons.button.setStyleSheet("""padding-top:7px;padding-bottom:7px;margin-top:10px;margin-bottom:10px""")

        qt_form_remove_layout.addRow(" ", wfr_buttons.qt_widget_layout)

        wfr_buttons.button.clicked.connect(lambda: self.on_click_confirm_remove_project())

        qt_gb_remove = QGroupBox()
        qt_gb_remove.setLayout(qt_form_remove_layout)
        qt_form_remove_layout_ext.addWidget(qt_gb_remove)

        self.comfun.add_wigdets(qt_lay_projects_forms, [qt_form_add, qt_form_edit, qt_form_remove])

        self.hide_all_forms()

        qt_but_add_form = QPushButton("Add Project")
        qt_but_edit_form = QPushButton("Edit Project")
        qt_but_def_project = QPushButton("Set Def Project")
        qt_but_remove_form = QPushButton("Remove Project")

        qt_but_add_form.clicked.connect(self.on_click_add_form)
        qt_but_edit_form.clicked.connect(self.on_click_edit_form)
        qt_but_def_project.clicked.connect(self.on_click_set_def)
        qt_but_remove_form.clicked.connect(self.on_click_remove_form)

        qt_lay_projects_lists.addWidget(qt_list_projects)

        self.comfun.add_wigdets(qt_lay_projects_buttons,
                                [qt_but_add_form, qt_but_edit_form, qt_but_def_project, qt_but_remove_form])
        self.comfun.add_layouts(qt_project_main_layout,
                                [qt_lay_projects_lists, qt_lay_projects_forms, qt_lay_projects_buttons])
        self.init_projects()

    def init_projects(self):
        projects = self.prj.projects_data
        widget_list = self.qt_list_projects
        qt_list_item = QListWidgetItem(widget_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)

        list_item_widget = ProjectListItem("ID", "proj name", "project dir", "description")

        widget_list.addItem(qt_list_item)
        widget_list.setItemWidget(qt_list_item, list_item_widget)
        qt_list_item.setSizeHint(QSize(1, 24))

        if self.sts.ui_brightness_mode == 0:
            qt_list_item.setBackground(self.sts.state_colors[0])
        else:
            qt_list_item.setBackground(self.sts.state_colors_up[0])

        for ip in range(self.prj.total_projects):
            qt_list_item = QListWidgetItem(widget_list)
            if projects[ip].is_default == 1:
                color_index = self.sts.INDEX_STATE_DEFAULT
            else:
                color_index = projects[ip].state_id

            curr_color = self.sts.state_colors[color_index].color()
            qt_list_item.setBackground(curr_color)
            list_item_widget = ProjectListItem(str(projects[ip].id), projects[ip].project_name,
                                               projects[ip].project_directory, projects[ip].description)

            widget_list.addItem(qt_list_item)
            widget_list.setItemWidget(qt_list_item, list_item_widget)
            qt_list_item.setSizeHint(QSize(130, 26))

    def clear_list(self):
        while self.qt_list_projects.count() > 0:
            self.qt_list_projects.takeItem(0)

    def reset_list(self, set_active_id=None):
        self.freeze_list_on_changed = 1
        index = self.batch.prj.current_project_index
        self.clear_list()
        self.init_projects()
        if set_active_id is None:
            if index > self.prj.total_projects - 1:
                index = self.prj.total_projects - 1
            self.prj.current_project_index = index
            self.prj.update_current_from_index(index)
        else:
            self.prj.update_current_from_id(set_active_id)
        self.freeze_list_on_changed = 0

    def reload_projects_data_and_refresh_list(self):
        curr_p_id = self.batch.prj.current_project_id
        self.batch.prj.clear_all_projects_data()
        self.batch.prj.load_projects()
        self.batch.prj.update_current_from_id(curr_p_id)
        self.reset_list()

    def set_as_default(self):
        self.prj.set_proj_as_default(index=self.batch.prj.current_project_index)
        self.prj.save_projects()
        self.reset_list()

    def on_menu_set_as_def(self):
        self.set_as_default()

    def _change_current_project_state_and_reset_list(self, state_id):
        self.batch.prj.current_project.state = self.sts.states_visible_names[state_id]
        self.batch.prj.current_project.state_id = state_id
        self.batch.prj.save_projects()
        self.reset_list()

    def on_menu_set_active(self):
        self._change_current_project_state_and_reset_list(self.sts.INDEX_STATE_ACTIVE)

    def on_menu_set_suspended(self):
        self._change_current_project_state_and_reset_list(self.sts.INDEX_STATE_SUSPEND)

    def on_right_click_show_menu(self, pos):
        global_pos = self.qt_list_projects.mapToGlobal(pos)
        qt_menu_right = QMenu()
        qt_menu_right.addAction("Set As Default Project", self.on_menu_set_as_def)
        qt_menu_right.addAction("Set ACTIVE", self.on_menu_set_active)
        qt_menu_right.addAction("Set SUSPEND", self.on_menu_set_suspended)
        qt_menu_right.exec_(global_pos)

    def hide_all_forms(self):
        self.qt_form_add.hide()
        self.qt_form_edit.hide()
        self.qt_form_remove.hide()

        self.add_form_state = 0
        self.edit_form_state = 0
        self.remove_form_state = 0

    def fa_get_project_directory(self, qt_edit_line):
        force_start_dir = ""
        if self.batch.prj.current_project_index >= 0:
            force_start_dir = self.batch.prj.projects_data[self.batch.prj.current_project_index].project_directory

        ret = self.comfun.get_dialog_directory(qt_edit_line, QFileDialog, force_start_dir)
        if len(ret) > 0:
            self.comfun.if_empty_put_text(self.wfa_working_dir_edit.qt_edit_line, ret + "FX\\")  # TODO user cfg FX
            self.comfun.if_empty_put_text(self.wfa_cam_dir_edit.qt_edit_line, ret + "cam\\")     # TODO user cfg cam
            self.comfun.if_empty_put_text(self.wfa_ani_dir_edit.qt_edit_line, ret + "ani\\")     # TODO user cfg ani
            self.comfun.if_empty_put_text(self.wfa_ani_dir_edit.qt_edit_line, ret + "env\\")     # TODO user cfg ani

    def fa_get_working_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    def fa_get_cam_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    def fa_get_cache_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    def get_dialog_project_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    def get_dialog_working_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    def get_dialog_cam_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    def get_dialog_anicache_directory(self, qt_edit_line):
        return self.comfun.get_dialog_directory(qt_edit_line, QFileDialog)

    #  Add
    #  Add  Add
    #  Add  Add  Add
    def clear_form_add(self):
        self.wfa_project_name_edit.qt_edit_line.setText("")
        self.wfa_project_dir_edit.qt_edit_line.setText("")
        self.wfa_working_dir_edit.qt_edit_line.setText("")
        self.wfa_cam_dir_edit.qt_edit_line.setText("")
        self.wfa_ani_dir_edit.qt_edit_line.setText("")
        self.wfa_descr_edit.qt_edit_line.setText("")

    def on_click_add_form(self):
        if self.add_form_state == 0:
            self.hide_all_forms()
            self.qt_form_add.show()
            self.add_form_state = 1
        else:
            self.qt_form_add.hide()
            self.add_form_state = 0

    def on_click_add_project(self, new_project_name, project_directory, working_directory, cameras_directory,
                             cache_directory, description, pin_checked):
        if len(new_project_name) > 0:
            cb_state = False   # TODO  get cb_state
            if cb_state:
                set_default = 1
            else:
                set_default = 0
            working_directory = self.batch.comfun.get_proper_path(working_directory)
            cameras_directory = self.batch.comfun.get_proper_path(cameras_directory)
            cache_directory = self.batch.comfun.get_proper_path(cache_directory)

            if self.batch.prj.total_projects == 0:
                set_default = 1

            new_project = SingleProject(0, new_project_name, set_default, self.sts.INDEX_STATE_ACTIVE, "ACTIVE",
                                        project_directory, working_directory, cameras_directory, cache_directory,
                                        "", "", "", "", "generate_directory_patterns=True", description)

            ret_id = self.batch.prj.add_project(new_project, do_save=True, generate_directory_patterns=True)

            self.batch.prj.current_project_id = ret_id

            list_item = QListWidgetItem(self.qt_list_projects)
            list_item_widget = ProjectListItem(str(new_project.id), new_project_name, working_directory, description)
            self.qt_list_projects.addItem(list_item)
            self.qt_list_projects.setItemWidget(list_item, list_item_widget)
            self.batch.sio.create_project_working_directory(new_project.working_directory_absolute)

            if pin_checked is False:
                self.clear_form_add()
                self.qt_form_add.hide()
                self.add_form_state = 0

            self.reset_list(set_active_id=self.batch.prj.current_project_id)
            self.mainw.sch_ui.hide_all_forms()
        else:
            self.top_ui.set_top_info(" Fill project name !", 8)

    #  Edit
    #  Edit  Edit
    #  Edit  Edit  Edit
    def on_click_edit_form(self):
        if self.edit_form_state == 0:
            self.hide_all_forms()
            self.qt_form_edit.show()
            self.on_click_form_edit_fill()
            self.edit_form_state = 1
        else:
            self.qt_form_edit.hide()
            self.edit_form_state = 0

    def save_project_changes(self, new_project_name, project_directory, working_directory, cameras_directory,
                             cache_directory, cb_state, description, pin_checked):
        if len(new_project_name) > 0:
            if cb_state:
                set_active = 1
            else:
                set_active = 0

            # using 'SingleProject' object only fof transfer data
            mock_project = SingleProject(0, new_project_name, set_active, 1, "MOCK", project_directory,
                                         working_directory, cameras_directory, cache_directory, "", "", "", "",
                                         "MOCK", description)
            self.batch.prj.update_project(mock_project, do_save=True)

            if pin_checked is False:
                self.qt_form_edit.hide()
                self.edit_form_state = 0

            self.reset_list()   # TODO update single item list
        else:
            self.top_ui.set_top_info(" Fill project name !", 8)

    #  Def
    #  Def  Def
    #  Def  Def  Def
    def on_click_set_def(self):
        self.set_as_default()

    def on_click_form_edit_fill(self):
        if self.batch.prj.current_project_index >= 0:
            curr_proj = self.batch.prj.projects_data[self.batch.prj.current_project_index]
            self.qt_fe_task_name.setText(curr_proj.project_name)
            self.qt_fe_proj_dir.setText(curr_proj.project_directory)
            self.qt_fe_working_dir.setText(curr_proj.working_directory)
            self.qt_fe_cam_dir.setText(curr_proj.cameras_directory)
            self.qt_fe_anicache_dir.setText(curr_proj.cache_directory)
            self.qt_fe_description.setText(curr_proj.description)

            if curr_proj.is_default == 1:
                self.qtcb_fe_default_proj.setChecked(True)
            else:
                self.qtcb_fe_default_proj.setChecked(False)

    #  Remove
    #  Remove  Remove
    #  Remove  Remove  Remove
    def on_click_remove_form(self):
        if self.remove_form_state == 0:
            self.hide_all_forms()
            self.qt_form_remove.show()
            self.remove_form_state = 1
        else:
            self.qt_form_remove.hide()
            self.remove_form_state = 0

    def on_click_confirm_remove_project(self):                  # TODO remove schemas and task after poj delete !
        if self.batch.prj.current_project_index is not None:
            remove_index = self.batch.prj.current_project_index
            self.batch.prj.current_project_index = None
            self.last_project_index = None
            self.batch.prj.remove_single_project(index=remove_index, do_save=True)
            self.qt_list_projects.takeItem(remove_index + 1)
            self.qt_form_remove.hide()
            self.remove_form_state = 0

    def update_sch_after_proj_changed(self):
        self.mainw.sch_ui.current_of_visible_schema_index = None
        self.mainw.sch_ui.last_schema_list_index = None
        self.mainw.sch_ui.reset_list()
        self.batch.sch.update_current_from_index(None)

    def update_tsk_after_proj_changed(self):
        self.batch.tsk.currentTaskID = None
        self.batch.tsk.currentTaskIndex = None
        self.batch.tsk.currentTaskListIndex = None
        tsk_ui = self.mainw.tsk_ui
        tsk_ui.qt_form_create.update_schema_names_combo(combo_current_index=0)
        tsk_ui.qt_form_edit.update_schema_names_combo(combo_current_index=0)
        tsk_ui.update_all_tasks()
        tsk_ui.update_list_of_visible_ids()

    def on_list_current_changed(self, currentRow):
        if self.freeze_list_on_changed == 1:
            self.batch.logger.deepdb(("proj chngd freeze_list_on_changed", self.qt_list_projects.currentRow()))
        else:
            self.batch.logger.inf(("listProjectsCurrentChanged", self.qt_list_projects.currentRow()))

            self.last_project_index = self.batch.prj.current_project_index
            current_list_index = self.qt_list_projects.currentRow() - 1
            self.batch.prj.current_project_index = current_list_index
            self.batch.prj.update_current_from_index(current_list_index)

            # update color of last item list
            if self.last_project_index >= 0:
                last_item = self.qt_list_projects.item(self.last_project_index+1)
                last_proj_state_id = self.batch.prj.projects_data[self.last_project_index].state_id
                last_proj_def = self.batch.prj.projects_data[self.last_project_index].is_default
                if last_proj_def == 1:
                    color_index = self.sts.INDEX_STATE_DEFAULT
                else:
                    color_index = last_proj_state_id
                if last_item is not None:
                    last_item.setBackground(self.batch.sts.state_colors[color_index].color())

            # update top info and color of current item list
            cur_proj = None
            if 0 <= current_list_index < len(self.batch.prj.projects_data):
                cur_proj = self.batch.prj.projects_data[current_list_index]
                if cur_proj.is_default == 1:
                    color_index = self.sts.INDEX_STATE_DEFAULT
                else:
                    color_index = cur_proj.state_id
                item_c = self.qt_list_projects.item(current_list_index + 1)
                cur_color = self.batch.sts.state_colors_up[color_index].color()
                item_c.setBackground(cur_color)
                if self.top_ui is not None:
                    self.top_ui.set_top_info("Current project:   " + cur_proj.project_name)
            else:
                self.batch.logger.wrn(("(on chng) Wrong current_list_index: ", current_list_index))

            self.update_sch_after_proj_changed()
            self.update_tsk_after_proj_changed()

            # update form edit project
            if self.edit_form_state == 1 and cur_proj is not None:
                self.qt_fe_task_name.setText(cur_proj.project_name)
                self.qt_fe_proj_dir.setText(cur_proj.project_directory)
                self.qt_fe_working_dir.setText(cur_proj.working_directory)
                self.qt_fe_cam_dir.setText(cur_proj.cameras_directory)
                self.qt_fe_anicache_dir.setText(cur_proj.cache_directory)
                self.qt_fe_description.setText(cur_proj.description)
                self.qtcb_fe_default_proj.setChecked(cur_proj.is_default)
