
import core.core as core

class SimBatchAPI:
    simbatch_core = None

    def __init__(self, ini_file="config.ini"):
        self.init_simbatch(ini_file=ini_file)

    def init_simbatch(self, ini_file="config.ini"):
        self.simbatch_core = core.SimBatch("no-gui", ini_file=ini_file)


    def load_data(self):
        self.simbatch_core.load_data()

    def get_data_path(self):
        return self.simbatch_core.sts.store_data_json_directory_abs

    def get_settings_path(self):
        return self.simbatch_core.sts.json_settings_data

    def create_example_data_if_not_exists(self):
        if self.simbatch_core.prj.total_projects == 0:
            self.simbatch_core.create_example_data()

    """   DEFINITIONS """

    

