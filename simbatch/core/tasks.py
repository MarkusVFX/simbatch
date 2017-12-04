import copy


class TaskItem():
    def __init__(self, id, task_name, schema_id, user, user_id, shot_A, shot_B, shot_C, frame_from, frame_to, state, state_id, schema_ver, queue_ver,evolution, prior, options, description, proj_id, frame_range_status, task_ver ):
        self.id = id
        self.task_name = task_name
        self.schema_id = schema_id
        self.user = user
        self.user_id = user_id
        self.shot_A = shot_A
        self.shot_B = shot_B
        self.shot_C = shot_C
        self.frame_from = frame_from
        self.frame_to = frame_to
        self.state = state
        self.state_id = state_id
        self.task_ver = task_ver
        self.schema_ver = schema_ver
        self.queue_ver = queue_ver
        self.evolution = evolution
        self.prior = prior
        self.options = options
        self.description = description
        self.proj_id = proj_id
        self.frame_range_status = frame_range_status


class Tasks:
    batch = None
    comfun = None

    tasks_data = []
    max_id = 0
    total_tasks = 0
    current_task_id = None
    current_task_index = None
    current_task = None

    def __init__(self, batch):
        self.batch = batch
        self.s = batch.s
        self.comfun = batch.comfun

    def print_all(self):
        for t in self.tasks_data:
            print " {} {}  schema_id:{}  from:{} to:{}  schema id:{}  sv:{}  tv:{}  qv:{}".format(t.task_name,
                                                                                                  t.id, t.schema_id,
                                                                                                  t.frame_from,
                                                                                                  t.frame_to, t.state,
                                                                                                  t.schema_ver,
                                                                                                  t.task_ver,
                                                                                                  t.queue_ver)

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

    def get_seq_shot_take(self, task_id=0, task_index=0, with_sh_A_dir=0):
        if task_id > 0:
            curr_index = self.get_task_index_from_id(task_id)
            curr_task = self.tasks_data[curr_index]
        else:
            if task_index > 0:
                curr_task = self.tasks_data[task_index]
            else:
                curr_task = self.tasks_data[self.current_task_index]
        ret = ""
        if len(curr_task.shot_A) > 0:
            if with_sh_A_dir == 0:
                ret = curr_task.shot_A
            else:
                ret = curr_task.shot_A + "\\" + curr_task.shot_A
        if len(curr_task.shot_B) > 0:
            if len(ret) > 0:
                ret += "_"+curr_task.shot_B
            else:
                ret = curr_task.shot_B
        if len(curr_task.shot_C) > 0:
            if len(ret) > 0:
                ret += "_"+curr_task.shot_C
            else:
                ret = curr_task.shot_C
        return ret

    def get_task_frame_range(self):
        curr_task = self.tasks_data[self.current_task_index]
        return [self.comfun.int_or_val(curr_task.frame_from, 1), self.comfun.int_or_val(curr_task.frame_to, 2)]

    def create_example_project_data(self,  schema_id, proj_id):
        sample_task_1 = TaskItem(0, "schema tre", schema_id, "M", 1, "01", "001", "a", 10, 20, "Waiting", 2, "a.max",
                                 1, "evo01", 5, "inp:1,1,1", "first task", proj_id, 0, 1)
        sample_task_2 = TaskItem(0, "schema tre", schema_id, "M", 1, "01", "002", "", 10, 20, "Waiting", 2, "a.max",
                                 1, "evo10", 5, "inp:1,1,1", "first task", proj_id, 0, 1)
        sample_task_3 = TaskItem(0, "schema tre", schema_id, "M", 1, "03", "456", "fix", 10, 20, "Waiting", 2, "a.max",
                                 44, "evo22", 5, "inp:1,1,1", "first task", proj_id, 0, 1)
        self.add_task(sample_task_1)
        self.add_task(sample_task_2)
        self.add_task(sample_task_3)
        self.save_tasks()
        return self.max_id

    def add_task(self, task_item, do_save=False):
        if task_item.id > 0:
            self.max_id = task_item.id
        else:
            self.max_id += 1
            task_item.id = self.max_id
        self.tasks_data.append(task_item)
        self.total_tasks += 1
        if do_save is True:
            self.save_tasks()

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

    def clear_all_tasks_data(self):
        del self.tasks_data[:]
        self.max_id = 0
        self.total_tasks = 0
        self.current_task_id = None
        self.current_task_index = None

    def load_tasks(self):
        if self.s.store_data_mode == 1:
            self.load_tasks_from_json()
        if self.s.store_data_mode == 2:
            self.load_tasks_from_mysql()

    def load_tasks_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.s.batch_data_path + self.s.tasks_file_name
        # TODO

    def load_tasks_from_mysql(self):
        # PRO VERSION
        if self.s.debug_level >= 3:
            print "  [INF] relational database available in the PRO version"

    def save_tasks(self):
        if self.s.store_data_mode == 1:
            self.save_tasks_to_json()
        if self.s.store_data_mode == 2:
            self.save_tasks_to_mysql()

    def save_tasks_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.s.batch_data_path + self.s.tasks_file_name
        # TODO

    def save_tasks_to_mysql(self):
        # PRO VERSION
        if self.s.debug_level >= 3:
            print "  [INF] relational database available in the PRO version"






