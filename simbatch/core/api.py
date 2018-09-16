import core


class SimBatchAPI:
    simbatch_core = None
    user_inputs_add_to_queue = None

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
        self.simbatch_core.sio.create_data_directory_if_not_exist()
        if self.simbatch_core.prj.total_projects == 0:
            self.simbatch_core.sio.create_example_data()
            
    def create_api_example_if_not_exists(self):
        api_project_id = 0
        if self.simbatch_core.prj.is_project_exists("API example") is False:
            print " cereste API exmppl "
            api_project = self.simbatch_core.prj.get_example_single_project()
            api_project.project_name = "API example"
            api_project.description = "proj created by API example script"
            api_project_id = self.simbatch_core.prj.add_project(api_project, do_save=True)
        else:
            api_project_id = self.simbatch_core.prj.get_id_from_name("API example")
        
        api_schema_id = 0
        if self.simbatch_core.sch.is_schema_exists("Simple Schema") is False:
            api_simple_schema = self.simbatch_core.sch.get_example_single_schema()
            api_simple_schema.schema_name = "Simple Schema"
            api_simple_schema.actions_array = []
            api_simple_schema.project_id = api_project_id
            
            ret = self.simbatch_core.sch.add_schema(api_simple_schema, do_save=True)
            if ret is not False:
                api_schema_id = ret
            else:
                api_schema_id = 0
        else:
            api_schema_id = self.simbatch_core.sch.get_id_by_name("Simple Schema")
        
        api_task_id = 0
        if self.simbatch_core.tsk.is_task_exists("API tsk 1") is False:
            get_id_by_name
            api_task_1 = self.simbatch_core.tsk.get_blank_task()
            api_task_1.task_name = "API tsk 1"
            api_task_1.state_id = self.simbatch_core.sts.INDEX_STATE_WAITING
            api_task_1.state = self.simbatch_core.sts.states_visible_names[api_task_1.state_id]
            api_task_1.project_id = api_project_id
            api_task_1.schema_id = api_schema_id
            api_task_1.shot = "api01"
            api_task_1.description = "API example task 01"
        else:
            api_task_id = self.simbatch_core.tsk.get_id_by_name("API tsk 1")
            
            

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

    def create_task_options_object(self):
        return self.simbatch_core.tsk.create_task_options_object()

    #
    ##
    ###
    """    QUEUE     """

    def clear_green_items_from_queue(self):
        self.simbatch_core.que.remove_all_queue_items(only_done=True)
        self.simbatch_core.que.save_queue()

    def add_current_task_to_queue(self, evo=None, action_inputs=None, schema_options=None, task_options=None):
        sib = self.simbatch_core
        if evo is not None:
            evolutions = sib.pat.get_evolutions_from_string(evo)
            # TODO EVO !!!

        sib.tsk.increase_queue_ver()
        new_queue_items = sib.que.generate_queue_items(sib.tsk.max_id, action_inputs=action_inputs,
                                                       schema_options=schema_options, task_options=task_options)
        sib.que.add_to_queue(new_queue_items)
        sib.que.save_queue()

    def print_queue_header(self):
        self.simbatch_core.que.print_header()

    def print_last_queue_item(self):
        if self.simbatch_core.que.total_queue_items > 0:
            self.simbatch_core.que.print_queue_item(self.simbatch_core.que.queue_data[-1])
    #
    ##
    ###
    # TODO OOP
    """     user    interaction   """
    def create_inputs_object(self):
        self.user_inputs_add_to_queue = []
        return self.user_inputs_add_to_queue

    def add_user_input(self, txt):  # TODO user_inputs_object.add
        vals = self.simbatch_core.sio.predefined.convert_predefined_variables_to_values(txt)
        self.user_inputs_add_to_queue.append([vals])
