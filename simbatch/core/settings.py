import os
import json
from random import randint
from lib.common import CommonFunctions

try:  # Maya 2016
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        print "PySide not found"
        class QBrush:
            def __init__(self, q):
                pass
        class QColor:
            @classmethod
            def fromRgb(self, r, g, b, a=""):
                pass


class Settings:
    logger = None                   # logger prints errors, warnings, info and db to console and to log file
    ini_file = None                 # fundamental config file, json format
    loading_state = 0               # check fundamental config.ini
    settings_err_info = ""          # store last err/wrn when loading config.ini
    json_settings_data = None       # basic config data

    # fundamental settings (config.ini)
    current_os = -1                             # 1 Linux, 2 windoza   detected on __init__ or forced by force_os
    dir_separator = ""                          # set on __init__   depend on  current_os
    store_data_mode = None                      # 1 json     2 MySQL (PRO version)
    debug_level = None                          # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    store_data_json_directory = None            # dir basic config settings (def:config.ini)
    store_data_json_directory_abs = None        # dir basic config settings (def:config.ini)
    store_data_backup_directory = None          # dir backup data
    store_data_backup_directory_abs = None      # dir backup data
    store_definitions_directory = None          # dir with software, actions, engines and param definitions
    store_definitions_directory_abs = None      # dir with software, actions, engines and param definitions
    installation_directory_abs = None           # dir used for update simnodes core (they can be independent)
    store_abs_dir = ""                          #
    sql = [None, None, None, None]              # "db"  "pass" "port" "user" (PRO version)
    admin_user = None                           # PRO version

    # predefined settings
    SIMBATCH_VERSION = "v0.2.50"   # current version
    JSON_PROJECTS_FILE_NAME = "data_projects.json"
    JSON_SCHEMAS_FILE_NAME = "data_schemas.json"
    JSON_TASKS_FILE_NAME = "data_tasks.json"
    JSON_QUEUE_FILE_NAME = "data_queue.json"
    JSON_SIMNODES_FILE_NAME = "data_simnodes.json"

    states_visible_names = {}

    INDEX_STATE_NULL = 0
    INDEX_STATE_INIT = 1
    INDEX_STATE_WAITING = 2
    INDEX_STATE_QUEUED = 3
    INDEX_STATE_WORKING = 4
    INDEX_STATE_SIM = 5
    INDEX_STATE_CACHE = 6
    INDEX_STATE_RENDER = 7
    INDEX_STATE_HOLD = 8
    INDEX_STATE_ERROR = 9
    INDEX_STATE_OK = 10
    INDEX_STATE_DONE = 11
    INDEX_STATE_REVIEW = 12
    INDEX_STATE_ACCEPTED = 13
    INDEX_STATE_REJECTED = 14

    INDEX_STATE_CUSTOM = 18
    INDEX_STATE_OFFLINE = 19
    INDEX_STATE_INACTIVE = 20
    INDEX_STATE_SUSPEND = 21
    INDEX_STATE_ACTIVE = 22
    INDEX_STATE_DEFAULT = 23

    states_visible_names[INDEX_STATE_NULL] = "NULL"
    states_visible_names[INDEX_STATE_INIT] = "INIT"
    states_visible_names[INDEX_STATE_WAITING] = "WAITING"
    states_visible_names[INDEX_STATE_QUEUED] = "QUEUED"
    states_visible_names[INDEX_STATE_WORKING] = "WORKING"
    states_visible_names[INDEX_STATE_SIM] = "SIM"
    states_visible_names[INDEX_STATE_CACHE] = "CACHE"
    states_visible_names[INDEX_STATE_RENDER] = "RENDER"
    states_visible_names[INDEX_STATE_ERROR] = "ERROR"
    states_visible_names[INDEX_STATE_HOLD] = "HOLD"
    states_visible_names[INDEX_STATE_OK] = "OK"
    states_visible_names[INDEX_STATE_DONE] = "DONE"
    states_visible_names[INDEX_STATE_REVIEW] = "REVIEW"
    states_visible_names[INDEX_STATE_ACCEPTED] = "ACCEPTED"
    states_visible_names[INDEX_STATE_REJECTED] = "REJECTED"

    states_visible_names[INDEX_STATE_CUSTOM] = "CUSTOM"
    states_visible_names[INDEX_STATE_OFFLINE] = "OFFLINE"
    states_visible_names[INDEX_STATE_INACTIVE] = "INACTIVE"
    states_visible_names[INDEX_STATE_SUSPEND] = "SUSPEND"        # TODO decide SUSPEND or SUSPENDED ?
    states_visible_names[INDEX_STATE_ACTIVE] = "ACTIVE"
    states_visible_names[INDEX_STATE_DEFAULT] = "DEFAULT"

    # GUI settings
    runtime_env = ""        # runtime environment as software name display on frame and set active definition
    ui_edition_mode = 0     # 0 open source    1 Pro version (with Wizard tab as first)
    ui_color_mode = 1       # color palette    1 gray,  2 pastel,  3 dark,  4 custom
    ui_brightness_mode = 1  # 0 dark mode  1 light mode
    state_colors = []       # item list colors
    state_colors_up = []    # selected item list colors
    window = None           # store def window position
    always_on_top = False   # obvious obviousness
    force_start_tab = 0     # if > 0 show tab with this index after run

    # check screen resolution: protect window position (outside screen if second monitor is off)
    CHECK_SCREEN_RES_ON_START = 1
    WITH_GUI = 1  # loading color schema # TODO auto detect
    COLORS_PASTEL_FILE_NAME = "colors_pastel.ini"
    COLORS_CUSTOM_FILE_NAME = "colors_custom.ini"
    COLORS_GRAY_FILE_NAME = "colors_gray.ini"
    COLORS_DARK_FILE_NAME = "colors_dark.ini"

    default_settings = {"! json info":
                        {"config": "this is fundamental config file", "format": "more about format: http://json.org"},
                        "dataMode":
                            {"current": 1, "modes": "1-json, 2-MySQL"},
                        "colorMode":
                            {"current": 2, "levels": "1 gray,  2 pastel,  3 dark,  4 custom  "},
                        "debugLevel":
                            {"current": 4, "levels": "1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL "},
                        "storeData":
                            {"dataDirectory": "/server/simbatch/dataDir/",
                             "backupDirectory": "/server/simbatch/backups/",
                             "definitionsDirectory": "/server/simbatch/definitions/"},
                        "sql":
                            {"db": "127.0.1.220", "user": "default", "pass": "default", "port": "3306"},
                        "adminUser":
                            {"name": "admin", "sign": "A", "pass": "pass"},
                        "window":
                            {"posX": 70, "posY": 150, "sizeX": 600, "sizeY": 800, "alwaysOnTop": False}
                        }

    def __init__(self, logger, runtime_env, ini_path="", ini_file="", force_os=False):
        self.logger = logger
        if force_os is False:
            if os.name == "posix":
                self.current_os = 1
            else:
                self.current_os = 2
        else:
            self.current_os = force_os
        if self.current_os == 1:
            self.dir_separator = "/"
        else:
            self.dir_separator = "\\"

        """  STANDALONE """
        # self.store_abs_dir = os.path.abspath("") + self.dir_separator  # os.path.dirname(os.path.realpath(__file__))
        self.store_abs_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + self.dir_separator
                              # + "data" + self.dir_separator

        """  MAYA win  C:\Program Files\Autodesk\Maya2014\ """
        # TODO check abs

        self.comfun = CommonFunctions()
        self.runtime_env = runtime_env
        self.ini_file = self.get_ini_file_and_path(ini_path, ini_file)

        """ check and force DEV config """
        if self.comfun.file_exists(os.path.join(os.path.dirname(self.ini_file), "config_dev.ini"), info=False):
            self.ini_file = os.path.join(os.path.dirname(self.ini_file), "config_dev.ini")
            self.logger.inf(("force DEV config:", self.ini_file), nl=True)

        self.sql = [None, None, None, None]
        self.clear_state_colors()

        self.load_settings()

        if self.loading_state >= 4:
            if self.WITH_GUI == 1:
                self.update_ui_colors()
        else:
            self.logger.err(("Settings not loaded !!!", self.loading_state))

    def print_all(self):
        print " loading_state: ", self.loading_state
        print " ini_file: ", self.ini_file
        print " runtime_env: ", self.runtime_env

        if self.json_settings_data is not None:
            if "dataMode" in self.json_settings_data:
                print " json_settings_data[dataMode][current]: ", self.json_settings_data["dataMode"]["current"]
            else:
                self.logger.err(("MISSING dataMode KEY IN SETTINGS FILE:", self.ini_file))
            if "colorMode" in self.json_settings_data:
                print " json_settings_data[colorMode][current]: ", self.json_settings_data["colorMode"]["current"]
            else:
                self.logger.err(("MISSING colorMode KEY IN SETTINGS FILE:", self.ini_file))
            if "debugLevel" in self.json_settings_data:
                print " json_settings_data[debugLevel][current]: ", self.json_settings_data["debugLevel"]["current"]
            else:
                self.logger.err(("MISSING debugLevel KEY IN SETTINGS FILE:", self.ini_file))
            if "window" in self.json_settings_data:
                print " json_settings_data[window]: ", self.json_settings_data["window"]
            else:
                self.logger.err(("MISSING window KEY IN SETTINGS FILE:", self.ini_file))

        print " store_data_mode: ", self.store_data_mode
        print " debug_level: ", self.debug_level
        print " store_data_json_directory: ", self.store_data_json_directory
        if self.store_data_json_directory != self.store_data_json_directory_abs:
            print " store_data_json_directory_abs: ", self.store_data_json_directory_abs
        print " store_data_backup_directory: ", self.store_data_backup_directory
        if self.store_data_backup_directory != self.store_data_backup_directory_abs:
            print " store_data_backup_directory_abs: ", self.store_data_backup_directory_abs
        print " store_definitions_directory: ", self.store_definitions_directory
        if self.store_definitions_directory != self.store_definitions_directory_abs:
            print " store_definitions_directory_abs: ", self.store_definitions_directory_abs
        print " sql settings: ", self.sql
        print " admin_user: ", self.admin_user
        print " window:", self.window

        print "\n\n"

    @staticmethod
    def random_welcome_message():
        messages = ("Welcome", "Have a nice sim!", "Sim, Forrest, sim!")
        rand = randint(0, len(messages)-1)
        return messages[rand]

    def clear_state_colors(self):
        self.state_colors = []
        self.state_colors_up = []
        for i in range(0, 40):
            self.state_colors.append(QBrush(QColor.fromRgb(40, 40, 40, a=255)))
            self.state_colors_up.append(QBrush(QColor.fromRgb(140, 140, 140, a=255)))

    """  get absolute path config file using relative or empty path/file  """
    def get_ini_file_and_path(self, ini_path="", ini_file="", check_is_exists=True):
        if ini_file == "":
            if ini_path != "tests":
                ini_file = "config.ini"
            else:
                ini_file = "config_tests.ini"
        if self.comfun.is_absolute(ini_file):
            ini_file_and_path = ini_file
        else:
            if ini_path == "":
                check_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + self.dir_separator
                ini_file_and_path = check_ini_path + ini_file
                if check_is_exists:
                    if self.comfun.file_exists(check_ini_path + ini_file) is False:
                        self.logger.err((" CONFIG FILE NOT EXIST:", (check_ini_path + ini_file)))
            else:
                if ini_path == "tests":
                    check_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    check_ini_path = os.path.dirname(check_ini_path) + self.dir_separator + "tests"   # cd ../tests
                    check_ini_path += self.dir_separator
                    ini_file_and_path = check_ini_path + ini_file
                    if check_is_exists:
                        if self.comfun.file_exists(check_ini_path + ini_file) is False:
                            self.logger.err((" CONFIG FILE FOR TESTS NOT EXIST:", (check_ini_path + ini_file)))
                else:
                    ini_file_and_path = ini_path + ini_file
                    if check_is_exists:
                        if self.comfun.is_absolute(ini_path):
                            if self.comfun.path_exists(ini_path):
                                if self.comfun.file_exists(ini_path + ini_file) is False:
                                    self.logger.err(("CONFIG FILE DO NOT EXIST IN CUSTOM PATH:", (ini_path + ini_file)))
                                else:
                                    pass   # the config file happily exists :)
                            else:
                                self.logger.err((" CONFIG PATH DO NOT EXIST:", ini_path))
                        else:
                            self.logger.err((" CONFIG PATH IS NOT ABSOLUTE:", ini_path))
            if self.comfun.is_absolute(ini_path):
                ini_file_and_path = ini_path + ini_file
        return ini_file_and_path

    def update_absolute_directories(self):
        data_path = self.store_data_json_directory

        if len(data_path) == 0:
            self.store_data_json_directory_abs = ""
        else:
            if self.comfun.is_absolute(data_path):
                if data_path[-1:] == "\\" or data_path[-1:] == "/":
                    self.store_data_json_directory_abs = data_path
                    self.store_data_backup_directory_abs = data_path + "backup" + self.dir_separator
                else:
                    self.store_data_json_directory = data_path + self.dir_separator
                    self.store_data_json_directory_abs = data_path + self.dir_separator
                    self.store_data_backup_directory_abs = data_path + self.dir_separator + "backup" + \
                                                           self.dir_separator
            else:
                if data_path[-1:] == "\\" or data_path[-1:] == "/":
                    self.store_data_json_directory_abs = self.store_abs_dir + data_path
                    self.store_data_backup_directory_abs = self.store_abs_dir + data_path + "backup" + \
                                                           self.dir_separator
                else:
                    self.store_data_json_directory_abs = self.store_abs_dir + data_path + self.dir_separator
                    self.store_data_backup_directory_abs = self.store_abs_dir + data_path + self.dir_separator + \
                                                           "backup" + self.dir_separator

        definitions_path = self.store_definitions_directory
        if len(definitions_path) == 0:
            self.store_definitions_directory_abs = ""
        else:
            if self.comfun.is_absolute(definitions_path):
                if definitions_path[-1:] == "\\" or definitions_path[-1:] == "/":
                    self.store_definitions_directory_abs = definitions_path
                else:
                    self.store_definitions_directory = definitions_path + self.dir_separator
                    self.store_definitions_directory_abs = definitions_path + self.dir_separator
            else:
                if definitions_path[-1:] == "\\" or definitions_path[-1:] == "/":
                    self.store_definitions_directory_abs = self.store_abs_dir + self.store_definitions_directory
                else:
                    self.store_definitions_directory_abs = self.store_abs_dir + self.store_definitions_directory + \
                                                           self.dir_separator

    def load_settings(self):
        self.settings_err_info = ""
        if self.comfun.file_exists(self.ini_file, info="settings init"):
            self.loading_state = 1
            with open(self.ini_file) as f:
                try:
                    self.json_settings_data = json.load(f)
                except IOError:
                    print " [ERR] json.load(f) exception ", f
                    pass
                ret = self.check_data_integration()
                if ret:
                    self.debug_level = self.json_settings_data["debugLevel"]["current"]
                    self.store_data_mode = self.json_settings_data["dataMode"]["current"]
                    self.ui_color_mode = self.json_settings_data["colorMode"]["current"]

                    self.store_data_json_directory = self.json_settings_data["storeData"]["dataDirectory"]
                    self.store_data_backup_directory = self.json_settings_data["storeData"]["backupDirectory"]
                    self.store_definitions_directory = self.json_settings_data["storeData"]["definitionsDirectory"]

                    self.update_absolute_directories()

                    s1 = self.json_settings_data["sql"]["db"]
                    s2 = self.json_settings_data["sql"]["user"]
                    s3 = self.json_settings_data["sql"]["pass"]
                    s4 = self.json_settings_data["sql"]["port"]
                    # self.sql = self.json_settings_data["sql"].values()
                    self.sql = (s1, s2, s3, s4)
                    self.admin_user = self.json_settings_data["adminUser"].values()  # TODO order  values()
                    wnd = self.json_settings_data["window"]
                    self.window = [wnd["posX"], wnd["posY"], wnd["sizeX"], wnd["sizeY"]]
                    self.always_on_top = wnd["alwaysOnTop"]
                    
                    if "simnodes" in self.json_settings_data:
                        simnodes = self.json_settings_data["simnodes"]
                        if "master_source" in simnodes:
                            self.installation_directory_abs = simnodes["master_source"]

                    if "startup" in self.json_settings_data.keys():
                        if "tab" in self.json_settings_data["startup"].keys():
                            self.force_start_tab = self.json_settings_data["startup"]["tab"]
                            self.logger.inf("forced startup tab index: {}".format(self.force_start_tab))

                    if self.comfun.can_get_int(self.store_data_mode):
                        if self.store_data_mode == 1:
                            if self.comfun.path_exists(self.store_data_json_directory_abs) is False:
                                if len(self.store_data_json_directory_abs) == 0:
                                    self.settings_err_info = "Data directory not defined!"
                                else:
                                    self.settings_err_info = "Data directory not exists!   (" + \
                                                             self.store_data_json_directory_abs + ")"
                            elif self.comfun.path_exists(self.store_definitions_directory_abs) is False:
                                if len(self.store_definitions_directory_abs) == 0:
                                    self.settings_err_info = "Definitions directory not defined!"
                                else:
                                    self.settings_err_info = "Definitions directory not exists!"
                            else:
                                """ SETTINGS VALUES ARE OK"""
                                self.loading_state = 4
                                if self.debug_level >= 3:
                                    self.logger.inf(("settings loaded ", self.ini_file))
                                return True

                        elif self.store_data_mode == 2:
                            # PRO VERSION
                            self.loading_state = 3
                            self.settings_err_info = "MySQL will be supported with the PRO version"
                        else:
                            self.loading_state = 3
                            self.settings_err_info = "Store data mode: {} incorrect value".format(self.store_data_mode)
                else:
                    print " [WRN] json data inconsistency:", self.ini_file
                    self.loading_state = 2
        else:
            self.settings_err_info = " [ERR] config.ini file not exists: {}".format(self.ini_file)
            self.loading_state = -1

        print self.settings_err_info
        return False

    def save_settings(self, settings_file=""):
        comfun = self.comfun
        data_path = self.store_data_json_directory_abs

        self.default_settings["dataMode"]["current"] = self.store_data_mode
        self.default_settings["colorMode"]["current"] = self.ui_color_mode
        self.default_settings["debugLevel"]["current"] = self.debug_level
        self.default_settings["storeData"]["dataDirectory"] = self.store_data_json_directory
        self.default_settings["storeData"]["backupDirectory"] = self.store_data_backup_directory
        self.default_settings["storeData"]["definitionsDirectory"] = self.store_definitions_directory
        self.default_settings["sql"]["db"] = self.sql[0]   # PRO VERSION
        self.default_settings["sql"]["user"] = self.sql[1]    # PRO VERSION
        self.default_settings["sql"]["pass"] = self.sql[2]    # PRO VERSION
        self.default_settings["sql"]["port"] = self.sql[3]    # PRO VERSION
        self.default_settings["window"]["posX"] = self.window[0]
        self.default_settings["window"]["posY"] = self.window[1]
        self.default_settings["window"]["sizeX"] = self.window[2]
        self.default_settings["window"]["sizeY"] = self.window[3]
        self.default_settings["window"]["alwaysOnTop"] = self.always_on_top

        if len(settings_file) == 0:
            settings_file = self.ini_file  # JSON format
        comfun.save_to_file(settings_file, json.dumps(self.default_settings, indent=2, sort_keys=True), nl_at_end=True)
        self.logger.inf(("settings saved to: ", settings_file))

        if self.store_data_mode == 1:
            if comfun.file_exists(data_path + self.JSON_PROJECTS_FILE_NAME) is False:
                comfun.create_empty_file(data_path + self.JSON_PROJECTS_FILE_NAME)
            if comfun.file_exists(data_path + self.JSON_SCHEMAS_FILE_NAME) is False:
                comfun.create_empty_file(data_path + self.JSON_SCHEMAS_FILE_NAME)
            if comfun.file_exists(data_path + self.JSON_TASKS_FILE_NAME) is False:
                comfun.create_empty_file(data_path + self.JSON_TASKS_FILE_NAME)
            if comfun.file_exists(data_path + self.JSON_QUEUE_FILE_NAME) is False:
                comfun.create_empty_file(data_path + self.JSON_QUEUE_FILE_NAME)
            if comfun.file_exists(data_path + self.JSON_SIMNODES_FILE_NAME) is False:
                comfun.create_empty_file(data_path + self.JSON_SIMNODES_FILE_NAME)

    def check_data_integration(self):
        #  out = json.dumps(self.json_settings_data, indent=2)  TODO cleanup
        jd = self.json_settings_data
        json_keys = ["dataMode", "debugLevel", "storeData", "sql", "adminUser", "window"]
        errors = 0
        if self.json_settings_data is not None:
            for k in json_keys:
                if (k in jd) is False:
                    self.logger.err(("missing key: ", k))
                    errors += 1
        else:
            return False

        if errors == 0:
            return True
        else:
            self.logger.err("found {} errors in config file".format(errors ))
            return False

    def update_ui_colors(self):
        if self.store_definitions_directory_abs is not None:
            palette_id = self.ui_color_mode
            if palette_id == 1:
                color_file = self.store_definitions_directory_abs + "colors" + self.dir_separator + \
                             self.COLORS_GRAY_FILE_NAME
            elif palette_id == 2:
                color_file = self.store_definitions_directory_abs + "colors" + self.dir_separator + \
                             self.COLORS_PASTEL_FILE_NAME
            elif palette_id == 3:
                color_file = self.store_definitions_directory_abs + "colors" + self.dir_separator + \
                             self.COLORS_DARK_FILE_NAME
            else:
                #  palette_id == 4:
                color_file = self.store_definitions_directory_abs + "colors" + self.dir_separator + \
                             self.COLORS_CUSTOM_FILE_NAME

            if self.comfun.file_exists(color_file, info="colors file"):
                self.clear_state_colors()
                f = open(color_file, 'r')
                for li_counter, line in enumerate(f.readlines()):
                    li = line.split(";")
                    if len(li) > 7:
                        self.state_colors[li_counter] = QBrush(
                            QColor.fromRgb(self.comfun.int_or_val(li[2], 40), self.comfun.int_or_val(li[3], 40),
                                           self.comfun.int_or_val(li[4], 40), a=255))
                        self.state_colors_up[li_counter] = QBrush(
                            QColor.fromRgb(self.comfun.int_or_val(li[6], 140), self.comfun.int_or_val(li[7], 140),
                                           self.comfun.int_or_val(li[8], 140), a=255))
                f.close()

                if self.debug_level >= 3:
                    self.logger.inf(("loaded colors: ", color_file))
                return True
            else:
                for i in range(0, 40):
                    self.state_colors.append(QBrush(QColor.fromRgb(40, 40, 40, a=255)))
                    self.state_colors_up.append(QBrush(QColor.fromRgb(140, 140, 140, a=255)))

                if self.debug_level >= 3:
                    self.logger.wrn(("NOT loaded colors: ", color_file))
                return False
        else:
            self.logger.wrn("store_definitions_directory  is None")
            return False
