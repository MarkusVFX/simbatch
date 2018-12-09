##################################
# Tested with Maya 2016 and 2017 #
##################################
#
##
###
simbatch_installation_root = "S:/"   # for  "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#
import sys
sys.path.append(simbatch_installation_root)

import simbatch.core.core as simbatch_core
import simbatch.server.server as simbatch_server
import simbatch.ui.mainw as simbatch_ui

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


simbatch = simbatch_core.SimBatch("Maya", ini_file=simbatch_config_ini)
loading_data_state = simbatch.load_data()
simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)


if simbatch.sts.WITH_GUI == 1:
    main_window = simbatch_ui.MainWindow(simbatch_server, parent=maya_window)
    main_window.show()
    main_window.post_run(loading_data_state)
