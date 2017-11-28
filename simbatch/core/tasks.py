
class Tasks:
    batch = None
    comfun = None

    total_tasks = 0

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
