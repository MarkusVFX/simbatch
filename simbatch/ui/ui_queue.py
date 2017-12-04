


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