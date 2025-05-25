import os
import sys
import definitions.interactions_base as interactions_base

class Interactions(interactions_base.BaseInteractions):
    current_os = -1
    logger = None
    comfun = None
    _max_available = False

    def __init__(self, current_os, logger, comfun):
        super().__init__(current_os, logger, comfun)
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun
        # Try to import MaxPlus but don't fail if not available
        try:
            import MaxPlus
            self._max_available = True
            self.MaxPlus = MaxPlus
        except ImportError:
            self._max_available = False
            self.logger.wrn("3ds Max Python API not available - some functionality will be limited")

    def print_info(self):
        self.logger.raw("This is interaction with 3ds Max")

    def _check_max(self):
        """Check if MaxPlus is available and raise appropriate error if not"""
        if not self._max_available:
            raise ImportError("3ds Max Python API not available")

    # common interactions
    def schema_item_double_click(self, param):
        self.max_open_scene(param)

    def task_item_double_click(self, param):
        self.max_open_scene(param)

    def open_scene(self, param):
        """Open a scene file"""
        self.max_open_file(param)

    def save_scene(self, param):
        """Save current scene"""
        self.save_current_scene_as(param)

    def save_scene_as_next_version(self, param):
        """Save current scene as next version"""
        self.save_current_scene_as(param)

    def set_param(self, objects, property, value):
        self.max_set_param(objects, property, value)

    # max interactions
    def max_open_scene(self, target):
        self.logger.int(("max_open_scene", target))
        try:
            self._check_max()
            if self.comfun.file_exists(target, info="(interactions max_open_scene)"):
                self.MaxPlus.FileManager.Open(target)
                ret = True
            else:
                self.logger.err((" no file :", target))
                ret = False
            return ret
        except ImportError:
            self.logger.err("3ds Max Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error opening 3ds Max file: {str(e)}")
            return False

    def max_save_scene(self, file):  # TODO cleanup  max_save_scene  vs save_current_scene_as
        self.logger.int(("max_save_scene", file))
        self.save_current_scene_as(file)

    def save_current_scene_as(self, target_file):
        target_dir = self.comfun.dirname(target_file)
        self.logger.db((" target_dir: ", str(target_dir)))
        self.comfun.create_directory_if_not_exists(target_dir)
        if self.comfun.path_exists(target_dir):
            self.comfun.create_directory(target_dir)
        self.MaxPlus.FileManager.Save(target_file)
        return True

    def max_select_objects(self, objs):
        self.MaxPlus.SelectionManager.ClearNodeSelection()
        for obj in objs.split(","):
            if self.MaxPlus.INode.GetINodeByName(obj):
                self.MaxPlus.SelectionManager.SelectNode(self.MaxPlus.INode.GetINodeByName(obj), True)

        selected_count = self.MaxPlus.SelectionManager.GetCount()
        if selected_count == 0:
            return False
        else:
            return selected_count

    def max_get_selection(self):
        sel = self.MaxPlus.SelectionManager.GetNodes()
        return sel

    def max_get_camera(self):
        print("TODO: max_get_camera")
        pass

    def get_curent_scene_file(self):
        """Get the current 3ds Max scene file path and info.
        
        Returns:
            tuple: (directory, filename, filename_without_ext, extension)
        """
        try:
            # Get current .max file path
            current_file = self.MaxPlus.FileManager.GetFileNameAndPath()
            
            if not current_file:
                self.logger.wrn("No current 3ds Max scene file")
                return "", "", "", "max"
                
            # Convert path separators for Windows if needed
            if self.current_os == 2:  # Windows
                current_file = current_file.replace('/', '\\')
            
            # Split path into components
            directory = os.path.dirname(current_file)
            filename = os.path.basename(current_file)
            filename_without_ext = os.path.splitext(filename)[0]
            extension = os.path.splitext(filename)[1].lstrip('.')
            
            return directory, filename, filename_without_ext, extension
            
        except Exception as e:
            self.logger.err(f"Error getting current 3ds Max scene file: {str(e)}")
            return "", "", "", "max"

    def get_curent_frame_range(self):
        playback_min = self.MaxPlus.Animation.GetAnimStart()
        playback_max = self.MaxPlus.Animation.GetAnimEnd()
        return playback_min, playback_max
        

    def max_import_ani(self, objects, dir=""):
        self.logger.int(("max_import_ani", objects, dir))

    def max_import_cam(self, objects, file_or_dir):
        self.logger.int(("max_import_cam", objects, file_or_dir))

    def max_import_obj(self, objects, file_or_dir):
        self.logger.int(("max_import_obj", objects, file_or_dir))


    def max_set_param(self, val, abbrev_param=None, value=None):
        if abbrev_param is None:
            str_expression = val             # first input as expression string  # TODO
            a1 = str_expression.split(".")
            a2 = a1[1].split("=")
            str_obj = a1[0].strip()
            str_attrib = a2[0].strip()
            str_val = a2[1].strip()
            try:
                self.MaxPlus.Core.EvalMAXScript(f"{str_obj}.{str_attrib} = {str_val}")
            except Exception as e:
                self.logger.err(("max_set_param: ", str_obj, str_attrib, str_val, "   ___   ", str_expression))
                self.logger.err(("max_set_param e: ", e))
        else:
            objects = val       # first input as objects string  # TODO

            if not objects:
                ret = self.get_cloth_objects()
                if ret:
                    objects = ",".join(ret)

            if objects == "<cloth_objects>":
                ret = self.get_cloth_objects()
                if ret:
                    objects = ",".join(ret)

            for obj in objects.split(","):
                param_full_name = abbrev_param
                self.MaxPlus.Core.EvalMAXScript(f"{obj}.{param_full_name} = {value}")
            self.logger.db(("max_set_param", object, property, value), nl=True)

    def max_simulate_cloth(self, ts, te, objects_names, cache_dir):
        self.logger.int(("max_simulate_cloth", ts, te, objects_names, cache_dir))

    def max_simulate_hair(self, ts, te, objects_names, cache_dir):
        self.logger.int(("max_simulate_hair", ts, te, objects_names, cache_dir))

    def max_simulate_particle(self, ts, te, objects_names, cache_dir):
        self.logger.int(("max_simulate_particle", ts, te, objects_names, cache_dir))

    def max_simulate_fume(self, ts, te, fume_container, cache_dir):
        self.logger.int(("max_simulate_fume", ts, te, fume_container, cache_dir))

    def max_simulate_fumewt(self, ts, te, fume_container, cache_dir):
        self.logger.int(("max_simulate_fumewt", ts, te, fume_container, cache_dir))

    def max_render_blast(self, ts, te, out_file=""):
        self.logger.int(("max_render_blast", ts, te, out_file))

    def max_render_software(self, ts, te, out_file=""):
        self.logger.int(("max_render_software", ts, te, out_file))

    def max_script_py(self, file):
        self.logger.int(("max_script_py", file))

    def max_script_max(self, file):
        self.logger.int(("max_script_max", file))

    def max_get_scene_objects(self):
        return self.MaxPlus.Core.GetRootNode().Children

    def get_objects_by_type(self, type):
        objs = []
        for obj in self.MaxPlus.Core.GetRootNode().Children:
            if obj.Object.GetClassName() == type:
                objs.append(obj.Name)
        return objs

    def get_cloth_objects(self):
        return self.get_objects_by_type("Cloth")

    def get_hair_objects(self):
        return self.get_objects_by_type("Hair")

    def get_particle_objects(self):
        return self.get_objects_by_type("Particle")

    def get_fume_container(self):
        return self.get_objects_by_type("FumeFX")

    def import_camera(self):
        self.logger.int("import_camera")
