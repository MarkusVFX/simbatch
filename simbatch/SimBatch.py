import core.core as core
import ui.mainw as ui

sim_batch = core.SimBatch("config.ini")
main_window = ui.MainWindow(sim_batch)
main_window.init_lists()
if sim_batch.s.debug_level >= 1:
    print " [INF] SimBatch run OK"
