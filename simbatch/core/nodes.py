#
# For network and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
# JSON Name Format, PEP8 Name Format

import os

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

    def __str__(self):
        return f"SingleNode  node_id:{self.id}  node_name:{self.node_name}  state:{self.state}  state_id:{self.state_id}  state_file:{self.state_file}  description:{self.description}"


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

    """  vars used as server mode (not framework_mode)  """
    state_file = None
    server_name = None

    def __init__(self, batch):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.nodes_data = []

    def print_current(self):
        self.print_node(self.current_node_index, prefix="current ")
            
    def print_node(self, index, prefix=""):
        if index is not None and index >= 0:
            if index < self.total_nodes:
                n = self.nodes_data[index]
                self.batch.logger.raw(f"{os.linesep}{os.linesep} {prefix} node: {n.node_name}  {n.state}  {n.description}")
            else:
                self.batch.logger.raw(f"{os.linesep} no {prefix} node with index: {index} ")
        else:
            self.batch.logger.raw(f"{os.linesep} no {prefix} node, index: {index} ")

    def print_all(self):
        self.batch.logger.raw(f"{os.linesep} Total nodes in database: {self.total_nodes}")
        if self.batch.sts.master_directory_abs is not None:
            self.batch.logger.raw(f"{os.linesep} Source dir: {self.batch.sts.master_directory_abs}")
        for n in self.nodes_data:
            self.batch.logger.raw(f"{os.linesep} {n.id} {n.node_name}    {n.state} ({n.state_id})  {n.description} {os.linesep}  {n.state_file}")

    def get_index_by_id(self, get_id):
        for i, nod in enumerate(self.nodes_data):
            if nod.id == get_id:
                return i
        self.batch.logger.wrn(f"no node with ID: {get_id}")
        return None
        
    """ get node by name | return False if no node, index if one, -count if found > 0 """
    def get_node_index_by_name(self, name, force_db=False):
        return self.get_node_index_by_param(name=name, force_db=force_db)
    
    def get_node_index_by_state_file(self, state_file, force_db=False):
        return self.get_node_index_by_param(state_file=state_file, force_db=force_db)
    
    def get_node_index_by_param(self, name=None, state_file=None, force_db=False):
        nod_count = 0 
        nod_last_index = None
        for i, nodi in enumerate(self.nodes_data):
            if name is not None:
                if nodi.node_name == name:
                    nod_count += 1
                    nod_last_index = i
            if state_file is not None:
                if nodi.state_file == state_file:
                    nod_count += 1
                    nod_last_index = i
        if force_db:
            self.batch.logger.deepdb(f"(gnibp) found:{str(nod_last_index)} count:{nod_count} by name:{name}", force_print=force_db)
        if nod_last_index is None:
            return False
        elif nod_count == 1:
            return nod_last_index
        else:
            return nod_count*-1
        
            
    #  update id, index and current for fast use by all modules
    def update_current_from_index(self, index):
        if index is None:
            self.current_node_id = None
            self.current_node = None
            self.current_node_index = None
            self.batch.logger.wrn("(update_current_from_index) index is None")
            return False
        elif 0 <= index < self.total_nodes:
            self.current_node_index = index
            self.current_node_id = self.nodes_data[index].id
            self.current_node = self.nodes_data[index]
            return True
        else:
            self.current_node_id = None
            self.current_node = None
            self.current_node_index = None
            self.batch.logger.err(f"(update_current_from_index) wrong index: {index}")
            self.batch.logger.err(f" total:{self.total_nodes}  len:{len(self.nodes_data)}")
            return False
            
    def set_node_state_in_database(self, index, state_id):
        if index >= 0 and index < len(self.nodes_data):
            self.nodes_data[index].state = self.batch.sts.states_visible_names[state_id]   # TODO test arr len and index
            self.nodes_data[index].state_id = state_id 
            return self.save_nodes()
        else:
            self.batch.logger.err(f"Wrong node index:{index} ! State NOT updated!")

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

    def detect_duplicates_by_state_file(self):   # TODO  remove if dup exist
        dup_count = 0
        dup_last = None
        dup_last_id = None
        for i, nodi in enumerate(self.nodes_data):
            for j, nodj in enumerate(self.nodes_data):
                if i != j:
                    if nodi.state_file == nodj.state_file:
                        dup_count += 1
                        dup_last = nodi.state_file
                        dup_last_id = nodi.id

        if dup_count > 0:
            self.batch.logger.wrn(f"Simnode duplicates found ({dup_count}) in database. Last id: {dup_last_id}, file:{dup_last}")
        return dup_count, dup_last_id

    def update_from_nodes(self, with_save=False):
        """  update current nodes_data from simnodes  """
        changes_count = 0
        self.reload_nodes()
        for nod in self.nodes_data:
            node_info = self.get_node_info_from_state_file(nod.state_file)
            if node_info is not None:
                real_node_state_id = node_info.state_id
                if nod.state_id != real_node_state_id:
                    if real_node_state_id < 0:
                        nod.state_id = self.batch.sts.INDEX_STATE_OFFLINE
                        nod.state = self.batch.sts.states_visible_names[self.batch.sts.INDEX_STATE_OFFLINE]
                        changes_count += 1
                    else:
                        nod.state_id = real_node_state_id
                        nod.state = self.batch.sts.states_visible_names[real_node_state_id]
                        changes_count += 1

                if node_info.node_name is not None:
                    if nod.node_name != node_info.node_name:
                        nod.node_name = node_info.node_name
                        changes_count += 1
            else:
                self.batch.logger.wrn(f"No access to: {nod.state_file}")

        if with_save and changes_count > 0:
            return self.save_nodes(), changes_count
        else:
            return True, changes_count

    def remove_node(self, node_id, do_save=False):
        self.reload_nodes()
        for i, node in enumerate(self.nodes_data):
            if node.id == node_id:
                del self.nodes_data[i]
                self.total_nodes -= 1
                break

        if do_save is True:
            return self.save_nodes()
        else:
            return True

    def reload_nodes(self):
        current_id = self.current_node_id
        self.clear_all_nodes_data()
        self.load_nodes()
        if current_id is not None:
            idx = self.get_index_by_id(current_id)
            self.update_current_from_index(idx)

    def load_nodes(self):
        if self.batch.sts.store_data_mode == 1:
            return self.load_nodes_from_json()
        if self.batch.sts.store_data_mode == 2:
            return self.load_nodes_from_mysql()

    def load_nodes_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = os.path.join(self.batch.sts.store_data_json_directory_abs, self.batch.sts.JSON_SIMNODES_FILE_NAME)

        if self.comfun.file_exists(json_file, info="simnodes file"):
            self.batch.logger.inf(f"loading simnodes: {json_file}")
            json_nodes = self.comfun.load_json_file(json_file)
            if json_nodes is not None and "simnodes" in json_nodes.keys():
                if json_nodes['simnodes']['meta']['total'] > 0:
                    for li in json_nodes['simnodes']['data'].values():
                        if len(li) == len(NODES_ITEM_FIELDS_NAMES):
                            new_simnode_item = SingleNode(int(li['id']), li['name'], li['state'],
                                                          int(li['stateId']), li['stateFile'], li['desc'])
                            self.add_simnode(new_simnode_item)
                        else:
                            self.batch.logger.wrn(f"simnode json data not consistent: {len(li)}, {len(NODES_ITEM_FIELDS_NAMES)}")
                else:
                    self.batch.logger.inf(f"no nodes data in : {json_file}")
                return True
            else:
                self.batch.logger.err(f"wrong format data in: {json_file}")
        else:
            self.batch.logger.err(f"no simnodes file: {json_file}")
        return False

    def load_nodes_from_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    def save_nodes(self):
        if self.batch.sts.store_data_mode == 1:
            return self.save_nodes_to_json()
        if self.batch.sts.store_data_mode == 2:
            return self.save_nodes_to_mysql()
            
    def save_nodes_to_json(self, json_file=None):
        if json_file is None:
            json_file = f"{self.sts.store_data_json_directory_abs}{os.sep}{self.sts.JSON_SIMNODES_FILE_NAME}"
        content = self.format_nodes_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def format_nodes_data(self, json=False, sql=False, backup=False):
        if json == sql == backup is False:
            self.batch.logger.err("(format_nodes_data) no format param !")
        else:
            if json or backup:
                tim = self.comfun.get_current_time()
                formatted_data = {"simnodes": {"meta": {"total": self.total_nodes,
                                                        "timestamp": tim,
                                                        "jsonFormat": "http://json-schema.org/"},
                                               "data": {}}}
                for i, td in enumerate(self.nodes_data):
                    nod = {}
                    for field in NODES_ITEM_FIELDS_NAMES:
                        nod[field[0]] = eval('td.'+field[1])
                    formatted_data["simnodes"]["data"][i] = nod
                return formatted_data
            else:
                # PRO version with SQL
                return False

    def save_nodes_to_mysql(self):
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
        
    """   
    
    """
    
    """
    
    operations on local state file   
    
    """

    def get_state_file(self, server_name=None):
        if server_name is not None:
            for nod in self.nodes_data:
                if nod.node_name == server_name:
                    return nod.state_file
            return False
        else:  # try get from current
            if self.current_node is not None:
                return self.current_node.state_file
            else:
                return False

    def get_node_info_from_state_file(self, state_file):
        if self.comfun.file_exists(state_file, "get state file txt"):
            with open(state_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            if len(first_line) > 0:
                li = first_line.split(";")
                state_int = self.comfun.int_or_val(li[0], -1)
                if state_int > 0:
                    self.batch.logger.deepdb(f"State from file : {state_int}")
                    server_name = li[1]
                    state_name = self.batch.sts.states_visible_names[state_int]
                    node_info = SingleNode(-1, server_name, state_name, state_int, state_file, "info from state file")
                    return node_info
                else:
                    self.batch.logger.err(f"State file err, wrong status value : {li[0]}")
                    return False
            else:
                self.batch.logger.err(f"First line of state file is empty : {state_file}")
                return False
        else:
            return None

    def get_node_state(self, state_file):     # TODO tryToCreateIfNotExist = False,
        if self.comfun.file_exists(state_file, "get state file txt"):
            with open(state_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            if len(first_line) > 0:
                li = first_line.split(";")
            else:
                li = [-1]
                self.batch.logger.deepdb(f" [db] len(first_line) : {len(first_line)} ___ {len(first_line)}")

            state_int = self.comfun.int_or_val(li[0], -1)
            self.batch.logger.deepdb(f" [db] get state_int : {state_int}")
            return state_int
        else:
            return -1

    def create_node_state_file(self, state_file, server_name, state, update_mode=False):
        if self.comfun.file_exists(state_file, info=False) is False or update_mode:
            self.batch.logger.deepdb(f" [db] set state : {state}")
            try:
                with open(state_file, 'w', encoding='utf-8') as f:
                    f.write(f"{state};{server_name};{self.comfun.get_current_time()}")
            except IOError:
                if update_mode is False:
                    self.batch.logger.err(f"Creating state file error: {state_file}")
                else:
                    self.batch.logger.err(f"Update state file error: {state_file}")
                return False
            return True
        else:
            if update_mode is False:
                self.batch.logger.err(f"[ERR] state file NOT created, file exist: {state_file}")
            else:
                self.batch.logger.err(f"[ERR] state file NOT updated, file exist: {state_file}")
            return False

    def check_node_as_server(self, must_also_check_database):
        if self.state_file is not None:
            if self.server_name is not None:
                if must_also_check_database:
                    # return self.batch.    #WIP TODO
                    return True
                else:
                    return True
            else:
                self.logger.err("Server name NOT set!")
        else:
            self.logger.err("Path to server state file NOT set!")
        return False

    def set_curent_node_state(self, state_id, must_set_in_database=True):
        """ check class variables and test acces to database if needed """
        ret = self.check_node_as_server(must_also_check_database=must_set_in_database)

        if ret is False:
            self.logger.err(f"State {state_id} NOT set! Wrong server init")
            return False
        else:
            state_file = self.state_file
            server_name = self.server_name

            if self.comfun.file_exists(state_file, "set state file txt"):
                up = True
            else:
                up = False
                
            ret = self.create_node_state_file(state_file, server_name, state_id, update_mode=up)
            if ret:
                return True
            else:
                return False

    def get_server_name_from_file(self, server_state_file):
        if self.comfun.file_exists(server_state_file, "get_server_name_from_file"):
            with open(server_state_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            if len(first_line) > 0:
                li = first_line.split(";")
                if len(li) > 0:
                    return li[1]
                else:
                    self.batch.logger.wrn(f"sim node name missing: {li}")
                    return ""
            else:
                self.batch.logger.wrn(f"len(first_line): {len(first_line)}")
                return ""
        else:
            self.batch.logger.err(f"server state file not exist: {server_state_file}")
            return ""

    def create_example_nodes_data(self, do_save=True):
        state_off = self.sts.states_visible_names[self.sts.INDEX_STATE_OFFLINE]
        state_off_id = self.sts.INDEX_STATE_OFFLINE
        state_file = f"{os.sep}srv{os.sep}simbatch{os.sep}server_1{os.sep}state.txt"
        example_node = SingleNode(0, "example sim node", state_off, state_off_id, state_file, "example node 1")
        self.add_simnode(example_node, do_save=do_save)
        return True

    def print_node_log(self, executor=False):
        if self.current_node is None:
            self.batch.logger.wrn("No node selected")
        else:
            log_dir = self.comfun.dirname(self.current_node.state_file)
            if executor:
                executor_inject = "executor_"
            else:
                executor_inject = ""
            log_file = f"{log_dir}{os.sep}{executor_inject}log.txt"
            content = self.comfun.load_from_file(log_file)
            self.batch.logger.raw(content)

    def print_node_executor_log(self):
        self.print_node_log(executor=True)


#
# For network and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
