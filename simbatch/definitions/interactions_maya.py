import sys
import os

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
            if self.comfun.file_exists(target, info="(interactions maya_open_scene)"):
                ret = cmd.file(target, o=True, force=True)
            else:
                self.logger.err((" no file :", target))
                ret = False
            return ret
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")

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

    def maya_select_objects(self, objs):
        import maya.cmds as cmds
        cmds.select(cl=True)
        for obj in objs.split(","):
            if cmds.objExists(obj):
                cmds.select(obj, tgl=True)

        selected_count = len(cmds.ls(sl=True))
        if selected_count == 0:
            return False
        else:
            return selected_count

    def maya_get_selection(self):
        import maya.cmds as cmds
        sel = cmds.ls(selection=True)
        return sel
        
    def maya_get_camera(self):
        print("TODO: maya_get_camera")
        pass
    
    def get_curent_scene_file(self):
        self.logger.int("get_curent_scene_file")
        import maya.cmds as cmds
        fi = cmds.file(query=True, sceneName=True)
        if self.current_os == 2:
            fi = fi.replace('/', '\\')
        basename = os.path.basename(fi)
        out_dir = fi[:-1*len(basename)]
        out_file_header = basename.split(".")[0]
        out_file_ext = basename.split(".")[1]
        return out_dir, basename, out_file_header, out_file_ext
    
    def get_curent_frame_range(self):
        import maya.cmds as cmds
        playback_min = cmds.playbackOptions(query=True, minTime=True)
        playback_max = cmds.playbackOptions(query=True, maxTime=True)
        return playback_min, playback_max
        
    def maya_import_ani(self, objects, dir=""):
        self.logger.int(("maya_import_ani", objects, dir))
        
    def maya_import_cam(self, objects, file_or_dir):
        self.logger.int(("maya_import_cam", objects, file_or_dir))
        
    def maya_import_obj(self, objects, file_or_dir):
        self.logger.int(("maya_import_obj", objects, file_or_dir))

    def maya_set_param(self, val, abbrev_param=None, value=None):
        if abbrev_param is None:
            str_expression = val             # first input as expression string  # TODO
            a1 = str_expression.split(".")
            a2 = a1[1].split("=")
            str_obj = a1[0].strip()
            str_attrib = a2[0].strip()
            str_val = a2[1].strip()
            try:
                import maya.cmds as cmds
                cmds.setAttr(f"{str_obj}.{str_attrib}", float(str_val))   # TODO check vals !!!
            except Exception as e:
                self.logger.err(("maya_set_param: ", str_obj, str_attrib, str_val, "   ___   ", str_expression))
                self.logger.err(("maya_set_param e: ", e))
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

            import maya.cmds as cmds
            for obj in objects.split(","):
                param_full_name = abbrev_param
                cmds.setAttr(f"{obj}.{param_full_name}", value)
            self.logger.db(("maya_set_param", object, property, value), nl=True)

    def maya_animate_nucleus_follow(self, nucleus_name, object_to_follow, vtx_id_to_follow=None, vals=None):
        import maya.cmds as cmds

        if vtx_id_to_follow is None:
            vtx_id_to_follow = 1     # TODO get vtx close to center
        if vals is None:
            vals = ((self.simFrameStart, 1), (self.animFrameStart, 1), (self.simFrameEnd, 0))

        if cmds.objExists(nucleus_name):
            if cmds.objExists(object_to_follow):
                if len(vals) == 0:
                    # TODO val err
                    pass
                elif len(vals) == 1:
                    cmds.setAttr("nucleus1.enable", 0)
                    for fr in range(cmds.playbackOptions(min=True, q=True), vals[0][0]):
                        cmds.currentTime(fr)
                        vtx_pos = cmds.pointPosition(f"{object_to_follow}.vtx[{vtx_id_to_follow}]", w=True)
                        cmds.setKeyframe(nucleus_name, attribute='translateX', t=fr, v=vtx_pos[0])
                        cmds.setKeyframe(nucleus_name, attribute='translateY', t=fr, v=vtx_pos[1])
                        cmds.setKeyframe(nucleus_name, attribute='translateZ', t=fr, v=vtx_pos[2])

                    cmds.setAttr("nucleus1.enable", 1)
                    # frs =
                    # fre = cmds.playbackOptions(max=True, q=True)
                else:
                    cmds.setAttr("nucleus1.enable", 0)
                    nucleus_base_pos = cmds.getAttr("nucleus1.translate")[0]
                    for i, v in enumerate(vals):
                        if i == 0:
                            val_from = v
                        else:
                            val_to = v
                            for fr in range(val_from[0], val_to[0]):
                                cmds.currentTime(fr)
                                vtx_pos = cmds.pointPosition(f"{object_to_follow}.vtx[{vtx_id_to_follow}]", w=True)

                                fr_min = val_from[0]
                                fr_max = val_to[0]

                                val_in_min = val_from[1]
                                val_in_max = val_to[1]

                                current_frame = fr
                                curent_multiper = val_in_min - 1.0 * (val_in_min - val_in_max) * 1.0 * (current_frame - fr_min) / (fr_max - fr_min)
                                # print fr, curent_multiper

                                # simpler: vtx_pos*curent_multiper + nucleus_base_pos*(1-curent_multiper)
                                med_x = vtx_pos[0]*curent_multiper+nucleus_base_pos[0]*(1-curent_multiper)
                                med_y = vtx_pos[1]*curent_multiper+nucleus_base_pos[1]*(1-curent_multiper)
                                med_z = vtx_pos[2]*curent_multiper+nucleus_base_pos[2]*(1-curent_multiper)
                                current_pos = [med_x, med_y, med_z]

                                if curent_multiper == 1.0:
                                    nucleus_base_pos = vtx_pos
                                cmds.setKeyframe(nucleus_name, attribute='translateX', t=fr, v=current_pos[0])
                                cmds.setKeyframe(nucleus_name, attribute='translateY', t=fr, v=current_pos[1])
                                cmds.setKeyframe(nucleus_name, attribute='translateZ', t=fr, v=current_pos[2])
                            val_from = v

                    cmds.setAttr("nucleus1.enable", 1)

                return True

            # TODO else err
        # TODO else err

        return False

    def maya_simulate_ncloth(self, ts, te, objects_names, cache_dir, cache_mode=1, cache_subsamples=1):
        import maya.cmds as cmds
        import maya.mel as ml

        if ts == "0" and te == "0":
            ts = cmds.playbackOptions(query=True, minTime=True)
            te = cmds.playbackOptions(query=True, maxTime=True)
            self.logger.int(("force simulate range from scene", ts, te))

        self.logger.int(("maya_simulate_ncloth", ts, te, objects_names, cache_dir))

        if self.comfun.path_exists(cache_dir) is False:
            self.comfun.create_directory(cache_dir)

        if len(objects_names) == 0 or objects_names == "<cloth_objects>":
            ret = self.get_cloth_objects()
            if len(ret) > 0:
                objects_names = ",".join(ret)

        if cache_mode == 1:
            pc_mode = "OneFile"
        if cache_mode == 2:
            pc_mode = "OneFilePerFrame"

        fr_start = self.comfun.int_or_val(ts, 0)
        fr_end = self.comfun.int_or_val(te, 0)
        cmds.playbackOptions(minTime=fr_start)
        cmds.playbackOptions(maxTime=fr_end)
        try:
            cmd = f'select -r {objects_names.replace(",", " ")}'    #  TODO ' ; viewFit;'
            self.logger.inf(cmd, nl=True, nl_after=True)
            ml.eval(cmd)
            self.logger.int(("selected:", len(cmds.ls(sl=True))), nl=True)

            cache_dir = cache_dir.replace("\\", "/")

            self.logger.int(("cache_dir:", cache_dir), nl=True)

            refresh_view = "1"    # TODO 0 for batch mode !!!
            cache_per_geo = "1"    # TODO do user option !!!

            # add, replace, merge or mergeDelete

            # maya 2015  # TODO !!!
            cmd = 'doCreateNclothCache 4 {"2", "1", "10", "' + pc_mode + '", "'+refresh_view+'", "' + cache_dir + '",'
            cmd += ' "'+cache_per_geo+'", "", "0", "replace", "1", "' + str(cache_subsamples) + '", "1","0","1" } ;'

            # maya 2018
            cmd = 'doCreateNclothCache 5 {"2", "1", "10", "' + pc_mode + '", "'+refresh_view+'", "' + cache_dir + '",'
            cmd += ' "'+cache_per_geo+'", "", "0", "replace", "1", "' + str(cache_subsamples) + '", "1", "0", "1", "mcx"};'

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
        import maya.cmds as cmds
        import maya.mel as ml
        if ts == "0" and te == "0":
            ts = cmds.playbackOptions(query=True, minTime=True)
            te = cmds.playbackOptions(query=True, maxTime=True)
            self.logger.int(("force playblast range from scene", ts, te))

        self.logger.int(("maya_render_blast", ts, te, out_file))


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
            out_file = out_file.replace("<fr>", "####")

            out_file = out_file.replace("####", "")   # TODO !!!
            out_file = out_file[:-5]
            self.logger.db((" render out file: ",  out_file))
            # cmds.playblast(f=outFile, st=int(ts), et=int(te), format='qt', compression='H.264', framePadding=4, percent=100, wh=[1920, 1080])
            cmds.playblast(f=out_file, st=int(ts), et=int(te), format='image', compression='jpg', framePadding=4,
                           percent=100, wh=[1280, 720], v=False)
        else:
            self.logger.err("var out_file is empty ")
        
    def maya_render_software(self, ts, te, out_file=""):
        self.logger.int(("maya_render_software", ts, te, out_file))
        
    def maya_script_py(self, file):
        self.logger.int(("maya_script_py file:", file))
        filearr = file.split(" ")
        file = filearr.pop(0)
        if self.comfun.file_exists(file):
            import sys
            if len(filearr) > 0:
                sys.argv = filearr
            with open(file, 'r') as f:
                exec(f.read())
        else:
            self.logger.err(("Script file not exist", file))
        
    def maya_script_mel(self, file):
        self.logger.int(("maya_script_mel", file))

    def maya_get_scene_objects(self):
        self.logger.int(("maya_get_scene_objects"))

    """   DEFAULTS   """

    def get_objects_by_type(self, type):
        if type == 'nCloth':
            objs = self.get_cloth_objects()
            self.logger.inf(f"Detected ({len(objs)}) nCloth objects: {objs}")

        objs_str = ""
        for obj in objs:
            objs_str += obj + ","
        if len(objs_str) > 0:
            objs_str = objs_str[:-1]
        return objs_str

    def get_cloth_objects(self):
        try:
            import maya.cmds as cmd
            return cmd.ls(type='nCloth')
        except Exception as e:
            self.logger.err(e)
            return []

    def get_hair_objects(self):
        return "hair"

    def get_particle_objects(self):
        return "prt"

    def get_fume_container(self):
        return "fume"

    def import_camera(self):
        return "cam"
