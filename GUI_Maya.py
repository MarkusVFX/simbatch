##################################
# Tested with Maya 2016 and 2017 #
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

import simbatch.core.core as simbatch_core
import simbatch.ui.mainw as simbatch_ui

import maya.OpenMayaUI as mui

try:    # Maya 2016
    import shiboken
except:
    try:  # Maya 2017
        import shiboken2 as shiboken
    except:
        print "shiboken import ERROR"

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)


sim_batch = simbatch_core.SimBatch("Maya", ini_file=simbatch_config_ini)
loading_data_state = sim_batch.load_data()


if sim_batch.sts.WITH_GUI == 1:
    main_window = simbatch_ui.MainWindow(sim_batch) 
    main_window.show()
    main_window.post_run(loading_data_state)
