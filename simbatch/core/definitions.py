try:
    import MaxPlus
except ImportError:
    pass

try:
    import hou
except ImportError:
    pass

# import os

# JSON Name Format, PEP8 Name Format
DEFINITION_ITEM_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'definition_name'),
    ('version', 'definition_version'),
    ('actions', 'actions_array'),
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


class SingleAction:
    id = None
    name = ""

    def __init__(self, action_id, name, description, default_value, template, mode=None, addi_butt=None, addi_fun=None):
        self.id = action_id
        self.name = name
        self.mode = mode  # subaction mode
        self.description = description
        self.default_value = default_value
        self.template = template

        self.addional_butt_caption = addi_butt
        self.addional_funcion_name = addi_fun

    def __repr__(self):
        return "SingleAction({},{})".format(self.action_id, self.name)

    def __str__(self):
        return "SingleAction"

    def print_minimum(self):
        print "   action: {}   id:{}   default_value:{}".format(self.name, self.id, self.default_value)

    def print_action(self):
        print "   action: {}   id:{}   description:{} default_value:{}, template:{}".format(self.name, self.id,
                                                                                            self.description,
                                                                                            self.default_value,
                                                                                            self.template)

    def get_action(self):
        return self

    def get_action_as_string(self):
        return


class GroupAction:
    id = None
    name = ""
    actions = []  # subactions as [SingleAction,...]
    current_sub_action_index = 0

    def __init__(self, action_id, name):
        self.id = action_id
        self.name = name
        self.actions = []
        pass

    def __repr__(self):
        return "GroupAction({},{})".format(self.name, self.name)

    def __str__(self):
        return "GroupAction"

    def get_action(self):
        return self.actions[self.current_sub_action_index]


class SingleDefinition:
    name = ""
    prev_ext = ""   # without dot "png"
    file_ext = ""   # without dot
    actions_array = []    # SingleAction or GroupAction
    total_actions = 0
    action_names = []
    # TODO list supported versions

    def __init__(self, software):
        self.software = software
        self.actions_array = []
        self.definitions_names = []
        self.action_names = []

    def __repr__(self):
        return "SingleDefinition({})".format(self.software)

    def __str__(self):
        return "SingleDefinition"

    def print_total(self, prefix=""):
        print "   [INF] {} total actions:{}".format(prefix, self.total_actions)

    def print_all(self):
        for a in self.actions_array:
            if isinstance(a, SingleAction):
                a.print_minimum()
            else:  # GroupAction
                if 'actions' in dir(a):
                    for ai in a.actions:
                        ai.print_minimum()
        self.print_total()

    def add_single_or_group_action(self, element):
        self.actions_array.append(element)
        self.total_actions += 1
        self.action_names.append(element.name)

    def get_base_setup_ext(self):
        return self.file_ext

    def get_prev_ext(self):
        return self.prev_ext


class Definitions:
    batch = None
    comfun = None

    definitions_array = []
    definitions_names = []

    total_definitions = 0
    current_definition = None

    # current_software_id = 0
    # soco = None   # software connector
    current_interact = None

    def __init__(self, batch):
        self.batch = batch
        self.s = batch.s
        self.comfun = batch.comfun
        self.definitions_array = []
        self.definitions_names = []
        # self.soco = SoftwareConnector(batch.c.current_schema_software_id)

    def __repr__(self):
        return "Definitions({})".format(self.batch)

    def __str__(self):
        return "Definitions"

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
        if self.s.store_data_mode == 1:
            return self.load_definitions_from_jsons()
        if self.s.store_data_mode == 2:
            return self.load_definitions_from_mysql()

    @staticmethod
    def get_additional_button_values(li):
        if "additionalButton" in li:
            return li["additionalButton"], li["additionalButtonFunction"]
        else:
            return None, None

    def load_definitions_from_jsons(self, definitions_dir=""):
        if len(definitions_dir) == 0:
            definitions_dir = self.s.store_definitions_directory

        if self.comfun.file_exists(definitions_dir):
            for json_file in self.batch.i.get_files_from_dir(definitions_dir, types="json"):
                self.batch.logger.inf(("loading definition: ", json_file))
                json_definition = self.comfun.load_json_file(definitions_dir+json_file)
                if json_definition is not None and "definition" in json_definition.keys():
                    self.batch.logger.db(("definition loaded: ", json_file))
                    if json_definition['definition']['meta']['total'] > 0:
                        new_definition = SingleDefinition(json_definition['definition']['meta']["software"])
                        if "setupExt" in json_definition['definition']['meta']:
                            new_definition.setup_ext = json_definition['definition']['meta']['setupExt']
                        if "prevExt" in json_definition['definition']['meta']:
                            new_definition.prev_ext = json_definition['definition']['meta']['prevExt']
                        self.definitions_names.append(json_definition['definition']['meta']["software"])
                        self.add_definition(new_definition)
                        for li in json_definition['definition']['actions'].values():

                            addi_vals = self.get_additional_button_values(li)

                            if li['type'] == "single":
                                new_action = SingleAction(li['id'], li['name'], li['desc'], li['default'],
                                                          li['template'], addi_butt=addi_vals[0], addi_fun=addi_vals[1])
                                new_definition.add_single_or_group_action(new_action)

                            elif li['type'] == "group":
                                new_group_action = GroupAction(li['id'], li['name'])
                                new_group_action.name = li['name']
                                for ag in li["subActions"].values():
                                    addi_vals = self.get_additional_button_values(ag)
                                    new_action = SingleAction(ag['id'], li['name'], ag['desc'], ag['default'],
                                                              ag['template'], mode=ag['mode'],
                                                              addi_butt=addi_vals[0], addi_fun=addi_vals[1])
                                    new_group_action.actions.append(new_action)
                                new_definition.add_single_or_group_action(new_group_action)
            # self.print_all(print_children=True)
            # self.print_total(print_children=True)
            return True
        else:
            self.batch.logger.err(("Definitions directory not exist: ", definitions_dir))
            return False

    @staticmethod
    def load_definitions_from_mysql():
        #  PRO version with sql
        pass
