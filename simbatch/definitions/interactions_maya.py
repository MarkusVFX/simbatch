import sys
import os
import definitions.interactions_base as interactions_base

class Interactions(interactions_base.BaseInteractions):
    current_os = -1
    logger = None
    comfun = None
    _maya_available = False
    cmds = None

    def __init__(self, current_os, logger, comfun):
        super().__init__(current_os, logger, comfun)
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun
        
        # Try to import maya but don't fail if not available
        try:
            import maya.cmds as cmds
            self._maya_available = True
            self.cmds = cmds
        except ImportError:
            self._maya_available = False
            self.cmds = None
            self.logger.wrn("Maya Python API not available - some functionality will be limited")

    def print_info(self):
        self.logger.raw("This is interaction with Maya")

    def _check_maya(self):
        """Check if maya is available and raise appropriate error if not"""
        if not self._maya_available:
            raise ImportError("Maya Python API not available")

    # common interactions
    def schema_item_double_click(self, param):
        self.maya_open_scene(param)

    def task_item_double_click(self, param):
        self.maya_open_scene(param)

    def open_scene(self, param):
        """Open a scene file"""
        self.maya_open_file(param)

    def save_scene(self, param):
        """Save current scene"""
        self.maya_save_scene(param)

    def save_scene_as_next_version(self, param):
        """Save current scene as next version"""
        self.maya_save_scene_as_next_version(param)

    def set_param(self, objects, property, value):
        self.maya_set_param(objects, property, value)

    # maya interactions
    def maya_open_scene(self, target):
        self.logger.int(("maya_open_scene", target))
        try:
            self._check_maya()
            if self.comfun.file_exists(target, info="(interactions maya_open_scene)"):
                ret = self.cmds.file(target, o=True, force=True)
            else:
                self.logger.err((" no file :", target))
                ret = False
            return ret
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error opening Maya file: {str(e)}")
            return False

    def maya_save_scene(self, file):
        self.logger.int(("maya_save_scene", file))
        return self.save_current_scene_as(file)

    def save_current_scene_as(self, target_file):
        try:
            self._check_maya()
            target_dir = self.comfun.dirname(target_file)
            self.logger.db((" target_dir: ", str(target_dir)))
            self.comfun.create_directory_if_not_exists(target_dir)
            if self.comfun.path_exists(target_dir):
                self.comfun.create_directory(target_dir)
            self.cmds.file(rename=target_file)
            ret = self.cmds.file(save=True, type="mayaBinary")
            return ret
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error saving Maya file: {str(e)}")
            return False

    def maya_select_objects(self, objs):
        try:
            self._check_maya()
            self.cmds.select(cl=True)
            for obj in objs.split(","):
                if self.cmds.objExists(obj):
                    self.cmds.select(obj, tgl=True)

            selected_count = len(self.cmds.ls(sl=True))
            if selected_count == 0:
                return False
            else:
                return selected_count
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error selecting objects in Maya: {str(e)}")
            return False

    def maya_get_selection(self):
        try:
            self._check_maya()
            sel = self.cmds.ls(selection=True)
            return sel
        except ImportError:
            self.logger.err("Maya Python API not available")
            return []
        except Exception as e:
            self.logger.err(f"Error getting selection in Maya: {str(e)}")
            return []

    def get_curent_scene_file(self):
        """Get the current Maya scene file path and info.
        
        Returns:
            tuple: (directory, filename, filename_without_ext, extension)
        """
        try:
            self._check_maya()
            # Get current .ma/.mb file path
            current_file = self.cmds.file(query=True, sceneName=True)
            
            if not current_file:
                self.logger.wrn("No current Maya scene file")
                return "", "", "", "mb"
                
            # Convert path separators for Windows if needed
            if self.current_os == 2:  # Windows
                current_file = current_file.replace('/', '\\')
            
            # Split path into components
            directory = os.path.dirname(current_file)
            filename = os.path.basename(current_file)
            filename_without_ext = os.path.splitext(filename)[0]
            extension = os.path.splitext(filename)[1].lstrip('.')
            
            return directory, filename, filename_without_ext, extension
            
        except ImportError:
            self.logger.err("Maya Python API not available")
            return "", "", "", "mb"
        except Exception as e:
            self.logger.err(f"Error getting current Maya scene file: {str(e)}")
            return "", "", "", "mb"

    def get_curent_frame_range(self):
        try:
            self._check_maya()
            playback_min = self.cmds.playbackOptions(query=True, minTime=True)
            playback_max = self.cmds.playbackOptions(query=True, maxTime=True)
            return playback_min, playback_max
        except ImportError:
            self.logger.err("Maya Python API not available")
            return 1, 250
        except Exception as e:
            self.logger.err(f"Error getting frame range in Maya: {str(e)}")
            return 1, 250

    def maya_set_param(self, val, abbrev_param=None, value=None):
        try:
            self._check_maya()
            if abbrev_param is None:
                str_expression = val
                a1 = str_expression.split(".")
                a2 = a1[1].split("=")
                str_obj = a1[0].strip()
                str_attrib = a2[0].strip()
                str_val = a2[1].strip()
                try:
                    self.cmds.setAttr(f"{str_obj}.{str_attrib}", float(str_val))
                except Exception as e:
                    self.logger.err(("maya_set_param: ", str_obj, str_attrib, str_val, "   ___   ", str_expression))
                    self.logger.err(("maya_set_param e: ", e))
            else:
                objects = val

                if not objects:
                    ret = self.get_cloth_objects()
                    if ret:
                        objects = ",".join(ret)

                if objects == "<cloth_objects>":
                    ret = self.get_cloth_objects()
                    if ret:
                        objects = ",".join(ret)

                self.cmds.setAttr(f"{obj}.{param_full_name}", value)
                self.logger.db(("maya_set_param", object, property, value), nl=True)
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error setting parameter in Maya: {str(e)}")
            return False

    def maya_get_camera(self):
        print("TODO: maya_get_camera")
        pass
    
    def maya_import_ani(self, objects, dir=""):
        self.logger.int(("maya_import_ani", objects, dir))
        
    def maya_import_cam(self, objects, file_or_dir):
        self.logger.int(("maya_import_cam", objects, file_or_dir))
        
    def maya_import_obj(self, objects, file_or_dir):
        self.logger.int(("maya_import_obj", objects, file_or_dir))

    def maya_animate_nucleus_follow(self, nucleus_name, object_to_follow, vtx_id_to_follow=None, vals=None):
        try:
            self._check_maya()
            if vtx_id_to_follow is None:
                vtx_id_to_follow = 1     # TODO get vtx close to center
            if vals is None:
                vals = ((self.simFrameStart, 1), (self.animFrameStart, 1), (self.simFrameEnd, 0))

            if self.cmds.objExists(nucleus_name):
                if self.cmds.objExists(object_to_follow):
                    if len(vals) == 0:
                        # TODO val err
                        pass
                    elif len(vals) == 1:
                        self.cmds.setAttr("nucleus1.enable", 0)
                        for fr in range(self.cmds.playbackOptions(min=True, q=True), vals[0][0]):
                            self.cmds.currentTime(fr)
                            vtx_pos = self.cmds.pointPosition(f"{object_to_follow}.vtx[{vtx_id_to_follow}]", w=True)
                            self.cmds.setKeyframe(nucleus_name, attribute='translateX', t=fr, v=vtx_pos[0])
                            self.cmds.setKeyframe(nucleus_name, attribute='translateY', t=fr, v=vtx_pos[1])
                            self.cmds.setKeyframe(nucleus_name, attribute='translateZ', t=fr, v=vtx_pos[2])

                        self.cmds.setAttr("nucleus1.enable", 1)
                    else:
                        self.cmds.setAttr("nucleus1.enable", 0)
                        nucleus_base_pos = self.cmds.getAttr("nucleus1.translate")[0]
                        for i, v in enumerate(vals):
                            if i == 0:
                                val_from = v
                            else:
                                val_to = v
                                for fr in range(val_from[0], val_to[0]):
                                    self.cmds.currentTime(fr)
                                    vtx_pos = self.cmds.pointPosition(f"{object_to_follow}.vtx[{vtx_id_to_follow}]", w=True)

                                    fr_min = val_from[0]
                                    fr_max = val_to[0]

                                    val_in_min = val_from[1]
                                    val_in_max = val_to[1]

                                    current_frame = fr
                                    curent_multiper = val_in_min - 1.0 * (val_in_min - val_in_max) * 1.0 * (current_frame - fr_min) / (fr_max - fr_min)

                                    med_x = vtx_pos[0]*curent_multiper+nucleus_base_pos[0]*(1-curent_multiper)
                                    med_y = vtx_pos[1]*curent_multiper+nucleus_base_pos[1]*(1-curent_multiper)
                                    med_z = vtx_pos[2]*curent_multiper+nucleus_base_pos[2]*(1-curent_multiper)
                                    current_pos = [med_x, med_y, med_z]

                                    if curent_multiper == 1.0:
                                        nucleus_base_pos = vtx_pos
                                    self.cmds.setKeyframe(nucleus_name, attribute='translateX', t=fr, v=current_pos[0])
                                    self.cmds.setKeyframe(nucleus_name, attribute='translateY', t=fr, v=current_pos[1])
                                    self.cmds.setKeyframe(nucleus_name, attribute='translateZ', t=fr, v=current_pos[2])
                                val_from = v

                        self.cmds.setAttr("nucleus1.enable", 1)

                    return True
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in nucleus follow animation: {str(e)}")
            return False

    def maya_simulate_ncloth(self, ts, te, objects_names, cache_dir, cache_mode=1, cache_subsamples=1):
        try:
            self._check_maya()
            import maya.mel as ml

            if ts == "0" and te == "0":
                ts = self.cmds.playbackOptions(query=True, minTime=True)
                te = self.cmds.playbackOptions(query=True, maxTime=True)
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
            self.cmds.playbackOptions(minTime=fr_start)
            self.cmds.playbackOptions(maxTime=fr_end)
            try:
                cmd = f'select -r {objects_names.replace(",", " ")}'
                self.logger.inf(cmd, nl=True, nl_after=True)
                ml.eval(cmd)
                self.logger.int(("selected:", len(self.cmds.ls(sl=True))), nl=True)

                cache_dir = cache_dir.replace("\\", "/")

                self.logger.int(("cache_dir:", cache_dir), nl=True)

                refresh_view = "1"
                cache_per_geo = "1"

                cmd = 'doCreateNclothCache 5 {"2", "1", "10", "' + pc_mode + '", "'+refresh_view+'", "' + cache_dir + '",'
                cmd += ' "'+cache_per_geo+'", "", "0", "replace", "1", "' + str(cache_subsamples) + '", "1", "0", "1", "mcx"};'

                self.logger.inf(cmd, nl=True, nl_after=True)
                ml.eval(cmd)
                status_after_sim = 4
            except KeyboardInterrupt:
                self.logger.inf("[runSim]   Canceled nCloth simulation by keyboard button!!!", nl=True, nl_after=True)
                status_after_sim = 5
            except RuntimeError:
                status_after_sim = 6
            return status_after_sim
        except ImportError:
            self.logger.err("Maya Python API not available")
            return 0
        except Exception as e:
            self.logger.err(f"Error in nCloth simulation: {str(e)}")
            return 0
        
    def maya_simulate_nhair(self, ts, te, objects_names, cache_dir):
        try:
            self._check_maya()
            pass
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in nHair simulation: {str(e)}")
            return False
        
    def maya_simulate_nparticle(self, ts, te, objects_names, cache_dir):
        try:
            self._check_maya()
            pass
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in nParticle simulation: {str(e)}")
            return False
        
    def maya_simulate_fume(self, ts, te, fume_container, cache_dir):
        try:
            self._check_maya()
            pass
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in fume simulation: {str(e)}")
            return False
        
    def maya_simulate_fumewt(self, ts, te, fume_container, cache_dir):
        try:
            self._check_maya()
            pass
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in fume with time simulation: {str(e)}")
            return False
        
    def maya_render_blast(self, ts, te, out_file=""):
        try:
            self._check_maya()
            import maya.mel as ml
            if ts == "0" and te == "0":
                ts = self.cmds.playbackOptions(query=True, minTime=True)
                te = self.cmds.playbackOptions(query=True, maxTime=True)
                self.logger.int(("force playblast range from scene", ts, te))

            self.logger.int(("maya_render_blast", ts, te, out_file))

            fr_start = self.comfun.int_or_val(ts, 0)
            fr_end = self.comfun.int_or_val(te, 0)
            self.cmds.playbackOptions(minTime=fr_start)
            self.cmds.playbackOptions(maxTime=fr_end)

            if len(out_file) > 0:
                out_file = out_file.replace("<fr>", "####")
                out_file = out_file.replace("####", "")
                out_file = out_file[:-5]
                self.logger.db((" render out file: ",  out_file))
                self.cmds.playblast(f=out_file, st=int(ts), et=int(te), format='image', compression='jpg', framePadding=4,
                               percent=100, wh=[1280, 720], v=False)
            else:
                self.logger.err("var out_file is empty ")
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in playblast render: {str(e)}")
            return False
        
    def maya_render_software(self, ts, te, out_file=""):
        try:
            self._check_maya()
            self.logger.int(("maya_render_software", ts, te, out_file))
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in software render: {str(e)}")
            return False
        
    def maya_script_py(self, file):
        try:
            self._check_maya()
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
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error running Python script: {str(e)}")
            return False
        
    def maya_script_mel(self, file):
        try:
            self._check_maya()
            import maya.mel as ml
            self.logger.int(("maya_script_mel", file))
            if self.comfun.file_exists(file):
                ml.eval(f'source "{file}";')
            else:
                self.logger.err(("Script file not exist", file))
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error running MEL script: {str(e)}")
            return False

    def maya_get_scene_objects(self):
        try:
            self._check_maya()
            self.logger.int(("maya_get_scene_objects"))
            return self.cmds.ls()
        except ImportError:
            self.logger.err("Maya Python API not available")
            return []
        except Exception as e:
            self.logger.err(f"Error getting scene objects: {str(e)}")
            return []

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
            self._check_maya()
            return self.cmds.ls(type='nCloth')
        except ImportError:
            self.logger.err("Maya Python API not available")
            return []
        except Exception as e:
            self.logger.err(f"Error getting cloth objects in Maya: {str(e)}")
            return []

    def get_hair_objects(self):
        try:
            self._check_maya()
            return "hair"
        except ImportError:
            self.logger.err("Maya Python API not available")
            return []
        except Exception as e:
            self.logger.err(f"Error getting hair objects in Maya: {str(e)}")
            return []

    def get_particle_objects(self):
        try:
            self._check_maya()
            return "prt"
        except ImportError:
            self.logger.err("Maya Python API not available")
            return []
        except Exception as e:
            self.logger.err(f"Error getting particle objects in Maya: {str(e)}")
            return []

    def get_fume_container(self):
        try:
            self._check_maya()
            return "fume"
        except ImportError:
            self.logger.err("Maya Python API not available")
            return []
        except Exception as e:
            self.logger.err(f"Error getting fume container in Maya: {str(e)}")
            return []

    def import_camera(self):
        try:
            self._check_maya()
            return "cam"
        except ImportError:
            self.logger.err("Maya Python API not available")
            return ""
        except Exception as e:
            self.logger.err(f"Error importing camera in Maya: {str(e)}")
            return ""

    def maya_import_file(self, file_name):
        try:
            self._check_maya()
            if self.comfun.file_exists(file_name):
                self.cmds.file(file_name, i=True)
                return True
            else:
                self.logger.err(f"File does not exist: {file_name}")
                return False
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error importing file: {str(e)}")
            return False

    def maya_simulate(self, ts, te, objects_names, cache_dir):
        try:
            self._check_maya()
            pass
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in simulation: {str(e)}")
            return False

    def maya_render(self, ts, te, out_file=""):
        try:
            self._check_maya()
            pass
        except ImportError:
            self.logger.err("Maya Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error in render: {str(e)}")
            return False
