

# JSON Name Format, PEP8 Name Format
QUEUE_ITEM_FIELDS_NAMES = [
    ('id', 'id')]

class QueueItem():
    total_items = 0
    max_id = 0

    def __init__(self, id, queue_item_name, task_id, user, user_id, shot_A, shot_B, shot_C, frame_from, frame_to, state,
                 state_id, version, evolution, evolution_nr, evolution_script_type, evolution_script, prior,
                 description, sim_node, sim_node_id, time, proj_id, soft_id):
        if id > 0:
            self.max_id = id
        else:
            self.max_id += 1
        self.total_items += 1

        self.id = self.max_id
        self.queue_item_name = queue_item_name
        self.task_id = task_id
        self.user = user
        self.user_id = user_id
        self.shot_A = shot_A
        self.shot_B = shot_B
        self.shot_C = shot_C
        self.frame_from = frame_from
        self.frame_to = frame_to
        self.state = state
        self.state_id = state_id
        self.version = version
        self.evolution = evolution
        self.evolution_nr = evolution_nr
        self.evolution_script_type = evolution_script_type
        self.evolution_script = evolution_script
        self.prior = prior
        self.description = description
        self.sim_node = sim_node
        self.sim_node_id = sim_node_id
        self.time = time
        self.proj_id = proj_id
        self.soft_id = soft_id


class Queue:
    batch = None
    comfun = None

    queue_data = []
    total_queue_items = 0

    current_queue_id = None
    current_queue_index = None
    current_queue = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.queue_data = []

    #  print project data, mainly for debug
    def print_header(self):
        print "\n QUEUE: "
        print "     current project: id: {}     index: {}    total_projects: {}\n".format(self.current_queue_id,
                                                                                          self.current_queue_index,
                                                                                          self.total_queue_items)

    def print_current(self):
        print "       current task index:{}, id:{}, total:{}".format(self.current_queue_index, self.current_queue_id,
                                                                     self.total_queue_items)
        if self.current_queue_index is not None:
            cur_que = self.current_queue
            print "       current queue name:{}".format(cur_que.queue_name)

    def print_all(self):
        if self.total_queue_items == 0:
            print "   [INF] no queu items loaded"
        for q in self.queue_data:
            print "\n\n ", q.queue_name
            # TODO
        print "\n\n"

    def get_queue_index_by_id(self, get_id):
        for i, que in enumerate(self.queue_data):
            if que.id == get_id:
                return i
        print "   [WRN] (get index by )no queue item with ID: ", get_id
        return None

    def get_first_with_state (self, state_id, soft=0):
        index = 0
        for q in self.queue_data :
            if q.state_id == state_id :
                # print " [db] state : "+str(q.state_id)+"    q.soft_id: ",  q.soft_id
                if soft > 0 :
                    if q.soft_id == soft:
                        return index, self.queue_data[index].id
                else:
                    return index, self.queue_data[index].id
            index += 1
        return -1, -1

    def set_state (self, id, state, state_id, server_name="", server_id=-1, set_time=0, add_current_time=False):
        for i, q in enumerate(self.queue_data):
            if q.id == id:
                self.queue_data[i].state = state
                self.queue_data[i].state_id = state_id
                self.queue_data[i].sim_node = server_name
                self.queue_data[i].sim_node_id = server_id
                if add_current_time:
                    self.queue_data[i].description = "[{}]  {}".format(self.comfun.get_current_time(only_time=True),
                                                                       self.queue_data[i].description)
                elif set_time > 0:
                    time_string = self.comfun.format_seconds_to_string(set_time)
                    self.queue_data[i].description = "[{}]  {}".format(time_string,
                                                                       self.queue_data[i].description)
                return True
        return False


    def clear_all_queue_items(self):
        del self.queue_data[:]
        self.max_id = 0
        self.total_queue_jobs = 0
        self.current_queue_index = -1
        self.current_queue_index = -1
        self.last_queue_index = -1

    def format_queue_data(self, json=False, sql=False, backup=False):
        if json == sql == backup == False:
            if self.s.debug_level >= 1:
                print " [ERR] (format_queue_data) no format param !"
        else:
            return False


    def load_queue(self):
        if self.s.store_data_mode == 1 :
            self.load_queue_from_json()
        if self.s.store_data_mode == 2 :
            self.load_queue_from_mysql()


    def load_queue_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.s.store_data_json_directory + self.s.JSON_QUEUE_FILE_NAME
        if self.comfun.file_exists(json_file, info="queue file"):
            if self.s.debug_level >= 3:
                print " [INF] loading queue items: " + json_file
        return False

    def load_queue_from_mysql(self):
        ### PRO VERSION
        return False

    def save_queue(self):
        if self.s.store_data_mode == 1 :
            self.save_queue_to_json()
        if self.s.store_data_mode == 2 :
            self.save_queue_to_mysql()

    def save_queue_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
        content = self.format_queue_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_queue_to_mysql(self):
        ### PRO VERSION
        return False







