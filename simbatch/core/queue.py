
class Queue:
    batch = None
    comfun = None

    queue_data = None
    total_queue_items = 0

    current_queue_id = None
    current_queue_index = None
    current_queue = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun

    #  print project data, mainly for debug
    def print_header(self):
        print "\n QUEUE: "
        print "     current project: id: {}     index: {}    total_projects: {}\n".format(self.current_queue_id,
                                                                                          self.current_queue_index,
                                                                                          self.total_queue_items)

    def print_current(self):
        print "       current task index:{}, id:{}, total:{}".format(self.current_queue_index, self.current_queue_id,
                                                                     self.total_queue_items)
        if self.current_queue_index is not None:
            cur_que = self.current_queue
            print "       current queue name:{}".format(cur_que.queue_name)
            # TODO
            #print "       schemaID:", cur_tsk.schemaID, "       projID:", cur_tsk.projID
            #print "       shotDetails ", cur_tsk.shotA, "   ", cur_tsk.shotB, "   ", cur_tsk.shotC
            #print "       frameFrom  frameTo ", cur_tsk.frameFrom, cur_tsk.frameTo
            #print "       state  state_id ", cur_tsk.state, "    ", cur_tsk.state_id

    def print_all(self):
        if self.total_queue_items == 0:
            print "   [INF] no queu items loaded"
        for q in self.queue_data:
            print "\n\n ", q.queue_name
            # TODO
        print "\n\n"