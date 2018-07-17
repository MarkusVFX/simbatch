
class Interactions:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger):
        self.current_os = current_os
        self.logger = logger

    def print_info(self):
        self.logger.raw("This is interaction with Houdini")

    # framework interactions
    def schema_item_double_click(self, param):
        self.houdini_open_scene(param)

    def save_as_next_version(self, param):
        self.save_current_scene_as(param)

    # houdini interactions
    def houdini_open_scene(self, file):
        pass
        
    def houdini_import_ani(self, objects, dir):
        pass
        
    def houdini_import_cam(self, objects, file_or_dir):
        pass
        
    def houdini_import_obj(self, objects, file_or_dir):
        pass
    
    def houdini_simulate(self, ts, te, objects_names, cache_dir):
        pass   
        
    def houdini_render(self, ts, te, out_file=""):
        pass

    def houdini_save_scene(self, file):
        pass

    def save_current_scene_as(self, file):
        pass
