#######################################
#      Tested with 3dsMAX 2016        #
#                                     #
#run MXS:
#      clearlistener()
#      python.ExecuteFile (@"S:\simbatch\GUI_3dsMAX.py") 
#######################################
#
##
###
simbatch_instalation_dir = "S:/"   # for  "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#

simbatch_installation_root = "E:\\simbatch\\"  
simbatch_config_ini = "config.ini"

import sys 
if not simbatch_instalation_dir in sys.path:
    sys.path.append(simbatch_instalation_dir)

import simbatch.core.core as simbatch_core
import simbatch.server.server as simbatch_server
import simbatch.ui.mainw as simbatch_ui

reload ( simbatch_core )
reload ( simbatch_server )
reload ( simbatch_ui ) 

from PySide2 import QtCore, QtGui, QtWidgets
import MaxPlus

class _GCProtector(object):
	widgets = []

app = QtGui.QApplication.instance()
if not app:
	app = QtGui.QApplication([])

def main():	
    MaxPlus.FileManager.Reset(True)
    
    simbatch = simbatch_core.SimBatch("3dsMAX", ini_file=simbatch_config_ini)
    loading_data_state = simbatch.load_data()
    simbatch_srv = simbatch_server.SimBatchServer(simbatch, framework_mode=True)
    simbatch_main_window = simbatch_ui.MainWindow(simbatch_srv, parent=None)
    
    MaxPlus.AttachQWidgetToMax( simbatch_main_window )
    
    simbatch_main_window.show() 
     

if __name__ == '__main__':
    main()
     