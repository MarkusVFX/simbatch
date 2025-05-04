try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    raise Exception('PySide import ERROR!  Please install PySide or PySide2')

from .widgets import *
import os


class SettingsUI:
    qt_widget_settings = None
    qt_scroll_widget = None
    settings = None
    sett_sql_test = None
    comfun = None
    sample_data_state = False
    batch = None
    top_ui = None
    scroll_margin = 26       # scroll child widget margin, used on init and resize

    def __init__(self, batch, mainw, top_ui):
        settings = batch.sts
        self.settings = batch.sts
        self.batch = batch
        self.mainw = mainw
        self.top_ui = top_ui
        self.comfun = batch.comfun

        qt_widget_settings = QWidget()
        self.qt_widget_settings = qt_widget_settings
        qt_scroll_area = QScrollArea()
        qt_lay_scroll_and_buttons = QVBoxLayout()  # layout for  scroll   and   bottom buttons
        qt_lay_scroll_and_buttons.addWidget(qt_scroll_area)
        qt_widget_settings.setLayout(qt_lay_scroll_and_buttons)
        qt_lay_scroll_and_buttons.setContentsMargins(0, 0, 0, 0)

        qt_lay_settings_main = QVBoxLayout()      # layout for all settings group boxes
        qt_scroll_widget = QWidget()
        self.qt_scroll_widget = qt_scroll_widget

        if settings.window is not None:
            qt_scroll_widget.setMinimumWidth(settings.window[2]-self.scroll_margin)
        else:
            qt_scroll_widget.setMinimumWidth(400)

        if self.settings.runtime_env == "Maya":
            qt_scroll_widget.setMinimumHeight(560)
        if self.settings.runtime_env == "Houdini":
            qt_scroll_widget.setMinimumHeight(760)
        else:
            qt_scroll_widget.setMinimumHeight(650)

        qt_scroll_area.setWidget(qt_scroll_widget)
        qt_scroll_widget.setLayout(qt_lay_settings_main)

        ''' CONFIG FILE '''
        qt_lay_config_ini = QVBoxLayout()
        qt_group_config_ini = QGroupBox()
        qt_group_config_ini.setTitle("Config file:")
        if self.settings.current_os == 1:
            show_ini_file = settings.ini_file
        else:
            show_ini_file = self.comfun.convert_to_win_path(settings.ini_file)
        err_info_config_ini = SimpleLabel("")   #  err info hidden on start
        self.err_info_config_ini = err_info_config_ini
        err_info_config_ini.hide()
        elwb_config_ini = EditLineWithButtons(show_ini_file, edit_text_string=None, text_on_button_1="Test Config",
                                              text_on_button_2="Test Access") # , button_width=85)

        elwb_config_ini.button_1.clicked.connect(self.test_data_config_ini)
        elwb_config_ini.button_2.clicked.connect(self.test_access_config_ini)
        qt_lay_config_ini.addLayout(elwb_config_ini.qt_widget_layout)
        qt_lay_config_ini.addLayout(err_info_config_ini.qt_widget_layout)
        qt_group_config_ini.setLayout(qt_lay_config_ini)

        ''' DATA OPTIONS  '''
        qt_group_data_options = QGroupBox()
        qt_group_data_options.setTitle("Data options")
        qt_lay_settings_mode = QHBoxLayout()
        qt_label_mode = QLabel("Data store mode: ")
        qt_lay_settings_mode.addWidget(qt_label_mode)

        qt_radio_mode1 = QRadioButton("json")
        if settings.store_data_mode == 1:
            qt_radio_mode1.setChecked(True)
        qt_lay_settings_mode.addWidget(qt_radio_mode1)
        qt_radio_mode1.clicked.connect(lambda: self.on_click_radio_data(1))

        qt_radio_mode2 = QRadioButton("MySQL")
        if settings.store_data_mode == 2:
            qt_radio_mode2.setChecked(True)
        qt_lay_settings_mode.addWidget(qt_radio_mode2)
        qt_radio_mode2.clicked.connect(lambda: self.on_click_radio_data(2))

        qt_group_data_options.setLayout(qt_lay_settings_mode)


        ''' DATA DIRECTORY '''
        qt_group_data_directory = QGroupBox()
        qt_lay_settings_data = QHBoxLayout()
        qt_settings_data_directory_label = QLabel("Database directory : ")

        if self.settings.current_os == 1:
            show_store_data_json_directory = settings.store_data_json_directory
        else:
            show_store_data_json_directory = self.comfun.convert_to_win_path(settings.store_data_json_directory)
        qt_settings_data_directory_edit = QLineEdit(show_store_data_json_directory)  # TODO   EditLineWithButtons
        qt_settings_data_directory_button = QPushButton("Get")  # TODO   EditLineWithButtons
        qt_settings_data_directory_test_button = QPushButton("Test")  # TODO   EditLineWithButtons
        # qt_settings_data_directory_button.setFixedWidth(40)  # TODO     Houdini no padding     if self.settings.runtime_env
        # qt_settings_data_directory_test_button.setFixedWidth(50)  # TODO     Houdini no padding  if self.settings.runtime_env
        qt_settings_data_directory_button.setToolTip('Select directory for store data')
        qt_settings_data_directory_button.clicked.connect(self.on_click_get_data_dir)
        qt_settings_data_directory_test_button.clicked.connect(self.on_click_test_data_dir)

        self.qt_settings_data_directory_edit = qt_settings_data_directory_edit
        qt_settings_data_directory_edit.textChanged.connect(self.on_change_data_dir)
        qt_lay_settings_data.addWidget(qt_settings_data_directory_label)
        qt_lay_settings_data.addWidget(qt_settings_data_directory_edit)
        qt_lay_settings_data.addWidget(qt_settings_data_directory_button)
        qt_lay_settings_data.addWidget(qt_settings_data_directory_test_button)

        qt_group_data_directory.setLayout(qt_lay_settings_data)


        ''' DEFINITIONS DIRECTORY '''
        qt_group_definitions_directory = QGroupBox() 
        qt_lay_settings_definitions = QHBoxLayout()
        qt_settings_definitions_directory_label = QLabel("Definitions directory : ")

        if self.settings.current_os == 1:
            show_store_definitions_directory = settings.store_definitions_directory
        else:
            show_store_definitions_directory = self.comfun.convert_to_win_path(settings.store_definitions_directory)
        qt_settings_definitions_directory_edit = QLineEdit(show_store_definitions_directory)
        qt_settings_definitions_directory_button = QPushButton("Get")  # TODO   EditLineWithButtons
        qt_settings_definitions_directory_test_button = QPushButton("Test")  # TODO   EditLineWithButtons

        # qt_settings_definitions_directory_button.setFixedWidth(40)  # TODO     Houdini no padding   if self.settings.runtime_env
        # qt_settings_definitions_directory_test_button.setFixedWidth(50)  # TODO   Houdini no padding   if self.settings.runtime_env
        qt_settings_definitions_directory_button.setToolTip('Select definitions directory')
        qt_settings_definitions_directory_button.clicked.connect(self.on_click_get_definitions_dir)
        qt_settings_definitions_directory_test_button.clicked.connect(self.on_click_test_definitions_dir)

        self.qt_settings_definitions_directory_edit = qt_settings_definitions_directory_edit
        qt_settings_definitions_directory_edit.textChanged.connect(self.on_change_definitions_dir)
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_label)
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_edit)
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_button)
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_test_button)
        
        qt_group_definitions_directory.setLayout(qt_lay_settings_definitions)


        ''' EXAMPLE DATA '''
        qt_group_example_data = QGroupBox()
        qt_lay_settings_buttons_data = QHBoxLayout()
        qt_settings_create_example_data_button = QPushButton("Create example data")
        qt_settings_clear_all_data_button = QPushButton("Clear all data")
        qt_lay_settings_buttons_data.addWidget(qt_settings_create_example_data_button)
        qt_lay_settings_buttons_data.addWidget(qt_settings_clear_all_data_button)
        qt_settings_create_example_data_button.clicked.connect(self.on_click_create_example_data)
        qt_settings_clear_all_data_button.clicked.connect(self.on_click_clear_all_data)

        qt_group_example_data.setLayout(qt_lay_settings_buttons_data)


        ''' MySQL '''
        qt_lay_settings_sql = QFormLayout()
        qt_radio_group_sql = QGroupBox()
        qt_radio_group_sql.setTitle("MySQL settings (available in the Pro version)")
        qt_radio_group_sql.setEnabled(False)

        sett_sql_1a = QLabel("host : ")
        sett_sql_1b = QLineEdit(settings.sql[0])
        sett_sql_1b.textChanged.connect(self.on_edit_update_sql_1)
        sett_sql_2a = QLabel("user : ")
        sett_sql_2b = QLineEdit(settings.sql[1])
        sett_sql_2b.textChanged.connect(self.on_edit_update_sql_3)
        sett_sql_3a = QLabel("pass : ")
        sett_sql_3b = QLineEdit(settings.sql[2])
        sett_sql_3b.textChanged.connect(self.on_edit_update_sql_3)
        # sett_sql_4a = QLabel("port : ") TODO cleanup
        # sett_sql_4b = QLineEdit(settings.sql[3])
        # sett_sql_4b.textChanged.connect(self.on_edit_update_sql_4)
        sett_sql_4abc = EditLineWithButtons("port : ", edit_text_string=settings.sql[3],
                                            text_on_button_1="  Test MySQL connection  ")

        # sett_sql_test = QPushButton("Test MySQL connection")
        # sett_sql_test.setFixedWidth(130)
        # sett_sql_test.clicked.connect(self.sql_test_connection)

        qt_lay_settings_sql.addRow(sett_sql_1a, sett_sql_1b)
        qt_lay_settings_sql.addRow(sett_sql_2a, sett_sql_2b)  # PRO version
        qt_lay_settings_sql.addRow(sett_sql_3a, sett_sql_3b)  # PRO version
        qt_lay_settings_sql.addRow(sett_sql_4abc.qt_widget_layout)  # PRO version

        qt_radio_group_sql.setLayout(qt_lay_settings_sql)  # PRO version

        ''' Users '''
        qt_lay_settings_user = QFormLayout()
        qt_radio_group_user = QGroupBox()

        qt_radio_group_user.setTitle("User settings (available in the Pro version)")
        qt_radio_group_user.setEnabled(False)

        qt_sett_ser_1a = QLabel("name : ")
        qt_sett_ser_1b = QLineEdit("Markus")
        qt_sett_ser_2a = QLabel("sign : ")
        qt_sett_ser_2b = QLineEdit("M")
        qt_sett_ser_3a = QLabel("pass : ")
        qt_sett_ser_3b = QLineEdit("*")
        qt_sett_ser_4a = QLabel("role : ")
        qt_sett_ser_4b = QLineEdit("admin")

        qt_lay_settings_user.addRow(qt_sett_ser_1a, qt_sett_ser_1b)   # PRO version
        qt_lay_settings_user.addRow(qt_sett_ser_2a, qt_sett_ser_2b)   # PRO version
        qt_lay_settings_user.addRow(qt_sett_ser_3a, qt_sett_ser_3b)   # PRO version
        qt_lay_settings_user.addRow(qt_sett_ser_4a, qt_sett_ser_4b)   # PRO version

        qt_radio_group_user.setLayout(qt_lay_settings_user)   # PRO version

        ''' Colors '''
        #qt_button_group_colors = QButtonGroup()
        qt_radio_group_colors = QGroupBox()
        qt_radio_group_colors.setTitle("Colors")
        qt_lay_settings_colors = QHBoxLayout()

        qt_radio_mode_1 = QRadioButton("grayscale")
        if settings.ui_color_mode == 1:
            qt_radio_mode_1.setChecked(True)
        qt_lay_settings_colors.addWidget(qt_radio_mode_1)
        qt_radio_mode_2 = QRadioButton("pastel")
        if settings.ui_color_mode == 2:
            qt_radio_mode_2.setChecked(True)
        qt_lay_settings_colors.addWidget(qt_radio_mode_2)
        qt_radio_mode_3 = QRadioButton("dark")
        if settings.ui_color_mode == 3:
            qt_radio_mode_3.setChecked(True)
        qt_lay_settings_colors.addWidget(qt_radio_mode_3)
        qt_radio_mode_4 = QRadioButton("custom")
        if settings.ui_color_mode == 4:
            qt_radio_mode_4.setChecked(True)
        qt_lay_settings_colors.addWidget(qt_radio_mode_4)

        qt_radio_group_colors.setLayout(qt_lay_settings_colors)

        qt_radio_mode_1.clicked.connect(lambda: self.on_clicked_radio_colors(1))
        qt_radio_mode_2.clicked.connect(lambda: self.on_clicked_radio_colors(2))
        qt_radio_mode_3.clicked.connect(lambda: self.on_clicked_radio_colors(3))
        qt_radio_mode_4.clicked.connect(lambda: self.on_clicked_radio_colors(4))

        ''' Debug level '''
        qt_button_group_debug_level = QButtonGroup()
        qt_radio_group_debug_level = QGroupBox()
        qt_radio_group_debug_level.setTitle("Debug level")
        qt_lay_settings_debug_level = QHBoxLayout()

        qt_radio_mode_db_1 = QRadioButton("only ERR")
        if settings.debug_level == 1:
            qt_radio_mode_db_1.setChecked(True)
        qt_button_group_debug_level.addButton(qt_radio_mode_db_1)
        qt_lay_settings_debug_level.addWidget(qt_radio_mode_db_1)
        qt_radio_mode_db_2 = QRadioButton("+WRN")
        if settings.debug_level == 2:
            qt_radio_mode_db_2.setChecked(True)
        qt_button_group_debug_level.addButton(qt_radio_mode_db_2)
        qt_lay_settings_debug_level.addWidget(qt_radio_mode_db_2)
        qt_radio_mode_db_3 = QRadioButton("+INF")
        if settings.debug_level == 3:
            qt_radio_mode_db_3.setChecked(True)
        qt_button_group_debug_level.addButton(qt_radio_mode_db_3)
        qt_lay_settings_debug_level.addWidget(qt_radio_mode_db_3)
        qt_radio_mode_db_4 = QRadioButton("+DB")
        if settings.debug_level == 4:
            qt_radio_mode_db_4.setChecked(True)
        qt_button_group_debug_level.addButton(qt_radio_mode_db_4)
        qt_lay_settings_debug_level.addWidget(qt_radio_mode_db_4)
        qt_radio_mode_db_5 = QRadioButton("+DEEP")
        if settings.debug_level == 5:
            qt_radio_mode_db_5.setChecked(True)
        qt_button_group_debug_level.addButton(qt_radio_mode_db_5)
        qt_lay_settings_debug_level.addWidget(qt_radio_mode_db_5)
        qt_radio_mode_db_6 = QRadioButton("ALL")
        if settings.debug_level == 6:
            qt_radio_mode_db_6.setChecked(True)
        qt_button_group_debug_level.addButton(qt_radio_mode_db_6)
        qt_lay_settings_debug_level.addWidget(qt_radio_mode_db_6)

        qt_radio_group_debug_level.setLayout(qt_lay_settings_debug_level)

        qt_button_group_debug_level.setExclusive(True)

        qt_radio_mode_db_1.clicked.connect(lambda: self.on_clicked_radio_debug_level(1))
        qt_radio_mode_db_2.clicked.connect(lambda: self.on_clicked_radio_debug_level(2))
        qt_radio_mode_db_3.clicked.connect(lambda: self.on_clicked_radio_debug_level(3))
        qt_radio_mode_db_4.clicked.connect(lambda: self.on_clicked_radio_debug_level(4))
        qt_radio_mode_db_5.clicked.connect(lambda: self.on_clicked_radio_debug_level(5))
        qt_radio_mode_db_6.clicked.connect(lambda: self.on_clicked_radio_debug_level(6))

        ''' Info '''
        qt_lay_settings_info = QFormLayout()
        qt_radio_group_info = QGroupBox()
        qt_radio_group_info.setTitle("Support and updates")
        qt_label_info = QLabel("              www.simbatch.com ")
        qt_lay_settings_info.addWidget(qt_label_info)
        qt_radio_group_info.setLayout(qt_lay_settings_info)

        ''' Settings bottom buttons '''
        qt_lay_settings_buttons = QHBoxLayout()
        qt_lay_settings_buttons.setContentsMargins(40, 4, 40, 13)

        qt_cb_always_on_top = QCheckBox("Always on top")
        if settings.always_on_top:
            qt_cb_always_on_top.setChecked(True)
        qt_cb_always_on_top.stateChanged.connect(self.on_changed_always_on_top)
        qt_lay_settings_buttons.addWidget(qt_cb_always_on_top)
        
        qt_cb_save_pos = QCheckBox("Save pos and size")
        if settings.save_window_position:
            qt_cb_save_pos.setChecked(True)
        qt_cb_save_pos.stateChanged.connect(self.on_changed_save_window_position)
        qt_lay_settings_buttons.addWidget(qt_cb_save_pos)
        self.qt_cb_save_pos = qt_cb_save_pos

        qt_button_save = QPushButton("Save")
        qt_button_save.clicked.connect(self.on_click_save_settings)
        qt_lay_settings_buttons.addWidget(qt_button_save)

        ''' Add all QGroupBoxes to  qt_scroll_widget  '''
        qt_lay_settings_main.addWidget(qt_group_config_ini)
        qt_lay_settings_main.addWidget(qt_group_data_options)
        qt_lay_settings_main.addWidget(qt_group_data_directory)
        qt_lay_settings_main.addWidget(qt_group_definitions_directory)
        qt_lay_settings_main.addWidget(qt_group_example_data)
        qt_lay_settings_main.addWidget(qt_radio_group_colors)
        qt_lay_settings_main.addWidget(qt_radio_group_debug_level)
        # qt_lay_settings_main.addWidget(qt_radio_group_sql)   # PRO version
        # qt_lay_settings_main.addWidget(qt_radio_group_user)   # PRO version
        qt_lay_settings_main.addWidget(qt_radio_group_info)
        qt_lay_settings_main.addItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))

        qt_lay_scroll_and_buttons.addLayout(qt_lay_settings_buttons)

    def pack_into_extra_widget(self, object):
        extra = QWidget()
        lay = QVBoxLayout()
        lay.addWidget(object)
        extra.setLayout(lay)
        extra.setMinimumHeight(200)
        return extra

    def test_data_config_ini(self):
        if self.test_exist_config_ini():
            ini = self.comfun.load_from_file(self.settings.ini_file)
            self.batch.logger.inf(("RAW config: ", ini))

            ini_content = self.comfun.load_json_file(self.settings.ini_file)
            ini_file = "{} is writable ".format(os.path.basename(self.settings.ini_file))
            vars_count = 0
            if ini_content is not None:
                ini_elements = ["colorMode", "dataMode", "debugLevel", "sql", "storeData", "window"]
                for ie in ini_elements:
                    if ie in ini_content.keys():
                        vars_count += 1
                    else:
                        self.batch.logger.err(("missing key in config file ", ie))
                if vars_count == len(ini_elements):
                    self.top_ui.set_top_info(ini_file+" integrity test OK ", 4)
                else:
                    self.top_ui.set_top_info(ini_file+" missing keys, more info in log ", 8)
            else:
                self.top_ui.set_top_info(ini_file+" wrong format ! ", 8)

    def test_access_config_ini(self):
        if self.test_exist_config_ini():
            ret_W = os.access(self.settings.ini_file, os.W_OK)
            if ret_W:
                info = "{} is writable ".format(os.path.basename(self.settings.ini_file))
                self.top_ui.set_top_info(info, 4)
                self.batch.logger.inf(info+self.settings.ini_file)
            else:
                ret_R = os.access(self.settings.ini_file, os.R_OK)
                if ret_R:
                    self.top_ui.set_top_info("config.ini is read only", 4)
                    self.batch.logger.inf("config.ini is read only")
                else:
                    self.top_ui.set_top_info("No access to config.ini", 7)
                    self.batch.logger.inf("No access to config.ini")

    def test_exist_config_ini(self):
        ret_d = self.comfun.path_exists(self.comfun.get_path_from_full(self.settings.ini_file), info="config.ini dir")
        if ret_d:
            ret_f = self.comfun.file_exists(self.settings.ini_file, info="config.ini")
            if ret_f:
                info = "{} exist ".format(os.path.basename(self.settings.ini_file))
                self.top_ui.set_top_info(info, 4)
                self.batch.logger.inf(info)
                return True
            else:
                info = "{} file not exist ! ".format(os.path.basename(self.settings.ini_file))
                self.top_ui.set_top_info(info, 9)
                self.batch.logger.wrn(info)
                self.err_info_config_ini.show("Please initialize SimBatch with proper startup configuration file")
                return False

        else:
            self.top_ui.set_top_info("config.ini dir not exist !", 9)
            self.batch.logger.wrn(("config.ini dir not exist !   ", self.settings.ini_file,
                                   self.comfun.get_path_from_full(self.settings.ini_file)))
            self.err_info_config_ini.show("Please initialize SimBatch with proper startup config file")
            return False

    def on_click_test_data_dir(self):
        if self.comfun.path_exists(self.batch.sts.store_data_json_directory_abs):
            acces_test = self.comfun.test_directory_access(self.batch.sts.store_data_json_directory_abs, "Database")
            if acces_test[1]:
                self.top_ui.set_top_info("Database dir is writable !", 1)
            else:
                self.top_ui.set_top_info("Database dir is not writable !", 9)
        else:
            self.top_ui.set_top_info("Database directory not exist !", 9)
            self.batch.logger.wrn(("Database dir not exist! ({})".format(self.batch.sts.store_data_json_directory_abs)))

    def on_click_test_definitions_dir(self):
        test_dir = self.batch.sts.store_definitions_directory_abs
        if self.comfun.path_exists(test_dir):
            if self.comfun.test_directory_access(test_dir, "Definitons" )[1]:
                self.top_ui.set_top_info("Definitons is writable !", 1)
            else:
                self.top_ui.set_top_info("Definitons is not writable !", 9)
        else:
            self.top_ui.set_top_info("Definitons directory not exist !", 9)
            self.batch.logger.wrn(("Definitons dir not exist! ({})".format(test_dir)))

    def on_click_radio_data(self, index):
        #  PRO version sql
        #  TODO json vs txt
        self.batch.logger.db(("on_click_radio_data ", index))

        if index > 1:
            # PRO version
            self.top_ui.set_top_info("MySQL will be supported with the PRO version", 7)
            self.batch.logger.inf("MySQL will be supported with the PRO version")
        else:
            self.top_ui.set_top_info("JSON data mode is active :)", 4)
            self.batch.logger.inf("JSON data mode is active")

    def on_change_data_dir(self, txt):
        self.batch.logger.deepdb(("on_change_data_dir: ", txt))
        self.batch.sts.store_data_json_directory = txt
        self.batch.sts.update_absolute_directories()

    def on_change_definitions_dir(self, txt):
        self.batch.logger.deepdb(("on_change_data_dir: ", txt))
        self.batch.sts.store_definitions_directory = txt
        self.batch.sts.update_absolute_directories()

    def on_clicked_radio_colors(self, index):
        self.batch.logger.db(("on_clicked_radio_colors ", index))

        self.settings.ui_color_mode = index
        self.settings.update_ui_colors()
        self.mainw.refresh_ui_with_reload_data()

    def on_clicked_radio_debug_level(self, level):
        prev_lvl = self.settings.debug_level
        self.settings.debug_level = level
        self.batch.logger.console_level = level
        self.batch.logger.db(("on_clicked_debug_level", level))
        if level >= 4 and prev_lvl < 4:     # show db UI elements
            self.mainw.top_ui.qt_but_print_general.show()
            self.mainw.top_ui.qt_but_print_details.show()
            self.mainw.top_ui.qt_but_debug.show()
        if level < 4 and prev_lvl >= 4:      # hide db UI elements
            self.mainw.top_ui.qt_but_print_general.hide()
            self.mainw.top_ui.qt_but_print_details.hide()
            self.mainw.top_ui.qt_but_debug.hide()

    def on_changed_always_on_top(self, state):   # state values 0 or 2  !
        if state:
            self.settings.always_on_top = True
            self.mainw.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.mainw.show()
        else:
            self.settings.always_on_top = False
            self.mainw.setWindowFlags(self.mainw.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.mainw.show()

    def on_edit_update_sql_1(self, txt):
        self.settings.mysql_host = txt

    def on_edit_update_sql_2(self, txt):
        self.settings.mysql_user = txt

    def on_edit_update_sql_3(self, txt):
        self.settings.mysql_pass = txt

    def on_edit_update_sql_4(self, txt):
        self.settings.mysql_port = txt

    def sql_test_connection(self):
        #  PRO version
        self.batch.logger.db("test conn sql  .... ")

    def on_click_get_data_dir(self):
        self.comfun.get_dialog_directory(self.qt_settings_data_directory_edit, QFileDialog)

    def on_click_get_definitions_dir(self):
        self.comfun.get_dialog_directory(self.qt_settings_definitions_directory_edit, QFileDialog)

    def on_click_create_example_data(self):
        batch = self.batch
        if len(self.batch.sts.store_data_json_directory_abs) == 0:
            self.batch.logger.wrn("Sample not created, directory not defined!")
            self.top_ui.set_top_info("Sample not created, directory not defined!", 7)
        else:
            batch.sio.create_data_directory_if_not_exist()
            if self.comfun.path_exists(self.batch.sts.store_data_json_directory_abs) is True:
                batch.sio.create_example_data()
                self.mainw.refresh_ui_with_reload_data()
            else:
                msg = "Sample not created, directory {} not exists".format(self.batch.sts.store_data_json_directory)
                self.batch.logger.wrn(msg)
                self.top_ui.set_top_info(msg, 7)

        if len(self.batch.sts.store_definitions_directory_abs) == 0:
            self.batch.logger.wrn("Sample definition not created, directory not defined!")
            self.top_ui.set_top_info("Sample definition not created, directory not defined!", 7)
        else:
            if self.comfun.path_exists(self.batch.sts.store_definitions_directory_abs) is False:
                self.comfun.create_directory(self.batch.sts.store_definitions_directory_abs)
            if self.comfun.path_exists(self.batch.sts.store_definitions_directory_abs) is True:

                batch.dfn.create_example_definition(do_save=True)
                self.batch.logger.inf("Created sample definition")
            else:
                sdda = self.batch.sts.store_definitions_directory_abs
                msg = "Definition not created, directory {} not exists".format(sdda)
                self.batch.logger.wrn(msg)
                self.top_ui.set_top_info(msg, 7)

    def on_click_clear_all_data(self):
        batch = self.batch
        ret = batch.sio.create_data_directory_if_not_exist()
        if ret:
            batch.prj.clear_all_projects_data(clear_stored_data=True)
            batch.sch.clear_all_schemas_data(clear_stored_data=True)
            batch.tsk.clear_all_tasks_data(clear_stored_data=True)
            batch.que.clear_all_queue_items(clear_stored_data=True)
            batch.nod.clear_all_nodes_data(clear_stored_data=True)
            # batch.que.clearSampleData(taskID, projID)  # TODO
            # batch.nod.clearSampleData()
            self.batch.logger.inf("Cleared sample data")
            self.mainw.refresh_ui_with_reload_data()
        else:
            self.batch.logger.wrn("Data directory NOT exist. Can NOT create data directory!")
            self.top_ui.set_top_info("Can NOT create data directory!", 7)

    def resize_settings_widget(self, val):
        self.qt_scroll_widget.setMinimumWidth(val-self.scroll_margin)
        self.qt_scroll_widget.setMaximumWidth(val-self.scroll_margin)

    def on_click_save_settings(self):
        data_path = str(self.qt_settings_data_directory_edit.text())
        if len(data_path) == 0:
            self.batch.logger.wrn(" data path is empty, please fill path or select directory")
            self.top_ui.set_top_info("data path is empty, please select directory ", 7)
            return False
        definitions_path = str(self.qt_settings_definitions_directory_edit.text())
        if len(definitions_path) == 0:
            self.batch.logger.wrn(" definitions path is empty, please fill path or pick directory")
            self.top_ui.set_top_info("definitions path is empty, please select directory", 7)
            return False

        # self.batch.logger.db(("Save data path :", data_path))
        if self.comfun.path_exists(self.settings.store_data_json_directory_abs) is False:
            self.comfun.create_directory(self.settings.store_data_json_directory_abs)
        if self.comfun.path_exists(self.settings.store_definitions_directory_abs) is False:
            self.comfun.create_directory(self.settings.store_definitions_directory_abs)
        if self.comfun.path_exists(self.settings.store_data_json_directory_abs, info="Data Path"):
            if self.comfun.path_exists(self.settings.store_definitions_directory_abs, info="Definitions Path"):
                # self.settings.store_data_json_directory = data_path
                # self.settings.store_definitions_directory = definitions_path
                # self.batch.sts.update_absolute_directories()
                ret = self.settings.save_settings()
                if ret is False:
                    self.top_ui.set_top_info("Settings NOT saved!", 9)
                    self.batch.logger.err(("Settings NOT saved ! ".format(self.settings.ini_file)))
            else:
                self.batch.logger.err(("Wrong definitions path, directory not exist  :", definitions_path))
        else:
            self.batch.logger.err((" Wrong data path, directory not exist :", data_path))
        self.resize_settings_widget(self.settings.window[2])

    def on_changed_save_window_position(self, state):   # state values 0 or 2  !
        if state == 0:
            self.settings.save_window_position = False
        elif state == 2:
            self.settings.save_window_position = True
        else:
            self.batch.logger.wrn("unknown state on_changed_save_window_position : " + str(state))
