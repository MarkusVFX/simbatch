
class Queue:
    batch = None
    comfun = None

    total_queue_jobs = 0

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
