""" users are fully implemented in Pro version """


class SingleUser:
    """ users are fully implemented in Pro version """
    id = None
    name = None
    abbrev = None

    def __init__(self, id, name, abbrev):
        self.id = id
        self.name = name
        self.abbrev = abbrev


class Users:
    """ users are fully implemented in Pro version """
    # users implemented in Pro version
    batch = None
    comfun = None
    mode = 0         # 1 single mode,   2 multi user mode
    all_users = []

    def __init__(self, batch, mode=None):
        self.batch = batch
        self.comfun = batch.comfun
        self.all_users = []
        if mode is not None:
            if mode == 1:
                self.setup_single_user_mode()

    def setup_single_user_mode(self):
        self.mode = 1
        u = SingleUser(1, "Single", ".")
        self.all_users.append(u)

    def get_user_by_id(self, uid):
        for u in self.all_users:
            if u.id == uid:
                return u
        return None

    def get_default_user(self):
        return self.all_users[0]


""" users are fully implemented in Pro version """
