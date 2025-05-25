import os
import sys
import definitions.interactions_base as interactions_base

class Interactions(interactions_base.BaseInteractions):
    current_os = -1
    logger = None
    comfun = None
    _houdini_available = False

    def __init__(self, current_os, logger, comfun):
        super().__init__(current_os, logger, comfun)
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun
        # Try to import hou but don't fail if not available
        try:
            import hou
            self._houdini_available = True
            self.hou = hou
        except ImportError:
            self._houdini_available = False
            self.logger.wrn("Houdini Python API not available - some functionality will be limited")

    def print_info(self):
        self.logger.raw("This is interaction with Houdini")

    def _check_houdini(self):
        """Check if hou is available and raise appropriate error if not"""
        if not self._houdini_available:
            raise ImportError("Houdini Python API not available")

    # common interactions
    def schema_item_double_click(self, param):
        self.houdini_open_scene(param)

    def task_item_double_click(self, param):
        self.houdini_open_scene(param)

    # Houdini-specific implementations
    def open_scene(self, param):
        """Open a scene file"""
        self.houdini_open_file(param)

    def save_scene(self, param):
        """Save current scene"""
        self.save_current_scene_as(param)

    def save_scene_as_next_version(self, param):
        """Save current scene as next version"""
        self.save_current_scene_as(param)

    # houdini interactions
    def houdini_open_scene(self, file_name):
        try:
            self._check_houdini()
            self.hou.hipFile.load(file_name, suppress_save_prompt=True, ignore_load_warnings=True)
        except ImportError:
            self.logger.err("Houdini Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error opening Houdini file: {str(e)}")
            return False

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
        try:
            self._check_houdini()
            self.hou.hipFile.save(file_name, save_to_recent_files=True)
            return True
        except ImportError:
            self.logger.err("Houdini Python API not available")
            return False
        except Exception as e:
            self.logger.err(f"Error saving Houdini file: {str(e)}")
            return False

    def get_curent_scene_file(self):
        """Get the current Houdini scene file path and info.
        
        Returns:
            tuple: (directory, filename, filename_without_ext, extension)
        """
        try:
            self._check_houdini()
            # Get current .hip file path
            current_file = self.hou.hipFile.path()
            
            if not current_file:
                self.logger.wrn("No current Houdini scene file")
                return "", "", "", "hip"
                
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
            self.logger.err("Houdini Python API not available")
            return "", "", "", "hip"
        except Exception as e:
            self.logger.err(f"Error getting current Houdini scene file: {str(e)}")
            return "", "", "", "hip"
