import core


class SimBatchAPI:
    simbatch_core = None
    user_inputs_add_to_queue = None

    def __init__(self, ini_file="config.ini"):
        self.init_simbatch(ini_file=ini_file)

    def init_simbatch(self, ini_file="config.ini"):
        self.simbatch_core = core.SimBatch("no-gui", ini_file=ini_file)

    def hello_world(self):
        print self.simbatch_core.sts.random_welcome_message()

    def load_data(self):
        self.simbatch_core.load_data()

    def get_data_path(self):
        return self.simbatch_core.sts.store_data_json_directory_abs

    def get_settings_path(self):
        return self.simbatch_core.sts.json_settings_data

    def create_example_data_if_not_exists(self):
        self.simbatch_core.sio.create_data_directory_if_not_exist()
        if self.simbatch_core.prj.total_projects == 0:
            self.simbatch_core.sio.create_example_data()
            
    def create_api_example_if_not_exists(self):
        ret = self.simbatch_core.sio.create_api_example_data()
        if ret is not False:
            api_task_id = ret
            self.set_current_definition("Maya")
            self.set_current_project(last=True)
            self.set_current_schema(last=True)
            self.set_current_task(last=True)
            task_options = self.create_task_options_object(task=api_task_1)
            task_options.set_task_value("description", "example api")
            self.add_current_task_to_queue(task_options=task_options)
            self.batch.logger.inf("Created API task example")
        else:
            self.batch.logger.err("Not created API task example")
            api_task_id = 0
            

    def print_basic_data_info(self):
        self.simbatch_core.print_important_values()

    #
    ##
    ###
    """   DEFINITIONS """
    def set_current_definition(self, definition_name):
        self.simbatch_core.dfn.update_current_definition_by_name(definition_name)
        # TODO return !

    #
    ##
    ###
    """   PROJECTS    """
    def set_current_project(self, last=True, project_id=None):
        if last:
            self.simbatch_core.prj.update_current_from_id(self.simbatch_core.prj.max_id)
        if project_id is not None:
            # TODO is number ?
            self.simbatch_core.prj.update_current_from_id(project_id)
        # TODO return id or false

    #
    ##
    ###
    """   SCHEMAS    """
    def set_current_schema(self, last=True, schema_id=None):
        if last is True:
            self.simbatch_core.sch.update_current_from_id(self.simbatch_core.tsk.tasks_data[-1].schema_id)
        if schema_id is not None:
            # TODO is number ?
            self.simbatch_core.sch.update_current_from_id(schema_id)
        # TODO return id or false

    def get_schema_options_object(self):
        return self.simbatch_core.sch.create_schema_options_object()
    #
    ##
    ###
    """   TASKS      """
    def set_current_task(self, last=True, task_id=None):
        if last is True:
            self.simbatch_core.tsk.update_current_from_id(self.simbatch_core.tsk.max_id)
        if task_id is not None:
            # TODO is number ?
            self.simbatch_core.tsk.update_current_from_id(task_id)
        # TODO return id or false

    def create_task_options_object(self, task=None):
        return self.simbatch_core.tsk.create_task_options_object(task=task)

    #
    ##
    ###
    """    QUEUE     """

    def clear_green_items_from_queue(self):
        self.simbatch_core.que.remove_queue_items(only_done=True)
        self.simbatch_core.que.save_queue()

    def add_current_task_to_queue(self, evo=None, schema_options=None, task_options=None):
        sib = self.simbatch_core
        sib.tsk.increase_queue_ver()
        new_queue_items = sib.que.generate_queue_items(sib.tsk.max_id, evo=evo, schema_options=schema_options,
                                                       task_options=task_options)
        sib.que.add_to_queue(new_queue_items)
        sib.que.set_last_as_current()
        sib.que.save_queue()

    def print_queue_info(self):
        self.simbatch_core.que.print_info()

    def print_last_queue_item(self):
        if self.simbatch_core.que.total_queue_items > 0:
            self.simbatch_core.que.print_queue_item(self.simbatch_core.que.queue_data[-1])
    #
    ##
    ###
    # TODO OOP
    """     user    interaction   """




