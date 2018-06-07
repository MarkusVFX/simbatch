simbatch_config_ini = "/job/pinwheel/dev/sandbox/sandbox_msulecki/work/msulecki/tmp/simbatch_test/config.ini"

import simbatch.core.core as simbatch_core
import simbatch.server.server as simbatch_server

no_gui_batch = simbatch_core.SimBatch("Server", ini_file=simbatch_config_ini)

sim_batch_server = simbatch_server.SimBatchServer(no_gui_batch)
sim_batch_server.run()