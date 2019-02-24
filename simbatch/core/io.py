import os
import re
import sys
import shutil


class PredefinedVariables:
    batch = None

    predefined = {
        "schema_base_setup": {"type": "f", "function": "get_schema_base_setup"},
        "shot_ani_cache_dir": {"type": "d", "function": "get_shot_ani_cache_dir"},
        "shot_cache_out_dir": {"type": "d", "function": "get_shot_cache_out_dir"},
        "project_cache_dir": {"type": "d", "function": "get_project_cache_dir"},
        "shot_cam_dir": {"type": "d", "function": "get_shot_cam_dir"},
        "project_props_dir": {"type": "d", "function": "get_project_props_dir"},
        "shot_camera_file": {"type": "f", "function": "get_shot_camera_file"},
        "shot_prev_file": {"type": "f", "function": "get_shot_prev_file"},
        "shot_prev_seq": {"type": "f", "function": "get_shot_prev_seq"},
        "shot_setup": {"type": "f", "function": "get_shot_setup"},
        "scripts_dir": {"type": "d", "function": "get_scripts_dir"},
        "shot_dir": {"type": "d", "function": "get_shot_dir"},
        "working_dir": {"type": "d", "function": "get_working_dir"},
        "schema_name": {"type": "s", "function": "get_schema_name"},
        "shot_name": {"type": "s", "function": "get_shot_name"},
        "default_camera": {"type": "s", "function": "get_default_camera_name"},
        "sim_time_start": {"type": "t", "function": "get_sim_time_start"},
        "sim_time_end": {"type": "t", "function": "get_sim_time_end"},
        "prev_time_start": {"type": "t", "function": "get_prev_time_start"},
        "prev_time_end": {"type": "t", "function": "get_prev_time_end"},
        "cloth_objects": {"type": "o", "function": "get_cloth_objects"}
    }
    defaults = {
        "d": "get_working_directory",
        "f": "get_default_file",
        "o": "get_default_object",
        "p": "get_default_param",
        "v": "get_default_value"
    }

    def __init__(self, batch):
        self.batch = batch

    """ marker ATQ 001   on show form, on update form and on generate_script_from_action_template   """
    def convert_predefined_variables_to_values(self, check_str, param=""):
        for key, predefined_item in self.predefined.items():
            key_plus = "<" + key + ">"
            if check_str.find(key_plus) >= 0:
                function_to_eval = "self.{}(\"{}\")".format(predefined_item["function"], param)
                # print "\n  found var to val ", key_plus, function_to_eval, "___  in ___", check_str
                try:
                    eval_ret = str(eval(function_to_eval))
                    check_str = check_str.replace(key_plus, eval_ret)
                    # "<" + predefined_item["type"] + ">"
                except ValueError:
                    pass
                    # TODO ex
        return check_str

    """ marker ATQ 250   convert undefined to default   """
    def convert_undefined_to_default(self, template, evo_inject=None):
        # TODO optimize !
        # for de in self.defaults:
        if len(evo_inject) == 0:
            ei_str = ""
        else:
            ei_str = "evo_inject=" + str(evo_inject)

        if template is not None:
            for key, get_default in self.defaults.items():
                check = "<"+key+">"
                if template.find(check) > 0:
                    # print "check", check ,  "   get_default: " , get_default
                    try:
                        function_to_eval = "self.{}({})".format(get_default, ei_str)
                        eval_ret = eval(function_to_eval)
                        # print "eval_ret", eval_ret
                        template = template.replace(check, str(eval_ret))
                    except ValueError:
                        # TODO ex
                        pass
        return template

    def get_default_camera_name(self, evo):
        ret = self.batch.sio.generate_default_camera_name()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_schema_base_setup(self, evo):
        ret = self.batch.sio.generate_base_setup_file_name()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_ani_cache_dir(self, evo):
        ret = self.batch.sio.generate_shot_ani_cache_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_project_cache_dir(self, evo):
        ret = self.batch.sio.generate_project_cache_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_project_props_dir(self, evo):
        ret = self.batch.sio.generate_project_props_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_cache_out_dir(self, evo):
        ret = self.batch.sio.generate_shot_cache_out_path(evo_inject=evo)
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_cam_dir(self, evo):
        ret = self.batch.sio.generate_shot_cam_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_camera_file(self, evo):
        ret = self.batch.sio.generate_shot_camera_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_prev_file(self, evo):
        ret = self.batch.sio.generate_shot_prev_file(evo_inject=evo)
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_prev_seq(self, evo):
        ret = self.batch.sio.generate_shot_prev_seq(evo_inject=evo)
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_project_props_path(self, evo):
        ret = self.batch.sio.generate_project_props_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_setup(self, evo):
        ret = self.batch.sio.generate_shot_setup_file_name(evo_inject=evo)
        if ret is not False:
            return ret
        else:
            return ""

    def get_scripts_dir(self, evo):
        ret = self.batch.sio.generate_scripts_dir()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_dir(self, evo):
        ret = self.batch.sio.generate_shot_working_dir()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_working_dir(self, evo):
        if self.batch.prj.current_project is not None:
            return self.batch.prj.current_project.working_directory_absolute
        else:
            return ""

    def get_schema_name(self, evo):
        schema_name = self.batch.sch.current_schema.schema_name
        return self.batch.sio.get_flat_name(schema_name)

    def get_shot_name(self, evo):
        ret = self.batch.sio.generate_shot_name()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    #
    #
    #
    #
    #
    #
    #
    #

    def get_sim_time_start(self, evo):
        return self.batch.tsk.current_task.sim_frame_start

    def get_sim_time_end(self, evo):
        return self.batch.tsk.current_task.sim_frame_end

    def get_prev_time_start(self, evo):
        return self.batch.tsk.current_task.prev_frame_start

    def get_prev_time_end(self, evo):
        return self.batch.tsk.current_task.prev_frame_end

    def get_working_directory(self, evo):
        ret = self.batch.prj.current_project.working_directory_absolute
        if ret is not None:
            return ret
        else:
            return ""

    def get_default_file(self, evo):
        return "[default_file]"

    def get_default_object(self, evo):
        return "[default_object]"

    def get_default_param(self, evo):
        return "[default_param]"

    def get_default_value(self, evo):
        return "[default_value]"

    def get_cloth_objects(self, evo):
        if self.batch.dfn.current_definition is None:
            self.batch.logger.wrn("(get_cloth_objects) current_definition is None !")
            return ""
        else:
            # TODO interactions   exists   and    get_objects_by_type    exists
            if self.batch.dfn.current_interactions is not None:
                cloths = self.batch.dfn.current_interactions.get_objects_by_type('nCloth')
                self.batch.logger.inf(("Detected nCloth objects:", cloths))
                cloths_str = ""
                for clt in cloths:
                    cloths_str += clt + ";"
                if len(cloths_str) > 0:
                    cloths_str = cloths_str[:-1]
                return cloths_str
            else:
                self.batch.logger.inf(("(get_cloth_objects) current_definition:", self.batch.dfn.current_definition))
                self.batch.logger.wrn("(get_cloth_objects) current_interactions is None !")
                return ""


class StorageInOut:
    batch = None
    comfun = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.prj = batch.prj
        self.sts = batch.sts
        self.predefined = PredefinedVariables(batch)
        self.dir_separator = batch.sts.dir_separator

    def get_files_from_dir(self, directory, types=""):
        files = []
        dir_path = self.comfun.get_path_from_full(directory)
        if os.path.isdir(dir_path):
            for fi in os.listdir(dir_path):
                if len(types) > 0:
                    if fi.endswith(types):
                        files.append(fi)
                else:
                    files.append(fi)
        return files

    def recursive_overwrite(self, src, dest, ends_with=None):
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            for f in files:
                self.recursive_overwrite(os.path.join(src, f), os.path.join(dest, f), ends_with)
        else:
            if ends_with is None:
                shutil.copyfile(src, dest)
                self.batch.logger.inf("copied  from: {}     to: {}".format(src, dest))
            else:
                if src.endswith(ends_with):
                    shutil.copyfile(src, dest)
                    self.batch.logger.inf("copied  from: {}     to: {}".format(src, dest))
                else:
                    pass

    def copy_tree(self, src, dst, sub_dir=None):
        if sub_dir is not None:
            if len(sub_dir) > 0:
                src += sub_dir
                dst += sub_dir
            else:
                self.batch.logger.wrn("sub dir is zero size")
        try:
            self.recursive_overwrite(src, dst, ends_with=".py")
        except IOError as why:
            self.batch.logger.err("copy_tree  IOError  from: {}     to: {}\n{}".format(src, dst, why))
        except OSError as why:
            self.batch.logger.err("copy_tree  OSError  from: {}     to: {}\n{}".format(src, dst, why))
        except TypeError as why:
            self.batch.logger.err("copy_tree  TypeError  from: {}     to: {}\n{}".format(src, dst, why))
        except:
            self.batch.logger.err("copy_tree {}".format(sys.exc_info()[0]))

    def copy_file(self, src_path, dst_path, file_name, sub_dir=None):
        if sub_dir is not None:
            if len(sub_dir) > 0:
                src_path += sub_dir + self.batch.sts.dir_separator
                dst_path += sub_dir + self.batch.sts.dir_separator
            else:
                self.batch.logger.wrn("sub dir is zero size")

        src_file = src_path + file_name
        dst_file = dst_path + file_name
        try:
            shutil.copyfile(src_file, dst_file)
        except IOError as why:
            self.batch.logger.err("copy_file  IOError  from: {}     to: {}\n{}".format(src_file, dst_file, why))
        except OSError as why:
            self.batch.logger.err("copy_file  OSError  from: {}     to: {}\n{}".format(src_file, dst_file, why))
        except TypeError as why:
            self.batch.logger.err("copy_file  TypeError  from: {}     to: {}\n{}".format(src_file, dst_file, why))
        except NameError as why:
            self.batch.logger.err("copy_file  NameError  from: {}     to: {}\n{}".format(src_file, dst_file, why))
        except:
            self.batch.logger.err("copy_file {}".format(sys.exc_info()[0]))
        else:
            self.batch.logger.inf("copy_file  from: {}     to: {}\n".format(src_file, dst_file))
        
    @staticmethod
    def get_flat_name(name):
        return re.sub('\s', '_', name)

    def create_data_directory_if_not_exist(self):
        dir_path = self.batch.sts.store_data_json_directory_abs
        if self.comfun.path_exists(dir_path) is True:
            return True
        else:
            ret = self.comfun.create_directory(dir_path)
            if ret:
                self.batch.logger.inf(("Data directory created: ", dir_path))
                return True
            else:
                self.batch.logger.err(("Data directory NOT created: ", dir_path))
                return False
        
    def create_project_working_directory(self, dir_path):
        self.comfun.create_directory(dir_path)

    def create_schema_directory(self, directory):
        self.comfun.create_directory(directory + "base_setup" + self.sts.dir_separator)
        self.comfun.create_directory(directory + "shot_setup" + self.sts.dir_separator)
        self.comfun.create_directory(directory + "prevs" + self.sts.dir_separator)
        self.comfun.create_directory(directory + "cache" + self.sts.dir_separator)

    def create_example_data(self):
        self.prj.create_example_project_data(do_save=True)
        self.batch.sch.create_example_schemas_data(do_save=True)
        self.batch.tsk.create_example_tasks_data(do_save=True)
        self.batch.que.create_example_queue_data(do_save=True)
        self.batch.nod.create_example_nodes_data(do_save=True)
        self.batch.logger.inf("Created sample data")

    def create_api_example_data(self):
        api_maya_schema_id = None
        if self.batch.prj.is_project_exists("API example", msg=False) is False:
            api_project = self.batch.prj.get_example_single_project()
            api_project.project_name = "API example"
            api_project.description = "project created by API as example"
            api_project_id = self.batch.prj.add_project(api_project, do_save=True)
            if api_project_id is not None:
                self.batch.logger.inf("Created API project example")
            else:
                self.batch.logger.wrn("NOT created API project example")
                return False
        else:
            api_project_id = self.batch.prj.get_id_from_name("API example")

        if self.batch.sch.is_schema_exists("API simple Schema", msg=False) is False:
            api_simple_schema = self.batch.sch.get_example_single_schema()
            api_simple_schema.schema_name = "API simple Schema"
            api_simple_schema.description = "api schema"
            api_simple_schema.project_id = api_project_id
            
            as_def = self.batch.dfn.get_definition_by_name("Stand-alone")
            if as_def is None:
                self.batch.logger.err("Stand-alone definition NOT found!")
                self.batch.logger.err("Example data will be incomplete!")
            else:
                api_simple_schema.based_on_definition = as_def.name
                api_simple_schema.add_action_to_schema(as_def.multi_actions_array[0].actions[0])
                api_simple_schema.add_action_to_schema(as_def.multi_actions_array[1].actions[0])

            ret = self.batch.sch.add_schema(api_simple_schema, do_save=True)
            if ret is not False:
                api_schema_id = ret
                self.batch.logger.inf("Created API stand-alone schema example")
                maya_def = self.batch.dfn.get_definition_by_name("Maya")
                if maya_def is None:
                    self.batch.logger.err("Maya definition NOT found!")
                else:
                    api_maya_schema = self.batch.sch.get_example_single_schema()
                    api_maya_schema.schema_name = "API Maya Schema"
                    api_maya_schema.description = "api maya schema"
                    api_maya_schema.project_id = api_project_id
                    api_maya_schema.based_on_definition = maya_def.name
                    api_maya_schema.add_action_to_schema(maya_def.multi_actions_array[0].actions[0])
                    api_maya_schema.add_action_to_schema(maya_def.multi_actions_array[3].actions[0])
                    api_maya_schema.add_action_to_schema(maya_def.multi_actions_array[4].actions[0])
                    ret2 = self.batch.sch.add_schema(api_maya_schema, do_save=True)
                    if ret2 is not False:
                        api_maya_schema_id = ret2
                        self.batch.logger.inf("Created API Maya schema example")
            else:
                self.batch.logger.wrn("NOT created API schema example")
                return False
        else:
            api_schema_id = self.batch.sch.get_id_by_name("API simple Schema")

        if self.batch.tsk.is_task_exists("API tsk 1", msg=False) is False:
            api_task_1 = self.batch.tsk.get_blank_task()
            api_task_1.task_name = "API tsk 1"
            api_task_1.state_id = self.batch.sts.INDEX_STATE_WAITING
            api_task_1.state = self.batch.sts.states_visible_names[api_task_1.state_id]
            api_task_1.project_id = api_project_id
            api_task_1.schema_id = api_schema_id
            api_task_1.shot = "api01"
            api_task_1.description = "API example task 01"
            ret = self.batch.tsk.add_task(api_task_1, do_save=True)
            if ret is not False:
                self.batch.logger.inf("Created API task example")
                if api_maya_schema_id is not None:
                    api_task_2 = self.batch.tsk.get_blank_task()
                    api_task_2.task_name = "API maya"
                    api_task_2.state_id = self.batch.sts.INDEX_STATE_WAITING
                    api_task_2.state = self.batch.sts.states_visible_names[api_task_2.state_id]
                    api_task_2.project_id = api_project_id
                    api_task_2.schema_id = api_maya_schema_id
                    api_task_2.sequence = "K"
                    api_task_2.shot = "02"
                    api_task_2.sim_frame_end = 222
                    api_task_2.prev_frame_end = 220
                    api_task_2.description = "API maya task"
                    ret2 = self.batch.tsk.add_task(api_task_2, do_save=True)
                    if ret2 is not False:
                        self.batch.logger.inf("Created API maya task example")
                return ret
            else:
                self.batch.logger.wrn("NOT created API task example")
                return False
        else:
            return 0   # api_task_id = self.batch.tsk.get_id_by_name("API tsk 1")

    def create_unit_tests_example_data(self, do_save=False):
        if self.batch.prj.is_project_exists("pytest proj", msg=False) is False:
            ut_project = self.batch.prj.get_example_single_project()
            ut_project.project_name = "pytest proj"
            ut_project.description = "project for unit tests"
            ut_proj_id = self.batch.prj.add_project(ut_project, do_save=do_save)
            if ut_proj_id is not None:
                self.batch.logger.inf("Created unit tests project example")
            else:
                self.batch.logger.wrn("NOT created unit tests project example")
                return False
        else:
            ut_proj_id = self.batch.prj.get_id_from_name("pytest proj")

        if self.batch.sch.is_schema_exists("unit tests schema", msg=False) is False:
            ut_simple_schema = self.batch.sch.get_example_single_schema()
            ut_simple_schema.schema_name = "unit tests schema"
            ut_simple_schema.actions_array = []
            ut_simple_schema.project_id = ut_proj_id

            maya_def = self.batch.dfn.get_definition_by_name("Maya")
            if maya_def is None:
                self.batch.logger.err("Maya definition NOT found!")
            else:
                ut_simple_schema.add_action_to_schema(maya_def.multi_actions_array[0].actions[0])
                ut_simple_schema.add_action_to_schema(maya_def.multi_actions_array[3].actions[0])
                ut_simple_schema.add_action_to_schema(maya_def.multi_actions_array[4].actions[0])
                ut_simple_schema.add_action_to_schema(maya_def.multi_actions_array[5].actions[0])

            ut_schema_id = self.batch.sch.add_schema(ut_simple_schema, do_save=do_save)
            if ut_schema_id is not False:
                self.batch.logger.inf("Created API schema example")
            else:
                self.batch.logger.wrn("NOT created API schema example")
                return False
        else:
            ut_schema_id = self.batch.sch.get_id_by_name("unit tests schema")

        if self.batch.tsk.is_task_exists("unit tests tsk 1", msg=False) is False:
            ut_task_1 = self.batch.tsk.get_blank_task()
            ut_task_1.task_name = "unit tests tsk 1"
            ut_task_1.state_id = self.batch.sts.INDEX_STATE_WAITING
            ut_task_1.state = self.batch.sts.states_visible_names[ut_task_1.state_id]
            ut_task_1.project_id = ut_proj_id
            ut_task_1.schema_id = ut_schema_id
            ut_task_1.shot = "ut01"
            ut_task_1.description = "unit tests example task 01"
            ret = self.batch.tsk.add_task(ut_task_1, do_save=do_save)
            if ret is not False:
                self.batch.logger.inf("Created unit tests task example")
            else:
                self.batch.logger.wrn("NOT created unit tests task example")
                return False
        else:
            return True   # api_task_id = self.batch.tsk.get_id_by_name("API tsk 1")

    def check_any_data_to_load_exist(self):
        if self.sts.store_data_mode == 1:
            return self.get_files_from_dir(self.sts.store_data_json_directory_abs, types="json")
        else:
            return True   # TODO POR VERSION

    def get_files_from_dir_by_object_names(self, directory, obj_list, file_type="", crowd_mode=False,
                                           crowd_mode_data=("pre", "post", 2, 10)):   # TODO  crowd_mode_data  as class
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
                if os.path.isfile(directory + self.sts.dir_separator + fi):
                    fi_no_ext = fi[:-4]
                    fi_arr = fi_no_ext.split("__")
                    if self.comfun.is_float(fi_arr[1]):
                        start = int(fi_arr[1])
                    if self.comfun.is_float(fi_arr[2]):
                        end = int(fi_arr[2])
            return [1, start, end]
        else:
            return [0, 0, 0]

    def generate_base_setup_file_name(self, schema_name="", ver=None):  # from existing TASK and SCHEMA data
        if len(self.prj.projects_data) < self.prj.current_project_index or self.prj.current_project_index < 0:
            self.batch.logger.err(("Wrong current proj ID  ", self.prj.current_project_index,
                                   len(self.prj.projects_data)))
            return -1, ""
        else:
            if ver is None:
                if self.batch.sch.current_schema is not None:
                    schema_name = self.batch.sch.current_schema.schema_name
                    ver = self.batch.sch.current_schema.schema_version
                if ver is None:
                    ver = 1
                    self.batch.logger.deepdb("(load_base_setup) set default setup version 1 ")

            if len(schema_name) == 0:
                if self.batch.sch.current_schema is not None:
                    schema_name = self.batch.sch.current_schema.schema_name
                else:
                    self.batch.logger.err("(generate_base_setup...) schema_name is empty and current_schema is None")
                    return -1, ""

            proj_working_dir = self.prj.current_project.working_directory_absolute
            schema_flat_name = self.get_flat_name(schema_name)
            directory = proj_working_dir+schema_flat_name+self.dir_separator+"base_setup"+self.dir_separator
            file_version = "_v" + self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
            file_ext = self.batch.dfn.get_current_setup_ext()
            return 1, directory + schema_flat_name + file_version + "." + file_ext

    def generate_shot_setup_file_name(self, tsk_id=None, ver=None, evo_nr=None, evo_inject="", simed=False):
        if self.prj.current_project_index < 0:
            self.batch.logger.err(("Wrong current proj ID  ",self.prj.current_project_index))
            return False
        else:
            if tsk_id is None:
                if self.batch.tsk.current_task is None:
                    self.batch.logger.err("Current task is undefined!")
                    return False
                else:
                    tsk_id = self.batch.tsk.current_task.id

            if ver is None:
                    # TODO MEGA !  custom ver
                pass

            abs_shot_working_dir = self.generate_shot_working_dir()
            if abs_shot_working_dir[0] == 0:  # TODO ret FALSE or "str"
                self.batch.logger.err("abs_shot_working_dir is not generated properly")
                return False

            else:
                schema_name = self.batch.tsk.get_schema_name_from_task_id(tsk_id)
                schema_flat_name = self.get_flat_name(schema_name)
                directory = abs_shot_working_dir[1] + "shot_setup" + self.dir_separator
                if ver is None:
                    ver = self.batch.tsk.current_task.queue_ver + 1
                file_version = self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
                file_ext = self.batch.dfn.get_current_setup_ext()
                if simed is True:
                    simed_inject = "__simed__v"
                else:
                    simed_inject = "__v"
                return directory + schema_flat_name + simed_inject + file_version + evo_inject + "." + file_ext

    def generate_shot_name(self):
        if self.prj.current_project is None or \
                self.batch.sch.current_schema is None or \
                self.batch.tsk.current_task is None:
            return -1, ""
        else:
            shot_name = ""
            cur_tsk = self.batch.tsk.current_task
            if len(cur_tsk.sequence) > 0:
                shot_name += cur_tsk.sequence + "_"
            if len(cur_tsk.shot) > 0:
                shot_name += cur_tsk.shot + "_"
            if len(cur_tsk.take) > 0:
                shot_name += cur_tsk.take + "_"
            shot_name = shot_name[:-1]
            return 1, shot_name

    def generate_shot_ani_cache_dir(self):
        if self.prj.current_project is None or self.batch.tsk.current_task is None:
            return -1, ""
        else:
            shot_dir = self.prj.current_project.cache_directory_absolute
            cur_tsk = self.batch.tsk.current_task
            if len(cur_tsk.sequence) > 0:
                shot_dir += cur_tsk.sequence + self.dir_separator
            if len(cur_tsk.shot) > 0:
                shot_dir += cur_tsk.shot + self.dir_separator
            if len(cur_tsk.take) > 0:
                shot_dir += cur_tsk.take + self.dir_separator

            return 1, shot_dir

    def generate_shot_cam_dir(self):
        if self.prj.current_project is None or self.batch.tsk.current_task is None:
            return -1, ""
        else:
            shot_dir = self.prj.current_project.cameras_directory_absolute
            cur_tsk = self.batch.tsk.current_task
            if len(cur_tsk.sequence) > 0:
                shot_dir += cur_tsk.sequence + self.dir_separator
            if len(cur_tsk.shot) > 0:
                shot_dir += cur_tsk.shot + self.dir_separator
            if len(cur_tsk.take) > 0:
                shot_dir += cur_tsk.take + self.dir_separator

            return 1, shot_dir

    def generate_shot_working_dir(self):
        if self.prj.current_project is None or \
                self.batch.sch.current_schema is None or \
                self.batch.tsk.current_task is None:
            return -1, ""
        else:
            shot_dir = self.prj.current_project.working_directory_absolute
            schema_name = self.batch.sch.current_schema.schema_name
            shot_dir += self.get_flat_name(schema_name) + self.dir_separator
            cur_tsk = self.batch.tsk.current_task
            if len(cur_tsk.sequence) > 0:
                shot_dir += cur_tsk.sequence + self.dir_separator
            if len(cur_tsk.shot) > 0:
                shot_dir += cur_tsk.shot + self.dir_separator
            if len(cur_tsk.take) > 0:
                shot_dir += cur_tsk.take + self.dir_separator

            return 1, shot_dir

    def get_project_data_dir(self):
        return 1, self.batch.prj.current_project.project_directory

    def generate_project_cache_path(self):
        ret = self.get_project_data_dir()
        return ret[0], ret[1] + "cache" + self.dir_separator

    def generate_shot_ani_cache_path(self):
        ret = self.generate_shot_ani_cache_dir()
        return ret

    def generate_shot_cache_out_path(self, evo_inject=""):
        ret = self.generate_shot_working_dir()
        if ret[0] == 1:
            ver = self.batch.tsk.current_task.queue_ver + 1
            version = self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
        else:
            version = "00000"   # TODO

        return ret[0], ret[1] + "cache" + self.dir_separator + "cache_v" + version + evo_inject

    def generate_shot_cam_path(self):
        ret = self.generate_shot_cam_dir()
        # TODO find higher version file cam
        return ret

    def generate_project_props_path(self):
        ret = self.generate_shot_working_dir()
        return ret[0], ret[1] + "props" + self.dir_separator

    def generate_shot_prev_file(self, evo_inject="", seq=""):
        ret = self.generate_shot_working_dir()
        if ret[0] == 1:
            ret_file_and_path = ret[1] + "prev" + self.dir_separator
            schema_name = self.batch.sch.current_schema.schema_name
            schema_flat_name = self.get_flat_name(schema_name)
            ver = self.batch.tsk.current_task.queue_ver + 1
            file_version = self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
            file_ext = self.batch.dfn.get_current_prev_ext()
            dir_and_head_name = schema_flat_name + "__prev__v" + file_version + evo_inject
            ret_file_and_path += dir_and_head_name + self.dir_separator + dir_and_head_name + seq + "." + file_ext
            return ret[0], ret_file_and_path
        return ret

    def generate_shot_prev_seq(self, evo_inject=""):
        return self.generate_shot_prev_file(evo_inject=evo_inject, seq="__####")

    def generate_scripts_dir(self):
        ret = self.generate_shot_working_dir()
        return ret[0], ret[1] + "scripts" + self.dir_separator

    #  get directory pattern for current project
    #  pattern is generated basis on directories structure on storage
    #  used for construct new path, generate path for load
    def get_dir_patterns(self, directory):
        self.batch.logger.db(("(get_dir_patterns) deep debug start dir:", directory))
        full_dir_pattern = None
        return full_dir_pattern

    def generate_default_camera_name(self):
        # TODO "<default_camera>"
        return 1, ""





