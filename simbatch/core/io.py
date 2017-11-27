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

    def is_absolute(self,path):
        if len(path) > 2:
            if path[1] == ":" and path[2] == "\\":
                return 1
            if path[0] == "\\" and path[1] == "\\":
                return 1
        return 0

    def get_flat_name(self, name):
        return re.sub('\s', '_', name)

    def get_path_from_full(self, full):
        return os.path.dirname(full)

    def create_directory(self, dir):
        if len(dir) > 0:
            if not os.path.exists(dir):
                if dir[1] == ":":
                    check_drive = dir[0] + ":\\"
                    if os.path.exists(check_drive):   # TODO os.access
                        os.makedirs(dir)
                    else:
                        print "ERR drive: ", dir[0], " NOT EXIST !!!"
            else:
                print " [INF] directory EXIST, not created:  ", dir, "\n"
        else:
            print " [WRN] directory null name    ", dir, "\n"

    def create_project_working_directory(self, dir):
        self.create_directory(dir)

    def create_schema_directory(self, dir):
        self.create_directory(dir)
        self.create_directory(dir+"base_setup\\")
        self.create_directory(dir+"computed_setups\\")
        self.create_directory(dir+"prevs\\")
        self.create_directory(dir+"cache\\")

    def get_setup_ext(self, soft_id):
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

    def get_prev_ext(self, soft_id):
        file_ext = ".png"
        if soft_id == 1:
            file_ext = ".png"
        if soft_id == 2:
            file_ext = ".png"
        if soft_id == 3:
            file_ext = ".png"
        return file_ext

    def getFilesFromDir(self, dir, types="", hack=""):
        files = []
        dir_path = self.get_path_from_full(dir)
        if os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                if len(types) > 0:
                    if file.endswith(types):
                        files.append(file)
                else:
                    files.append(file)

        return files



    def get_files_from_dir_by_object_names(self, dir, obj_list, file_type="", crowd_mode=False,
                                     crowd_mode_data=["pre", "post", 2, 10]):   # TODO  crowd_mode_data  as class
        files = []
        crowd = []
        zeros = []
        dir_path = dir   # TODO  check dir_path = self.get_path_from_full(dir)
        if os.path.isdir(dir_path):
            for file in os.listdir(dir_path):
                if len(file_type) == 0:
                    file_name_to_check = file.split(".")[0]
                else:
                    file_name_to_check = file
                for o in obj_list:
                    if len(file_type) > 0:
                        o = o + "." + file_type
                    if o == file_name_to_check:
                        files.append(file)
                        if crowd_mode:
                            crowd.append(o)
                            zeros.append("")
                    if crowd_mode:
                        o_name_pre = crowd_mode_data[0]
                        o_name_post = crowd_mode_data[1]
                        nr_zeros = crowd_mode_data[2]
                        for i in range(0, crowd_mode_data[3]):
                            nrZ = self.comfun.str_with_zeros(i, nr_zeros)
                            co = o_name_pre + nrZ + o_name_post
                            if len(file_type) > 0:
                                co = co + "." + file_type
                            if co == file_name_to_check:
                                files.append(file)
                                crowd.append(co)
                                zeros.append(nrZ)
        return [files, crowd, zeros]


    def get_frame_range_from_dir(self, dir):    # TODO improve   for fi in os.listdir(dir):
        start = 0
        end = 0
        if os.path.isdir(dir):
            for fi in os.listdir(dir):
                if os.path.isfile(dir+"\\"+fi):
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
            dir = proj_working_dir + schema_flat_name + "\\base_setup\\"
            file = schema_flat_name + "_v" + self.comfun.str_with_zeros(ver, self.p.current_project.zeros_in_version)
            file_ext = self.get_setup_ext(self.s.current_soft)
            return [1, dir + file + file_ext]
























