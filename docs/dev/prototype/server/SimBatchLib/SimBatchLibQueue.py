
from SimBatchLibCommon import * 
import random

class QueueItem():
    totalItems = 0
    maxID = 0
    
    def __init__(self, id, queueItemName, taskID, user, userID,  shotA, shotB, shotC,  frameFrom, frameTo, state, stateID, stateColor, version, evolution, evolutionNr, evolutionScriptType, evolutionScript, prior, description, simNode, simNodeID, time,  projID, softID ):
        if id > 0 :
            QueueItem.maxID = id
        else:
            QueueItem.maxID += 1
        QueueItem.totalItems += 1
        
        self.id = QueueItem.maxID
        self.queueItemName = queueItemName
        self.taskID = taskID
        self.user = user
        self.userID = userID
        self.shotA = shotA
        self.shotB = shotB
        self.shotC = shotC
        self.frameFrom = frameFrom
        self.frameTo = frameTo
        self.state = state
        self.stateID = stateID
        self.stateColor = stateColor  
        self.version = version
        self.evolution = evolution
        self.evolutionNr = evolutionNr
        self.evolutionScriptType = evolutionScriptType
        self.evolutionScript = evolutionScript
        self.prior = prior   
        self.description = description   
        self.simNode = simNode  
        self.simNodeID = simNodeID
        self.time = time 
        self.projID = projID
        self.softID = softID
    
    
class Queue():
    queueData = []
    maxID = 0
    totalQueueJobs = 0
    currentQueueIndex = -1 
    lastQueueIndex = -1 
    
    currentQueueID = -1 # noyt used ????
    
    arrayQueueIDs = []
    
    comfun = CommonFunctions()

    def __init__(self,globalSettings):
        self.s = globalSettings 
        
    
    def printAll(self):
        for q in self.queueData:
            print q.id ,   q.queueItemName  ,     q.taskID  ,     q.shotA  ,     q.shotB  ,     q.shotC  ,     q.state  
            print "        evoNR: ",   q.evolutionNr  ,      "    evoNR: ", q.evolution  ,     "    simNode: ",    q.simNode,    "   evoType: ",   q.evolutionScriptType 
            esArr = q.evolutionScript.split("|")
            for esi in esArr:
                # print "        evoScr:",   q.evolutionScript 
                print "        evoScr:",   esi 
            print "   ."
            
            
    def getQueueIndexFromID(self, getID ):
        counter = 0
        for que in self.queueData:
            if que.id == getID:
                return counter 
            counter +=1
        print "   [WRN] no queue with ID: ", getID
        return None
        
            
    def getFirstState (self, stateID ,  soft = 0 ):
        # print " [db] getFirstState    soft " , soft , "  stateID ", stateID
        index = 0
        for q in self.queueData :
            if q.stateID == stateID :
                print " [db] state : "+str(q.stateID)+"    q.softID: ",  q.softID
                if soft > 0 :
                    if q.softID == soft:
                        return [ index, self.queueData[index].id ]
                        break
                else:
                    return [ index, self.queueData[index].id ]
                    break
            index += 1
        return [-1, -1]
            
    def setState (self, id, state, stateID, serverName="", serverID=-1, setTime="", addCurrentTime = False):
        index = 0        
        for q in self.queueData :            
            if q.id == id :
                self.queueData[index].state =  state
                self.queueData[index].stateID =  stateID
                # if serverID > 0:
                self.queueData[index].simNode = serverName
                self.queueData[index].simNodeID = serverID
                
                if addCurrentTime :
                    self.queueData[index].description = "["+self.comfun.getCurrentTime(onlyTime = True)+"] "  +  self.queueData[index].description
                elif len(setTime) > 0 :
                    self.queueData[index].description = "["+setTime+"]  "  +  self.queueData[index].description
                    
                break
            index += 1
        

    def createSampleData(self,  taskID, projID ):
        softID = 3
        sampleQueue1 = QueueItem( 0, "schema tre", taskID, "M", 1, "01", "001", "a", 10, 20, "Waiting",2,"aa55ff",1, "evo01_BRN_10",1,"MXS","$Fume.burn = 10", 1 , "description 1 ", "", 0, "2017 01 04 11:11",  projID, softID ) # "sim",
        sampleQueue2 = QueueItem( 0, "schema tre", taskID, "M", 1, "01", "002", "", 10, 20, "Waiting",2,"aa55ff",40, "evo01_BRN_+10",1,"MXS","$Fume.burn += 10", 2 ,"description 2", "", 0,  "2017 02 04 12:12", projID, softID ) 
        self.addToQueue (sampleQueue1)
        self.addToQueue (sampleQueue2)
        self.saveQueueToFile()
        return self.maxID
        
    def addToQueue (self, queueItem,  doSave = False):
        if queueItem.id > 0 :
            self.maxID = queueItem.id
        else:
            self.maxID +=1
            queueItem.id = self.maxID
        
        self.queueData.append( queueItem )
        
        self.totalQueueJobs += 1

        if doSave == True :
            self.saveQueue()
            
        return True
        
        
    def updateQueueItem (self, updatedQueueItem,  doSave = False):
        if self.currentQueueIndex >= 0 :
            upQueueItem = self.queueData[self.currentQueueIndex]
            
            upQueueItem.queueItemName = updatedQueueItem.queueItemName
            upQueueItem.prior = updatedQueueItem.prior
            upQueueItem.state = updatedQueueItem.state 
            upQueueItem.description = updatedQueueItem.description 
            if doSave == True :
                self.saveQueue()
        else :
            print " [ERR] self.currentQueueIndex < 0  (none selected ???)"    
    
            
        
    def removeQueueItem (self, index = -1, id = -1 , doSave = False):
        # index = 0
        # for q in self.queueData :            
            # if q.id == id :
                # del self.queueData[index] 
                # break
            # index += 1
        if id > 0 :
            for q in self.queueData :            
                if q.id == id :
                    del self.queueData[index] 
                    break
                index += 1
        if index >= 0 :
            del self.queueData[index] 
        if doSave == True :
            self.saveQueue()
            
    def clearAllQueueItems(self):
        del self.queueData[:]
        self.maxID = 0
        self.totalQueueJobs = 0
        self.currentQueueID = -1
        self.currentQueueIndex = -1    
        self.lastQueueIndex = -1  
            
            
            
            
            
            
    def loadQueue( self ):
        if self.s.storeDataMode == 1 :
            self.loadQueueFromFile()
        if self.s.storeDataMode == 2 :
            self.loadQueueFromSqlite()
        if self.s.storeDataMode == 3 :
            self.loadQueueFromMySql()
            
            
    def loadQueueFromFile(self, file = "", dbMode = 1):
        if len(file) == 0:
            file = self.s.batchDataPath+self.s.queueFileName
        if dbMode>0:
            print " [INF] loading queue: " + file
        if self.comfun.fileExists (file, "queue file" ) :
            f = open(file, 'r')
            for line in f.readlines() :
                if len(line) > 4 :
                    li = line.split(";")
                    # self.comfun.printArray (li,  checkIsFloat = True )   # tesst copy
                    newQueueJob = QueueItem( int(li[0]), li[1], int(li[2]), li[3], int(li[4]), li[5], li[6], li[7], self.comfun.intOrVal(li[8],-1), self.comfun.intOrVal(li[9],-1), li[10], int(li[11]), li[12], int(li[13]), li[14], int(li[15]), li[16], li[17], int(li[18]) , li[19], li[20], int(li[21]), li[22], int(li[23]), int(li[24])) 
                                           #2;     Simple_Cape;  1;       M;        1;           ;        01;        ;     ;           ;Init     ;  1;5533dd;;;0;MXS;loadMaxFile "P:\SiB_SchTests\fx\Simple_Cape\base_setup\Simple_Cape_v001.max" quiet:True|;50;;;0;2017-09-13 15:51:50;2; 
                                           #6;      Emit Trails;1       ;M;         1;         01;    0010;        ;   0;            10;     Init;   1;           5533dd;    22;1;22;                      16         17         18     okkoko_22;      ;   0;        2017 07 06;      3;
                                           # 2;      sch3;      1;       M;         1;         01;    0010;      ;   40;             100;    Init;    1;          5533dd;      ; ;0;                       MXS;     ||||;     50;       ;         ;         0;        2017-08-09 02:28:21;    1; 

                    self.addToQueue(newQueueJob)
            f.close()
    
    def loadQueueFromSqlite(self, file):
        1
    def loadQueueFromMySql(self, file):
        1
        
        
    def saveQueue(self):
        if self.s.storeDataMode == 1 :
            self.saveQueueToFile()
        if self.s.storeDataMode == 2 :
            self.saveQueueToSqlite()
        if self.s.storeDataMode == 3 :
            self.saveQueueToMySql()
        
        
    def saveQueueToFile(self, file=None):
        if file==None:
            file=self.s.batchDataPath + self.s.queueFileName
        f = open(file, 'w')
        for q in self.queueData :   # "_"+(str(random.randint(100,700)))   
            f.write(  str(q.id)+';'+q.queueItemName+';'+str(q.taskID)+';'+str(q.user)+';'+str(q.userID)+';'+str(q.shotA)+';'+str(q.shotB)+';'+str(q.shotC)+';'+str(q.frameFrom)+';'+str(q.frameTo)+';'+str(q.state)+';'+str(q.stateID)+';'+str(q.stateColor)+';'+str(q.version)+';'+q.evolution+';'+str(q.evolutionNr)+';'+q.evolutionScriptType+';'+q.evolutionScript+';'+str(q.prior)+';'+str(q.description)+';'+str(q.simNode)+';'+str(q.simNodeID)+';'+str(q.time)+';'+str(q.projID)+';'+str(q.softID)+'; \n')  
        f.close()
        
    def saveQueueToSqlite(self, file):
        1
    def saveQueueToMySql(self, file):
        1

        