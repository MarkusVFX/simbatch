from PySide.QtGui import *

import core.core as core
import ui.mainw as ui

app = QApplication([])


sim_batch = core.SimBatch("Stand-alone")
#sim_batch.clear_all_stored_data()
#sim_batch.create_example_data()
sim_batch.load_data()
#sim_batch.print_data()
if sim_batch.s.debug_level >= 1:
    print " [INF] SimBatch initiated!"


if sim_batch.s.WITH_GUI == 1:
    main_window = ui.MainWindow(sim_batch)
    main_window.init_lists()
    main_window.show()
app.exec_()
