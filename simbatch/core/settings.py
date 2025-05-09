import os
import json
from random import randint
from .lib.common import CommonFunctions
import sys


class Settings:
    logger = None                   # logger prints errors, warnings, info and db to console and to log file
    ini_file = None                 # fundamental config file, json format
    loading_state = 0               # check fundamental config.ini
    settings_err_info = ""          # store last err/wrn when loading config.ini
    json_settings_data = None       # basic config data

    # fundamental settings (config.ini)
    current_os = -1                             # 1 Linux, 2 windoza   detected on __init__ or forced by force_os
    dir_separator = ""                          # set on __init__   depend on  current_os        # TODO move to os.sep
    store_data_mode = None                      # 1 json     2 MySQL (PRO version)
    debug_level = None                          # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    store_data_json_directory = None            # dir basic config settings (def:config.ini)
    store_data_json_directory_abs = None        # dir basic config settings (def:config.ini)
    store_data_backup_directory = None          # dir backup data
    store_data_backup_directory_abs = None      # dir backup data
    store_definitions_directory = None          # dir with software, actions, engines and param definitions
    store_definitions_directory_abs = None      # dir with software, actions, engines and param definitions
    master_directory_abs = None                 # dir used for update simnodes code
    store_abs_dir = ""                          #
    sql = [None, None, None, None]              # "db"  "pass"  "port"  "user" (PRO version)
    admin_user = None                           # PRO version

    # predefined settings
    SIMBATCH_VERSION = "v0.3.0"   # current version
    JSON_PROJECTS_FILE_NAME = "data_projects.json"
    JSON_SCHEMAS_FILE_NAME = "data_schemas.json"
    JSON_TASKS_FILE_NAME = "data_tasks.json"
    JSON_QUEUE_FILE_NAME = "data_queue.json"
    JSON_SIMNODES_FILE_NAME = "data_simnodes.json"

    states_visible_names = {}

    INDEX_HEADER = 0   # state id will set header color
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
    INDEX_STATE_KILLED = 15

    INDEX_STATE_CUSTOM = 18
    INDEX_STATE_OFFLINE = 19
    INDEX_STATE_INACTIVE = 20
    INDEX_STATE_SUSPEND = 21
    INDEX_STATE_ACTIVE = 22
    INDEX_STATE_DEFAULT = 23

    states_visible_names[INDEX_HEADER] = "HEADER"
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
    states_visible_names[INDEX_STATE_KILLED] = "KILLED"

    states_visible_names[INDEX_STATE_CUSTOM] = "CUSTOM"
    states_visible_names[INDEX_STATE_OFFLINE] = "OFFLINE"
    states_visible_names[INDEX_STATE_INACTIVE] = "INACTIVE"
    states_visible_names[INDEX_STATE_SUSPEND] = "SUSPENDED"
    states_visible_names[INDEX_STATE_ACTIVE] = "ACTIVE"
    states_visible_names[INDEX_STATE_DEFAULT] = "DEFAULT"

    # GUI settings
    with_gui = 1                                # loading color schema # TODO auto detect
    runtime_env = ""        # runtime environment as software name display on frame and set active definition
    ui_edition_mode = 0     # 0 open source    1 Pro version (with Wizard tab as first)
    ui_color_mode = 1       # color palette    1 gray,  2 pastel,  3 dimmed,  4 custom
    ui_brightness_mode = 1  # 0 dark mode  1 light mode
    state_colors = []       # item list colors
    state_colors_up = []    # selected item list colors
    state_colors_rgb_str = []   # item list colors   as RGB string
    state_colors_up_rgb_str = []   # item list colors   as RGB string

    default_gray_brush = None
    default_light_gray_brush = None
    default_gray_rgb_str = None          # as RGB string
    default_light_gray_rgb_str = None    # as RGB string

    window = None           # store def window position
    always_on_top = False   # obvious obviousness
    save_window_position = True  # whether to save window position and size
    force_start_tab = 0     # if > 0 show tab with this index after run

    # check screen resolution: protect window position (outside screen if second monitor is off)
    CHECK_SCREEN_RES_ON_START = 1
    COLORS_PASTEL_FILE_NAME = "colors_pastel.ini"
    COLORS_CUSTOM_FILE_NAME = "colors_custom.ini"
    COLORS_GRAY_FILE_NAME = "colors_gray.ini"
    COLORS_DIMMED_FILE_NAME = "colors_dimmed.ini"

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
            self.dir_separator = "/"        # TODO  move to os.sep
        else:
            self.dir_separator = "\\"       # TODO  move to os.sep

        """  STANDALONE """
        self.store_abs_dir = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}{os.sep}"

        """  MAYA win  C:\Program Files\Autodesk\Maya2014\ """
        # TODO check abs

        self.comfun = CommonFunctions(self.logger)
        self.runtime_env = runtime_env
        if runtime_env == "Server":
            self.with_gui = 0
        self.ini_file = self.get_ini_file_and_path(ini_path, ini_file)

        """ check and force DEV config """
        if self.comfun.file_exists(os.path.join(os.path.dirname(self.ini_file), "config_dev.ini"), info=False):
            self.ini_file = os.path.join(os.path.dirname(self.ini_file), "config_dev.ini")
            self.logger.inf(("force DEV config:", self.ini_file), nl=True)

        self.sql = [None, None, None, None]

        self.load_settings()

        if self.loading_state < 4:
            self.logger.err(f"Data not loaded !!!  ({self.loading_state})")

    def get_version(self):
        return self.SIMBATCH_VERSION

    def print_all(self):
        print(" loading_state: ", self.loading_state)
        print(" ini_file: ", self.ini_file)
        print(" runtime_env: ", self.runtime_env)

        if self.json_settings_data is not None:
            if "dataMode" in self.json_settings_data:
                print(" json_settings_data[dataMode][current]: ", self.json_settings_data["dataMode"]["current"])
            else:
                self.logger.err(("MISSING dataMode KEY IN SETTINGS FILE:", self.ini_file))
            if "colorMode" in self.json_settings_data:
                print(" json_settings_data[colorMode][current]: ", self.json_settings_data["colorMode"]["current"])
            else:
                self.logger.err(("MISSING colorMode KEY IN SETTINGS FILE:", self.ini_file))
            if "debugLevel" in self.json_settings_data:
                print(" json_settings_data[debugLevel][current]: ", self.json_settings_data["debugLevel"]["current"])
            else:
                self.logger.err(("MISSING debugLevel KEY IN SETTINGS FILE:", self.ini_file))
            if "window" in self.json_settings_data:
                print(" json_settings_data[window]: ", self.json_settings_data["window"])
            else:
                self.logger.err(("MISSING window KEY IN SETTINGS FILE:", self.ini_file))

        print(" store_data_mode: ", self.store_data_mode)
        print(" debug_level: ", self.debug_level)
        print(" store_data_json_directory: ", self.store_data_json_directory)
        if self.store_data_json_directory != self.store_data_json_directory_abs:
            print(" store_data_json_directory_abs: ", self.store_data_json_directory_abs)
        print(" store_data_backup_directory: ", self.store_data_backup_directory)
        if self.store_data_backup_directory != self.store_data_backup_directory_abs:
            print(" store_data_backup_directory_abs: ", self.store_data_backup_directory_abs)
        print(" store_definitions_directory: ", self.store_definitions_directory)
        if self.store_definitions_directory != self.store_definitions_directory_abs:
            print(" store_definitions_directory_abs: ", self.store_definitions_directory_abs)
        print(" sql settings: ", self.sql)
        print(" admin_user: ", self.admin_user)
        print(" window:", self.window)

        print("\n\n")

    @staticmethod
    def random_welcome_message():
        messages = ("Welcome", "Have a nice sim!", "Sim, Forrest, sim!")
        rand = randint(0, len(messages)-1)
        return messages[rand]
    
    """  trigered from mainw, used only with GUI """
    def init_colors(self, rbg_to_brush):
        self.clear_state_colors()
        self.rbg_to_brush = rbg_to_brush

    def clear_state_colors(self):
        self.state_colors = []
        self.state_colors_up = []
        for i in range(0, 40):
            self.state_colors.append(self.default_gray_brush)
            self.state_colors_up.append(self.default_light_gray_brush)

        self.state_colors_rgb_str = []
        self.state_colors_up_rgb_str = []
        for i in range(0, 40):
            self.state_colors_rgb_str.append(self.default_gray_rgb_str)
            self.state_colors_up_rgb_str.append(self.default_light_gray_rgb_str)

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
                check_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
                ini_file_and_path = check_ini_path + ini_file
                if check_is_exists:
                    if self.comfun.file_exists(check_ini_path + ini_file) is False:
                        self.logger.err((" CONFIG FILE NOT EXIST:", (check_ini_path + ini_file)))
            else:
                if ini_path == "tests":
                    check_ini_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    check_ini_path = os.path.dirname(check_ini_path) + os.sep + "tests"   # cd ../tests
                    check_ini_path += os.sep
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
        dir_sep = os.sep

        if len(data_path) == 0:
            self.store_data_json_directory_abs = ""
        else:
            if self.comfun.is_absolute(data_path):
                if data_path[-1:] == "\\" or data_path[-1:] == "/":
                    self.store_data_json_directory_abs = data_path
                    self.store_data_backup_directory_abs = data_path + "backup" + dir_sep
                else:
                    self.store_data_json_directory = data_path + dir_sep
                    self.store_data_json_directory_abs = data_path + dir_sep
                    self.store_data_backup_directory_abs = data_path + dir_sep + "backup" + dir_sep
            else:
                if data_path[-1:] == "\\" or data_path[-1:] == "/":
                    self.store_data_json_directory_abs = self.store_abs_dir + data_path
                    self.store_data_backup_directory_abs = self.store_abs_dir + data_path + "backup" + dir_sep
                else:
                    self.store_data_json_directory_abs = self.store_abs_dir + data_path + dir_sep
                    self.store_data_backup_directory_abs = self.store_abs_dir + data_path + dir_sep + "backup" + dir_sep

        definitions_path = self.store_definitions_directory
        if len(definitions_path) == 0:
            self.store_definitions_directory_abs = ""
        else:
            if self.comfun.is_absolute(definitions_path):
                if definitions_path[-1:] == "\\" or definitions_path[-1:] == "/":
                    self.store_definitions_directory_abs = definitions_path
                else:
                    self.store_definitions_directory = definitions_path + dir_sep
                    self.store_definitions_directory_abs = definitions_path + dir_sep
            else:
                if definitions_path[-1:] == "\\" or definitions_path[-1:] == "/":
                    self.store_definitions_directory_abs = self.store_abs_dir + self.store_definitions_directory
                else:
                    self.store_definitions_directory_abs = self.store_abs_dir + self.store_definitions_directory + dir_sep

    def load_settings(self):
        self.settings_err_info = ""
        if self.comfun.file_exists(self.ini_file, info="settings init"):
            self.loading_state = 1
            try:
                with open(self.ini_file, encoding='utf-8') as f:
                    self.json_settings_data = json.load(f)
                ret = self.check_data_integration()
                if ret:
                    self.debug_level = self.json_settings_data["debugLevel"]["current"]
                    self.logger.console_level = self.debug_level
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
                    # Store original window settings for use when save_window_position is False
                    self.original_window_settings = {
                        "posX": wnd["posX"], 
                        "posY": wnd["posY"], 
                        "sizeX": wnd["sizeX"], 
                        "sizeY": wnd["sizeY"]
                    }
                    self.always_on_top = wnd["alwaysOnTop"]
                    
                    if "simnodes" in self.json_settings_data:
                        simnodes = self.json_settings_data["simnodes"]
                        if "master_source" in simnodes:
                            self.master_directory_abs = simnodes["master_source"]

                    if "startup" in self.json_settings_data.keys():
                        if "tab" in self.json_settings_data["startup"].keys():
                            self.force_start_tab = self.json_settings_data["startup"]["tab"]
                            self.logger.inf(f"forced startup tab index: {self.force_start_tab}")

                    if self.comfun.can_get_int(self.store_data_mode):
                        if self.store_data_mode == 1:
                            if self.comfun.path_exists(self.store_data_json_directory_abs) is False:
                                if len(self.store_data_json_directory_abs) == 0:
                                    self.settings_err_info = "Database directory not defined!"
                                else:
                                    self.settings_err_info = "Database directory not exists!"
                            elif self.comfun.path_exists(self.store_definitions_directory_abs) is False:
                                if len(self.store_definitions_directory_abs) == 0:
                                    self.settings_err_info = "Definitions directory not defined!"
                                else:
                                    self.settings_err_info = "Definitions directory not exists!"
                            else:
                                """ SETTINGS VALUES ARE OK"""
                                self.loading_state = 4
                                if self.debug_level >= 3:
                                    self.logger.inf(f"settings loaded {self.ini_file}")
                                return True

                        elif self.store_data_mode == 2:
                            # PRO VERSION
                            self.loading_state = 3
                            self.settings_err_info = "MySQL will be supported with the PRO version"
                        else:
                            self.loading_state = 3
                            self.settings_err_info = f"Store data mode: {self.store_data_mode} incorrect value"
                else:
                    self.logger.wrn(f"json data inconsistency: {self.ini_file}")
                    self.loading_state = 2
            except IOError as e:
                self.logger.err(("I/O error loading settings file({0}): {1}".format(e.errno, e.strerror), self.ini_file))
                return False
            except ValueError as ve:
                self.logger.err(("value error settings:", ve, self.ini_file))
                return False
            except Exception:
                self.logger.err(("unexpected error loading settings:", sys.exc_info()[0], self.ini_file))
                return False
        else:
            self.settings_err_info = f" [ERR] config.ini file not exists: {self.ini_file}"
            self.loading_state = -1

        print(f"\n\n[ERR] {self.settings_err_info}")
        return False

    def save_settings(self, settings_file=""):
        if len(settings_file) == 0:
            settings_file = self.ini_file  # JSON format
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
        
        # Only save current window position and size if save_window_position is True
        if self.save_window_position:
            self.default_settings["window"]["posX"] = self.window[0]
            self.default_settings["window"]["posY"] = self.window[1]
            self.default_settings["window"]["sizeX"] = self.window[2]
            self.default_settings["window"]["sizeY"] = self.window[3]
        else:
            # Use the original window settings from the loaded JSON file when save_window_position is False
            if hasattr(self, 'original_window_settings'):
                self.default_settings["window"]["posX"] = self.original_window_settings["posX"]
                self.default_settings["window"]["posY"] = self.original_window_settings["posY"]
                self.default_settings["window"]["sizeX"] = self.original_window_settings["sizeX"]
                self.default_settings["window"]["sizeY"] = self.original_window_settings["sizeY"]
        
        self.default_settings["window"]["alwaysOnTop"] = self.always_on_top

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

        ret = comfun.save_to_file(settings_file, json.dumps(self.default_settings, indent=2, sort_keys=True),
                                  nl_at_end=True)
        if ret:
            self.logger.inf((" Settings saved to: ", settings_file))
        else:
            self.logger.err((" Settings NOT saved to: ", settings_file))
            return ret

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
            self.logger.err(f"found {errors} errors in config file")
            return False
            
    def get_settings_as_json(self):
        """
        Return the current settings as a JSON object loaded from config.ini
        """
        # Use the existing ini file or find it
        config_file = self.ini_file
        
        # Check if file exists
        if not self.comfun.file_exists(config_file, info=False):
            self.logger.wrn(f"Config file not found: {config_file}")
            return None
            
        # Load settings from file
        try:
            with open(config_file, encoding='utf-8') as f:
                settings_data = json.load(f)
                
            # Ensure simnodes section exists
            if "simnodes" not in settings_data:
                settings_data["simnodes"] = {}
                
            # Set master_source to current installation directory if available
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            settings_data["simnodes"]["master_source"] = current_dir
            
            # Make sure storeData paths are defined
            if "storeData" not in settings_data:
                settings_data["storeData"] = {}
                
            # Update storeData paths if they exist
            if "dataDirectory" in settings_data["storeData"]:
                data_dir = settings_data["storeData"]["dataDirectory"]
                if not os.path.isabs(data_dir) and data_dir:
                    settings_data["storeData"]["dataDirectory"] = os.path.join(current_dir, data_dir)
                    
            if "backupDirectory" in settings_data["storeData"]:
                backup_dir = settings_data["storeData"]["backupDirectory"]
                if not os.path.isabs(backup_dir) and backup_dir:
                    settings_data["storeData"]["backupDirectory"] = os.path.join(current_dir, backup_dir)
                    
            if "definitionsDirectory" in settings_data["storeData"]:
                defs_dir = settings_data["storeData"]["definitionsDirectory"]
                if not os.path.isabs(defs_dir) and defs_dir:
                    settings_data["storeData"]["definitionsDirectory"] = os.path.join(current_dir, defs_dir)
                
            return settings_data
        except json.JSONDecodeError as e:
            self.logger.err(f"JSON decode error in {config_file}: {str(e)}")
            return None    
        except IOError as e:
            self.logger.err(f"I/O error loading settings from {config_file}: {str(e)}")
            return None
        except Exception as e:
            self.logger.err(f"Error loading settings from {config_file}: {str(e)}")
            return None

    def rbg_to_brush(self, r, g, b):
        self.logger.wrn("This function should be never used")
        return ""
    
    def update_ui_colors(self):
        if self.store_definitions_directory_abs is not None:
            palette_id = self.ui_color_mode
            if palette_id == 1:
                color_file = self.store_definitions_directory_abs + "colors" + os.sep + \
                             self.COLORS_GRAY_FILE_NAME
            elif palette_id == 2:
                color_file = self.store_definitions_directory_abs + "colors" + os.sep + \
                             self.COLORS_PASTEL_FILE_NAME
            elif palette_id == 3:
                color_file = self.store_definitions_directory_abs + "colors" + os.sep + \
                             self.COLORS_DIMMED_FILE_NAME
            else:
                #  palette_id == 4:
                color_file = self.store_definitions_directory_abs + "colors" + os.sep + \
                             self.COLORS_CUSTOM_FILE_NAME

            if self.comfun.file_exists(color_file, info="colors file"):
                self.clear_state_colors()
                try:
                    with open(color_file, 'r', encoding='utf-8') as f:
                        for li_counter, line in enumerate(f.readlines()):
                            li = line.split(";")
                            if len(li) > 7: 
                                self.state_colors[li_counter] = self.rbg_to_brush(self.comfun.int_or_val(li[2], 40), 
                                                                                  self.comfun.int_or_val(li[3], 40),
                                                                                  self.comfun.int_or_val(li[4], 40))
                                                                                    
                                self.state_colors_up[li_counter] = self.rbg_to_brush(self.comfun.int_or_val(li[6], 140), 
                                                                                     self.comfun.int_or_val(li[7], 140),
                                                                                     self.comfun.int_or_val(li[8], 140))

                                self.state_colors_rgb_str[li_counter] = ", ".join([str(self.comfun.int_or_val(li[2], 40)), 
                                                                                   str(self.comfun.int_or_val(li[3], 40)),
                                                                                   str(self.comfun.int_or_val(li[4], 40))])

                                self.state_colors_up_rgb_str[li_counter] = ", ".join([str(self.comfun.int_or_val(li[6], 140)), 
                                                                                      str(self.comfun.int_or_val(li[7], 140)),
                                                                                      str(self.comfun.int_or_val(li[8], 140))])
                    
                    if self.debug_level >= 3:
                        self.logger.inf(("loaded colors: ", color_file))
                    return True
                except Exception as e:
                    self.logger.err(f"Error loading colors: {str(e)}")
                    return False
            else:
                for i in range(0, 40):
                    self.state_colors.append(self.default_gray_brush)
                    self.state_colors_up.append(self.default_light_gray_brush)
                    self.state_colors_rgb_str.append(self.default_gray_rgb_str)
                    self.state_colors_up_rgb_str.append(self.default_light_gray_rgb_str)

                if self.debug_level >= 3:
                    self.logger.wrn(("NOT loaded colors: ", color_file))
                return False
        else:
            self.logger.wrn("store_definitions_directory is None")
            return False
