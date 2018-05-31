import sys
import os
import json
from os import path
from collections import OrderedDict
from datetime import datetime


class Logger:
    # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    console_level = 0
    log_file_level = 0
    log_file_path = ""
    force_add_to_log = False
    buffering = False
    buffer = ""

    def __init__(self, log_level=0, console_level=3):
        if console_level is None or console_level > 4:
            print "Logger init"
        self.console_level = console_level
        self.log_file_level = log_level

    def set_log_level(self, lvl):
        self.log_file_level = lvl

    def set_console_level(self, lvl):
        self.console_level = lvl

    def add_to_log(self, prefix, message):
        pass
        # TODO !!!

    def dispatch(self, level, message, force_print=False, raw=False):
        if self.console_level >= level or force_print:
            console_print = True
        else:
            console_print = False

        if self.log_file_level >= level:
            log_append = True
        else:
            log_append = False

        if level == 1:
            indent = ""
            prefix = "ERR"
        elif level == 2:
            indent = "  "
            prefix = "WRN"
        elif level == 3:
            indent = "    "
            prefix = "INF"
        elif level == 4:
            indent = "    _"
            prefix = "DB"
        elif level == 5:
            indent = "    ___"
            prefix = "deep"
        else:
            indent = "'"
            prefix = "_"

        if raw:
            print message
        elif console_print:
            if type(message) is tuple:
                out = "  ".join([str(el) for el in message])
                print "{}[{}] {}".format(indent, prefix, out)
            else:
                print "{}[{}] {}".format(indent, prefix, message)

        if self.force_add_to_log or log_append:
            self.add_to_log(prefix, message)

        if self.buffering is not False:
            self.buffer += "\n"+message

    def err(self, message, force_print=False):
        self.dispatch(1, message, force_print=force_print)

    def wrn(self, message, force_print=True):
        self.dispatch(2, message, force_print=force_print)

    def inf(self, message, force_print=False):
        self.dispatch(3, message, force_print=force_print)

    def db(self, message, force_print=False):
        self.dispatch(4, message, force_print=force_print)

    def deepdb(self, message, force_print=False):
        self.dispatch(5, message, force_print=force_print)

    def raw(self, message):
        self.dispatch(5, message, raw=True)

    def clear_buffer(self):
        self.buffer = ""

    def get_buffer(self):
        return self.buffer

    def buffering_on(self):
        self.buffering = True

    def buffering_off(self):
        self.buffering = False


class CommonFunctions:
    # debug_level = None
    logger = None

    # def __init__(self, debug_level=3):
    #     self.debug_level = debug_level
    def __init__(self, logger=None):
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Logger(log_level=0, console_level=3)

    def print_list(self, get_list, check_float=False):
        for index, val in enumerate(get_list):
            if check_float:
                print "     ", index, " : ", val, "   ___  ", self.is_float(val)
            else:
                print "     ", index, " : ", val

    @staticmethod
    def is_int(value):     # check is int   [for True return 0]
        try:
            if type(value) == int:
                return True
            else:
                return False
        except ValueError:
            return False

    @staticmethod
    def can_get_int(value):   # check can convert to int (e.g.: test string "1")   [for True return 1]
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(value):
        try:
            if type(value) == float:
                return True
            else:
                return False
        except ValueError:
            return False

    def int_or_val(self, in_val, def_val):
        if self.can_get_int(in_val):
            self.logger.deepdb(("(int_or_val) is int", in_val, def_val))
            return int(in_val)
        else:
            self.logger.deepdb(("(int_or_val) is not int", in_val, def_val))
            return def_val

    def str_with_zeros(self, number, zeros=3):
        if self.can_get_int(zeros) is False:
            zeros = 0
            self.logger.err(("(str_with_zeros) zeros is not number:", zeros))
        stri = str(number)
        while len(stri) < zeros:
            stri = "0" + stri
        return stri

    @staticmethod
    def list_as_string(get_list, only_first=False, start_from_item=0, separator=";"):
        ret_str = ""
        if len(get_list) == 1 or only_first:
            if len(get_list) > 0:
                return str(get_list[0])
            else:
                return ""
        else:
            for a in get_list[start_from_item:-1]:
                ret_str += str(a) + separator
            ret_str += str(get_list[-1])
        return ret_str

    @staticmethod
    def string_as_list(stri, separator=";", remove_empty=True, remove_shorter_than=0):
        ret_list = []
        tmp_list = stri.split(separator)
        if remove_shorter_than > 0:
            for a in tmp_list:
                if len(a) >= remove_shorter_than:
                    ret_list.append(a)
            return ret_list
        elif remove_empty:
            for a in tmp_list:
                if len(a) > 0:
                    ret_list.append(a)
            return ret_list
        else:
            return tmp_list

    def find_string_in_list(self, strings_array, wanted_string, exactly=True, starting=False, db=False):
        for index, sa in enumerate(strings_array):
            if exactly:
                if sa == wanted_string:
                    self.logger.deepdb(("isStringInArray : exactly ", sa, wanted_string), force_print=db)
                    return index
            else:
                if starting:
                    if sa.startswith(wanted_string):
                        self.logger.deepdb(("isStringInArray : starting ", sa, wanted_string), force_print=db)
                        return index
                else:
                    ret = sa.find(wanted_string)
                    if ret >= 0:
                        self.logger.deepdb(("isStringInArray : substring ", sa, wanted_string), force_print=db)
                        return index
                    ret = wanted_string.find(sa)
                    if ret >= 0:
                        self.logger.deepdb(("isStringInArray : substring ", sa, wanted_string), force_print=db)
                        return index
        return None

    # time date ...
    @staticmethod
    def get_current_time(filename_mode=False, only_time=False):
        if filename_mode:
            return datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        else:
            if only_time:
                return datetime.now().strftime('%H:%M:%S')
            else:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def format_seconds_to_string(seconds):
        if seconds < 60:
            return str(int(seconds)) + "s"
        elif seconds < 3600:
            return "{:.1f}m".format(1.0 * seconds / 60)
        else:
            return "{:.1f}h".format(1.0 * seconds / 3600)

    # files and directories ...
    @staticmethod
    def current_scripts_path():
        return path.dirname(path.realpath(sys.argv[0])) + "\\"

    def file_exists(self, check_file, info="", check_not_empty=False):
        if path.exists(check_file):
            if check_not_empty:
                finfo = os.stat(check_file)
                if finfo.st_size > 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            if len(check_file) > 0:
                if len(info) > 0:
                    self.logger.wrn("File {} not exist !  ({})\n".format(check_file, info))
                else:
                    self.logger.wrn("File {} not exist !\n".format(check_file))
            else:
                self.logger.err("File name length is zero! {}".format(info))
            return False

    def path_exists(self, check_path, info=""):
        if isinstance(check_path, basestring):
            if path.exists(str(check_path)):
                return True
            else:
                if len(info) > 0:
                    self.logger.err(("Dir ", info, " don't exist!"))
                return False
        else:
            self.logger.err(("(path_exists) wrong parameter!", check_path, info))
            return False

    def get_win_visual_path(self, path):
        return path.replace("/", "\\")

    def get_proper_path(self, get_path, info=""):
        if len(get_path) > 0:
            if get_path.find("/") >= 0:
                if get_path[-1] != "/":
                    get_path += "/"
            else:
                if get_path[-1] != "\\":
                    get_path += "\\"
        else:
            self.logger.err("(get_proper_path) param len 0 ! ({})".format(info))
        return get_path
    
    def get_path_from_full(self, full):
        path_out = os.path.dirname(full)
        path_out = self.get_proper_path(path_out)   # win 7 vs 10 fix
        
        return path_out

    def create_directory(self, directory):
        if len(directory) > 0:
            if not os.path.exists(directory):
                if directory[1] == ":":
                    check_drive = directory[0] + ":\\"
                    if os.path.exists(check_drive):   # TODO os.access
                        os.makedirs(directory)
                        return True
                    else:
                        self.logger.err(("drive: ", directory[0], " NOT EXIST !!!"))
                        return False
                else:  # linux /     or     win server \\
                    os.makedirs(directory)
                    return True
            else:
                self.logger.inf(("directory EXIST, not created:  ", directory))
                return False
        else:
            self.logger.wrn(("directory null name ", directory))
            return False

    def remove_directory(self, directory):
        if len(directory) > 0:
            if os.path.exists(directory):
                if directory[1] == ":":
                    check_drive = directory[0] + ":\\"
                    if os.path.exists(check_drive):   # TODO os.access
                        os.rmdir(directory)           # TODO shutil.rmtree
                        return True
                    else:
                        self.logger.err(("drive: ", directory[0], " NOT EXIST !!!"))
                        return False
                else:  # TODO test server \\
                    os.rmdir(directory)
                    return True
            else:
                self.logger.inf(("directory not EXIST, not removed:  ", directory))
                return False
        else:
            self.logger.wrn(("directory null name    ", directory))
            return False

    @staticmethod
    def is_absolute(check_path):
        if len(check_path) > 2:
            if check_path[1] == ":" and check_path[2] == "\\":
                return True
            if check_path[1] == ":" and check_path[2] == "/":
                return True
            if check_path[0] == "\\" and check_path[1] == "\\":
                return True
            if check_path[0] == "/":
                return True
        return False

    def create_empty_file(self, file_name):
        try:
            with open(file_name, 'a') as f:
                f.write("")
            return True
        except IOError as e:
            self.logger.err("I/O error({0}): {1}".format(e.errno, e.strerror))
        except RuntimeError:
            self.logger.err(("Unexpected error:", sys.exc_info()[0]))
            raise

    def delete_file(self, file_name):
        try:
            os.remove(file_name)
            return True
        except IOError as e:
            self.logger.err("I/O error({0}): {1}".format(e.errno, e.strerror))
            return True
        except RuntimeError:
            self.logger.err(("Unexpected error:", sys.exc_info()[0]))
            raise

    def load_from_file(self, file_name):  # TODO rename it: load content from file
        if self.file_exists(file_name):
            try:
                with open(file_name, 'r') as f:
                    content = f.readlines()
                    content = [x.strip() for x in content]
                    return content
            except IOError:
                self.logger.err(("Loading IOError error:", file_name))
                return None
        else:
            self.logger.err(("Loading: File not exists:", file_name))

    def load_json_file(self, file_name):
        if self.file_exists(file_name, info=file_name, check_not_empty=True):
            with open(file_name) as f:
                json_data = json.load(f, object_pairs_hook=OrderedDict)
            return json_data
        else:
            return None

    @staticmethod
    def save_json_file(file_name, content):
        with open(file_name, 'w') as f:
            json.dump(content, f,  indent=2)
        return True   # TODO  Exception

    @staticmethod
    def save_to_file(file_name, content):
        with open(file_name, 'w') as f:
            f.write(content)

    # widgets QT ...
    @staticmethod
    def add_wigdets(lay, arr):
        for ar in arr:
            lay.addWidget(ar)

    @staticmethod
    def add_layouts(lay, arr):
        for ar in arr:
            lay.addLayout(ar)

    def get_dialog_directory(self, qt_edit_line, qt_file_dialog, force_start_dir="", dir_separator="/"):
        start_dir = ""
        if len(force_start_dir) > 0:
            start_dir = force_start_dir
        else:
            if len(qt_edit_line.text()) > 0:
                start_dir = qt_edit_line.text()

        get_directory = qt_file_dialog.getExistingDirectory(dir=start_dir)  # TODO caption="hymmmm...."
        self.logger.inf(("selected directory:", get_directory))
        if len(get_directory) > 0:
            qt_edit_line.setText(get_directory + dir_separator)
            return get_directory + dir_separator
        return ""

    @staticmethod
    def if_empty_put_text(qt_edit_line, text):
        if len(qt_edit_line.text()) == 0:
            qt_edit_line.setText(text)

    def file_dialog_to_edit_line(self, qt_edit_line, qt_file_dialog, init_dir):
        file_dialog = qt_file_dialog.getOpenFileName(dir=init_dir)
        get_file = file_dialog[0]
        # if self.settings.current_os == 1:
        #    get_file = get_file.replace("/", "\\")
        self.logger.inf(("selected file:", get_file))
        if len(get_file) > 0:
            qt_edit_line.setText(get_file)
            return get_file
        return ""

    def get_save_file(self, qt_edit_line, qt_file_dialog, dir_separator="/"):
        get_directory = qt_file_dialog.getSaveFileName()
        if len(get_directory) > 0:
            qt_edit_line.setText(get_directory + dir_separator)

    def get_incremented_name(self, name_in, db=False):
        last_not_digit = next((i for i, j in list(enumerate(name_in, 1))[::-1] if not j.isdigit()), -1)
        if db:
            if (len(name_in) - last_not_digit) > 0:
                self.logger.deepdb(("(get_incremented_name) (gin) last ", name_in[-(len(name_in) - last_not_digit):]))
                self.logger.deepdb(("(get_incremented_name) (gin) len ", len(name_in) - last_not_digit))
                self.logger.deepdb(("(get_incremented_name) (gin) head ", name_in[:-(len(name_in) - last_not_digit)]))
            else:
                self.logger.deepdb("(get_incremented_name) (gin) empty")
        if (len(name_in) - last_not_digit) > 0:
            head = name_in[:-(len(name_in) - last_not_digit)]
            nr = int(name_in[-(len(name_in) - last_not_digit):])
            nr_len = len(name_in[-(len(name_in) - last_not_digit):])
            number = self.str_with_zeros(nr + 1, nr_len)
        else:
            head = name_in
            number = "_02"
        if db:
            self.logger.deepdb(("(get_incremented_name) (gin) return ", head, number))
        return head + number
