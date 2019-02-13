class Interactions:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger, comfun):
        self.current_os = current_os
        self.logger = logger
        self.comfun = comfun

    def print_info(self):
        self.logger.raw("This is stand-alone's interactions")

    # framework interactions
    def schema_item_double_click(self, param):
        self.logger.raw("[INF interactions] Double clicked on stand-alone schema item (defined in interactions file)")
        
    def sa_loop_over_files(self, file):
        return ret2
        
        
    def sa_loop_over_dir(self, file):
        import maya.cmds as cmd
        ret1 = cmd.file(rename=target)
        ret2 = cmd.file(save=True, type="mayaBinary")
        return ret2
        
    def simple_info_print(self):
        print "\n\n simple info test "
        
    def detailed_info_print(self):
        print "\n\n detailed info test "
        
    def reset_filter(self):
        return "*.*"
        
    def reset_details(self):
        return "*.*|time|date|size"
       
    