from settings import Settings
from common import CommonFunctions
from users import Users
from definitons import Definitions
from projects import Projects
from schemas import Schemas
from tasks import Tasks
from queue import Queue
from nodes import SimNodes
from io import InOutStorage


class SimBatch:
    s = None
    comfun = None

    def __init__(self, soft_id, ini_file="config.ini"):
        self.s = Settings(soft_id, ini_file=ini_file)
        self.comfun = CommonFunctions(debug_level=self.s.debug_level)

        self.u = Users(self)
        self.d = Definitions(self)
        self.p = Projects(self)
        self.c = Schemas(self)
        self.t = Tasks(self)
        self.q = Queue(self)
        self.n = SimNodes(self)
        self.i = InOutStorage(self)
        #  self.o = Softwares(self)  <- Definitions
        #  self.s.load_definitions()
        print " [INF] SimBatch started"

    def print_data(self):
        self.p.print_all()

    def print_important_values(self):
        print "  \n\n  Current soft: {}\n\n  PROJECT: ".format(self.s.current_soft_name)
        print "     current project: id: {}     index: {}    total_projects: {}".format(self.p.current_project_id,
                                                                                        self.p.current_project_index,
                                                                                        self.p.total_projects)

        if self.p.current_project_index >= 0:
            cur_proj = self.p.current_project
            print "       current project: ", cur_proj.project_name
            print "       project_directory ", cur_proj.project_directory
            print "       working_directory ", cur_proj.working_directory
            print "       cameras_directory ", cur_proj.cameras_directory
            print "       cache_directory ", cur_proj.cache_directory

        print "\n  SCHEMA: "
        print "       current schema id:{}   index:{}   total:{}".format(self.c.current_schema_id,
                                                                         self.c.current_schema_index,
                                                                         self.c.total_schemas)
        if self.c.current_schema_id >= 0:
            cur_sch = self.c.current_schema
            print "       current schema: "
            print "       name: {}  definition id:{}   project id:{}".format(cur_sch.schema_name,
                                                                             cur_sch.definition_id,
                                                                             cur_sch.project_id)
            for i, a in enumerate(cur_sch.actions_array):
                print "       a:{}  soft:{}   type:{}  sub type:{} ".format(i, a.soft_id, a.action_type, a.actionParam)
        '''
        print " TASK: "
        print "       currentTaskID:", self.t.currentTaskID, "   currentTaskIndex:", self.t.currentTaskIndex, "   total_projects:", self.p.total_projects
        if self.t.currentTaskIndex >= 0:
            curTsk = self.t.tasksData[self.t.currentTaskIndex]
            print "       current task: ", curTsk.taskName
            print "       schemaID:", curTsk.schemaID, "       projID:", curTsk.projID  # ,  "       soft_id:", curTsk.projID, 
            print "       shotDetails ", curTsk.shotA, "   ", curTsk.shotB, "   ", curTsk.shotC
            print "       frameFrom  frameTo ", curTsk.frameFrom, curTsk.frameTo
            print "       state  state_id ", curTsk.state, "    ", curTsk.state_id

        print " QUEUE: "
        print "       currentQueueID:", self.q.currentQueueID, "   currentQueueIndex:", self.q.currentQueueIndex, "   total_projects:", self.p.total_projects
        if self.q.currentQueueIndex >= 0:
            curQue = self.q.queueData[self.q.currentQueueIndex]
            print "       current queueItem: ", curQue.queueItemName, "     version :", curQue.version, "     evolutionNr :", curQue.evolutionNr

        print " NODES: "
        print "       currentNodeNr:", self.n.currentNodeNr, "   totalNodes:", self.n.totalNodes
        if self.n.currentNodeNr >= 0:
            curNod = self.n.nodesData[self.n.currentNodeNr]
            print "       current node: ", curNod.nodeName, curNod.description
        '''
        print "\n\n\n\n"


    def print_current_module_values(self, module_index):
        print "  \n\n\n "
        if module_index == 0:
            print " WIZARD: "
        if module_index == 1:
            print " PROJECTS: "
            print "       current_project_index: {}   total_projects: {}".format(self.p.total_projects,
                                                                                 self.p.current_project_index)
            print "\n\n"
            self.p.print_all()
        if module_index == 2:
            print " SCHEMAS: "
            print "       current_schema_index: {}   total_schemas: {}".format(self.c.total_schemas,
                                                                                 self.c.current_schema_index)
            print "\n\n"
            self.c.print_all()

    def clear_all_stored_data(self):
        self.p.clear_all_projects_data(clear_stored_data=True)
        self.c.clear_all_schemas_data(clear_stored_data=True)

    def clear_all_memory_data(self):
        self.p.clear_all_projects_data()
        self.c.clear_all_schemas_data()

    def load_data(self):
        if self.p.load_projects():
            self.p.init_default_proj()
            if self.c.load_schemas():
                return True
            else:
                return False
        else:
            return False

    def create_example_data(self):
        self.p.create_example_project_data()


if __name__ == "__main__":
    sib = SimBatch(5)
