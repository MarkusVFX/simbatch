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
        #  self.o = Softwares(self.s, self.i)
        #  self.s.load_definitions()
        print " [INF] SimBatch started"

    def print_data(self):
        self.p.print_all()

    def print_important_values(self):
        print "  \n\n  current soft: {}\n\n  PROJECT: ".format(self.s.current_soft_name)
        print "     current_project_id: {}    current_project_index: {}    total_projects: {}".format(
            self.p.current_project_id, self.p.current_project_index, self.p.total_projects)

        if self.p.current_project_index >= 0:
            cur_proj = self.p.current_project
            print "       current project: ", cur_proj.project_name
            print "       project_directory ", cur_proj.project_directory
            print "       working_directory ", cur_proj.working_directory
            print "       cameras_directory ", cur_proj.cameras_directory
            print "       cache_directory ", cur_proj.cache_directory

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

    def clear_all_stored_data(self):
        self.p.clear_all_projects_data(clear_stored_data=True)

    def clear_all_memory_data(self):
        self.p.clear_all_projects_data()

    def load_data(self):
        if self.p.load_projects():
            self.p.init_default_proj()
            return True
        else:
            return False

    def create_example_data(self):
        self.p.create_example_project_data()


if __name__ == "__main__":
    sib = SimBatch(5)
