from PySide.QtGui import *

import core.core as core
import ui.mainw as ui
import server.server as simbatch_server

app = QApplication([])

#sim_batch = core.SimBatch("Stand-alone")

simbatch = core.SimBatch("Maya", ini_file="config.ini")
loading_data_state = simbatch.load_data()
server = simbatch_server.SimBatchServer(simbatch, force_local=True)


if simbatch.sts.WITH_GUI == 1:
    main_window = ui.MainWindow(server)
    main_window.show()
    main_window.post_run(loading_data_state)

app.exec_()
