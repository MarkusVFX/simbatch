import os
import subprocess

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

from ui_queue_forms import QueueFormEdit, QueueFormRemove


class QueueListItem(QWidget):
    # def __init__(self, txt_id, txt_name, txt_user, txt_prior, txt_state, txt_evo, txt_node, txt_desc):
    # TODO PRO VER PRIOR
    def __init__(self, txt_id, txt_name, txt_user, txt_state, txt_evo, txt_node, txt_desc):
        super(QueueListItem, self).__init__()
        self.qt_widget = QWidget(self)
        self.qt_label_font = QFont()
        self.qt_label_font.setPointSize(8)

        self.qt_lay = QHBoxLayout(self.qt_widget)
        self.qt_lay.setSpacing(0)
        self.qt_lay.setContentsMargins(0, 0, 0, 0)

        self.qt_label_id = QLabel(txt_id)
        self.qt_label_id.setFont(self.qt_label_font)
        self.qt_label_id.setStyleSheet("""color:#000;""")
        self.qt_label_id.setMinimumWidth(22)
        self.qt_label_id.setMaximumWidth(22)
        self.qt_lay.addWidget(self.qt_label_id)

        self.qt_label_name = QLabel(txt_name)
        self.qt_label_name.setFont(self.qt_label_font)
        self.qt_label_name.setStyleSheet("""color:#000;""")
        self.qt_label_name.setMinimumWidth(180)
        self.qt_label_name.setMaximumWidth(250)
        self.qt_lay.addWidget(self.qt_label_name)

        self.qt_label_user = QLabel(txt_user)
        self.qt_label_user.setFont(self.qt_label_font)
        self.qt_label_user.setStyleSheet("""color:#000;""")
        self.qt_label_user.setMinimumWidth(22)
        self.qt_label_user.setMaximumWidth(30)
        self.qt_lay.addWidget(self.qt_label_user)

        # TODO PRO VER PRIOR
        # self.qt_label_prior = QLabel(txt_prior)
        # self.qt_label_prior.setFont(self.qt_label_font)
        # self.qt_label_prior.setStyleSheet("""color:#000;""")
        # self.qt_label_prior.setMinimumWidth(22)
        # self.qt_label_prior.setMaximumWidth(30)
        # self.qt_lay.addWidget(self.qt_label_prior)

        self.qt_label_state = QLabel(txt_state)
        self.qt_label_state.setFont(self.qt_label_font)
        self.qt_label_state.setStyleSheet("""color:#000;""")
        self.qt_label_state.setMinimumWidth(50)
        self.qt_label_state.setMaximumWidth(60)
        self.qt_lay.addWidget(self.qt_label_state)

        self.qt_label_evo = QLabel(txt_evo)
        self.qt_label_evo.setFont(self.qt_label_font)
        self.qt_label_evo.setStyleSheet("""color:#000;""")
        self.qt_label_evo.setMinimumWidth(10)
        self.qt_label_evo.setMaximumWidth(170)
        self.qt_lay.addWidget(self.qt_label_evo)

        self.qt_label_node = QLabel(txt_node)
        self.qt_label_node.setFont(self.qt_label_font)
        self.qt_label_node.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_node)

        self.qt_label_desc = QLabel(txt_desc)
        self.qt_label_desc.setFont(self.qt_label_font)
        self.qt_label_desc.setStyleSheet("""color:#000;""")
        self.qt_lay.addWidget(self.qt_label_desc)

        self.setLayout(self.qt_lay)


class QueueUI:
    list_queue = None
    qt_widget_queue = None

    batch = None
    top_ui = None

    qt_form_edit = None
    qt_form_remove = None

    edit_form_state = 0
    remove_form_state = 0

    freeze_list_on_changed = 0

    array_visible_queue_items_ids = []

    current_list_item_index = None
    last_list_item_index = None

    qt_list_item = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.sts = batch.sts
        self.que = batch.que
        self.comfun = batch.comfun
        self.top_ui = top
        self.mainw = mainw

        list_queue = QListWidget()
        list_queue.setSelectionMode(QAbstractItemView.NoSelection)

        list_queue.setFrameShadow(QFrame.Raised)
        list_queue.currentItemChanged.connect(self.on_current_item_changed)
        list_queue.setSpacing(1)
        p = list_queue.sizePolicy()
        p.setVerticalPolicy(QSizePolicy.Policy.Maximum)

        list_queue.setContextMenuPolicy(Qt.CustomContextMenu)
        list_queue.customContextMenuRequested.connect(self.on_right_click_show_menu)

        self.list_queue = list_queue

        qt_widget_queue = QWidget()
        self.qt_widget_queue = qt_widget_queue
        qt_lay_queue_main = QVBoxLayout(qt_widget_queue)
        qt_lay_queue_main.setContentsMargins(0, 0, 0, 0)

        qt_lay_queue_list = QHBoxLayout()
        qt_lay_forms = QVBoxLayout()
        qt_lay_queue_buttons = QHBoxLayout()

        # EDIT
        # EDIT EDIT
        # EDIT EDIT EDIT
        qt_form_edit = QueueFormEdit(self.batch, self.mainw)
        self.qt_form_edit = qt_form_edit

        # REMOVE
        # REMOVE REMOVE
        # REMOVE REMOVE REMOVE
        qt_form_remove = QueueFormRemove(self.batch, self.mainw)
        self.qt_form_remove = qt_form_remove

        self.comfun.add_widgets(qt_lay_forms, [qt_form_edit, qt_form_remove])

        self.hide_all_forms()

        self.qt_button_sim_one = QPushButton("Simulate One")
        self.qt_button_sim_all = QPushButton("Simulate All")
        self.qt_button_queue_remove = QPushButton("Remove from Queue")
        self.qt_button_queue_edit = QPushButton("Edit")

        self.qt_button_sim_one.clicked.connect(self.on_click_sim_one)
        self.qt_button_sim_all.clicked.connect(self.on_click_sim_all)
        self.qt_button_queue_remove.clicked.connect(self.on_click_remove)
        self.qt_button_queue_edit.clicked.connect(self.on_click_edit)

        qt_lay_queue_list.addWidget(list_queue)
        self.comfun.add_widgets(qt_lay_queue_buttons, [self.qt_button_sim_one, self.qt_button_sim_all,
                                                       self.qt_button_queue_remove, self.qt_button_queue_edit])
        self.comfun.add_layouts(qt_lay_queue_main, [qt_lay_queue_list, qt_lay_forms, qt_lay_queue_buttons])

        self.init_queue_items()

    def init_queue_items(self):
        widget_list = self.list_queue
        qt_list_item = QListWidgetItem(widget_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)

        # TODO PRO VER PRIOR
        # list_item_widget = QueueListItem("ID", "queue item name", "user", "prior", "state", "evo", "sim node", "desc")
        list_item_widget = QueueListItem("ID", "queue item name", "user", "state", "evo", "sim node", "desc")

        widget_list.addItem(qt_list_item)
        widget_list.setItemWidget(qt_list_item, list_item_widget)
        qt_list_item.setSizeHint(QSize(1, 24))
        if self.sts.ui_brightness_mode == 0:
            qt_list_item.setBackground(self.sts.state_colors[0])
        else:
            qt_list_item.setBackground(self.sts.state_colors_up[0])

        for que in self.batch.que.queue_data:
            qt_list_item = QListWidgetItem(widget_list)
            cur_color = self.sts.state_colors[que.state_id].color()
            qt_list_item.setBackground(cur_color)
            # list_item_widget = QueueListItem(str(que.id), que.queue_item_name, que.user, str(que.prior), que.state,
            #                                  que.evolution, que.sim_node, que.description)
            list_item_widget = QueueListItem(str(que.id), que.queue_item_name, que.user, que.state,
                                             que.evolution, que.sim_node, que.description)

            widget_list.addItem(qt_list_item)
            widget_list.setItemWidget(qt_list_item, list_item_widget)
            qt_list_item.setSizeHint(QSize(130, 26))
            qt_list_item.setBackground(self.sts.state_colors[que.state_id])

        self.list_queue.scrollToBottom()

    def reset_list(self):
        self.freeze_list_on_changed = 1
        current_id = self.batch.que.current_queue_id
        self.clear_list(with_freeze=False)
        self.init_queue_items()
        if current_id is not None:
            index = self.batch.que.get_index_by_id(current_id)
            if index is not None:
                self.batch.que.current_queue_index = index
                self.batch.que.current_queue_id = self.batch.que.queue_data[self.batch.que.current_queue_index].id
            else:
                self.batch.que.current_queue_id = None   # not exist anymore
            # TODO highlight q item
        self.freeze_list_on_changed = 0

    def update_all_queue(self):
        self.clear_list()
        self.init_queue_items()
        self.update_list_of_visible_ids()

    def reload_queue_data_and_refresh_list(self):
        self.batch.que.clear_all_queue_items()
        self.batch.que.load_queue()
        self.reset_list()
        self.update_list_of_visible_ids()
        self.hide_all_forms()

    def _change_current_queue_item_state_and_reset_list(self, state_id):
        self.batch.que.current_queue.state = self.sts.states_visible_names[state_id]
        self.batch.que.current_queue.state_id = state_id
        self.batch.que.save_queue()
        self.reset_list()

    def on_click_menu_set_init(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_INIT)

    def on_click_menu_set_waiting(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_WAITING)

    def on_click_menu_set_working(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_WORKING)

    def on_click_menu_set_done(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_DONE)

    def on_click_menu_set_accepted(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_ACCEPTED)

    def on_click_menu_set_hold(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_HOLD)

    def on_click_menu_set_killed(self):
        self._change_current_queue_item_state_and_reset_list(self.sts.INDEX_STATE_KILLED)


    def get_prev_dir_from_queue_item(self):
        cur_queue_item = self.batch.que.queue_data[self.batch.que.current_queue_index]
        proj_id = cur_queue_item.proj_id
        task_id = cur_queue_item.task_id
        evo_nr = cur_queue_item.evolution_nr
        version = cur_queue_item.version
        # prev_dir = self.batch.dfn.get_task_prev_dir(forceProjID=proj_id, forceTaskID=task_id, evolution_nr=evo_nr,
        #                                             forceQueueVersion=version)
        # prev_dir = self.batch.sio.generate_shot_prev_seq()   # TODO   cleanup def generate_shot_prev_seq

        prj = self.batch.prj.get_project_by_id(proj_id)
        tsk = self.batch.tsk.get_task_by_id(task_id)
        sch = self.batch.sch.get_schema_by_id(tsk.schema_id)
        if evo_nr > 0:
            evo = "_evo" + self.batch.comfun.str_with_zeros(evo_nr, 2)  # TODO batch.prj.current_project.zeros_in_evo
        else:
            evo = None

        ret = self.batch.sio.generate_shot_prev_seq(prj=prj, sch=sch, tsk=tsk, ver=version, evo=evo)  # TODO cleanup)

        if ret[0] == 1:
            return ret[1]
        else:
            ret = self.batch.sio.generate_shot_working_dir()
            if ret[0] == 1:
                self.batch.logger.wrn("can not generate prev dir")
            else:
                self.batch.logger.wrn("can not generate shot_working_dir")
                if self.batch.prj.current_project is None:
                    self.batch.logger.wrn(" self.prj.current_project in None")
                if self.batch.sch.current_schema is None:
                    self.batch.logger.wrn(" self.batch.sch.current_schema in None")
                if self.batch.tsk.current_task is None:
                    self.batch.logger.wrn(" self.batch.tsk.current_task in None")
            return False

    def on_menu_locate_prev(self):
        ret = self.get_prev_dir_from_queue_item()

        if ret is not False:
            prev_dir = self.comfun.dirname(ret)
            self.batch.logger.inf(("Prev dir: ", prev_dir))

            prev_dir = prev_dir + self.sts.dir_separator
            if self.comfun.path_exists(prev_dir, " prev open "):
                if self.sts.current_os == 1:
                    os.system('xdg-open "{}"'.format(prev_dir))
                else:
                    subprocess.Popen('explorer "' + prev_dir + '"')
        else:
            self.batch.logger.wrn("prev dir not exist ")
            self.top_ui.set_top_info("prev dir not exist", 8)

    def on_menu_open_prev(self):
        ret = self.get_prev_dir_from_queue_item()

        if ret is not False:
            prev_dir = self.comfun.dirname(ret)
            self.batch.logger.inf(("Prev dir: ", prev_dir))

            prev_dir = prev_dir + self.sts.dir_separator
            if self.comfun.path_exists(prev_dir, " prev open "):
                import subprocess
                if self.sts.current_os == 1:
                    # TODO hardcode
                    print "HK rv:",  ret
                    subprocess.Popen(['rv', 'rvlink://'+ret])
                    # TODO hardcode
                else:
                    subprocess.Popen('explorer "' + prev_dir + '"')
        else:
            self.batch.logger.wrn("prev dir not exist ")
            self.top_ui.set_top_info("prev dir not exist", 8)

    def on_click_menu_open_shot_setup(self):
        self.open_shot_setup()   # TODO ret

    def on_click_menu_open_simed_shot_setup(self):
        self.open_shot_setup(simed=True)

    def open_shot_setup(self, simed=False):
        cur_queue_item = self.batch.que.queue_data[self.batch.que.current_queue_index]
        task_id = cur_queue_item.task_id
        version = cur_queue_item.version

        file_to_load = self.batch.sio.generate_shot_setup_file_name(tsk_id=task_id, ver=version, simed=simed)

        if file_to_load is not False:
            if self.comfun.file_exists(file_to_load):
                self.batch.logger.inf(("file_to_load ", file_to_load))
                if self.batch.dfn.current_interactions is not None:
                    self.batch.dfn.current_interactions.open_setup(file_to_load)  # TODO check ret
                else:
                    self.batch.logger.err("Current interactions are not loaded")
                    self.top_ui.set_top_info("Current interactions are not loaded", 8)
            else:
                self.batch.logger.wrn(("file_to_load not exist: ", file_to_load))
                self.top_ui.set_top_info("file_to_load not exist", 8)
        else:
            self.batch.logger.wrn(("can not get file_to_load   from : task_id, version : ", task_id, version))

    def on_click_menu_sim_selected(self):
        self.sim_current()

    def on_click_menu_queue_item_remove(self):
        self.on_click_confirmed_remove_queue_item()
        
    def on_click_menu_queue_item_remove_all_green(self):
        self.on_click_confirmed_remove_queue_items_green()

    def on_click_menu_queue_item_remove_all_done(self):
        self.on_click_confirmed_remove_queue_items_done()

    def on_click_menu_queue_item_remove_all_killed(self):
        self.on_click_confirmed_remove_queue_items_killed()

    def on_click_menu_queue_item_remove_all_hold(self):
        self.on_click_confirmed_remove_queue_items_hold()

    def on_click_menu_queue_item_remove_all_working(self):
        self.on_click_confirmed_remove_queue_items_working()

    @staticmethod
    def on_click_menu_spacer():
        pass

    def on_right_click_show_menu(self, pos):
        global_cursor_pos = self.list_queue.mapToGlobal(pos)
        qt_right_menu = QMenu()
        # qt_right_menu.addAction("Set INIT", self.on_click_menu_set_init)
        qt_right_menu.addAction("Set WAITING", self.on_click_menu_set_waiting)
        qt_right_menu.addAction("Set WORKING", self.on_click_menu_set_working)
        qt_right_menu.addAction("Set DONE", self.on_click_menu_set_done)
        qt_right_menu.addAction("Set ACCEPTED", self.on_click_menu_set_accepted)
        qt_right_menu.addAction("Set HOLD", self.on_click_menu_set_hold)
        qt_right_menu.addAction("Set KILLED", self.on_click_menu_set_killed)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Locate prev", self.on_menu_locate_prev)
        qt_right_menu.addAction("Open prev", self.on_menu_open_prev)
        qt_right_menu.addAction("Open shot scene", self.on_click_menu_open_shot_setup)
        qt_right_menu.addAction("Open simed shot scene", self.on_click_menu_open_simed_shot_setup)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Simulate Selected", self.on_click_menu_sim_selected)
        qt_right_menu.addAction("________", self.on_click_menu_spacer)
        qt_right_menu.addAction("Remove All DONE", self.on_click_menu_queue_item_remove_all_done)
        qt_right_menu.addAction("Remove All WORKING", self.on_click_menu_queue_item_remove_all_working)
        qt_right_menu.addAction("Remove All HOLD", self.on_click_menu_queue_item_remove_all_hold)
        qt_right_menu.addAction("Remove All KILLED", self.on_click_menu_queue_item_remove_all_killed)
        qt_right_menu.addAction("Remove", self.on_click_menu_queue_item_remove)
        qt_right_menu.exec_(global_cursor_pos)

    def hide_all_forms(self):
        self.qt_form_edit.hide()
        self.qt_form_remove.hide()
        self.edit_form_state = 0
        self.remove_form_state = 0

    def add_queue_item_to_list(self, new_queue_item):
        wigdet_list = self.list_queue
        qt_list_item = QListWidgetItem(wigdet_list)
        qt_list_item.setBackground(QBrush(QColor("#ddd")))
        qt_list_item.setFlags(Qt.ItemFlag.NoItemFlags)
        new_queue_item = new_queue_item
        list_item_widget = QueueListItem(str(new_queue_item.id), new_queue_item.queue_item_name, new_queue_item.user,
                                         str(new_queue_item.prior), new_queue_item.state, new_queue_item.evolution,
                                         new_queue_item.sim_node, new_queue_item.description)

        wigdet_list.addItem(qt_list_item)
        wigdet_list.setItemWidget(qt_list_item, list_item_widget)
        qt_list_item.setSizeHint(QSize(1, 24))

    def set_buttons_state(self, state):
        self.qt_button_sim_one.setEnabled(state)
        self.qt_button_sim_one.repaint()
        self.qt_button_sim_all.setEnabled(state)
        self.qt_button_sim_all.repaint()
        self.qt_button_queue_remove.setEnabled(state)
        self.qt_button_queue_remove.repaint()
        self.qt_button_queue_edit.setEnabled(state)
        self.qt_button_queue_edit.repaint()

    def sim_current(self):
        if self.batch.que.current_queue is not None:
            self.run_server_from_framework("single", force_id=self.batch.que.current_queue_id)

    def run_server_from_framework(self, mode, force_id=None):
        server = self.mainw.server  # .SimBatchServer(self.batch, framework_mode=True)
        server.framework_mode = True
        server.loops_counter = 0
        server.timer_delay_seconds = 0
        server.reset()
        #
        server.run(mode, force_id=force_id)
        #
        report = server.generate_report()  # TODO report as class
        if report[0] > 0:
            if report[0] == 1:
                self.top_ui.set_top_info(server.last_info, 1)
            else:
                self.top_ui.set_top_info(("total computed:", report[0], "   last", server.last_info), 6)

            self.reload_queue_data_and_refresh_list()  # TODO check threads, pararell DB print, duplicate items !!!
            self.reload_queue_data_and_refresh_list()  # TODO solve doubled refresh protection (que list dupicates) !!!
        else:
            if len(server.last_info) > 0:
                self.top_ui.set_top_info(server.last_info, 1)
        
    def on_click_sim_one(self):
        self.top_ui.set_top_info("start single simulation")
        self.set_buttons_state(False)
        self.run_server_from_framework("single")
        self.set_buttons_state(True)

    def on_click_sim_all(self):
        self.top_ui.set_top_info("start simulate all")
        self.set_buttons_state(False)
        self.run_server_from_framework("all")
        self.set_buttons_state(True)

    def on_click_edit(self):
        if self.edit_form_state == 0:
            if self.batch.que.current_queue_index is not None:
                self.hide_all_forms()
                self.qt_form_edit.update_edit_ui()
                self.qt_form_edit.show()
                self.edit_form_state = 1
            else:
                self.batch.logger.wrn("(on_click_edit) Please Select Queue Item")
                self.top_ui.set_top_info("Please select queue item first", 7)
        else:
            self.qt_form_edit.hide()
            self.edit_form_state = 0

    def on_click_remove(self):
        if self.remove_form_state == 0:
            if self.batch.que.current_queue_index is not None:
                self.hide_all_forms()
                self.qt_form_remove.show()
                self.remove_form_state = 1
            else:
                self.batch.logger.wrn("(on_click_edit) Please Select Queue Item")
                self.top_ui.set_top_info("Please select queue item first", 7)
        else:
            self.qt_form_remove.hide()
            self.remove_form_state = 0
    
    def remove_queue_item(self):
        if self.current_list_item_index >= 0:
            take_item_list = self.current_list_item_index + 1
            ret = self.batch.que.remove_single_queue_item(index=self.batch.que.current_queue_index, do_save=True)
            if ret:
                self.last_list_item_index = None
                self.batch.que.current_queue_index = None
                self.current_list_item_index = None
                self.list_queue.takeItem(take_item_list)
                self.qt_form_remove.hide()
                self.remove_form_state = 0
            else:
                self.batch.logger.err(("cannot remove q item from database, index: ", self.current_list_item_index))
        else:
            self.batch.logger.wrn(("cannot remove from list, element unknown for list index: ",
                                   self.current_list_item_index))

    def on_click_confirmed_remove_queue_item(self):
        self.batch.logger.db(("remove_queue_item", self.batch.que.current_queue_index,
                              self.current_list_item_index))
        self.remove_queue_item()
        self.update_list_of_visible_ids()


    def remove_items_by_state(self, state_id):
        self.batch.logger.db(("remove_queue_items", self.sts.states_visible_names[state_id]))
        self.batch.que.remove_queue_items(state_id=state_id)
        self.batch.que.save_queue()
        self.reset_list()
        self.update_list_of_visible_ids()

    def on_click_confirmed_remove_queue_items_green(self):
        self.remove_items_by_state(self.sts.INDEX_STATE_DONE)

    def on_click_confirmed_remove_queue_items_done(self):
        self.remove_items_by_state(self.sts.INDEX_STATE_DONE)

    def on_click_confirmed_remove_queue_items_killed(self):
        self.remove_items_by_state(self.sts.INDEX_STATE_KILLED)

    def on_click_confirmed_remove_queue_items_hold(self):
        self.remove_items_by_state(self.sts.INDEX_STATE_HOLD)

    def on_click_confirmed_remove_queue_items_working(self):
        self.remove_items_by_state(self.sts.INDEX_STATE_WORKING)

    def clear_list(self, with_freeze=True):
        if with_freeze:
            self.freeze_list_on_changed = 1
        while self.list_queue.count() > 0:
            self.list_queue.takeItem(0)
        if with_freeze:
            self.freeze_list_on_changed = 0

    def update_list_of_visible_ids(self, filters=None):
        array_visible_queue_items_ids = []
        for que in self.batch.que.queue_data:
            if filters is None:
                array_visible_queue_items_ids.append(que.id)
            else:
                # TODO filter project, limit, user, ...
                if que.proj_id == self.batch.prj.current_project_id:
                    array_visible_queue_items_ids.append(que.id)
        self.array_visible_queue_items_ids = array_visible_queue_items_ids

    def on_current_item_changed(self, current_queue_item):
        if self.freeze_list_on_changed == 1:   # freeze update changes on massive action    i.e  clear_list()
            self.batch.logger.deepdb(("que chngd freeze_list_on_changed", self.list_queue.currentRow()))
        else:
            self.batch.logger.db(("list_queue_current_item_changed: ", self.list_queue.currentRow()))
            self.last_list_item_index = self.current_list_item_index
            current_list_index = self.list_queue.currentRow() - 1
            self.current_list_item_index = current_list_index

            if self.last_list_item_index is not None:
                if self.last_list_item_index is not None and self.last_list_item_index < len(self.batch.que.queue_data):
                    item = self.list_queue.item(self.last_list_item_index + 1)
                    if self.last_list_item_index < len(self.array_visible_queue_items_ids):
                        last_id = self.array_visible_queue_items_ids[self.last_list_item_index]
                        last_index = self.batch.que.get_index_by_id(last_id)
                        if item is not None and last_index is not None:
                            color_index = self.batch.que.queue_data[last_index].state_id
                            item.setBackground(self.batch.sts.state_colors[color_index].color())
                else:
                    self.batch.logger.wrn("Wrong last_que_list_index {} vs {} ".format(self.last_list_item_index,
                                                                                       len(self.batch.tsk.tasks_data)))
            else:
                self.batch.logger.db("last_task_list_index is None")

            if len(self.array_visible_queue_items_ids) <= current_list_index:
                self.update_list_of_visible_ids()  # TODO move  to init / change list
                if len(self.array_visible_queue_items_ids) > current_list_index:
                    self.batch.logger.deepdb(("vis ids FIXED: len(array_visible_queue_items_ids):",
                                              len(self.array_visible_queue_items_ids),
                                              "vs current_list_index:", current_list_index))
                else:
                    self.batch.logger.err(("vis ids NOT FIXED: len(array_visible_queue_items_ids):",
                                           len(self.array_visible_queue_items_ids),
                                           "vs current_list_index:", current_list_index))

            if 0 <= current_list_index < len(self.array_visible_queue_items_ids):
                current_queue_item_id = self.array_visible_queue_items_ids[current_list_index]
                self.batch.que.current_queue_id = current_queue_item_id
                self.batch.que.update_current_from_id(current_queue_item_id)
            else:
                self.batch.logger.err(("Wrong current_list_index: ", current_list_index,
                                       " or array_visible_queue_items_ids", len(self.array_visible_queue_items_ids)))

            current_queue_index = self.batch.que.current_queue_index
            if 0 <= current_queue_index < len(self.batch.que.queue_data):
                cur_queue = self.batch.que.queue_data[current_queue_index]
                if self.top_ui is not None:
                    self.top_ui.set_top_info("[{}]   {}".format(cur_queue.id, cur_queue.queue_item_name))
                else:
                    self.batch.logger.err("top_ui is None")

                if current_list_index >= 0:
                    item_c = self.list_queue.item(current_list_index + 1)
                    cur_color = self.batch.sts.state_colors_up[cur_queue.state_id].color()
                    item_c.setBackground(cur_color)

                # update QUE form
                if self.edit_form_state == 1:
                    self.qt_form_edit.update_edit_ui(cur_queue)  # update edit form
            else:
                self.batch.logger.err("on chng list que {} < {}".format(current_queue_index,
                                                                        len(self.batch.que.queue_data)))
