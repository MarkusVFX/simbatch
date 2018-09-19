import core.core as simbatch_core
import server.server as simbatch_server

no_gui_batch = simbatch_core.SimBatch("Server", ini_file="config.ini")

server = simbatch_server.SimBatchServer(no_gui_batch)
server.run()
