from PySide.QtGui import *

import simbatch.core.core as core
import simbatch.ui.mainw as ui

app = QApplication([])


sim_batch = core.SimBatch("Stand-alone")
loading_data_state = sim_batch.load_data()


if sim_batch.sts.WITH_GUI == 1:
    main_window = ui.MainWindow(sim_batch)
    # main_window.init_lists()
    main_window.show()
    if loading_data_state is True:
        main_window.top_ui.set_top_info(sim_batch.sts.random_welcome_message())
    elif loading_data_state is False:
        main_window.top_ui.set_top_info("Data not loaded")
    else:
        if loading_data_state == 1:
            main_window.top_ui.set_top_info("Loaded with one data error")
        else:
            main_window.top_ui.set_top_info("Loaded with data errors ({})".format(loading_data_state))
app.exec_()
