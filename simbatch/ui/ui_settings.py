try:
    from PySide.QtGui import *
except ImportError:
    print "PySide.QtGui ERR"

from widgets import *


class SettingsUI:
    qt_widget_settings = None
    settings = None
    sett_sql_test = None
    comfun = None
    sample_data_state = False
    batch = None
    top_ui = None

    def __init__(self, batch, top_ui):
        settings = batch.s
        self.settings = batch.s
        self.batch = batch
        self.top_ui = top_ui
        self.comfun = batch.comfun

        qt_widget_settings = QWidget()
        self.qt_widget_settings = qt_widget_settings

        qt_lay_settings_main = QVBoxLayout(qt_widget_settings)

        ''' MODE '''
        qt_button_group_data = QButtonGroup()
        qt_radio_group_mode = QGroupBox()
        qt_lay_settings_mode = QHBoxLayout()
        qt_label_mode = QLabel("Data store mode: ")
        qt_lay_settings_mode.addWidget(qt_label_mode)
        qt_button_group_data.setExclusive(True)
        # qt_radio_mode1 = QRadioButton("text")
        # if settings.store_data_mode == 1:
        # qt_radio_mode1.setChecked(True)
        # qt_button_group_data.addButton(qt_radio_mode1)
        # qt_lay_settings_mode.addWidget(qt_radio_mode1)
        qt_radio_mode2 = QRadioButton("json")
        if settings.store_data_mode == 1:
            qt_radio_mode2.setChecked(True)
        qt_button_group_data.addButton(qt_radio_mode2)
        qt_lay_settings_mode.addWidget(qt_radio_mode2)
        qt_radio_mode3 = QRadioButton("MySql")
        if settings.store_data_mode == 2:
            qt_radio_mode3.setChecked(True)
        qt_button_group_data.addButton(qt_radio_mode3)
        qt_lay_settings_mode.addWidget(qt_radio_mode3)

        # qt_radio_mode1.clicked.connect(lambda: self.on_click_radio_data(1))
        qt_radio_mode2.clicked.connect(lambda: self.on_click_radio_data(1))
        qt_radio_mode3.clicked.connect(lambda: self.on_click_radio_data(2))

        ''' DATA '''
        qt_lay_settings_data = QHBoxLayout()
        qt_settings_data_directory_label = QLabel("Data directory : ")
        qt_settings_data_directory_edit = QLineEdit(settings.store_data_json_directory)
        qt_settings_data_directory_button = QPushButton("Get")
        qt_settings_data_directory_button.setToolTip('Select directory for store data')
        qt_settings_data_directory_button.clicked.connect(self.on_click_get_data_dir)

        self.qt_settings_data_directory_edit = qt_settings_data_directory_edit
        qt_lay_settings_data.addWidget(qt_settings_data_directory_label)
        qt_lay_settings_data.addWidget(qt_settings_data_directory_edit)
        qt_lay_settings_data.addWidget(qt_settings_data_directory_button)

        qt_lay_settings_definitions = QHBoxLayout()
        qt_settings_definitions_directory_label = QLabel("Definitions directory : ")
        qt_settings_definitions_directory_edit = QLineEdit(settings.store_definitions_directory)
        qt_settings_definitions_directory_button = QPushButton("Get")
        qt_settings_definitions_directory_button.setToolTip('Select definitions directory')
        qt_settings_definitions_directory_button.clicked.connect(self.on_click_get_definitions_dir)

        self.qt_settings_definitions_directory_edit = qt_settings_definitions_directory_edit
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_label)
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_edit)
        qt_lay_settings_definitions.addWidget(qt_settings_definitions_directory_button)

        qt_lay_settings_mode_data = QVBoxLayout()
        qt_lay_settings_mode_data.addLayout(qt_lay_settings_mode)
        qt_lay_settings_mode_data.addLayout(qt_lay_settings_data)
        qt_lay_settings_mode_data.addLayout(qt_lay_settings_definitions)

        qt_radio_group_mode.setLayout(qt_lay_settings_mode_data)

        ''' MySQL '''
        qt_lay_settings_sql = QFormLayout()

        qt_radio_group_sql = QGroupBox()

        sett_sql_1a = QLabel("host : ")
        sett_sql_1b = QLineEdit(settings.sql[0])
        sett_sql_1b.textChanged.connect(self.on_edit_update_sql_1)
        sett_sql_2a = QLabel("user : ")
        sett_sql_2b = QLineEdit(settings.sql[1])
        sett_sql_2b.textChanged.connect(self.on_edit_update_sql_3)
        sett_sql_3a = QLabel("pass : ")
        sett_sql_3b = QLineEdit(settings.sql[2])
        sett_sql_3b.textChanged.connect(self.on_edit_update_sql_3)
        #   sett_sql_4a = QLabel("port : ") TODO cleanup
        sett_sql_4b = QLineEdit(settings.sql[3])
        sett_sql_4b.textChanged.connect(self.on_edit_update_sql_4)

        sett_sql_4abc = EditLineWithButtons("port : ", edit_text_string=settings.sql[0],
                                            text_on_button_1="  Test MySQL connection  ")

        sett_sql_test = QPushButton("Test MySQL connection")
        sett_sql_test.setFixedWidth(130)
        sett_sql_test.clicked.connect(self.sql_test_connection)

        qt_lay_settings_sql.addRow(sett_sql_1a, sett_sql_1b)
        qt_lay_settings_sql.addRow(sett_sql_2a, sett_sql_2b)
        qt_lay_settings_sql.addRow(sett_sql_3a, sett_sql_3b)
        qt_lay_settings_sql.addRow(sett_sql_4abc.qt_widget_layout)

        qt_radio_group_sql.setTitle("MySQL settigs")
        qt_radio_group_sql.setLayout(qt_lay_settings_sql)

        ''' Users '''
        qt_lay_settings_user = QFormLayout()
        qt_radio_group_user = QGroupBox()
        qt_sett_ser_1a = QLabel("name : ")
        qt_sett_ser_1b = QLineEdit("Markus")
        qt_sett_ser_2a = QLabel("sign : ")
        qt_sett_ser_2b = QLineEdit("M")
        qt_sett_ser_3a = QLabel("pass : ")
        qt_sett_ser_3b = QLineEdit("*")
        qt_sett_ser_4a = QLabel("role : ")
        qt_sett_ser_4b = QLineEdit("admin")

        qt_lay_settings_user.addRow(qt_sett_ser_1a, qt_sett_ser_1b)
        qt_lay_settings_user.addRow(qt_sett_ser_2a, qt_sett_ser_2b)
        qt_lay_settings_user.addRow(qt_sett_ser_3a, qt_sett_ser_3b)
        qt_lay_settings_user.addRow(qt_sett_ser_4a, qt_sett_ser_4b)

        qt_radio_group_user.setTitle("user settings : ")
        qt_radio_group_user.setLayout(qt_lay_settings_user)

        ''' Colors '''
        qt_button_group_colors = QButtonGroup()
        qt_radio_group_colors = QGroupBox()
        qt_lay_settings_colors = QHBoxLayout()

        qt_radio_mode_1 = QRadioButton("grayscale")
        if settings.ui_color_mode == 1:
            qt_radio_mode_1.setChecked(True)
            qt_button_group_colors.addButton(qt_radio_mode_1)
        qt_lay_settings_colors.addWidget(qt_radio_mode_1)
        qt_radio_mode_2 = QRadioButton("pastel")
        if settings.ui_color_mode == 2:
            qt_radio_mode_2.setChecked(True)
            qt_button_group_colors.addButton(qt_radio_mode_2)
        qt_lay_settings_colors.addWidget(qt_radio_mode_2)
        qt_radio_mode_3 = QRadioButton("dark")
        if settings.ui_color_mode == 3:
            qt_radio_mode_3.setChecked(True)
            qt_button_group_colors.addButton(qt_radio_mode_3)
        qt_lay_settings_colors.addWidget(qt_radio_mode_3)
        qt_radio_mode_4 = QRadioButton("custom")
        if settings.ui_color_mode == 4:
            qt_radio_mode_4.setChecked(True)
            qt_button_group_colors.addButton(qt_radio_mode_4)
        qt_lay_settings_colors.addWidget(qt_radio_mode_4)

        qt_radio_group_colors.setTitle("Colors")
        qt_radio_group_colors.setLayout(qt_lay_settings_colors)

        qt_button_group_colors.setExclusive(True)

        qt_radio_mode_1.clicked.connect(lambda: self.on_clicked_radio_colors(1))
        qt_radio_mode_2.clicked.connect(lambda: self.on_clicked_radio_colors(2))
        qt_radio_mode_3.clicked.connect(lambda: self.on_clicked_radio_colors(3))
        qt_radio_mode_4.clicked.connect(lambda: self.on_clicked_radio_colors(4))

        '''  structure '''
        qt_lay_settings_structure = QHBoxLayout()
        qt_radio_group_structure = QGroupBox()
        s1a = QLabel("camera dir : ")
        s1b = QLineEdit("\\\\cam")
        s2a = QLabel("envo dir : ")
        s2b = QLineEdit("\\\\env")
        s3a = QLabel("anim cache : ")
        s3b = QLineEdit("\\\\ani")

        qt_lay_settings_structure.addWidget(s1a)
        qt_lay_settings_structure.addWidget(s1b)
        qt_lay_settings_structure.addWidget(s2a)
        qt_lay_settings_structure.addWidget(s2b)
        qt_lay_settings_structure.addWidget(s3a)
        qt_lay_settings_structure.addWidget(s3b)

        qt_radio_group_structure.setTitle("Structure")
        qt_radio_group_structure.setLayout(qt_lay_settings_structure)

        ''' Info '''
        qt_lay_settings_info = QFormLayout()
        qt_label_info = QLabel(" \n\n             www.simbatch.com ")
        qt_lay_settings_info.addWidget(qt_label_info)

        qt_lay_settings_buttons = QHBoxLayout()

        qt_cb_sample_data = QCheckBox("Create sample data")
        qt_cb_sample_data.stateChanged.connect(self.on_changed_sample_data)
        qt_lay_settings_buttons.addWidget(qt_cb_sample_data)

        qt_button_save = QPushButton("Save")
        qt_button_save.clicked.connect(self.on_click_save_settings)
        qt_lay_settings_buttons.addWidget(qt_button_save)

        qt_lay_settings_main.addWidget(qt_radio_group_mode)
        qt_lay_settings_main.addWidget(qt_radio_group_sql)
        qt_lay_settings_main.addWidget(qt_radio_group_user)
        qt_lay_settings_main.addWidget(qt_radio_group_colors)
        qt_lay_settings_main.addWidget(qt_radio_group_structure)

        qt_lay_settings_main.addItem(QSpacerItem(1, 22))
        qt_lay_settings_main.addLayout(qt_lay_settings_info)
        qt_lay_settings_main.addItem(QSpacerItem(1, 22))
        qt_lay_settings_main.addLayout(qt_lay_settings_buttons)

    def on_click_radio_data(self, index):
        #  PRO version sql
        #  TODO json vs txt
        if self.settings.debug_level <= 4:
            print " [db] on_click_radio_data ", index
        if index > 1:
            # PRO version
            self.top_ui.set_top_info("MySQL only with proversion", 4)

    def on_clicked_radio_colors(self, index):
        if self.settings.debug_level <= 4:
            print " [db] clickedRadioColors ", index
        self.settings.ui_color_mode = index
        self.settings.update_ui_colors()

    def on_changed_sample_data(self, state):
        self.sample_data_state = state

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
        if self.settings.debug_level >= 3:
            print "test conn sql  .... "

    def on_click_get_data_dir(self):
        self.comfun.get_dialog_directory(self.qt_settings_data_directory_edit, QFileDialog)

    def on_click_get_definitions_dir(self):
        self.comfun.get_dialog_directory(self.qt_settings_definitions_directory_edit, QFileDialog)

    def on_click_save_settings(self):
        data_path = str(self.qt_settings_data_directory_edit.text())
        definitions_path = str(self.qt_settings_definitions_directory_edit.text())
        if self.settings.debug_level >= 4:
            print " [db] data_path ", data_path
        if self.comfun.path_exists(data_path, info="Data Path"):
            if self.comfun.path_exists(definitions_path, info="Definitions Path"):
                self.settings.store_data_json_directory = data_path
                self.settings.store_data_backup_directory = data_path + "backup\\"
                self.settings.store_definitions_directory = definitions_path
                self.settings.save_settings()

                if self.sample_data_state:
                    batch = self.batch
                    batch.prj.create_example_project_data(do_save=True)
                    batch.sch.create_example_schemas_data(do_save=True)
                    batch.t.create_example_tasks_data(do_save=True)
                    # batch.q.createSampleData(taskID, projID)  # TODO
                    # batch.n.createSampleData()  # TODO
                    if self.settings.debug_level >= 3:
                        print " [INF] created sample data: ", data_path
            else:
                print " [ERR] wrong definitions path !!!"
        else:
            print " [ERR] wrong data path !!!"




