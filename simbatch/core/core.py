import platform

from settings import Settings
from common import CommonFunctions, Logger
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
                self.os = "win"
            elif self.os == "Linux":
                self.os = "lnx"
            else:
                self.os = "undefined"

        # below one place abbreviation for variables
        # reasons:
        # - repeated use
        # - identification of the main modules

        self.usr = Users(self)         # usr
        self.prj = Projects(self)      # prj
        self.sch = Schemas(self)       # sch
        self.tsk = Tasks(self)         # tsk
        self.que = Queue(self)         # que
        self.nod = SimNodes(self)      # nod
        self.dfn = Definitions(self)   # dfn
        self.sio = StorageInOut(self)  # sio

        #  abbreviation  END

        self.logger.inf("SimBatch started")

    def print_data(self):
        self.prj.print_all()

    def print_important_values(self):
        print "  \n\n  Current runtime_env: {}", self.sts.runtime_env

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
        if index == 0:
            print " WIZARD: "
        if index == 1:
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
        # if index == 5:
        #     print " TO DO NODES: "
            # TODO NODES !!!!
            # self.nod.print_all()
            # self.nod.print_current()

        if index == 5:  # TODO NODES  index 4 vs 5 !
            print " SETTINGS: "
            self.sts.print_all()

        print "\n\n"

    def clear_all_stored_data(self):
        self.prj.clear_all_projects_data(clear_stored_data=True)
        self.sch.clear_all_schemas_data(clear_stored_data=True)

    def clear_all_memory_data(self):
        self.prj.clear_all_projects_data()
        self.sch.clear_all_schemas_data()

    def load_data(self):
        self.dfn.load_definitions()

        if self.prj.load_projects():
            self.prj.init_default_proj()
            if self.sch.load_schemas():
                if self.tsk.load_tasks():
                    return True
                else:
                    return -1
            else:
                return -2
        else:
            return -3

    def create_example_data(self):
        self.prj.create_example_project_data()


if __name__ == "__main__":
    sib = SimBatch(5)
