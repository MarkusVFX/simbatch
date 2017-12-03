
class TaskItem():
    def __init__(self, id, task_name, schema_id, user, user_id, shot_A, shot_B, shot_B, frame_from, frame_to, state, state_id, schema_ver, queue_ver,evolution, prior, options, description, proj_id, frame_range_status, task_ver ):
        self.id = id
        self.task_name = task_name
        self.schema_id = schema_id
        self.user = user
        self.user_id = user_id
        self.shot_A = shot_A
        self.shot_B = shot_B
        self.shot_B = shot_B
        self.frame_from = frame_from
        self.frame_to = frame_to
        self.state = state
        self.state_id = state_id
        self.task_ver = task_ver
        self.schema_ver = schema_ver
        self.queue_ver = queue_ver
        self.evolution = evolution
        self.prior = prior
        self.options = options
        self.description = description
        self.proj_id = proj_id
        self.frame_range_status = frame_range_status



class Tasks:
    batch = None
    comfun = None

    total_tasks = 0

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
