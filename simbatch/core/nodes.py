
class SimNodes:
    batch = None
    comfun = None

    nodes_data = None
    total_nodes = 0

    current_node_id = None
    current_node_index = None
    current_node = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun

    #  print project data, mainly for debug
    def print_current(self):
        print "       current node index:{}, id:{}, total:{}".format(self.current_node_index, self.current_node_id,
                                                                     self.total_nodes)

        if self.current_node_index is not None:
            cur_nod = self.current_node   # TODO
            #print "       schemaID:", cur_tsk.schemaID, "       projID:", cur_tsk.projID
            #print "       shotDetails ", cur_tsk.shotA, "   ", cur_tsk.shotB, "   ", cur_tsk.shotC
            #print "       frameFrom  frameTo ", cur_tsk.frameFrom, cur_tsk.frameTo
            #print "       state  state_id ", cur_tsk.state, "    ", cur_tsk.state_id

    def print_all(self):
        for n in self.nodes_data:
            print "\n\n ", n.node_name
            # TODO
        if self.total_nodes == 0:
            print "   [INF] no info about nodes"
        print "\n\n"
