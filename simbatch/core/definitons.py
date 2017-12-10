try:
    import MaxPlus
except ImportError:
    pass

try:
    import hou
except ImportError:
    pass

import os


class SoftwareConnector():
    currentSoft = -1

    def __init__(self, currentSoft):
        self.currentSoft = currentSoft

    def load_scene(self, target ):
        pass

    def save_curent_scene_as(self, target ):
        pass




class Definitions:
    batch = None
    comfun = None

    definitions_array =[]
    total_definitions = 0
    current_definition = ""
    # current_software_id = 0

    soco = None   # software connector

    def __init__(self, batch):
        self.batch = batch
        self.s = batch.s
        self.comfun = batch.comfun

        self.soco = SoftwareConnector(batch.c.current_schema_software_id)

    def get_definitions(self):
        return False


    def load_definitions(self):
        if self.s.store_data_mode == 1:
            return self.load_definitions_from_jsons()
        if self.s.store_data_mode == 2:
            return self.load_definitions_from_mysql()


    def load_definitions_from_jsons(self, definitions_dir=""):
        if len(definitions_dir) == 0:
            #json_file = self.s.store_data_json_directory + self.s.JSON_SCHEMAS_FILE_NAME
            definitions_dir = self.s.store_data_definitions_directory

        if self.comfun.file_exists(definitions_dir):
            for json_file in self.batch.i.get_files_from_dir(definitions_dir, types="json"):
                print " yyy json_file", json_file
                pass
        return True




        # if self.comfun.file_exists(json_file, info="schemas file"):
        #     if self.s.debug_level >= 3:
        #         print " [INF] loading schemas: " + json_file
        #     json_schemas = self.comfun.load_json_file(json_file)
        #     if json_schemas is not None and "schemas" in json_schemas.keys():
        #         if json_schemas['schemas']['meta']['total'] > 0:
        #             for li in json_schemas['schemas']['data'].values():
        #                 if len(li) == len(SCHEMA_ITEM_FIELDS_NAMES):
        #                     for lia in li['actions']:
        #                         print " actions "   # TODO
        #                     # new_schema_actions = [Action()]
        #                     new_schema_actions = []
        #                     new_schema_item = SchemaItem(int(li['id']), li['name'], int(li['stateId']), li['state'],
        #                                                  int(li['projId']), int(li['definition']), int(li['version']),
        #                                                  new_schema_actions, li['desc'])
        #                     self.add_schema(new_schema_item)
        #                 else:
        #                     if self.s.debug_level >= 2:
        #                         print "   [WRN] schema data not consistent: {} {}".format(len(li),
        #                                                                                   len(SCHEMA_ITEM_FIELDS_NAMES))
        #             return True
        #     else:
        #         if self.s.debug_level >= 2:
        #             print " [WRN] no projects data in : ", json_file
        #         return False
        # else:
        #     if self.s.debug_level >= 1:
        #         print " [ERR] no schema file: " + json_file
        #         return False


    @staticmethod
    def load_definitions_from_mysql():
        #  PRO version with sql
        pass


    def save_definitions(self):
        return False


    @staticmethod
    def save_definitions_to_mysql():
        #  PRO version with sql
        pass
