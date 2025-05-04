####################################################
##   Tested with Houdini 19.5.716  and 20.5.326   ##
####################################################
#
##
###
simbatch_instalation_dir = "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#

import hou
import sys
import os

try:
    from PySide2 import QtCore, QtUiTools, QtWidgets
except ImportError:
    try:
        # Try alternative import path that might work in Houdini
        from PySide2.QtCore import *
        from PySide2.QtUiTools import *
        from PySide2.QtWidgets import *
    except ImportError as e:
        hou.ui.displayMessage("Error: Could not import PySide2. Please ensure you're running this script from within Houdini.", severity=hou.severityType.Error)
        raise e
        
if not os.path.exists(simbatch_instalation_dir):
    msg = f"Error: SimBatch installation directory not found!\nPath: {simbatch_instalation_dir}\n\nPlease check your installation and configuration."
    hou.ui.displayMessage(msg, severity=hou.severityType.Error)
else:
    if not simbatch_instalation_dir in sys.path:
        sys.path.append(simbatch_instalation_dir)
    
    import core.core as simbatch_core
    import server.server as simbatch_server
    import ui.mainw as simbatch_ui
    
    
    simbatch = simbatch_core.SimBatch("Houdini", ini_file=simbatch_config_ini)
    loading_data_state = simbatch.load_data()
    simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)
    
    if simbatch.sts.with_gui == 1:
        simbatch_window = simbatch_ui.MainWindow(simbatch_server)
        simbatch_window.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        simbatch_window.show()
        simbatch_window.post_run(loading_data_state)
        
