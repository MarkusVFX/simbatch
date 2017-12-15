import sys
import os
import json
from os import path
from collections import OrderedDict
from datetime import datetime


class CommonFunctions:
    debug_level = None

    def __init__(self, debug_level=3):
        self.debug_level = debug_level

    def print_list(self, get_list, check_float=False):
        for index, val in enumerate(get_list):
            if check_float:
                print "     ", index, " : ", val, "   ___  ", self.is_float(val)
            else:
                print "     ", index, " : ", val

    # values ...
    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def int_or_val(self, in_val, def_val):
        if self.is_int(in_val):
            if self.debug_level >= 5:
                print " [db] (int_or_val) is int", in_val, def_val
            return int(in_val)
        else:
            if self.debug_level >= 3:
                print " [WRN] (int_or_val) is not int!", in_val, def_val
            return def_val

    def str_with_zeros(self, number, zeros=3):
        if self.is_float(zeros) is False:
            zeros = 3
            if self.debug_level >= 1:
                print " [ERR] not int as zeros in str_with_zeros"
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
                    if self.debug_level >= 6 or db is True:
                        print " [db] isStringInArray : exactly ", sa, wanted_string
                    return index
            else:
                if starting:
                    if sa.startswith(wanted_string):
                        if self.debug_level >= 6 or db is True:
                            print " [db] isStringInArray :  starting ", sa, wanted_string
                        return index
                else:
                    ret = sa.find(wanted_string)
                    if ret >= 0:
                        if self.debug_level >= 6 or db is True:
                            print " [db] isStringInArray :  substring ", sa, wanted_string
                        return index
                    ret = wanted_string.find(sa)
                    if ret >= 0:
                        if self.debug_level >= 6 or db is True:
                            print " [db] isStringInArray :  substring ", sa, wanted_string
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
                    if self.debug_level >= 1:
                        print " [WRN] File {} not exist !  ({})\n".format(check_file, info)
                else:
                    if self.debug_level >= 4:
                        print " [WRN] File {} not exist.".format(check_file)
            else:
                if self.debug_level >= 1:
                    print " [ERR] File name length is zero! {}".format(info)
            return False

    def path_exists(self, check_path, info=""):
        if isinstance(check_path, basestring):
            if path.exists(str(check_path)):
                return True
            else:
                if len(info) > 0:
                    if self.debug_level >= 1:
                        print " [ERR] dir (", info, ") dont exist!"
                return False
        else:
            if self.debug_level >= 1:
                print " [ERR] (path_exists) wrong parameter!", check_path, info
            return False

    def get_proper_path(self, get_path, info=""):
        if len(get_path) > 0:
            if get_path.find("/") >= 0:
                if get_path[-1] != "/":
                    get_path += "/"
            else:
                if get_path[-1] != "\\":
                    get_path += "\\"
        else:
            if self.debug_level >= 1:
                print " [ERR] (get_proper_path) param len 0 ! ({})".format(info)
        return get_path

    @staticmethod
    def get_path_from_full(full):
        return os.path.dirname(full)

    @staticmethod
    def create_directory(directory):
        if len(directory) > 0:
            if not os.path.exists(directory):
                if directory[1] == ":":
                    check_drive = directory[0] + ":\\"
                    if os.path.exists(check_drive):   # TODO os.access
                        os.makedirs(directory)
                        return True
                    else:
                        print "ERR drive: ", directory[0], " NOT EXIST !!!"
                        return False
                else:  # TODO test server \\
                    os.makedirs(directory)
                    return True
            else:
                print " [INF] directory EXIST, not created:  ", directory, "\n"
                return False
        else:
            print " [WRN] directory null name    ", directory, "\n"
            return False

    @staticmethod
    def remove_directory(directory):
        if len(directory) > 0:
            if os.path.exists(directory):
                if directory[1] == ":":
                    check_drive = directory[0] + ":\\"
                    if os.path.exists(check_drive):   # TODO os.access
                        os.rmdir(directory)           # TODO shutil.rmtree
                        return True
                    else:
                        print "ERR drive: ", directory[0], " NOT EXIST !!!"
                        return False
                else:  # TODO test server \\
                    os.rmdir(directory)
                    return True
            else:
                print " [INF] directory not EXIST, not removed:  ", directory, "\n"
                return False
        else:
            print " [WRN] directory null name    ", directory, "\n"
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
        return False

    @staticmethod
    def create_empty_file(file_name):
        try:
            with open(file_name, 'a') as f:
                f.write("")
            return True
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    @staticmethod
    def delete_file(file_name):
        try:
            os.remove(file_name)
            return True
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return True
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    @staticmethod
    def load_from_file(file_name):  # TODO rename it: load content from file
        with open(file_name, 'a') as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            return content

    def load_json_file(self, file_name):
        if self.file_exists(file_name, info=file_name, check_not_empty=True):
            with open(file_name) as f:
                json_data = json.load(f, object_pairs_hook=OrderedDict)
            return json_data
        else:
            return None

    @staticmethod
    def save_json_file(file_name, content):
        json_data = None
        # if self.file_exists(file_name, file_name): # if self.comfun.file_exists(file, "") :

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

    def get_dialog_directory(self, qt_edit_line, qt_file_dialog, force_start_dir=""):
        start_dir = ""
        if len(force_start_dir) > 0:
            start_dir = force_start_dir
        else:
            if len(qt_edit_line.text()) > 0:
                start_dir = qt_edit_line.text()

        get_directory = qt_file_dialog.getExistingDirectory(dir=start_dir)  # TODO caption="hymmmm...."
        get_directory = get_directory.replace("/", "\\")
        if self.debug_level >= 3:
            print ' [INF] selected_directory:', get_directory
        if len(get_directory) > 0:
            qt_edit_line.setText(get_directory + "\\")
            return get_directory + "\\"
        return ""

    @staticmethod
    def if_empty_put_text(qt_edit_line, text):
        if len(qt_edit_line.text()) == 0:
            qt_edit_line.setText(text)

    @staticmethod
    def get_get_file(qt_edit_line, qt_file_dialog, init_dir):
        get_directory = qt_file_dialog.getOpenFileName(dir=init_dir)
        get_dir = get_directory[0].replace("/", "\\")
        if len(get_dir) > 0:
            qt_edit_line.setText(get_dir)

    @staticmethod
    def get_save_file(qt_edit_line, qt_file_dialog):
        get_directory = qt_file_dialog.getSaveFileName()
        get_dir = get_directory[0].replace("/", "\\")
        if len(get_dir) > 0:
            qt_edit_line.setText(get_dir + "\\")

    def get_incremented_name(self, name_in, db=False):
        last_not_digit = next((i for i, j in list(enumerate(name_in, 1))[::-1] if not j.isdigit()), -1)
        if db:
            if (len(name_in) - last_not_digit) > 0:
                print "\n [db] (gin) last ", name_in[-(len(name_in) - last_not_digit):]
                print " [db] (gin) len ", len(name_in) - last_not_digit
                print " [db] (gin) head ", name_in[:-(len(name_in) - last_not_digit)]
            else:
                print "\n [db] (gin) empty"
        if (len(name_in) - last_not_digit) > 0:
            head = name_in[:-(len(name_in) - last_not_digit)]
            nr = int(name_in[-(len(name_in) - last_not_digit):])
            nr_len = len(name_in[-(len(name_in) - last_not_digit):])
            number = self.str_with_zeros(nr + 1, nr_len)
        else:
            head = name_in
            number = "_02"
        if db:
            print " [db] (gin) return ", head + number
        return head + number
