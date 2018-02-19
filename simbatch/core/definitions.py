try:
    import MaxPlus
except ImportError:
    pass

try:
    import hou
except ImportError:
    pass

from actions import MultiAction, SingleAction

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


# class SoftwareConnector:
#     currentSoft = -1
#
#     def __init__(self, current_soft):
#         self.currentSoft = current_soft
#
#     def load_scene(self, target ):
#         pass
#
#     def save_curent_scene_as(self, target ):
#         pass


class SingleDefinition:
    name = ""       # actions in schema are copied from definition for protect schema data if no definition
    version = 0     # version are useful for recognize exact source of definition
    software = ""   # TODO software name or software version ???
    #               # TODO list supported versions
    prev_ext = ""   # "prevExt" without dot "png"
    file_ext = ""   # "setupExt" without dot
    multi_actions_array = []    # old  GroupAction  grouped_actions_array
    total_actions = 0
    action_names = []

    interactions = None  # file with common functions for current definition

    def __init__(self, name, logger):
        self.name = name
        self.multi_actions_array = []
        self.action_names = []
        self.logger = logger

    def __repr__(self):
        return "SingleDefinition({})".format(self.software)

    def __str__(self):
        return "SingleDefinition"

    def print_total(self, prefix=""):
        print "   [INF] {} total actions:{}".format(prefix, self.total_actions)

    def print_all(self):
        for action_group in self.multi_actions_array:
            for ai in action_group.actions:
                ai.print_minimum()
        self.print_total()

    def print_single(self):
        logger_raw = self.logger.raw
        logger_raw("\n\n name:{} total_actions:{} names count:{}".format(self.name, self.total_actions,
                                                                         len(self.action_names)))
        for i, an in enumerate(self.action_names):
            logger_raw("  arr action_names:{}  {} ".format(i, an))
        for i, ga in enumerate(self.multi_actions_array):
            if ga.actions_count == len(ga.actions):
                logger_raw("  _group_name:{} {}  count: {}".format(i, ga.name, ga.actions_count))
            else:
                logger_raw("  _group_name:{} {}  ERR count : {} != {} ".format(i, ga.name, ga.actions_count,
                                                                               len(ga.actions)))
            for j, sa in enumerate(ga.actions):
                logger_raw("    ___action {}  name:{}  default_value:{}  ui:{}".format(j, sa.name,
                                                                                       sa.default_value, sa.ui))

    def add_group_action(self, element):
        self.multi_actions_array.append(element)
        self.total_actions += 1
        self.action_names.append(element.name)

    def get_base_setup_ext(self):
        return self.file_ext

    def get_prev_ext(self):
        return self.prev_ext


class ExampleInteractions:

    def __init__(self):
        self.load()

    @staticmethod
    def load():
        print " [interact example] loaded "

    @staticmethod
    def test():
        print " [interact example] test "

    @staticmethod
    def maya_get_scene_objects():
        print " [interact example]      def maya_get_scene_objects "


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

    current_interactions = None        # OLD soco = None   # software connector

    def __init__(self, batch):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.definitions_array = []
        self.definitions_names = []
        # self.soco = SoftwareConnector(batch.sch.current_schema_software_id)

        # self.current_interactions = ExampleInteractions()

    def __repr__(self):
        return "Definitions({})".format(self.batch)

    def __str__(self):
        return "Definitions"

    #  print project data, for debug
    def print_current(self):
        print "     current definition index: {}   name: {}  total_: {}\n".format(self.current_definition_index,
                                                                                  self.current_definition_name,
                                                                                  self.total_definitions)

    #  print definitions data, for debug
    def print_total(self, print_children=False):
        if print_children:
            for i, d in enumerate(self.definitions_array):
                d.print_total(prefix="Definition "+str(i))
        print "   [INF] Definitions total_definitions:", self.total_definitions

    def print_all(self, print_children=False):
        for d in self.definitions_array:
            print "\n\n   software:{}".format(d.software)
            if print_children:
                d.print_all()
        if self.total_definitions == 0:
            print "   [INF] no definition loaded"
        else:
            print "   [INF] definition total:", self.total_definitions

    def get_definitions(self):
        return self.definitions_array

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

    @staticmethod
    def get_ui_values(li):
        if "ui" in li:
            return li["ui"]
        else:
            return None

    def get_example_definition(self):
        example_defi = SingleDefinition("example_defi", self.batch.logger)
        example_group_actions = MultiAction(1, "example a gr")
        example_action = SingleAction("ex_a", "desc", "<def>", "templ <o>", mode="single",
                                      ui=(("Tst", "print('ex')"), ("Tst", "print('ex')")))
        example_group_actions.add_single_action(example_action)
        example_defi.add_group_action(example_group_actions)
        return example_defi

    # TODO move to common !!!!
    def class_from_file(self, filename):
        with file(filename) as f:
            content = f.read()
        try:
            exec content
            return eval("Interaction")
        except SyntaxError:
            self.batch.logger.err(("syntax error definition file:", filename))
            return None
    # TODO move to common !!!!

    def load_interaction_file(self, file_path):
        self.batch.logger.db(("__load_interaction_file: ", file_path))
        if self.batch.os == "win":
            file_path = file_path.replace("/", "\\")
        if self.comfun.file_exists(file_path):
            InteractionClass = self.class_from_file(file_path)
            if InteractionClass is None:
                return None
            else:
                loaded_interaction = InteractionClass()
            return loaded_interaction
        else:
            return None

    def load_definitions_from_jsons(self, definitions_dir=""):
        if len(definitions_dir) == 0:
            definitions_dir = self.sts.store_definitions_directory
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

                            if "actions" in json_definition['definition']:
                                for li in json_definition['definition']['actions'].values():
                                    new_group_action = MultiAction(li['id'], li['name'])

                                    if li['type'] == "single":   # id:1  for all single SingleAction in group
                                        li_ui = self.get_ui_values(li)
                                        new_action = SingleAction(li['name'], li['desc'], li['default'],
                                                                  li['template'], ui=li_ui)
                                        new_group_action.add_single_action(new_action)

                                    elif li['type'] == "multi":
                                        for ag in li["subActions"].values():
                                            ag_ui = self.get_ui_values(ag)
                                            new_action = SingleAction(li['name'], ag['desc'], ag['default'],
                                                                      ag['template'], mode=ag['mode'], ui=ag_ui)
                                            new_group_action.add_single_action(new_action)
                                    new_definition.add_group_action(new_group_action)
                            else:
                                self.batch.logger.wrn(("No actions defined in : ", json_file, " dir:", definitions_dir))
            # self.print_all(print_children=True)
            # self.print_total(print_children=True)
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
        self.batch.logger.deepdb(("update_current_definition ", index))
        if len(self.definitions_array) > index:
            self.current_definition_index = index
            self.current_definition = self.definitions_array[index]
            self.current_definition_name = self.definitions_array[index].name
            self.current_interactions = self.definitions_array[index].interactions
        else:
            self.batch.logger.wrn(("update current definition is not possible, definitions count:  ",
                                   len(self.definitions_array), "  try set:", index))

        # if self.current_interactions is not None:
        #    self.current_interactions.test()
