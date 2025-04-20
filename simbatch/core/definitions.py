try:
    import MaxPlus
except ImportError:
    pass

try:
    import hou
except ImportError:
    pass

import os
from .actions import MultiAction, SingleAction, ActionParameters



# JSON Name Format, PEP8 Name Format
DEFINITION_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'definition_name'),
    ('version', 'definition_version'),
    ('actions', 'actions_groups_array'),
    ('desc', 'description')]


ACTION_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'action_name'),
    ('template', 'template'),
    ('subActions', 'sub_actions'),
    ('desc', 'description')]


class ExampleInteractions:
    def __init__(self):
        self.load()

    @staticmethod
    def load():
        print("[interact example] loaded")

    @staticmethod
    def test():
        print("[interact example] test")

    @staticmethod
    def interact_get_scene_objects():
        print("[interact example]     def interact_get_scene_objects")


class SingleDefinition:
    name = ""       # actions in schema are copied from definition for protect schema data if no definition
    version = 0     # version are useful for recognize exact source of definition
    software = ""   # TODO software name or software version ???
    #               # TODO list supported versions
    prev_ext = ""   # "prevExt" without dot "png"
    setup_ext = ""  # "setupExt" without dot

    multi_actions_array = []    # array of MultiAction objects
    total_actions = 0
    action_names = []

    interactions = None  # object of class Interaction created by: def class_from_file(self, filename)

    def __init__(self, name, logger):
        self.name = name
        self.multi_actions_array = []
        self.action_names = []
        self.logger = logger

    def __repr__(self):
        return f"SingleDefinition({self.software})"

    def __str__(self):
        return f"SingleDefinition  name:{self.name}"

    def print_total(self, prefix=""):
        print(f"   [INF] {prefix} total actions:{self.total_actions}")

    def print_all(self):
        for action_group in self.multi_actions_array:
            for ai in action_group.actions:
                ai.print_minimum()
        self.print_total()

    def print_single(self):
        self.logger.clear_buffer()
        self.logger.buffering_on()
        logger_raw = self.logger.raw
        logger_raw(f"{os.linesep}{os.linesep} name: {self.name} total_actions: {self.total_actions} names count: {len(self.action_names)}")
        for i, an in enumerate(self.action_names):
            logger_raw(f"  arr action_names: {i}  {an} ")
        for i, ga in enumerate(self.multi_actions_array):
            if ga.actions_count == len(ga.actions):
                logger_raw(f"   group_name: {i} {ga.name}  count: {ga.actions_count}")
            else:
                logger_raw(f"   group_name: {i} {ga.name}  ERR count : {ga.actions_count} != {len(ga.actions)} ")
            for j, sa in enumerate(ga.actions):
                logger_raw(f"       action {j}  name: {sa.name}  default_value: {sa.ui[0]}  ui: {sa.ui}")
        self.logger.buffering_off()
        return self.logger.get_buffer()

    def add_group_action(self, element):
        self.multi_actions_array.append(element)
        self.total_actions += 1
        self.action_names.append(element.name)

    def get_multiaction_by_name(self, name):
        for mac in self.multi_actions_array:
            if mac.name == name:
                return mac
        return None

    def get_base_setup_ext(self):
        return self.setup_ext

    def get_prev_ext(self):
        return self.prev_ext

    def project_item_double_click(self, param):
        self.logger.wrn("definition not loaded, default project_item_double_click()")

    def schema_item_double_click(self, param):
        self.logger.wrn("definition not loaded, default schema_item_double_click()")

    def task_item_double_click(self, param):
        self.logger.wrn("definition not loaded, default task_item_double_click()")

    def queue_item_double_click(self, param):
        self.logger.wrn("definition not loaded, default queue_item_double_click()")

    def node_item_double_click(self, param):
        self.logger.wrn("definition not loaded, default queue_item_double_click()")

    def open_setup(self, param):
        self.logger.wrn("definition not loaded, default open_setup()")

    def save_setup(self, param):
        self.logger.wrn("definition not loaded, default save_setup()")


class Definitions:
    batch = None
    comfun = None

    definitions_array = []
    definitions_names = []

    total_definitions = 0
    current_definition = None          # current definition       (definition object)
    current_definition_name = None     # current definition name  (unique name)
    current_definition_index = None    # current definition index (array index)

    # current_software_id = 0

    current_interactions = None        # depreciate: soco = None   # software connector

    def __init__(self, batch):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.definitions_array = []
        self.definitions_names = []
        # self.soco = SoftwareConnector(batch.sch.current_schema_software_id)

        # self.current_interactions = ExampleInteractions()

    def __repr__(self):
        return f"Definitions({self.batch})"

    def __str__(self):
        return f"Definitions,  current_definition:{self.current_definition}"

    '''  print project data, for debug  '''
    def print_current(self):
        print(f"     current definition:     index: {self.current_definition_index}    total_definitions: {self.total_definitions}{os.linesep}")
        if self.current_definition_index is not None:
            cur_def = self.current_definition
            print(f"       current definition: {cur_def.name}")
            print(f"       software: {cur_def.software}")
            print(f"       actions count: {len(cur_def.multi_actions_array)}")
            for group in cur_def.multi_actions_array:
                for action in group.actions:
                    if hasattr(action, 'ui') and len(action.ui) > 0:
                        ui_value = action.ui[0]
                    else:
                        ui_value = "N/A"
                    print(f"       __action: {action.name}__{ui_value}")

    '''  print definitions data, for debug  '''
    def print_total(self, print_children=False):
        if print_children:
            for i, d in enumerate(self.definitions_array):
                d.print_total(prefix=f"Definition {i}")
        print(f"   [INF] Definitions total_definitions: {self.total_definitions}")

    def print_all(self, print_children=False):
        if self.total_definitions == 0:
            print("   [INF] no definitions loaded")
        for d in self.definitions_array:
            print(f"{os.linesep}{os.linesep}   {d.name}   id:{d.id}   software:{d.software}")
            print(f"   description: {d.description}")
            print(f"   actions count: {len(d.actions_array)}")
            for a in d.actions_array:
                print(f"   __action: {a.name}__{a.ui[0]}__{a.actual_value}__{a.template}")
            print(f"{os.linesep}{os.linesep}")

    def get_definitions(self):
        return self.definitions_array

    def get_definition_by_name(self, name):
        for i, d in enumerate(self.definitions_array):
            if d.name == name:
                return d
        return None

    @staticmethod
    def is_single_action(obj):
        return isinstance(obj, SingleAction)

    @staticmethod
    def create_single_action(name, description, template, actual_value=None, mode=None, ui=None):
        return SingleAction(name, description, template, actual_value=actual_value, mode=mode, ui=ui)

    @staticmethod
    def create_multiaction(mac_id, name):
        return MultiAction(mac_id, name)

    def create_example_definition(self, do_save=False):
        content = {"definition": {"meta": {"name": "Dfn Example 1", "software": "Example", "totalActions": 3},
                                  "actions": {"1": {"id": 1, "type": "single", "name": "Print1",
                                                    "desc": "p1", "ui": [], "default": "print 1",
                                                    "template": ["print 111"]},
                                              "2": {"id": 1, "type": "single", "name": "Print2",
                                                    "desc": "p2", "ui": [], "default": "print 2",
                                                    "template": ["print 222"]},
                                              "3": {"id": 1, "type": "single", "name": "Print3",
                                                    "desc": "p3", "ui": [], "default": "print 3",
                                                    "template": ["print 333"]}
                                              }
                                  }}
        if do_save:
            return self.save_definition("example", content)
        else:
            return content

    def get_current_setup_ext(self):    # TODO  env = self.sts.runtime_env
        if self.current_definition is not None:
            return self.current_definition.setup_ext
        else:
            self.batch.logger.err("get_current_setup_ext unknown, current_definition is None")
            return "DEF"

    def get_current_prev_ext(self):    # TODO  env = self.sts.runtime_env
        if self.current_definition is not None:
            return self.current_definition.prev_ext
        else:
            self.batch.logger.err("get_current_prev_ext unknown, current_definition is None")
            return "DEF"

    def add_definition(self, defi):
        self.definitions_array.append(defi)
        self.total_definitions += 1

    def load_definitions(self):
        if self.sts.store_data_mode == 1:
            ret = self.load_definitions_from_jsons()
            if ret == 0:   # return number of errors
                return True
            else:
                return ret
        elif self.sts.store_data_mode == 2:
            ret = self.load_definitions_from_mysql()
        else:
            ret = False

        if self.current_definition_name is None:
            if self.total_definitions > 0:
                self.current_definition_name = self.definitions_names[0]
                self.current_definition_index = 0
            else:
                self.batch.logger.wrn("No definition loaded!")
        return ret

    def save_definition(self, defi_name, defi_content):
        if self.sts.store_data_mode == 1:
            ret = self.save_definition_to_json(defi_name, defi_content)
            if ret == 0:   # return number of errors
                return True
            else:
                return ret
        elif self.sts.store_data_mode == 2:
            ret = self.save_definitions_to_mysql()
        else:
            ret = False
        return ret

    def save_definition_to_json(self, json_file, content):
        if json_file is None or len(json_file) == 0:
            return False
        if self.comfun.is_absolute(json_file) is False:
            json_file = self.sts.store_definitions_directory_abs + "interaction_" + json_file + ".json"
        return self.comfun.save_json_file(json_file, content)

    @staticmethod
    def save_definitions_to_mysql():
        # PRO version
        return False

    @staticmethod
    def get_ui_values(li):
        if "ui" in li:
            return li["ui"]
        else:
            return None

    def get_example_definition(self):
        example_defi = SingleDefinition("example_defi", self.batch.logger)
        example_group_actions = MultiAction(1, "example a gr")
        example_action = SingleAction("ex_a", "desc", "templ <o>", mode="single",
                                      ui=(("Tst", "print('ex')"), ("Tst", "print('ex')")))
        example_group_actions.add_single_action(example_action)
        example_defi.add_group_action(example_group_actions)
        return example_defi

    # TODO move to common !!!!
    def class_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            exec(content)
            return eval("Interactions")
        except SyntaxError as e:
            self.batch.logger.err(f"syntax error definition file: {filename}", nl=True, nl_after=True)
            return None
        except Exception as e:
            self.batch.logger.err(f"Error loading definition file: {str(e)}")
            return None
    # TODO move to common !!!!

    def load_interaction_file(self, file_path):
        self.batch.logger.deepdb(("__load_interaction_file: ", file_path))
        if self.sts.current_os == 2:    # win
            file_path = file_path.replace("/", "\\")
        if self.comfun.file_exists(file_path):
            InteractionClass = self.class_from_file(file_path)
            if InteractionClass is None:
                return None
            else:
                loaded_interaction = InteractionClass(self.sts.current_os, self.batch.logger, self.comfun)
            return loaded_interaction
        else:
            return None

    def load_definitions_from_jsons(self, definitions_dir=""):
        if len(definitions_dir) == 0:
            definitions_dir = self.sts.store_definitions_directory_abs
        loading_errors = 0
        if self.comfun.file_exists(definitions_dir):
            for file_nr, json_file in enumerate(self.batch.sio.get_files_from_dir(definitions_dir, types="json")):
                self.batch.logger.inf(("loading definition: ", json_file))
                json_definition = self.comfun.load_json_file(definitions_dir+json_file)
                if json_definition is not None and "definition" in json_definition.keys():
                    self.batch.logger.db(("definition loaded: ", json_file))

                    if self.sts.runtime_env == json_definition['definition']['meta']['name']:
                        self.current_definition_name = self.sts.runtime_env
                        self.current_definition_index = file_nr

                    if json_definition['definition']['meta']['totalActions'] > 0:
                        if "name" in json_definition['definition']['meta']:
                            definition_name = json_definition['definition']['meta']["name"]
                            new_definition = SingleDefinition(definition_name, self.batch.logger)
                            if "software" in json_definition['definition']['meta']:
                                new_definition.software = json_definition['definition']['meta']["software"]
                            if "setupExt" in json_definition['definition']['meta']:
                                new_definition.setup_ext = json_definition['definition']['meta']['setupExt']
                            if "prevExt" in json_definition['definition']['meta']:
                                new_definition.prev_ext = json_definition['definition']['meta']['prevExt']
                            if "version" in json_definition['definition']['meta']:
                                new_definition.version = json_definition['definition']['meta']['version']
                            self.definitions_names.append(json_definition['definition']['meta']["name"])
                            self.add_definition(new_definition)

                            if "interactionScript" in json_definition['definition']['meta']:
                                inters_f = definitions_dir + json_definition['definition']['meta']["interactionScript"]
                                new_definition.interactions = self.load_interaction_file(inters_f)
                                if new_definition.interactions is None:
                                    loading_errors += 1
                                    self.batch.logger.err(("interaction file not loaded: ", inters_f), nl_after=True)

                            if "actions" in json_definition['definition']:
                                for li in json_definition['definition']['actions'].values():
                                    new_group_action = MultiAction(li['id'], li['name'])

                                    if li['type'] == "single":   # id:1  for all single SingleAction in group
                                        li_ui = self.get_ui_values(li)
                                        new_action = SingleAction(li['name'], li['desc'], li['template'], ui=li_ui)
                                        if "params" in li:
                                            new_action.parameters = li["params"]
                                        new_group_action.add_single_action(new_action)

                                    elif li['type'] == "multi":
                                        for ag in li["subActions"].values():
                                            ag_ui = self.get_ui_values(ag)
                                            new_action = SingleAction(li['name'], ag['desc'], ag['template'],
                                                                      mode=ag['mode'], ui=ag_ui)
                                            if "params" in ag:
                                                template = ag["params"]["paramsTemplate"]
                                                new_action.parameters = ActionParameters(ag['mode'], template)
                                                for key, val in ag["params"]["paramsList"].items():
                                                    new_action.parameters.add_param_to_list(key, val[0], val[1],
                                                                                            val[2], val[3])
                                                new_action.set_evos_possible(True)
                                            new_group_action.add_single_action(new_action)
                                    else:
                                        self.batch.logger.err(("wrong action type : ", li['type']))

                                    new_definition.add_group_action(new_group_action)
                            else:
                                self.batch.logger.wrn(("No actions defined in : ", json_file, " dir:", definitions_dir))
            return loading_errors
        else:
            self.batch.logger.err(("Definitions directory not exist: ", definitions_dir))
            return False

    def load_definitions_from_mysql(self):
        #  PRO version with sql
        self.batch.logger.inf("PRO version support SQL ")
        return False

    def clear_all_definions_data(self):
        del self.definitions_array[:]
        del self.definitions_names[:]
        self.total_definitions = 0
        self.current_definition = None
        self.current_definition_name = None
        self.current_definition_index = None

    def reload_definitions(self):
        self.clear_all_definions_data()
        ret = self.load_definitions()
        return ret

    def update_current_definition(self, index):
        if index is not None:
            self.batch.logger.deepdb(("update_current_definition ", index))
            if len(self.definitions_array) > index:
                self.current_definition_index = index
                self.current_definition = self.definitions_array[index]
                self.current_definition_name = self.definitions_array[index].name
                self.current_interactions = self.definitions_array[index].interactions
            else:
                self.batch.logger.wrn(("update current definition is not possible, definitions count:  ",
                                       len(self.definitions_array), "  try set:", index))
        else:
            self.batch.logger.wrn("trying update_current_definition by None")

    def update_current_definition_by_name(self, name):
        for i, d in enumerate(self.definitions_array):
            if d.name == name:
                self.update_current_definition(i)
