####################################
# Tested with Maya 2015 2016 2017 #
##################################
#
##
###
simbatch_instalation_dir = "S:\\simbatch\\"
simbatch_config_ini = "S:\\simbatch\\config.ini"
###
##
#
import sys
sys.path.append(simbatch_instalation_dir)

import simbatch.core.core as simbatch_core
import simbatch.ui.mainw as simbatch_ui


############  force reload  START
reload (simbatch_core)
reload (simbatch_ui)
############  force reload  END

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

############  force reload  START
import simbatch.core.common as simbatch_comfun
reload (simbatch_comfun)
sim_batch.comfun = simbatch_comfun.CommonFunctions()

import simbatch.core.settings as simbatch_settings
reload (simbatch_settings)
sim_batch.sts = simbatch_settings.Settings(sim_batch.logger, "Maya", ini_file="/job/pinwheel/dev/sandbox/sandbox_msulecki/work/msulecki/tmp/simbatch_test/config.ini")
############  force reload  END

loading_data_state = sim_batch.load_data()


if sim_batch.sts.WITH_GUI == 1:
    ############  force update UI  START
    import simbatch.ui.ui_settings as simbatch_ui_settings
    reload (simbatch_ui_settings)
    reload (simbatch_ui)
    ############  force update UI  END
    main_window = simbatch_ui.MainWindow(sim_batch)
    main_window.show()
    main_window.post_run(loading_data_state)
