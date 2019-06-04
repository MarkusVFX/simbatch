############################################
##   Tested with Houdini 16.5  and 17.5   ##
############################################
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

if not simbatch_instalation_dir in sys.path:
    sys.path.append(simbatch_instalation_dir)

import core.core as simbatch_core
import server.server as simbatch_server
import ui.mainw as simbatch_ui

from PySide2 import QtCore, QtUiTools, QtWidgets

simbatch = simbatch_core.SimBatch("Houdini", ini_file=simbatch_config_ini)
loading_data_state = simbatch.load_data()
simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)

if simbatch.sts.with_gui == 1:
    simbatch_window = simbatch_ui.MainWindow(simbatch_server)
    simbatch_window.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
    simbatch_window.show()
    simbatch_window.post_run(loading_data_state)
