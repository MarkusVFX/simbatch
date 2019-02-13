import datetime
import time

try:
    import hou
except ImportError:
    pass

try:
    import maya.cmds as cmds
    import maya.mel as ml
except ImportError:
    pass


class SimBatchExecutor():
    server_dir = "server"
    log_file_name = "server_log.txt"
    job_start_time = None
    hack_sim_node_name = "SimNode_01"

    def __init__(self, batch, soft_id, queue_id, force_local=False):
        self.softID = soft_id
        self.force_local = force_local
        self.executor_queue_id = queue_id

        self.job_start_time = time.time()

        self.batch = batch
        self.batch.load_data()
        self.batch.dfn.update_current_definition_by_name("Maya")
        self.add_to_log_with_new_line("")
        time.sleep(0.5)
        self.add_to_log_with_new_line("")

    def add_to_log_with_new_line(self, logStr):
        self.add_to_log(logStr, with_new_line=True)

    def add_to_log(self, log_txt, with_new_line=False):
        log_file = self.server_dir + self.log_file_name

        if with_new_line:
            log_txt += "\n"

        text_file = open(log_file, "a")
        text_file.write(self.get_current_time() + "   " + log_txt)
        text_file.close()

    @staticmethod
    def get_current_time(filename_mode=False):
        if filename_mode:
            return datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        else:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def set_queue_state_and_add_to_log(self, state_name, state_id, server_name, with_save=True, add_current_time=False,
                                       set_time=""):

        self.batch.que.clear_all_queue_items()
        self.batch.que.load_queue()
        self.batch.que.update_state_and_node_name(self.executor_queue_id, state_name, state_id, server_name=server_name,
                                                  server_id=1, set_time=set_time, add_current_time=add_current_time)

        if self.batch.que.get_index_by_id(self.executor_queue_id) > 0:
            qin = self.batch.que.queue_data[self.batch.que.get_index_by_id(self.executor_queue_id)].queue_item_name
            self.add_to_log_with_new_line(" set " + state_name + " [" + str(self.executor_queue_id) + "]   " + qin +
                                          "   by server: " + server_name)
        else:
            self.add_to_log_with_new_line(" set " + state_name + " [" + str(self.executor_queue_id) + "]   by server: "
                                          + server_name)
        if with_save is True:
            self.batch.que.save_queue()

    def set_queue_job_working(self, server_name, with_save=True):
        self.set_queue_state_and_add_to_log("WORKING", 4, server_name, with_save=with_save, add_current_time=True)

    def set_queue_job_done(self, server_name, with_save=True, set_time=""):
        self.set_queue_state_and_add_to_log("DONE", 11, server_name, with_save=with_save, set_time=set_time)

    def set_queue_job_error(self, server_name, with_save=True):
        self.set_queue_state_and_add_to_log("ERR", 9, server_name, with_save=with_save, add_current_time=True)

    def finalize_queue_job(self):
        time.sleep(1)
        job_time = str(0.1 * int((time.time() - self.job_start_time) * 10))
        print " [INF] job time   ", job_time

        self.set_queue_job_done(self.hack_sim_node_name, set_time=job_time)

        idx = self.batch.nod.get_node_index_by_name(self.hack_sim_node_name)
        # print " idx  ", idx, self.hack_sim_node_name
        self.batch.nod.set_node_state_in_database(idx, 2)

        self.batch.nod.update_current_from_index(idx)
        cur_nod = self.batch.nod.current_node
        state_id = self.batch.sts.INDEX_STATE_WAITING
        self.batch.nod.create_node_state_file(cur_nod.state_file, cur_nod.node_name, state_id, update_mode=True)

        if self.softID == 1:
            self.add_to_log_with_new_line("HOU Exiting")
            print " [INF] HOU Exit  "
            self.exit_houdini()
        else:  # maya !!!
            self.add_to_log_with_new_line("Maya Exiting")
            print " [INF] Maya Exit  "
            self.exit_maya()

    def exit_houdini(self):
        import hou
        hou.exit(suppress_save_prompt=True)

    def exit_maya(self):
        import maya.cmds as cmds
        cmds.quit(force=True)
        self.add_to_log_with_new_line("Maya Exited")

