import sys
import core.core as simbatch_core
import server.server as simbatch_server


no_gui_batch = simbatch_core.SimBatch("Server", ini_file="config.ini")

server = simbatch_server.SimBatchServer(no_gui_batch)
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == "1" or arg == "one":
        print "  [INF] run single job : ", len(sys.argv), sys.argv[1]
        server.run(mode="single")
    else:
        print "  [WRN] unknown arg  : ", len(sys.argv), sys.argv[1]
else:
    server.run()


