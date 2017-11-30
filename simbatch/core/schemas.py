import copy

#  from common import CommonFunctions


class SingleAction:
    def __init__(self, action_id, soft_id, action_type, action_sub_type, action_param):
        self.id = action_id
        self.soft_id = soft_id
        self.action_type = action_type
        self.action_sub_type = action_sub_type
        self.action_param = action_param


class SchemaItem:
    total_items = 0
    max_id = 0

    def __init__(self, schema_id, schema_name, description, schema_version, objects_to_sim, project_name, project_id,
                 soft_id, actions):
        if schema_id > 0:
            self.max_id = schema_id
        else:
            self.max_id += 1
            self.total_items += 1

        self.id = self.max_id
        self.schema_name = schema_name
        self.description = description
        self.schema_version = schema_version
        self.objects_to_sim = objects_to_sim
        self.project_name = project_name
        self.project_id = project_id
        self.soft_id = soft_id
        self.actions = actions
        self.actions_array = []
        self.actions_string_to_array()

    def actions_string_to_array(self, stri=""):
        arr_out = []
        if len(stri) == 0:
            stri = self.actions
        arr1 = stri.split('|')
        for strWew in arr1:
            if len(strWew) > 0:
                arr2 = strWew.split(',')
                arr_out.append(SingleAction(int(arr2[0]), int(arr2[1]), arr2[2], arr2[3], arr2[4]))
        self.actions_array = arr_out


class Schemas:
    schemas_data = []
    max_id = 0
    total_schemas = 0
    current_schema = None   # TODO  update !!!
    current_schema_id = None
    current_schema_index = None

    def __init__(self, batch):
        self.s = batch.s
        self.comfun = batch.comfun

    #  print schema data, for debug
    def print_schemas(self):
        for c in self.schemas_data:
            print "\n   {} id:{} state:{}".format(c.schema_name, c.id, c.state)
            print "   ", c.schema_version
            print "   sch proj:{},    proj id:{},   soft id:{} ".format(c.project_name, c.project_id, c.soft_id)
            print "   ."
            for a in c.actions_array:
                print "       action   : ", a.soft_id, a.action_type, a.action_sub_type, a.action_param
        print "schemaas count: ", self.total_schemas, "\n"

        if self.total_schemas == 0:
            print "   [INF] no schema loaded"
        else:
            print "\n   [INF] total schemas count:", self.total_schemas
            if self.current_schema_index is not None:
                print "       current index: ", self.current_schema_index
                print "       current id: ", self.current_schema_id
                print "       current schema: ", self.current_schema.schema_name
            print "   ."



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
        print "   [WRN] no schema with ID: ", get_id
        return None

    def get_schema_index_by_name(self, schema_name):
        counter = 0
        for sch in self.schemas_data:
            if sch.schema_name == schema_name:
                return counter
            counter += 1
        print "   [WRN] no schema with name: ", schema_name
        return -1

    def get_schema_index_by_id(self, get_id):
        counter = 0
        for sch in self.schemas_data:
            if sch.id == get_id:
                return counter
            counter += 1
        print "   [WRN] no schema with ID: ", get_id
        return -1

    def update_current_schema(self, schema_id=-1, index=-1, last=-1):
        if last == 1:
            last_sch = self.schemas_data[self.total_schemas - 1]
            self.current_schema_index = self.total_schemas - 1
            self.current_schema_id = last_sch.id
            return 1
        else:
            1
            # TODO
        print " [WRN] update_current_schema parameter missing !\n"

    def get_current_project_schemas_indexes(self, proj_id):
        counter = 0
        schemas_indexes = []
        for sch in self.schemas_data:
            if sch.project_id == proj_id:
                schemas_indexes.append(counter)
            counter += 1
        return schemas_indexes

    def create_example_project_data(self, proj_id):
        sample_schema_item_1 = SchemaItem(0, "schema 1", "first schema", "base.max", "s1", "sch1", proj_id, 1, "")
        sample_schema_item_2 = SchemaItem(0, "schema 2", "fire by FumeFx", "base.max", "s2", "sch2", proj_id, 1, "")
        sample_schema_item_3 = SchemaItem(0, "schema 3", "fire with smoke", "base.max", "s3", "sch3", proj_id, 2, "")
        sample_schema_item_4 = SchemaItem(0, "schema 4", "cloth with fire", "base.max", "s4", "sch4", proj_id, 3, "")
        self.add_schema(sample_schema_item_1)
        self.add_schema(sample_schema_item_2)
        self.add_schema(sample_schema_item_3)
        self.add_schema(sample_schema_item_4, do_save=True)
        return self.max_id

    def update_current_from_id(self, schema_id):
        counter = 0
        for sch in self.schemas_data:
            if sch.id == schema_id:
                self.current_schema_index = counter
            counter += 1

    def update_current_from_index(self, index):
        if len(self.schemas_data) > 0 and index > -1:
            self.current_schema_id = self.schemas_data[index].id
        else:
            self.current_schema_id = -1

    def add_schema(self, schema_item, do_save=False):
        if schema_item.id > 0:
            self.max_id = schema_item.id
        else:
            self.max_id += 1
            schema_item.id = self.max_id
        self.schemas_data.append(schema_item)
        self.total_schemas += 1
        if do_save is True:
            self.save_schemas()

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
            print " [ERR] self.current_schema_index < 0  (none selected ???) "

    def increase_curent_schema_version(self):
        cur_sch = self.schemas_data[self.current_schema_index]
        print "  increase_curent_schema_version  ", cur_sch.schema_version, str(int(cur_sch.schema_version) + 1)
        self.schemas_data[self.current_schema_index].schema_version = str(int(cur_sch.schema_version) + 1)
        self.save_schemas()

    def remove_single_schema(self, index=-1, id=-1, do_save=False):
        if id > 0:
            index_by_id = 0
            for q in self.schemas_data:
                if q.id == id:
                    del self.schemas_data[index_by_id]
                    #  TODO    algorithm max_id
                    self.total_schemas -= 1
                    print "  [INF]  remove_single_schema id ", id
                    break
                index_by_id += 1
        if index >= 0:
            del self.schemas_data[index]
            #  TODO    algorithm max_id
            self.total_schemas -= 1
            print "  [INF]  remove_single_schema index ", index
        if do_save is True:
            self.save_schemas()

    def clear_all_schemas(self):
        del self.schemas_data[:]
        self.max_id = 0
        self.total_schemas = 0
        self.current_schema_id = -1
        self.current_schema_index = -1
        # TODO check clear UI val (last current...)

    def load_schemas(self):
        if self.s.store_data_mode == 1:
            self.load_schemas_from_json()
        if self.s.store_data_mode == 2:
            self.load_schemas_from_mysql()

    def load_schemas_from_json(self, json_file=""):
        if len(json_file) == 0:
            json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
        print " [INF] loading schema: " + json_file
        if self.comfun.file_exists(json_file, "schema file"):
            f = open(json_file, 'r')
            for line in f.readlines():
                if len(line) > 4:
                    li = line.split(";")
                    new_schema_item = SchemaItem(int(li[0]), li[1], li[2], li[3], li[4],
                                                 li[5], int(li[6]), int(li[7]), li[8])
                    self.add_schema(new_schema_item)
            f.close()

    @staticmethod
    def load_schemas_from_mysql():
        #  PRO VERSION
        1

    def save_schemas(self):
        if self.s.store_data_mode == 1:
            self.save_schemas_to_json()
        if self.s.store_data_mode == 2:
            self.save_schemas_to_mysql()

    def save_schemas_to_json(self, content=None, json_file=None):
        if json_file is None:
            json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
        if path.exists(json_file):
            print " [INF] saving schemas: " + json_file
            if content is None:
                content = ""
                for c in self.schemas_data:
                    content_line = str(c.id) + ';' + c.schema_name + ';' + c.description + ';' + str(
                        c.schema_version) + ';' + c.objects_to_sim + ';' + c.project_name + ';' + str(
                        c.project_id) + ';' + str(c.soft_id) + ';' + c.actions + ';\n'
                    content += content_line
            self.comfun.save_to_file(json_file, content)
        else:
            print " [ERR] schema file not exist !\n"

    @staticmethod
    def save_schemas_to_mysql():
        #  PRO VERSION
        1

    def get_all_object_from_all_schemas(self, soft_id=0):
        if soft_id <= 0:
            soft_id = self.s.current_soft
        print "     [db] (get_all_object_from_all_schemas) soft_id ", soft_id
        for sch in self.schemas_data:
            if sch.soft_id == soft_id:
                for a in sch.actions_array:
                    if a.action_type == "MaxImport" or a.action_type == "MaxSimulate":
                        print "       action   : ", a.soft_id, a.action_type, a.action_param

    def copy_schema(self, source_schema_index, proj_target_id):
        if 0 <= source_schema_index < len(self.schemas_data):
            new_sch = copy.deepcopy(self.schemas_data[source_schema_index])
            new_sch.id = -1
            new_sch.project_id = proj_target_id
            if proj_target_id >= 0:
                self.add_schema(new_sch, do_save=False)
            else:
                print " [ERR] proj ID wrong : ", proj_target_id
        else:
            print " [ERR] sch nr wrong : ", source_schema_index
