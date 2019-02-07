##################################
##   Tested with Houdini 16.5   ##
##################################
#
##
###
simbatch_instalation_dir = "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#

import sys
sys.path.append(simbatch_instalation_dir)

import core.core as simbatch_core
import simbatch.server.server as simbatch_server
import ui.mainw as simbatch_ui

    
simbatch = simbatch_core.SimBatch("Houdini", ini_file=simbatch_config_ini)
loading_data_state = simbatch.load_data()
simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)


if simbatch.sts.with_gui == 1:
    main_window = simbatch_ui.MainWindow(simbatch_server)
    main_window.show()
    main_window.post_run(loading_data_state)
