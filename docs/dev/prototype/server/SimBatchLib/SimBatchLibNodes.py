
from SimBatchLibCommon import * 

class SingleNode():
    totalItems = 0
    maxID = 0
    
    def __init__(self, id, nodeName, state, stateID, color , colorUp ,stateFile, description):
        if id > 0 :
            SingleNode.maxID = id
        else:
            SingleNode.maxID += 1
        SingleNode.totalItems += 1
        
        self.id = SingleNode.maxID
        self.nodeName = nodeName
        self.state = state
        self.stateID = stateID
        self.color = color
        self.colorUp = colorUp
        self.stateFile = stateFile
        self.description = description
        
    
class SimNodes():
    totalNodes = 0 # ?
    maxID = 0  # ???
    nodesData = []
    
    lastNodeNr = -1
    currentNodeNr = -1
    
    def __init__(self,globalSettings):
        self.nodesData = []
        self.maxID = 0
        self.totalNodes = 0
        self.s = globalSettings 
        self.comfun = CommonFunctions()
        
    def printAll(self):
        for n in self.nodesData:
            print " node: ", n.nodeName, n.state, n.description
        
        
    def createSampleData(self ): # ,  schemaID, projID
        sampleNode = SingleNode(0,"Node UNO", "OFFLINE", 23,  "68a5e1",  "8533FF", "\\virta\SimBatch_server\state.txt", "virtual sample A")
        self.addNode(sampleNode)
        sampleNode2 = SingleNode(0,"Node DUO", "OFFLINE", 23,  "68a5e1",  "8533FF", "Z:\SimBatch_server\state.txt","virtual sample B")
        self.addNode(sampleNode2)
        self.saveNodesToFile()
        
    def addNode (self, singleNode):
        if singleNode.id > 0 :
            self.maxID = singleNode.id
        else:
            self.maxID +=1
            singleNode.id = self.maxID
        
        self.nodesData.append( singleNode )
        
        self.totalNodes += 1
        
        
    # def removeProject (self, id):
        # index = 0
        # for q in self.nodesData :            
            # if q.id == id :
                # del self.nodesData[index] 
                # break
            # index += 1
            
            
    def clearAllNodes (self):
        del self.nodesData[:]
        self.maxID = 0
        self.totalNodes = 0
        self.lastNodeNr = -1
        self.currentNodeNr = -1    
            
        
    def loadNodes ( self ):
        if self.s.storeDataMode == 1 :
            self.loadNodesFromFile()
        if self.s.storeDataMode == 2 :
            self.loadNodesFromSqlite()
        if self.s.storeDataMode == 3 :
            self.loadNodesFromMySql() 
            
            
            
    
    
    def loadNodesFromFile(self, file = ""):
        if len(file) == 0:
            file = self.s.batchDataPath+self.s.nodesFileName
        print " [INF] loading nodes: " + file
        if self.comfun.fileExists (file, "nodes file" ) :
            f = open(file, 'r')
            for line in f.readlines() :
                if len(line) > 4 :
                    li = line.split(";")
                    newNode = SingleNode( int(li[0]), li[1], li[2] , int(li[3]) , li[4], li[5], li[6], li[7]   ) 
                    self.addNode(newNode)                    
            f.close()
    
    def loadNodesFromSqlite(self, file):
        1
    def loadNodesFromMySql(self, file):
        1
        
        
        
    def saveNodes ( self ):
        if self.s.storeDataMode == 1 :
            self.saveNodesToFile()
        if self.s.storeDataMode == 2 :
            self.saveNodesToSqlite()
        if self.s.storeDataMode == 3 :
            self.saveNodesToMySql() 
        
    def saveNodesToFile(self, file=None):
        if file==None:
            file=self.s.batchDataPath + self.s.nodesFileName
        f = open(file, 'w')
        for p in self.nodesData :    
            f.write(  str(p.id)+';'+p.nodeName+';'+p.state+';'+str(p.stateID)+';'+p.color+';'+p.colorUp+';'+p.stateFile+';'+p.description+'; \n')
        f.close()
        
    def saveNodesToSqlite(self):
        1
    def saveNodesToMySql(self):
        1
        
        
    def checkNodesStateFiles (self):

        counter = 0
        doUpdateNodeDataFile = 0
        
        for nod in self.nodesData:
            fi = nod.stateFile
            if self.comfun.fileExists(fi," stateFile ") :
                st = self.getNodeState(fi)
                # print "\n ___ [db] noide state ", st
                
                #   iiiinnnffoo setState:  # 23 OFFLINE;   8 off(HOLD);  2  server run (WAITIG); 20 server exe (ACTIVE);  4 proces run(WORKING);  11 proc done;  9 err 
                      
                      
                curentState = "null"
                if st == 23 :    
                    curentState = "OFFLINE"
                if st == 8 :    
                    curentState = "HOLD"
                if st == 2 :    
                    curentState = "WAITING"
                if st == 20 :    
                    curentState = "ACTIVE"
                if st == 4 :    
                    curentState = "WORKING"
                if st == 5 :    
                    curentState = "SIM"
                if st == 6 :    
                    curentState = "CACHE"
                if st == 7 :    
                    curentState = "RENDER"
                if st == 11 :    
                    curentState = "DONE"
                if st == 9 :    
                    curentState = "ERROR"
                    
                doUpdateNodeData = 0
                
                if self.nodesData[counter].state != curentState:
                    doUpdateNodeData = 1 
                    
                if self.nodesData[counter].stateID != st:
                    doUpdateNodeData = 1 
                    
                if doUpdateNodeData == 1 :
                    self.nodesData[counter].state = curentState
                    self.nodesData[counter].stateID = st
                    doUpdateNodeDataFile = 1
                    print " [db]   doUpdateNodeData !  "
                
            counter += 1
            
        return doUpdateNodeDataFile
        
        
    
        
        
    def getNodeState(self, file, dbMode = 0 ):  # tryToCreateIfNotExist = False,
        # file  =  self.workingDir + self.stateFileName 
        if self.comfun.fileExists ( file, "get state file txs" ) :
            f = open(file, 'r')
            # for line in f.readlines() :
            firstLine = f.readline()
            f.close()
            if len(firstLine) > 0 :
                li = firstLine.split(";")
            else :
                li= [-1]
                if dbMode == 1:
                    print " [db] len(firstLine) : ", len(firstLine),  " ___ ", len(firstLine)
            
            stateInt = self.comfun.intOrVal(li[0],-1);
            
            if dbMode == 1:
                print " [db] get stateInt : ",  stateInt
            

            # if stateInt>0 :
            return stateInt
        else :
            return -1; 
            # if tryToCreateIfNotExist :
                # self.comfun.saveToFile ( file ,  str (0) )
                # return 0
            # else:
                # return 9
                
    def getServerNameFromFile (self,file):
        if self.comfun.fileExists ( file, "get state file txs" ) :
            f = open(file, 'r')
            # for line in f.readlines() :
            firstLine = f.readline()
            f.close()
            if len(firstLine) > 0 :
                li = firstLine.split(";")
                if len(li) > 0:
                    return li[1]
                else:
                    return ""
            else :
                if dbMode == 1:
                    print " [db] len(firstLine) : ", len(firstLine),  " ___ ", len(firstLine)
                return ""
        
        
        
        
          
         
    def setNodeState(self, file, serverName, state, dbMode=0):
        # file  =  self.workingDir + self.stateFileName 
        if self.comfun.fileExists ( file, "set state file txs" ) :
            if dbMode == 1:
                print " [db] set state : ",  state
            f = open(file, 'w') 
            f.write( str (state) +";" +  serverName  +";" + self.comfun.getCurrentTime()  )
            f.close()
        else :
            self.addToLog("[ERR] file set state not exist: " + file) 
        
        
        
        
        
        
        


        