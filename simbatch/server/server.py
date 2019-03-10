import os
import subprocess
import threading
import time


class SimBatchServer:
    timer_delay_seconds = 3  # delay for each loop execution
    loops_counter = 0        # total loops executed
    jobs_computed = 0        # count computed jobs (queue items) by this server'ssession
    jobs_limit = 0           # if act as server 0:infinite loop, >0 limit jobs to compute
    mode = None              # "single" or "all"
    framework_mode = False   # True: execution form framework,  False: execution from server

    current_simnode_state = None
    server_name = None

    batch = None
    logger = None
    force_software = 0
    break_loop = False

    server_dir = ""
    state_file_name = "state.txt"
    log_file_name = "log.txt"
    script_execute = "script_execute.py"

    last_info = ""
    report_total_jobs = 0
    report_done_jobs = 0

    def __init__(self, batch, force_software=0, jobs_limit=0, framework_mode=False):
        self.force_software = force_software
        self.jobs_limit = jobs_limit
        if framework_mode:
            self.framework_mode = True
        self.batch = batch
        self.logger = batch.logger
        self.comfun = batch.comfun
        if self.framework_mode is False:
            ret = self.batch.que.load_queue()
            if ret:
                if self.batch.que.total_queue_items == 0:
                    self.logger.inf("Queue data is empty, nothing loaded")
                    self.batch.que.print_info()
            else:
                self.logger.err("Queue data not loaded !")

        ''' elif self.framework_mode is True: queue is already loaded ! (no need to load) '''

        self.server_dir = os.path.dirname(os.path.realpath(__file__)) + self.batch.sts.dir_separator
        self.test_server_dir()

        simnode_state_file = self.server_dir + self.state_file_name

        if framework_mode:
            self.current_simnode_state = 0
        else:
            node_info = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
            if node_info is not None:
                if node_info is not False:
                    """ state file exists """
                    self.current_simnode_state = node_info.state_id
                    self.server_name = node_info.node_name

                    """  init batch.nod vars as server """
                    self.batch.nod.state_file = simnode_state_file
                    self.batch.nod.server_name = node_info.node_name

                    """  check existence in database  """
                    state_file = self.batch.nod.get_state_file(server_name=str(self.server_name))
                    if state_file is False:
                        """  try to add simnode state file to database  """
                        pass  # TODO !!!
                    if state_file != simnode_state_file:
                        """  try to fix simnode state file in database  """
                        pass  # TODO !!!
                else:
                    self.logger.err(("State file empty or corrupted :", simnode_state_file))
                    self.logger.err("Server NOT initiated properly!")
            else:
                self.logger.err(("State file not exist:", simnode_state_file))
                self.logger.err("Server NOT initiated properly!")
        
        if self.framework_mode is True:
            print_server_name = batch.sts.runtime_env + " (local)"
        else:
            simnode_name = self.batch.nod.get_server_name_from_file(simnode_state_file)
            print_server_name = "{} ({})".format(batch.sts.runtime_env, simnode_name)
        self.logger.inf(("init server :", print_server_name, self.server_dir))
        
    def print_is_something_to_do(self):
        ret = self.is_something_to_do()
        if ret[0] == 1:
            self.logger.inf(("Something to do: ", ret[1]), force_prefix=" > ")
        else:
            self.logger.inf("Nothing to do", force_prefix=" > ")
        
    def print_server_info(self):
        self.logger.raw("\n\n\n")
        
        simnode_state_file = self.server_dir + self.state_file_name
        self.logger.inf("Local server state file: {}".format(simnode_state_file), force_prefix=" > ")
            
        if self.comfun.file_exists(simnode_state_file):
            node_info = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
            if node_info is not None:
                if node_info is not False:
                    ''' state file exists '''
                    info = "Found server name: {} ".format(node_info.node_name)
                    self.logger.inf(info, force_prefix=" ! ", nl=True)
                    info = "Server local state: {}  {} ".format(node_info.state_id,
                                                                self.batch.sts.states_visible_names[node_info.state_id])
                    self.logger.inf(info, force_prefix=" ! ", nl=True)

                    node_index = self.batch.nod.get_node_index_by_name(node_info.node_name)
                    if node_index is not False:
                        if node_index >= 0:
                            self.batch.nod.print_node(node_index)
                            self.print_is_something_to_do()
                        else:
                            self.logger.err("Found {} duplicates in database for name:{}".format(str(node_index*-1),
                                                                                                 node_info.node_name))
                    else:
                        self.logger.err("Server name {} not found in database".format(node_info.node_name))
                else:
                    self.logger.err(("State file empty or corrupted :", simnode_state_file))
            else:
                self.logger.err(("State file not exist:", simnode_state_file))
        else:
            self.logger.wrn("Server state file not exit!")
      
    def add_node_to_database(self, name):
        if len(name) > 0:
            node_index = self.batch.nod.get_node_index_by_name(name, force_db=True)
            if node_index is False:
                simnode_state_file = self.server_dir + self.state_file_name
                node_index = self.batch.nod.get_node_index_by_state_file(simnode_state_file)
                if node_index is False:
                    if self.comfun.file_exists(simnode_state_file):
                        self.logger.inf("Local server state file exist: {}".format(simnode_state_file),
                                        force_prefix=" > ")
                    else:
                        self.logger.inf("Local server state file NOT exist: {}".format(simnode_state_file),
                                        force_prefix=" > ")

                        create_ret = self.batch.nod.create_node_state_file(simnode_state_file, name,
                                                                           self.batch.sts.INDEX_STATE_WAITING)
                        if create_ret:
                            self.logger.inf("Local server state file created: {}".format(simnode_state_file),
                                            force_prefix=" > ")

                    node_info = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
                    if node_info is not None:
                        if node_info is not False:
                            if 0 <= node_info.state_id < len(self.batch.sts.states_visible_names):
                                state_name = self.batch.sts.states_visible_names[node_info.state_id]
                                new_node_entry = self.batch.nod.get_new_node(node_info.node_name, state_name,
                                                                             node_info.state_id, simnode_state_file, "")
                                return self.batch.nod.add_simnode(new_node_entry, do_save=True)
                            else:
                                self.logger.err("Wrong state id in state file")
                        else:
                            self.logger.err(("State file empty or corrupted :", simnode_state_file))
                    else:
                        self.logger.err(("State file not exist:", simnode_state_file))
                else:
                    self.logger.wrn("Server state file exist on database! Skipped adding")
            else:
                self.logger.wrn("Server name exist on database! Skipped adding")
        else:
            self.logger.err("Server name is empty! Please set status file")
        
        return False

    """  test loading state, status file, database  """
    def do_all_tests(self):
        self.logger.raw("\n\n\n")
        '''  test loading data  '''
        if self.batch.sts.loading_state >= 4:
            self.logger.inf("Settings loaded", force_prefix=" > ")
        else:
            self.logger.err("Settings NOT loaded")
        
        '''  test data access  '''
        if self.batch.sts.store_data_mode == 1:
            ret = self.batch.load_data()
            if ret[0]:
                self.logger.inf("Simbatch data loaded with no errors or warnings ", force_prefix=" > ")
            elif ret[0] > 0:  
                self.logger.wrn("Simbatch data loaded with {} errors".format(ret[0]))
            else:
                self.logger.err("Critical error during data loading! ({})".format(ret))
        else:
            pass
            # SQL with PRO version
            
        '''  test local node status file  '''
        if len(self.server_dir) > 0:
            self.batch.comfun.test_directory_access(self.server_dir)
            
            if len(self.state_file_name) > 0:
                simnode_state_file = self.server_dir + self.state_file_name
                self.logger.inf("Local server state file: {}".format(simnode_state_file), force_prefix=" > ")
                    
                if self.comfun.file_exists(simnode_state_file):
                    node_info = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
                    if node_info is not None:
                        if node_info is not False:
                            ''' state file exists '''
                            state_name = self.batch.sts.states_visible_names[node_info.state_id]
                            info = "Found server name: {}    server state: {}  {} ".format(node_info.node_name,
                                                                                           node_info.state_id, state_name)
                            self.logger.inf(info, force_prefix=" ! ")
                        else:
                            self.logger.err(("State file empty or corrupted :", simnode_state_file))
                    else:
                        self.logger.err(("State file not exist:", simnode_state_file))
                else:
                    self.logger.err("Local state file not exist!  ({})".format(simnode_state_file))
            else:
                self.logger.err("Variable  self.state_file_name  is undefined!")
        else:
            self.logger.err("Server dir not defined! Variable  self.server_dir  is not defined!")

        '''  test master source update  '''
        master_source_path = self.get_existing_source_path()
        if master_source_path is not None:
            self.logger.inf("Master source path exist: {}".format(master_source_path), force_prefix=" > ")
            self.comfun.test_directory_access(master_source_path, "master source")
        else:
            self.logger.err("Master source path NOT exist")
       
        self.print_is_something_to_do()
            
    def reset_status(self):        
        simnode_state_file = self.server_dir + self.state_file_name   # TODO create def check simnode state file +global
        if self.comfun.file_exists(simnode_state_file):
            node_name = self.batch.nod.get_server_name_from_file(simnode_state_file)
            if len(node_name) > 0:
                INDEX_WAITING = self.batch.sts.INDEX_STATE_WAITING
                NAME_WAITING = self.batch.sts.states_visible_names[INDEX_WAITING]
                ret = self.batch.nod.create_node_state_file(simnode_state_file, node_name, INDEX_WAITING,
                                                            update_mode=True)
                if ret:
                    info = "Local server status updated  {} ".format(INDEX_WAITING)
                    self.logger.inf(info)
                    node_index = self.batch.nod.get_node_index_by_name(node_name)
                    if node_index is False:
                        self.add_node_to_database(node_name)
                    elif node_index >= 0:
                        ret = self.batch.nod.set_node_state_in_database(node_index, INDEX_WAITING)
                        if ret:
                            self.logger.inf("Simnode state updated in database to {}".format(NAME_WAITING))
                        else:
                            self.logger.err("Detected duplicated server name in database, please cleanup simnodes data")
                    else:
                        self.logger.err("Detected server name duplication in database, please cleanup simnodes data")
                else:
                    self.logger.err("Cant get server name from status file: {}".format(simnode_state_file))
            else:
                self.logger.err("Data not consistent in file: {} ".format(simnode_state_file))
        else:
            self.logger.err("Local state file not exist!  ({})".format(simnode_state_file))
        
    def test_server_dir(self):
        # TODO test write access create data dir
        pass
        
    def get_existing_source_path(self):
        if self.batch.sts.installation_directory_abs is None:
            return None
        source_path = self.batch.sts.installation_directory_abs + "/"
        if self.batch.comfun.path_exists(source_path):
            return source_path
        else:
            return None

    def update_sources_from_master(self):
        self.update_sources()
        
    def update_sources_to_master(self):
        self.update_sources(reverse_to_master=True)
        
    def update_sources(self, reverse_to_master=False):
        if self.batch.sts.installation_directory_abs is not None:
            # TODO self.batch.sts.dir_separator  vs universal separator
            source_path = self.get_existing_source_path()
            if source_path is not None:
                dst_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
            
                if reverse_to_master:
                    source_path, dst_path = dst_path, source_path
            
                if self.batch.sts.current_os == 2:
                    source_path = self.batch.comfun.convert_to_win_path(source_path)
                    dst_path = self.batch.comfun.convert_to_win_path(dst_path)

                ret_r = self.batch.comfun.test_directory_access(source_path, with_info=False)[0]
                ret_w = self.batch.comfun.test_directory_access(dst_path, with_info=False)[1]
                if ret_r and ret_w:
                    #
                    self.logger.inf(("update sources from  {}  ".format(source_path)), nl=True)
                    self.batch.sio.copy_file(source_path, dst_path, "server.py", sub_dir="server")
                    self.batch.sio.copy_tree(str(source_path), str(dst_path), sub_dir="core")
                    #
                else:
                    if ret_r is False:
                        self.logger.err("could NOT read from source path  {} ".format(source_path))
                    if ret_w is False:
                        self.logger.err("could NOT save to destination path  {} ".format(dst_path))
            else:
                self.logger.err("master source path  {}  not exist".format(source_path))
        else:
            self.logger.err("(update_sources_from_master) installation_directory_abs is not defined")
        
    def add_to_log(self, info, log_file=None):
        date = self.comfun.get_current_time()
        if log_file is None:
            log_file = self.server_dir + self.log_file_name
        f = open(log_file, 'a')
        f.write(date + " " + info + '; \n')
        f.close()
        self.logger.log(info)

    def reset(self):
        self.jobs_computed = 0
        self.loops_counter = 0
        self.reset_report()

    def reset_report(self):
        self.report_total_jobs = 0
        self.report_done_jobs = 0

    def generate_report(self):   # TODO
        return self.report_total_jobs, self.report_done_jobs
        
    # def set_database_node_state(self, queue_id, state, state_id, server_name, state_file):
    #     return self.batch.nod.update_node_state_file(state_file, server_name, state_id)
 
    def set_simnode_state(self, state_id):
        if self.server_name is not None:
            # simnode_state_file = self.server_dir + self.state_file_name   # TODO create  def check simnode state file    ret = self.batch.nod.set_node_state(simnode_state_file, self.server_name, state_id)
            
            self.batch.nod.set_curent_node_state(state_id)
            # TODO  check ret
            node_index = self.batch.nod.get_node_index_by_name(self.server_name)
            if node_index is not None:
                ret = self.batch.nod.set_node_state_in_database(node_index, state_id)
                # TODO  check ret
        else:
            self.logger.err("(set_simnode_state) Server name not set")

    def set_queue_item_state(self, queue_id, state, state_id, server_name, with_save=True, add_current_time=False,
                             set_time=""):
        self.logger.deepdb(("try to set_state: ", state, state_id, server_name, add_current_time, set_time))
        self.batch.que.clear_all_queue_items()  # TODO  check is in framework_mode  ? !!!!
        self.batch.que.load_queue()
        ret = self.batch.que.update_current_from_id(queue_id)
        if ret is not False:
            ret = self.batch.que.update_state_and_node_name(queue_id, state, state_id, server_name=server_name,
                                                            server_id=1, set_time=set_time,
                                                            add_current_time=add_current_time)
            state_length_10 = self.batch.comfun.str_with_spaces(state, length=10)
            if ret:
                qin = self.batch.que.current_queue.queue_item_name
                self.add_to_log("set state:{}   id:{}    qin:{}   by server:{}".format(state_length_10,
                                                                                       self.batch.que.current_queue_id,
                                                                                       qin, self.server_name))
            else:
                self.add_to_log("[ERR] state NOT set:{}    id:{}  by server:{}".format(state_length_10,
                                                                                       self.batch.que.current_queue_id,
                                                                                       self.server_name))
                return False
        else:
            self.logger.err(("set_state  update_current_from_id  failed ", queue_id, ret))

        if with_save is True:
            ret = self.batch.que.save_queue()
            if ret:
                return True
            else:
                return False
        else:
            return True

    def set_queue_item_working(self, queue_id, server_name, with_save=True):  # setStatus
        return self.set_queue_item_state(queue_id, "WORKING", 4, server_name, with_save=with_save,
                                         add_current_time=True)

    def set_queue_item_done(self, queue_id, server_name="", with_save=True, set_time=None):  # setStatus
        return self.set_queue_item_state(queue_id, "DONE", 11, server_name, with_save=with_save, set_time=set_time)

    def set_queue_item_error(self, queue_id, server_name, with_save=True):  # setStatus
        return self.set_queue_item_state(queue_id, "ERR", 9, server_name, with_save=with_save, add_current_time=True)

    def generate_script_from_queue_item(self, py_file, job_script, job_description, job_id):
        script_out = "'''   created by: " + str(self.server_name) + "   [" + self.comfun.get_current_time() + "]   '''\n"

        append_dir = os.path.dirname(os.path.dirname(os.path.dirname(self.server_dir)))
        append_dir = append_dir.replace("\\", "/")  # OS MARKER

        script_out += "\nimport sys\nsys.path.append(\"" + append_dir + "\")"
        script_out += "\nimport simbatch.core.core as simbatch_core\nimport simbatch.server.executor as executor"
        script_out += '\n\nsimbatch = simbatch_core.SimBatch("executor")'

        script_out += "\nsibe = executor.SimBatchExecutor(simbatch, 2, " + str(job_id) + ")"  # TODO 1:id
        script_out += "\ninteractions = sibe.batch.dfn.current_interactions"

        script_out += "\nsibe.add_to_log_with_new_line( \"START:" + job_description + "\")\n"  # TODO Soft+format+PEP

        script_lines = job_script.split(";")
        for li in script_lines:
            li_slash = li.replace('\\', '\\\\').lstrip()
            script_out += li_slash + "\n"

        script_out += "\nsibe.finalize_queue_job()\n"

        ret = self.batch.comfun.save_to_file(py_file, script_out)
        if ret:
            return script_out
        else:
            self.comfun.logger.err("script_for_external_software NOT saved !")
            return None

    def is_something_to_do(self, force_software=0):
        ret = self.batch.que.get_first_with_state_id(self.batch.sts.INDEX_STATE_WAITING, soft=force_software)
        if ret[0] >= 0:
            queue_item = self.batch.que.queue_data[ret[0]]
            script = queue_item.evolution_script
            soft_id = queue_item.soft_id
            info = " id:{}  evo:{}  descr:{}".format(ret[1], queue_item.evolution, queue_item.description)
            self.logger.db(("there is_something_to_do: ", ret[0], ret[1], force_software))
            return 1, ret[0], ret[1], script, soft_id, info
        else:
            return 0, None, None, None, None, None  # bool, index, id, script, soft_id  # TODO class

    def run_external_software(self, script):
        self.logger.db(("run_external_software", script))
        if self.batch.sts.current_os == 1:
            script = script[:-2] + "mel"
            comm = "maya -script " + script  # TODO universal info/text/message
            subprocess.Popen(comm, shell=True)
        if self.batch.sts.current_os == 2:
            script = script[:-2] + "mel"

            # comm = "maya.exe -command python(\"execfile('" + self.comfun.convert_to_unix_path(script) + "')\")"
            comm = "maya.exe -script " + self.comfun.convert_to_unix_path(script)
            self.logger.db(("run_external_software comm", comm))
            try:
                subprocess.Popen(comm, shell=True)
            except:
                self.logger.err(("Command not recognized/invalid: ", comm))
                self.logger.err(("run_external_software script:", script))
                pass

            self.jobs_computed += 1


    """   MAIN RUN  FOR LOCAL AND REMOTE  """
    """ marker SIM 010   running   """
    def run(self, argv=None):
        if self.batch.sts.loading_state < 4:
            self.logger.err(("settings not loaded properly: ", self.batch.sts.loading_state), nl=True)
            return False
            
        if self.framework_mode is False:
            if len(argv) > 1:
                argv = argv[1]
            else:
                del argv[:]
            
        if len(argv) > 0:
            if argv == "1" or argv == "single":
                mode = "single"
            elif argv == "all":
                mode = "all"
            elif self.comfun.can_get_int(argv):
                mode = "limit"
            elif argv == "up" or argv == "update_form_master":
                self.update_sources_from_master()
                return True
            elif argv == "upm" or argv == "update_to_master":
                self.update_sources_to_master()
                return True
            elif argv == "info" or argv =="i":
                self.print_server_info()
                return True
            elif argv == "test" or argv == "tst":
                self.do_all_tests()
                return True
            elif argv == "reset":
                self.reset_status()
                return True
            else:
                self.logger.err(("unknown arg  : ", argv), nl=True)
                self.logger.raw("Available options are: single, 1, all, update_form_master, up, update_to_master, " 
                                "upm, info, test, reset")
                return False
        else:
            mode = "all"

        self.logger.raw("\n\n")
        if mode == "single":
            self.jobs_limit = 1
            self.logger.inf("run single job")
        elif mode == "limit":
            limit = int(argv)
            if limit > 0:
                self.jobs_limit = limit
                self.logger.inf("run only {} queue items".format(limit))
            else:
                self.logger.inf("wrong run parameter: {}".format(argv))
        elif mode == "all":  # default option
            self.jobs_limit = 0
            self.logger.inf("run sim all")

        self.mode = mode

        self.run_loop()
            
    def run_loop(self):
        self.loops_counter += 1
        if self.break_loop is False and (self.jobs_limit == 0 or self.jobs_computed < self.jobs_limit):
            if self.jobs_limit == 0:
                '''  infinite loop  '''
                self.logger.db((self.comfun.get_current_time(), "loop:", self.loops_counter))
            else:
                '''  limited loop  '''
                self.logger.db((self.comfun.get_current_time(), "loop:", self.loops_counter,
                                "  limit:", self.jobs_limit, "   computed:", self.jobs_computed))

            """    MAIN EXECUTION LOOP    """

            if self.current_simnode_state != 0:   # server not in local mode
                self.current_simnode_state = self.batch.nod.get_node_state(self.server_dir + self.state_file_name)

                if self.current_simnode_state == self.batch.sts.INDEX_STATE_ERROR:
                    self.logger.err("file state not exist")
                    self.logger.log(("file state not exist", self.server_dir, self.state_file_name))

            '''  server INIT or WAITING  '''
            if self.current_simnode_state <= self.batch.sts.INDEX_STATE_WAITING:
                # if self.current_simnode_state == 1:
                #     self.set_simnode_state(self.batch.sts.INDEX_STATE_WAITING)
                self.batch.que.clear_all_queue_items()
                self.batch.que.load_queue()

                is_something_to_compute = self.is_something_to_do(force_software=self.force_software)

                if self.jobs_limit > 1:
                    loop_prefix = self.comfun.str_with_spaces(str(self.jobs_limit - self.jobs_computed), 3, as_prefix=True)
                else:
                    loop_prefix = None

                if is_something_to_compute[0] == 1:
                    self.report_total_jobs += 1
                    self.logger.inf((self.comfun.get_current_time(), "   there is something to compute:",
                                     is_something_to_compute[2]), force_prefix=loop_prefix)

                    job_id = is_something_to_compute[2]
                    job_script = is_something_to_compute[3]
                    job_description = is_something_to_compute[5]

                    ret = self.batch.que.update_current_from_id(job_id)
                    if ret is False:
                        self.logger.err(("current queue item not updated! id:", job_id))

                    ret = self.set_queue_item_working(job_id, str(self.server_name))
                    if ret is False:
                        self.logger.err(("current queue item set_working failed! id:", job_id))

                    if self.framework_mode is True:  # run local
                        """     RUN SINGLE JOB AS LOCAL     """

                        interactions = self.batch.dfn.current_interactions   # used in eval
                        if interactions is not None:
                            for job_line in job_script.split(";"):
                                clean_job_line = job_line.replace('\\', '\\\\').lstrip()
                                if len(clean_job_line) > 0:
                                    self.logger.db((" eval:", clean_job_line))
                                    try:
                                        ret = eval(clean_job_line)
                                        self.logger.deepdb((" q job line ret:", ret))
                                    except ValueError:
                                        self.logger.err(("eval q job", clean_job_line))
                                else:
                                    self.logger.deepdb(" empty q job line")

                            self.set_queue_item_done(job_id, str(self.server_name))
                            self.last_info = "DONE id: {}".format(job_id)
                            self.report_done_jobs += 1
                            self.jobs_computed += 1
                        else:
                            self.logger.err("interactions yyy  not loaded!")
                        #######
                        is_something_more_to_compute = self.is_something_to_do(force_software=self.force_software)

                        if is_something_more_to_compute[0] == 1:
                            self.run_loop()
                    else:
                        """     RUN SINGLE JOB AS SIMNODE     """

                        generated_script_file = self.server_dir + self.script_execute
                        
                        if self.current_simnode_state != 0:
                            self.set_simnode_state(self.batch.sts.INDEX_STATE_WORKING)
                        self.generate_script_from_queue_item(generated_script_file, job_script, job_description, job_id)

                        self.run_external_software(generated_script_file)
                        self.last_info = "run external software for job id:{}, {}".format(job_id, job_description)
                    """     END SINGLE JOB     """

                else:
                    '''   nothing more to compute!   '''
                    info = "{}   there is nothing to compute ".format(self.comfun.get_current_time())
                    self.logger.inf(info, force_prefix=loop_prefix)
                    if self.loops_counter == 1:
                        self.last_info = "there is nothing to compute"   # else last_info ->  last job id
                    
                    if self.jobs_limit > 0:  # nothing to compute on mode with LIMIT ON
                        """  BREAK ! """
                        if self.jobs_computed == self.jobs_limit:
                            self.logger.db("Breaking loop! The limit has been reached:{}".format(self.jobs_limit))
                            self.break_loop = True
                            self.last_info = "The limit has been reached."
                        else:
                            self.logger.inf("Nothing to do! The limit was not reached :{}/{}".format(
                                                  self.jobs_computed, self.jobs_limit))
                    else:
                        '''   job_limit == 0   ->   NO LIMIT  -> INFINITE LOOP   '''
                        pass

                    if self.framework_mode is True:  # run local
                        """  BREAK ! """
                        self.logger.db("Nothing to compute, exiting.  Limit:{}".format(self.jobs_limit))
                        self.break_loop = True
                        self.last_info = "Nothing to compute, exiting."
                
                self.logger.raw("\n")
            else:
                '''  server is busy:  WORKING   '''
                if self.current_simnode_state == self.batch.sts.INDEX_STATE_ERROR:
                    self.logger.err((self.comfun.get_current_time(), "   sim node ERROR ", str(self.server_name)))
                else:
                    busy_prefixes = " | ", " \\ ", "  |", " / ", "|  ", "\\  "
                    busy_prefix_index = self.loops_counter
                    while busy_prefix_index > 5:
                        busy_prefix_index -= 5
                    busy_prefix = busy_prefixes[busy_prefix_index]
                    state_str = self.batch.sts.states_visible_names[self.current_simnode_state]
                    self.logger.inf("{}       {}   is bussy now:{}".format(self.comfun.get_current_time(),
                                                                           str(self.server_name), state_str),
                                    force_prefix=busy_prefix)
                if self.mode == "single":
                    self.last_info = "Server is busy, WORKING now"    # TODO add job_id
                    
            """    MAIN EXECUTION  FIN    """

            external_breaker = self.server_dir + "break.txt"
            external_breaker_off = self.server_dir + "break__.txt"
            check_breaker = self.batch.comfun.file_exists(external_breaker, info=False)
            if check_breaker:
                self.logger.inf(("breaking main loop", self.last_info))
                self.logger.deepdb(("breaking file exists: ", external_breaker))
                if self.batch.comfun.file_exists(external_breaker_off, info=False):
                    os.remove(external_breaker_off)
                os.rename(external_breaker, external_breaker_off)
                time.sleep(0.5)
            else:
                threading.Timer(self.timer_delay_seconds, lambda: self.run_loop()).start()
        else:
            self.logger.inf(("End main loop. ", self.last_info))
