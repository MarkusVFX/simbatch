#
# For network and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
# JSON Name Format, PEP8 Name Format
NODES_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'node_name'),
    ('stateId', 'state_id'),
    ('state', 'state'),
    ('stateFile', 'state_file'),
    ('desc', 'description')]


class SingleNode:
    def __init__(self, node_id, node_name, state, state_id, state_file, description):
        self.id = node_id
        self.node_name = node_name
        self.state = state
        self.state_id = state_id
        self.state_file = state_file
        self.description = description


class SimNodes:
    batch = None
    comfun = None
    sts = None

    nodes_data = []
    total_nodes = 0

    current_node_id = None
    current_node_index = None
    current_node = None

    max_id = 0

    def __init__(self, batch):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.nodes_data = []

    def print_current(self):
        if self.current_node_index is not None and self.current_node_index > 0:
            n = self.nodes_data[self.current_node_index]
            self.batch.logger.raw((" node: ", n.node_name, n.state, n.description))
        else:
            self.batch.logger.raw((" no current node, index: ", self.current_node_index))

    def print_all(self):
        for n in self.nodes_data:
            self.batch.logger.raw((" node: ", n.node_name, n.state, n.state_id, n.description, n.state_file))

    def get_index_by_id(self, get_id):
        for i, nod in enumerate(self.nodes_data):
            if nod.id == get_id:
                return i
        self.batch.logger.wrn(("no node with ID: ", get_id))
        return None

    #  update id, index and current for fast use by all modules
    def update_current_from_index(self, index):
        if 0 <= index < self.total_nodes:
            self.current_node_index = index
            self.current_node_id = self.nodes_data[index].id
            self.current_node = self.nodes_data[index]
            return True
        else:
            self.current_node_id = None
            self.current_node = None
            self.batch.logger.err(("(update_current_from_index) wrong index:", index))
            self.batch.logger.err(" total:{}  len:{}".format(self.total_nodes, len(self.nodes_data)))
            return False

    @staticmethod
    def get_new_node(node_name, node_state, node_state_id, state_file, desc):
        return SingleNode(0, node_name, node_state, node_state_id, state_file, desc)

    def add_simnode(self, single_node, do_save=False):
        if single_node.id > 0:
            self.max_id = single_node.id
        else:
            self.max_id += 1
            single_node.id = self.max_id
        self.nodes_data.append(single_node)
        self.total_nodes += 1
        if do_save is True:
            return self.save_nodes()
        else:
            return True

    def update_from_nodes(self, with_save=False):
        """  update current nodes_data from simnodes  """
        changes_count = 0
        for nod in self.nodes_data:
            real_node_state_id = self.get_node_state(nod.state_file)
            if nod.state_id != real_node_state_id:
                if real_node_state_id < 0:
                    nod.state_id = self.batch.sts.INDEX_STATE_OFFLINE
                    nod.state = self.batch.sts.states_visible_names[self.batch.sts.INDEX_STATE_OFFLINE]
                    changes_count += 1
                else:
                    nod.state_id = real_node_state_id
                    nod.state = self.batch.sts.states_visible_names[real_node_state_id]
                    changes_count += 1
            if with_save and changes_count > 0:
                self.save_nodes()

    def remove_node(self, node_id, do_save=False):
        for i, node in enumerate(self.nodes_data):
            if node.id == node_id:
                del self.nodes_data[i]
                self.total_nodes -= 1
                break

        if do_save is True:
            return self.save_nodes()
        else:
            return True

    def load_nodes(self):
        if self.batch.sts.store_data_mode == 1:
            return self.load_nodes_from_json()
        if self.batch.sts.store_data_mode == 2:
            return self.load_nodes_from_mysql()

    def load_nodes_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.batch.sts.store_data_json_directory_abs + self.batch.sts.JSON_SIMNODES_FILE_NAME
        if self.comfun.file_exists(json_file, info="simnodes file"):
            self.batch.logger.inf(("loading simnodes: ", json_file))
            json_nodes = self.comfun.load_json_file(json_file)
            if json_nodes is not None and "simnodes" in json_nodes.keys():
                if json_nodes['simnodes']['meta']['total'] > 0:
                    for li in json_nodes['simnodes']['data'].values():
                        if len(li) == len(NODES_ITEM_FIELDS_NAMES):
                            new_simnode_item = SingleNode(int(li['id']), li['name'], li['state'],
                                                          int(li['stateId']), li['stateFile'], li['desc'])
                            self.add_simnode(new_simnode_item)
                        else:
                            self.batch.logger.wrn(("simnode json data not consistent: ", len(li),
                                                   len(NODES_ITEM_FIELDS_NAMES)))
                else:
                    self.batch.logger.inf(("no nodes data in : ", json_file))
                return True
            else:
                self.batch.logger.err(("wrong format data in: ", json_file))
        else:
            self.batch.logger.err(("no simnodes file: ", json_file))
        return False

    def load_nodes_from_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    def save_nodes(self):
        if self.batch.sts.store_data_mode == 1:
            return self.save_nodes_to_json()
        if self.batch.sts.store_data_mode == 2:
            return self.save_nodes_to_myqsl()

    def save_nodes_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_SIMNODES_FILE_NAME
        content = self.format_nodes_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def format_nodes_data(self, json=False, sql=False, backup=False):
        if json == sql == backup is False:
            self.batch.logger.err("(format_nodes_data) no format param !")
        else:
            if json or backup:
                tim = self.comfun.get_current_time()
                formated_data = {"simnodes": {"meta": {"total": self.total_nodes,
                                                       "timestamp": tim,
                                                       "jsonFormat": "http://json-schema.org/"
                                                       },
                                              "data": {}}}
                for i, td in enumerate(self.nodes_data):
                    nod = {}
                    for field in NODES_ITEM_FIELDS_NAMES:
                        nod[field[0]] = eval('td.'+field[1])
                    formated_data["simnodes"]["data"][i] = nod
                return formated_data
            else:
                # PRO version with SQL
                return False

    def save_nodes_to_myqsl(self):
        # PRO VERSION
        self.batch.logger.inf("PRO version with SQL")

    def clear_all_nodes_data(self, clear_stored_data=False):
        del self.nodes_data[:]
        self.max_id = 0
        self.total_nodes = 0
        self.current_node_id = -1
        self.current_node_index = -1
        if clear_stored_data:
            return self.save_nodes()
        return True

    def get_node_state(self, state_file):     # TODO tryToCreateIfNotExist = False,
        if self.comfun.file_exists(state_file, "get state file txt"):
            f = open(state_file, 'r')
            first_line = f.readline()
            f.close()
            if len(first_line) > 0:
                li = first_line.split(";")
            else:
                li = [-1]
                self.batch.logger.deepdb((" [db] len(first_line) : ", len(first_line), " ___ ", len(first_line)))

            state_int = self.comfun.int_or_val(li[0], -1)
            self.batch.logger.deepdb((" [db] get state_int : ", state_int))
            return state_int
        else:
            return -1

    def create_node_state_file(self, state_file, server_name, state):
        if self.comfun.file_exists(state_file, "set state file txt") is False:
            self.batch.logger.deepdb((" [db] set state : ", state))
            try:
                f = open(state_file, 'w')
                f.write(str(state) + ";" + server_name + ";" + self.comfun.get_current_time())
                f.close()
            except IOError:
                self.logger.err(("Creating state file error:", state_file))
                return False
            return True
        else:
            self.batch.logger.err(("[ERR] state file NOT created, file exist: ", state_file))
            return False

    def set_node_state(self, state_file, server_name, state):
        if self.comfun.file_exists(state_file, "set state file txt"):
            self.batch.logger.deepdb((" [db] set state : ", state))
            try:
                f = open(state_file, 'w')
                f.write(str(state) + ";" + server_name + ";" + self.comfun.get_current_time())
                f.close()
            except IOError:
                self.batch.logger.err(("[ERR] node state file NOT updated: ", state_file))
                return False
            return True
        else:
            self.batch.logger.err(("[ERR] file set state not exist: ", state_file))
            return False

    def get_server_name_from_file(self, server_state_file):
        if self.comfun.file_exists(server_state_file, "get_server_name_from_file"):
            f = open(server_state_file, 'r')
            first_line = f.readline()
            f.close()
            if len(first_line) > 0:
                li = first_line.split(";")
                if len(li) > 0:
                    return li[1]
                else:
                    self.batch.logger.wrn(("sim node name missing: ", li))
                    return ""
            else:
                self.batch.logger.wrn(("len(first_line): ", len(first_line)))
                return ""
        else:
            self.batch.logger.err(("server state file not exist: ", server_state_file))
            return ""


#
# For network and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
