import sys
import os
import math
import json
from os import path
from collections import OrderedDict
from datetime import datetime

from logger import Logger


class CommonFunctions:
    # debug_level = None
    logger = None
    sep = "/"
    # def __init__(self, debug_level=3):
    # self.debug_level = debug_level

    def __init__(self, logger=None, separator=None):
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Logger(log_level=0, console_level=2)
        if separator is None:
            self.sep = os.sep

    def set_separator(self, sep):
        self.sep = sep

    def print_list(self, get_list, check_float=False):
        for index, val in enumerate(get_list):
            if check_float:
                print "     ", index, " : ", val, "  ___  ", self.is_float(val)
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
        if value is None:
            return False
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def can_get_float(value):   # check can convert to int (e.g.: test string "1")   [for True return 1]
        if value is None:
            return False
        try:
            float(value)
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

    def str_with_spaces(self, text, length=3, as_prefix=False):
        if self.is_int(length):
            while len(text) < length:
                if as_prefix:
                    text = " " + text
                else:
                    text += " "
        else:
            self.logger.err(("(str_with_spaces) length is not int:", length))

        return text

    @staticmethod
    def str_get_decorative(txt, header=False):
        if header:
            txt = " _______/// {} \\\\\\_______ ".format(txt)
        else:
            txt = " _/|\\_ _/|\\_ _/|\\_ {} _/|\\_ _/|\\_ ".format(txt)
        return txt

    @staticmethod
    def generate_sin_values(samples_total=100, amplitudes_count=4, amplitude_min=40, amplitude_max=120, period_min=20,
                            period_max=120, period_grow=False, debug_mode=False):
        sin_arr = []
        for ci in range(samples_total / amplitudes_count):
            for ai in range(amplitudes_count):
                tmp_sin = []
                if period_grow:
                    period = period_min + ci * (period_max - period_min) / (samples_total / amplitudes_count - 1)
                else:
                    period = period_max - ci * (period_max - period_min) / (samples_total / amplitudes_count - 1)
                amplitude = amplitude_min + ai * (amplitude_max - amplitude_min) / (amplitudes_count - 1)

                for ti in range(period):
                    tmp_sin.append(int(amplitude * math.sin(ti * math.pi / period * 2)))
                sin_arr.append(tmp_sin)
                if debug_mode > 0:
                    print " [{}]   new sinus len:{}    per:{}   amp:{}".format(len(sin_arr), len(sin_arr[-1]), period,
                                                                               amplitude)
                    if debug_mode > 1:
                        print sin_arr[-1]
            if debug_mode > 0:
                print "\n"
        return sin_arr

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

    def format_seconds_to_string(self, seconds):
        if self.is_float(seconds) is False:
            if self.can_get_float(seconds):
                seconds = float(seconds)
            else:
                return "NaN:{}".format(seconds)

        if seconds < 60:
            return str(int(seconds)) + "s"
        elif seconds < 3600:
            return "{:.1f}m".format(1.0 * seconds / 60)
        else:
            return "{:.1f}h".format(1.0 * seconds / 3600)

    # files and directories ...
    def current_scripts_path(self):
        return path.dirname(path.realpath(sys.argv[0])) + self.sep

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
                if info is not False:
                    if len(info) > 0:
                        self.logger.wrn("File {} not exist ! ({})\n".format(check_file, info))
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
            
    def get_dir_depth(self, dir, level=1):
        max_dir_depth = 0
        arr_dirs = []
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                if level > self.max_dir_depth:
                    self.max_dir_depth = level
                dir_name = os.path.join(dir, d)
                if os.path.isdir(dir_name):
                    self.arr_dirs.append([level, d, dir_name])
                    self.get_dir_depth(dir_name, level + 1)

    @staticmethod
    def convert_to_win_path(path_to_convert):
        if path_to_convert is not None:
            return path_to_convert.replace("/", "\\")
        else:
            return None

    @staticmethod
    def convert_to_unix_path(path_to_convert):
        if path_to_convert is not None:
            return path_to_convert.replace("\\", "/")
        else:
            return None

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
                        if os.path.exists(directory):
                            self.logger.deepdb(("directory created ", directory))
                            return True
                        else:
                            self.logger.wrn(("directory not created ", directory))
                            return False
                    else:
                        self.logger.err(("drive: ", directory[0], " NOT EXIST !!!"))
                        return False
                else:  # linux /     or     win server \\
                    os.makedirs(directory)
                    if os.path.exists(directory):
                        self.logger.deepdb(("directory created ", directory))
                        return True
                    else:
                        self.logger.wrn(("directory not created ", directory))
                        return False
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

    def test_directory_access(self, directory, directory_info="directory", with_info=True):
        ret_r = os.access(directory, os.R_OK)
        ret_w = False
        if ret_r:
            if with_info:
                self.logger.inf("Read from {} test".format(directory_info), force_prefix="OK ")
            ret_w = os.access(directory, os.W_OK)
            if ret_w:
                if with_info:
                    self.logger.inf("Save to {} test".format(directory_info), force_prefix="OK ")
            else:
                if with_info:
                    self.logger.err("Could NOT save to {} :  {} ".format(directory_info, directory))
        else:
            if with_info:
                self.logger.err("Could NOT read from {} :  {} ".format(directory_info, directory))
        return ret_r, ret_w

    @staticmethod
    def is_absolute(check_path):
        if len(check_path) > 2:
            if check_path[0] == "/":  # linux
                return True
            if check_path[1] == ":" and check_path[2] == "\\":  # win storage
                return True
            if check_path[1] == ":" and check_path[2] == "/":  # win storage nice notation
                return True
            if check_path[0] == "\\" and check_path[1] == "\\":  # win network
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

    def load_from_file(self, file_name, force_no_lines=False):  # TODO rename it: load content from file
        if self.file_exists(file_name):
            try:
                with open(file_name, 'r') as f:
                    if force_no_lines:
                        content = f.readlines()
                        content = [x.strip() for x in content]
                    else:
                        content = f.read()
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
        with open(file_name, 'w+') as f:
            json.dump(content, f,  indent=2)
        return True   # TODO  Exception

    def save_to_file(self, file_name, content, nl_at_end=False):
        try:
            with open(file_name, 'w') as f:
                f.write(content)
                if nl_at_end:
                    f.write("\n")
            return True
        except IOError:
            self.logger.err("No data saved to file: {}".format(file_name))
            return False

    """
    
    """

    """ 
    
    widgets QT ... 
    
    """

    @staticmethod
    def add_widgets(lay, arr):
        for ar in arr:
            lay.addWidget(ar)

    @staticmethod
    def add_layouts(lay, arr):
        for ar in arr:
            lay.addLayout(ar)

    def get_dialog_directory(self, qt_edit_line, qt_file_dialog, force_start_dir="", dir_separator="/"):
        start_dir = ""
        self.logger.deepdb(("force_start_dir:", force_start_dir ))
        if len(force_start_dir) > 0:
            start_dir = force_start_dir
        else:
            if len(qt_edit_line.text()) > 0:
                start_dir = qt_edit_line.text()

        '''  getExistingDirectory always return UNIX format /  '''
        get_directory = qt_file_dialog.getExistingDirectory(dir=start_dir)  # TODO caption="dir ...."
        self.logger.deepdb(("dir_separator:", dir_separator, "start_dir:", start_dir))
        self.logger.inf(("selected directory:", get_directory))
        if len(get_directory) > 0:
            if dir_separator == "\\":  # OS MARKER
                get_directory = self.convert_to_win_path(get_directory)
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
        self.logger.db(("selected file:", get_file))
        if len(get_file) > 0:
            qt_edit_line.setText(get_file)
            return get_file
        return ""

    def get_save_file(self, qt_edit_line, qt_file_dialog):
        get_directory = qt_file_dialog.getSaveFileName()
        if len(get_directory) > 0:
            qt_edit_line.setText(get_directory + self.sep)

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
