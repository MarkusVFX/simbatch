##################################
# Tested with Maya 2016 and 2017 #
##################################
#
##
###
simbatch_installation_dir = "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#
import sys
sys.path.append(simbatch_installation_dir)

import core.core
import server.server
import ui.mainw as simbatch_ui

import maya.OpenMayaUI as mui

try:  # Maya 2015 and 2016
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtGui import *
    except ImportError:
        raise Exception('PySide import ERROR!  Please install PySide or PySide2')


try:  # Maya 2015 and 2016
    import shiboken
except ImportError:
    try:  # Maya 2017
        import shiboken2 as shiboken
    except ImportError:
        print "shiboken import ERROR"


def get_maya_window():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QWidget)


maya_window = get_maya_window()


simbatch = core.core.SimBatch("Maya", ini_file=simbatch_config_ini)
loading_data_state = simbatch.load_data()
simbatch_server = server.server.SimBatchServer(simbatch, force_local=True)



if simbatch.sts.WITH_GUI == 1:
    main_window = simbatch_ui.MainWindow(simbatch, simbatch_server, parent=maya_window)
    main_window.show()
    main_window.post_run(loading_data_state)
