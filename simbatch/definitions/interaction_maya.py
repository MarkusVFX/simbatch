class Interaction:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger):
        self.current_os = current_os
        self.logger = logger

    def print_info(self):
        self.logger.raw("This is interaction with Maya")

    # framework interactions
    def schema_item_double_click(self, param):
        self.maya_open_scene(param)

    def save_as_next_version(self, param):
        self.save_current_scene_as(param)

    # maya interactions
    def maya_open_scene(self, file):
        import maya.cmds as cmd
        ret = cmd.file ( target, o=True, force=True)
        return ret

    def save_current_scene_as(self, file):
        import maya.cmds as cmd
        ret1 = cmd.file ( rename = target )
        ret2 = cmd.file ( save=True, type="mayaBinary")
        return ret2

    def maya_get_selection(self):
        print "TODO: maya_get_selection"
        return "test sel obj"
        
    def maya_get_camera(self):
        print "TODO: maya_get_camera"
        pass
    
    def get_curent_scenefile(self):
        import maya.cmds as cmd
        fi = cmd.file(query=True, sceneName=True)
        if self.current_os == 2:
            fi = fi.replace('/', '\\')
        basename = os.path.basename(fi)
        out_dir = fi[:-1*len(basename)]
        out_file_header = basename.split(".")[0]
        out_file_ext = basename.split(".")[1]
        return [out_dir, basename, out_file_header]
    
    def get_curent_framerange(self):
        orgMin = cmd.playbackOptions(query = True, minTime = True)
        orgMax = cmd.playbackOptions(query = True, maxTime = True)
        return [orgMin, orgMax]
    
    def maya_get_selection(self):
        sel = cmd.ls(selection = True)
        return sel
        
    def maya_import_ani(self, objects, dir):
        pass
        
    def maya_import_cam(self, objects, file_or_dir):
        pass
        
    def maya_import_obj(self, objects, file_or_dir):
        pass
        
    def maya_set_param(self, object, property, value):
        pass
        
    def maya_simulate_ncloth(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_nhair(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_nparticle(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_fume(self, ts, te, fume_container, cache_dir):
        pass
        
    def maya_simulate_fumewt(self, ts, te, fume_container, cache_dir):
        pass
        
    def maya_render_blast(self, ts, te, out_file=""):
        pass
        
    def maya_render_software(self, ts, te, out_file=""):
        pass
        
    def maya_save_scene(self, file):
        pass
        
    def maya_script_py(self, file):
        pass
        
    def maya_script_mel(self, file):
        pass 

    def maya_get_scene_objects(self):
        print "\n test maya_get_scene_objects\n"
