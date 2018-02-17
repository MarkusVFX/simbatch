##################################
##   Tested with Houdini 16.5   ##
##################################

import sys
sys.path.append("S:\\simbatch\\")

import simbatch.core.core as simbatch_core
import simbatch.ui.mainw as simbatch_ui

    
sim_batch = simbatch_core.SimBatch("Houdini", ini_file="S:\\simbatch\\config.ini")
loading_data_state = sim_batch.load_data()


if sim_batch.sts.WITH_GUI == 1:
    main_window = simbatch_ui.MainWindow(sim_batch) 
    main_window.show()
    if loading_data_state is True:
        main_window.top_ui.set_top_info(sim_batch.sts.random_welcome_message())
    elif loading_data_state is False:
        main_window.top_ui.set_top_info("Data not loaded")
    else:
        if loading_data_state == 1:
            main_window.top_ui.set_top_info("Loaded with one data error")
        else:
            main_window.top_ui.set_top_info("Loaded with data errors ({})".format(loading_data_state))
