
class Schemas:
    batch = None
    comfun = None

    total_schemas = 0

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
