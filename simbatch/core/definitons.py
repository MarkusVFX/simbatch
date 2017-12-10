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
        self.comfun = batch.comfun

        self.soco = SoftwareConnector(batch.c.current_schema_software_id)
