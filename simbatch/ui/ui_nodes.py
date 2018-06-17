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
# from simbatch.core.nodes import *


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

    freeze_list_on_changed = 0
    last_node_list_index = None   # used for list item color change to unselected

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
        qt_lay_nodes_buttons = QHBoxLayout()

        qt_b_add_node = QPushButton("Add Node ")
        qt_b_remove_node = QPushButton("Remove Node ")
        qt_b_restart_node = QPushButton("Restart Node ")
        qt_b_refresh_nodes = QPushButton("Refresh Nodes")

        qt_lay_nodes_list.addWidget(qt_list_nodes)
        qt_lay_nodes_buttons.addWidget(qt_b_add_node)
        qt_lay_nodes_buttons.addWidget(qt_b_remove_node)
        qt_lay_nodes_buttons.addWidget(qt_b_restart_node)
        qt_lay_nodes_buttons.addWidget(qt_b_refresh_nodes)

        qt_b_add_node.clicked.connect(self.add_node)
        qt_b_remove_node.clicked.connect(self.on_remove_node)
        qt_b_restart_node.clicked.connect(self.on_restart_node)
        qt_b_refresh_nodes.clicked.connect(self.on_refresh_nodes)

        qt_lay_nodes_main.addLayout(qt_lay_nodes_list)
        qt_lay_nodes_main.addLayout(qt_lay_nodes_buttons)

        # get_node_state
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

    def on_menu_remove(self):    # TODO
        self.batch.logger.db("on menu: Remove  TODO")

    def on_menu_reset(self):
        self.batch.logger.db("on menu: Reset")
        self.on_restart_node()

    def show_right_click_menu(self, pos):
        global_pos = self.qt_list_nodes.mapToGlobal(pos)
        qt_right_menu = QMenu()
        qt_right_menu.addAction("Reset Node", self.on_menu_reset)
        qt_right_menu.addAction("Remove Node", self.on_menu_remove)
        qt_right_menu.exec_(global_pos)

    def clear_list(self, with_freeze=False):  # TODO with freeze
        while self.qt_list_nodes.count() > 0:
            self.qt_list_nodes.takeItem(0)

    def add_node(self):    # TODO
        self.batch.logger.raw(" TODO: add_node ")

    def on_remove_node(self):    # TODO
        self.batch.logger.raw(" TODO: on_remove_node ")

    def on_restart_node(self):
        if self.nod.current_node_index >= 0:
            current_node = self.nod.nodes_data[self.nod.current_node_index]
            srv_name = self.nod.get_server_name_from_file(current_node.state_file)
            self.batch.logger.db(("set IDLE to node:", srv_name))
            self.nod.set_node_state(current_node.state_file, srv_name, 2)
        else:
            self.batch.logger.wrn("(on restart node) PLEASE SELECT ITEM FIRST")
            self.top_ui.set_top_info(" Select item first ", 7)

    def on_menu_reset(self):
        self.batch.logger.db("on menu: Reset")
        self.on_restart_node()

    def on_refresh_nodes(self):
        self.batch.logger.db("on_refresh_nodes")
        self.clear_list()
        self.nod.clear_all_nodes_data()
        self.nod.load_nodes()
        # self.nod.checkNodesState()     #TODO
        self.batch.initNodes(self.qt_list_nodes)
        do_update_node_data_file = self.nod.checkNodesStateFiles()
        if do_update_node_data_file == 1:     # TODO optimize  up
            self.batch.logger.db("do_update_node_data_file")
            self.nod.save_nodes()
            self.clear_list()
            self.nod.clear_all_nodes_data()
            self.nod.load_nodes()
            # self.nod.checkNodesState()   ### TODO
            self.batch.initNodes(self.qt_list_nodes)

    def on_list_nodes_current_changed(self, x):
        if self.freeze_list_on_changed == 1:   # freeze update changes on massive action    i.e  clear_list()
            self.batch.logger.deepdb(("simnodes chngd freeze_list_on_changed", self.qt_list_nodes.currentRow()))
        else:
            self.batch.logger.inf(("on_list_current_changed", self.qt_list_nodes.currentRow()))

            self.last_node_list_index = self.batch.nod.current_node_index
            current_list_index = self.qt_list_nodes.currentRow() - 1
            self.batch.nod.current_node_index = current_list_index
            self.batch.nod.update_current_from_index(current_list_index)

            # update color of last item list
            if self.last_node_list_index >= 0:
                last_item = self.qt_list_nodes.item(self.last_node_list_index + 1)
                last_node_state_id = self.batch.nod.nodes_data[self.last_node_list_index].state_id
                color_index = last_node_state_id
                if last_item is not None:
                    last_item.setBackground(self.batch.sts.state_colors[color_index].color())

            # update top info and color of current item list
            if 0 <= current_list_index < len(self.batch.nod.nodes_data):
                cur_node = self.batch.nod.nodes_data[current_list_index]
                color_index = cur_node.state_id
                item_c = self.qt_list_nodes.item(current_list_index + 1)
                cur_color = self.batch.sts.state_colors_up[color_index].color()
                item_c.setBackground(cur_color)
                if self.top_ui is not None:
                    self.top_ui.set_top_info("Current node:   " + cur_node.node_name)
            else:
                self.batch.logger.wrn(("(on chng) Wrong current_list_index: ", current_list_index))
