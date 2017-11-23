from settings import Settings
from common import CommonFunctions

class SimBatch:
    s=None
    comfun=None
    def __init__(self,ini_file):
        self.s = Settings(ini_file)
        self.comfun = CommonFunctions(self.s.debug_level)
        #self.s.load_definitions()
        print "SimBatch started"

if __name__ == "__main__":
    sib = SimBatch()