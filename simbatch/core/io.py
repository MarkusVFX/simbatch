import os
import re


class InOutStorage:
    batch = None
    comfun = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.p = batch.p
        self.s = batch.s

    @staticmethod
    def is_absolute(path):
        if len(path) > 2:
            if path[1] == ":" and path[2] == "\\":
                return 1
            if path[0] == "\\" and path[1] == "\\":
                return 1
        return 0

    @staticmethod
    def get_flat_name(name):
        return re.sub('\s', '_', name)

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
                    else:
                        print "ERR drive: ", directory[0], " NOT EXIST !!!"
            else:
                print " [INF] directory EXIST, not created:  ", directory, "\n"
        else:
            print " [WRN] directory null name    ", directory, "\n"

    def create_project_working_directory(self, directory):
        self.create_directory(directory)

    def create_schema_directory(self, directory):
        self.create_directory(directory)
        self.create_directory(directory + "base_setup\\")
        self.create_directory(directory + "computed_setups\\")
        self.create_directory(directory + "prevs\\")
        self.create_directory(directory + "cache\\")

    @staticmethod
    def get_setup_ext(soft_id):
        file_ext = ".null"
        if soft_id == 1:
            #  file_ext = ".hip"   # TODO ext list
            file_ext = ".hipnc"
        if soft_id == 2:
            #  file_ext = ".mb"    # TODO ext list
            file_ext = ".ma"
        if soft_id == 3:
            file_ext = ".max"
        return file_ext

    @staticmethod
    def get_prev_ext(soft_id):
        file_ext = ".png"
        if soft_id == 1:
            file_ext = ".png"
        if soft_id == 2:
            file_ext = ".png"
        if soft_id == 3:
            file_ext = ".png"
        return file_ext

    def get_files_from_dir(self, directory, types=""):
        files = []
        dir_path = self.get_path_from_full(directory)
        if os.path.isdir(dir_path):
            for fi in os.listdir(dir_path):
                if len(types) > 0:
                    if fi.endswith(types):
                        files.append(fi)
                else:
                    files.append(fi)
        return files

    def get_files_from_dir_by_object_names(self, directory, obj_list, file_type="", crowd_mode=False,
                                           crowd_mode_data=["pre", "post", 2, 10]):   # TODO  crowd_mode_data  as class
        files = []
        crowd = []
        zeros = []
        dir_path = directory   # TODO  check dir_path = self.get_path_from_full(dir)
        if os.path.isdir(dir_path):
            for fi in os.listdir(dir_path):
                if len(file_type) == 0:
                    file_name_to_check = fi.split(".")[0]
                else:
                    file_name_to_check = fi
                for o in obj_list:
                    if len(file_type) > 0:
                        o = o + "." + file_type
                    if o == file_name_to_check:
                        files.append(fi)
                        if crowd_mode:
                            crowd.append(o)
                            zeros.append("")
                    if crowd_mode:
                        o_name_pre = crowd_mode_data[0]
                        o_name_post = crowd_mode_data[1]
                        nr_zeros = crowd_mode_data[2]
                        for i in range(0, crowd_mode_data[3]):
                            nr_z = self.comfun.str_with_zeros(i, nr_zeros)
                            co = o_name_pre + nr_z + o_name_post
                            if len(file_type) > 0:
                                co = co + "." + file_type
                            if co == file_name_to_check:
                                files.append(fi)
                                crowd.append(co)
                                zeros.append(nr_z)
        return [files, crowd, zeros]

    def get_frame_range_from_dir(self, directory):    # TODO improve   for fi in os.listdir(dir):
        start = 0
        end = 0
        if os.path.isdir(directory):
            for fi in os.listdir(directory):
                if os.path.isfile(directory + "\\" + fi):
                    fi_no_ext = fi[:-4]
                    fi_arr = fi_no_ext.split("__")
                    if self.comfun.is_float(fi_arr[1]):
                        start = int(fi_arr[1])
                    if self.comfun.is_float(fi_arr[2]):
                        end = int(fi_arr[2])
            return [1, start, end]
        else:
            return [0, 0, 0]

    def generate_base_setup_file_name(self, schema_name="", ver=1):  # from existing TASK and SCHEMA data
        if len(self.p.projects_data) < self.p.current_project_index or self.p.current_project_index < 0:
            print " ERR wrong current proj ID  ", self.p.current_project_index, len(self.p.projects_data)
            return [-1, ""]
        else:
            proj_working_dir = self.p.current_project.working_directory_absolute
            schema_flat_name = self.get_flat_name(schema_name)
            directory = proj_working_dir + schema_flat_name + "\\base_setup\\"
            file_version = "_v" + self.comfun.str_with_zeros(ver, self.p.current_project.zeros_in_version)
            file_ext = self.get_setup_ext(self.s.current_soft)
            return [1, directory + schema_flat_name + file_version + file_ext]
























