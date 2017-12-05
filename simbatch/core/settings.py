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
    soft_id = None                  # current soft mode

    # basic config settings (def:config.ini)
    store_data_mode = None                      # 1 json     2 MySQL (PRO version)
    debug_level = None                          # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    store_data_json_directory = None            # dir basic config settings (def:config.ini)
    store_data_backup_directory = None          # dir backup data
    store_data_definitions_directory = None     # dir with software, actions, engines and param definitions
    sql = [None, None, None, None]              # "db"  "pass" "port" "user" (PRO version)
    admin_user = None                           # PRO version

    # predefined settings
    SIMBATCH_VERSION = "v0.2.05"   # current version
    JSON_PROJECTS_FILE_NAME = "data_projects.json"
    JSON_SCHEMAS_FILE_NAME = "data_schemas.json"
    JSON_TASKS_FILE_NAME = "data_tasks.json"
    JSON_QUEUE_FILE_NAME = "data_queue.json"
    JSON_SIMNODES_FILE_NAME = "data_simnodes.json"

    # GUI settings
    current_soft_name = ""  # only for display at this moment
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
                        "datamode":
                            {"current": 1, "modes": "1-json, 2-MySQL"},
                        "colormode":
                            {"current": 2, "levels": "1 gray,  2 pastel,  3 dark,  4 custom  "},
                        "debuglevel":
                            {"current": 4, "levels": "1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL "},
                        "storedata":
                            {"datadirectory": "S:/simbatch/data/",
                             "backupdirectory": "S:/simbatch/data/backups/",
                             "definitionsdirectory": "S:/simbatch/simbatch/definitions/"},
                        "sql":
                            {"db": "127.0.1.220", "user": "default", "pass": "default", "port": "3306"},
                        "adminuser":
                            {"name": "admin", "sign": "A", "pass": "pass"},
                        "window":
                            {"posx": 70, "posy": 150, "sizex": 600, "sizey": 800}
                        }

    def __init__(self, soft_id, ini_file="config.ini"):
        self.set_current_soft(soft_id)
        self.ini_file = ini_file
        self.comfun = CommonFunctions(2)

        self.load_settings()

        if self.loading_state == 2:
            if self.WITH_GUI == 1:
                self.update_ui_colors()

    def print_all(self):
        print " loading_state: ", self.loading_state
        print " ini_file: ", self.ini_file
        print " soft_id: ", self.soft_id

        print " json_settings_data[datamode][current]: ", self.json_settings_data["datamode"]["current"]
        print " json_settings_data[colormode][current]: ", self.json_settings_data["colormode"]["current"]
        print " json_settings_data[debuglevel][current]: ", self.json_settings_data["debuglevel"]["current"]
        print " json_settings_data[window]: ", self.json_settings_data["window"]

        print " store_data_mode: ", self.store_data_mode
        print " debug_level: ", self.debug_level
        print " store_data_json_directory: ", self.store_data_json_directory
        print " store_data_backup_directory: ", self.store_data_backup_directory
        print " store_data_definitions_directory: ", self.store_data_definitions_directory
        print " sql settings: ", self.sql
        print " admin_user: ", self.admin_user

        print "\n\n"



    def load_settings(self):
        if self.comfun.file_exists(self.ini_file, info="settings init"):
            self.loading_state = 1
            with open(self.ini_file) as f:
                self.json_settings_data = json.load(f)
                self.loading_state = 2
                ret = self.check_data_integration()
                if ret:
                    self.debug_level = self.json_settings_data["debuglevel"]["current"]
                    self.store_data_mode = self.json_settings_data["datamode"]["current"]
                    self.ui_color_mode = self.json_settings_data["colormode"]["current"]

                    self.store_data_json_directory = self.json_settings_data["storedata"]["datadirectory"]
                    self.store_data_backup_directory = self.json_settings_data["storedata"]["backupdirectory"]
                    self.store_data_definitions_directory = self.json_settings_data["storedata"]["definitionsdirectory"]

                    self.sql = self.json_settings_data["sql"].values()  # TODO order  values()
                    self.admin_user = self.json_settings_data["adminuser"].values()  # TODO order  values()
                    wnd = self.json_settings_data["window"]
                    self.window = [wnd["posx"], wnd["posy"], wnd["sizex"], wnd["sizey"]]

                    if self.debug_level >= 3:
                        print "\n\n [INF] settings init"
                else:
                    print " [WRN] json data inconsistency:", self.ini_file
        else:
            print " [ERR] ini file not exists: ", self.ini_file
            self.loading_state = -1

    def save_settings(self, settings_file=""):
        comfun = self.comfun
        data_path = self.store_data_json_directory

        self.default_settings["datamode"]["current"] = self.store_data_mode
        self.default_settings["colormode"]["current"] = self.ui_color_mode
        self.default_settings["debuglevel"]["current"] = self.debug_level
        self.default_settings["storedata"]["datadirectory"] = self.store_data_json_directory
        self.default_settings["storedata"]["backupdirectory"] = self.store_data_backup_directory
        self.default_settings["storedata"]["definitionsdirectory"] = self.store_data_definitions_directory
        self.default_settings["sql"]["db"] = self.sql[0]   # PRO VERSION
        self.default_settings["sql"]["user"] = self.sql[1]    # PRO VERSION
        self.default_settings["sql"]["pass"] = self.sql[2]    # PRO VERSION
        self.default_settings["sql"]["port"] = self.sql[3]    # PRO VERSION
        self.default_settings["window"]["posx"] = self.window[0]
        self.default_settings["window"]["posy"] = self.window[1]
        self.default_settings["window"]["sizex"] = self.window[2]
        self.default_settings["window"]["sizey"] = self.window[3]

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

    def set_current_soft(self, soft_id):  # 1 Houdini,  2 Maya,  3 3dsmax,  4  RF,  5 standalone,  6 blender, 7 c4d, ...
        self.soft_id = soft_id
        if soft_id == 1:
            self.current_soft_name = "Houdini"
        elif soft_id == 2:
            self.current_soft_name = "Maya"
        elif soft_id == 3:
            self.current_soft_name = "3dsMAX"
        elif soft_id == 4:
            self.current_soft_name = "RealFlow"
        elif soft_id == 5:
            self.current_soft_name = ":>"

    def check_data_integration(self):
        #  out = json.dumps(self.json_settings_data, indent=2)  TODO cleanup
        jd = self.json_settings_data
        json_keys = ["datamode", "debuglevel", "storedata", "sql", "adminuser", "window"]
        errors = 0
        for k in json_keys:
            if (k in jd) is False:
                print " [ERR] missing key:", k
                errors += 1
        if errors == 0:
            return True
        else:
            return False

    def print_all(self):
        print "  ini_file:", self.ini_file
        print "  loading_state:", self.loading_state
        print "  len(json_settings_data):", len(self.json_settings_data)
        print "   ."
        print "  store_data_mode:", self.store_data_mode
        print "  debug_level:", self.debug_level
        print "  store_data_json_directory:", self.store_data_json_directory
        print "  store_data_backup_directory:", self.store_data_backup_directory
        print "  store_data_definitions_directory:", self.store_data_definitions_directory
        print "   ."
        print "  sql:", self.sql
        print "  admin_user:", self.admin_user
        print "  window:", self.window
        print "   ."

    def update_ui_colors(self):
        palette_id = self.ui_color_mode
        if palette_id == 1:
            color_file = self.store_data_definitions_directory + self.COLORS_GRAY_FILE_NAME
        elif palette_id == 2:
            color_file = self.store_data_definitions_directory + self.COLORS_PASTEL_FILE_NAME
        elif palette_id == 3:
            color_file = self.store_data_definitions_directory + self.COLORS_DARK_FILE_NAME
        else:
            #  palette_id == 4:
            color_file = self.store_data_definitions_directory + self.COLORS_CUSTOM_FILE_NAME

        if self.debug_level >= 3:
            print " [INF] loading colors: ", color_file

        if self.comfun.file_exists(color_file, info="colors file"):
            self.state_colors = []
            self.state_colors_up = []
            for i in range(0, 40):
                # print "a " , i
                self.state_colors.append(QBrush(QColor.fromRgb(40, 40, 40, a=255)))
                self.state_colors_up.append(QBrush(QColor.fromRgb(140, 140, 140, a=255)))

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


if __name__ == "__main__":
    settings = Settings("..\\config.ini")
    if settings.debug_level >= 3:
        settings.print_all()
