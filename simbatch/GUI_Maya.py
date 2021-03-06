#######################################
# Tested with Maya 2016 2017 and 2018 #
#######################################
#
##
###
simbatch_installation_root = "S:/"   # for  "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#

import sys
if not simbatch_instalation_dir in sys.path:
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
        try:  # Maya 2018
            from PySide2.QtWidgets import *
        except ImportError:
            raise Exception('PySide import ERROR!')
    except ImportError:
        raise Exception('PySide import ERROR!  Please install PySide or PySide2')


try:  # Maya 2015 and 2016
    import shiboken
except ImportError:
    try:  # Maya 2017
        import shiboken2 as shiboken
    except ImportError:
        print "shiboken import ERROR"

try:
    simbatch_window.close()
except:
    pass


def get_maya_window():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QWidget)


maya_window = get_maya_window()


simbatch = simbatch_core.SimBatch("Maya", ini_file=simbatch_config_ini)
loading_data_state = simbatch.load_data()
simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)


if simbatch.sts.with_gui == 1:
    simbatch_window = simbatch_ui.MainWindow(simbatch_server, parent=maya_window)
    simbatch_window.show()
    simbatch_window.post_run(loading_data_state)
