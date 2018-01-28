from settings import Settings
from common import CommonFunctions, Logger
from users import Users
from definitions import Definitions
from projects import Projects
from schemas import Schemas
from tasks import Tasks
from queue import Queue
from nodes import SimNodes
from io import InOutStorage


class SimBatch:
    s = None
    comfun = None
    logger = None

    def __init__(self, runtime_env, ini_file="config.ini"):
        self.s = Settings(runtime_env, ini_file=ini_file)
        self.logger = Logger(log_level=0, console_level=self.s.debug_level)
        self.comfun = CommonFunctions(self.logger)

        self.u = Users(self)
        self.p = Projects(self)
        self.c = Schemas(self)
        self.t = Tasks(self)
        self.q = Queue(self)
        self.n = SimNodes(self)
        self.d = Definitions(self)
        self.i = InOutStorage(self)
        #  self.o = Softwares(self)  <- Definitions
        #  self.s.load_definitions()
        self.logger.inf("SimBatch started")

    def print_data(self):
        self.p.print_all()

    def print_important_values(self):
        print "  \n\n  Current runtime_env: {}", self.s.runtime_env

        # projects
        print "\n PROJECTS: "
        self.p.print_current()

        # schemas
        print "\n SCHEMAS: "
        self.c.print_current()

        # tasks
        print "\n TASKS: "
        self.t.print_current()

        # queue
        print "\n QUEUE: "
        self.q.print_current()

        # nodes
        print "\n NODES: "
        self.n.print_current()
        
        # print "       currentTaskID:", self.t.currentTaskID, "   currentTaskIndex:", self.t.currentTaskIndex, "   total_projects:", self.p.total_projects
        # if self.t.currentTaskIndex >= 0:
        #     curTsk = self.t.tasksData[self.t.currentTaskIndex]
        #     print "       current task: ", curTsk.taskName
        #     print "       schemaID:", curTsk.schemaID, "       projID:", curTsk.projID  # ,  "       soft_id:", curTsk.projID,
        #     print "       shotDetails ", curTsk.shotA, "   ", curTsk.shotB, "   ", curTsk.shotC
        #     print "       frameFrom  frameTo ", curTsk.frameFrom, curTsk.frameTo
        #     print "       state  state_id ", curTsk.state, "    ", curTsk.state_id
        #
        #
        # print "       currentQueueID:", self.q.currentQueueID, "   currentQueueIndex:", self.q.currentQueueIndex, "   total_projects:", self.p.total_projects
        # if self.q.currentQueueIndex >= 0:
        #     curQue = self.q.queueData[self.q.currentQueueIndex]
        #     print "       current queueItem: ", curQue.queueItemName, "     version :", curQue.version, "     evolutionNr :", curQue.evolutionNr
        print "\n\n"

    def print_current_detailed_values(self, index):
        print "  \n\n"
        if index == 0:
            print " WIZARD: "
        if index == 1:
            self.p.print_all()
            self.p.print_current()
        if index == 2:
            print " SCHEMAS: "
            self.c.print_all()
            self.c.print_current()
        if index == 3:
            print " TASKS: "
            self.t.print_all()
            self.t.print_current()
        if index == 4:
            print " QUEUE: "
            self.q.print_all()
            self.q.print_current()
        if index == 5:
            print " NODES: "
            self.n.print_all()
            self.n.print_current()

        if index == 4:
            print " SETTINGS: "
            self.s.print_all()

        print "\n\n"

    def clear_all_stored_data(self):
        self.p.clear_all_projects_data(clear_stored_data=True)
        self.c.clear_all_schemas_data(clear_stored_data=True)

    def clear_all_memory_data(self):
        self.p.clear_all_projects_data()
        self.c.clear_all_schemas_data()

    def load_data(self):
        self.d.load_definitions()

        if self.p.load_projects():
            self.p.init_default_proj()
            if self.c.load_schemas():
                if self.t.load_tasks():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def create_example_data(self):
        self.p.create_example_project_data()


if __name__ == "__main__":
    sib = SimBatch(5)
