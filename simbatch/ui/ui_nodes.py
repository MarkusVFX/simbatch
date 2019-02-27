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
    remove_node_form_state = 0

    qt_form_add_node = None
    qt_form_add_node_el_path = None
    qt_form_add_node_el_name = None
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
        qt_b_reset_node = QPushButton("Reset")
        qt_b_remove_node = QPushButton("Remove")
        qt_b_update_nodes = QPushButton("Reload")

        qt_lay_nodes_list.addWidget(qt_list_nodes)
        qt_lay_nodes_buttons.addWidget(qt_b_add_node)
        qt_lay_nodes_buttons.addWidget(qt_b_reset_node)
        qt_lay_nodes_buttons.addWidget(qt_b_remove_node)
        qt_lay_nodes_buttons.addWidget(qt_b_update_nodes)

        qt_b_add_node.clicked.connect(self.on_click_show_add_node_form)
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
        wfa_name.button_1.clicked.connect(self.on_click_name_from_file)
        self.qt_form_add_node_el_name = wfa_name.qt_edit_line

        wfr_button_src = ButtonWithCheckBoxes("Copy/Update source files", button_width=155, label_text=" ")
        wfr_button_add = ButtonWithCheckBoxes("Add Path To Database", button_width=155, label_text=" ")
        wfr_button_add.button.clicked.connect(self.on_click_add_node)

        qt_form_add_node_layout.addRow(" ", QLabel("   "))
        qt_form_add_node_layout.addRow(" ", wfa_path.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", wfa_name.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", wfr_button_add.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", wfr_button_src.qt_widget_layout)
        qt_form_add_node_layout.addRow(" ", QLabel("   "))

        qt_gb_add_node = QGroupBox()
        qt_gb_add_node.setLayout(qt_form_add_node_layout)
        qt_form_add_node_layout_ext.addWidget(qt_gb_add_node)
        qt_gb_add_node.setTitle("Add Sim Node")


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

        self.comfun.add_widgets(qt_lay_nodes_forms, [qt_form_add_node, qt_form_remove_node])

        self.comfun.add_layouts(qt_lay_nodes_main, [qt_lay_nodes_list, qt_lay_nodes_forms, qt_lay_nodes_buttons])

        self.init_nodes()

    def init_nodes(self):
        widget_list = self.qt_list_nodes
        qt_list_item = QListWidgetItem(widget_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)

        list_item_widget = NodeListItem("ID", "name",  "state", "descr")

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
        qt_right_menu.addAction("Remove Node", self.on_menu_remove)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Break server's main loop", self.on_menu_break)

        qt_right_menu.exec_(global_pos)

    def clear_list(self, with_freeze=False):  # TODO with freeze
        while self.qt_list_nodes.count() > 0:
            self.qt_list_nodes.takeItem(0)

    def hide_all_forms(self):
        self.qt_form_add_node.hide()
        self.qt_form_remove_node.hide()
        self.add_node_form_state = 0
        self.remove_node_form_state = 0

    def on_click_show_add_node_form(self):
        if self.add_node_form_state == 0:
            self.hide_all_forms()
            self.qt_form_add_node.show()
            self.add_node_form_state = 1
        else:
            self.qt_form_add_node.hide()
            self.add_node_form_state = 0

    def on_click_name_from_file(self):
        dir = self.qt_form_add_node_el_path.text()
        file = "state.txt"   # TODO  move to setttings  or add custom

        if len(dir) == 0:
            self.top_ui.set_top_info("Please set path first!", 8)
            return False
        if self.batch.comfun.file_exists(dir + file):
            ret = self.batch.nod.get_server_name_from_file(dir + file)
            if len(ret) > 0:
                self.qt_form_add_node_el_name.setText(ret)
                self.top_ui.set_top_info("Found name: " + ret, 4)
            else:
                self.top_ui.set_top_info("Name not defined in state file!", 8)
        else:
            self.top_ui.set_top_info("State file not exist, please insert name manually ", 8)

    def on_click_path_get(self):
        # self.batch.comfun.file_dialog_to_edit_line(self.qt_form_add_node_el_path, QFileDialog, "")
        self.batch.comfun.get_dialog_directory(self.qt_form_add_node_el_path, QFileDialog,
                                               dir_separator=self.batch.sts.dir_separator)

    def on_click_path_check(self):
        dir = self.qt_form_add_node_el_path.text()
        file = "state.txt"   # TODO  move to setttings  or add custom
        if self.batch.comfun.path_exists(dir):
            if self.batch.comfun.file_exists(dir+file):
                self.top_ui.set_top_info("Directory exist, state file exist ", 4)
            else:
                self.top_ui.set_top_info("Directory exist, state file not exist ", 4)
        else:
            self.top_ui.set_top_info("Directory not exist ", 7)

    def on_click_add_node(self):
        self.batch.logger.db(("add_node",  "add"))
        desc = self.batch.comfun.get_current_time()
        node_dir = self.qt_form_add_node_el_path.text()

        if len(node_dir) > 0:
            if self.batch.comfun.path_exists(node_dir):
                node_name = self.qt_form_add_node_el_name.text()
                if len(node_name) > 0:
                    state_file = node_dir + "state.txt"   # TODO  move to setttings  or add custom

                    node_state_id = self.batch.sts.INDEX_STATE_WAITING
                    if self.batch.comfun.file_exists(state_file):
                        ret = self.batch.nod.get_node_state(state_file)
                        if ret > 0:
                            node_state_id = ret
                        self.batch.nod.create_node_state_file(state_file, node_name, node_state_id, update_mode=True)
                    else:
                        self.batch.nod.create_node_state_file(state_file, node_name, node_state_id)
                        # TODO  server py files !!!

                    node_state = self.batch.sts.states_visible_names[node_state_id]

                    new_node = self.batch.nod.get_new_node(node_name, node_state, node_state_id, state_file, desc)
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

    def on_click_show_remove_node_form(self):
        if self.remove_node_form_state == 0:
            self.hide_all_forms()
            self.qt_form_remove_node.show()
            self.remove_node_form_state = 1
        else:
            self.qt_form_remove_node.hide()
            self.remove_node_form_state = 0

    def on_click_confirmed_remove_node(self):
        if self.nod.current_node_index >= 0:
            current_node = self.nod.nodes_data[self.nod.current_node_index]
            self.batch.logger.db(("remove node:", current_node.id, current_node.node_name))
            self.nod.remove_node(current_node.id, do_save=True)
            self.reset_list()
            self.hide_all_forms()
        else:
            self.batch.logger.wrn("(on remove node) PLEASE SELECT ITEM FIRST")
            self.top_ui.set_top_info(" Select item first ", 7)

    def on_reset_node(self):
        if self.nod.current_node_index >= 0:
            current_node = self.nod.nodes_data[self.nod.current_node_index]

            default_state_id = self.batch.sts.INDEX_STATE_WAITING

            if self.batch.comfun.file_exists(current_node.state_file) is False:
                self.batch.nod.create_node_state_file(current_node.state_file, current_node.node_name, default_state_id)
                self.top_ui.set_top_info("Simnode state file created", 4)
            else:
                srv_name = current_node.node_name
                self.batch.logger.db(("Set WAITING state to node:", srv_name))
                self.nod.create_node_state_file(current_node.state_file, srv_name, default_state_id, update_mode=True)
                self.top_ui.set_top_info("Simnode state file updated", 4)
            current_node.state_id = default_state_id
            current_node.state = self.batch.sts.states_visible_names[default_state_id]
            self.batch.nod.save_nodes()
            self.reset_list()
        else:
            self.batch.logger.wrn("(on reset node) PLEASE SELECT ITEM FIRST")
            self.top_ui.set_top_info(" Select item first ", 7)

    def on_menu_reset(self):
        self.batch.logger.db("on menu: Reset")
        self.on_reset_node()

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

    def on_list_nodes_current_changed(self, x):
        if self.freeze_list_on_changed == 1:   # freeze update changes on massive action    i.e  clear_list()
            self.batch.logger.deepdb(("simnodes change freeze_list_on_changed", self.qt_list_nodes.currentRow()))
        else:
            self.batch.logger.inf(("on_list_current_changed", self.qt_list_nodes.currentRow()))
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
            else:
                self.batch.logger.wrn(("(on change) Wrong current_list_index: ", current_list_index))
