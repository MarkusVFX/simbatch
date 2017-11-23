
class Settings:
    version = "v0.2.02"
    ini_file = None
    debug_level = 3

    def __init__(self, ini_file):
        print "settings init"
        self.ini_file = ini_file
