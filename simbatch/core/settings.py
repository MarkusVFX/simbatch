import json
from common import CommonFunctions

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    print " [ERR] import PySide error"


class Settings:
    ini_file = None                 # basic config file
    loading_state = 0               # check basic config # TODO data loading and GUI init
    json_settings_data = None       # basic config data

    # basic config settings (def:config.ini)
    store_data_mode = None                      # 1 json     2 MySQL (PRO version)
    debug_level = None                          # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    store_data_json_directory = None            # dir basic config settings (def:config.ini)
    store_data_backup_directory = None          # dir backup data
    store_definitions_directory = None          # dir with software, actions, engines and param definitions
    sql = [None, None, None, None]              # "db"  "pass" "port" "user" (PRO version)
    admin_user = None                           # PRO version

    # predefined settings
    SIMBATCH_VERSION = "v0.2.06"   # current version
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
    ui_color_mode = 1       # color palette    1 gray,  2 pastel,  3 dark,  4 custom
    ui_brightness_mode = 1  # 0 dark mode  1 light mode
    state_colors = []       # item list colors
    state_colors_up = []    # selected item list colors
    window = None           # store def window position

    # check screen resolution: protect window position (outside screen if second monitor is off)
    CHECK_SCREEN_RES_ON_START = 1
    WITH_GUI = 1  # loading color schema # TODO auto detect
    COLORS_PASTEL_FILE_NAME = "colors_pastel.ini"
    COLORS_CUSTOM_FILE_NAME = "colors_custom.ini"
    COLORS_GRAY_FILE_NAME = "colors_gray.ini"
    COLORS_DARK_FILE_NAME = "colors_dark.ini"

    default_settings = {"! json info":
                        {"config": "this is basic config", "format": "more about json format: http://json.org"},
                        "dataMode":
                            {"current": 1, "modes": "1-json, 2-MySQL"},
                        "colorMode":
                            {"current": 2, "levels": "1 gray,  2 pastel,  3 dark,  4 custom  "},
                        "debugLevel":
                            {"current": 4, "levels": "1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL "},
                        "storeData":
                            {"dataDirectory": "\\simbatch\\dataDir\\",
                             "backupDirectory": "\\simbatch\\backups\\",
                             "definitionsDirectory": "\\simbatch\\definitions\\"},
                        "sql":
                            {"db": "127.0.1.220", "user": "default", "pass": "default", "port": "3306"},
                        "adminUser":
                            {"name": "admin", "sign": "A", "pass": "pass"},
                        "window":
                            {"posX": 70, "posY": 150, "sizeX": 600, "sizeY": 800}
                        }

    def __init__(self, runtime_env, ini_file="config.ini"):
        self.runtime_env = runtime_env
        self.ini_file = ini_file
        self.comfun = CommonFunctions(2)
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

        print " json_settings_data[dataMode][current]: ", self.json_settings_data["dataMode"]["current"]
        print " json_settings_data[colorMode][current]: ", self.json_settings_data["colorMode"]["current"]
        print " json_settings_data[debugLevel][current]: ", self.json_settings_data["debugLevel"]["current"]
        print " json_settings_data[window]: ", self.json_settings_data["window"]

        print " store_data_mode: ", self.store_data_mode
        print " debug_level: ", self.debug_level
        print " store_data_json_directory: ", self.store_data_json_directory
        print " store_data_backup_directory: ", self.store_data_backup_directory
        print " store_definitions_directory: ", self.store_definitions_directory
        print " sql settings: ", self.sql
        print " admin_user: ", self.admin_user
        print " window:", self.window

        print "\n\n"

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

                    self.sql = self.json_settings_data["sql"].values()  # TODO order  values()
                    self.admin_user = self.json_settings_data["adminUser"].values()  # TODO order  values()
                    wnd = self.json_settings_data["window"]
                    self.window = [wnd["posX"], wnd["posY"], wnd["sizeX"], wnd["sizeY"]]

                    self.loading_state = 3

                    if self.debug_level >= 3:
                        print "\n\n [INF] settings init"
                else:
                    print " [WRN] json data inconsistency:", self.ini_file
                    self.loading_state = 2
        else:
            print " [ERR] ini file not exists: ", self.ini_file
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

        if len(settings_file) == 0:
            settings_file = comfun.current_scripts_path() + "config.ini"  # JSON format
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
        for k in json_keys:
            if (k in jd) is False:
                print " [ERR] missing key:", k
                errors += 1
        if errors == 0:
            return True
        else:
            return False

    def update_ui_colors(self):
        if self.store_definitions_directory is not None:
            palette_id = self.ui_color_mode
            if palette_id == 1:
                color_file = self.store_definitions_directory + self.COLORS_GRAY_FILE_NAME
            elif palette_id == 2:
                color_file = self.store_definitions_directory + self.COLORS_PASTEL_FILE_NAME
            elif palette_id == 3:
                color_file = self.store_definitions_directory + self.COLORS_DARK_FILE_NAME
            else:
                #  palette_id == 4:
                color_file = self.store_definitions_directory + self.COLORS_CUSTOM_FILE_NAME

            if self.debug_level >= 3:
                print " [INF] loading colors: ", color_file

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
                return True
            else:
                for i in range(0, 40):
                    self.state_colors.append(QBrush(QColor.fromRgb(40, 40, 40, a=255)))
                    self.state_colors_up.append(QBrush(QColor.fromRgb(140, 140, 140, a=255)))
                return False
        else:
            # TO DO dblvl
            print " [WRN] store_definitions_directory  is None"
            return False


if __name__ == "__main__":
    settings = Settings("..\\config.ini")
    if settings.debug_level >= 3:
        settings.print_all()
