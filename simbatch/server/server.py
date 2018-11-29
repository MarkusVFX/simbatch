import time
import os
import subprocess
import threading


class SimBatchServer:
    timer_delay_seconds = 3  # delay for each loop execution
    loops_limit = 0  # 0 infinite loop
    loops_counter = 0  # total loop executions

    dbMode = 1  # 0 debug OFF    1 debug ON
    runExecutorState = 0  # 0 idle   1 something to do     2 runnning      9 err
    """
    0 skip checking state (run localy from framework)
    1 waiting (server idle)
    2 working (job run)
    3 hold    (server off)
    9 error   
    """
    current_simnode_state = None   #

    # 23 OFFLINE   8 off(HOLD)

    batch = None
    force_local = False
    forceSoftware = 0
    server_name = None  # TODO  custom name on init
    server_dir = ""
    state_file_name = "state.txt"
    log_file_name = "log.txt"
    script_execute = "script_execute.py"
    forces_software = 0
    last_info = ""
    report_total_jobs = 0
    report_done_jobs = 0

    def __init__(self, batch, force_software=0, loops_limit=0, force_local=False):
        self.force_software = force_software
        self.loops_limit = loops_limit
        if force_local:
            self.force_local = True
        self.batch = batch
        self.comfun = batch.comfun
        if self.force_local is False:
            self.batch.que.load_queue()            
            if self.batch.que.total_queue_items == 0:
                self.batch.logger.inf("queue data is empty, nothing loaded")
                self.batch.que.print_info()

        ''' elif self.force_local is True: queue is already loaded ! (no need to load) '''

        self.server_dir = os.path.dirname(os.path.realpath(__file__)) + self.batch.sts.dir_separator
        self.test_server_dir()
        
        simnode_state_file = self.server_dir + self.state_file_name

        if force_local:
            self.current_simnode_state = 0
        else:
            ret = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
            if ret[1] is not None:  # state file exists
                self.current_simnode_state = ret[0]
                self.server_name = ret[1]

                """  check existence in database  """
                state_file = self.batch.nod.get_state_file(server_name=ret[1])
                if state_file is False:
                    """  try to add simnode state file to database  """
                    pass
                # if state_file != simnode_state_file:
                    # TODO WIP
                    # self.batch.nod.create_node_state_file(simnode_state_file)
            else:
                self.batch.logger.err(("state file not exist or corrupted :", simnode_state_file))

        # if self.current_simnode_state == -1:
        #     simnode_state_data = "{};{};{}".format(2, self.server_name, self.comfun.get_current_time())
        #     self.batch.comfun.save_to_file(simnode_state_file, simnode_state_data)
        #     self.set_simnode_state(2)
        
        if self.force_local is True:
            print_server_name = batch.sts.runtime_env + " (local)"
        else:
            simnode_name = self.batch.nod.get_server_name_from_file(simnode_state_file)
            print_server_name = "{} ({})".format(batch.sts.runtime_env, simnode_name)
        self.batch.logger.inf(("init server :", print_server_name, self.server_dir))
        
    def print_server_info(self):
        self.batch.logger.raw("\n\n\n")
        
        simnode_state_file = self.server_dir + self.state_file_name
        self.batch.logger.inf("Local server state file: {}".format(simnode_state_file), force_prefix=" > ")
            
        if self.comfun.file_exists(simnode_state_file):
            ret = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
            if ret[0] >= 0:
                info = "Found server name: {} ".format(ret[1])
                self.batch.logger.inf(info, force_prefix=" ! ", nl=True)
                info = "Server local state: {}  {} ".format( ret[0], self.batch.sts.states_visible_names[ret[0]])
                self.batch.logger.inf(info, force_prefix=" ! ", nl=True)
            else:
                self.batch.logger.err("Server state file not consistent or empty!")
        else:
            self.batch.logger.wrn("Server state file not exit!")
            
         
           

    def do_all_tests(self):  # test server pure pyton (no unit tests)
        self.batch.logger.raw("\n\n\n")
        '''  simbatch load wtih settings  '''
        if self.batch.sts.loading_state >= 4:
            self.batch.logger.inf("Settings loaded", force_prefix=" > ")
        else:
            self.batch.logger.err("Settings NOT loaded")
        
        '''  data acces  '''
        if self.batch.sts.store_data_mode == 1:
            ret = self.batch.load_data()
            if ret[0]:
                self.batch.logger.inf("Simbatch data loaded with no errors or warnings ", force_prefix=" > ")
            elif ret[0] > 0:  
                self.batch.logger.wrn("Simbatch data loaded with {} errors".format(ret[0]))
            else:
                self.batch.logger.err("Critical error during dataloading! ({})".format(ret))
        else:
            pass
            # SQL with PRO version
            
        '''  local node status file  '''
        if len(self.server_dir) > 0:
            ret_R = os.access(self.server_dir, os.R_OK)  # TODO test write acces ,   move to common
            if ret_R:
                self.batch.logger.inf("Read from server directory test", force_prefix="OK ")
                ret_W = os.access(self.server_dir, os.W_OK)  # TODO test write acces ,   move to common
                if ret_W:
                    self.batch.logger.inf("Save to server directory test", force_prefix="OK ")
                else:
                    self.batch.logger.err("could NOT save to server directory  {} ".format(self.server_dir))
            
            if len(self.state_file_name) > 0:
                simnode_state_file = self.server_dir + self.state_file_name
                self.batch.logger.inf("Local server state file: {}".format(simnode_state_file), force_prefix=" > ")
                    
                if self.comfun.file_exists(simnode_state_file):
                    ret = self.batch.nod.get_node_info_from_state_file(simnode_state_file)
                    if ret[0] >= 0:
                        info = "Found server name: {}    server state: {}  {} ".format(ret[1], ret[0], self.batch.sts.states_visible_names[ret[0]])
                        self.batch.logger.inf(info, force_prefix=" ! ")
                        # self.batch.logger.inf("Found server name: {}    server state: {}  ".format(ret[1], ret[0]), force_prefix=" > ")
                    else:
                        self.batch.logger.err("Data not consistent in file: {} ({}) ".format(simnode_state_file, ret))
                else:
                    self.batch.logger.err("Local state file not exist!  ({})".format(simnode_state_file))
            else:
                self.batch.logger.err("Variable  self.state_file_name  is undefined!")
        else:
            self.batch.logger.err("Server dir not defined! Variable  self.server_dir  is not defined!")
        '''  master sourcefor update  '''
        master_source_path = self.get_existing_source_path()
        if master_source_path is not None:
            self.batch.logger.inf("Master source path exist: {}".format(master_source_path), force_prefix=" > ")
            ret_R = os.access(master_source_path, os.R_OK)  # TODO test write acces ,   move to common
            if ret_R:
                self.batch.logger.inf("Read from master source test", force_prefix="OK ")
                ret_W = os.access(master_source_path, os.W_OK)  # TODO test write acces ,   move to common
                if ret_W:
                    self.batch.logger.inf("Save to master source test", force_prefix="OK ")
                else:
                    self.batch.logger.wrn("could NOT save to master source path  {} ".format(master_source_path))
            else:
                self.batch.logger.err("could NOT read from master source path  {} ".format(master_source_path))
        else:
            self.batch.logger.err("Master source path NOT exist")
       
            
        '''  queue status  '''
        ret = self.is_something_to_do()
        if ret[0] == 1:
            self.batch.logger.inf(("Something to do: ", ret[1]), force_prefix=" > ")
        else:
            self.batch.logger.err("Nothing to do", force_prefix=" > ")
            
            
        
    def test_server_dir(self):
        # TODO test write acces   create data dir
        pass
        
    def get_existing_source_path(self):
        source_path = self.batch.sts.installation_directory_abs + "/"
        if self.batch.comfun.path_exists(source_path):
            return source_path
        else:
            None

    def update_sources_from_master(self):
        self.update_sources()
        
    def update_sources_to_master(self):
        self.update_sources(reverse_to_master=True)
        
    def update_sources(self, reverse_to_master=False):
        if self.batch.sts.installation_directory_abs is not None:
            # TODO self.batch.sts.dir_separator  vs universal separator
            source_path = self.get_existing_source_path()   #self.batch.sts.installation_directory_abs + "/"
            if source_path is not None:
                dst_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
            
                if reverse_to_master:
                    source_path, dst_path = dst_path, source_path
            
                if self.batch.sts.current_os == 2:
                    source_path = self.batch.comfun.convert_to_win_path(source_path)
                    dst_path = self.batch.comfun.convert_to_win_path(dst_path)
            
                
                
                ret_R = os.access(source_path, os.R_OK)  # TODO test write acces ,   move to common
                ret_W = os.access(dst_path, os.W_OK)  # TODO test write acces ,   move to common
                if ret_R and ret_W:
                    #
                    self.batch.logger.inf(("update sources from  {}  ".format(source_path)), nl=True)
                    self.batch.sio.copy_file(source_path, dst_path, "server.py", sub_dir="server")
                    self.batch.sio.copy_tree(str(source_path), str(dst_path), sub_dir="core")
                    #
                else:
                    if ret_R is False:
                        self.batch.logger.err("could NOT read from source path  {} ".format(src_path))
                    if ret_W is False:
                        self.batch.logger.err("could NOT save to dest path  {} ".format(dst_path))
            else:
                self.batch.logger.err("master source path  {}  not exist".format(source_path))
        else:
            self.batch.logger.err("(update_sources_from_master) installation_directory_abs is not defined")
        
    def add_to_log(self, info, log_file=None):
        date = self.comfun.get_current_time()
        if log_file is None:
            log_file = self.server_dir + self.log_file_name
        f = open(log_file, 'a')
        f.write(date + " " + info + '; \n')
        f.close()
        self.batch.logger.log(info)

    def reset_report(self):
        self.report_total_jobs = 0
        self.report_done_jobs = 0

    def generate_report(self):   # TODO
        return self.report_total_jobs, self.report_done_jobs
        
    # def set_database_node_state(self, queue_id, state, state_id, server_name, state_file):
    #     return self.batch.nod.set_node_state(state_file, server_name, state_id)
            
    def set_simnode_state(self, stste):     # TODO clean up this !!!!
        print "\n WIP  set_simnode_state  : ", stste, self.batch.sts.dir_separator

        # if self.force_local==False:
        # file_and_path = self.server_dir + self.state_file_name
        # self.batch.nod.set_node_state(file_and_path, self.server_name, state)

    def set_queue_item_state(self, queue_id, state, state_id, server_name, with_save=True, add_current_time=False,
                             set_time=""):
        self.batch.logger.deepdb(("try to set_state: ", state, state_id, server_name, add_current_time, set_time))
        self.batch.que.clear_all_queue_items()  # TODO  check is mode LOCAL ? !!!!
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
            self.batch.logger.err(("set_state  update_current_from_id  failed ", queue_id, ret))

        if with_save is True:
            ret = self.batch.que.save_queue()
            if ret:
                return True
            else:
                return False
        else:
            return True

    """
    def set_state(self, queue_id, state, state_id, server_name, with_save=True, add_current_time=False, set_time=""):
        self.set_queue_state(queue_id, state, state_id, server_name, with_save=True, add_current_time=False, set_time="")
        if self.force_local is False:
            state_file = self.batch.nod.get_state_file(server_name=server_name)
            if state_file is False:
                self.batch.logger.err(("state file not found by server name: ", server_name))
            else:
                # set_node_database_state(queue_id, state, state_id, server_name, state_file)
                self.set_simnode_state(10000)  # WIP TODO
    """

    def set_queue_item_working(self, queue_id, server_name, with_save=True):  # setStatus
        return self.set_queue_item_state(queue_id, "WORKING", 4, server_name, with_save=with_save, add_current_time=True)

    def set_queue_item_done(self, queue_id, server_name="", with_save=True, set_time=None):  # setStatus
        return self.set_queue_item_state(queue_id, "DONE", 11, server_name, with_save=with_save, set_time=set_time)

    def set_queue_item_error(self, queue_id, server_name, with_save=True):  # setStatus
        return self.set_queue_item_state(queue_id, "ERR", 9, server_name, with_save=with_save, add_current_time=True)

    def generate_script_for_external_software(self, py_file, job_script, job_description, job_id):
        script_out = "'''   created by: " + self.server_name + "   [" + self.comfun.get_current_time() + "]   '''\n\n"
        script_out += "\n# sys append script dir    " + self.server_dir  # TODO sys append script dir
        script_out += "\nfrom SimBatch_executor import * \nSiBe = SimBatchExecutor(1, " + str(job_id) + ")"  # TODO 1:id
        script_out += "\nSiBe.addToLogWithNewLine( \"Soft START:" + job_description + "\")\n"  # TODO Soft+format+PEP

        script_lines = job_script.split("|")
        for li in script_lines:
            li_slash = li.replace('\\', '\\\\')
            script_out += li_slash + "\n"

        script_out += "\nSiBe.finalizeQueueJob()\n"

        self.batch.comfun.save_to_file(py_file, script_out)
        return script_out

    def is_something_to_do(self, force_software=0):
        ret = self.batch.que.get_first_with_state_id(2, soft=force_software)  # TODO cnst state from settings
        if ret[0] >= 0:
            queue_item = self.batch.que.queue_data[ret[0]]
            script = queue_item.evolution_script
            soft_id = queue_item.soft_id
            info = " id:{}  evo:{}  descr:{}".format(ret[1], queue_item.evolution, queue_item.description)
            self.batch.logger.db(("there is_something_to_do: ", ret[0], ret[1], force_software))
            return 1, ret[0], ret[1], script, soft_id, info
        else:
            return 0, None, None, None, None, None  # bool, index, id, script, soft_id  # TODO class

    def run_external_software(self, script):
        self.batch.logger.db(("run_external_software", script))
        if self.batch.sts.current_os == 1:
            comm = "kate " + script  # TODO universal info/text/message
            subprocess.Popen(comm, shell=True)
        if self.batch.sts.current_os == 2:
            comm = "maya.exe -script " + script  # mayabatch   self.mayaExeFilePath +
            try:
                subprocess.Popen(comm, shell=True)
            except:
                self.batch.logger.err(("Command not recognized/inalid: ", comm))
                self.batch.logger.err(("run_external_software script:", script))
                pass

    """   MAIN RUN  FOR LOCAL AND REMOTE  """
    """ marker SIM 010   running   """
    def run(self, argv=None):
        if self.batch.sts.loading_state < 4:
            print " [ERR] settings not loaded properly: ", self.batch.sts.loading_state
            return False
            
        if self.force_local is False:
            if len(argv) > 1:
                argv = argv[1]
            else:
                del argv[:]
            
        if len(argv) > 0:
            if argv == "1" or argv == "single":
                mode = "single"
            else:
                if argv == "all":
                    mode = "all"
                elif argv == "up" or argv == "update_form_master":
                    self.update_sources_from_master()
                    return True
                elif argv == "upm" or argv == "update_to_master":
                    self.update_sources_to_master()
                    return True
                elif argv == "info":
                    self.print_server_info()
                    return True
                elif argv == "test":
                    self.do_all_tests()
                    return True
                else:
                    self.batch.logger.inf(("unknown arg  : ", argv))
                    return False
        else:
            mode = "all"
                
        if mode == "single":
            self.loops_limit = 1
            self.batch.logger.raw("\n")
            self.batch.logger.inf("run single job")
                
        if mode == "all":
            self.loops_limit = 0
            self.batch.logger.raw("\n\n") 
            self.batch.logger.inf("run sim all")
        
        self.run_loop()
            
    def run_loop(self):
        self.loops_counter += 1
        if self.loops_counter <= self.loops_limit or self.loops_limit < 1:
            if self.loops_limit > 0:
                self.batch.logger.db((self.comfun.get_current_time(), "loop:", self.loops_counter,
                                      "  limit:", self.loops_limit))
            else:
                self.batch.logger.db((self.comfun.get_current_time(), "loop:", self.loops_counter))

            """    MAIN EXECUTION LOOP    """

            if self.current_simnode_state != 0:   # server not in local mode
                self.current_simnode_state = self.batch.nod.get_node_state(self.server_dir + self.state_file_name)

                if self.current_simnode_state == 9:
                    self.batch.logger.err("file state not exist")
                    self.batch.logger.log(("file state not exist", self.server_dir, self.state_file_name))

            if self.current_simnode_state <= 2:   # server waiting or in local mode   # TODO cnst 2WAIT 1INIT  0LOCAL
                if self.current_simnode_state != 0:
                    self.set_simnode_state(2)
                self.batch.que.clear_all_queue_items()
                self.batch.que.load_queue()

                is_something_to_compute = self.is_something_to_do(force_software=self.forces_software)

                if is_something_to_compute[0] == 1:
                    self.report_total_jobs += 1
                    self.batch.logger.inf((self.comfun.get_current_time(), "   there is_something_to_compute",
                                           is_something_to_compute[2]))
                    execute_queue_id = is_something_to_compute[2]  # TODO   ret check and  del

                    ret = self.batch.que.update_current_from_id(execute_queue_id)
                    if ret is False:
                        self.batch.logger.err(("current queue item not updated! id:", execute_queue_id))

                    ret = self.set_queue_item_working(execute_queue_id, self.server_name)
                    if ret is False:
                        self.batch.logger.err(("current queue item set_working failed! id:", execute_queue_id))

                    """     RUN SINGLE JOB AS LOCAL     """
                    if self.force_local is True:  # run local
                        print "\n\n            [FOO] run_script(generate_script_file)"
                        print "            [FOO] run_script(generate_script_file)"  # TODO
                        print "            [FOO] run_script(generate_script_file)"
                        self.set_queue_item_done(execute_queue_id, self.server_name)
                        self.last_info = "DONE id: {}".format(execute_queue_id)
                        self.report_done_jobs += 1
                        #######
                        is_something_more_to_compute = self.is_something_to_do(force_software=self.forces_software)

                        if is_something_more_to_compute[0] == 1:
                            self.run_loop()
                    else:
                        """     RUN SINGLE JOB AS SIMNODE     """
                        job_id = is_something_to_compute[2]
                        job_script = is_something_to_compute[3]
                        job_description = is_something_to_compute[5]
                        generated_script_file = self.server_dir + self.script_execute
                        
                        if self.current_simnode_state != 0:
                            self.set_simnode_state(1)
                        self.generate_script_for_external_software(generated_script_file, job_script, job_description,
                                                                   job_id)

                        self.run_external_software(generated_script_file)
                    """     END SINGLE JOB     """

                else:  # nothing more to compute!
                    self.batch.logger.inf((self.comfun.get_current_time(), "   there is nothing to compute"))
                    if self.loops_counter == 1:
                        self.last_info = "there is nothing to compute"   # else last_info ->  last job id

                    if self.force_local is True:  # run local
                        """  BREAK ! """
                        self.loops_limit = self.loops_counter
                        self.loops_counter += 1
            else:
                if self.current_simnode_state == 9:
                    self.batch.logger.err((self.comfun.get_current_time(), "   sim node ERROR ", self.server_name))
                else:
                    state_str = self.batch.sts.states_visible_names[self.current_simnode_state]
                    self.batch.logger.inf((self.comfun.get_current_time(), "   sim node", self.server_name, state_str))
            """    MAIN EXECUTION  FIN    """

            external_breaker = self.server_dir + "break.txt"
            external_breaker_off = self.server_dir + "break__.txt"
            check_breaker = self.batch.comfun.file_exists(external_breaker, info=False)
            if check_breaker:
                self.batch.logger.inf(("breaking main loop", self.last_info))
                self.batch.logger.deep(("breaking file exists: ", external_breaker))
                if self.batch.comfun.file_exists(external_breaker_off):
                    os.remove(external_breaker_off)
                os.rename(external_breaker, external_breaker_off)
            else:
                threading.Timer(self.timer_delay_seconds, lambda: self.run_loop()).start()
        else:
            self.batch.logger.inf(("end main loop", self.last_info))
