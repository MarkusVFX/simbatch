########################################
# Tested with Maya 2015 2016 2017 2018 #
########################################
#
##
###
simbatch_instalation_dir = "S:/"   # for  "S:/simbatch/"
simbatch_config_ini = "S:/simbatch/config.ini"
###
##
#
import sys
if not simbatch_instalation_dir in sys.path:
    sys.path.append(simbatch_instalation_dir)

import simbatch.core.core as simbatch_core
import simbatch.server.server as simbatch_server
import simbatch.ui.mainw as simbatch_ui


"""   force reload roots """
reload(simbatch_core)
reload(simbatch_server)
reload(simbatch_ui)
"""   force reload roots END  """

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
simbatch_server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)


"""   force reload core   """
import simbatch.core.lib.logger as simbatch_logger
reload(simbatch_logger)
simbatch.logger = simbatch_logger.Logger()

import simbatch.core.settings as simbatch_settings
reload(simbatch_settings)
simbatch.sts = simbatch_settings.Settings(simbatch.logger, "Maya", ini_file=simbatch_config_ini)

import simbatch.core.lib.common as simbatch_comfun
reload(simbatch_comfun)
simbatch.comfun = simbatch_comfun.CommonFunctions(simbatch.logger)

import simbatch.core.projects as simbatch_projects
reload(simbatch_projects)
simbatch.prj = simbatch_projects.Projects(simbatch)

import simbatch.core.schemas as simbatch_schemas
reload(simbatch_schemas)
simbatch.sch = simbatch_schemas.Schemas(simbatch)

import simbatch.core.tasks as simbatch_tasks
reload(simbatch_tasks)
simbatch.tsk = simbatch_tasks.Tasks(simbatch)

import simbatch.core.queue as simbatch_queue
reload(simbatch_queue)
simbatch.que = simbatch_queue.Queue(simbatch)

import simbatch.core.nodes as simbatch_nodes
reload(simbatch_nodes)
simbatch.nod = simbatch_nodes.SimNodes(simbatch)

import simbatch.core.definitions as simbatch_definitions
reload(simbatch_definitions)
simbatch.dfn = simbatch_definitions.Definitions(simbatch)

import simbatch.core.io as simbatch_ios
reload(simbatch_ios)
simbatch.sio = simbatch_ios.StorageInOut(simbatch)
"""   force reload core  END   """

loading_data_state = simbatch.load_data()

if simbatch.sts.with_gui == 1:
    """   force reload UI """
    import simbatch.ui.ui_settings as simbatch_ui_settings
    reload(simbatch_ui_settings)
    import simbatch.ui.ui_projects as simbatch_ui_projects
    reload(simbatch_ui_projects)
    import simbatch.ui.ui_schemas as simbatch_ui_schemas
    reload(simbatch_ui_schemas)
    import simbatch.ui.ui_schemas_form as simbatch_ui_schemas_form
    reload(simbatch_ui_schemas_form)
    import simbatch.ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    import simbatch.ui.ui_tasks_forms as simbatch_ui_tasks_forms
    reload(simbatch_ui_tasks_forms)
    import simbatch.ui.ui_tasks as simbatch_ui_tasks
    reload(simbatch_ui_tasks)
    import simbatch.ui.ui_queue as simbatch_ui_queue
    reload(simbatch_ui_queue)
    import simbatch.ui.ui_definitions as simbatch_ui_definitions
    reload(simbatch_ui_definitions)
    import simbatch.ui.ui_nodes as simbatch_nodes
    reload(simbatch_nodes)
    reload(simbatch_ui)
    """   force reload UI  END   """

    simbatch_window = simbatch_ui.MainWindow(simbatch_server, parent=maya_window)
    simbatch_window.show()
    simbatch_window.post_run(loading_data_state)
