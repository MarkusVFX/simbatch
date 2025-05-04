import os

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    raise Exception('PySide import ERROR!  Please install PySide or PySide2')

from .widgets import *


class NodeListItem(QWidget):
    def __init__(self, txt_id, txt_node, txt_state, txt_description):
        super(NodeListItem, self).__init__()
        self.widget = QWidget(self)
        self.qt_label_font = QFont()
        self.qt_label_font.setPointSize(8)

        self.qt_lay = QHBoxLayout(self.widget)
        self.qt_lay.setSpacing(0)
        self.qt_lay.setContentsMargins(0, 0, 0, 0)

        self.qt_label_id = QLabel(txt_id)
        self.qt_label_id.setFont(self.qt_label_font)
        self.qt_label_id.setStyleSheet("""color:#000;""")
        self.qt_label_id.setMinimumWidth(22)
        self.qt_label_id.setMaximumWidth(22)
        self.qt_lay.addWidget(self.qt_label_id)

        self.qt_label_node = QLabel(txt_node)
        self.qt_label_node.setStyleSheet("""padding-left:4px;""")
        self.qt_label_node.setFont(self.qt_label_font)
        self.qt_label_node.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_node)
        self.qt_label_state = QLabel(txt_state)
        self.qt_label_state.setFont(self.qt_label_font)
        self.qt_label_state.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_state)
        self.qt_label_description = QLabel(txt_description)
        self.qt_label_description.setFont(self.qt_label_font)
        self.qt_label_description.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_description)

        self.setLayout(self.qt_lay)


class NodesUI:
    qt_list_nodes = None
    widgetNodes = None
    qt_widget_nodes = None

    batch = None
    top_ui = None

    sts = None
    nod = None
    comfun = None

    add_node_form_state = 0
    edit_node_form_state = 0
    remove_node_form_state = 0

    qt_form_add_node = None
    qt_form_add_node_el_path = None
    qt_form_add_node_el_name = None
    qt_form_edit_node = None
    qt_form_edit_node_el_path = None
    qt_form_edit_node_el_name = None
    qt_form_edit_node_el_desc = None
    qt_form_remove_node = None

    freeze_list_on_changed = 0
    # last_node_list_index = None   # used for list item color change to unselected
    current_list_item_index = None
    last_list_item_index = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.debug_level = batch.sts.debug_level
        self.top_ui = top
        self.mainw = mainw
        self.server = mainw.server

        self.nod = batch.nod   # TODO
        self.sts = batch.sts   # TODO

        # init GUI
        qt_list_nodes = QListWidget()
        qt_list_nodes.setSelectionMode(QAbstractItemView.NoSelection)
        qt_list_nodes.setFrameShadow(QFrame.Raised)
        qt_list_nodes.currentItemChanged.connect(self.on_list_nodes_current_changed)
        qt_list_nodes.setSpacing(1)
        p = qt_list_nodes.sizePolicy()
        p.setVerticalPolicy(QSizePolicy.Policy.Maximum)

        qt_list_nodes.setContextMenuPolicy(Qt.CustomContextMenu)
        qt_list_nodes.customContextMenuRequested.connect(self.show_right_click_menu)

        self.qt_list_nodes = qt_list_nodes

        qt_widget_nodes = QWidget()
        self.qt_widget_nodes = qt_widget_nodes
        qt_lay_nodes_main = QVBoxLayout(qt_widget_nodes)
        qt_lay_nodes_main.setContentsMargins(0, 0, 0, 0)

        qt_lay_nodes_list = QHBoxLayout()
        qt_lay_nodes_forms = QVBoxLayout()
        qt_lay_nodes_buttons = QHBoxLayout()

        qt_b_add_node = QPushButton("Add")
        qt_b_edit_node = QPushButton("Edit")
        qt_b_reset_node = QPushButton("Reset")
        qt_b_remove_node = QPushButton("Remove")
        qt_b_update_nodes = QPushButton("Reload")

        qt_lay_nodes_list.addWidget(qt_list_nodes)
        qt_lay_nodes_buttons.addWidget(qt_b_add_node)
        qt_lay_nodes_buttons.addWidget(qt_b_edit_node)
        qt_lay_nodes_buttons.addWidget(qt_b_reset_node)
        qt_lay_nodes_buttons.addWidget(qt_b_remove_node)
        qt_lay_nodes_buttons.addWidget(qt_b_update_nodes)

        qt_b_add_node.clicked.connect(self.on_click_show_add_node_form)
        qt_b_edit_node.clicked.connect(self.on_click_show_edit_node_form)
        qt_b_reset_node.clicked.connect(self.on_reset_node)
        qt_b_remove_node.clicked.connect(self.on_click_show_remove_node_form)
        qt_b_update_nodes.clicked.connect(self.on_update_nodes)

        # ADD
        # ADD ADD
        # ADD ADD ADD
        qt_form_add_node = QWidget()
        self.qt_form_add_node = qt_form_add_node
        qt_form_add_node_layout_ext = QVBoxLayout()
        qt_form_add_node.setLayout(qt_form_add_node_layout_ext)

        qt_form_add_node_layout = QFormLayout()

        wfa_path = EditLineWithButtons("Path: ", text_on_button_1="Get dir",  text_on_button_2="Check")
        wfa_path.button_1.clicked.connect(self.on_click_path_get)
        wfa_path.button_2.clicked.connect(self.on_click_path_check)
        # wfa_path.qt_edit_line.textChanged.connect(self.on_changed_add_node)
        self.qt_form_add_node_el_path = wfa_path.qt_edit_line

        wfa_name = EditLineWithButtons("Name: ", text_on_button_1="Get from path")
        wfa_name.button_1.clicked.connect(self.on_click_name_from_path)
        wfa_name.button_1.setToolTip("Get current name from server file status.txt")  # TODO Consistent naming in database and server status file 
        self.qt_form_add_node_el_name = wfa_name.qt_edit_line

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        
        # Full init server button
        wfr_button_full_init = ButtonWithCheckBoxes("Full init server", button_width=155, label_text=" ")
        wfr_button_full_init.button.setToolTip("Complete server initialization: creates directory if needed, adds to database, copies source files and config.ini, creates state.txt")
        wfr_button_full_init.button.clicked.connect(self.on_click_full_init_server)    #mmm
        
        wfr_button_src = ButtonWithCheckBoxes("Copy/Update source files", button_width=155, label_text=" ")
        # wfr_button_src.button.setEnabled(False)
        wfr_button_src.button.clicked.connect(self.on_click_copy_src)
        wfr_button_add = ButtonWithCheckBoxes("Add Path To Database", button_width=155, label_text=" ")
        wfr_button_add.button.clicked.connect(self.on_click_add_node)
        
        wfr_button_config = ButtonWithCheckBoxes("Copy config.ini", button_width=155, label_text=" ")
        wfr_button_config.button.clicked.connect(self.on_click_copy_config)

        qt_form_add_node_layout.addRow(" ", QLabel("   "))
        qt_form_add_node_layout.addRow(" ", wfa_path.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", wfa_name.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", separator)
        qt_form_add_node_layout.addRow(" ", wfr_button_full_init.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", separator)
        qt_form_add_node_layout.addRow(" ", wfr_button_add.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", wfr_button_src.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", wfr_button_config.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", QLabel("   "))

        qt_gb_add_node = QGroupBox()
        qt_gb_add_node.setLayout(qt_form_add_node_layout)
        qt_form_add_node_layout_ext.addWidget(qt_gb_add_node)
        qt_gb_add_node.setTitle("Add Sim Node")


        # EDIT
        # EDIT EDIT
        # EDIT EDIT EDIT
        qt_form_edit_node = QWidget()
        self.qt_form_edit_node = qt_form_edit_node
        qt_form_edit_node_layout_ext = QVBoxLayout()
        qt_form_edit_node.setLayout(qt_form_edit_node_layout_ext)

        qt_form_edit_node_layout = QFormLayout()

        wfe_path = EditLineWithButtons("Path: ", text_on_button_1="Get dir", text_on_button_2="Check")
        wfe_path.button_1.clicked.connect(self.on_click_edit_path_get)
        wfe_path.button_2.clicked.connect(self.on_click_edit_path_check)
        self.qt_form_edit_node_el_path = wfe_path.qt_edit_line

        wfe_name = EditLineWithButtons("Name: ", text_on_button_1="Get from server")
        wfe_name.button_1.setToolTip("Get current name from server file status.txt")  # TODO Consistent naming in database and server status file 
        wfe_name.button_1.clicked.connect(self.on_click_get_name_from_server)
        self.qt_form_edit_node_el_name = wfe_name.qt_edit_line

        wfe_desc = EditLineWithButtons("Description: ", text_on_button_1="Get date")
        wfe_desc.button_1.clicked.connect(self.on_click_edit_desc_date)
        self.qt_form_edit_node_el_desc = wfe_desc.qt_edit_line

        wfe_button_update = ButtonWithCheckBoxes("Update Node", button_width=155, label_text=" ")
        wfe_button_update.button.clicked.connect(self.on_click_update_node)
        
        wfe_button_src = ButtonWithCheckBoxes("Copy/Update source files", button_width=155, label_text=" ")
        wfe_button_src.button.clicked.connect(self.on_click_update_src)
        
        wfe_button_config = ButtonWithCheckBoxes("Update server's config.ini", button_width=155, label_text=" ")
        wfe_button_config.button.clicked.connect(self.on_click_update_server_config)

        qt_form_edit_node_layout.addRow(" ", QLabel("   "))
        qt_form_edit_node_layout.addRow(" ", wfe_path.qt_widget_layout)
        qt_form_edit_node_layout.addRow(" ", wfe_name.qt_widget_layout)
        qt_form_edit_node_layout.addRow(" ", wfe_desc.qt_widget_layout)
        qt_form_edit_node_layout.addRow(" ", wfe_button_update.qt_widget_layout)
        qt_form_edit_node_layout.addRow(" ", wfe_button_src.qt_widget_layout)
        qt_form_edit_node_layout.addRow(" ", wfe_button_config.qt_widget_layout)
        qt_form_edit_node_layout.addRow(" ", QLabel("   "))

        qt_gb_edit_node = QGroupBox()
        qt_gb_edit_node.setLayout(qt_form_edit_node_layout)
        qt_form_edit_node_layout_ext.addWidget(qt_gb_edit_node)
        qt_gb_edit_node.setTitle("Edit Sim Node")


        # REMOVE
        # REMOVE REMOVE
        # REMOVE REMOVE REMOVE
        qt_form_remove_node = QWidget()
        self.qt_form_remove_node = qt_form_remove_node
        qt_form_remove_node_layout_ext = QVBoxLayout()
        qt_form_remove_node.setLayout(qt_form_remove_node_layout_ext)

        qt_form_remove_node_layout = QFormLayout()

        wfr_buttons = ButtonWithCheckBoxes("Yes, remove", label_text="Remove selected ?        ")
        wfr_buttons.button.clicked.connect(self.on_click_confirmed_remove_node)

        qt_form_remove_node_layout.addRow(" ", QLabel("   "))
        qt_form_remove_node_layout.addRow(" ", wfr_buttons.qt_widget_layout)
        qt_form_remove_node_layout.addRow(" ", QLabel("   "))

        qt_gb_remove_node = QGroupBox()
        qt_gb_remove_node.setLayout(qt_form_remove_node_layout)
        qt_form_remove_node_layout_ext.addWidget(qt_gb_remove_node)
        qt_gb_remove_node.setTitle("Remove Sim Node")


        # TAB LAY
        # TAB LAY LAY
        # TAB LAY LAY LAY

        self.hide_all_forms()

        self.comfun.add_widgets(qt_lay_nodes_forms, [qt_form_add_node, qt_form_edit_node, qt_form_remove_node])

        self.comfun.add_layouts(qt_lay_nodes_main, [qt_lay_nodes_list, qt_lay_nodes_forms, qt_lay_nodes_buttons])

        self.init_nodes()

    def init_nodes(self):
        widget_list = self.qt_list_nodes
        qt_list_item = QListWidgetItem(widget_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)

        list_item_widget = NodeListItem("ID", "name",  "state", "descr")

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

        for nod in self.batch.nod.nodes_data:
            qt_list_item = QListWidgetItem(widget_list)
            cur_color = self.sts.state_colors[nod.state_id].color()
            qt_list_item.setBackground(cur_color)
            list_item_widget = NodeListItem(str(nod.id), nod.node_name, nod.state, nod.description)

            if self.sts.runtime_env == "Houdini":
                color = self.batch.sts.state_colors_rgb_str[nod.state_id]
                list_item_widget.setStyleSheet("background-color: rgb(" + color + ");")       # uicolor

            widget_list.addItem(qt_list_item)
            widget_list.setItemWidget(qt_list_item, list_item_widget)
            qt_list_item.setSizeHint(QSize(130, 26))
            qt_list_item.setBackground(self.sts.state_colors[nod.state_id])

    def reload_simnodes_data_and_refresh_list(self):
        self.batch.nod.clear_all_nodes_data()
        self.batch.nod.load_nodes()
        self.reset_list()

    def reset_list(self):
        self.freeze_list_on_changed = 1
        # index = self.batch.tsk.current_task_index
        self.clear_list(with_freeze=False)
        self.init_nodes()
        # self.batch.tsk.update_current_from_index(index)
        self.freeze_list_on_changed = 0

    def set_state_in_node_state_file(self, state_id):
        """  set state in config file  """
        cur_nod = self.batch.nod.current_node
        return self.batch.nod.create_node_state_file(cur_nod.state_file, cur_nod.node_name, state_id, update_mode=True)

    def set_state_in_database(self, state_id):
        """  set state in database  """
        cur_nod = self.batch.nod.current_node
        cur_nod.state = self.sts.states_visible_names[state_id]
        cur_nod.state_id = state_id
        self.batch.nod.save_nodes()

    def set_state(self, state_id):
        if self.batch.nod.current_node is not None:
            ret = self.set_state_in_node_state_file(state_id)
            if ret:
                self.set_state_in_database(state_id)
                self.reset_list()
                self.top_ui.set_top_info(" State updated ", 1)
            else:
                if self.batch.comfun.file_exists(self.batch.nod.current_node.state_file):
                    self.batch.logger.err("Simode state file NOT updated!")
                    self.top_ui.set_top_info(" State NOT updated !", 8)
                else:
                    self.batch.logger.err("Simnode state file NOT updated! File not exist!")
                    self.top_ui.set_top_info(" State NOT updated ! Simnode state file not exist!", 8)
        else:
            self.batch.logger.wrn("Current node is None!")
        
    def on_menu_set_waiting(self):
        self.set_state(self.batch.sts.INDEX_STATE_WAITING)
        
    def on_menu_set_working(self):
        self.set_state(self.batch.sts.INDEX_STATE_WORKING)
        
    def on_menu_set_offline(self):
        self.set_state(self.batch.sts.INDEX_STATE_OFFLINE)

    def on_menu_remove(self):
        self.on_click_confirmed_remove_node()

    def on_menu_print_log(self):
        self.nod.print_node_log()

    def on_menu_print_executor_log(self):
        self.nod.print_node_executor_log()

    def on_menu_reset(self):
        self.batch.logger.db("on menu: Reset")
        self.on_reset_node()

    def on_menu_break(self):
        file = self.comfun.get_path_from_full(self.nod.get_state_file()) + "break.txt"
        if self.comfun.file_exists(file, info=False):
            self.batch.logger.wrn(("Break file exist: ", file))
        else:
            info = "If this file name is break.txt, it will break main server's loop. It's nice way to stop server"
            info += "\nIf this file is named break__.txt it means loop was successful broken and break.txt was renamed"
            ret = self.comfun.save_to_file(file, info)
            if ret:
                self.batch.logger.inf(("Break file created: ", file))
            else:
                self.batch.logger.err(("Break file NOT created: ", file))

    @staticmethod
    def on_click_menu_spacer():
        pass

    def show_right_click_menu(self, pos):
        global_pos = self.qt_list_nodes.mapToGlobal(pos)
        qt_right_menu = QMenu()
        qt_right_menu.addAction("Reset Node", self.on_menu_reset)
        qt_right_menu.addAction("Set WAITING", self.on_menu_set_waiting)
        qt_right_menu.addAction("Set WORKING", self.on_menu_set_working)
        qt_right_menu.addAction("Set OFFLINE", self.on_menu_set_offline)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Print Node Log", self.on_menu_print_log)
        qt_right_menu.addAction("Print Node Exec Log", self.on_menu_print_executor_log)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Remove Node", self.on_menu_remove)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Break server's main loop", self.on_menu_break)

        qt_right_menu.exec_(global_pos)

    def clear_list(self, with_freeze=False):  # TODO with freeze
        while self.qt_list_nodes.count() > 0:
            self.qt_list_nodes.takeItem(0)

    def hide_all_forms(self):
        if hasattr(self, 'qt_form_add_node') and self.qt_form_add_node is not None:
            self.qt_form_add_node.hide()
            self.add_node_form_state = 0
        if hasattr(self, 'qt_form_edit_node') and self.qt_form_edit_node is not None:
            self.qt_form_edit_node.hide()
            self.edit_node_form_state = 0
        if hasattr(self, 'qt_form_remove_node') and self.qt_form_remove_node is not None:
            self.qt_form_remove_node.hide()
            self.remove_node_form_state = 0

    def on_click_show_add_node_form(self):
        if self.add_node_form_state == 0:
            self.hide_all_forms()
            self.qt_form_add_node.show()
            self.add_node_form_state = 1
        else:
            self.qt_form_add_node.hide()
            self.add_node_form_state = 0

    def on_click_name_from_path(self):     # mmm
        dir = self.qt_form_add_node_el_path.text()

        dir_name = os.path.basename(os.path.normpath(dir))
        self.qt_form_add_node_el_name.setText(dir_name)
        self.top_ui.set_top_info("Directory name: " + dir_name, 4)

    def on_click_path_get(self):
        # self.batch.comfun.file_dialog_to_edit_line(self.qt_form_add_node_el_path, QFileDialog, "")
        self.batch.comfun.get_dialog_directory(self.qt_form_add_node_el_path, QFileDialog, dir_separator=os.sep)

    def on_click_path_check(self):
        dir = self.qt_form_add_node_el_path.text()
        file = "state.txt"   # TODO  move filename defininition to setttings  or add custom
        
        if not dir.endswith(os.sep):
            dir = dir + os.sep
            
        if self.batch.comfun.path_exists(dir):
            if self.batch.comfun.file_exists(dir+file):
                self.top_ui.set_top_info("Directory exist, state file exist ", 4)
            else:
                self.top_ui.set_top_info("Directory exist, state file not exist ", 4)
        else:
            self.top_ui.set_top_info("Directory not exist ", 7)

    def on_click_copy_src(self): # 'Add' form
        dest = self.qt_form_add_node_el_path.text()   # 'Add' form path
        self.server.update_sources_from_master(force_destination=dest)

    def on_click_update_src(self): # 'Edit' form
        dest = self.qt_form_edit_node_el_path.text()  # 'Edit' form path    
        self.server.update_sources_from_master(force_destination=dest)

    def on_click_add_node(self): #mmm
        desc = self.batch.comfun.get_current_time()
        node_dir = self.qt_form_add_node_el_path.text()
        self.batch.logger.db(f"on_click_add_node: {node_dir}")

        if len(node_dir) > 0:
            if not node_dir.endswith(os.sep):
                node_dir = node_dir + os.sep
                
            if self.batch.comfun.path_exists(node_dir):
                node_name = self.qt_form_add_node_el_name.text()
                if len(node_name) > 0:
                    state_file = node_dir + "state.txt"   # TODO  move to setttings  or add custom
                    node_state_id = self.batch.sts.INDEX_STATE_INIT
                    if self.batch.comfun.file_exists(state_file, info=False):
                        ret = self.batch.nod.get_node_state(state_file)
                        if ret > 0:
                            node_state_id = ret
                        self.batch.nod.create_node_state_file(state_file, node_name, node_state_id, update_mode=True)
                    else:
                        self.batch.nod.create_node_state_file(state_file, node_name, node_state_id)
                        # TODO  server py files !!!
                    node_state = self.batch.sts.states_visible_names[node_state_id]

                    new_node = self.batch.nod.get_new_node(node_name, node_state, node_state_id, state_file, desc)
                    self.batch.nod.reload_nodes()
                    ret = self.batch.nod.add_simnode(new_node, do_save=True)
                    if ret:
                        self.top_ui.set_top_info("Added simnode: {}".format(node_name), 1)
                    else:
                        self.top_ui.set_top_info("Not added simnode! ", 6)
                    self.reset_list()
                else:
                    self.top_ui.set_top_info("Please set sim node name! ", 9)
            else:
                self.top_ui.set_top_info("Directory not exist ", 9)
        else:
            self.top_ui.set_top_info("Please set path first!", 8)

    def on_click_show_edit_node_form(self):
        if self.nod.current_node is None:
            self.batch.logger.wrn("(edit node) PLEASE SELECT NODE FIRST")
            self.top_ui.set_top_info("Select a node to edit first", 7)
            return
            
        if self.edit_node_form_state == 0:
            self.hide_all_forms()
            # Pre-populate form with current node data
            current_node = self.nod.current_node
            self.qt_form_edit_node_el_path.setText(os.path.dirname(current_node.state_file))
            self.qt_form_edit_node_el_name.setText(current_node.node_name)
            self.qt_form_edit_node_el_desc.setText(current_node.description)
            
            self.qt_form_edit_node.show()
            self.edit_node_form_state = 1
        else:
            self.qt_form_edit_node.hide()
            self.edit_node_form_state = 0
    
    def on_click_edit_path_get(self):
        self.batch.comfun.get_dialog_directory(self.qt_form_edit_node_el_path, QFileDialog, dir_separator=os.sep)
    
    def on_click_edit_path_check(self):
        if len(self.qt_form_edit_node_el_path.text()) > 0:
            if self.batch.comfun.path_exists(self.qt_form_edit_node_el_path.text()):
                self.top_ui.set_top_info("Directory exists!", 1)
            else:
                self.top_ui.set_top_info("Directory NOT exists!", 9)
        else:
            self.top_ui.set_top_info("Please set path first!", 8)
            
    def on_click_get_name_from_server(self):     # mmm
        node_dir = self.qt_form_edit_node_el_path.text()
        if len(node_dir) > 0:
            if not node_dir.endswith(os.sep):
                node_dir = node_dir + os.sep
                
            state_file = node_dir + "state.txt"
            if self.batch.comfun.file_exists(state_file):
                server_name = self.batch.nod.get_server_name_from_file(state_file)
                if len(server_name) > 0:
                    self.qt_form_edit_node_el_name.setText(server_name)
                    self.top_ui.set_top_info("Node name loaded from file", 1)
                    self.batch.logger.inf(f"Node name '{server_name}' loaded from file: {state_file}")
                else:
                    self.top_ui.set_top_info("Node name is empty in file", 8)
            else:
                self.top_ui.set_top_info("State file not exists!", 9)
        else:
            self.top_ui.set_top_info("Please set path first!", 8)
            
    def on_click_edit_desc_date(self):
        desc = self.batch.comfun.get_current_time()
        self.qt_form_edit_node_el_desc.setText(desc)
    
    def on_click_update_node(self):
        if self.nod.current_node is None:
            self.batch.logger.wrn("(update node) PLEASE SELECT NODE FIRST")
            self.top_ui.set_top_info("Select a node to update first", 7)
            return
            
        self.batch.logger.db(("update_node", "update"))
        node_dir = self.qt_form_edit_node_el_path.text()
        
        if len(node_dir) > 0:
            if not node_dir.endswith(os.sep):
                node_dir = node_dir + os.sep
                
            if self.batch.comfun.path_exists(node_dir):
                node_name = self.qt_form_edit_node_el_name.text()
                if len(node_name) > 0:
                    state_file = node_dir + "state.txt"
                    desc = self.qt_form_edit_node_el_desc.text()
                    
                    current_node = self.nod.current_node
                    current_node.node_name = node_name
                    current_node.state_file = state_file
                    current_node.description = desc
                    
                    # Update state file if changed
                    if self.batch.comfun.file_exists(state_file):
                        # Only update name in state file, keep state
                        node_state_id = current_node.state_id
                        self.batch.nod.create_node_state_file(state_file, node_name, node_state_id, update_mode=True)
                    else:
                        # Create new state file
                        node_state_id = self.batch.sts.INDEX_STATE_WAITING
                        self.batch.nod.create_node_state_file(state_file, node_name, node_state_id)
                    
                    # Save changes to database
                    if self.batch.nod.save_nodes():
                        self.top_ui.set_top_info(f"Updated simnode: {node_name}", 1)
                        self.reset_list()
                        self.hide_all_forms()
                    else:
                        self.top_ui.set_top_info("Failed to update simnode!", 6)
                else:
                    self.top_ui.set_top_info("Please set sim node name!", 9)
            else:
                self.top_ui.set_top_info("Directory not exist", 9)
        else:
            self.top_ui.set_top_info("Please set path first!", 8)

    def on_click_show_remove_node_form(self):
        if self.remove_node_form_state == 0:
            self.hide_all_forms()
            self.qt_form_remove_node.show()
            self.remove_node_form_state = 1
        else:
            self.qt_form_remove_node.hide()
            self.remove_node_form_state = 0

    def on_click_confirmed_remove_node(self):
        if self.nod.current_node_index is not None and self.nod.current_node_index >= 0:
            current_node = self.nod.nodes_data[self.nod.current_node_index]
            self.batch.logger.db(("remove node:", current_node.id, current_node.node_name))
            self.nod.remove_node(current_node.id, do_save=True)
            self.reset_list()
            self.hide_all_forms()
        else:
            self.batch.logger.wrn("(on remove node) PLEASE SELECT ITEM FIRST")
            self.top_ui.set_top_info(" Select item first ", 7)

    def on_reset_node(self):
        current_node = self.batch.nod.current_node
        if current_node is not None:
            self.batch.nod.reload_nodes()

            default_state_id = self.batch.sts.INDEX_STATE_WAITING

            if self.batch.comfun.file_exists(current_node.state_file) is False:
                self.batch.nod.create_node_state_file(current_node.state_file, current_node.node_name, default_state_id)
                self.top_ui.set_top_info("Simnode state file created", 4)
            else:
                srv_name = current_node.node_name
                self.batch.logger.db(("Set WAITING state to node:", srv_name, default_state_id))
                self.nod.create_node_state_file(current_node.state_file, srv_name, default_state_id, update_mode=True)
                self.top_ui.set_top_info("Simnode state file updated", 4)
            current_node.state_id = default_state_id
            current_node.state = self.batch.sts.states_visible_names[default_state_id]
            self.batch.nod.set_node_state_in_database(self.batch.nod.current_node_index, default_state_id)
            self.batch.nod.save_nodes()
            self.reset_list()
        else:
            self.batch.logger.wrn("(on reset node) PLEASE SELECT ITEM FIRST")
            self.top_ui.set_top_info(" Select item first ", 7)

    def on_update_nodes(self):
        if self.nod.total_nodes == 0:
            self.top_ui.set_top_info("No Simnodes in database! If node exists, please add it first")
            return False
        self.batch.logger.db("on_update_nodes")
        self.nod.clear_all_nodes_data()
        self.nod.load_nodes()

        ret = self.nod.detect_duplicates_by_state_file()
        if ret[0] > 0:
            self.top_ui.set_top_info("Found {} duplicates, please remove it from list. Last id: {}".format(ret[0],
                                                                                                           ret[1]), 7)
            return False

        ret2 = self.nod.update_from_nodes(with_save=True)
        if ret2[1] > 0:
            self.reset_list()
        return True

    def on_list_nodes_current_changed(self, x):  # update_current_from_index
        if self.freeze_list_on_changed == 1:   # freeze update changes on massive action    i.e  clear_list()
            self.batch.logger.deepdb(("simnodes change freeze_list_on_changed", self.qt_list_nodes.currentRow()))
        else:
            self.batch.logger.db(("on_list_current_changed", self.qt_list_nodes.currentRow()))
            self.last_list_item_index = self.current_list_item_index
            current_list_index = self.qt_list_nodes.currentRow() - 1
            self.current_list_item_index = current_list_index

            self.batch.nod.update_current_from_index(current_list_index)

            if self.last_list_item_index is not None:
                if self.last_list_item_index is not None and self.last_list_item_index < len(self.batch.nod.nodes_data):
                    item = self.qt_list_nodes.item(self.last_list_item_index + 1)

                    if item is not None and self.last_list_item_index is not None:
                        color_index = self.batch.nod.nodes_data[self.last_list_item_index].state_id
                        item.setBackground(self.batch.sts.state_colors[color_index].color())
                else:
                    self.batch.logger.wrn("Wrong last_list_item_index {} vs {} ".format(self.last_list_item_index,
                                                                                        len(self.batch.nod.nodes_data)))
            else:
                self.batch.logger.db("last_list_item_index is None")

            # update top info and color of current item list
            if 0 <= current_list_index < len(self.batch.nod.nodes_data):
                cur_node = self.batch.nod.nodes_data[current_list_index]
                color_index = cur_node.state_id
                item_c = self.qt_list_nodes.item(current_list_index + 1)
                cur_color = self.batch.sts.state_colors_up[color_index].color()
                item_c.setBackground(cur_color)
                if self.top_ui is not None:
                    self.top_ui.set_top_info("Current node:   " + str(cur_node.node_name))
                
                # Update edit form if it's visible
                if self.edit_node_form_state == 1 and hasattr(self, 'qt_form_edit_node_el_path'):
                    self.qt_form_edit_node_el_path.setText(os.path.dirname(cur_node.state_file))
                    self.qt_form_edit_node_el_name.setText(cur_node.node_name)
                    self.qt_form_edit_node_el_desc.setText(cur_node.description)
            else:
                self.batch.logger.wrn(("(on change) Wrong current_list_index: ", current_list_index))

    def on_click_update_server_config(self):
        """
        Update the server's config.ini with absolute paths
        1) Get current json data from current SimBatch config.ini
        2) Change paths to absolute paths
        3) Add master_source setting
        4) Save as config.ini in server directory
        """
        if self.nod.current_node is None:
            self.batch.logger.wrn("(update server config) PLEASE SELECT NODE FIRST")
            self.top_ui.set_top_info("Select a node to update config first", 7)
            return
            
        # Get server directory from current node's state file
        current_node = self.nod.current_node
        server_dir = os.path.dirname(current_node.state_file)
        
        # Use the common helper function to create/update config.ini
        self.create_or_update_config(server_dir, "Server config updated")

    def on_click_copy_config(self):
        """
        Copy the config.ini file to the server directory
        1) Get current json data from current SimBatch config.ini
        2) Change paths to absolute paths
        3) Add master_source setting
        4) Save as config.ini in server directory
        """
        # Get server directory from the path input field
        server_dir = self.qt_form_add_node_el_path.text()
        
        # Use the common helper function to create/update config.ini
        self.create_or_update_config(server_dir, "Config copied")
        
    def create_or_update_config(self, server_dir, success_msg_prefix="Config updated"):
        """
        Common helper function to create or update config.ini in the specified directory
        
        Args:
            server_dir (str): The server directory where config.ini should be created/updated
            success_msg_prefix (str): Prefix for success message (e.g. "Config copied" or "Server config updated")
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not server_dir or not os.path.exists(server_dir):
            self.top_ui.set_top_info("Invalid server directory path", 8)
            return False
            
        # Get current config
        current_config = None
        try:
            # Try to load config from settings
            current_config = self.batch.sts.get_settings_as_json()
            if not current_config:
                self.top_ui.set_top_info("Could not get current settings", 8)
                return False
                
            # Update paths to absolute paths
            if "storeData" in current_config:
                if "dataDirectory" in current_config["storeData"]:
                    current_config["storeData"]["dataDirectory"] = self.ensure_absolute_path(current_config["storeData"]["dataDirectory"])
                    
                if "backupDirectory" in current_config["storeData"]:
                    current_config["storeData"]["backupDirectory"] = self.ensure_absolute_path(current_config["storeData"]["backupDirectory"])
                    
                if "definitionsDirectory" in current_config["storeData"]:
                    current_config["storeData"]["definitionsDirectory"] = self.ensure_absolute_path(current_config["storeData"]["definitionsDirectory"])
                
            # Add master_source path if it doesn't exist
            if "simnodes" not in current_config:
                current_config["simnodes"] = {}
                
            # Set master_source to current installation directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            current_config["simnodes"]["master_source"] = current_dir
            
            # Save config to server directory
            config_path = os.path.join(server_dir, "config.ini")
            import json
            with open(config_path, 'w') as f:
                json.dump(current_config, f, indent=4)
                
            success_message = f"{success_msg_prefix} at: {config_path}"
            self.top_ui.set_top_info(success_message, 1)
            self.batch.logger.inf(success_message)
            return True
            
        except Exception as e:
            error_message = f"Error updating config: {str(e)}"
            self.top_ui.set_top_info(error_message, 8)
            self.batch.logger.err(error_message)
            return False

    def ensure_absolute_path(self, path):
        """Convert relative path to absolute path if needed"""
        if not path or len(path) == 0:
            return ""
            
        if os.path.isabs(path):
            return path
            
        # If path is just a directory name or relative path
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(current_dir, path)

    def on_click_full_init_server(self):
        """
        Full server initialization:
        1) Check path in Path field (must be not empty and absolute path)
        2) Create directory if it doesn't exist
        3) Execute Add Path To Database
        4) Execute Copy/Update source files
        5) Execute copy config.ini
        6) Create state.txt file with INDEX_STATE_INIT and name from Name field
        """
                
        # 0) Check node name
        node_name = self.qt_form_add_node_el_name.text()
        if not node_name:
            self.top_ui.set_top_info("Name field is empty", 8)
            return False

        if self.batch.sts.master_directory_abs is None:
            self.batch.sts.master_directory_abs =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   #mmm
            self.batch.sts.save_settings()
            self.batch.logger.inf(f"new valuse saved to settings: master_directory_abs: {self.batch.sts.master_directory_abs }")

        # 1) Check path
        node_dir = self.qt_form_add_node_el_path.text()
        if not node_dir:
            self.top_ui.set_top_info("Path field is empty", 8)
            return False
            
        if not self.comfun.is_absolute(node_dir):
            self.top_ui.set_top_info("Path must be absolute", 8)
            return False
            
        if not node_dir.endswith(os.sep):
            node_dir = node_dir + os.sep
            self.qt_form_add_node_el_path.setText(node_dir)
            
        # 2) Create directory if it doesn't exist
        if not os.path.exists(node_dir):
            try:
                os.makedirs(node_dir)
                self.top_ui.set_top_info(f"Created directory: {node_dir}", 1)
            except Exception as e:
                self.top_ui.set_top_info(f"Failed to create directory: {str(e)}", 8)
                return False

        # 3) Add Path To Database
        self.batch.logger.db(("on_click_full_init_server 3", node_dir, node_name))
        self.on_click_add_node()
        
        # 4) Copy/Update source files
        self.batch.logger.db(("on_click_full_init_server 4", node_dir, node_name))
        dest = self.qt_form_add_node_el_path.text() # 'Add' form path
        self.server.update_sources_from_master(force_destination=dest)
        
        # 5) Copy config.ini
        self.batch.logger.db(("on_click_full_init_server 5", node_dir, node_name))
        self.create_or_update_config(node_dir, "Config copied")
            
        # 6) Create state.txt file with INDEX_STATE_INIT

        self.batch.logger.db(("on_click_full_init_server 6", node_dir, node_name))
        state_file = node_dir + "state.txt"
        if self.batch.comfun.file_exists(state_file, info=False) is False: 
            init_state_id = self.batch.sts.INDEX_STATE_INIT
            create_result = self.batch.nod.create_node_state_file(state_file, node_name, init_state_id)
            if not create_result:
                self.top_ui.set_top_info("Failed to create state.txt file", 8)
                self.batch.logger.err(f"Failed to create state.txt file: {state_file}")
                return False
            
        self.top_ui.set_top_info(f"Server '{node_name}' fully initialized: {node_dir}", 1)
        return True
