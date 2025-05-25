import os
import sys
import definitions.interactions_base as interactions_base

class Interactions(interactions_base.BaseInteractions):
    current_os = -1
    logger = None
    comfun = None
    _bpy_available = False

    def __init__(self, current_os, logger, comfun):
        super().__init__(current_os, logger, comfun)
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun
        # Try to import bpy but don't fail if not available
        try:
            import bpy
            self._bpy_available = True
        except ImportError:
            self._bpy_available = False
            self.logger.wrn("Blender Python API (bpy) not available - some functionality will be limited")

    def print_info(self):
        self.logger.raw("This is interaction with Blender")

    def _check_bpy(self):
        """Check if bpy is available and raise appropriate error if not"""
        if not self._bpy_available:
            raise ImportError("Blender Python API (bpy) not available")

    # common interactions
    def schema_item_double_click(self, param):
        self.blender_open_file(param)

    def task_item_double_click(self, param):
        self.blender_open_file(param)

    def open_scene(self, param):
        """Open a scene file"""
        self.blender_open_file(param)

    def save_scene(self, param):
        """Save current scene"""
        self.save_current_scene_as(param)

    def save_scene_as_next_version(self, param):
        """Save current scene as next version"""
        self.save_current_scene_as(param)

    def set_param(self, objects, property, value):
        self.blender_set_param(objects, property, value)

    # blender interactions
    def blender_open_file(self, target):
        self.logger.int(("blender_open_file", target))
        try:
            self._check_bpy()
            import bpy
            
            if self.comfun.file_exists(target, info="(interactions blender_open_file)"):
                # Save and clear existing scene if it has changes
                if bpy.data.is_dirty:
                    self.logger.db("Scene has unsaved changes, will save before opening new file")
                    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
                
                # Load the new file
                bpy.ops.wm.open_mainfile(filepath=target)
                return True
            else:
                self.logger.err((" no file :", target))
                return False
        except ImportError:
            self.logger.err("Blender Python API (bpy) not available")
            return False
        except Exception as e:
            self.logger.err(f"Error opening Blender file: {str(e)}")
            return False

    def blender_save_file(self, file):
        self.logger.int(("blender_save_file", file))
        return self.save_current_scene_as(file)

    def save_current_scene_as(self, target_file):
        try:
            target_dir = self.comfun.dirname(target_file)
            self.logger.db((" target_dir: ", str(target_dir)))
            self.comfun.create_directory_if_not_exists(target_dir)
            
            bpy.ops.wm.save_as_mainfile(filepath=target_file)
            return True
        except Exception as e:
            self.logger.err(f"Error saving Blender file: {str(e)}")
            return False

    def blender_select_objects(self, objs):
        try:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            
            # Select objects by name
            selected_count = 0
            for obj_name in objs.split(","):
                obj_name = obj_name.strip()
                if obj_name in bpy.data.objects:
                    bpy.data.objects[obj_name].select_set(True)
                    selected_count += 1
            
            # Set active object if at least one was selected
            if selected_count > 0:
                # Set the last selected object as active
                for obj_name in objs.split(","):
                    obj_name = obj_name.strip()
                    if obj_name in bpy.data.objects:
                        bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
                        break
                return selected_count
            return False
        except Exception as e:
            self.logger.err(f"Error selecting objects in Blender: {str(e)}")
            return False

    def blender_get_selection(self):
        try:
            selected = [obj.name for obj in bpy.context.selected_objects]
            return selected
        except Exception as e:
            self.logger.err(f"Error getting selection in Blender: {str(e)}")
            return []
    
    def get_curent_scene_file(self):
        self.logger.int("get_curent_scene_file")
        try:
            # Get current .blend file path
            current_file = bpy.data.filepath
            
            if not current_file:
                self.logger.wrn("No current Blender scene file")
                return "", "", "", "blend"
                
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
            self.logger.err(f"Error getting current Blender scene file: {str(e)}")
            return "", "", "", "blend"
    
    def get_curent_frame_range(self):
        try:
            scene = bpy.context.scene
            return scene.frame_start, scene.frame_end
        except Exception as e:
            self.logger.err(f"Error getting frame range: {str(e)}")
            return 1, 250
    
    def blender_import_ani(self, objects, dir=""):
        self.logger.int(("blender_import_ani", objects, dir))
        try:
            # Implementation depends on animation format
            # For Alembic:
            if dir.endswith(".abc"):
                bpy.ops.wm.alembic_import(filepath=dir, as_background_job=False)
                return True
            # For MDD:
            elif dir.endswith(".mdd"):
                if objects and objects in bpy.data.objects:
                    bpy.context.view_layer.objects.active = bpy.data.objects[objects]
                    bpy.ops.object.modifier_add(type='MESH_SEQUENCE_CACHE')
                    bpy.ops.import_shape.mdd(filepath=dir)
                    return True
            return False
        except Exception as e:
            self.logger.err(f"Error importing animation: {str(e)}")
            return False
    
    def blender_import_cam(self, objects, file_or_dir):
        self.logger.int(("blender_import_cam", objects, file_or_dir))
        try:
            if file_or_dir.endswith(".fbx"):
                bpy.ops.import_scene.fbx(filepath=file_or_dir, use_custom_normals=True)
                return True
            elif file_or_dir.endswith(".abc"):
                bpy.ops.wm.alembic_import(filepath=file_or_dir)
                return True
            return False
        except Exception as e:
            self.logger.err(f"Error importing camera: {str(e)}")
            return False
    
    def blender_import_obj(self, objects, file_or_dir):
        self.logger.int(("blender_import_obj", objects, file_or_dir))
        try:
            if file_or_dir.endswith(".obj"):
                bpy.ops.import_scene.obj(filepath=file_or_dir)
                return True
            return False
        except Exception as e:
            self.logger.err(f"Error importing OBJ: {str(e)}")
            return False
            
    def blender_import_fbx(self, objects, file_or_dir):
        self.logger.int(("blender_import_fbx", objects, file_or_dir))
        try:
            if file_or_dir.endswith(".fbx"):
                bpy.ops.import_scene.fbx(filepath=file_or_dir)
                return True
            return False
        except Exception as e:
            self.logger.err(f"Error importing FBX: {str(e)}")
            return False
            
    def blender_import_alembic(self, objects, file_or_dir):
        self.logger.int(("blender_import_alembic", objects, file_or_dir))
        try:
            if file_or_dir.endswith(".abc"):
                bpy.ops.wm.alembic_import(filepath=file_or_dir)
                return True
            return False
        except Exception as e:
            self.logger.err(f"Error importing Alembic: {str(e)}")
            return False

    def blender_set_param(self, val, abbrev_param=None, value=None):
        try:
            # Parse expression string like "Cube.scale=2.0"
            str_expression = val
            parts = str_expression.split(".")
            if len(parts) < 2:
                self.logger.err(f"Invalid expression format: {str_expression}")
                return False
            
            obj_name = parts[0].strip()
            attr_value = parts[1].split("=")
            
            if len(attr_value) < 2:
                self.logger.err(f"Invalid expression format: {str_expression}")
                return False
            
            attr_name = attr_value[0].strip()
            attr_val = attr_value[1].strip()
            
            # Get the object
            if obj_name not in bpy.data.objects:
                self.logger.err(f"Object not found: {obj_name}")
                return False
            
            obj = bpy.data.objects[obj_name]
            
            # Handle common properties
            if hasattr(obj, attr_name):
                # Check property type and convert value
                prop = getattr(obj, attr_name)
                if isinstance(prop, float):
                    setattr(obj, attr_name, float(attr_val))
                elif isinstance(prop, int):
                    setattr(obj, attr_name, int(attr_val))
                elif isinstance(prop, bool):
                    setattr(obj, attr_name, bool(int(attr_val)))
                elif isinstance(prop, str):
                    setattr(obj, attr_name, attr_val)
                else:
                    # Handle vector properties (like location, scale)
                    if attr_name in ('location', 'scale', 'rotation_euler'):
                        # Assuming single axis value change like "Cube.location.x=5"
                        parts = attr_name.split('.')
                        if len(parts) > 1:
                            main_attr = parts[0]
                            sub_attr = parts[1]
                            
                            if main_attr in ('location', 'scale', 'rotation_euler'):
                                vec = getattr(obj, main_attr)
                                if sub_attr == 'x':
                                    vec[0] = float(attr_val)
                                elif sub_attr == 'y':
                                    vec[1] = float(attr_val)
                                elif sub_attr == 'z':
                                    vec[2] = float(attr_val)
                        else:
                            self.logger.err(f"Unable to set vector property: {attr_name}")
                            return False
            else:
                self.logger.err(f"Property not found: {attr_name} on object {obj_name}")
                return False
            
            return True
        except Exception as e:
            self.logger.err(f"Error setting parameter: {str(e)}")
            return False

    def blender_simulate_cloth(self, ts, te, objects_names, cache_dir, cache_mode=1, cache_subsamples=1):
        try:
            # Set frame range if provided
            if ts != "0" and te != "0":
                bpy.context.scene.frame_start = int(ts)
                bpy.context.scene.frame_end = int(te)
            else:
                ts = bpy.context.scene.frame_start
                te = bpy.context.scene.frame_end
                self.logger.int(("Using scene frame range", ts, te))
                
            self.logger.int(("blender_simulate_cloth", ts, te, objects_names, cache_dir))
            
            # Create cache directory if it doesn't exist
            if not self.comfun.path_exists(cache_dir):
                self.comfun.create_directory(cache_dir)
                
            # Get cloth objects if not specified
            if not objects_names or objects_names == "<cloth_objects>":
                objects_list = self.get_cloth_objects()
                if objects_list:
                    objects_names = ",".join(objects_list)
                else:
                    self.logger.err("No cloth objects found")
                    return False
                
            # Select objects
            self.blender_select_objects(objects_names)
            
            # Make sure each object has a cloth modifier
            for obj_name in objects_names.split(","):
                obj_name = obj_name.strip()
                if obj_name in bpy.data.objects:
                    obj = bpy.data.objects[obj_name]
                    
                    # Check for existing cloth modifier
                    cloth_mod = None
                    for mod in obj.modifiers:
                        if mod.type == 'CLOTH':
                            cloth_mod = mod
                            break
                    
                    # Add cloth modifier if not present
                    if not cloth_mod:
                        cloth_mod = obj.modifiers.new(name="SimBatchCloth", type='CLOTH')
                    
                    # Set up caching
                    cloth_mod.point_cache.frame_start = int(ts)
                    cloth_mod.point_cache.frame_end = int(te)
                    
                    # Set cache directory if different from default
                    cloth_mod.point_cache.use_external = True
                    cache_name = f"cloth_cache_{obj_name}"
                    cloth_mod.point_cache.filepath = os.path.join(cache_dir, cache_name)
                    
                    # Set quality based on cache_subsamples
                    cloth_mod.settings.quality = max(1, cache_subsamples * 5)
                    
            # Bake the simulation
            bpy.ops.ptcache.bake_all(bake=True)
            
            return True
        except Exception as e:
            self.logger.err(f"Error in cloth simulation: {str(e)}")
            return False

    def blender_simulate_fluid(self, ts, te, objects_names, cache_dir):
        self.logger.int(("blender_simulate_fluid", ts, te, objects_names, cache_dir))
        # Implement fluid simulation setup
        return False
        
    def blender_simulate_particles(self, ts, te, objects_names, cache_dir):
        self.logger.int(("blender_simulate_particles", ts, te, objects_names, cache_dir))
        # Implement particle simulation setup
        return False
        
    def blender_simulate_rigid(self, ts, te, objects_names, cache_dir):
        self.logger.int(("blender_simulate_rigid", ts, te, objects_names, cache_dir))
        # Implement rigid body simulation setup
        return False

    def blender_render_viewport(self, ts, te, out_file=""):
        try:
            # Set frame range
            if ts != "0" and te != "0":
                start_frame = int(ts)
                end_frame = int(te)
            else:
                start_frame = bpy.context.scene.frame_start
                end_frame = bpy.context.scene.frame_end
                
            self.logger.int(("blender_render_viewport", start_frame, end_frame, out_file))
            
            # Ensure output directory exists
            out_dir = os.path.dirname(out_file)
            if not self.comfun.path_exists(out_dir):
                self.comfun.create_directory(out_dir)
                
            # Set output path
            if out_file:
                bpy.context.scene.render.filepath = out_file
                
            # Configure for OpenGL render
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            
            # Render frames
            original_frame = bpy.context.scene.frame_current
            for frame in range(start_frame, end_frame + 1):
                bpy.context.scene.frame_set(frame)
                bpy.ops.render.opengl(write_still=True, view_context=True)
                
            # Reset frame
            bpy.context.scene.frame_set(original_frame)
            
            return True
        except Exception as e:
            self.logger.err(f"Error rendering viewport: {str(e)}")
            return False

    def blender_render_cycles(self, ts, te, out_file=""):
        try:
            # Set frame range
            if ts != "0" and te != "0":
                start_frame = int(ts)
                end_frame = int(te)
            else:
                start_frame = bpy.context.scene.frame_start
                end_frame = bpy.context.scene.frame_end
                
            self.logger.int(("blender_render_cycles", start_frame, end_frame, out_file))
            
            # Ensure output directory exists
            out_dir = os.path.dirname(out_file)
            if not self.comfun.path_exists(out_dir):
                self.comfun.create_directory(out_dir)
                
            # Set output path
            if out_file:
                bpy.context.scene.render.filepath = out_file
                
            # Configure for Cycles render
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            
            # Set frame range
            bpy.context.scene.frame_start = start_frame
            bpy.context.scene.frame_end = end_frame
            
            # Render animation
            bpy.ops.render.render(animation=True)
            
            return True
        except Exception as e:
            self.logger.err(f"Error rendering with Cycles: {str(e)}")
            return False
            
    def blender_render_eevee(self, ts, te, out_file=""):
        try:
            # Set frame range
            if ts != "0" and te != "0":
                start_frame = int(ts)
                end_frame = int(te)
            else:
                start_frame = bpy.context.scene.frame_start
                end_frame = bpy.context.scene.frame_end
                
            self.logger.int(("blender_render_eevee", start_frame, end_frame, out_file))
            
            # Ensure output directory exists
            out_dir = os.path.dirname(out_file)
            if not self.comfun.path_exists(out_dir):
                self.comfun.create_directory(out_dir)
                
            # Set output path
            if out_file:
                bpy.context.scene.render.filepath = out_file
                
            # Configure for Eevee render
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            
            # Set frame range
            bpy.context.scene.frame_start = start_frame
            bpy.context.scene.frame_end = end_frame
            
            # Render animation
            bpy.ops.render.render(animation=True)
            
            return True
        except Exception as e:
            self.logger.err(f"Error rendering with Eevee: {str(e)}")
            return False

    def blender_script_py(self, file):
        self.logger.int(("blender_script_py", file))
        try:
            if self.comfun.file_exists(file, "(interactions blender_script_py)"):
                with open(file, 'r', encoding='utf-8') as f:
                    script_content = f.read()
                    
                # Execute the script in Blender's Python environment
                exec(script_content)
                return True
            else:
                self.logger.err(f"Script file not found: {file}")
                return False
        except Exception as e:
            self.logger.err(f"Error executing Python script: {str(e)}")
            return False

    def get_cloth_objects(self):
        try:
            cloth_objects = []
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for mod in obj.modifiers:
                        if mod.type == 'CLOTH':
                            cloth_objects.append(obj.name)
                            break
            return cloth_objects
        except Exception as e:
            self.logger.err(f"Error getting cloth objects: {str(e)}")
            return []
            
    def get_fluid_objects(self):
        try:
            fluid_objects = []
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for mod in obj.modifiers:
                        if mod.type == 'FLUID':
                            fluid_objects.append(obj.name)
                            break
            return fluid_objects
        except Exception as e:
            self.logger.err(f"Error getting fluid objects: {str(e)}")
            return []
            
    def get_particle_objects(self):
        try:
            particle_objects = []
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    if obj.particle_systems:
                        particle_objects.append(obj.name)
            return particle_objects
        except Exception as e:
            self.logger.err(f"Error getting particle objects: {str(e)}")
            return []
            
    def get_rigid_objects(self):
        try:
            rigid_objects = []
            for obj in bpy.data.objects:
                if obj.rigid_body:
                    rigid_objects.append(obj.name)
            return rigid_objects
        except Exception as e:
            self.logger.err(f"Error getting rigid body objects: {str(e)}")
            return [] 