import copy
import os
from .lib.common import CommonFunctions
from .lib.logger import Logger
from .schemas import SchemaItem

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
        return f"QueueItem: {self.id},{self.queue_item_name},{self.task_id},... ,{self.sequence},{self.shot},{self.take},... ,{self.version},{self.evolution},{self.evolution_nr},{self.evolution_script}"

    def print_this(self):
        print(f"{os.linesep} QUEUE ITEM: {self.queue_item_name}")
        print(f"   id: {self.id}   [seq|sh|tk] : [{self.sequence}|{self.shot}|{self.take}] {os.linesep}")
        print(f"   ver:{self.version}  evo_nr: {self.evolution_nr}   evo: {self.evolution}    {os.linesep}")
        print(f"   state:{self.state}  state_id: {self.state_id}    {os.linesep}")
        print(f"   evolution_script:{self.evolution_script}{os.linesep}")

    """ marker ATQ 220   generate name   """
    def generate_queue_item_name(self, task, with_update=False, with_sufix=None):
        name = task.task_name + " ^ "
        if len(task.sequence) > 0:
            name += task.sequence + "_"
        if len(task.shot) > 0:
            name += task.shot + "_"
        if len(task.take) > 0:
            name += task.take

        if name[-1] == "_":
            name = name[:-1]
        name += " ^  v:"+str(task.queue_ver)
        if with_sufix is not None:
            name += with_sufix
        if with_update:
            self.queue_item_name = name
        return name

    def get_evolution_script_with_nl(self):
        es = self.evolution_script
        es_arr = es.split(";")
        return f"{os.linesep}          ".join(es_arr)


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
        print(f"{os.linesep} QUEUE: ")
        print(f"     current queue item id: {self.current_queue_id}   index: {self.current_queue_index}   total queue items: {self.total_queue_items}{os.linesep}")

    def print_current(self):
        print(f" QUEUE INFO:   items total:{self.total_queue_items}, current index:{self.current_queue_index}, current id:{self.current_queue_id}")
        if self.current_queue_index is not None:
            self.current_queue.print_this()

    def print_all(self):
        if self.total_queue_items == 0:
            print("   [INF] no queue items loaded")
        for q in self.queue_data:
            print(f"{os.linesep}{os.linesep} {q.id}  {q.queue_item_name}  {q.prior}  {q.proj_id} state:{q.state}   evo:{q.evolution}   simnode:{q.sim_node}  desc:{q.description}")
        print(f"{os.linesep}{os.linesep}")

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
                    self.queue_data[i].description = f"[{self.comfun.get_current_time(only_time=True)}]  {self.queue_data[i].description}"
                elif set_time is not None:
                    if len(self.queue_data[i].description) > 3:
                        if self.queue_data[i].description[0] == "[":
                            en = self.queue_data[i].description.find("]")
                            if en > 0:
                                self.queue_data[i].description = self.queue_data[i].description[en+1:]
                    time_string = self.comfun.format_seconds_to_string(set_time)
                    self.queue_data[i].description = f"[{time_string}]  {self.queue_data[i].description}"
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

    def remove_queue_items(self, only_done=False, state_id=None):
        if only_done:
            state_id = self.sts.INDEX_STATE_DONE    # TODO clean API  -> conwert done to GREEN
        if state_id is not None:
            for qi in copy.deepcopy(self.queue_data):
                if qi.state_id == state_id:
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
                            soft_id = li['softId'] 
                            if soft_id is None:
                                soft_id = 0
                                
                            new_queue_item = QueueItem(int(li['id']), li['name'], int(li['taskId']), li['user'],
                                                       int(li['userId']), li['sequence'], li['shot'], li['take'],
                                                       int(li['frameFrom']), int(li['frameTo']),
                                                       li['state'], int(li['stateId']), li['ver'],
                                                       li['evo'], int(li['evoNr']), li['evoScript'], int(li['prior']),
                                                       li['desc'], li['simNode'], int(li['simNodeId']),
                                                       li['time'], int(li['projId']), soft_id)
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
    # def generate_script_from_Xactions(self, batch, based_on_schema, evo_scr=None, engine_index=None):
    #     scr = ""
    #     engines_counter = 0
    #     for act in based_on_schema.actions_array:
    #         if act.evos_possible is True:
    #             if engines_counter == engine_index:
    #                 scr += evo_scr
    #             engines_counter += 1
    #         scr += act.generate_script_from_action_template(batch, "", with_new_line=False) + "; "
    #         #                               TODO check    option   ""   !!!
    #
    #     return scr

    """ marker ATQ 210   generate queue item template   """
    def generate_template_queue_item(self, task, schema):
        from .tasks import TaskItem  # Lazy import
        """  generate template for multi use on add to queue process   """

        if task is not None:
            current_time = self.comfun.get_current_time(only_time=True)
            """ marker SO (SchemaOptions)   use   """
            """ marker TO (TaskOptions)   use   """
            user = self.batch.usr.get_user_by_id(task.user_id)
            if user is None:
                user = self.batch.usr.get_default_user()
                
            # Determine softId based on schema definition
            soft_id = 0  # Default to standalone mode
            if schema.based_on_definition == "Houdini":
                soft_id = 1
            elif schema.based_on_definition == "Maya":
                soft_id = 2
            elif schema.based_on_definition == "Blender":
                soft_id = 3
                
            proxy_queue_item = QueueItem(0, "template queue item", task.id, user.abbrev, 0, task.sequence,
                                         task.shot, task.take, task.sim_frame_start, task.sim_frame_end,
                                         self.batch.sts.states_visible_names[self.batch.sts.INDEX_STATE_WAITING],
                                         self.batch.sts.INDEX_STATE_WAITING, task.queue_ver, "evo", 0, "evo_script",
                                         task.priority, task.description, "", -1, current_time, task.project_id,
                                         soft_id)
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
    def generate_template_evo_script(self, schema, task_id=""):
        scr = ""
        if schema is None:
            return ""
        for i, act in enumerate(schema.actions_array):
            if act.evos_possible:
                scr += "[evo_scr];"
            # marker ATQ 235
            scr += act.generate_script_from_action_template(self.batch, act.actual_value, evo="[evo]", task_id=task_id) + "; "
        return scr

    @staticmethod
    def fill_evos_in_script_template(templ, evo=None, evo_scr=""):
        if evo is None:
            # evo = "zzz_evo_www"   # TODO  ATQ prrocess
            evo = ""
        templ = templ.replace("[evo]", evo)
        templ = templ.replace("[evo_scr]", evo_scr)
        return templ

    """ marker ATQ 202   generate all evos arr with scripts   """
    '''
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

                    for ie in ret[1]:    # TODO optimize !!!     (evos_var)  ret[1][0] == ['BND', '7.0', '14.5']
                        for c, subie in enumerate(ie):
                            if c > 0:
                                all_evos.append([ie[0]+":"+subie, "interactions.set_param(\""+ie[0]+"\","+subie+")"])

        return all_evos
    '''

    """ marker ATQ 302   generate all evos arr (scripts for evolving parameters)   """
    def get_array_of_scripts_params_val_from_schema_actions(self, schema):
        all_evos = []
        if schema is None:
            return all_evos

        for i, ai in enumerate(schema.actions_array):
            if ai.evos_possible:
                if "^" in ai.actual_value:
                    '''  evos!!!     option^evo    nClothShape4^STR 40 55  '''
                    splited_actual_value = ai.actual_value.split("^")
                    ret = self.batch.pat.get_params_val_arr_from_string(splited_actual_value[1])
                else:
                    splited_actual_value = "<cloth_objects>"  # TODO !!! other types !
                    ret = self.batch.pat.get_params_val_arr_from_string(ai.actual_value)
                if ret[0] > 0:   # ret[0] count evos
                    for ie in ret[1]:  # ['STR', '4.0', '5.0', '6.0']  # TODO optimize, create EVOS class
                        param_arr = []
                        for c, subie in enumerate(ie):
                            if c > 0:
                                descr = ie[0] + ":" + subie
                                multi_act = self.batch.dfn.current_definition.get_multiaction_by_name(ai.name)
                                mode_index = multi_act.get_action_index_by_mode(ai.mode)
                                act = multi_act.actions[mode_index]
                                execution_name = act.parameters.get_execution_name_by_abbrev(ie[0])

                                '''
                                if ai.parameters is not None:
                                    full_name_param = ai.parameters.get_execution_name_by_abbrev(ie[0])
                                else:
                                    full_name_param = ie[0]
                                    self.batch.logger.wrn(("(et_array_of_scripts...) ai.parameters is not None! ", ie[0]) )
                                '''
                                scr = f'interactions.set_param("{splited_actual_value[0]}","{execution_name}",{subie})'
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

        # set proxy for global use by: act.generate_script_from_action_template

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

        # marker ATQ 211 !!!
        template_script = self.generate_template_evo_script(based_on_schema, task_id=str(task_id))

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

    def get_simed_shot_file_name(self, que_item):
        scr = que_item.evolution_script
        if "_save_scene" in scr:
            spl_scr = scr.split("_save_scene")
            self.batch.logger.deepdb(f"(get_simed_shot_file_name) found_A:{len(spl_scr)}, spl_scr:{spl_scr}")

            if len(spl_scr)>0:
                spl_spl_scr = spl_scr[1][2:]
                self.batch.logger.deepdb(f"(get_simed_shot_file_name) found_B:{len(spl_spl_scr)}, spl_spl_scr:{spl_spl_scr}")
                spl_spl_spl_scr = spl_spl_scr.split(")")[0][:-1]
                if len(spl_spl_spl_scr) > 0:
                    self.batch.logger.deepdb(f"(get_simed_shot_file_name) name:{spl_spl_spl_scr}")
                    return spl_spl_spl_scr
                else:
                    self.batch.logger.deepdb(f"(get_simed_shot_file_name) found_C:{len(spl_scr)}, spl_scr:{spl_scr}")
                    return None
            else:
                self.batch.logger.deepdb(f"(get_simed_shot_file_name) found:{len(spl_scr)}, spl_scr:{spl_scr}")
                return None

        else:
            self.batch.logger.deepdb("(get_simed_shot_file_name) None")
            return None 

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
