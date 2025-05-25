####################################################
##   Tested with Maya 2018-2022                    ##
##   Note: This version uses Python 2 reload()     ##
##   For Python 3 support, use GUI_Houdini_Dev.py  ##
##   as a reference for importlib.reload()         ##
####################################################
#
##
###
simbatch_instalation_dir = "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#

import maya.cmds as cmds
import sys
import os

try:
    from PySide2 import QtCore, QtUiTools, QtWidgets
except ImportError:
    try:
        # Try alternative import path that might work in Maya
        from PySide2.QtCore import *
        from PySide2.QtUiTools import *
        from PySide2.QtWidgets import *
    except ImportError as e:
        cmds.confirmDialog(title="Error", message="Could not import PySide2. Please ensure you're running this script from within Maya.", button=["OK"])
        raise e
        
if not os.path.exists(simbatch_instalation_dir):
    msg = f"Error: SimBatch installation directory not found!\nPath: {simbatch_instalation_dir}\n\nPlease check your installation and configuration."
    cmds.confirmDialog(title="Error", message=msg, button=["OK"])
else:
    if not simbatch_instalation_dir in sys.path:
        sys.path.append(simbatch_instalation_dir)
    
    # Force reload all modules in correct dependency order
    
    # First reload core library modules
    import core.lib.logger as simbatch_logger
    reload(simbatch_logger)
    
    import core.lib.common as simbatch_comfun
    reload(simbatch_comfun)
    
    # Then reload definitions modules first (needed by core)
    import definitions.interactions_base as simbatch_interactions_base
    reload(simbatch_interactions_base)
    
    import definitions.interactions_maya as simbatch_interactions_maya
    reload(simbatch_interactions_maya)
    
    # Then reload core modules
    import core.settings as simbatch_settings
    reload(simbatch_settings)
    
    import core.projects as simbatch_projects
    reload(simbatch_projects)
    
    import core.schemas as simbatch_schemas
    reload(simbatch_schemas)
    
    import core.tasks as simbatch_tasks
    reload(simbatch_tasks)
    
    import core.queue as simbatch_queue
    reload(simbatch_queue)
    
    import core.nodes as simbatch_nodes
    reload(simbatch_nodes)
    
    import core.definitions as simbatch_definitions
    reload(simbatch_definitions)
    
    import core.io as simbatch_ios
    reload(simbatch_ios)
    
    # Then reload server
    import server.server as simbatch_server
    reload(simbatch_server)
    
    # Finally reload UI modules in dependency order
    import ui.ui_settings as simbatch_ui_settings
    reload(simbatch_ui_settings)
    
    import ui.ui_projects as simbatch_ui_projects
    reload(simbatch_ui_projects)
    
    import ui.ui_schemas as simbatch_ui_schemas
    reload(simbatch_ui_schemas)
    
    import ui.ui_schemas_form as simbatch_ui_schemas_form
    reload(simbatch_ui_schemas_form)
    
    import ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    
    import ui.ui_tasks_forms as simbatch_ui_tasks_forms
    reload(simbatch_ui_tasks_forms)
    
    import ui.ui_queue as simbatch_ui_queue
    reload(simbatch_ui_queue)
    
    import ui.ui_definitions as simbatch_ui_definitions
    reload(simbatch_ui_definitions)
    
    import ui.ui_nodes as simbatch_nodes
    reload(simbatch_nodes)
    
    # Reload main UI module last
    import ui.mainw as simbatch_ui
    reload(simbatch_ui)
    
    # Reload core module last
    import core.core as simbatch_core
    reload(simbatch_core)
    
    # Initialize and run
    simbatch = simbatch_core.SimBatch("Maya", ini_file=simbatch_config_ini)
    loading_data_state = simbatch.load_data()
    simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)
    
    if simbatch.sts.with_gui == 1:
        simbatch_window = simbatch_ui.MainWindow(simbatch_server)
        simbatch_window.setParent(cmds.maya.mainWindow(), QtCore.Qt.Window)
        simbatch_window.show()
        simbatch_window.post_run(loading_data_state) 