import copy
import os

# JSON Name Format, PEP8 Name Format
SCHEMA_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'schema_name'),
    ('stateId', 'state_id'),
    ('state', 'state'),
    ('version', 'schema_version'),
    ('projId', 'project_id'),
    ('actions', 'actions_array'),
    ('definition', 'definition_id'),
    ('desc', 'description')
    ]

ACTION_DATA_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'action_name'),
    ('type', 'action_type'),
    ('sub_type', 'action_sub_type'),
    ('param', 'action_param'),
    ('soft_id', 'soft_id')
    ]


# class SingleAction:    #  goes to definition
#     def __init__(self, action_id, action_name, action_type, action_sub_type, action_param, soft_id):
#         self.id = action_id
#         self.action_name = action_name
#         self.action_type = action_type
#         self.action_sub_type = action_sub_type
#         self.action_param = action_param
#         self.soft_id = soft_id


class SchemaItem:
    def __init__(self, schema_id, schema_name, state_id, state, project_id, definition_id, schema_version,
                 actions_array, description):

        self.id = schema_id
        self.schema_name = schema_name
        self.state_id = state_id
        self.state = state
        self.project_id = project_id
        self.definition_id = definition_id
        self.schema_version = schema_version
        self.actions_array = actions_array
        # self.actions_string = ""
        self.description = description
        # self.actions_to_string()

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


class Schemas:
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
        self.s = batch.s
        self.batch = batch
        self.comfun = batch.comfun
        self.schemas_data = []

    def get_blank_schema(self):
        return SchemaItem(0, "", 1, "NULL", 1, 1, 1, [], "")

    #  print schema data, for debug
    def print_current(self):
        print "       current schema id:{}   index:{}   total:{}".format(self.current_schema_id,
                                                                         self.current_schema_index,
                                                                         self.total_schemas)
        if self.current_schema_id is not None:
            cur_sch = self.current_schema
            print "       current schema name: ", cur_sch.schema_name
            print "       definition id:{}   project id:{}".format(cur_sch.definition_id, cur_sch.project_id)
            for i, a in enumerate(cur_sch.actions_array):
                print "        a:{}  soft:{}   type:{}  sub type:{} ".format(i, a.soft_id, a.action_type, a.actionParam)

    def print_all(self):
        if self.total_schemas == 0:
            print "   [INF] no schema loaded"
        for c in self.schemas_data:
            print "\n\n   {}   id:{}   state:{}".format(c.schema_name, c.id, c.state)
            print "   sch ver:", c.schema_version
            print "   proj id:{},  definition:{} ".format(c.project_id, c.definition_id)
            for a in c.actions_array:
                print "       action   : ", a.soft_id, a.action_type, a.action_sub_type, a.action_param
        print "\n\n"

    def get_schema_names(self, as_string=False, fit=[]):
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
            # TODO
            self.batch.logger.wrn("update_current_schema parameter missing !")

    def get_current_project_schemas_indexes(self, proj_id):
        counter = 0
        schemas_indexes = []
        for sch in self.schemas_data:
            if sch.project_id == proj_id:
                schemas_indexes.append(counter)
            counter += 1
        return schemas_indexes

    def update_current_from_id(self, schema_id):
        for i, sch in enumerate(self.schemas_data):
            if sch.id == schema_id:
                self.current_schema_index = i
                self.current_schema_id = schema_id
                self.current_schema = sch
                return i
        self.current_schema_id = None
        self.current_schema_index = None
        self.current_schema = None
        return False

    def update_current_from_index(self, index):
        if len(self.schemas_data) > 0 and index > -1:
            self.current_schema_index = index
            self.current_schema_id = self.schemas_data[index].id
            self.current_schema = self.schemas_data[index]
            return self.current_schema_id
        else:
            self.current_schema_id = None
            self.current_schema_index = None
            self.current_schema = None
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
            up_sch.objects_to_sim = edited_schema_item.objects_to_sim
            up_sch.project_name = edited_schema_item.project_name
            up_sch.project_id = edited_schema_item.project_id
            up_sch.soft_id = edited_schema_item.soft_id
            up_sch.actions = edited_schema_item.actions
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

    def remove_single_schema(self, index=None, id=None, do_save=False):
        if index is None and id is None:
            return False
        if id > 0:
            for i, q in enumerate(self.schemas_data):
                if q.id == id:
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
            json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
        if self.comfun.file_exists(json_file):
            return os.remove(json_file)
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
            if self.s.store_data_mode == 1:
                if self.delete_json_schema_file():
                    return True
                else:
                    return False
            if self.s.store_data_mode == 2:
                if self.clear_schemas_in_mysql():
                    return True
                else:
                    return False
        return True

    def create_example_schemas_data(self, do_save=True):
        collect_ids = 0
        sample_schema_item_1 = SchemaItem(0, "schema 1", 22, "ACTIVE", 1, 1, 1, [], "first schema")
        sample_schema_item_2 = SchemaItem(0, "schema 2", 22, "ACTIVE", 1, 2, 3, [], "fire by FumeFx")
        sample_schema_item_3 = SchemaItem(0, "schema 3", 22, "ACTIVE", 2, 2, 5, [], "fire with smoke")
        sample_schema_item_4 = SchemaItem(0, "schema 4", 22, "ACTIVE", 3, 3, 4, [], "cloth with fire")
        collect_ids += self.add_schema(sample_schema_item_1)
        collect_ids += self.add_schema(sample_schema_item_2)
        collect_ids += self.add_schema(sample_schema_item_3)
        collect_ids += self.add_schema(sample_schema_item_4, do_save=do_save)
        self.sample_data_checksum = 10
        self.sample_data_total = 4
        return collect_ids

    def load_schemas(self):
        if self.s.store_data_mode == 1:
            return self.load_schemas_from_json()
        if self.s.store_data_mode == 2:
            return self.load_schemas_from_mysql()

    def load_schemas_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
        if self.comfun.file_exists(json_file, info="schemas file"):
            self.batch.logger.inf(("loading schemas: ", json_file))
            json_schemas = self.comfun.load_json_file(json_file)
            if json_schemas is not None and "schemas" in json_schemas.keys():
                if json_schemas['schemas']['meta']['total'] > 0:
                    for li in json_schemas['schemas']['data'].values():
                        if len(li) == len(SCHEMA_ITEM_FIELDS_NAMES):
                            new_schema_actions = []
                            for lia in li['actions']:
                                self.batch.logger.deepdb(("(lsfj) actions: ", lia))
                                new_schema_actions.append( Action(lia) ) # TODO
                            new_schema_item = SchemaItem(int(li['id']), li['name'], int(li['stateId']), li['state'],
                                                         int(li['projId']), int(li['definition']), int(li['version']),
                                                         new_schema_actions, li['desc'])
                            self.add_schema(new_schema_item)
                        else:
                            self.batch.logger.err(("schema json data not consistent:",len(li),
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
        self.batch.logger.inf("MySQL database available in the PRO version")
        return None

    def save_schemas(self):
        if self.s.store_data_mode == 1:
            return self.save_schemas_to_json()
        if self.s.store_data_mode == 2:
            return self.save_schemas_to_mysql()

    #  prepare 'schemas_data' for backup or save
    def format_schemas_data(self, json=False, sql=False, backup=False):
        if json == sql == backup == False:
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
                        sch[field[0]] = eval('sd.'+field[1])
                    formated_data["schemas"]["data"][i] = sch
                return formated_data
            else:
                # PRO version with SQL
                return False

    #  save projects data as json
    def save_schemas_to_json(self, json_file=None):
        if json_file is None:
            json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
        content = self.format_schemas_data(json=True)
        return self.comfun.save_json_file(json_file, content)

    def save_schemas_to_mysql(self):
        # PRO VERSION
        self.batch.logger.inf("MySQL database available in the PRO version")
        return None

    def get_all_object_from_all_schemas(self, soft_id=0):
        if soft_id <= 0:
            soft_id = self.s.current_soft
        for sch in self.schemas_data:
            if sch.soft_id == soft_id:
                for a in sch.actions_array:
                    if a.action_type == "MaxImport" or a.action_type == "MaxSimulate":
                        #print "       action   : ", a.soft_id, a.action_type, a.action_param
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
