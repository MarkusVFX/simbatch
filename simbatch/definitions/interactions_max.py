import sys

class Interactions:
    current_os = -1
    logger = None
    comfun = None

    def __init__(self, current_os, logger, comfun):
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun

    def print_info(self):
        self.logger.raw("This is interaction with 3ds Max")

    # common interactions
    def schema_item_double_click(self, param):
        self.max_open_scene(param)

    def task_item_double_click(self, param):
        self.max_open_scene(param)

    def open_setup(self, param):
        self.max_open_scene(param)

    def save_setup(self, param):
        self.save_current_scene_as(param)

    def save_setup_as_next_version(self, param):
        self.save_current_scene_as(param)

    def set_param(self, objects, property, value):
        self.max_set_param(objects, property, value)

    # max interactions
    def max_open_scene(self, target):
        self.logger.int(("max_open_scene", target))
        try:
            import MaxPlus
            if self.comfun.file_exists(target, info="(interactions max_open_scene)"):
                MaxPlus.FileManager.Open(target)
                ret = True
            else:
                self.logger.err((" no file :", target))
                ret = False
            return ret
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")

    def max_save_scene(self, file):  # TODO cleanup  max_save_scene  vs save_current_scene_as
        self.logger.int(("max_save_scene", file))
        self.save_current_scene_as(file)

    def save_current_scene_as(self, target_file):
        target_dir = self.comfun.dirname(target_file)
        self.logger.db((" target_dir: ", str(target_dir)))
        self.comfun.create_directory_if_not_exists(target_dir)
        if self.comfun.path_exists(target_dir):
            self.comfun.create_directory(target_dir)
        import MaxPlus
        MaxPlus.FileManager.Save(target_file)
        return True

    def max_select_objects(self, objs):
        import MaxPlus
        MaxPlus.SelectionManager.ClearNodeSelection()
        for obj in objs.split(","):
            if MaxPlus.INode.GetINodeByName(obj):
                MaxPlus.SelectionManager.SelectNode(MaxPlus.INode.GetINodeByName(obj), True)

        selected_count = MaxPlus.SelectionManager.GetCount()
        if selected_count == 0:
            return False
        else:
            return selected_count

    def max_get_selection(self):
        import MaxPlus
        sel = MaxPlus.SelectionManager.GetNodes()
        return sel

    def max_get_camera(self):
        print("TODO: max_get_camera")
        pass

    def get_curent_scene_file(self):
        self.logger.int("get_curent_scene_file")
        import MaxPlus
        fi = MaxPlus.FileManager.GetFileNameAndPath()
        if self.current_os == 2:
            fi = fi.replace('/', '\\')
        basename = os.path.basename(fi)
        out_dir = fi[:-1*len(basename)]
        out_file_header = basename.split(".")[0]
        out_file_ext = basename.split(".")[1]
        return out_dir, basename, out_file_header, out_file_ext

    def get_curent_frame_range(self):
        import MaxPlus
        playback_min = MaxPlus.Animation.GetAnimStart()
        playback_max = MaxPlus.Animation.GetAnimEnd()
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
                import MaxPlus
                MaxPlus.Core.EvalMAXScript(f"{str_obj}.{str_attrib} = {str_val}")
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

            import MaxPlus
            for obj in objects.split(","):
                param_full_name = abbrev_param
                MaxPlus.Core.EvalMAXScript(f"{obj}.{param_full_name} = {value}")
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
        import MaxPlus
        return MaxPlus.Core.GetRootNode().Children

    def get_objects_by_type(self, type):
        import MaxPlus
        objs = []
        for obj in MaxPlus.Core.GetRootNode().Children:
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
