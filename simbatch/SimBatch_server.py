import simbatch.core.core as simbatch_core
import simbatch.server.server as simbatch_server

simbatch_config_ini = "S:/simbatch/config.ini"

no_gui_batch = simbatch_core.SimBatch("Server", ini_file=simbatch_config_ini)

sim_batch_server = simbatch_server.SimBatchServer(no_gui_batch)
sim_batch_server.run()
