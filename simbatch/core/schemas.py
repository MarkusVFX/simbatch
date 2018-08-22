import copy
import os

from actions import SingleAction


# JSON Name Format, PEP8 Name Format
SCHEMA_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'schema_name'),
    ('stateId', 'state_id'),
    ('state', 'state'),
    ('projId', 'project_id'),
    ('definition', 'based_on_definition'),
    ('actions', 'actions_array'),
    ('version', 'schema_version'),
    ('desc', 'description')
    ]


class SchemaOptions:
    """ class used for store and exchange options on "add to queue process" """
    """ marker SO (SchemaOptions)   class   """

    proxy_schema = None

    def __init__(self, schema):
        self.proxy_schema = copy.deepcopy(schema)

    def set_action_value(self, action_name, val, occurrence=None):
        # TODO  try , check attrib exist....
        action_index = self.proxy_schema.get_action_index_by_name(action_name, occurrence=occurrence)
        # action_value = self.proxy_schema.actions_array[action_index].actual_value
        self.proxy_schema.actions_array[action_index].actual_value = val
        # setattr(action_value, param, val)
        return True  # TODO


class SchemaItem:
    """ Single schema """
    id = None
    schema_name = None
    state_id = None
    state = None
    project_id = None
    based_on_definition = None
    actions_array = []
    schema_version = None
    description = None
    soft_name = None

    def __init__(self, schema_id, schema_name, state_id, state, project_id, based_on_definition,
                 actions_array, schema_version, description):  # actions_array

        self.id = schema_id
        self.schema_name = schema_name
        self.state_id = state_id
        self.state = state
        self.project_id = project_id
        self.based_on_definition = based_on_definition     # OLD definition_name
        self.actions_array = actions_array                 # OLD actions_groups_array   TODO add grops for edit action
        self.schema_version = schema_version
        # self.actions_string = ""
        self.description = description
        # self.actions_to_string()
        soft_name = "Maya_TODO"  # TODO

    def __str__(self):
        return "SchemaItem   id:{}  name:{}".format(self.id, self.schema_name)

    def basic_print(self):
        print "\n [INF] basic print: "
        print "       schema name: ", self.schema_name
        print "       project id:{}   actions_array:{}".format(self.project_id, self.actions_array)

    def detailed_print(self):
        print "\n [INF] detailed print: "
        print "       schema id:{}   name:{} ".format(self.id, self.schema_name)
        print "       state id:{}   state:{} ".format(self.state_id, self.state)
        print "       proj id:{}   definition:{}".format(self.project_id, self.based_on_definition)
        print "       schema_version {}   description:{}".format(self.schema_version, self.description)
        print "       actions count:{}".format(len(self.actions_array))
        for i, act in enumerate(self.actions_array):
            print "           {}  {}".format(i, act.name)

    def add_example_actions_to_schema(self):
        self.based_on_definition = "virtual_definition"
        self.add_action_to_schema(SingleAction("virtual action", "virt descr", "<def_val>", "template <f>",
                                               ui=("ui", "interaction.ui_fun()")))
        return True

    def add_action_to_schema(self, single_action_object):
        self.actions_array.append(single_action_object)

    def get_action_index_by_name(self, name, occurrence=None):
        occurr_count = 0
        for i, act in enumerate(self.actions_array):
            if act.name == name:
                if occurrence is None:
                    return i
                else:
                    occurr_count += 1
                    if occurr_count == occurrence:
                        return i
        return None

    # def actions_to_string(self):
    #     for a in self.actions_array:
    #         self.actions_string += a + "|"

    # def actions_string_to_array(self, stri=""):
    #     arr_out = []
    #     if len(stri) == 0:
    #         stri = self.actions_string
    #     arr1 = stri.split('|')
    #     for strWew in arr1:
    #         if len(strWew) > 0:
    #             arr2 = strWew.split(',')
    #             arr_out.append(SingleAction(int(arr2[0]), int(arr2[1]), arr2[2], arr2[3], arr2[4]))
    #     self.actions_array = arr_out

    """ marker ATQ 212   get evo scripts   """
    def get_evo_scripts_array(self, batch, evos_str, engine_index):
        count_actions_with_evos = 0
        for act in self.actions_array:
            parameters = None
            # TODO optimize  -> is evo !!!!
            current_dfn = batch.dfn.get_definition_by_name(self.based_on_definition)
            mac = current_dfn.get_multiaction_by_name(act.name)
            if act.mode is not None:
                if mac is not None:
                    action_index = mac.get_action_index_by_mode(act.mode)
                    if action_index is not None:
                        if mac.actions[action_index].parameters is not None:
                            parameters = mac.actions[action_index].parameters

            if parameters is not None:
                if count_actions_with_evos == engine_index:
                    ret = batch.pat.get_evolutions_from_string(evos_str)
                    tmp2_arr = []
                    tmp2i_arr = []
                    for ev_params in ret[1]:
                        tmp_arr = []
                        tmpi_arr = []
                        for i, ev_param in enumerate(ev_params):
                            if i > 0:
                                for par in parameters.param_list:
                                    if par.abbrev == ev_params[0]:
                                        """ marker ATQ 214   generate evo param script   """
                                        ap = "<o>." + par.execution_name + " = " + str(ev_param)
                                        ap = "interactions.set_evo_param(" + ap + "); "
                                        api = (par.abbrev + " " + str(ev_param)+" ")
                                        tmp_arr.append(ap)
                                        tmpi_arr.append(api)
                        tmp2_arr.append(tmp_arr)
                        tmp2i_arr.append(tmpi_arr)

                    out_arr = []
                    outi_arr = []
                    len_arr = []
                    idx_arr = []
                    sum_len = 1
                    for i, ev in enumerate(tmp2_arr):
                        idx_arr.append(0)
                        len_arr.append(len(ev))
                        sum_len *= len(ev)

                    for sl in range(0, sum_len):
                        combi = ""
                        combii = ""
                        for i, ev in enumerate(tmp2_arr):
                            combi += ev[idx_arr[i]]
                            combii += tmp2i_arr[i][idx_arr[i]]
                        idx_arr[0] += 1

                        for j, dx in enumerate(idx_arr):
                            if dx > len_arr[j]-1:
                                if j+1 < len(idx_arr):
                                    idx_arr[j+1] += 1
                                idx_arr[j] = 0

                        out_arr.append(combi)
                        outi_arr.append(combii)

                    # print "zz",  len(out_arr), sum_len , out_arr
                    # print "zzi",  len(outi_arr), sum_len , outi_arr
                    return outi_arr, out_arr

                count_actions_with_evos += 1

        return [], []


class Schemas:
    """ All schemas from all projects, TODO project schemas for PRO """
    schemas_data = []
    max_id = 0
    total_schemas = 0
    current_schema = None   # TODO  update !!!
    current_schema_id = None
    current_schema_index = None
    current_schema_software_id = None   # used for SoftwareConnector

    sample_data_checksum = None
    sample_data_total = None

    def __init__(self, batch):
        self.sts = batch.sts
        self.batch = batch
        self.comfun = batch.comfun
        self.schemas_data = []

    @staticmethod
    def get_blank_schema():
        return SchemaItem(0, "", 1, "NULL", 1, "blank defn", [], 1, "")

    #  print schema data, for debug
    def print_schema(self, schema=None):
        prefix = ""
        if schema is None:
            prefix = "current "
            if self.current_schema_id is not None:
                print "\n     current schema id:{}   index:{}   total:{}".format(self.current_schema_id,
                                                                                 self.current_schema_index,
                                                                                 self.total_schemas)
                schema = self.current_schema
            else:
                self.batch.logger.wrn("current schema undefined, nothing to print")
                return False

        print "\n       {}schema name:{}".format(prefix, schema.schema_name)
        print "       definition id:{}   project id:{}".format(schema.based_on_definition, schema.project_id)
        for a in schema.actions_array:
            print "       __a: name:{}  def_val:{}  actual_val:{}  descr:{}  mode:{}".format(a.name,
                                                                                             a.default_value,
                                                                                             a.actual_value,
                                                                                             a.description,
                                                                                             a.mode)

    def print_current(self):
        self.print_schema()

    def print_all(self):
        if self.total_schemas == 0:
            print "   [INF] no schema loaded"
        for sch in self.schemas_data:
            print "\n\n   {}   id:{}   state:{}".format(sch.schema_name, sch.id, sch.state)
            print "   sch ver:", sch.schema_version
            print "   proj id:{},  definition:{} ".format(sch.project_id, sch.based_on_definition)
            print "   actions count: ", len(sch.actions_array)
            for a in sch.actions_array:
                print "   __action: {}__{}__{}__{}".format(a.name, a.default_value, a.actual_value, a.template)
        print "\n\n"

    def get_schema_names(self, as_string=False, fit=()):
        schema_names = []
        if len(fit) > 0:
            for sch in self.schemas_data:
                if self.comfun.find_string_in_list(fit, sch.schema_name.lower(), exactly=False) >= 0:
                    schema_names.append(sch.schema_name)
        else:
            for sch in self.schemas_data:
                schema_names.append(sch.schema_name)
        schema_names = sorted(set(schema_names))
        if as_string is True:
            names_string = ""
            for schema_name in schema_names:
                names_string += schema_name + ";"   # TODO optimize
            return names_string
        else:
            return schema_names

    def get_schema_by_id(self, get_id):
        for sch in self.schemas_data:
            if sch.id == get_id:
                return sch
        self.batch.logger.wrn(("no schema with ID: ", get_id))
        return None

    def get_index_by_name(self, schema_name):
        counter = 0
        for sch in self.schemas_data:
            if sch.schema_name == schema_name:
                return counter
            counter += 1
        self.batch.logger.wrn(("no schema with name: ", schema_name))
        return None

    def get_index_by_id(self, get_id):
        counter = 0
        for sch in self.schemas_data:
            if sch.id == get_id:
                return counter
            counter += 1
        self.batch.logger.wrn(("no schema with ID: ", get_id))
        return None

    def update_current_schema(self, schema_id=-1, index=-1, last=-1):
        if last == 1:
            last_sch = self.schemas_data[self.total_schemas - 1]
            self.current_schema_index = self.total_schemas - 1
            self.current_schema_id = last_sch.id
            return 1
        else:
            # TODO schema_id  index !!!
            self.batch.logger.wrn("update_current_schema parameter missing !")

    def get_current_project_schemas_indexes(self, proj_id):
        counter = 0
        schemas_indexes = []
        for sch in self.schemas_data:
            if sch.project_id == proj_id:
                schemas_indexes.append(counter)
            counter += 1
        return schemas_indexes

    def clear_current_schema(self):
        self.current_schema_id = None
        self.current_schema_index = None
        self.current_schema = None

    def update_current_definition_on_schema_change(self):
        if self.current_schema.based_on_definition != self.batch.dfn.current_definition_name:
            # update DEFINITION
            if self.current_schema.based_on_definition is not None:
                self.batch.dfn.update_current_definition_by_name(self.current_schema.based_on_definition)

    def update_current_from_id(self, schema_id):
        for i, sch in enumerate(self.schemas_data):
            if sch.id == schema_id:
                self.current_schema_index = i
                self.current_schema_id = schema_id
                self.current_schema = sch
                self.update_current_definition_on_schema_change()
                return i
        self.clear_current_schema()
        return False

    def update_current_from_index(self, index):
        if len(self.schemas_data) > 0 and index > -1:
            self.current_schema_index = index
            self.current_schema_id = self.schemas_data[index].id
            self.current_schema = self.schemas_data[index]
            self.update_current_definition_on_schema_change()
            return self.current_schema_id
        else:
            self.clear_current_schema()
            return False

    def add_schema(self, schema_item, do_save=False):
        if schema_item.id > 0:
            self.max_id = schema_item.id
        else:
            self.max_id += 1
            schema_item.id = self.max_id
        self.schemas_data.append(schema_item)
        self.total_schemas += 1

        if do_save is True:
            if self.save_schemas():
                return schema_item.id
            else:
                return False
        else:
            return schema_item.id

    def update_schema(self, edited_schema_item, do_save=False):
        if self.current_schema_index >= 0:
            up_sch = self.schemas_data[self.current_schema_index]
            up_sch.schema_name = edited_schema_item.schema_name
            up_sch.description = edited_schema_item.description
            up_sch.schema_version = edited_schema_item.schema_version
            # up_sch.objects_to_sim = edited_schema_item.objects_to_sim
            # up_sch.project_name = edited_schema_item.project_name
            up_sch.project_id = edited_schema_item.project_id
            # up_sch.soft_id = edited_schema_item.soft_id
            up_sch.actions_array = copy.deepcopy(edited_schema_item.actions_array)
            if do_save is True:
                self.save_schemas()
        else:
            self.batch.logger.err("(update_schema) self.current_schema_index < 0  (none selected ???)")

    def increase_current_schema_version(self):
        if self.current_schema is not None:
            cur_sch = self.current_schema
            self.batch.logger.db(("curent_schema_ver++", cur_sch.schema_version, str(int(cur_sch.schema_version) + 1)))
            self.schemas_data[self.current_schema_index].schema_version = str(int(cur_sch.schema_version) + 1)
            self.save_schemas()
        else:
            self.batch.logger.err("(increase_current_schema_version) current schema undefined")

    def remove_single_schema(self, index=None, sch_id=None, do_save=False):
        if index is None and sch_id is None:
            return False
        if sch_id > 0:
            for i, q in enumerate(self.schemas_data):
                if q.id == sch_id:
                    del self.schemas_data[i]
                    self.total_schemas -= 1
                    break
            if do_save is False:
                return True
        if index >= 0:
            del self.schemas_data[index]
            self.total_schemas -= 1
            if do_save is False:
                return True
        if do_save is True:
            return self.save_schemas()

    def delete_json_schema_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_SCHEMAS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)
        else:
            return True

    def clear_json_schema_file(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_SCHEMAS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return self.comfun.save_to_file(json_file, "")
        else:
            return True

    @staticmethod
    def clear_schemas_in_mysql():
        # PRO VERSION with sql
        return False

    def clear_all_schemas_data(self, clear_stored_data=False):
        del self.schemas_data[:]
        self.max_id = 0
        self.total_schemas = 0
        self.current_schema_id = None
        self.current_schema_index = None
        # TODO check clear UI val (last current...)
        if clear_stored_data:
            if self.sts.store_data_mode == 1:
                if self.clear_json_schema_file():
                    return True
                else:
                    return False
            if self.sts.store_data_mode == 2:
                if self.clear_schemas_in_mysql():
                    return True
                else:
                    return False
        return True

    def add_examples_actions_to_all_schemas(self):
        for sch in self.schemas_data:
            sch.add_example_actions_to_schema()

    def create_example_schemas_data(self, do_save=True):
        collect_ids = 0
        sample_schema_item_1 = SchemaItem(0, "schema 1", 22, "ACTIVE", 1, "sample_definition_1", [], 1, "first schema")
        sample_schema_item_2 = SchemaItem(0, "schema 2", 22, "ACTIVE", 1, "sample_definition", [], 3, "fire by FumeFx")
        sample_schema_item_3 = SchemaItem(0, "schema 3", 22, "ACTIVE", 2, "sample_definition", [], 5, "fire with smoke")
        sample_schema_item_4 = SchemaItem(0, "schema 4", 22, "ACTIVE", 3, "sample_definition", [], 4, "cloth with fire")
        collect_ids += self.add_schema(sample_schema_item_1)
        collect_ids += self.add_schema(sample_schema_item_2)
        collect_ids += self.add_schema(sample_schema_item_3)
        collect_ids += self.add_schema(sample_schema_item_4)
        self.sample_data_checksum = 10
        self.sample_data_total = 4
        self.add_examples_actions_to_all_schemas()
        if do_save:
            self.save_schemas()
        return collect_ids

    def load_schemas(self):
        if self.sts.store_data_mode == 1:
            return self.load_schemas_from_json()
        if self.sts.store_data_mode == 2:
            return self.load_schemas_from_mysql()

    def load_schemas_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_SCHEMAS_FILE_NAME
        if self.comfun.file_exists(json_file, info="schemas file"):
            self.batch.logger.inf(("loading schemas: ", json_file))
            json_schemas = self.comfun.load_json_file(json_file)
            if json_schemas is not None and "schemas" in json_schemas.keys():
                if json_schemas['schemas']['meta']['total'] > 0:
                    for li in json_schemas['schemas']['data'].values():
                        if len(li) == len(SCHEMA_ITEM_FIELDS_NAMES):
                            new_schema_actions = []
                            if "actions" in li:
                                for lia in li['actions'].values():
                                    self.batch.logger.deepdb(("(lsfj) actions: ", lia))
                                    av = lia["actual"]
                                    new_action = SingleAction(lia["name"], lia["desc"], lia["default"], lia["template"],
                                                              actual_value=av, mode=lia["mode"],
                                                              evos_possible=lia["evos"])
                                    new_schema_actions.append(new_action)
                            new_schema_item = SchemaItem(int(li['id']), li['name'], int(li['stateId']), li['state'],
                                                         int(li['projId']), li['definition'], new_schema_actions,
                                                         int(li['version']), li['desc'])
                            self.add_schema(new_schema_item)
                        else:
                            self.batch.logger.err(("schema json data not consistent:", len(li),
                                                   len(SCHEMA_ITEM_FIELDS_NAMES)))
                    return True
            else:
                self.batch.logger.wrn(("no projects data in : ", json_file))
                return False
        else:
            self.batch.logger.err(("no schema file: ", json_file))
            return False

    def load_schemas_from_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    def save_schemas(self):
        if self.sts.store_data_mode == 1:
            return self.save_schemas_to_json()
        if self.sts.store_data_mode == 2:
            return self.save_schemas_to_mysql()

    #  prepare 'schemas_data' for backup or save
    def format_schemas_data(self, json=False, sql=False, backup=False):
        if json == sql == backup is False:
            self.batch.logger.err("(format_projects_data) no format param !")
        else:
            if json or backup:
                tim = self.comfun.get_current_time()
                formated_data = {"schemas": {"meta": {"total": self.total_schemas,
                                                      "timestamp": tim,
                                                      "jsonFormat": "http://json-schema.org/"},
                                             "data": {}}}
                for i, sd in enumerate(self.schemas_data):
                    sch = {}
                    for field in SCHEMA_ITEM_FIELDS_NAMES:
                        if field[0] == "actions":
                            schema_actions = {}
                            for j, a in enumerate(sd.actions_array):
                                new_action = {}
                                for field_a in a.json_FIELDS_NAMES:
                                    new_action[field_a[0]] = eval('a.' + field_a[1])
                                schema_actions[j] = new_action
                            sch["actions"] = dict(schema_actions)
                        else:
                            sch[field[0]] = eval('sd.'+field[1])
                    formated_data["schemas"]["data"][i] = sch
                return formated_data
            else:
                # PRO version with SQL
                return False

    #  save projects data as json
    def save_schemas_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.sts.store_data_json_directory_abs + self.sts.JSON_SCHEMAS_FILE_NAME
        content = self.format_schemas_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_schemas_to_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL will be supported with the PRO version")
        return None

    def get_all_object_from_all_schemas(self, soft_id=0):
        if soft_id <= 0:
            soft_id = self.sts.current_soft
        for sch in self.schemas_data:
            if sch.soft_id == soft_id:
                for a in sch.actions_array:
                    if a.user_value == a.default_value:
                        # print "       action   : ", a.soft_id, a.action_type, a.action_param
                        pass
                        # TODO  get_all_object_from_all_schemas

    def copy_schema(self, source_schema_index, proj_target_id):
        if 0 <= source_schema_index < len(self.schemas_data):
            new_sch = copy.deepcopy(self.schemas_data[source_schema_index])
            new_sch.id = 0
            new_sch.project_id = proj_target_id
            if proj_target_id >= 0:
                self.add_schema(new_sch, do_save=False)
            else:
                self.batch.logger.err(("wrong proj ID: ", proj_target_id))
        else:
            self.batch.logger.err(("wrong sch nr: ", source_schema_index))

    """ marker SO (SchemaOptions)   create object   """
    def create_schema_options_object(self, schema=None):
        if schema is None:
            schema = self.current_schema
        return SchemaOptions(schema)
