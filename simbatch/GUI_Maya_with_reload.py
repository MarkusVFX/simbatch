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

import core.core
import server.server
import ui.mainw as simbatch_ui

"""   force reload roots """
reload(core.core)
reload(server.server)
reload(simbatch_ui)
"""   force reload roots END  """

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


"""   force reload core   """
import core.settings as simbatch_settings
reload(simbatch_settings)
simbatch.sts = simbatch_settings.Settings(simbatch.logger, "Maya", ini_file=simbatch_config_ini)

import core.lib.common as simbatch_comfun
reload(simbatch_comfun)
simbatch.comfun = simbatch_comfun.CommonFunctions()

import core.lib.logger as simbatch_logger
reload(simbatch_logger)
simbatch.logger = simbatch_logger.Logger()

import core.projects as simbatch_projects
reload(simbatch_projects)
simbatch.prj = simbatch_projects.Projects(simbatch)

import core.schemas as simbatch_schemas
reload(simbatch_schemas)
simbatch.sch = simbatch_schemas.Schemas(simbatch)

import core.tasks as simbatch_tasks
reload(simbatch_tasks)
simbatch.tsk = simbatch_tasks.Tasks(simbatch)

import core.queue as simbatch_queue
reload(simbatch_queue)
simbatch.que = simbatch_queue.Queue(simbatch)

import core.nodes as simbatch_nodes
reload(simbatch_nodes)
simbatch.nod = simbatch_nodes.SimNodes(simbatch)

import core.definitions as simbatch_definitions
reload(simbatch_definitions)
simbatch.dfn = simbatch_definitions.Definitions(simbatch)

import core.io as simbatch_ios
reload(simbatch_ios)
simbatch.sio = simbatch_ios.StorageInOut(simbatch)
"""   force reload core  END   """

if simbatch.sts.WITH_GUI == 1:
    """   force reload UI """
    import ui.ui_settings as simbatch_ui_settings
    reload(simbatch_ui_settings)
    import ui.ui_projects as simbatch_ui_projects
    reload(simbatch_ui_projects)
    import ui.ui_schemas as simbatch_ui_schemas
    reload(simbatch_ui_schemas)
    import ui.ui_schemas_form as simbatch_ui_schemas_form
    reload(simbatch_ui_schemas_form)
    import ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    import ui.ui_tasks_forms as simbatch_ui_tasks_forms
    reload(simbatch_ui_tasks_forms)
    import ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    import ui.ui_queue as simbatch_ui_queue
    reload(simbatch_ui_queue)
    import ui.ui_definitions as simbatch_ui_definitions
    reload(simbatch_ui_definitions)
    import ui.ui_nodes as simbatch_nodes
    reload(simbatch_nodes)
    reload(simbatch_ui)
    """   force reload UI  END   """
    main_window = simbatch_ui.MainWindow(simbatch, simbatch_server, parent=maya_window)
    main_window.show()
    main_window.post_run(loading_data_state)
