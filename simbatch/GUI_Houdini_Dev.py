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
import importlib  # Add this for reload functionality

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
    
    # Force reload all modules in correct dependency order
    
    # First reload core library modules
    import core.lib.logger as simbatch_logger
    importlib.reload(simbatch_logger)
    
    import core.lib.common as simbatch_comfun
    importlib.reload(simbatch_comfun)
    
    # Then reload definitions modules first (needed by core)
    import definitions.interactions_base as simbatch_interactions_base
    importlib.reload(simbatch_interactions_base)
    
    import definitions.interactions_houdini as simbatch_interactions_houdini
    importlib.reload(simbatch_interactions_houdini)
    
    import definitions.interactions_maya as simbatch_interactions_maya
    importlib.reload(simbatch_interactions_maya)
    
    import definitions.interactions_max as simbatch_interactions_max
    importlib.reload(simbatch_interactions_max)
    
    import definitions.interactions_blender as simbatch_interactions_blender
    importlib.reload(simbatch_interactions_blender)
    
    # Then reload core modules
    import core.settings as simbatch_settings
    importlib.reload(simbatch_settings)
    
    import core.projects as simbatch_projects
    importlib.reload(simbatch_projects)
    
    import core.schemas as simbatch_schemas
    importlib.reload(simbatch_schemas)
    
    import core.tasks as simbatch_tasks
    importlib.reload(simbatch_tasks)
    
    import core.queue as simbatch_queue
    importlib.reload(simbatch_queue)
    
    import core.nodes as simbatch_nodes
    importlib.reload(simbatch_nodes)
    
    import core.definitions as simbatch_definitions
    importlib.reload(simbatch_definitions)
    
    import core.io as simbatch_ios
    importlib.reload(simbatch_ios)
    
    # Then reload server
    import server.server as simbatch_server
    importlib.reload(simbatch_server)
    
    # Finally reload UI modules in dependency order
    import ui.ui_settings as simbatch_ui_settings
    importlib.reload(simbatch_ui_settings)
    
    import ui.ui_projects as simbatch_ui_projects
    importlib.reload(simbatch_ui_projects)
    
    import ui.ui_schemas as simbatch_ui_schemas
    importlib.reload(simbatch_ui_schemas)
    
    import ui.ui_schemas_form as simbatch_ui_schemas_form
    importlib.reload(simbatch_ui_schemas_form)
    
    import ui.ui_tasks as simbatch_ui_tasks
    importlib.reload(simbatch_ui_tasks)
    
    import ui.ui_tasks_forms as simbatch_ui_tasks_forms
    importlib.reload(simbatch_ui_tasks_forms)
    
    import ui.ui_queue as simbatch_ui_queue
    importlib.reload(simbatch_ui_queue)
    
    import ui.ui_definitions as simbatch_ui_definitions
    importlib.reload(simbatch_ui_definitions)
    
    import ui.ui_nodes as simbatch_nodes
    importlib.reload(simbatch_nodes)
    
    # Reload main UI module last
    import ui.mainw as simbatch_ui
    importlib.reload(simbatch_ui)
    
    # Reload core module last
    import core.core as simbatch_core
    importlib.reload(simbatch_core)
    
    # Initialize and run
    simbatch = simbatch_core.SimBatch("Houdini", ini_file=simbatch_config_ini)
    loading_data_state = simbatch.load_data()
    simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)
    
    if simbatch.sts.with_gui == 1:
        simbatch_window = simbatch_ui.MainWindow(simbatch_server)
        simbatch_window.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        simbatch_window.show()
        simbatch_window.post_run(loading_data_state) 