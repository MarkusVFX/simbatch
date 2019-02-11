import datetime
import os
import time
import sys
import random




try:
    import hou
    self.houImportState = 1
except ImportError:
    pass
    
    
try:
    import maya.cmds as cmds
    import maya.mel as ml 
except ImportError:
    pass
    
    

class SimBatchExecutor(): 
    logHouFile = "S:\\sib_src\\SimBatch_server\\logHou.txt"
    logMayaFile = "C:\\mqs\\git\\simbatch\\simbatch\\server\\logMaya.txt"
    jobStartTime = None
    hackSimNodeName = "SimNode_01"
    
    def __init__ (self, batch, softID, queueID,  forceLocal = False ):
        self.softID = softID
        self.forceLocal = forceLocal
        self.executorQueueID  = queueID
        
        self.jobStartTime = time.time()
        
        
        self.batch = batch
        self.batch.load_data()
        self.batch.dfn.update_current_definition_by_name("Maya")
        self.addToLogWithNewLine("")
        time.sleep(1)
        self.addToLogWithNewLine("")
        
    def addToLogWithNewLine(self, logStr):
        self.addToLog (logStr, withNewLine=True)
        
    def addToLog ( self , logStr,  withNewLine=False):
        if self.softID == 1 :
            file = self.logHouFile
        else:
            file = self.logMayaFile
         
        if withNewLine:
            logStr+="\n"
            
        textFile = open(file, "a")
        textFile.write( self.getCurrentTime() + "   " + logStr )
        textFile.close() 
        
    def getCurrentTime(self, filenameMode = False):    
        if filenameMode :
            return datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        else:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def setStateAndAddToLog (self, stateName, stateID, serverName, withSave=True, addCurrentTime = False , setTime=""):
    
        self.batch.que.clear_all_queue_items()
        self.batch.que.load_queue()
        self.batch.que.update_state_and_node_name( self.executorQueueID , stateName, stateID, server_name=serverName, server_id=1, set_time=setTime, add_current_time = addCurrentTime )
        
        if self.batch.que.get_index_by_id(self.executorQueueID) > 0:
            qin = self.batch.que.queue_data[   self.batch.que.get_index_by_id(self.executorQueueID)   ].queue_item_name
            self.addToLogWithNewLine( " set "+stateName+" [" +  str( self.executorQueueID ) +  "]   "+ qin +"   by server: " +  serverName  )
        else:
            self.addToLogWithNewLine( " set "+stateName+" [" +  str( self.executorQueueID ) +  "]   by server: " +  serverName  )
        if withSave == True:
            self.batch.que.save_queue()
        
    def setQueueJobWorking (self, id, serverName, serverID, withSave = True  ):  # setStatus
        self.setStateAndAddToLog ("WORKING", 4, serverName,  withSave = withSave , addCurrentTime = True)
        
    def setQueueJobDone (self, id, serverName, serverID, withSave = True, setTime="" ):  # setStatus
        self.setStateAndAddToLog ("DONE", 11, serverName, withSave = withSave , setTime=setTime )
        
    def setQueueJobError (self, id, serverName, serverID, withSave = True ):  # setStatus
        self.setStateAndAddToLog ("ERR", 9, serverName, withSave = withSave , addCurrentTime = True )
        
    def finalizeQueueJob(self): 
        time.sleep(1)
        jobTime = str ( 0.1 * int ((  ( time.time() - self.jobStartTime )  ) * 10 )   )
        print " [INF] job time   ", jobTime
        
        self.setQueueJobDone( self.executorQueueID ,   self.hackSimNodeName, 123456 , setTime=jobTime )
       
        idx = self.batch.nod.get_node_index_by_name(self.hackSimNodeName)
        print " idx  " , idx , self.hackSimNodeName
        self.batch.nod.set_node_state_in_database ( idx, 2 )
        
        self.batch.nod.update_current_from_index(idx)
        cur_nod = self.batch.nod.current_node
        state_id = self.batch.sts.INDEX_STATE_WAITING
        self.batch.nod.create_node_state_file(cur_nod.state_file, cur_nod.node_name, state_id, update_mode=True)
        
        if self.softID == 1 :
            self.addToLogWithNewLine( "HOU Exit" )
            print " [INF] HOU Exit  " 
            self.exitHoudini()
        else :  ###  maya !!
            self.addToLogWithNewLine( "Maya Exit" )
            print " [INF] Maya Exit  " 
            self.exitMaya()
            
    def exitMaya(self): 
        #sys.exit()
        import maya.cmds as cmds
        cmds.quit(force=True)
   
        
        
        
        
        
        
        
        
        
        