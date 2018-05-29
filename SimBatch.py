from PySide.QtGui import *

import simbatch.core.core as core
import simbatch.ui.mainw as ui

app = QApplication([])

#sim_batch = core.SimBatch("Stand-alone")
sim_batch = core.SimBatch("Maya", ini_file="S:/simbatch/config.ini")
loading_data_state = sim_batch.load_data()

if sim_batch.sts.WITH_GUI == 1:
    main_window = ui.MainWindow(sim_batch)
    main_window.show()
    main_window.post_run(loading_data_state)

app.exec_()
