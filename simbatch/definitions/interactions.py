
class Interactions:
    def __init__(self):
        pass
        
    # houdini executions     
    def houdini_open_scene(self, file):
        pass
        
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
        
    def houdini_save_scene(self, file):
        pass
    
    # 3dsmax executions 
    def max_open_scene(self, file):
        pass
        
    def max_import_ani(self, objects, dir):
        pass
        
    def max_import_cam(self, objects, file_or_dir):
        pass
        
    def max_import_obj(self, objects, file_or_dir):
        pass
    
    def max_simulate(self, ts, te, objects_names, cache_dir):
        pass   
        
    def max_render(self, ts, te, out_file=""):
        pass 
        
    def max_save_scene(self, file):
        pass
    
    # maya executions
    def maya_open_scene(self, file):
        pass
        
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