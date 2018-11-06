from PySide.QtGui import *

import core.core as core
import ui.mainw as ui
import server.server as simbatch_server

app = QApplication([])

simbatch = core.SimBatch("Stand-alone")   # you can set startup config by changing argument: ini_file="your_config.json"
loading_data_state = simbatch.load_data()
server = simbatch_server.SimBatchServer(simbatch, force_local=True)


if simbatch.sts.WITH_GUI == 1:
    main_window = ui.MainWindow(server)
    main_window.show()
    main_window.post_run(loading_data_state)

app.exec_()
