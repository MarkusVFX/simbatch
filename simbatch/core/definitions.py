try:
    import MaxPlus
except ImportError:
    pass

try:
    import hou
except ImportError:
    pass

from actions import GroupedActions, SingleAction

# import os


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
    name = ""
    software = ""
    prev_ext = ""   # without dot "png"
    file_ext = ""   # without dot
    # actions_array = []    # SingleAction or GroupAction
    grouped_actions_array = []    # GroupAction array
    total_actions = 0
    action_names = []
    # TODO list supported versions

    def __init__(self, name):
        self.name = name
        self.grouped_actions_array = []
        self.action_names = []

    def __repr__(self):
        return "SingleDefinition({})".format(self.software)

    def __str__(self):
        return "SingleDefinition"

    def print_total(self, prefix=""):
        print "   [INF] {} total actions:{}".format(prefix, self.total_actions)

    def print_all(self):
        for action_group in self.grouped_actions_array:
            for ai in action_group.actions:
                ai.print_minimum()
        self.print_total()

    def add_group_action(self, element):
        self.grouped_actions_array.append(element)
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
    current_definition_name = None     # current definition name  (unique name)
    current_definition_index = None    # current definition index (array index)

    # current_software_id = 0
    # soco = None   # software connector
    current_interact = None

    def __init__(self, batch):
        self.batch = batch
        self.sts = batch.sts
        self.comfun = batch.comfun
        self.definitions_array = []
        self.definitions_names = []
        # self.soco = SoftwareConnector(batch.sch.current_schema_software_id)

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
        if self.sts.store_data_mode == 1:
            ret = self.load_definitions_from_jsons()
        if self.sts.store_data_mode == 2:
            ret = self.load_definitions_from_mysql()

        if self.current_definition_name is None:
            if self.total_definitions > 0:
                self.current_definition_name = self.definitions_names[0]  #   self.definitions_array[0].name
                self.current_definition_index = 0
            else:
                self.batch.logger.wrn("No definition loaded!")
        return ret

    # @staticmethod
    # def get_additional_button_values(li):
    #     if "additionalButton" in li:
    #         return li["additionalButton"], li["additionalButtonFunction"]
    #     else:
    #         return None, None

    @staticmethod
    def get_ui_values(li):
        # print "\ntest  zzz  li " , li
        if "ui" in li:
            return li["ui"] # ,  li["additionalButtonFunction"]
        else:
            return None



    def get_example_definition(self):
        example_defi = SingleDefinition("example_defi")
        example_group_actions = GroupedActions()
        example_defi.add_group_action()
        return example_defi

    def load_definitions_from_jsons(self, definitions_dir=""):
        if len(definitions_dir) == 0:
            definitions_dir = self.sts.store_definitions_directory

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
                            new_definition = SingleDefinition(definition_name)
                            if "software" in json_definition['definition']['meta']:
                                new_definition.software = json_definition['definition']['meta']["software"]
                            if "setupExt" in json_definition['definition']['meta']:
                                new_definition.setup_ext = json_definition['definition']['meta']['setupExt']
                            if "prevExt" in json_definition['definition']['meta']:
                                new_definition.prev_ext = json_definition['definition']['meta']['prevExt']
                            self.definitions_names.append(json_definition['definition']['meta']["name"])
                            self.add_definition(new_definition)

                            if "actions" in json_definition['definition']:
                                for li in json_definition['definition']['actions'].values():

                                    # print "\n loaddd",  file_nr ,  li
                                    # addi_vals = self.get_additional_button_values(li)
                                    new_group_action = GroupedActions(li['id'], li['name'])

                                    if li['type'] == "single":   # id:1  for all single SingleAction in group
                                        # new_action = SingleAction(1, li['name'], li['desc'], li['default'],
                                        #                           li['template'], addi_butt=addi_vals[0],
                                        #                           addi_fun=addi_vals[1])
                                        li_ui = self.get_ui_values(li)
                                        new_action = SingleAction(1, li['name'], li['desc'], li['default'],
                                                                  li['template'], ui=li_ui)
                                        new_group_action.add_single_action(new_action)

                                    elif li['type'] == "group":
                                        for ag in li["subActions"].values():
                                            # addi_vals = self.get_additional_button_values(ag)
                                            ag_ui = self.get_ui_values(ag)
                                            # new_action = SingleAction(ag['id'], li['name'], ag['desc'], ag['default'],
                                            #                           ag['template'], mode=ag['mode'],
                                            #                           addi_butt=addi_vals[0], addi_fun=addi_vals[1])
                                            new_action = SingleAction(ag['id'], li['name'], ag['desc'], ag['default'],
                                                                      ag['template'], mode=ag['mode'], ui=ag_ui)
                                            new_group_action.add_single_action(new_action)
                                    new_definition.add_group_action(new_group_action)
                                    # print "\n new_group_action: ", new_group_action
                            else:
                                self.batch.logger.wrn(("No actions defined in : ", json_file, " dir:", definitions_dir))
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
