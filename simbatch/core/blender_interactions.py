import os
import sys
import bpy
import mathutils


class Interactions:
    """
    Interactions class for Blender operations.
    Provides methods to interact with Blender through Python API.
    """
    
    def __init__(self, comfun, logger=None):
        """
        Initialize the Interactions class for Blender.
        
        Args:
            comfun: Common functions module
            logger: Logger instance for logging operations
        """
        self.os_name = os.name
        self.logger = logger
        self.comfun = comfun
        
    def blender_open_file(self, file_path):
        """
        Open a Blender file.
        
        Args:
            file_path (str): Path to the Blender file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                bpy.ops.wm.open_mainfile(filepath=file_path)
                if self.logger:
                    self.logger.info(f"Opened Blender file: {file_path}")
                return True
            else:
                if self.logger:
                    self.logger.error(f"File not found: {file_path}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error opening Blender file: {str(e)}")
            return False
            
    def blender_save_file(self, file_path):
        """
        Save current Blender scene to a file.
        
        Args:
            file_path (str): Path to save the Blender file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            bpy.ops.wm.save_as_mainfile(filepath=file_path)
            if self.logger:
                self.logger.info(f"Saved Blender file to: {file_path}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error saving Blender file: {str(e)}")
            return False
            
    def blender_select_objects(self, object_names=None):
        """
        Select objects in the Blender scene.
        
        Args:
            object_names (list, optional): List of object names to select. If None, selects all objects.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Deselect all objects first
            bpy.ops.object.select_all(action='DESELECT')
            
            if object_names is None:
                # Select all objects
                bpy.ops.object.select_all(action='SELECT')
            else:
                # Select specified objects
                for name in object_names:
                    if name in bpy.data.objects:
                        bpy.data.objects[name].select_set(True)
                    else:
                        if self.logger:
                            self.logger.warning(f"Object not found: {name}")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error selecting objects: {str(e)}")
            return False
            
    def blender_get_selection(self):
        """
        Get currently selected objects in the Blender scene.
        
        Returns:
            list: List of selected object names
        """
        try:
            return [obj.name for obj in bpy.context.selected_objects]
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting selection: {str(e)}")
            return []
            
    def blender_get_current_scene_file(self):
        """
        Get the path to the current Blender scene file.
        
        Returns:
            str: Path to the current scene file or empty string if not saved
        """
        try:
            return bpy.data.filepath
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting current scene file: {str(e)}")
            return ""
            
    def blender_get_frame_range(self):
        """
        Get the current scene's frame range.
        
        Returns:
            tuple: (start_frame, end_frame)
        """
        try:
            start = bpy.context.scene.frame_start
            end = bpy.context.scene.frame_end
            return start, end
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting frame range: {str(e)}")
            return 1, 250  # Default values
            
    def blender_set_frame_range(self, start_frame, end_frame):
        """
        Set the scene's frame range.
        
        Args:
            start_frame (int): Start frame
            end_frame (int): End frame
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            bpy.context.scene.frame_start = start_frame
            bpy.context.scene.frame_end = end_frame
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error setting frame range: {str(e)}")
            return False
            
    def blender_import_alembic(self, file_path):
        """
        Import an Alembic file.
        
        Args:
            file_path (str): Path to the Alembic file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                bpy.ops.wm.alembic_import(filepath=file_path)
                if self.logger:
                    self.logger.info(f"Imported Alembic file: {file_path}")
                return True
            else:
                if self.logger:
                    self.logger.error(f"Alembic file not found: {file_path}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error importing Alembic file: {str(e)}")
            return False
            
    def blender_import_fbx(self, file_path):
        """
        Import an FBX file.
        
        Args:
            file_path (str): Path to the FBX file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                bpy.ops.import_scene.fbx(filepath=file_path)
                if self.logger:
                    self.logger.info(f"Imported FBX file: {file_path}")
                return True
            else:
                if self.logger:
                    self.logger.error(f"FBX file not found: {file_path}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error importing FBX file: {str(e)}")
            return False
            
    def blender_import_obj(self, file_path):
        """
        Import an OBJ file.
        
        Args:
            file_path (str): Path to the OBJ file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                bpy.ops.import_scene.obj(filepath=file_path)
                if self.logger:
                    self.logger.info(f"Imported OBJ file: {file_path}")
                return True
            else:
                if self.logger:
                    self.logger.error(f"OBJ file not found: {file_path}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error importing OBJ file: {str(e)}")
            return False
            
    def blender_export_alembic(self, file_path, selected_only=False, frame_start=None, frame_end=None):
        """
        Export scene to Alembic file.
        
        Args:
            file_path (str): Path to save the Alembic file
            selected_only (bool): Export only selected objects
            frame_start (int): Start frame (if None, uses scene's start frame)
            frame_end (int): End frame (if None, uses scene's end frame)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if frame_start is None:
                frame_start = bpy.context.scene.frame_start
            if frame_end is None:
                frame_end = bpy.context.scene.frame_end
                
            bpy.ops.wm.alembic_export(
                filepath=file_path,
                selected=selected_only,
                start=frame_start,
                end=frame_end
            )
            
            if self.logger:
                self.logger.info(f"Exported Alembic file to: {file_path}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error exporting Alembic file: {str(e)}")
            return False
            
    def blender_set_cloth_parameters(self, object_name, parameters):
        """
        Set cloth simulation parameters for an object.
        
        Args:
            object_name (str): Name of the object
            parameters (dict): Dictionary of parameter name-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if object_name in bpy.data.objects:
                obj = bpy.data.objects[object_name]
                
                # Ensure object has a cloth modifier
                cloth_modifier = None
                for modifier in obj.modifiers:
                    if modifier.type == 'CLOTH':
                        cloth_modifier = modifier
                        break
                
                if cloth_modifier is None:
                    cloth_modifier = obj.modifiers.new(name="Cloth", type='CLOTH')
                
                # Set parameters
                for param_name, param_value in parameters.items():
                    try:
                        if hasattr(cloth_modifier.settings, param_name):
                            setattr(cloth_modifier.settings, param_name, param_value)
                    except Exception as param_err:
                        if self.logger:
                            self.logger.warning(f"Error setting cloth parameter {param_name}: {str(param_err)}")
                
                return True
            else:
                if self.logger:
                    self.logger.error(f"Object not found: {object_name}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error setting cloth parameters: {str(e)}")
            return False
            
    def blender_set_fluid_parameters(self, object_name, parameters, domain_object=None):
        """
        Set fluid simulation parameters for an object.
        
        Args:
            object_name (str): Name of the object
            parameters (dict): Dictionary of parameter name-value pairs
            domain_object (str): Name of the domain object (if different from object_name)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if object_name in bpy.data.objects:
                obj = bpy.data.objects[object_name]
                
                # Ensure object has a fluid modifier
                fluid_modifier = None
                for modifier in obj.modifiers:
                    if modifier.type == 'FLUID':
                        fluid_modifier = modifier
                        break
                
                if fluid_modifier is None:
                    fluid_modifier = obj.modifiers.new(name="Fluid", type='FLUID')
                
                # Set parameters
                for param_name, param_value in parameters.items():
                    try:
                        if hasattr(fluid_modifier.settings, param_name):
                            setattr(fluid_modifier.settings, param_name, param_value)
                    except Exception as param_err:
                        if self.logger:
                            self.logger.warning(f"Error setting fluid parameter {param_name}: {str(param_err)}")
                
                return True
            else:
                if self.logger:
                    self.logger.error(f"Object not found: {object_name}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error setting fluid parameters: {str(e)}")
            return False
            
    def blender_set_particle_parameters(self, object_name, parameters, system_index=0):
        """
        Set particle system parameters for an object.
        
        Args:
            object_name (str): Name of the object
            parameters (dict): Dictionary of parameter name-value pairs
            system_index (int): Index of the particle system if multiple exist
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if object_name in bpy.data.objects:
                obj = bpy.data.objects[object_name]
                
                # Ensure object has a particle system
                if len(obj.particle_systems) <= system_index:
                    # Add a new particle system
                    obj.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM')
                
                if system_index < len(obj.particle_systems):
                    particle_system = obj.particle_systems[system_index]
                    settings = particle_system.settings
                    
                    # Set parameters
                    for param_name, param_value in parameters.items():
                        try:
                            if hasattr(settings, param_name):
                                setattr(settings, param_name, param_value)
                        except Exception as param_err:
                            if self.logger:
                                self.logger.warning(f"Error setting particle parameter {param_name}: {str(param_err)}")
                    
                    return True
                else:
                    if self.logger:
                        self.logger.error(f"Particle system index out of range: {system_index}")
                    return False
            else:
                if self.logger:
                    self.logger.error(f"Object not found: {object_name}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error setting particle parameters: {str(e)}")
            return False
            
    def blender_set_rigid_body_parameters(self, object_name, parameters):
        """
        Set rigid body simulation parameters for an object.
        
        Args:
            object_name (str): Name of the object
            parameters (dict): Dictionary of parameter name-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if object_name in bpy.data.objects:
                obj = bpy.data.objects[object_name]
                
                # Ensure object has rigid body physics
                if obj.rigid_body is None:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.rigidbody.object_add()
                
                # Set parameters
                for param_name, param_value in parameters.items():
                    try:
                        if hasattr(obj.rigid_body, param_name):
                            setattr(obj.rigid_body, param_name, param_value)
                    except Exception as param_err:
                        if self.logger:
                            self.logger.warning(f"Error setting rigid body parameter {param_name}: {str(param_err)}")
                
                return True
            else:
                if self.logger:
                    self.logger.error(f"Object not found: {object_name}")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error setting rigid body parameters: {str(e)}")
            return False
            
    def blender_run_simulation(self, frame_start=None, frame_end=None, cache_dir=None):
        """
        Run simulation for the specified frame range.
        
        Args:
            frame_start (int): Start frame (if None, uses scene's start frame)
            frame_end (int): End frame (if None, uses scene's end frame)
            cache_dir (str): Directory to store cache files
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if frame_start is None:
                frame_start = bpy.context.scene.frame_start
            if frame_end is None:
                frame_end = bpy.context.scene.frame_end
            
            # Set frame range
            bpy.context.scene.frame_start = frame_start
            bpy.context.scene.frame_end = frame_end
            
            # Set cache directory if provided
            if cache_dir:
                os.makedirs(cache_dir, exist_ok=True)
                # Note: Setting cache directory depends on the simulation type
            
            # Run simulation for each frame
            for frame in range(frame_start, frame_end + 1):
                bpy.context.scene.frame_set(frame)
                if self.logger and frame % 10 == 0:  # Log every 10 frames
                    self.logger.info(f"Simulating frame {frame}/{frame_end}")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error running simulation: {str(e)}")
            return False
            
    def blender_render_opengl(self, output_path, frame_start=None, frame_end=None):
        """
        Render using OpenGL.
        
        Args:
            output_path (str): Base path for output files
            frame_start (int): Start frame (if None, uses scene's start frame)
            frame_end (int): End frame (if None, uses scene's end frame)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if frame_start is None:
                frame_start = bpy.context.scene.frame_start
            if frame_end is None:
                frame_end = bpy.context.scene.frame_end
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Set up render settings
            bpy.context.scene.render.filepath = output_path
            
            # Render each frame
            for frame in range(frame_start, frame_end + 1):
                bpy.context.scene.frame_set(frame)
                bpy.ops.render.opengl(animation=False, write_still=True)
                if self.logger and frame % 10 == 0:  # Log every 10 frames
                    self.logger.info(f"Rendering frame {frame}/{frame_end}")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error rendering with OpenGL: {str(e)}")
            return False
            
    def blender_render_cycles(self, output_path, frame_start=None, frame_end=None, samples=128):
        """
        Render using Cycles renderer.
        
        Args:
            output_path (str): Base path for output files
            frame_start (int): Start frame (if None, uses scene's start frame)
            frame_end (int): End frame (if None, uses scene's end frame)
            samples (int): Number of samples for Cycles rendering
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if frame_start is None:
                frame_start = bpy.context.scene.frame_start
            if frame_end is None:
                frame_end = bpy.context.scene.frame_end
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Set up render settings
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.samples = samples
            bpy.context.scene.render.filepath = output_path
            
            # Render animation
            bpy.ops.render.render(animation=True, write_still=True)
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error rendering with Cycles: {str(e)}")
            return False
            
    def blender_render_eevee(self, output_path, frame_start=None, frame_end=None):
        """
        Render using Eevee renderer.
        
        Args:
            output_path (str): Base path for output files
            frame_start (int): Start frame (if None, uses scene's start frame)
            frame_end (int): End frame (if None, uses scene's end frame)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if frame_start is None:
                frame_start = bpy.context.scene.frame_start
            if frame_end is None:
                frame_end = bpy.context.scene.frame_end
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Set up render settings
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
            bpy.context.scene.render.filepath = output_path
            
            # Render animation
            bpy.ops.render.render(animation=True, write_still=True)
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error rendering with Eevee: {str(e)}")
            return False
            
    def blender_get_cloth_objects(self):
        """
        Get all objects with cloth simulation.
        
        Returns:
            list: List of object names with cloth simulation
        """
        try:
            cloth_objects = []
            for obj in bpy.data.objects:
                for modifier in obj.modifiers:
                    if modifier.type == 'CLOTH':
                        cloth_objects.append(obj.name)
                        break
            return cloth_objects
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting cloth objects: {str(e)}")
            return []
            
    def blender_get_fluid_objects(self):
        """
        Get all objects with fluid simulation.
        
        Returns:
            list: List of object names with fluid simulation
        """
        try:
            fluid_objects = []
            for obj in bpy.data.objects:
                for modifier in obj.modifiers:
                    if modifier.type == 'FLUID':
                        fluid_objects.append(obj.name)
                        break
            return fluid_objects
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting fluid objects: {str(e)}")
            return []
            
    def blender_get_particle_objects(self):
        """
        Get all objects with particle systems.
        
        Returns:
            list: List of object names with particle systems
        """
        try:
            particle_objects = []
            for obj in bpy.data.objects:
                if len(obj.particle_systems) > 0:
                    particle_objects.append(obj.name)
            return particle_objects
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting particle objects: {str(e)}")
            return []
            
    def blender_get_rigid_body_objects(self):
        """
        Get all objects with rigid body physics.
        
        Returns:
            list: List of object names with rigid body physics
        """
        try:
            rigid_body_objects = []
            for obj in bpy.data.objects:
                if obj.rigid_body is not None:
                    rigid_body_objects.append(obj.name)
            return rigid_body_objects
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting rigid body objects: {str(e)}")
            return [] 