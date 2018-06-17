import time
import os
import subprocess
import threading


class SimBatchServer:
    timerDelaySeconds = 3  # delay for each loop execution
    loopsLimit = 0  # 0 infinite loop
    loops_counter = 0  # total loop executions

    dbMode = 1  # 0 debug OFF    1 debug ON
    runExecutorState = 0  # 0 idle   1 something to do     2 runnning      9 err
    current_simnode_state = None
    # 23 OFFLINE   8 off(HOLD)  2(WAITING)  20 server executor(ACTIVE)  4 proces run  (WORKING)  11 process done  9 err

    batch = None
    forceSoftware = 0
    server_name = "SimNode_01"  # TODO  custom name on init
    server_dir = ""
    state_file_name = "state.txt"
    log_file_name = "log.txt"
    script_execute = "script_execute.py"
    forces_software = 0
    last_info = ""
    is_batching_mode_framework = False

    def __init__(self, batch, force_software=0, loops_limit=0, force_local=False):
        self.force_software = force_software
        self.loopsLimit = loops_limit
        if force_local:
            self.is_batching_mode_framework = True
        self.batch = batch
        self.batch.que.load_queue()
        if self.batch.que.total_queue_items == 0:
            self.batch.logger.err("queue data is empty, nothing loaded")
            self.batch.que.print_header()

        self.server_dir = os.path.dirname(os.path.realpath(__file__)) + self.batch.sts.dir_separator
        self.test_server_dir()

        self.current_simnode_state = self.batch.nod.get_node_state(self.server_dir + self.state_file_name)
        if self.current_simnode_state == -1:
            simnode_state_file = self.server_dir + self.state_file_name
            simnode_state_data = "{};{};{}".format(2, self.server_name, self.get_date())
            self.batch.comfun.save_to_file(simnode_state_file, simnode_state_data)
            self.set_simnode_state(2)
        self.batch.logger.inf(("init server", self.server_dir))

    def test_server_dir(self):
        # TODO tesdt write acces   create data dir
        pass

    def get_date(self):  # TODO move to common
        return time.strftime("%Y-%m-%d_%H:%M:%S")

    def set_simnode_state(self, state):
        file = self.server_dir + self.state_file_name
        self.batch.nod.set_node_state(file, self.server_name, state)

    def add_to_log(self, info, log_file=None):  # TODO move to common
        date = self.get_date()
        if log_file == None:
            log_file = self.server_dir + self.log_file_name
        f = open(log_file, 'a')
        f.write(date + info + '; \n')
        f.close()
        self.batch.logger.log(info)

    def set_state(self, queue_id, state, state_id, server_name, with_save=True, add_current_time=False, set_time=""):
        self.batch.logger.db(("set_state: ", state, state_id, server_name))
        self.batch.que.clear_all_queue_items()  # TODO  check REFERS IF LOCAL !!!!
        self.batch.que.load_queue()
        self.batch.que.update_current_from_id(queue_id)
        self.batch.que.update_state_and_node(queue_id, state, state_id, server_name=server_name, server_id=1,
                                             set_time=set_time, add_current_time=add_current_time)

        if self.batch.que.current_queue_index is not None:
            qin = self.batch.que.current_queue.queue_item_name
            self.add_to_log(" state:{}   id:{}    qin:{}   by server:{}".format(state, self.batch.que.current_queue_id,
                                                                                qin, self.server_name))
        else:
            self.add_to_log(" state:{}   id:{}   by server:{}".format(state, self.batch.que.current_queue_id,
                                                                      self.server_name))

        if with_save == True:
            ret = self.batch.que.save_queue()
            # TODO ret (OK, WRN ERR)

    def set_working(self, queue_id, server_name, with_save=True):  # setStatus
        self.set_state(queue_id, "WORKING", 4, server_name, with_save=with_save, add_current_time=True)

    def set_done(self, queue_id, server_name="", with_save=True, set_time=""):  # setStatus
        self.set_state(queue_id, "DONE", 11, server_name, with_save=with_save, set_time=set_time)

    def set_error(self, queue_id, server_name, with_save=True):  # setStatus
        self.set_state(queue_id, "ERR", 9, server_name, with_save=with_save, add_current_time=True)

    def generate_script_for_external_software(self, pyFile, jobScript, jobDescription, jobID, local=False):
        scritp_out = "'''   create time: " + self.get_date() + "   '''\n'''   create node: " + self.server_name + "   '''\n\n"
        scritp_out += "\n# sys append script dir    " + self.server_dir  # TODO sys append script dir
        scritp_out += "\nfrom SimBatch_executor import * \nSiBe = SimBatchExecutor(1, " + str(
            jobID) + " ) "  # TODO 1: id
        scritp_out += "\nSiBe.addToLogWithNewLine( \"Soft START:" + jobDescription + "\" )  \n"  # TODO Soft + format + PEP

        script_lines = jobScript.split("|")
        for li in script_lines:
            li_slash = li.replace('\\', '\\\\')
            scritp_out += li_slash + "\n"

        scritp_out += "\nSiBe.finalizeQueueJob()\n"

        self.batch.comfun.save_to_file(pyFile, scritp_out)
        return scritp_out

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

    def run(self):
        self.loops_counter += 1
        if self.loops_counter <= self.loopsLimit or self.loopsLimit < 1:
            if self.loopsLimit > 0:
                self.batch.logger.db((self.get_date(), "loop:", self.loops_counter))
            else:
                self.batch.logger.db(self.get_date())

            ############   MAIN EXECUTION LOOP    ##########

            self.current_simnode_state = self.batch.nod.get_node_state(self.server_dir + self.state_file_name)

            if self.current_simnode_state == 9:
                self.batch.logger.err("file state not exist")
                self.batch.logger.log(("file state not exist", self.server_dir, self.state_file_name))

            if self.current_simnode_state == 8 or self.current_simnode_state == 2:  # 2  server run (WAITING or HOLD)
                if self.current_simnode_state == 8:  # 8 off(HOLD)
                    self.current_simnode_state = 2
                    self.set_simnode_state(2)
                self.batch.que.clear_all_queue_items()
                self.batch.que.load_queue()

                is_something_to_compute = self.is_something_to_do(force_software=self.forces_software)

                if is_something_to_compute[0] == 1:
                    self.batch.logger.inf(
                        (self.get_date(), "   there is_something_to_compute", is_something_to_compute))
                    execute_queue_index = is_something_to_compute[1]  # TODO   ret check and  del     job_to_compute
                    execute_queue_id = is_something_to_compute[2]  # TODO   ret check and  del

                    ret = self.batch.que.update_current_from_id(execute_queue_id)
                    if ret is False:
                        self.batch.logger.db(("queue item state not updated, id:", execute_queue_id))

                    # set queue item state
                    self.set_working(execute_queue_id)

                    job_id = is_something_to_compute[2]
                    job_script = is_something_to_compute[3]
                    job_description = is_something_to_compute[5]

                    generate_script_file = self.server_dir + self.script_execute

                    ##############  RUN SINGLE JOB  ####################
                    if self.is_batching_mode_framework is True:  # run local
                        print "run_script(generate_script_file)"
                        print "run_script(generate_script_file)"
                        print "run_script(generate_script_file)"  # TODO
                        print "run_script(generate_script_file)"  # TODO
                        print "run_script(generate_script_file)"  # TODO
                        print "run_script(generate_script_file)"
                        print "run_script(generate_script_file)"
                        self.set_done(execute_queue_id, self.server_name)
                        self.last_info = "DONE: {}".format(execute_queue_id)
                        #######
                        is_something_more_to_compute = self.is_something_to_do(force_software=self.forces_software)
                        if is_something_more_to_compute[0] == 1:
                            self.run()
                    else:  # use simnode
                        # set node state
                        self.set_simnode_state(20)
                        self.generate_script_for_external_software(generate_script_file, job_script, job_description,
                                                                   job_id, local=True)

                        self.run_external_software(generate_script_file)
                        ##############  END SINGLE JOB  ####################



                else:
                    self.batch.logger.inf((self.get_date(), "   there is nothing to compute"))
                    self.last_info = "there is nothing to compute"
            else:
                if self.current_simnode_state == 9:
                    print "  [INF] sim node ERROR [err_code:23] !!! \n"
                    self.batch.logger.inf((self.get_date(), "   sim node ERROR ", self.server_name))
                else:
                    self.batch.logger.inf((self.get_date(), "   sim node", self.server_name, "looks bussy "))

            ############   MAIN EXECUTION  FIN  ##########

            check_breaker = self.batch.comfun.file_exists(self.server_dir + "break.txt", info=False)
            if check_breaker:
                print " [INF]  BREAK MAIN LOOP !"
                os.rename(self.server_dir + "break.txt", self.server_dir + "break___.txt")
                print "break loopopop", self.last_info
            else:
                threading.Timer(self.timerDelaySeconds, self.run).start()

        else:
            print "end loopopop", self.last_info

