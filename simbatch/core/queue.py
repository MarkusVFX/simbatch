

class QueueItem():
    total_items = 0
    max_id = 0

    def __init__(self, id, queue_item_name, task_id, user, user_id, shot_A, shot_B, shot_C, frame_from, frame_to, state,
                 state_id, version, evolution, evolution_nr, evolution_script_type, evolution_script, prior,
                 description, sim_node, sim_node_id, time, proj_id, soft_id):
        if id > 0:
            self.max_id = id
        else:
            self.max_id += 1
        self.total_items += 1

        self.id = self.max_id
        self.queue_item_name = queue_item_name
        self.task_id = task_id
        self.user = user
        self.user_id = user_id
        self.shot_A = shot_A
        self.shot_B = shot_B
        self.shot_C = shot_C
        self.frame_from = frame_from
        self.frame_to = frame_to
        self.state = state
        self.state_id = state_id
        self.version = version
        self.evolution = evolution
        self.evolution_nr = evolution_nr
        self.evolution_script_type = evolution_script_type
        self.evolution_script = evolution_script
        self.prior = prior
        self.description = description
        self.sim_node = sim_node
        self.sim_node_id = sim_node_id
        self.time = time
        self.proj_id = proj_id
        self.soft_id = soft_id


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