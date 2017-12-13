
class Users:
    batch = None
    comfun = None
    all_users = []

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.all_users = []
