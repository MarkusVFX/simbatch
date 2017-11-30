try:
    import MaxPlus
except ImportError:
    pass

try:
    import hou
except ImportError:
    pass

import os


class Definitions:
    batch = None
    comfun = None

    softwares_array =[]
    total_softwares = 0
    current_software = ""
    current_software_id = 0

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
