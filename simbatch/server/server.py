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
    server_name = ""  # TODO  custom name on init
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
        if force_local is False:
            self.batch.que.load_queue()
        # else:
            # already loaded !
        if self.batch.que.total_queue_items == 0:
            self.batch.logger.err("queue data is empty, nothing loaded")
            self.batch.que.print_header()

        self.server_dir = os.path.dirname(os.path.realpath(__file__)) + self.batch.sts.dir_separator
        self.test_server_dir()

        if force_local:
            self.current_simnode_state = 0
        else:
            self.current_simnode_state = self.batch.nod.get_node_state(self.server_dir + self.state_file_name)

        if self.current_simnode_state == -1:
            simnode_state_file = self.server_dir + self.state_file_name
            simnode_state_data = "{};{};{}".format(2, self.server_name, self.comfun.get_current_time())
            self.batch.comfun.save_to_file(simnode_state_file, simnode_state_data)
            self.set_simnode_state(2)

        self.server_name = batch.sts.runtime_env + " (local)"
        print "srv"
        self.batch.logger.inf(("init server :", self.server_name, self.server_dir))

    def test_server_dir(self):
        # TODO tesdt write acces   create data dir
        pass

    def set_simnode_state(self, state):
        file_and_path = self.server_dir + self.state_file_name
        self.batch.nod.set_node_state(file_and_path, self.server_name, state)

    def add_to_log(self, info, log_file=None):  # TODO move to common
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

    def set_state(self, queue_id, state, state_id, server_name, with_save=True, add_current_time=False, set_time=""):
        self.batch.logger.db(("try to set_state: ", state, state_id, server_name, add_current_time, set_time))
        self.batch.que.clear_all_queue_items()  # TODO  check is mode LOCAL ? !!!!
        self.batch.que.load_queue()
        ret = self.batch.que.update_current_from_id(queue_id)
        if ret is not False:
            ret = self.batch.que.update_state_and_node(queue_id, state, state_id, server_name=server_name, server_id=1,
                                                       set_time=set_time, add_current_time=add_current_time)
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
            self.batch.logger.err(("set_state  update_current_from_id  failed " , queue_id, ret))

        if with_save is True:
            ret = self.batch.que.save_queue()
            if ret:
                return True
            else:
                return False
        else:
            return True

    def set_working(self, queue_id, server_name, with_save=True):  # setStatus
        return self.set_state(queue_id, "WORKING", 4, server_name, with_save=with_save, add_current_time=True)

    def set_done(self, queue_id, server_name="", with_save=True, set_time=None):  # setStatus
        return self.set_state(queue_id, "DONE", 11, server_name, with_save=with_save, set_time=set_time)

    def set_error(self, queue_id, server_name, with_save=True):  # setStatus
        return self.set_state(queue_id, "ERR", 9, server_name, with_save=with_save, add_current_time=True)

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
        try:
            self.batch.logger.db(("run_external_software", script))
            if self.batch.sts.current_os == 1:
                # comm ="mayapy "+script
                comm = "kate " + script
                subprocess.Popen(comm, shell=True)
            if self.batch.sts.current_os == 2:
                comm = "maya.exe -script " + script  # mayabatch   self.mayaExeFilePath +
                subprocess.Popen(comm, shell=True)
        except:
            self.batch.logger.err(("run_external_software", script))
            pass

    """   MAIN RUN  FOR LOCAL AND REMOTE  """
    def run(self, mode="all"):
        if mode == "single":
            self.loops_limit = 1
        if mode == "all":
            self.batch.logger.db("\n\n")

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

            if self.current_simnode_state <= 1:   # server waiting or in local mode
                if self.current_simnode_state != 0:
                    self.set_simnode_state(2)
                self.batch.que.clear_all_queue_items()
                self.batch.que.load_queue()

                is_something_to_compute = self.is_something_to_do(force_software=self.forces_software)

                if is_something_to_compute[0] == 1:
                    self.report_total_jobs += 1
                    self.batch.logger.inf((self.comfun.get_current_time(), "   there is_something_to_compute",
                                           is_something_to_compute))
                    execute_queue_id = is_something_to_compute[2]  # TODO   ret check and  del

                    ret = self.batch.que.update_current_from_id(execute_queue_id)
                    if ret is False:
                        self.batch.logger.err(("current queue item not updated! id:", execute_queue_id))

                    ret = self.set_working(execute_queue_id, self.server_name)
                    if ret is False:
                        self.batch.logger.err(("current queue item set_working failed! id:", execute_queue_id))

                    """     RUN SINGLE JOB     """
                    if self.force_local is True:  # run local
                        print "\n\nrun_script(generate_script_file)"
                        print "run_script(generate_script_file)"  # TODO
                        print "run_script(generate_script_file)"
                        self.set_done(execute_queue_id, self.server_name)
                        self.last_info = "DONE id: {}".format(execute_queue_id)
                        self.report_done_jobs += 1
                        #######
                        is_something_more_to_compute = self.is_something_to_do(force_software=self.forces_software)

                        if is_something_more_to_compute[0] == 1:
                            print ("\n pre run wew" + str(self.loops_counter) + "\n")
                            self.run(mode)
                            print ("\n post run wew" + str(self.loops_counter) + "\n")
                    else:
                        """ run as simnode """

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

                else:
                    self.batch.logger.inf((self.comfun.get_current_time(), "   there is nothing to compute"))
                    if self.loops_counter == 1:
                        self.last_info = "there is nothing to compute"

                    """ MODE ALL END """
                    if mode == "all":
                        self.loops_limit = self.loops_counter - 1
            else:
                if self.current_simnode_state == 9:
                    self.batch.logger.err((self.comfun.get_current_time(), "   sim node ERROR ", self.server_name))
                else:
                    self.batch.logger.inf((self.comfun.get_current_time(), "   sim node", self.server_name, "is busy"))
            """    MAIN EXECUTION  FIN    """

            external_breaker = self.server_dir + "break.txt"
            external_breaker_off = self.server_dir + "break__.txt"
            check_breaker = self.batch.comfun.file_exists(external_breaker, info=False)
            if check_breaker:
                self.batch.logger.inf(("breaking main loop", self.last_info))
                if self.batch.comfun.file_exists(external_breaker_off):
                    os.remove(external_breaker_off)
                os.rename(external_breaker, external_breaker_off)
            else:
                threading.Timer(self.timer_delay_seconds, lambda: self.run(mode)).start()
        else:
            self.batch.logger.inf(("end main loop", self.last_info))
