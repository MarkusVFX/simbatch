from settings import Settings
from common import CommonFunctions
from users import Users
from definitions import Definitions
from projects import Projects
from schemas import Schemas
from tasks import Tasks
from queue import Queue
from nodes import SimNodes
from io import InOutStorage


class Logger:
    # 1 only ERR, 2 +WRN, 3 +INF, 4 +important [db], 5 +[db], 6 ALL
    console_level = 0
    log_file_level = 0
    log_file_path = ""
    force_add_to_log = False

    def __init__(self, init_level_log=None, init_level_console=None ):
        if init_level_console is None or init_level_console > 4:
            print "Logger init"

    def set_logger_level(self, lvl):
        self.level = lvl

    def add_to_log(self,prefix, message):
        pass
        # TODO !!!

    def dispatch (self, level, message, add_to_log):
        if level == 1:
            prefix = "ERR"
        elif level == 2:
            prefix = "WRN"
        elif level == 3:
            prefix = "INF"
        elif level == 4:
            prefix = "DB"
        elif level == 4:
            prefix = "DEEPDB"
        else:
            prefix = "null"

        if type(message) is tuple:
            out = "  ".join([str(el) for el in message])
            print "   [{}] {}".format(prefix, out)
        else:
            print "   [{}] {}".format(prefix, message)

        if self.force_add_to_log or add_to_log:
            self.add_to_log(prefix, message)

    def err(self, message, add_to_log=True):
        self.dispatch(1, message, add_to_log=add_to_log)

    def wrn(self, message, add_to_log=True):
        self.dispatch(2, message, add_to_log=add_to_log)

    def inf(self, message, add_to_log=False):
        self.dispatch(3, message, add_to_log=add_to_log)

    def db(self, message, add_to_log=False):
        self.dispatch(4, message, add_to_log=add_to_log)

    def deepdb(self, message, add_to_log=False):
        self.dispatch(5, message, add_to_log=add_to_log)



class SimBatch:
    s = None
    comfun = None
    logger = None

    def __init__(self, runtime_env, ini_file="config.ini"):
        self.s = Settings(runtime_env, ini_file=ini_file)
        self.logger = Logger(init_level_log=0, init_level_console=self.s.debug_level)
        self.comfun = CommonFunctions(debug_level=self.s.debug_level)


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
        print " [INF] SimBatch started"

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
