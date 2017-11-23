class MainWindow(  ):
    sim_batch = None
    def __init__(self, sim_batch):
        print "Main window init"
        self.sim_batch = sim_batch

    def init_lists (self):
        print "init lists"
