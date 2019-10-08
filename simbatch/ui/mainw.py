import ctypes, sys, errno

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        print 'PySide import ERROR!  Please install PySide or PySide2'
        sys.exit(errno.EACCES)

from ui_wizard import WizardUI
from ui_projects import ProjectsUI
from ui_schemas import SchemasUI
from ui_tasks import TasksUI
from ui_queue import QueueUI
from ui_nodes import NodesUI
from ui_settings import SettingsUI
from ui_definitions import DefinitionsUI


class TopMenuUI:
    qt_lay_top_menu = None
    instance = None
    batch = None

    qt_but_debug = None
    qt_but_filter = None
    qt_but_refresh = None
    qt_but_print_general = None
    qt_but_print_details = None

    current_top_info_mode = 1

    def __init__(self, layout, instance, batch):
        self.batch = batch
        qt_lay_top_menu = QHBoxLayout()
        self.qt_lay_top_menu = qt_lay_top_menu
        self.instance = instance
        layout.addLayout(qt_lay_top_menu)

        qt_lbl_info = QLabel("info")
        qt_font = QFont()
        qt_font.setPointSize(10)
        qt_font.setBold(True)
        qt_font.setFamily("Veranda")
        qt_lbl_info.setFont(qt_font)
        self.qt_lbl_info = qt_lbl_info
        qt_lbl_info.setStyleSheet("""border: 0px solid white;padding-left:7px;""")

        if self.batch.comfun.is_int(self.batch.sts.window[2]):
            if self.batch.sts.window[2] > 330:
                qt_lbl_info.setMaximumWidth(self.batch.sts.window[2] - 130)
            else:
                qt_lbl_info.setMaximumWidth(200)
        else:
            qt_lbl_info.setMaximumWidth(220)  # TODO dynamic size

        qt_lay_top_menu.addWidget(qt_lbl_info)

        qt_lay_top_menu.addStretch(1)

        qt_but_print_general = QPushButton("I")
        qt_but_print_general.setMinimumSize(22, 22)
        qt_but_print_general.setMaximumSize(22, 22)
        qt_lay_top_menu.addWidget(qt_but_print_general)
        self.qt_but_print_general = qt_but_print_general

        qt_but_print_details = QPushButton("I+")
        qt_but_print_details.setMinimumSize(22, 22)
        qt_but_print_details.setMaximumSize(22, 22)
        qt_lay_top_menu.addWidget(qt_but_print_details)
        if self.batch.sts.debug_level < 4:            # hide debug button
            qt_but_print_details.hide()
        self.qt_but_print_details = qt_but_print_details

        qt_but_debug = QPushButton("[db]")
        qt_but_debug.setMinimumSize(22, 22)
        qt_but_debug.setMaximumSize(22, 22)
        qt_lay_top_menu.addWidget(qt_but_debug)
        if self.batch.sts.debug_level < 4:            # hide debug button
            qt_but_debug.hide()
        self.qt_but_debug = qt_but_debug

        qt_but_filter_1 = QPushButton("F1")
        qt_but_filter_1.setMinimumSize(22, 22)
        qt_but_filter_1.setMaximumSize(22, 22)
        qt_lay_top_menu.addWidget(qt_but_filter_1)
        self.qt_but_filter_1 = qt_but_filter_1

        qt_but_filter_2 = QPushButton("F2")
        qt_but_filter_2.setMinimumSize(22, 22)
        qt_but_filter_2.setMaximumSize(22, 22)
        qt_lay_top_menu.addWidget(qt_but_filter_2)
        self.qt_but_filter_2 = qt_but_filter_2

        qt_but_refresh = QPushButton("R")
        qt_but_refresh.setMinimumSize(22, 22)
        qt_but_refresh.setMaximumSize(22, 22)
        qt_lay_top_menu.addWidget(qt_but_refresh)
        self.qt_but_refresh = qt_but_refresh

    def set_top_info(self, txt, mode=1, limit=0):  # 1 normal ...  9 error
        if type(txt) is tuple:
            txt = "  ".join([str(el) for el in txt])
        if mode > 1:
            txt = "    " + txt + "      "
        else:
            txt = "  " + txt
        if limit > 0:
            if len(txt) > limit:
                txt = txt[:limit] + "  ..."
        self.qt_lbl_info.setText(txt)
        if self.current_top_info_mode != mode:
            if self.batch.sts.ui_brightness_mode == 1:
                if mode < 6:
                    self.qt_lbl_info.setStyleSheet("")
                if mode == 7:
                    self.qt_lbl_info.setStyleSheet("""color:#000000;background-color:#ffdc1a;""")
                if mode == 8:
                    self.qt_lbl_info.setStyleSheet("""color:#000000;background-color:#ffa722;""")
                if mode == 9:
                    self.qt_lbl_info.setStyleSheet("""color:#000000;background-color:#ff4422;""")
            else:
                if mode < 6:
                    self.qt_lbl_info.setStyleSheet("")
                if mode == 7:
                    self.qt_lbl_info.setStyleSheet("""background-color:#f2dc1a;""")
                if mode == 8:
                    self.qt_lbl_info.setStyleSheet("""background-color:#ffa722;""")
                if mode == 9:
                    self.qt_lbl_info.setStyleSheet("""background-color:#ff4422;""")
        self.current_top_info_mode = mode


class MainWindow(QMainWindow):
    batch = None
    server = None
    comfun = None
    debug_level = None

    top_ui = None
    wiz_ui = None
    pro_ui = None
    sch_ui = None
    tsk_ui = None
    que_ui = None
    nod_ui = None
    set_ui = None
    dfn_ui = None

    qt_tab_widget = None

    filter_state_1 = False
    filter_state_2 = False
    current_filters = None

    def __init__(self, server, parent=None):
        super(MainWindow, self).__init__(parent)
        self.server = server
        self.batch = server.batch
        self.comfun = server.batch.comfun
        self.sts = server.batch.sts
        self.debug_level = server.batch.sts.debug_level
        self.init_sts_colors()
        self.init_ui(server.batch)

        self.connect(QShortcut(QKeySequence(Qt.Key_R), self), SIGNAL('activated()'), self.on_clicked_but_refresh)
        self.connect(QShortcut(QKeySequence(Qt.Key_W), self), SIGNAL('activated()'), self.on_shortcut_set_waiting)
        self.connect(QShortcut(QKeySequence(Qt.Key_D), self), SIGNAL('activated()'), self.on_shortcut_set_done)
        self.connect(QShortcut(QKeySequence(Qt.Key_A), self), SIGNAL('activated()'), self.on_shortcut_set_accepted)
        self.connect(QShortcut(QKeySequence(Qt.Key_H), self), SIGNAL('activated()'), self.on_shortcut_set_hold)
        self.connect(QShortcut(QKeySequence(Qt.Key_X), self), SIGNAL('activated()'), self.on_shortcut_delete)
        self.connect(QShortcut(QKeySequence(Qt.Key_Y), self), SIGNAL('activated()'), self.on_shortcut_yes)

    def init_ui(self, batch):
        current_screen_width = 800
        current_screen_height = 600
        if self.sts.current_os == 1:
            try:
                app = QApplication.instance()
                screen_resolution = app.desktop().screenGeometry()
                current_screen_width = screen_resolution.width() + screen_resolution.left()
                current_screen_height = screen_resolution.height() + screen_resolution.top()
                if app.desktop().numScreens() >= 2:
                    self.batch.logger.inf(("numScreens detected: ", app.desktop().numScreens()))
                    screen_0 = app.desktop().availableGeometry(screen=0)
                    screen_1 = app.desktop().availableGeometry(screen=1)
                    screen_0_w = screen_0.width() + screen_0.left()
                    screen_1_w = screen_1.width() + screen_1.left()
                    current_screen_width = max(screen_0_w,  screen_1_w)
                    self.batch.logger.inf(("current width: ", screen_resolution.width(), screen_resolution.left()))
                    current_screen_height = screen_resolution.height() + screen_resolution.top()
            except RuntimeError:
                pass   # TODO multi screen
        if self.sts.current_os == 2:
            user32 = ctypes.windll.user32
            current_screen_width = user32.GetSystemMetrics(78)    # SM_CXVIRTUALSCREEN
            current_screen_height = user32.GetSystemMetrics(79)   # SM_CYVIRTUALSCREEN

        wnd = self.sts.window
        if wnd is not None and len(wnd) == 4:
            x_wnd_pos = wnd[0]
            y_wnd_pos = wnd[1]
            if self.sts.CHECK_SCREEN_RES_ON_START == 1:
                if wnd[0] > current_screen_width - 130:
                    x_wnd_pos = 220
                    self.batch.logger.inf("reset window position X ({}) ({})".format(wnd[0], current_screen_width))
                if wnd[1] > current_screen_height - 130:
                    y_wnd_pos = 70
                    self.batch.logger.inf("reset window position Y ({}) ({})".format(wnd[1], current_screen_height))
            else:
                x_wnd_pos = wnd[0]
                y_wnd_pos = wnd[1]
            self.batch.logger.inf(("set wind pos :", x_wnd_pos, y_wnd_pos,  wnd[2],  wnd[3]))
            self.setGeometry(x_wnd_pos, y_wnd_pos, wnd[2], wnd[3])
        else:
            self.setMinimumSize(480, 700)
            self.sts.window = [40, 40, 480, 700]

        if self.sts.runtime_env == "Houdini":
            self.setStyleSheet("background-color: rgb(42, 44, 45);")    # uicolor

        self.setWindowTitle("SimBatch " + self.sts.SIMBATCH_VERSION + "     " + self.sts.runtime_env)
        if self.sts.always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        qt_central_widget = QWidget(self)
        self.setCentralWidget(qt_central_widget)
        qt_lay_central = QVBoxLayout(qt_central_widget)
        qt_lay_central.setContentsMargins(0, 0, 0, 0)

        top = TopMenuUI(qt_lay_central, self, batch)
        top.qt_but_print_general.clicked.connect(self.on_clicked_but_print_general)
        top.qt_but_print_details.clicked.connect(self.on_clicked_but_print_details)
        top.qt_but_debug.clicked.connect(self.on_clicked_but_debug)
        top.qt_but_filter_1.clicked.connect(self.on_clicked_but_filter_1)
        top.qt_but_filter_2.clicked.connect(self.on_clicked_but_filter_2)
        top.qt_but_refresh.clicked.connect(self.on_clicked_but_refresh)

        self.top_ui = top
        self.wiz_ui = WizardUI(batch, self, top)        # PRO version
        self.pro_ui = ProjectsUI(batch, self, top)
        self.sch_ui = SchemasUI(batch, self, top)
        self.tsk_ui = TasksUI(batch, self, top)
        self.que_ui = QueueUI(batch, self, top)
        self.nod_ui = NodesUI(batch, self, top)
        self.dfn_ui = DefinitionsUI(batch, self, top)
        self.set_ui = SettingsUI(batch, self, top)

        #

        #  TABs
        #  TABs   TABs
        #  TABs   TABs   TABs
        qt_tab_widget = QTabWidget(self)
        self.qt_tab_widget = qt_tab_widget

        # qt_tab_widget.addTab(self.wiz_ui.qt_widget_wizard, "Wizard")       # PRO version
        qt_tab_widget.addTab(self.pro_ui.qt_widget_projects, "Projects")
        qt_tab_widget.addTab(self.sch_ui.qt_widget_schema, "Schemas")
        qt_tab_widget.addTab(self.tsk_ui.qt_widget_tasks, "Tasks")
        qt_tab_widget.addTab(self.que_ui.qt_widget_queue, "Queue")
        qt_tab_widget.addTab(self.nod_ui.qt_widget_nodes, "Sim Nodes")
        qt_tab_widget.addTab(self.dfn_ui.qt_widget_definitions, "Definitions")
        qt_tab_widget.addTab(self.set_ui.qt_widget_settings, "Settings")
        qt_tab_widget.setMinimumSize(220, 400)

        if self.sts.loading_state >= 4:
            """ force start tab index by settings """
            if self.sts.force_start_tab > 0:
                qt_tab_widget.setCurrentIndex(self.sts.force_start_tab)
            else:
                """ STANDARD START TAB """
                if self.sts.ui_edition_mode == 0:
                    qt_tab_widget.setCurrentIndex(2)
                else:
                    qt_tab_widget.setCurrentIndex(3)  # PRO version with Wizard tab
        else:
            """ settings not loaded properly """
            if self.sts.ui_edition_mode == 0:
                qt_tab_widget.setCurrentIndex(6)  # wrong config data: show settings
            else:
                qt_tab_widget.setCurrentIndex(7)  # wrong config data: show settings  (PRO version)

        qt_lay_central.addWidget(qt_tab_widget)
        qt_central_widget.setLayout(qt_lay_central)
        qt_tab_widget.currentChanged.connect(self.on_tab_change)

        # status after init main window and load settings and data
        if self.sts.loading_state < 4:
            top.set_top_info("Settings loaded not properly", 7)
            self.batch.logger.wrn(("Settings loaded not properly", self.sts.loading_state, self.sts.settings_err_info))
        else:
            self.batch.logger.inf("Settings and data loaded\n\n")

    def rbg_to_brush(self, r, g, b):
        return QBrush(QColor.fromRgb(r, g, b, a=255))
        
    def init_sts_colors(self):
        self.sts.default_gray_brush = self.rbg_to_brush(40, 40, 40)
        self.sts.default_light_gray_brush = self.rbg_to_brush(140, 140, 140)
        self.sts.init_colors(self.rbg_to_brush)
        self.sts.update_ui_colors()
    
    def post_run(self, loading_data_state):  # show welcome message or error info
        if loading_data_state[0] is True:
            self.top_ui.set_top_info(self.batch.sts.random_welcome_message())
        elif loading_data_state[0] is False:
            self.top_ui.set_top_info(self.sts.settings_err_info, 6)
        else:
            if loading_data_state[0] > 1:
                self.top_ui.set_top_info(("Loaded with errors ({}): {}".format(loading_data_state[0],
                                          loading_data_state[1])), 7)
            else:
                self.top_ui.set_top_info("Loading error. {}".format(loading_data_state[1]), 7)

        if len(self.batch.logger.err_buffer) > 0:
            self.batch.logger.raw("///////  List of all ERRORS during loading  :", nl=True, force_print=True)
            self.batch.logger.print_err_buffer()
            self.batch.logger.clear_err_buffer()

        if self.batch.prj.current_project_index is not None:
            item = self.pro_ui.qt_list_projects.item(self.batch.prj.current_project_index+1)
            self.pro_ui.qt_list_projects.setCurrentItem(item)

    def on_tab_change(self, tab):
        self.batch.logger.db(("tab change:", tab, self.qt_tab_widget.tabText(tab)))
        # if tab==3:
        #     if self.que_ui.qt_list_item is not None:
        #         self.que_ui.qt_list_item

    def on_clicked_but_print_general(self):
        self.batch.print_important_values()

    def on_clicked_but_print_details(self):
        self.batch.print_current_detailed_values(self.qt_tab_widget.currentIndex())  # valid for: P C T Q N D S

    def on_clicked_but_debug(self):
        self.batch.logger.inf("but_debug clicked")
        self.batch.logger.inf(self.batch.logger.console_level)
        self.batch.logger.inf(self.batch.sts.logger.console_level)

    def on_clicked_but_filter_1(self):
        self.batch.logger.inf("but_filter clicked")
        if self.filter_state_1:
            self.filter_state_1 = False
            filters = None
        else:
            if self.batch.tsk.current_task is None:
                self.batch.logger.wrn("no task selected")
                self.top_ui.set_top_info("no task selected", 7)
                filters = None
            else:
                self.filter_state_1 = True
                filters = [[1, self.batch.tsk.current_task.schema_id],[0]]       # TODO  filters class
                if self.filter_state_2:
                    self.filter_state_2 = False

        self.current_filters = filters

        self.tsk_ui.reset_list(filters=filters)

    def on_clicked_but_filter_2(self):
        self.batch.logger.inf("but_filter clicked")
        if self.filter_state_2:
            self.filter_state_2 = False
            filters = None
        else:
            if self.batch.tsk.current_task is None:
                self.batch.logger.wrn("no task selected")
                self.top_ui.set_top_info("no task selected", 7)
                filters = None
            else:
                self.filter_state_2 = True
                filters = [[0],[1, self.batch.tsk.current_task.sequence, self.batch.tsk.current_task.shot, self.batch.tsk.current_task.take]]
                if self.filter_state_1:
                    self.filter_state_1 = False

        self.current_filters = filters

        self.tsk_ui.reset_list(filters=filters)

    def on_clicked_but_refresh(self):
        self.batch.logger.inf("but_refresh clicked")
        self.sts.update_ui_colors()
        ret = self.refresh_ui_with_reload_data()
        if ret is True:
            self.top_ui.set_top_info("Refreshed", 1)
        elif ret is False:
            self.top_ui.set_top_info("NOT REFRESHED PROPERLY (see log)!", 8)
        else:
            self.top_ui.set_top_info("Refreshed with errors: ({})".format(ret), 7)
        # TODO update debug level

    def on_shortcut_delete(self):
        if self.qt_tab_widget.currentIndex() == 2:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut R) delete active task")
            self.tsk_ui.on_click_show_remove_form()
        if self.qt_tab_widget.currentIndex() == 3:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut R) delete active queue item")
            self.que_ui.on_click_remove()

    def on_shortcut_set_done(self):
        if self.qt_tab_widget.currentIndex() == 2:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut D) set DONE state")
            self.tsk_ui.on_click_menu_set_done()
        if self.qt_tab_widget.currentIndex() == 3:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut D) set DONE state")
            self.que_ui.on_click_menu_set_done()

    def on_shortcut_set_accepted(self):
        if self.qt_tab_widget.currentIndex() == 3:   # valid for: Q
            self.batch.logger.inf("(shotcut A) set ACCEPTED state")
            self.que_ui.on_click_menu_set_accepted()

    def on_shortcut_set_waiting(self):
        if self.qt_tab_widget.currentIndex() == 3:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut W) set WAITING state")
            self.que_ui.on_click_menu_set_waiting()

    def on_shortcut_set_hold(self):
        if self.qt_tab_widget.currentIndex() == 2:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut H) set HOLD state")
            self.tsk_ui.on_click_menu_set_hold()
        if self.qt_tab_widget.currentIndex() == 3:   # valid for: P C T Q N D S
            self.batch.logger.inf("(shotcut H) set HOLD state")
            self.que_ui.on_click_menu_set_hold()

    def on_shortcut_yes(self):
        if self.qt_tab_widget.currentIndex() == 2:  # valid for: P C T Q N D S
            if self.tsk_ui.remove_form_state == 1:
                self.tsk_ui.qt_form_remove.hide()
                self.tsk_ui.remove_form_state = 0
                self.tsk_ui.on_click_confirmed_remove_task()
        if self.qt_tab_widget.currentIndex() == 3:  # valid for: P C T Q N D S
            if self.que_ui.remove_form_state == 1:
                self.que_ui.qt_form_remove.hide()
                self.que_ui.remove_form_state = 0
                self.que_ui.on_click_confirmed_remove_queue_item()

    def resizeEvent(self, event):            # PySide  resizeEvent
        self.on_resize_window(event)

    def on_resize_window(self, event):
        new_size = event.size()
        if self.sts.window is not None:       # if None settings not loaded
            self.sts.window[2] = new_size.width()
            self.sts.window[3] = new_size.height()
            self.set_ui.resize_settings_widget(self.sts.window[2])

    def moveEvent(self, event):              # PySide  moveEvent
        self.on_move_window(event)

    def on_move_window(self, event):
        new_pos = event.pos()
        if self.sts.window is not None:      # if None settings not loaded
            self.sts.window[0] = new_pos.x()
            self.sts.window[1] = new_pos.y()

    def refresh_ui_with_reload_data(self):
        self.batch.logger.inf("reload PROJECTS")
        self.pro_ui.reload_projects_data_and_refresh_list()
        self.pro_ui.hide_all_forms()

        self.batch.logger.inf("reload SCHEMAS")
        self.sch_ui.reload_schemas_data_and_refresh_list()

        self.batch.logger.inf("reload DEFINITIONS")
        cur_index = self.batch.dfn.current_definition_index
        ret = self.batch.dfn.reload_definitions()
        self.batch.dfn.current_definition_index = cur_index
        self.sch_ui.schema_form_create.refresh_actions_ui()
        self.sch_ui.hide_all_forms()

        self.batch.logger.inf("reload TASKS")
        self.tsk_ui.reload_tasks_data_and_refresh_list(filters=self.current_filters)
        self.tsk_ui.hide_all_forms()

        self.batch.logger.inf("reload QUEUE")
        self.que_ui.reload_queue_data_and_refresh_list()

        self.batch.logger.inf("reload SIMNODES")
        self.nod_ui.reload_simnodes_data_and_refresh_list()

        return ret
