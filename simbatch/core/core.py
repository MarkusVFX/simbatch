import platform

from settings import Settings
from lib.common import CommonFunctions
from lib.logger import Logger
from lib.patterns import Patterns
from users import Users
from definitions import Definitions
from projects import Projects
from schemas import Schemas
from tasks import Tasks
from queue import Queue
from nodes import SimNodes
from io import StorageInOut


class SimBatch:
    s = None
    comfun = None
    logger = None
    os = None

    def __init__(self, runtime_env, ini_file="config.ini", os=None):
        self.logger = Logger(log_level=0, console_level=3)
        self.sts = Settings(self.logger, runtime_env, ini_file=ini_file)   # sts
        self.logger.set_console_level(self.sts.debug_level)
        self.logger.set_log_level(0)
        self.comfun = CommonFunctions(self.logger)

        if os is None:
            self.os = platform.system()
            if self.os == "Windows":
                self.os = "w"
            elif self.os == "Linux":
                self.os = "l"
            else:
                self.os = None

        # abbreviation for very often used variables, helping with identification the main modules
        self.usr = Users(self, mode=1)  # usr  """ users are fully implemented in Pro version """
        self.prj = Projects(self)       # prj
        self.sch = Schemas(self)        # sch
        self.tsk = Tasks(self)          # tsk
        self.que = Queue(self)          # que
        self.nod = SimNodes(self)       # nod
        self.dfn = Definitions(self)    # dfn
        self.sio = StorageInOut(self)   # sio
        self.pat = Patterns()           # pat
        #  abbreviation  END

        self.logger.inf("SimBatch started", nl=True, nl_after=True)

    def print_data(self):
        self.prj.print_all()

    def print_important_values(self):
        print "  \n\n  Current runtime_env: {}".format(self.sts.runtime_env)

        # projects
        print "\n PROJECTS: "
        self.prj.print_current()

        # schemas
        print "\n SCHEMAS: "
        self.sch.print_current()

        # tasks
        print "\n TASKS: "
        self.tsk.print_current()

        # queue
        print "\n QUEUE: "
        self.que.print_current()

        # nodes
        print "\n NODES: "
        self.nod.print_current()

        # nodes
        print "\n DEFINITIONS: "
        self.dfn.print_current()

        print "\n\n"

    def print_current_detailed_values(self, index):
        print "  \n\n"
        if self.sts.ui_edition_mode == 0:    # open source no wizard tab
            index += 1                       # index compensation

        if index == 0:
            print " WIZARD: "
        if index == 1:
            print " PROJECTS: "
            self.prj.print_all()
            self.prj.print_current()
        if index == 2:
            print " SCHEMAS: "
            self.sch.print_all()
            self.sch.print_current()
        if index == 3:
            print " TASKS: "
            self.tsk.print_all()
            self.tsk.print_current()
        if index == 4:
            print " QUEUE: "
            self.que.print_all()
            self.que.print_current()
        if index == 5:
            print " SIMNODES: "
            self.nod.print_all()
            self.nod.print_current()
        if index == 6:
            print " DEFINITIONS: "
            self.dfn.print_all()
            self.dfn.print_current()
        if index == 7:
            print " SETTINGS: "
            self.sts.print_all()

        print "\n\n"

    def clear_all_stored_data(self):
        self.prj.clear_all_projects_data(clear_stored_data=True)
        self.sch.clear_all_schemas_data(clear_stored_data=True)

    def clear_all_memory_data(self):
        self.prj.clear_all_projects_data()
        self.sch.clear_all_schemas_data()

    def loading_errors(self, check_this, counter, msg):
        if self.comfun.is_int(check_this):
            counter += check_this
            self.logger.err("Loading error! File: ({}) file errors count:{}".format(msg, check_this))
        return counter

    def load_data(self):
        if self.sts.loading_state >= 4:
            ret_def = self.dfn.load_definitions()
            if self.sio.check_any_data_to_load_exist():
                ret_prj = self.prj.load_projects()
                if ret_prj is not False:
                    self.prj.init_default_proj()
                    ret_sch = self.sch.load_schemas()
                    if ret_sch is not False:
                        ret_tsk = self.tsk.load_tasks()
                        if ret_tsk is not False:
                            ret_que = self.que.load_queue()
                            if ret_que is not False:
                                ret_nod = self.nod.load_nodes()
                                if ret_nod is not False:
                                    loading_err_count = 0     # count number errors while of loading external data
                                    loading_err_count = self.loading_errors(ret_def, loading_err_count, "definitions")
                                    loading_err_count = self.loading_errors(ret_prj, loading_err_count, "project")
                                    loading_err_count = self.loading_errors(ret_sch, loading_err_count, "schemas")
                                    loading_err_count = self.loading_errors(ret_tsk, loading_err_count, "tasks")
                                    loading_err_count = self.loading_errors(ret_tsk, loading_err_count, "queue")
                                    loading_err_count = self.loading_errors(ret_tsk, loading_err_count, "simnodes")
                                    if loading_err_count == 0:
                                        return True, ""
                                    else:
                                        return loading_err_count, "error info in log"
                                else:
                                    return -5, "SimNodes not loaded"
                            else:
                                return -4, "Queue items not loaded"
                        else:
                            return -1, "Tasks data not loaded"
                    else:
                        return -2, "Schemas data not loaded"
                else:
                    return -3, "Projects data not loaded"
            else:
                return -100, "No data exist"
        else:
            return False, "config.ini not loaded"

if __name__ == "__main__":
    sib = SimBatch(5)
