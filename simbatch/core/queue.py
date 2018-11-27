import os
import copy

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
    def __init__(self, queue_item_id, queue_item_name, task_id, user, user_id, sequence, shot, take,
                 frame_from, frame_to, state, state_id, ver, evo, evo_nr, evo_script, prior,
                 description, sim_node, sim_node_id, time, proj_id, soft_id):
        self.id = queue_item_id
        self.queue_item_name = queue_item_name
        self.task_id = task_id
        self.user = user
        self.user_id = user_id
        self.sequence = sequence
        self.shot = shot
        self.take = take
        self.frame_from = frame_from    # TODO  use it   or   remove
        self.frame_to = frame_to        # TODO  use it   or   remove
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

    def __str__(self):
        return "QueueItem: {},{},{},... ,{},{},{},... ,{},{},{},{} ".format(self.id, self.queue_item_name, self.task_id,
                                                                            self.sequence, self.shot, self.take,
                                                                            self.version, self.evolution,
                                                                            self.evolution_nr, self.evolution_script)

    def print_this(self):
        print "\n QUEUE ITEM: {}".format(self.queue_item_name)
        print "   id: {}   [seq|sh|tk] : [{}|{}|{}] \n".format(self.id, self.sequence, self.shot, self.take)
        print "   ver:{}  evo_nr: {}   evo: {}    \n".format(self.version, self.evolution_nr, self.evolution)
        print "   state:{}  state_id: {}    \n".format(self.state, self.state_id)
        print "   evolution_script:{}\n".format(self.evolution_script)

    """ marker ATQ 220   generate name   """
    def generate_queue_item_name(self, task, with_update=False, with_sufix=None):
        name = task.task_name + " "
        if len(task.sequence) > 0:
            name += task.sequence + "_"
        if len(task.shot) > 0:
            name += task.shot + "_"
        if len(task.take) > 0:
            name += task.take

        if name[-1] == "_":
            name = name[:-1]
        name += "  v:"+str(task.queue_ver)
        if with_sufix is not None:
            name += with_sufix
        if with_update:
            self.queue_item_name = name
        return name

    def get_evolution_script_with_nl(self):
        es = self.evolution_script
        es_arr = es.split(";")
        return "\n           " + "\n          ".join(es_arr)


class Queue:
    """  store info about all queue items """
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

    '''   print project data, mainly for debug  '''
    def print_info(self):
        print "\n QUEUE: "
        print "     current queue item id: {}   index: {}   total queue items: {}\n".format(self.current_queue_id,
                                                                                            self.current_queue_index,
                                                                                            self.total_queue_items)

    def print_current(self):
        print " QUEUE INFO:   items total:{}, current index:{}, current id:{}".format(self.total_queue_items, 
                                                                                      self.current_queue_index,
                                                                                      self.current_queue_id)
        if self.current_queue_index is not None:
            self.current_queue.print_this()

    def print_all(self):
        if self.total_queue_items == 0:
            print "   [INF] no queue items loaded"
        for q in self.queue_data:
            print "\n\n {}  {}  {}  {} state:{}   evo:{}   simnode:{}  desc:{}".format(q.id, q.queue_item_name, q.prior,
                                                                                       q.proj_id, q.state, q.evolution,
                                                                                       q.sim_node, q.description,
                                                                                       q.proj_id)
        print "\n\n"

    @staticmethod
    def get_blank_queue_item():
        return QueueItem(0, "", 1, "M", 1, "", "", "", 10, 20, "NULL", 0, 1, "", 0, "", 50, " 1 ", "", 0, "", 1, 3)

    def get_index_by_id(self, get_id):
        for i, que in enumerate(self.queue_data):
            if que.id == get_id:
                return i
        self.batch.logger.wrn(("(get index by id) no queue item with id: ", get_id))
        return None

    def update_current_from_id(self, queue_id):
        for i, que in enumerate(self.queue_data):
            if que.id == queue_id:
                self.current_queue_index = i
                self.current_queue_id = queue_id
                self.current_queue = que
                return i
        self.clear_current_queue_item()
        return False

    def set_last_as_current(self):
        self.update_current_from_id(self.queue_data[-1].id)

    def clear_current_queue_item(self):
        self.current_queue_id = None
        self.current_queue_index = None
        self.current_queue = None

    def get_first_with_state_id(self, state_id, soft=0):
        for index, q in enumerate(self.queue_data):
            if q.state_id == state_id:
                if soft > 0:
                    if q.soft_id == soft:
                        return index, self.queue_data[index].id
                else:
                    return index, self.queue_data[index].id
        return -1, -1

    def update_state_and_node_name(self, queue_id, state, state_id, server_name="", server_id=-1, set_time=None,
                              add_current_time=False):
        for i, q in enumerate(self.queue_data):
            if q.id == queue_id:
                self.queue_data[i].state = state
                self.queue_data[i].state_id = state_id
                self.queue_data[i].sim_node = server_name
                self.queue_data[i].sim_node_id = server_id
                if add_current_time:
                    if len(self.queue_data[i].description) > 3:
                        if self.queue_data[i].description[0] == "[":
                            en = self.queue_data[i].description.find("]")
                            if en > 0:
                                self.queue_data[i].description = self.queue_data[i].description[en+1:]
                    self.queue_data[i].description = "[{}]  {}".format(self.comfun.get_current_time(only_time=True),
                                                                       self.queue_data[i].description)
                elif set_time is not None:
                    if len(self.queue_data[i].description) > 3:
                        if self.queue_data[i].description[0] == "[":
                            en = self.queue_data[i].description.find("]")
                            if en > 0:
                                self.queue_data[i].description = self.queue_data[i].description[en+1:]
                    time_string = self.comfun.format_seconds_to_string(set_time)
                    self.queue_data[i].description = "[{}]  {}".format(time_string, self.queue_data[i].description)
                return True
        return False

    def delete_json_queue_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_QUEUE_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)
        else:
            return True

    def clear_json_queue_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_QUEUE_FILE_NAME
        if self.comfun.file_exists(json_file):
            return self.comfun.save_to_file(json_file, "")
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
            return self.save_queue()
        return True

    def add_to_queue(self, queue_items, do_save=False):
        last_queue_item_id = None
        for queue_item in queue_items:
            if queue_item.id > 0:
                self.max_id = queue_item.id
            else:
                self.max_id += 1
                queue_item.id = self.max_id
            last_queue_item_id = self.max_id
            self.queue_data.append(queue_item)
            self.total_queue_items += 1

        if do_save is True:
            if self.save_queue():
                return last_queue_item_id
            else:
                return False
        return last_queue_item_id

    def remove_single_queue_item(self, index=None, queue_id=None, do_save=False):
        if index is None and queue_id is None:
            self.batch.logger.err("queue item data not removed, skipping, missing index or id!")
            return False
        removed = False
        if queue_id > 0:
            for i, que in enumerate(self.queue_data):
                if que.id == queue_id:
                    del self.queue_data[i]
                    self.total_queue_items -= 1
                    removed = True
                    break
        if index >= 0:
            del self.queue_data[index]
            self.total_queue_items -= 1
            removed = True
        if removed:
            if do_save is True:
                return self.save_queue()
            else:
                return True
        else:
            self.batch.logger.err("queue item data not removed, item not found!")
            return False

    def remove_queue_items(self, only_done=False):
        if only_done:
            for qi in copy.deepcopy(self.queue_data):
                if qi.state_id == self.batch.sts.INDEX_STATE_DONE:
                    self.remove_single_queue_item(queue_id=qi.id)
        else:
            self.clear_all_queue_items(clear_stored_data=True)

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
                                        "script", 50, "second", "sim_01", 1, "2018_06_20 02:02:03", 1, 1)
        sample_queue_item_3 = QueueItem(0, "queue item 3", 4, "T", 1, "", "", "", 5, 6, "WAITING", 2, 1, "", 0,
                                        "script", 40, "third", "sim_01", 1, "2018_06_20 02:02:04", 1, 1)
        collect_ids += self.add_to_queue((sample_queue_item_1, ))
        collect_ids += self.add_to_queue((sample_queue_item_2, ))
        collect_ids += self.add_to_queue((sample_queue_item_3, ), do_save=do_save)

        self.sample_data_checksum = 6
        self.sample_data_total = 3
        return collect_ids

    def load_queue(self):
        if self.sts.store_data_mode == 1:
            return self.load_queue_from_json()
        if self.sts.store_data_mode == 2:
            return self.load_queue_from_mysql()

    def load_queue_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_QUEUE_FILE_NAME
        if self.comfun.file_exists(json_file, info="queue file"):
            self.batch.logger.inf(("loading queue items: ", json_file))
            json_nodes = self.comfun.load_json_file(json_file)
            if json_nodes is not None and "queueItems" in json_nodes.keys():
                if json_nodes['queueItems']['meta']['total'] > 0:
                    for li in json_nodes['queueItems']['data'].values():
                        if len(li) == len(QUEUE_ITEM_FIELDS_NAMES):
                            new_queue_item = QueueItem(int(li['id']), li['name'], int(li['taskId']), li['user'],
                                                       int(li['userId']), li['sequence'], li['shot'], li['take'],
                                                       int(li['frameFrom']), int(li['frameTo']),
                                                       li['state'], int(li['stateId']), li['ver'],
                                                       li['evo'], int(li['evoNr']), li['evoScript'], int(li['prior']),
                                                       li['desc'], li['simNode'], int(li['simNodeId']),
                                                       li['time'], int(li['projId']), "TMP")  # TODO int(li['softId'])
                            self.add_to_queue((new_queue_item, ))
                        else:
                            self.batch.logger.wrn(("queue json data not consistent:", len(li),
                                                   len(QUEUE_ITEM_FIELDS_NAMES)))
                else:
                    self.batch.logger.wrn(("no queue data in : ", json_file))
                return True
            else:
                self.batch.logger.wrn(("wrong format data in: ", json_file))
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
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_QUEUE_FILE_NAME
        content = self.format_queue_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_queue_to_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    #
    ##
    ###
    """   ADD TO QUEUE   """
    ###
    ##
    #

    """ marker X ATQ X 230   generate script from actions  """
    def generate_script_from_Xactions(self, batch, based_on_schema, evo_scr=None, engine_index=None):
        scr = ""
        engines_counter = 0
        for act in based_on_schema.actions_array:
            if act.evos_possible is True:
                if engines_counter == engine_index:
                    scr += evo_scr
                engines_counter += 1
            scr += act.generate_script_from_action_template(batch, "", with_new_line=False) + "; "
            #                               TODO check    option   ""   !!!

        return scr

    """ marker ATQ 210   generate queue item template   """
    def generate_template_queue_item(self, task, schema):
        """  generate template for multi use on add to queue process   """

        if task is not None:
            current_time = self.comfun.get_current_time(only_time=True)
            """ marker SO (SchemaOptions)   use   """
            """ marker TO (TaskOptions)   use   """
            user = self.batch.usr.get_user_by_id(task.user_id)
            if user is None:
                user = self.batch.usr.get_default_user()
            proxy_queue_item = QueueItem(0, "template queue item", task.id, user.abbrev, 0, task.sequence,
                                         task.shot, task.take, task.sim_frame_start, task.sim_frame_end,
                                         self.batch.sts.states_visible_names[self.batch.sts.INDEX_STATE_WAITING],
                                         self.batch.sts.INDEX_STATE_WAITING, task.queue_ver, "evo", 0, "evo_script",
                                         task.priority, task.description, "", -1, current_time, task.project_id,
                                         schema.soft_name)
            return proxy_queue_item
        else:
            return None

    # TODO remove , cleanup
    # def old generate_template_evo_script(self, action_inputs):
    #     scr = ""
    #     if action_inputs is None:
    #         return ""
    #     for i, act in enumerate(self.batch.sch.current_schema.actions_array):
    #         if len(action_inputs[i]) > 1:
    #             scr += "[evo_scr]  ; "
    #         scr += act.generate_script_from_action_template(self.batch, action_inputs[i][0], evo="[evo]") + "; "
    #     return scr

    """ marker ATQ 211   generate template script   """
    def generate_template_evo_script(self, schema):
        scr = ""
        if schema is None:
            return ""
        for i, act in enumerate(schema.actions_array):
            if act.evos_possible:
                scr += "[evo_scr]  ; "
            scr += act.generate_script_from_action_template(self.batch, act.actual_value, evo="[evo]") + "; "
        return scr

    @staticmethod
    def fill_evos_in_script_template(templ, evo=None, evo_scr=""):
        if evo is None:
            evo = "zzz_evo_www"   # TODO  ATQ prrocess
        templ = templ.replace("[evo]", evo)
        templ = templ.replace("[evo_scr]", evo_scr)
        return templ

    """ marker ATQ 202   generate all evos arr with scripts   """
    def get_evos_from_action_inputs(self, action_inputs):   # depreciated!
        all_evos = []
        found_evos = 0
        if action_inputs is None:
            return all_evos
        for i, ai in enumerate(action_inputs):
            if len(ai) > 1:
                ret = self.batch.pat.get_params_val_arr_from_string(ai[1])
                if ret[0] > 0:
                    found_evos += ret[0]

                    for ie in ret[1]:    # TODO optimize !!!
                        for c, subie in enumerate(ie):
                            if c > 0:
                                all_evos.append([ie[0]+":"+subie, "interactions.set_param(\""+ie[0]+"\","+subie+")"])

        return all_evos

    """ marker ATQ 302   generate all evos arr (scripts for evolving parameters)   """
    def get_array_of_scripts_params_val_from_schema_actions(self, schema):
        all_evos = []
        if schema is None:
            return all_evos

        for i, ai in enumerate(schema.actions_array):
            if ai.evos_possible:
                ret = self.batch.pat.get_params_val_arr_from_string(ai.actual_value)
                if ret[0] > 0:   # ret[0] count evos
                    for ie in ret[1]:  # ['STR', '4.0', '5.0', '6.0']  # TODO optimize, create EVOS class
                        param_arr = []
                        for c, subie in enumerate(ie):
                            if c > 0:
                                descr = ie[0] + ":" + subie
                                scr = "interactions.set_param(\"" + ie[0] + "\"," + subie + ")"
                                param_arr.append([descr, scr])
                        all_evos.append(param_arr)
        return all_evos

    """ marker ATQ 200   generate queue items   """
    def generate_queue_items(self, task_id, evo=None, schema_options=None, task_options=None):
        tsk = self.batch.tsk
        sch = self.batch.sch
        queue_items = []

        if task_options is None:
            based_on_task = copy.deepcopy(tsk.get_task_by_id(task_id))
        else:
            # marker TO (TaskOptions)   use
            based_on_task = task_options.proxy_task
            self.batch.logger.db("generate_queue_items with user's task_options", nl=True)

        if schema_options is None:
            schema_index = sch.get_index_by_id(based_on_task.schema_id)
            based_on_schema = sch.schemas_data[schema_index]
        else:
            # marker SO (SchemaOptions) use
            based_on_schema = schema_options.proxy_schema
            self.batch.logger.db("generate_queue_items with user's schema_options")

        if evo is not None:
            evo_action_index = based_on_schema.get_first_evos_possible()
            if evo_action_index is not None:
                based_on_schema.actions_array[evo_action_index].actual_value = evo

        # marker ATQ 210
        template_queue_item = self.generate_template_queue_item(based_on_task, based_on_schema)

        # marker ATQ 211
        template_script = self.generate_template_evo_script(based_on_schema)

        if template_queue_item is not None:
            # template_queue_item.print_this()
            template_queue_item.evolution_script = template_script

            # marker ATQ 302
            arr_scripts_params = self.get_array_of_scripts_params_val_from_schema_actions(based_on_schema)

            # marker ATQ 303
            all_evo_combinations_array = self.do_params_combinations(arr_scripts_params)

            # action_inputs = None    # TODO  generate from schema or schema options
            # all_evos = self.get_evos_from_action_inputs(action_inputs)   # depreciated!
            # template_queue_item.evolution_script = self.generate_template_evo_script(action_inputs)

            if len(all_evo_combinations_array) == 0:
                template_queue_item.generate_queue_item_name(based_on_task, with_update=True)
                template_queue_item.evolution = ""

                #
                # script = self.generate_script_from_Xactions(self.batch, based_on_schema)
                script = self.fill_evos_in_script_template(template_queue_item.evolution_script, evo=None)
                template_queue_item.evolution_script = script
                #

                queue_items.append(template_queue_item)
            else:
                for i, single_evo in enumerate(all_evo_combinations_array):
                    evo_i_s = self.comfun.str_with_zeros(i + 1, zeros=2)
                    queue_item = copy.deepcopy(template_queue_item)
                    queue_item.generate_queue_item_name(based_on_task, with_update=True, with_sufix=" [e:"+evo_i_s+"]")

                    #  marker ATQ 304
                    single_evo_params = self.get_params_from_evo_combinations(single_evo)
                    queue_item.evolution = single_evo_params[0]
                    queue_item.evolution_nr = i + 1
                    #
                    script = self.fill_evos_in_script_template(template_queue_item.evolution_script, evo="_evo"+evo_i_s,
                                                               evo_scr=single_evo_params[1])
                    queue_item.evolution_script = script

                    #
                    queue_items.append(queue_item)

        else:
            self.batch.logger.err("template_queue_item is None")
        return queue_items

    """ marker ATQ 304   get scripts set_param  from combinations array   """
    def get_params_from_evo_combinations(self, arr):
        scripts_str = ""
        info_str = ""
        for i in arr:
            scripts_str += i[1] + ";"
            info_str += i[0] + ";"
        return info_str, scripts_str

    """ marker ATQ 303   generate queue items   """
    @staticmethod
    def do_params_combinations(arr_in):
        if len(arr_in) == 0:
            return []
        else:
            all_combs = []
            tmp_combs = []
            copy_arr_in = (copy.deepcopy(arr_in))
            if len(copy_arr_in) == 1:
                for j, pj in enumerate(copy_arr_in[0]):
                    all_combs.append([[pj[0], pj[1]]])
                return all_combs
            for i in range(0, len(copy_arr_in)):
                popi = copy_arr_in.pop()
                for j, pj in enumerate(popi):
                    if i == 0:
                        tmp_combs.append([pj[0], pj[1]])
                    else:
                        tmp_arr = []
                        for m in tmp_combs:
                            tmp_arr.append([[pj[0], pj[1]], m])
                        all_combs.extend(tmp_arr)
            return all_combs
