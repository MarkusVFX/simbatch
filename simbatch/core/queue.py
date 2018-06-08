import os

# JSON Name Format, PEP8 Name Format
QUEUE_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'queue_item_name'),
    ('taskId', 'task_id'),
    ('user', 'user'),
    ('userId', 'user_id'),
    ('sequence', 'sequence'),
    ('shot', 'shot'),
    ('take', 'take'),
    ('frameFrom', 'frame_from'),
    ('frameTo', 'frame_to'),
    ('state', 'state'),
    ('stateId', 'state_id'),
    ('ver', 'version'),
    ('evo', 'evolution'),
    ('evoNr', 'evolution_nr'),
    ('evoScript', 'evolution_script'),
    ('prior', 'prior'),
    ('desc', 'description'),
    ('simNode', 'sim_node'),
    ('simNodeId', 'sim_node_id'),
    ('time', 'time'),
    ('projId', 'proj_id'),
    ('softId', 'soft_id')
    ]


class QueueItem:
    total_items = 0
    max_id = 0

    def __init__(self, id, queue_item_name, task_id, user, user_id, sequence, shot, take, frame_from, frame_to, state,
                 state_id, ver, evo, evo_nr, evo_script, prior, description, sim_node, sim_node_id, time, proj_id, soft_id):
        self.id = id
        self.queue_item_name = queue_item_name
        self.task_id = task_id
        self.user = user
        self.user_id = user_id
        self.sequence = sequence
        self.shot = shot
        self.take = take
        self.frame_from = frame_from
        self.frame_to = frame_to
        self.state = state
        self.state_id = state_id
        self.version = ver
        self.evolution = evo
        self.evolution_nr = evo_nr
        self.evolution_script = evo_script
        self.prior = prior
        self.description = description
        self.sim_node = sim_node
        self.sim_node_id = sim_node_id
        self.time = time
        self.proj_id = proj_id   # TODO  change to project_id
        self.soft_id = soft_id


class Queue:
    batch = None
    comfun = None

    queue_data = []
    total_queue_items = 0
    max_id = 0

    current_queue_id = None
    current_queue_index = None
    current_queue = None

    sample_data_checksum = 0
    sample_data_total = 0

    def __init__(self, batch):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.queue_data = []

    #  print project data, mainly for debug
    def print_header(self):
        print "\n QUEUE: "
        print "     current project: id: {}     index: {}    total_projects: {}\n".format(self.current_queue_id,
                                                                                          self.current_queue_index,
                                                                                          self.total_queue_items)

    def print_current(self):
        print "       current queue index:{}, id:{}, total:{}".format(self.current_queue_index, self.current_queue_id,
                                                                      self.total_queue_items)
        if self.current_queue_index is not None:
            cur_que = self.current_queue
            print "       current queue name:{}".format(cur_que.queue_name)

    def print_all(self):
        if self.total_queue_items == 0:
            print "   [INF] no queu items loaded"
        for q in self.queue_data:
            print "\n\n {}  {}  {}  {} state:{}   evo:{}   simnode:{}  desc:{}".format(q.id, q.queue_item_name, q.prior,
                                                                                       q.proj_id, q.state, q.evolution,
                                                                                       q.sim_node, q.description,
                                                                                       q.proj_id)
        print "\n\n"

    @staticmethod
    def get_blank_queue_item():
        return QueueItem(0, "", 1, "M", 1, "", "", "", 10, 20, "NULL", 0, "ver", "evo", 0, "script", 50, " 1 ", "", 0, "", 1, 3)

    def get_queue_index_by_id(self, get_id):
        for i, que in enumerate(self.queue_data):
            if que.id == get_id:
                return i
        self.batch.logger.wrn(("(get index by id) no queue item with id: ", get_id))
        return None

    def get_first_with_state(self, state_id, soft=0):
        for index, q in enumerate(self.queue_data):
            if q.state_id == state_id:
                if soft > 0:
                    if q.soft_id == soft:
                        return (index, self.queue_data[index].id)
                else:
                    return (index, self.queue_data[index].id)
        return (-1, -1)

    def set_state(self, id, state, state_id, server_name="", server_id=-1, set_time=0, add_current_time=False):
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

    def delete_json_queue_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_QUEUE_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)
        else:
            return True

    @staticmethod
    def clear_queue_items_in_mysql():
        # PRO VERSION with sql
        return False

    def clear_all_queue_items(self, clear_stored_data=False):
        del self.queue_data[:]
        self.max_id = 0
        self.total_queue_items = 0
        self.current_queue_id = None
        self.current_queue_index = None
        # TODO check clear UI val (last current...)
        if clear_stored_data:
            if self.sts.store_data_mode == 1:
                if self.delete_json_queue_file():
                    return True
                else:
                    return False
            if self.sts.store_data_mode == 2:
                if self.clear_queue_items_in_mysql():
                    return True
                else:
                    return False
        return True

    def add_to_queue(self, queue_item, do_save=False):
        if queue_item.id > 0:
            self.max_id = queue_item.id
        else:
            self.max_id += 1
            queue_item.id = self.max_id
        self.queue_data.append(queue_item)
        self.total_queue_items += 1

        if do_save is True:
            if self.save_queue():
                return queue_item.id
            else:
                return False
        return queue_item.id


    def remove_single_queue_item(self, index=None, id=None, do_save=False):
        if index is None and id is None:
            return False
        if id > 0:
            for i, que in enumerate(self.queue_data):
                if que.id == id:
                    del self.queue_data[i]
                    self.total_queue_items -= 1
                    break
        if index >= 0:
            del self.queue_data[index]
            self.total_queue_items -= 1
        if do_save is True:
            return self.save_queue()
        else:
            return True

    def generate_queue_items(self, task_id, options=None):
        # TODO
        # TODO
        # TODO
        # TODO
        print "\n  !!! TODO compile2 ", task_id, options
        return self.get_blank_queue_item()

    # prepare 'queue_data' for backup or save
    def format_queue_data(self, json=False, sql=False, backup=False):
        if json == sql == backup is False:
            self.batch.logger.err("(format_queue_data) no format param !")
        else:
            if json or backup:
                tim = self.comfun.get_current_time()
                formated_data = {"queueItems": {"meta": {"total": self.total_queue_items,
                                                         "timestamp": tim,
                                                         "jsonFormat": "http://json-schema.org/"},
                                                "data": {}}}
                for i, qu in enumerate(self.queue_data):
                    que = {}
                    for field in QUEUE_ITEM_FIELDS_NAMES:
                        que[field[0]] = eval('qu.'+field[1])
                    formated_data["queueItems"]["data"][i] = que
                return formated_data
            else:
                # PRO version with SQL
                return False

    def create_example_queue_data(self, do_save=True):
        collect_ids = 0
        sample_queue_item_1 = QueueItem(0, "queue item 1", 1, "T", 1, "", "", "", 1, 2, "DONE", 11, 3, "", 0,
                                        "script", 50, "first", "sim_01", 1, "2017_12_28 02:02:02", 1, 1)
        sample_queue_item_2 = QueueItem(0, "queue item 2", 3, "T", 1, "", "", "", 3, 4, "WORKING", 4, 2, "", 0,
                                        "script", 50, "second", "sim_01", 1, "2017_12_28 02:02:03", 1, 1)
        sample_queue_item_3 = QueueItem(0, "queue item 3", 4, "T", 1, "", "", "", 5, 6, "WAITING", 2, 1, "", 0,
                                        "script", 40, "third", "sim_01", 1, "2017_12_28 02:02:04", 1, 1)
        collect_ids += self.add_to_queue(sample_queue_item_1)
        collect_ids += self.add_to_queue(sample_queue_item_2)
        collect_ids += self.add_to_queue(sample_queue_item_3, do_save=do_save)
        self.sample_data_checksum = 6
        self.sample_data_total = 3
        return collect_ids

    def load_queue(self):
        if self.sts.store_data_mode == 1:
            self.load_queue_from_json()
        if self.sts.store_data_mode == 2:
            self.load_queue_from_mysql()

    def load_queue_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_QUEUE_FILE_NAME
        if self.comfun.file_exists(json_file, info="queue file"):
            self.batch.logger.inf(("loading queue items: ", json_file))

        else:
            self.batch.logger.wrn(("queue file doesn't exist: ", json_file))
        return False

    def load_queue_from_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    def save_queue(self):
        if self.sts.store_data_mode == 1:
            return self.save_queue_to_json()
        if self.sts.store_data_mode == 2:
            return self.save_queue_to_mysql()

    def save_queue_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory + self.sts.JSON_QUEUE_FILE_NAME
        content = self.format_queue_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_queue_to_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None
