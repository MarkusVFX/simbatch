'''   create time: 2018-06-13_01:56:16   '''
'''   create node: SimNode_01   '''


# sys append script dir    S:\update_after_3_mo\simbatch\simbatch\server\
from SimBatch_executor import * 
SiBe = SimBatchExecutor(1, 4 ) 
SiBe.addToLogWithNewLine( "Soft START: id:4  evo:evo  descr:BND:4" )  
evo_script

SiBe.finalizeQueueJob()
