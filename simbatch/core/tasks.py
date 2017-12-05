import copy
import os

TASK_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'task_name'),
    ('state_id', 'state_id'),
    ('state', 'state'),
    ('project', 'project_id'),
    ('schema', 'schema_id'),
    ('sequence', 'sequence'),
    ('shot', 'shot'),
    ('take', 'take'),
    ('frame_from', 'frame_from'),
    ('frame_to', 'frame_to'),
    ('sch_ver', 'schema_ver'),
    ('tsk_ver', 'task_ver'),
    ('que_ver', 'queue_ver'),
    ('options', 'options'),
    ('user', 'user_id'),
    ('prior', 'priority'),
    ('desc', 'description')]


class TaskItem:
    def __init__(self, task_id, task_name, state_id, state, project_id, schema_id, sequence, shot, take,
                 frame_from, frame_to, schema_ver, task_ver, queue_ver, options, user_id, prior, description):
        self.id = task_id
        self.task_name = task_name
        self.state_id = state_id
        self.state = state
        self.project_id = project_id
        self.schema_id = schema_id
        self.sequence = sequence
        self.shot = shot
        self.take = take
        self.frame_from = frame_from
        self.frame_to = frame_to
        self.schema_ver = schema_ver
        self.task_ver = task_ver
        self.queue_ver = queue_ver
        self.options = options
        self.user_id = user_id
        self.priority = prior
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

    def __init__(self, batch):
        self.batch = batch
        self.s = batch.s
        self.comfun = batch.comfun

    #  print project data, mainly for debug
    def print_current(self):
        print "       current task index:{}, id:{}, total:{}".format(self.current_task_index, self.current_task_id,
                                                                     self.total_tasks)
        if self.current_task_id is not None:
            cur_tsk = self.current_task
            print "       current task name:{}".format(cur_tsk.task_name)
            print "       schemaID:", cur_tsk.schemaID, "       projID:", cur_tsk.projID
            print "       shotDetails ", cur_tsk.shotA, "   ", cur_tsk.shotB, "   ", cur_tsk.shotC
            print "       frameFrom  frameTo ", cur_tsk.frameFrom, cur_tsk.frameTo
            print "       state  state_id ", cur_tsk.state, "    ", cur_tsk.state_id

    def print_all(self):
        if self.total_tasks == 0:
            print "   [INF] no schema loaded"
        for t in self.tasks_data:
            print "\n\n {} {}  schema_id:{}  ".format(t.task_name, t.id, t.schema_id)
            print "from:{} to:{}  state:{}  sv:{}  tv:{}  qv:{}".format(t.frame_from, t.frame_to, t.state,
                                                                        t.schema_ver, t.task_ver, t.queue_ver)
        print "\n\n"

    def get_task_index_from_id(self, get_id):
        for i, tsk in enumerate(self.tasks_data):
            if tsk.id == get_id:
                return i
        if self.s.debug_level >= 2:
            print "   [WRN] no task with ID: ", get_id
        return None

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
        if self.s.debug_level >= 2:
            print "   [WRN] no task with ID: ", get_id
        return None

    def update_current_from_index(self, index):
        if len(self.tasks_data) > index >= 0:
            self.current_task_id = self.tasks_data[index].id
            self.current_task_index = index
            self.current_task = self.tasks_data[index]
        else:
            self.current_task_index = None
            self.current_task_id = None
            self.current_task = None

    def get_seq_shot_take(self, task_id=0, task_index=0, with_sequence_dir=0):
        if task_id > 0:
            curr_index = self.get_task_index_from_id(task_id)
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
        return [self.comfun.int_or_val(curr_task.frame_from, 1), self.comfun.int_or_val(curr_task.frame_to, 2)]

    def create_example_tasks_data(self, do_save=True):
        collect_ids = 0
        sample_task_1 = TaskItem(0, "task 1", 1, "INIT", 1, 1,  "01", "001", "", 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_2 = TaskItem(0, "task 2", 1, "INIT", 1, 1,  "01", "001", "", 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_3 = TaskItem(0, "task 3", 1, "INIT", 2, 1,  "01", "001", "", 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_4 = TaskItem(0, "task 4", 1, "INIT", 3, 1,  "01", "001", "", 10, 20, 1, 1, 1, "", 1, 50, "")
        sample_task_5 = TaskItem(0, "task 5", 1, "INIT", 3, 1,  "01", "001", "", 10, 20, 1, 1, 1, "", 1, 50, "")
        collect_ids += self.add_task(sample_task_1)
        collect_ids += self.add_task(sample_task_2)
        collect_ids += self.add_task(sample_task_3)
        collect_ids += self.add_task(sample_task_4)
        collect_ids += self.add_task(sample_task_5, do_save=do_save)
        self.sample_data_checksum = 15
        self.sample_data_total = 5
        self.save_tasks()
        return collect_ids

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
                self.save_tasks()
        else:
            if self.s.debug_level >= 1:
                print "  [ERR] wrong current_task_id:", self.current_task_index

    def set_state(self, task_id, state):
        index = 0
        for q in self.tasks_data:
            if q.id == task_id:
                self.tasks_data[index].state = state
                break
            index += 1

    def remove_task(self, task_id):
        index = 0
        for t in self.tasks_data:
            if t.id == task_id:
                del self.tasks_data[index]
                break
            index += 1

    def delete_json_tasks_file(self, json_file=None):
        if json_file is None:
            json_file = self.s.store_data_json_directory + self.s.JSON_TASKS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)

    def clear_tasks_in_mysql(self):
        # PRO VERSION with sql
        pass

    def clear_all_tasks_data(self, clear_stored_data=False):
        del self.tasks_data[:]
        self.max_id = 0
        self.total_tasks = 0
        self.current_task_id = None
        self.current_task_index = None
        # TODO check clear UI val (last current...)
        if clear_stored_data:
            if self.s.store_data_mode == 1:
                if self.delete_json_tasks_file():
                    return True
                else:
                    return False
            if self.s.store_data_mode == 2:
                if self.clear_tasks_in_mysql():
                    return True
                else:
                    return False
        return True

    def load_tasks(self):
        if self.s.store_data_mode == 1:
            self.load_tasks_from_json()
        if self.s.store_data_mode == 2:
            self.load_tasks_from_mysql()

    def load_tasks_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.s.store_data_json_directory + self.s.JSON_TASKS_FILE_NAME
        if self.comfun.file_exists(json_file, info="tasks file"):
            if self.s.debug_level >= 2:
                print " [INF] loading tasks: " + json_file
            json_tasks = self.comfun.load_json_file(json_file)

            if "tasks" in json_tasks.keys():
                if json_tasks['tasks']['meta']['total'] > 0:
                    for li in json_tasks['tasks']['data'].values():
                        if len(li) == len(TASK_ITEM_FIELDS_NAMES):
                            new_task_item = TaskItem(int(li['id']), li['name'], int(li['state_id']), li['state'],
                                                         int(li['version']), int(li['proj_id']), li['proj'],
                                                         int(li['definition']), new_schema_actions, li['desc'])

                            self.add_task(new_task_item)
                    return True
            else:
                if self.s.debug_level >= 2:
                    print " [WRN] no projects data in : ", json_file
                return False
        else:
            if self.s.debug_level >= 1:
                print " [ERR] no schema file: " + json_file
                return False

    def load_tasks_from_mysql(self):
        # PRO VERSION
        if self.s.debug_level >= 3:
            print "  [INF] relational database available in the PRO version"

    def save_tasks(self):
        if self.s.store_data_mode == 1:
            return self.save_tasks_to_json()
        if self.s.store_data_mode == 2:
            return self.save_tasks_to_mysql()

    def format_tasks_data(self, json=False, sql=False, backup=False):
        if json == sql == backup == False:
            if self.s.debug_level >= 1:
                print " [ERR] (format_projects_data) no format param !"
        else:
            if json or backup:
                tim = self.comfun.get_current_time()
                formated_data = {"tasks": {"meta": {"total": self.total_tasks, "timestamp": tim}, "data": {}}}
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
            json_file = self.s.store_data_json_directory + self.s.JSON_TASKS_FILE_NAME
        content = self.format_tasks_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_tasks_to_mysql(self):
        # PRO VERSION
        if self.s.debug_level >= 3:
            print "  [INF] relational database available in the PRO version"






