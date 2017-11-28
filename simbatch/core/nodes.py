
class SimNodes:
    batch = None
    comfun = None

    total_nodes = 0

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
