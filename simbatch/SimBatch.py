from PySide.QtGui import *

import core.core as core
import ui.mainw as ui

app = QApplication([])


# sim_batch = core.SimBatch("Maya")
sim_batch = core.SimBatch("Stand-alone")
# sim_batch = core.SimBatch("xxx")
# sim_batch.clear_all_stored_data()
# sim_batch.create_example_data()
load_data_ret = sim_batch.load_data()
# sim_batch.print_data()


if sim_batch.sts.WITH_GUI == 1:
    main_window = ui.MainWindow(sim_batch)
    # main_window.init_lists()
    main_window.show()
    if load_data_ret is True:
        main_window.top_ui.set_top_info(sim_batch.sts.random_welcome_message())
    elif load_data_ret is False:
        main_window.top_ui.set_top_info("Data not loaded")
    else:
        if load_data_ret == 1:
            main_window.top_ui.set_top_info("Loaded with one data error")
        else:
            main_window.top_ui.set_top_info("Loaded with data errors ({})".format(load_data_ret))
app.exec_()
