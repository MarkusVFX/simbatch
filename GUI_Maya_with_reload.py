####################################
# Tested with Maya 2015 2016 2017 #
##################################
#
##
###
simbatch_installation_dir = "S:\\simbatch\\"
simbatch_config_ini = "S:\\simbatch\\config.ini"
###
##
#
import sys
sys.path.append(simbatch_installation_dir)

import simbatch.core.core as simbatch_core
import simbatch.ui.mainw as simbatch_ui


############  force reload  START
reload(simbatch_core)
reload(simbatch_ui)
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

############  force update  START
import simbatch.core.settings as simbatch_settings
reload(simbatch_settings)
sim_batch.sts = simbatch_settings.Settings(sim_batch.logger, "Maya", ini_file=simbatch_config_ini)

import simbatch.core.lib.common as simbatch_comfun
reload(simbatch_comfun)
sim_batch.comfun = simbatch_comfun.CommonFunctions()

import simbatch.core.projects as simbatch_projects
reload(simbatch_projects)
sim_batch.prj = simbatch_projects.Projects(sim_batch)

import simbatch.core.schemas as simbatch_schemas
reload(simbatch_schemas)
sim_batch.sch = simbatch_schemas.Schemas(sim_batch)

import simbatch.core.tasks as simbatch_tasks
reload(simbatch_tasks)
sim_batch.tsk = simbatch_tasks.Tasks(sim_batch)

import simbatch.core.queue as simbatch_queue
reload(simbatch_queue)
sim_batch.que = simbatch_queue.Queue(sim_batch)

import simbatch.core.definitions as simbatch_definitions
reload(simbatch_definitions)
sim_batch.dfn = simbatch_definitions.Definitions(sim_batch)

import simbatch.core.io as simbatch_ios
reload(simbatch_ios)
sim_batch.sio = simbatch_ios.StorageInOut(sim_batch)
############  force update  END

loading_data_state = sim_batch.load_data()


if sim_batch.sts.WITH_GUI == 1:
    ############  force update UI  START
    import simbatch.ui.ui_settings as simbatch_ui_settings
    reload(simbatch_ui_settings)
    import simbatch.ui.ui_projects as simbatch_ui_projects
    reload(simbatch_ui_projects)
    import simbatch.ui.ui_schemas as simbatch_ui_schemas
    reload(simbatch_ui_schemas)
    import simbatch.ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    import simbatch.ui.ui_tasks_form as simbatch_ui_tasks_form
    reload(simbatch_ui_tasks_form)
    import simbatch.ui.ui_schemas_form as simbatch_ui_schemas_form
    reload(simbatch_ui_schemas_form)
    import simbatch.ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    import simbatch.ui.ui_queue as simbatch_ui_queue
    reload (simbatch_ui_queue)
    import simbatch.ui.ui_definitions as simbatch_ui_definitions
    reload (simbatch_ui_definitions)
    reload(simbatch_ui)
    ############  force update UI  END
    main_window = simbatch_ui.MainWindow(sim_batch)
    main_window.show()
    main_window.post_run(loading_data_state)
