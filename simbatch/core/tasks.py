import copy
import os
from queue import QueueItem

# JSON Name Format, PEP8 Name Format
TASK_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'task_name'),
    ('stateId', 'state_id'),
    ('state', 'state'),
    ('project', 'project_id'),
    ('schema', 'schema_id'),
    ('sequence', 'sequence'),
    ('shot', 'shot'),
    ('take', 'take'),
    ('simFrStart', 'sim_frame_start'),
    ('simFrEnd', 'sim_frame_end'),
    ('prevFrStart', 'prev_frame_start'),
    ('prevFrEnd', 'prev_frame_end'),
    ('schVer', 'schema_ver'),
    ('tskVer', 'task_ver'),
    ('queVer', 'queue_ver'),
    ('options', 'options'),
    ('user', 'user_id'),
    ('prior', 'priority'),
    ('desc', 'description')]


class TaskOptions:
    """ class used for store and exchange options on "add to queue process" """
    """ marker TO (TaskOptions)   class   """
    proxy_task = None

    def __init__(self, task):
        self.proxy_task = copy.deepcopy(task)

    def set_task_value(self, param, val):
        if hasattr(self.proxy_task, param):
            setattr(self.proxy_task, param, val)
            return True
        else:
            return False


class TaskItem:
    def __init__(self, task_id, task_name, state_id, state, project_id, schema_id, sequence, shot, take,
                 sim_frame_start, sim_frame_end, prev_frame_start, prev_frame_end, schema_ver, task_ver, queue_ver,
                 options, user_id, priority, description):
        self.id = task_id
        self.task_name = task_name
        self.state_id = state_id
        self.state = state
        self.project_id = project_id
        self.schema_id = schema_id
        self.sequence = sequence
        self.shot = shot
        self.take = take
        self.sim_frame_start = sim_frame_start
        self.sim_frame_end = sim_frame_end
        self.prev_frame_start = prev_frame_start
        self.prev_frame_end = prev_frame_end
        self.schema_ver = schema_ver
        self.task_ver = task_ver
        self.queue_ver = queue_ver
        self.options = options
        self.user_id = user_id
        self.priority = priority
        self.description = description


class Tasks:
    batch = None
    comfun = None

    tasks_data = []
    max_id = 0
    total_tasks = 0
    current_task_id = None
    current_task_index = None
    current_task = None

    sample_data_checksum = None
    sample_data_total = None

    proxy_task = None         # used on add to queue process
    proxy_task_evos = None    # store current evolutions

    def __init__(self, batch):
        self.batch = batch
        self.logger = batch.logger
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.tasks_data = []

    @staticmethod
    def get_blank_task():
        return TaskItem(0, "", 1, "NULL", 1, 1, "01", "001", "", 100, 101, 100, 101, 1, 1, 1, "", 1, 50, "")

    #  print project data, mainly for debug
    def print_task(self, task=None):
        prefix = ""
        if task is None:
            prefix = "current "
            if self.current_task_id is not None:
                print "       current task index:{}, id:{}, total:{}".format(self.current_task_index,
                                                                             self.current_task_id,
                                                                             self.total_tasks)
                task = self.current_task
            else:
                self.batch.logger.wrn("current task undefined, nothing to print")
                return False

        print "       {}task name:{}".format(prefix, task.task_name)
        print "       schemaID:{}        projID:{}".format(task.schema_id, task.project_id)
        print "       seq/shot/take: {} {} {}".format(task.sequence, task.shot, task.take)
        print "       sim frame range {} {} ".format(task.sim_frame_start, task.sim_frame_end)
        print "       prev frame range {} {} ".format(task.prev_frame_start, task.prev_frame_end)
        print "       state:{}   state_id:{} ".format(task.state, task.state_id)
        print "       options ", task.options
        print "       description ", task.description
        base_setup_name = self.batch.sch.get_base_setup(use_task_id=str(self.current_task_id))
        print "       base setup: ", base_setup_name

    def print_current(self):
        self.print_task()

    def print_all(self):
        if self.total_tasks == 0:
            print "   [INF] no schema loaded"
        for t in self.tasks_data:
            print "\n\n {} {}  schema_id:{}  ".format(t.task_name, t.id, t.schema_id)
            print "from:{} to:{}  state:{}  sv:{}  tv:{}  qv:{}".format(t.sim_frame_start, t.sim_frame_end, t.state,
                                                                        t.schema_ver, t.task_ver, t.queue_ver)
        print "\n\n"

    def get_index_by_id(self, get_id):
        for i, tsk in enumerate(self.tasks_data):
            if tsk.id == get_id:
                return i
        self.batch.logger.wrn(("no task with ID: ", get_id))
        return None
        
    def get_id_by_name(self, name, msg=True):
        for tsk in self.tasks_data:
            if tsk.task_name == name:
                return tsk.id
        if msg:
            self.batch.logger.wrn(("no task with name: ", name))
        return None
        
    def is_task_exists(self, name, msg=True):
        if self.get_id_by_name(name, msg=msg) is None:
            return False
        else:
            return True

    def get_task_by_id(self, task_id):
        index = self.get_index_by_id(task_id)
        if index is not None:
            return self.tasks_data[index]

    def update_current_from_id(self, get_id):
        for i, tsk in enumerate(self.tasks_data):
            if tsk.id == get_id:
                self.current_task_index = i
                self.current_task_id = get_id
                self.current_task = tsk
                return i
        self.current_task_index = None
        self.current_task_id = None
        self.current_task = None
        self.logger.wrn(("no task with ID: ", get_id))
        return None

    def update_current_from_index(self, index):
        if len(self.tasks_data) > index >= 0:
            self.current_task_id = self.tasks_data[index].id
            self.current_task_index = index
            self.current_task = self.tasks_data[index]
            return self.current_task_id
        else:
            self.current_task_index = None
            self.current_task_id = None
            self.current_task = None
            return False

    def get_seq_shot_take(self, task_id=0, task_index=0, with_sequence_dir=0):
        if task_id > 0:
            curr_index = self.get_index_by_id(task_id)
            curr_task = self.tasks_data[curr_index]
        else:
            if task_index > 0:
                curr_task = self.tasks_data[task_index]
            else:
                curr_task = self.tasks_data[self.current_task_index]
        ret = ""
        if len(curr_task.sequence) > 0:
            if with_sequence_dir == 0:
                ret = curr_task.sequence
            else:
                ret = curr_task.sequence + "\\" + curr_task.sequence
        if len(curr_task.shot) > 0:
            if len(ret) > 0:
                ret += "_"+curr_task.shot
            else:
                ret = curr_task.shot
        if len(curr_task.take) > 0:
            if len(ret) > 0:
                ret += "_"+curr_task.take
            else:
                ret = curr_task.take
        return ret

    def get_task_frame_range(self):
        curr_task = self.tasks_data[self.current_task_index]
        return[self.comfun.int_or_val(curr_task.sim_frame_start, 1), self.comfun.int_or_val(curr_task.sim_frame_end, 2)]

    def get_schema_name_from_task_id(self, task_id):
        get_tsk = self.get_task_by_id(task_id)
        get_sch = self.batch.sch.get_schema_by_id(get_tsk.schema_id)
        return get_sch.schema_name

    def create_example_tasks_data(self, do_save=True):
        collect_ids = 0
        sample_task_1 = TaskItem(0, "tsk 1", 1, "INIT", 1, 1,  "01", "001", "", 10, 20, 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_2 = TaskItem(0, "tsk 2", 1, "INIT", 1, 2,  "01", "002", "", 10, 20, 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_3 = TaskItem(0, "tsk 3", 1, "INIT", 2, 3,  "02", "004", "b", 7, 28, 8, 22, 4, 5, 6, "o", 1, 8, "d")
        sample_task_4 = TaskItem(0, "tsk 4", 1, "INIT", 3, 4,  "10", "022", "", 10, 20, 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_5 = TaskItem(0, "tsk 5", 1, "INIT", 3, 4,  "40", "070", "", 10, 20, 10, 20, 1, 1, 1, "", 1, 50, "")
        collect_ids += self.add_task(sample_task_1)
        collect_ids += self.add_task(sample_task_2)
        collect_ids += self.add_task(sample_task_3)
        collect_ids += self.add_task(sample_task_4)
        collect_ids += self.add_task(sample_task_5, do_save=do_save)
        self.sample_data_checksum = 15
        self.sample_data_total = 5
        return collect_ids

    def check_is_task_exist(self, task_item):
        for ta in self.tasks_data:
            if ta.schema_id == task_item.schema_id:
                if ta.sequence == task_item.sequence:
                    if ta.shot == task_item.shot:
                        if ta.take == task_item.take:
                            if ta.id != task_item.id:
                                return ta.id
        return False

    def add_task(self, task_item, do_save=False):
        if task_item.id > 0:
            self.max_id = task_item.id
        else:
            self.max_id += 1
            task_item.id = self.max_id
        self.tasks_data.append(task_item)
        self.total_tasks += 1
        if do_save is True:
            if self.save_tasks():
                return task_item.id
            else:
                return False
        else:
            return task_item.id

    def update_task(self, edited_task_item, do_save=False):
        if 0 <= self.current_task_index < len(self.tasks_data):
            self.tasks_data[self.current_task_index] = copy.deepcopy(edited_task_item)
            if do_save is True:
                return self.save_tasks()
            return True
        else:
            self.logger.err(("wrong current_task_id:", self.current_task_index))
            return False

    def set_state(self, task_id, state):
        index = 0
        for q in self.tasks_data:
            if q.id == task_id:
                self.tasks_data[index].state = state
                break
            index += 1

    def increase_queue_ver(self):
        self.current_task.queue_ver += 1
        self.current_task.state_id = self.sts.INDEX_STATE_QUEUED
        self.current_task.state = self.sts.states_visible_names[self.sts.INDEX_STATE_QUEUED]
        self.save_tasks()

    def remove_single_task(self, index=None, task_id=None, do_save=False):
        if index is None and task_id is None:
            return False
        if task_id > 0:
            for i, tsk in enumerate(self.tasks_data):
                if tsk.id == task_id:
                    del self.tasks_data[i]
                    self.total_tasks -= 1
                    break
        if index >= 0:
            del self.tasks_data[index]
            self.total_tasks -= 1
        if do_save is True:
            return self.save_tasks()
        else:
            return True

    def delete_json_tasks_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_TASKS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)
        else:
            return True

    def clear_json_tasks_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_TASKS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return self.comfun.save_to_file(json_file, "")
        else:
            return True

    def clear_tasks_in_mysql(self):
        # PRO VERSION with sql
        self.logger.inf("MySQL will be supported with the PRO version")
        return False

    def clear_all_tasks_data(self, clear_stored_data=False):
        del self.tasks_data[:]
        self.max_id = 0
        self.total_tasks = 0
        self.current_task_id = None
        self.current_task_index = None
        # TODO check clear UI val (last current...)
        if clear_stored_data:
            return self.save_tasks()
        return True

    def load_tasks(self):
        if self.sts.store_data_mode == 1:
            return self.load_tasks_from_json()
        if self.sts.store_data_mode == 2:
            return self.load_tasks_from_mysql()

    def load_tasks_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_TASKS_FILE_NAME
        if self.comfun.file_exists(json_file, info="tasks file"):
            self.logger.inf(("loading tasks: ", json_file))
            json_tasks = self.comfun.load_json_file(json_file)
            if json_tasks is not None and "tasks" in json_tasks.keys():
                if json_tasks['tasks']['meta']['total'] > 0:
                    for li in json_tasks['tasks']['data'].values():
                        if len(li) == len(TASK_ITEM_FIELDS_NAMES):
                            new_task_item = TaskItem(int(li['id']), li['name'], int(li['stateId']), li['state'],
                                                     int(li['project']), int(li['schema']), li['sequence'],
                                                     li['shot'], li['take'],
                                                     int(li['simFrStart']), int(li['simFrEnd']),
                                                     int(li['prevFrStart']), int(li['prevFrEnd']),
                                                     int(li['schVer']), int(li['tskVer']), int(li['queVer']),
                                                     li['options'], int(li['user']), int(li['prior']), li['desc'])
                            self.add_task(new_task_item)
                        else:
                            self.logger.wrn(("task json data not consistent: ", len(li), len(TASK_ITEM_FIELDS_NAMES)))
                else:
                    self.logger.wrn(("no tasks data in: ", json_file))
                return True
            else:
                self.logger.err(("wrong format data: ", json_file))
        else:
            self.logger.err(("no schema file: ", json_file))
        return False

    def load_tasks_from_mysql(self):
        # PRO VERSION
        self.logger.inf("MySQL will be supported with the PRO version")
        return None

    def save_tasks(self):
        if self.sts.store_data_mode == 1:
            return self.save_tasks_to_json()
        if self.sts.store_data_mode == 2:
            return self.save_tasks_to_mysql()

    def format_tasks_data(self, json=False, sql=False, backup=False):
        if json == sql == backup is False:
            self.logger.err("(format_projects_data) no format param !")
        else:
            if json or backup:
                tim = self.comfun.get_current_time()
                formated_data = {"tasks": {"meta": {"total": self.total_tasks,
                                                    "timestamp": tim,
                                                    "jsonFormat": "http://json-schema.org/"
                                                    },
                                           "data": {}}}
                for i, td in enumerate(self.tasks_data):
                    tsk = {}
                    for field in TASK_ITEM_FIELDS_NAMES:
                        tsk[field[0]] = eval('td.'+field[1])
                    formated_data["tasks"]["data"][i] = tsk
                return formated_data
            else:
                # PRO version with SQL
                return False

    # save tasks data as json
    def save_tasks_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_TASKS_FILE_NAME
        content = self.format_tasks_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_tasks_to_mysql(self):
        # PRO VERSION
        self.logger.inf("MySQL will be supported with the PRO version")
        return None

    #
    # #
    # # # #
    # # # # #
    # section #      adding task to queue

    """ marker TO (TaskOptions)   create object   """
    def create_task_options_object(self, task=None):
        if task is None:
            if self.current_task is None:
                task = self.get_blank_task()
            else:
                task = self.current_task
        return TaskOptions(task)

    def clear_proxy_task(self):
        self.proxy_task = None

    def update_proxy_task_form_current(self):
        if self.current_task is not None:
            self.update_proxy_task(self.current_task.id)
        else:
            self.logger.err("skipped update_proxy_task_form_current , current task is None")

    def update_proxy_task(self, task_id=None, task_ver=None, priority=None, sim_frame_start=None, sim_frame_end=None,
                          prev_frame_start=None, prev_frame_end=None, description=None, from_task=None):
        if task_id is not None:
            if self.comfun.is_int(task_id):
                index = self.get_index_by_id(task_id)
                self.proxy_task = copy.deepcopy(self.tasks_data[index])
                self.logger.db(("update_proxy_task from id:", task_id))
            else:
                self.logger.err(("skipped update_proxy_task, wrong id:", task_id))
        if task_ver is not None:
            self.proxy_task.task_ver = task_ver
        if priority is not None:
            self.proxy_task.priority = priority
        if sim_frame_start is not None:
            self.proxy_task.sim_frame_start = sim_frame_start
        if sim_frame_end is not None:
            self.proxy_task.sim_frame_end = sim_frame_end
        if prev_frame_start is not None:
            self.proxy_task.prev_frame_start = prev_frame_start
        if prev_frame_end is not None:
            self.proxy_task.prev_frame_end = prev_frame_end
        if description is not None:
            self.proxy_task.description = description
        if from_task is not None:
            self.proxy_task = copy.deepcopy(from_task)

    """
    def generate_evo_script(self, hymm):
        self.batch.logger.wrn(" TODO generate_evo_script ")
        return " eval("+hymm+") ...  WIP  TODO "   # TODO
    """

    """
    def generate_queue_items_from_proxy_task_XXX(self, evolutions=None, schema_options=None, task_options=None):
        # TODO   WIP
        queue_items = []

        if self.proxy_task is not None:
            task_to_add = self.proxy_task  # self.batch.tsk.tasks_data[task_index]
            schema_index = self.batch.sch.get_index_by_id(task_to_add.schema_id)
            schema_to_queued = self.batch.sch.schemas_data[schema_index]
            task_definition = self.batch.dfn.get_definition_by_name(schema_to_queued.based_on_definition)
            if task_definition is None:
                self.batch.logger.err(("Missing definition: ", schema_to_queued.based_on_definition))
                return None

            if schema_options is None:
                schema_options = self.batch.sch.create_schema_options_object(schema_to_queued)
            schema_options_proxy = schema_options.proxy_schema

            if task_options is None:
                task_options = self.batch.tsk.create_task_options_object(task_to_add)
            task_options_proxy = task_options.proxy_task

            "" x marker SO (SchemaOptions)   send to compile   ""
            "" x marker TO (TaskOptions)   send to compile   ""
            template_queue_item = self.generate_template_queue_item(task_to_add, schema_to_queued, task_options_proxy)
            print "evolutions:" , evolutions  ### ['Bnd 111 222']
            if template_queue_item is not None:
                if evolutions is None or len(evolutions) == 0:
                    template_queue_item.generate_queue_item_name(task_to_add, with_update=True)
                    template_queue_item.evolution = ""

                    #script = schema_to_queued.generate_script_from_Xactions(self.batch)
                    #script = self.batch.sio.predefined.convert_var_to_val_in_script(script)
                    #script = self.batch.sio.predefined.convert_undefined_to_default(script)
                    script = schema_to_queued.generate_script_from_Xactions(self.batch)
                    template_queue_item.evolution_script = script

                    template_queue_item.description = self.proxy_task.description
                    queue_items.append(template_queue_item)

                else:
                    # evolutions = [  "BND 4 5; DMP 7"  ,      "BRN: 1 2 3"  ]    # example for 2 engines !!!
                    for engine_index, evos in enumerate(evolutions):
                        print "eeevvvooooo" , evos  ### Bnd 111 222
                        inject_evo_scr_arr = schema_to_queued.get_evo_scripts_array(self.batch, evos, engine_index)
                        print "schema_to_queued ", schema_to_queued
                        print "schema_to_queued a arr ", schema_to_queued.actions_array
                        print "evo_scr_arr ", inject_evo_scr_arr
                        for j, evo_scr in enumerate(inject_evo_scr_arr[1]):
                            j1 = j+1
                            print "eeevvvo_scr ", evo_scr   ### interactions.set_evo_param(<o>.bendResistance = 111.0);
                            queue_item = copy.deepcopy(template_queue_item)

                            queue_item.generate_queue_item_name(task_to_add, with_update=True,
                                                                with_sufix=" [e:"+str(j1)+"]")
                            # queue_item.evolution = "["+str(i)+"] "+evo_scr[0]
                            queue_item.evolution = inject_evo_scr_arr[0][j]
                            queue_item.evolution_nr = engine_index

                            script = schema_to_queued.generate_script_from_Xactions(self.batch, evo_scr=evo_scr,
                                                                                   engine_index=engine_index)

                            print "\n\n zzzz SCR : \n", script

                            script = self.batch.sio.predefined.convert_var_to_val_in_script(script, evo_index=j1)
                            # script = self.batch.sio.predefined.convert_undefined_to_default(script, evo_index=j1)
                            queue_item.evolution_script = script

                            # queue_item.description = "[{}] {}".format(j, self.proxy_task.description)
                            queue_item.description = self.proxy_task.description
                            queue_items.append(queue_item)
            else:
                self.batch.logger.wrn("template_queue_item is None")
        else:
            self.batch.logger.wrn("Proxy task is None")
        return queue_items
    """

    """ marker ATQ 010b   on API command   """
    """
    def generate_queue_items_from_task(self, task_id, evolutions=None, schema_options=None, task_options=None):
        self.update_proxy_task(task_id)
        return self.generate_queue_items_from_proxy_task(evolutions=evolutions, schema_options=schema_options,
                                                         task_options=task_options)
    """
    # def apply_evolutions_to_task(self, evo, task=None):
        # if task is None:
        #     task = self.proxy_task

        # task.schema_id
        #  task.schema_ver

        # self.proxy_task_evos

        # add_to_queue
        # get_blank_task
        # self.batch.que.add_to_queue()








