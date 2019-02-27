class Interactions:
    current_os = -1
    logger = None
    comfun = None

    def __init__(self, current_os, logger, comfun):
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun

    def print_info(self):
        self.logger.raw("This is interaction with Maya")

    # common interactions
    def schema_item_double_click(self, param):
        self.maya_open_scene(param)

    def task_item_double_click(self, param):
        self.maya_open_scene(param)

    def open_setup(self, param):
        self.maya_open_scene(param)

    def save_setup(self, param):
        self.save_current_scene_as(param)

    def save_setup_as_next_version(self, param):
        self.save_current_scene_as(param)

    def set_param(self, objects, property, value):
        self.maya_set_param(objects, property, value)

    # maya interactions
    def maya_open_scene(self, target):
        self.logger.int(("maya_open_scene", target))
        try:
            import maya.cmds as cmd
            ret = cmd.file(target, o=True, force=True)
            return ret
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

    def maya_save_scene(self, file):  # TODO cleanup  maya_save_scene  vs save_current_scene_as
        self.logger.int(("maya_save_scene", file))
        self.save_current_scene_as(file)

    def save_current_scene_as(self, target_file):
        target_dir = self.comfun.dirname(target_file)
        self.logger.db((" target_dir: ", str(target_dir)))
        self.comfun.create_directory_if_not_exists(target_dir)
        if self.comfun.path_exists(target_dir):
            self.comfun.create_directory(target_dir)
        import maya.cmds as cmd
        cmd.file(rename=target_file)
        ret = cmd.file(save=True, type="mayaBinary")
        return ret

    def maya_get_selection(self):
        import maya.cmds as cmd
        sel = cmd.ls(selection=True)
        return sel
        
    def maya_get_camera(self):
        print "TODO: maya_get_camera"
        pass
    
    def get_curent_scene_file(self):
        self.logger.int("get_curent_scene_file")
        import maya.cmds as cmd
        fi = cmd.file(query=True, sceneName=True)
        if self.current_os == 2:
            fi = fi.replace('/', '\\')
        basename = os.path.basename(fi)
        out_dir = fi[:-1*len(basename)]
        out_file_header = basename.split(".")[0]
        out_file_ext = basename.split(".")[1]
        return out_dir, basename, out_file_header, out_file_ext
    
    def get_curent_frame_range(self):
        import maya.cmds as cmd
        playback_min = cmd.playbackOptions(query=True, minTime=True)
        playback_max = cmd.playbackOptions(query=True, maxTime=True)
        return playback_min, playback_max
        
    def maya_import_ani(self, objects, dir=""):
        self.logger.int(("maya_import_ani", objects, dir))
        
    def maya_import_cam(self, objects, file_or_dir):
        self.logger.int(("maya_import_cam", objects, file_or_dir))
        
    def maya_import_obj(self, objects, file_or_dir):
        self.logger.int(("maya_import_obj", objects, file_or_dir))
        
    def maya_set_param(self, objects, abbrev_param, value):
        import maya.cmds as cmd
        for obj in objects.split(","):
            param_full_name = abbrev_param
            cmd.setAttr(obj+"."+param_full_name, value)
        self.logger.db(("maya_set_param", object, property, value), nl=True)
        
    def maya_simulate_ncloth(self, ts, te, objects_names, cache_dir, cache_mode=1, cache_subsamples=1):
        self.logger.int(("maya_simulate_ncloth", ts, te, objects_names, cache_dir))

        if self.comfun.path_exists(cache_dir) is False:
            self.comfun.create_directory(cache_dir)

        import maya.cmds as cmds
        import maya.mel as ml

        if cache_mode == 1:
            pc_mode = "OneFile"
        if cache_mode == 2:
            pc_mode = "OneFilePerFrame"

        fr_start = self.comfun.int_or_val(ts, 0)
        fr_end = self.comfun.int_or_val(te, 0)
        cmds.playbackOptions(minTime=fr_start)
        cmds.playbackOptions(maxTime=fr_end)
        try:
            cmd = 'select -r ' + objects_names.replace(",", " ")    #  TODO ' ; viewFit;'
            self.logger.inf(cmd, nl=True, nl_after=True)
            ml.eval(cmd)

            cache_dir = cache_dir.replace("\\", "/")

            # maya 2015  # TODO !!!
            cmd = 'doCreateNclothCache 4 {"2", "1", "10", "' + pc_mode + '", "1", "' + cache_dir + '",'
            cmd += ' "1", "", "0", "add", "1", "' + str(cache_subsamples) + '", "1","0","1" } ;'

            # maya 2018
            cmd = 'doCreateNclothCache 5 {"2", "1", "10", "' + pc_mode + '", "1", "' + cache_dir + '",'
            cmd += ' "0", "", "0", "add", "0", "' + str(cache_subsamples) + '", "1", "0", "1", "mcx"};'

            self.logger.inf(cmd, nl=True, nl_after=True)
            ml.eval(cmd)
            status_after_sim = 4
        except KeyboardInterrupt:
            self.logger.inf("[runSim]   Canceled nCloth simulation by keyboard button!!!", nl=True, nl_after=True)
            status_after_sim = 5
        except RuntimeError:     # TODO catch e
            status_after_sim = 6
        # for fr in range(int(ts), int(te)):
        #    cmd.currentTime(fr)
        #    cmd.refresh()
        return status_after_sim

        
    def maya_simulate_nhair(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_nparticle(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_fume(self, ts, te, fume_container, cache_dir):
        pass
        
    def maya_simulate_fumewt(self, ts, te, fume_container, cache_dir):
        pass
        
    def maya_render_blast(self, ts, te, out_file=""):
        self.logger.int(("maya_render_blast", ts, te, out_file))

        import maya.cmds as cmds
        import maya.mel as ml

        fr_start = self.comfun.int_or_val(ts, 0)
        fr_end = self.comfun.int_or_val(te, 0)
        cmds.playbackOptions(minTime=fr_start)
        cmds.playbackOptions(maxTime=fr_end)

        if len(out_file) > 0:
            # base_name = self.comfun.basename(out_file)
            # out_dir = self.comfun.dirname(out_file)
            # out_file_header = base_name.split(".")[0]
            # out_file_ext = base_name.split(".")[1]
            # print " [db] SimC Rend !   ",  out_dir,  out_file_header,  out_file_ext
            out_file = out_file.replace("####", "")
            out_file = out_file[:-5]
            self.logger.db((" render out file: ",  out_file))
            # cmds.playblast(f=outFile, st=int(ts), et=int(te), format='qt', compression='H.264', framePadding=4, percent=100, wh=[1920, 1080])
            cmds.playblast(f=out_file, st=int(ts), et=int(te), format='image', compression='jpg', framePadding=4,
                           percent=100, wh=[1280, 720])
        else:
            self.logger.err("var out_file is empty ")
        
    def maya_render_software(self, ts, te, out_file=""):
        self.logger.int(("maya_render_software", ts, te, out_file))
        
    def maya_script_py(self, file):
        self.logger.int(("maya_script_py", file))
        if self.comfun.file_exists(file):
            execfile(file)
        else:
            self.logger.wrn(("Script file not exist", file))
        
    def maya_script_mel(self, file):
        self.logger.int(("maya_script_mel", file))

    def maya_get_scene_objects(self):
        self.logger.int(("maya_get_scene_objects"))

    """   DEFAULTS   """

    def get_objects_by_type(self, type):
        if type == 'nCloth':
            objs = self.get_cloth_objects()
            self.logger.inf("Detected ({}) nCloth objects:".format(len(objs), objs))

        objs_str = ""
        for obj in objs:
            objs_str += obj + ","
        if len(objs_str) > 0:
            objs_str = objs_str[:-1]
        return objs_str

    def get_cloth_objects(self):
        import maya.cmds as cmd
        return cmd.ls(type='nCloth')

    def get_hair_objects(self):
        return "hair"

    def get_particle_objects(self):
        return "prt"

    def get_fume_container(self):
        return "fume"

    def import_camera(self):
        return "cam"
