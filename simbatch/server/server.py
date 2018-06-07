import time
import os

class SimBatchServer:
    timerDelaySeconds = 3   # delay for each loop execution
    loopsLimit = 0          # 0 infinite loop
    loopsCounter = 0        # total loop executions

    dbMode = 1    #  0 debug OFF    1 debug ON
    runExecutorState = 0  ####   0 idle   1 something to do     2 runnning      9 err
    # currentSimNodeState = -1;    #  -1 ERR   0 off   1  server run   2 server exeute    3 proces run   4 process done   9 err
    currentSimNodeState = -1;   # 23 OFFLINE   8 off(HOLD)  2  server run (WAITIG) 20 server exeutor(ACTIVE)  4 proces run  (WORKING)   11 process done   9 err

    batch = None
    forceSoftware = 0
    serverName = "SiNode_01"   # TODO  custom name on init
    serverDir = ""
    stateFileName = "state.txt"

    currentSimNodeState = None

    def __init__( self, batch ):
        self.batch = batch
        self.serverDir = os.path.dirname(os.path.realpath(__file__)) + self.batch.sts.dir_separator
        self.stateFileName   # TODO option

        self.currentSimNodeState = self.batch.nod.get_node_state( self.serverDir + self.stateFileName )
        if self.currentSimNodeState == -1:
            self.batch.comfun.save_to_file(self.serverDir+self.stateFileName,"2;"+self.serverName+";"+self.getDate())
            self.setSimNodeState(2)

        print "__init node state : ", self.currentSimNodeState

    def getDate (self):
        return time.strftime("%Y-%m-%d_%H:%M:%S")

    def setSimNodeState(self,state, dbMode = 0):
        file=self.serverDirt+self.stateFileName
        self.batch.nod.set_node_state(file, self.serverName, state, dbMode = dbMode)

    def setStateAndAddToLog (self, stateName, stateID, serverName, withSave=True, addCurrentTime = False , setTime=""):
        print " [INF] setStateAndAddToLog : ",  stateName, stateID, serverName

        self.batch.que.clearAllQueueItems()  # TODO  check REFERS ON LOCAL !!!!
        self.batch.que.loadQueue()
        self.batch.que.setState( self.executeQueueID , stateName, stateID, serverName=serverName, serverID=1, setTime=setTime, addCurrentTime = addCurrentTime )

        if self.batch.que.getQueueIndexFromID(self.executeQueueID) > 0:
            qin = self.batch.que.queueData[   self.batch.que.getQueueIndexFromID(self.executeQueueID)   ].queueItemName
            self.addToLog( " set qID "+stateName+" [" +  str( self.executeQueueID) +  "]   "+ qin +"   by server: " +  self.serverName  )
        else:
            self.addToLog( " set qID "+stateName+" [" +  str( self.executeQueueID) +  "]   by server: " +  self.serverName  )
        if withSave == True:
            self.saveUpdatedQueue()



    def setWorking (self, id, serverName, serverID, withSave = True  ):  # setStatus
        self.setStateAndAddToLog ("WORKING", 4, serverName,  withSave = withSave , addCurrentTime = True)

    def setDone (self, id, serverName, serverID, withSave = True, setTime="" ):  # setStatus
        self.setStateAndAddToLog ("DONE", 11, serverName, withSave = withSave , setTime=setTime )

    def setError (self, id, serverName, serverID, withSave = True ):  # setStatus
        self.setStateAndAddToLog ("ERR", 9, serverName, withSave = withSave , addCurrentTime = True )



    def isSomethingToDo (self, forceSoftware = 0 ):
        ret = self.batch.que.get_first_with_state(1, soft = forceSoftware)  #  TODO   cnst state from settings
        if ret[0]>=0:
            # self.executeQueueIndex = ret[0]   #  TODO   ret check and  del
            # self.executeQueueID   =  ret[1]   #  TODO   ret check and  del
            print  "\n_[db] there isSomethingToDo " , ret[0]  ,  "      ",  ret[1]  # TODO
            return (1 , ret[0], ret[1])
        else:
            return (0, None, None)

    def getJobFromQueue (self, queueID):
        index = self.batch.que.get_queue_index_by_id(queueID)
        if not index is None:
            script = self.batch.que.queue_data[index].evolutionScript
            softID = self.batch.que.queue_data[index].softID

            info = str( " id:["+str(self.batch.que.queue_data[index].id)+"] " +" evo:["+str(self.batch.que.queue_data[index].evolution)+"] "  +" descr:"+ self.batch.que.queue_data[index].description   )
            ret = [1, softID, script, info, self.batch.que.queue_data[index].id  ]
            return ret
        else:
            ret = [0,"null","","err", -1]
            return ret

    def run(self):
        self.loopsCounter += 1
        if self.loopsCounter <= self.loopsLimit  or  self.loopsLimit < 1 :
            if self.dbMode == 1:
                if self.loopsLimit > 0 :
                    print " [db] ", self.getDate(), "loop:" , self.loopsCounter  # , "    time:",  self.timerSecondsCounter
                else:
                    print " [db] ", self.getDate()

        ############   MAIN EXECUTION    ##########

        self.currentSimNodeState = self.batch.nod.get_node_state(self.serverDir + self.stateFileName )

        print "zzz self.currentSimNodeState" , self.currentSimNodeState
        print "zz2 self.serverDir + self.stateFileName " , self.serverDir , self.stateFileName

        if self.currentSimNodeState == 9 :
            self.addToLog("[ERR] file state not exist: " + file)
            print "[ERR] file state not exist: ", file



        if self.currentSimNodeState == 8 or self.currentSimNodeState == 2 :  # 2  server run (WAITIG)

            if self.currentSimNodeState == 8 :  # 8 off(HOLD)
                self.currentSimNodeState = 2
                # self.setSimNodeState(1)
                self.setSimNodeState(2)
            self.batch.que.clear_all_queue_items()
            self.batch.que.load_queue()

        is_something_to_compute = self.isSomethingToDo(forceSoftware = self.forceSoftware)
        print "\n [db1] job_to_compute  ", is_something_to_compute  # TODO

        if is_something_to_compute[0] == 1 :

            executeQueueIndex = is_something_to_compute[1]   #  TODO   ret check and  del     job_to_compute
            executeQueueID   =  s_something_to_compute[2]   #  TODO   ret check and  del
            self.setWorking ( executeQueueID, "local" , self.serverID )

            job_to_compute = self.getJobFromQueue( self.executeQueueID )
            print "job_to_compute : ", job_to_compute

            if job_to_compute[0] == 1:
                script_to_execute = self.generatePY ( 1, retJob[2], retJob[3], retJob[4] )