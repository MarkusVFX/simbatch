class BaseInteractions:
    current_os = -1
    logger = None
    comfun = None

    def __init__(self, current_os, logger, comfun):
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun

    def print_info(self):
        """Print information about the current interaction class"""
        self.logger.raw("This is base interaction class")

    # Scene Management
    def get_curent_scene_file(self):
        """Get the current scene file path and info.
        
        Returns:
            tuple: (directory, filename, filename_without_ext, extension)
        """
        raise NotImplementedError("Subclasses must implement get_curent_scene_file()")

    def get_curent_frame_range(self):
        """Get the current frame range of the scene.
        
        Returns:
            tuple: (start_frame, end_frame)
        """
        raise NotImplementedError("Subclasses must implement get_curent_frame_range()")

    # File Operations
    def open_scene(self, param):
        """Open a scene file"""
        raise NotImplementedError("Subclasses must implement open_scene()")

    def save_scene(self, param):
        """Save current scene"""
        raise NotImplementedError("Subclasses must implement save_scene()")

    def save_scene_as_next_version(self, param):
        """Save current scene as next version"""
        raise NotImplementedError("Subclasses must implement save_scene_as_next_version()")

    # UI Interactions
    def schema_item_double_click(self, param):
        """Handle schema item double click"""
        self.open_scene(param)

    def task_item_double_click(self, param):
        """Handle task item double click"""
        self.open_scene(param)

    # Selection Management
    def get_selection(self):
        """Get currently selected objects.
        
        Returns:
            list: List of selected object names
        """
        raise NotImplementedError("Subclasses must implement get_selection()")

    def select_objects(self, objects):
        """Select objects by name.
        
        Args:
            objects (str): Comma-separated list of object names
            
        Returns:
            int: Number of objects selected
        """
        raise NotImplementedError("Subclasses must implement select_objects()")

    # Parameter Management
    def set_param(self, objects, property, value):
        """Set parameter value on objects.
        
        Args:
            objects (str): Comma-separated list of object names
            property (str): Property name to set
            value: Value to set
        """
        raise NotImplementedError("Subclasses must implement set_param()")

    # Import/Export
    def import_ani(self, objects, dir):
        """Import animation data.
        
        Args:
            objects (str): Target objects
            dir (str): Source directory/file
        """
        raise NotImplementedError("Subclasses must implement import_ani()")

    def import_cam(self, objects, file_or_dir):
        """Import camera data.
        
        Args:
            objects (str): Target objects
            file_or_dir (str): Source file/directory
        """
        raise NotImplementedError("Subclasses must implement import_cam()")

    def import_obj(self, objects, file_or_dir):
        """Import object data.
        
        Args:
            objects (str): Target objects
            file_or_dir (str): Source file/directory
        """
        raise NotImplementedError("Subclasses must implement import_obj()")

    # Simulation
    def simulate(self, ts, te, objects_names, cache_dir):
        """Run simulation.
        
        Args:
            ts (str): Start time
            te (str): End time
            objects_names (str): Objects to simulate
            cache_dir (str): Cache directory
        """
        raise NotImplementedError("Subclasses must implement simulate()")

    # Rendering
    def render(self, ts, te, out_file=""):
        """Render scene.
        
        Args:
            ts (str): Start time
            te (str): End time
            out_file (str): Output file path
        """
        raise NotImplementedError("Subclasses must implement render()")

    # Script Execution
    def script_py(self, file):
        """Execute Python script.
        
        Args:
            file (str): Script file path
        """
        raise NotImplementedError("Subclasses must implement script_py()")
