
class Interactions:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger, comfun):
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun

    def print_info(self):
        self.logger.raw("This is interaction with Houdini")

    # common interactions
    def schema_item_double_click(self, param):
        self.houdini_open_scene(param)

    def task_item_double_click(self, param):
        self.houdini_open_scene(param)

    def open_setup(self, param):
        self.houdini_open_scene(param)

    def save_setup(self, param):
        self.save_current_scene_as(param)

    def save_setup_as_next_version(self, param):
        self.save_current_scene_as(param)

    # houdini interactions
    def houdini_open_scene(self, file_name):
        hou.hipFile.load(file_name, suppress_save_prompt=True, ignore_load_warnings=True)

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

    def save_current_scene_as(self, file_name):
        hou.hipFile.save(file_name, save_to_recent_files=True)
