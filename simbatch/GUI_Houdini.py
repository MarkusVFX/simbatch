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
import ui.mainw as simbatch_ui

    
sim_batch = simbatch_core.SimBatch("Houdini", ini_file=simbatch_config_ini)
loading_data_state = sim_batch.load_data()


if sim_batch.sts.with_gui == 1:
    main_window = simbatch_ui.MainWindow(sim_batch) 
    main_window.show()
    main_window.post_run(loading_data_state)
