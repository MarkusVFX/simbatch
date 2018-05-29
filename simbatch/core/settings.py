import os
import json
from random import randint
from common import CommonFunctions

try:  # Maya 2016
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        print "PySide import ERROR"


class Settings:
    logger = None                   # logger prints errors, warnings, info and db to console and to log file
    ini_file = None                 # fundamental config file, json format
    loading_state = 0               # check fundamental config # TODO data loading and GUI init
    json_settings_data = None       # basic config data

    # fundamental settings (config.ini)
    current_os = -1                             # 1 Linux, 2 windoza   detected on __init__ or forced by force_os
    dir_separator = ""                          # set on __init__   depend on  current_os
    store_data_mode = None                      # 1 json     2 MySQL (PRO version)
    debug_level = None                          # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    store_data_json_directory = None            # dir basic config settings (def:config.ini)
    store_data_backup_directory = None          # dir backup data
    store_definitions_directory = None          # dir with software, actions, engines and param definitions
    sql = [None, None, None, None]              # "db"  "pass" "port" "user" (PRO version)
    admin_user = None                           # PRO version

    # predefined settings
    SIMBATCH_VERSION = "v0.2.18"   # current version
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
    ui_edition_mode = 0     # 0 open source    1 Pro
    ui_color_mode = 1       # color palette    1 gray,  2 pastel,  3 dark,  4 custom
    ui_brightness_mode = 1  # 0 dark mode  1 light mode
    state_colors = []       # item list colors
    state_colors_up = []    # selected item list colors
    window = None           # store def window position
    always_on_top = False   # obvious obviousness
    force_start_tab = 5     # if > 0 show tab with this index after run

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
                            {"dataDirectory": "\\\\simbatch\\dataDir\\",
                             "backupDirectory": "\\\\simbatch\\backups\\",
                             "definitionsDirectory": "\\\\simbatch\\definitions\\"},
                        "sql":
                            {"db": "127.0.1.220", "user": "default", "pass": "default", "port": "3306"},
                        "adminUser":
                            {"name": "admin", "sign": "A", "pass": "pass"},
                        "window":
                            {"posX": 70, "posY": 150, "sizeX": 600, "sizeY": 800, "alwaysOnTop": False}
                        }

    def __init__(self, logger, runtime_env, ini_file="config.ini", force_os=False):
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

        self.runtime_env = runtime_env
        self.ini_file = ini_file
        self.comfun = CommonFunctions()
        self.sql = [None, None, None, None]
        self.clear_state_colors()

        self.load_settings()

        if self.loading_state >= 3:
            if self.WITH_GUI == 1:
                self.update_ui_colors()
        else:
            print " [WRN]  Settings not loaded !!!", self.loading_state

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
        print " store_data_backup_directory: ", self.store_data_backup_directory
        print " store_definitions_directory: ", self.store_definitions_directory
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

    def load_settings(self):
        if self.comfun.file_exists(self.ini_file, info="settings init"):
            self.loading_state = 1
            with open(self.ini_file) as f:
                self.json_settings_data = json.load(f)
                ret = self.check_data_integration()
                if ret:
                    self.debug_level = self.json_settings_data["debugLevel"]["current"]
                    self.store_data_mode = self.json_settings_data["dataMode"]["current"]
                    self.ui_color_mode = self.json_settings_data["colorMode"]["current"]

                    self.store_data_json_directory = self.json_settings_data["storeData"]["dataDirectory"]
                    self.store_data_backup_directory = self.json_settings_data["storeData"]["backupDirectory"]
                    self.store_definitions_directory = self.json_settings_data["storeData"]["definitionsDirectory"]

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
                    self.loading_state = 3

                    if self.debug_level >= 3:
                        print "\n\n [INF] settings init"
                else:
                    print " [WRN] json data inconsistency:", self.ini_file
                    self.loading_state = 2
        else:
            print " [ERR] config.ini file not exists: ", self.ini_file
            self.loading_state = -1

    def save_settings(self, settings_file=""):
        comfun = self.comfun
        data_path = self.store_data_json_directory

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
        comfun.save_to_file(settings_file, json.dumps(self.default_settings, indent=2, sort_keys=True))
        print ' [INF] settings saved to: ', settings_file

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
                    print " [ERR] missing key:", k
                    errors += 1
        else:
            return False

        if errors == 0:
            return True
        else:
            return False

    def update_ui_colors(self):
        if self.store_definitions_directory is not None:
            palette_id = self.ui_color_mode
            if palette_id == 1:
                color_file = self.store_definitions_directory + "colors/" + self.COLORS_GRAY_FILE_NAME
            elif palette_id == 2:
                color_file = self.store_definitions_directory + "colors/" + self.COLORS_PASTEL_FILE_NAME
            elif palette_id == 3:
                color_file = self.store_definitions_directory + "colors/" + self.COLORS_DARK_FILE_NAME
            else:
                #  palette_id == 4:
                color_file = self.store_definitions_directory + "colors/" + self.COLORS_CUSTOM_FILE_NAME

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
                    print " [INF] loaded colors: ", color_file
                return True
            else:
                for i in range(0, 40):
                    self.state_colors.append(QBrush(QColor.fromRgb(40, 40, 40, a=255)))
                    self.state_colors_up.append(QBrush(QColor.fromRgb(140, 140, 140, a=255)))

                if self.debug_level >= 3:
                    print " [WRN] not loaded colors: ", color_file
                return False
        else:
            # TO DO dblvl
            print " [WRN] store_definitions_directory  is None"
            return False
