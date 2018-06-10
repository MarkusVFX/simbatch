
import subprocess
import threading
import time
import os

from SimBatchLibCommon import CommonFunctions

class SimBatchServer :

    timerDelaySeconds = 3
    timerSecondsCounter = 0 ### not used  
    
    loopsLimit = 0    #  0 infiniti
    loopsCounter = 0 
    
    dbMode = 1    #  0 debug OFF    1 debug ON 
    runExecutorState = 0  ####   0 idle   1 something to do      2 runnning         9 err 
    
    qFile = "S:\\sib_src\\SimBatchData\\data_Queue.txt"
    serverDir = "S:\\sib_src\\SimBatch_server\\"   #  workingDir
    logFileName = "log.txt"
    stateFileName = "state.txt"
    
    serverName="SiNode_01"
    serverID = 1
    
    jobStartTime = None
    
    
    
    houdiniExeFilePath = "\"C:\\Program Files\\Side Effects Software\\Houdini 15.5.717\\bin\\houdinifx.exe\""   # !!!!!!   TU DO CHECK Exist !!!!!
    
    mayaExeFilePath = "\"C:\\Program Files\\Autodesk\\Maya2016\\bin\\mayapy.exe\""   # !!!!!!   TU DO CHECK Exist !!!!!
    # mayaExeFilePath = "\"C:\\Program Files\\Autodesk\\Maya2016\\bin\\mayabatch.exe\""   # !!!!!!   TU DO CHECK Exist !!!!!    

    
    maxExeFilePath = "C:\\Program Files\\Autodesk\\3ds Max 2016\\3dsmax.exe"
    maxExeFilePath = "\"C:\\Program Files\\Autodesk\\3ds Max 2016\\3dsmax.exe\""   # !!!!!!   TU DO CHECK Exist !!!!!
    
    
    
    # currentSimNodeState = -1;    #  -1 ERR   0 off   1  server run   2 server exeute    3 proces run   4 process done   9 err  
    currentSimNodeState = -1;   # 23 OFFLINE   8 off(HOLD)  2  server run (WAITIG) 20 server exeutor(ACTIVE)  4 proces run  (WORKING)   11 process done   9 err 
                        
    
    comfun = CommonFunctions()
    
    s = None
    q = None
    n = None
    soCo = None
    
    # self.inside3Dsoft = 0
    # currentSoftware = 0
    forceSoftware = 0 
    forceLocal = False
    
    def __init__( self, settings, queue, simNodes, soCo, forceLocal = False  ): 
        self.s = settings
        self.s.storeDataMode = 1
        self.q = queue
        self.n = simNodes   ##  SimNodes(self.s)
        self.soCo = soCo
        
        self.forceLocal = forceLocal
        
        self.jobStartTime = time.time()
        
        # if comfun.fileExists ( self.serverDir + self.stateFileName ) :
            
        self.currentSimNodeState = self.n.getNodeState( self.serverDir + self.stateFileName ) #  , tryToCreateIfNotExist = True)
        if self.currentSimNodeState == -1 :
            self.comfun.saveToFile ( self.serverDir + self.stateFileName ,  str (2)+";"+self.serverName+";"+  self.getDate() )
            self.setSimNodeState(2)
            
           
        if forceLocal == True:
            print "SimBatchServer local mode"
        else:
            self.addToLog( "\n\n[INF]  SimBatchServer starts : " + self.getDate()+ "   "+  self.serverName+"   "+ str(self.currentSimNodeState)  )
         
    

        
    def setSimNodeState(self,state, dbMode = 0):   ####  setState
        file  =  self.serverDir + self.stateFileName 
        self.n.setNodeState(file, self.serverName, state, dbMode = dbMode)
        
    def getDate (self):
        return time.strftime("%Y-%m-%d_%H:%M:%S") 
    
    def addToLog (self, info, file=None):
        date = self.getDate ()
        if file==None:
            file=self.serverDir + self.logFileName
        
        f = open(file, 'a')  
        f.write( date + info +'; \n')
        f.close() 
        if self.dbMode == 1:
            print "[LOG] " , info
        
        if not self.comfun.fileExists (file, "server log file" ) :
            print "ERROR log file ", file
    
    def readQueueFile (self, file=None):
        if file==None:
            file = self.qFile
        # print " [INF] loading queue: " + file
        
        if self.comfun.fileExists (file, "server queue file" ) :
            self.q.loadQueueFromFile ( file = file, dbMode=0 )
    
    def isSomethingToDo (self, forceSoftware = 0 ):
        # ret = self.q.getFirstState("INIT")
        ret = self.q.getFirstState(1, soft = forceSoftware)
        if ret[0]>=0:
            self.executeQueueIndex = ret[0]
            self.executeQueueID   =  ret[1]
            print  "\n_[db] there isSomethingToDo " , self.executeQueueID  ,  "      ",  self.executeQueueIndex
            return 1 
        else:
            return 0
            
    def getJobFromQueue (self, queueID):
        # queueID
        index = self.q.getQueueIndexFromID (queueID)
        if not index is None:
            # scriptOut = ""
            script = self.q.queueData[index].evolutionScript
            softID = self.q.queueData[index].softID
            # type = self.q.queueData[index].evolutionScriptType
            # if type =="MXS" :
                # soft = "max"
            # else:
                # if type =="MEL" :
                    # soft = "maya"
                # else : # type =="PY"
                    # soft = "hou"
            
            
            
            # print "\n\n\n  vzzzziii job str(id) " , str(self.q.queueData[index].id) , "\n\n\n"
            # print "\n\n\n  vzzzziii job .description " , self.q.queueData[index].description , "\n\n\n"
            # print "\n\n\n  vzzzziii job descr " , str(index) , "\n\n\n"
            # print "\n\n\n  vzzzziii job descr " ,   str( "["+str(self.q.queueData[index].id)+"] " + self.q.queueData[index].description )     , "\n\n\n"
            
            info = str( " id:["+str(self.q.queueData[index].id)+"] " +" evo:["+str(self.q.queueData[index].evolution)+"] "  +" descr:"+ self.q.queueData[index].description   )
            ret = [1,softID, script, info,  self.q.queueData[index].id  ]
            return ret
        else:
            ret = [0,"null","","err", -1]
            return ret
            
            
    def saveUpdatedQueue (self, file=None):
        if file==None:
            file = self.qFile
        print " [INF] save queue : " + file
        self.q.saveQueueToFile(file = file )
        
        
        
        
        
    def saveUpdatedQueue (self, file=None):
        if file==None:
            file = self.qFile
        # print " [INF] save queue : " + file
        self.q.saveQueueToFile(file = file )
        
    def setStateAndAddToLog (self, stateName, stateID, serverName, withSave=True, addCurrentTime = False , setTime=""):
        print " [INF] setStateAndAddToLog : ",  stateName, stateID, serverName
        
        self.q.clearAllQueueItems()  ###   check REFERS ON LOCAL !!!! tudu
        self.q.loadQueue()
        self.q.setState( self.executeQueueID , stateName, stateID, serverName=serverName, serverID=1, setTime=setTime, addCurrentTime = addCurrentTime )
        
        if self.q.getQueueIndexFromID(self.executeQueueID) > 0:
            qin = self.q.queueData[   self.q.getQueueIndexFromID(self.executeQueueID)   ].queueItemName
            self.addToLog( " set qID "+stateName+" [" +  str( self.executeQueueID) +  "]   "+ qin +"   by server: " +  self.serverName  )
        else:
            self.addToLog( " set qID "+stateName+" [" +  str( self.executeQueueID) +  "]   by server: " +  self.serverName  )
        if withSave == True:
            self.saveUpdatedQueue()
        
    def setWorking (self, id, serverName,serverID, withSave = True  ):  # setStatus
        self.setStateAndAddToLog ("WORKING", 4, serverName,  withSave = withSave , addCurrentTime = True)
        
    def setDone (self, id, serverName,serverID, withSave = True, setTime="" ):  # setStatus
        self.setStateAndAddToLog ("DONE", 11, serverName, withSave = withSave , setTime=setTime )
        
    def setError (self, id, serverName,serverID, withSave = True ):  # setStatus
        self.setStateAndAddToLog ("ERR", 9, serverName, withSave = withSave , addCurrentTime = True )
        
            
            
            
            
            
    
    # def setWorking (self, id, serverName,serverID, withSave = True ):  # setStatus
        # self.q.setState(id, "WORKING", 4, serverName=serverName, serverID=1, addCurrentTime = True)
        # self.addToLog( " set working [" +  str( self.executeQueueID) +  "]   "+  self.q.queueData[self.executeQueueIndex].queueItemName+"   by server: " +  self.serverName  )
        # if withSave == True:
            # self.saveUpdatedQueue()
    # def setDone (self, id, serverName,serverID, withSave = True ):  # setStatus
        # self.q.setState(id, "DONE", 11, serverName=serverName, serverID=1)
        # self.addToLog( " set DONE [" +  str( self.executeQueueID) +  "]   "+  self.q.queueData[self.executeQueueIndex].queueItemName+"   by server: " +  self.serverName  )
        # if withSave == True:
            # self.saveUpdatedQueue()
    # def setError (self, id, serverName,serverID, withSave = True ):  # setStatus
        # self.q.setState(id, "ERR", 9, serverName=serverName, serverID=1)
        # self.addToLog( " set ERR [" +  str( self.executeQueueID) +  "]   "+  self.q.queueData[self.executeQueueIndex].queueItemName+"   by server: " +  self.serverName  )
        # if withSave == True:
            # self.saveUpdatedQueue()
    

    

    
    
    def generatePyHoudini (self, pyFile, jobScript, jobDescription, jobID, local=False  ):   ##   mmm  houdini -foreground
    
        scrtipOut="'''  generate time : "+ self.getDate() +"'''\n'''  generate node : "+  self.serverName +"'''\n\n"
        scrtipOut+="\nfrom SimBatch_executor import * \nSiBe = SimBatchExecutor( 1 , "+ str(self.executeQueueID) +" ) "        ####      SimBatchExecutor( 1 )  ###  1 hou !!!!!
        scrtipOut+="\nSiBe.addToLogWithNewLine( \"Houdini START:"+ jobDescription  +"\" )  \n"
        
        scriptLines = jobScript.split("|")
        for li in scriptLines :
            lislash = li.replace('\\', '\\\\')
            scrtipOut += lislash + "\n"
            
            
        scrtipOut+="\nSiBe.finalizeQueueJob()  \n"
        
        
        
        self.comfun.saveToFile ( pyFile, scrtipOut )
        return scrtipOut
        
        
    def generatePyMaya(self, pyFile, jobScript, jobDescription, jobID, local=False  ):   ##   mmm  houdini -foreground
    
        scrtipOut="'''  generate time : "+ self.getDate() +"'''\n'''  generate node : "+  self.serverName +"'''\n\n"
        scrtipOut+="\nfrom SimBatch_executor import * \nSiBe = SimBatchExecutor( 2 , "+ str(self.executeQueueID) +" ) "        ####      SimBatchExecutor( 1 )  ###  1 hou !!!!!
        scrtipOut+="\nSiBe.addToLogWithNewLine( \"Maya START:"+ jobDescription  +"\" )  \n"
        
        scriptLines = jobScript.split("|")
        for li in scriptLines :
            lislash = li.replace('\\', '\\\\')
            scrtipOut += lislash + "\n"
            
        scrtipOut+="\nSiBe.finalizeQueueJob( soft = 2 )  \n"
        
        self.comfun.saveToFile ( pyFile, scrtipOut )
        return scrtipOut
    
       
    def generateMaxScript (self, maxScriptFile, jobScript, jobDescription, jobID, local=False  ):
        
        scrtipOut="---  generate time : "+ self.getDate() +"\n---  generate node : "+  self.serverName +"\n\n"
        scrtipOut+="\n global SimBatchExecutorState = 0  "        
        scrtipOut+="\n try ( \n   filein ( @\"" + self.serverDir + "SimBatch_executor.ms\"" + ") \n   SimBatchExecutorState = 1 \n ) catch ()  \n\n"  # include  "S:\\sib_src\\SimBatch_server\\SimBatch_executor.ms"
        scrtipOut+="\n try( \n\n if SimBatchExecutorState == 1 do \n  (  \n    SiBe = SimBatchExecutor()\n    SiBe.addToLogWithNewLine( \"MAX START:"+ jobDescription  +"\" )  \n  ) \n\n"
        
        scriptLines = jobScript.split("|")
        for li in scriptLines :
            scrtipOut += "   "+li + "\n"
           
        if local == False:
            # scrtipOut+="\n  \n\n if SimBatchExecutorState == 1 do \n  (  \n    SiBe = SimBatchExecutor()\n    SiBe.addToLog( \"MAX FINISH:"+ jobDescription  +"\" )  \n  SiBe.setHoldNodeState() \n  ) \n\n "
            scrtipOut+="\n  \n\n if SimBatchExecutorState == 1 do \n  (  \n    SiBe = SimBatchExecutor()\n    SiBe.addToLog( \"MAX FINISH:"+ jobDescription  +"\" )  \n    SiBe.setHoldNodeState() \n    SiBe.setQueueState \"Done\"  11  "+ str(jobID) +" \n   ) \n\n "   #  SiBe.setQueueState( "Done", 11, 58 ) 
        
            scrtipOut+="\n ) catch ( \n\n  if SimBatchExecutorState == 1 do \n  (  \n    SiBe = SimBatchExecutor()\n    SiBe.addToLog( \"ERR:"+ jobDescription  +"\" )  \n    SiBe.setErrorNodeState() \n  ) \n\n) \n "
            scrtipOut+="\n\n\n quitMax #noPrompt"
        else : ####   skip   :     SiBe.setHoldNodeState() \n
            scrtipOut+="\n  \n\n if SimBatchExecutorState == 1 do \n  (  \n    SiBe = SimBatchExecutor()\n    SiBe.addToLog( \"MAX FINISH:"+ jobDescription  +"\" )  \n   ) \n\n "
            scrtipOut+="\n ) catch ( \n\n  if SimBatchExecutorState == 1 do \n  (  \n    SiBe = SimBatchExecutor()\n    SiBe.addToLog( \"ERR:"+ jobDescription  +"\" )  \n   ) \n\n) \n "
        
        
        self.comfun.saveToFile ( maxScriptFile, scrtipOut )
        return scrtipOut
        


        
    def runHoudiniWithScript (self, pythonFile):    # mmm    
        try:
            print "\n\n run Houdini with ",  pythonFile , "\n\n"
            # comm = self.houdiniExeFilePath + " -foreground " + pythonFile      #####   houdinifx.exe     waitforui
            comm = self.houdiniExeFilePath + " -apprentice   " + pythonFile      #####   houdinifx.exe        -foreground  MAC  linux
            subprocess.Popen(  comm , shell = True )
        except:
            print " [ERR] Houdini run !!!! \n\n",  pythonFile
            pass
            
            
        
    def runMayaWithScript (self, scriptFile):
        try:
            print "\n\n run Maya with ",  scriptFile , "\n\n"
            comm = self.mayaExeFilePath + " -script " + scriptFile   #  mayabatch
            subprocess.Popen(  comm , shell = True )
        except:
            print " [ERR] Maya run !!!! \n\n",  scriptFile
            pass
        
    def runMaxWithScript (self, maxScriptFile):
        try:
            print "\n\n run 3dsMAX with ",  maxScriptFile , "\n\n"
            comm = self.maxExeFilePath + " -q -mip -silent -u MAXScript " + maxScriptFile
            subprocess.Popen(  comm , shell = True )
        except:
            print " [ERR] 3dsMAX run !!!! \n\n",  maxScriptFile
            pass
            
            
    def executeHoudini (self, jobScript , jobDescription, jobID ):
    
        pyFile = self.serverDir + "localPY.py"
        self.generatePyHoudini( pyFile, jobScript, jobDescription, jobID, local = True )
        
        self.runHoudiniWithScript(pyFile)
        
    def executeMaya (self, jobScript , jobDescription, jobID):
        pyFile = self.serverDir + "localPY.py"
        self.generatePyMaya( pyFile, jobScript, jobDescription, jobID, local = True )
        
        self.runMayaWithScript(pyFile)
        
    def executeMAX (self, jobScript , jobDescription, jobID ):
    
        ##### def mxs !!!!!
        maxScriptFile = self.serverDir + "runMXS.ms"
        mxs = self.generateMaxScript( maxScriptFile, jobScript, jobDescription, jobID )
        
        self.runMaxWithScript(maxScriptFile)
        
    def generateMXS(self, jobScript , jobDescription, jobID ):
    
        ##### only mxs !!!!!
        maxScriptFile = self.serverDir + "localMXS.ms"
        mxs = self.generateMaxScript( maxScriptFile, jobScript, jobDescription, jobID, local = True )
        
        return maxScriptFile
        
    def generatePY (self, softID, jobScript , jobDescription, jobID ):
        pyFile = self.serverDir + "localPY.py"
        if softID == 1 :
            self.generatePyHoudini( pyFile, jobScript, jobDescription, jobID, local = True )
        if softID == 2 :
            self.generatePyMaya( pyFile, jobScript, jobDescription, jobID, local = True )
        
        return pyFile
        
    
    
    
    
        
    # def executeScript (self):
        # 1
    # def executeRF (self):
        # 1
     
        
    def finish (self):
        if self.currentSimNodeState == 2:
            # self.setSimNodeState(0)
            # self.setSimNodeState(23)   #  9 ERR   23 off(LINE) 2  server run (WAITIG) 20 server exeutor(ACTIVE)  4 proces run  (WORKING)   11 process done   9 err 
            

            # self.setSimNodeState(3)              #  -1 ERR   0 off        1  server run          2 server exeutor           3 proces run      4 process done    9 err
            self.setSimNodeState(8, dbMode  = 1 )  # 23 OFFLINE   8 off(HOLD)  2  server run (WAITIG) 20 server exeutor(ACTIVE)  4 proces run  (WORKING)   11 process done   9 err 
                        
            
                        
            self.addToLog( "\n[INF]  Executor normal exit : " + self.getDate()+ "   "+  self.serverName+"   "+ str(self.currentSimNodeState)  +"\n"   )
        else:
            self.addToLog( "\n[INF]  Executor exit with working state : " + self.getDate()+ "   "+  self.serverName+"   "+ str(self.currentSimNodeState) +"\n"  )
          

    def getSiBeParams (self, line ) :
        # retArr = []
        print "\n"
        print " ____  line " , line , len(line)
        print "\n"
        li1 = line.replace('"', '')
        li2 = li1.split( "(" )
        li3 = li2[1].split ( ")" )
        li4 = li3[0].split( "," )
        li4.append("")
        li4.append("")
        li4.append("")
        li4.append("")
        li4.append("")  #####   arrr elements param exist
        return li4
          
            
    def runSimOne (self , forceSoftware = 0 ):  ####   local node !!!!!     ####   SimBatchExecutor    forceLocal = True
        if self.dbMode == 1:
            print "\n [db1] ", self.getDate(), "loop:" , self.loopsCounter  # , "    time:",  self.timerSecondsCounter
        
        # retToDo = self.isSomethingToDo( forceSoftware = self.forceSoftware  )   ###   ---  >>>   self.executeQueueID
        retToDo = self.isSomethingToDo( forceSoftware = forceSoftware  )   ###   ---  >>>   self.executeQueueID
        
        if self.dbMode == 1:
            print "\n [db1] retToDo  " , retToDo
            
        if retToDo == 1 :
            
            self.setWorking ( self.executeQueueID, "local" , self.serverID )  ##   withSave = True
            
            retJob = self.getJobFromQueue( self.executeQueueID )
            
            if retJob[0] == 1:
                if retJob[1] == 1: #"hou":
                    pyHouScriptFile = self.generatePY ( 1, retJob[2], retJob[3], retJob[4] )
                    
                    from SimBatch_executor import SimBatchExecutor 
                    SiBe = SimBatchExecutor( 1,  self.executeQueueID , forceLocal = True ) 
                    jobDescription = retJob[4]
                    SiBe.addToLogWithNewLine( "local Houdini START:"+ str( jobDescription )  ) 
        
                    jobScript = retJob[2]
                    scriptLines = jobScript.split("|")
                    for li in scriptLines :
                        if len(li) > 10 :
                            paramsArr = self.getSiBeParams (li)
                            char5 = li[5]             
                            char6 = li[6]
                            
                            
                            if char5 == "a" :   # SiBe.addToLogWithNewLine( "HOU START: id:[39]  evo:[(7) LFT_7.0]  descr:" ) 
                                SiBe.addToLogWithNewLine( paramsArr[0] )  
                            if char5 == "l" :    # SiBe.loadHoudini ( "P:\SiB_SimpleBurn\fx\burn\base_setup\burn_v001.hip" ) 
                                SiBe.loadHoudini( paramsArr[0] )  
                            if char5 == "p" :    # SiBe.paramHoudini ( "pyro1" , "lift" , "7.0"  ) 
                                SiBe.paramHoudini( paramsArr[0],paramsArr[1],paramsArr[2] ) 
                            if char5 == "s"  and  char6 =="i":   # SiBe.simulateHoudini ( "pyro1" ) 
                                SiBe.simulateHoudini( paramsArr[0],paramsArr[1],paramsArr[2] ) 
                                
                            if char5 == "r" :  # SiBe.renderHoudini( 123 , 123 , outFile="P:\SiB_SimpleBurn\fx\burn\prevs\burn__v004_evo07\burn__v004_evo07__.png"  ) 
                                if paramsArr[2][:8] == "outFile=" :
                                    SiBe.renderHoudini( paramsArr[0],paramsArr[1], outFile = paramsArr[2][8:] ) 
                                else:
                                    SiBe.renderHoudini( paramsArr[0],paramsArr[1]  ) 
                                
                            if char5 == "s"  and  char6 =="a":   # SiBe.saveHoudini( "P:\SiB_SimpleBurn\fx\burn\computed_setups\burn__v004_evo07.hip" )  
                                SiBe.saveHoudini( paramsArr[0] )  
                     
                    
                    
                if retJob[1] == 2: # "maya":
                    pyMayaScriptFile = self.generatePY ( 2, retJob[2], retJob[3], retJob[4] )
                    
                    from SimBatch_executor import SimBatchExecutor 
                    SiBe = SimBatchExecutor( 1,  self.executeQueueID , forceLocal = True ) 
                    jobDescription = retJob[4]
                    SiBe.addToLogWithNewLine( "local Maya START:"+ str( jobDescription )  ) 
        
                    jobScript = retJob[2]
                    scriptLines = jobScript.split("|")
                    

                    for li in scriptLines :
                        if len(li) > 10 :
                            paramsArr = self.getSiBeParams (li)
                            char5 = li[5]             
                            char6 = li[6]
                            

                            print "\nparams QWA :  ",  paramsArr[0],paramsArr[1],paramsArr[2]
                            print "\n  "
                            
                            
                            if char5 == "a" :   # SiBe.addToLogWithNewLine( "HOU START: id:[39]  evo:[(7) LFT_7.0]  descr:" ) 
                                SiBe.addToLogWithNewLine( paramsArr[0] ) 
                            if char5 == "o" :   # SiBe.openMaya( "P:\\SiB_PromoAnim\\fx\\U_14\\base_setup\\U_14_v001.mb" )  
                                SiBe.openMaya ( paramsArr[0] )
                            if char5 == "i" :   # SiBe.importMaya( "def_o" ) 
                                SiBe.importMaya (paramsArr[0])
                                # playbackOptions -min 1 -max 75 ;
                                import maya.cmds as cmx
                                cmx.playbackOptions ( minTime = 1, maxTime = 70, animationStartTime = 1, animationEndTime = 70)
                            if char5 == "n" :   # SiBe.nClothSim( "Ufok_T__cape",123,123  ) 
                                SiBe.nClothSim ( paramsArr[0],paramsArr[1],paramsArr[2] ) 
                            if char5 == "xr" :   # SiBe.renderMaya( 123 , 123 , outFile="P:\\SiB_PromoAnim\\fx\\U_14\\prevs\\01_005\\U_14__01_005__v002\\U_14__01_005__v002__.png"  )
                                hackfile = paramsArr[2][8:].replace('\\', '\\\\')
                                SiBe.renderMaya( paramsArr[0],paramsArr[1], outFile = hackfile ) 
                            if char5 == "xs" :   # SiBe.saveMaya( "P:\\SiB_PromoAnim\\fx\\U_14\\computed_setups\\01_005\\U_14__01_005__v002.mb" ) 
                                hackfile = paramsArr[0].replace('\\', '\\\\')
                                SiBe.saveMaya( hackfile ) 
                                
                            schemaHack = "CapeTest"   ###   HAckl      "+schemaHack+"
                            
                            if char5 == "r" :   
                                SiBe.renderMaya( 123 , 123 , outFile="P:\\SiB_MultipleShots\\fx\\"+schemaHack+"\\prevs\\01_010\\"+schemaHack+"__01_010__v001\\"+schemaHack+"__01_010__v001__.png"  )
                            if char5 == "s" :
                                SiBe.saveMaya( "P:\\SiB_MultipleShots\\fx\\"+schemaHack+"\\computed_setups\\01_010\\"+schemaHack+"__01_010__v001.mb" ) 
                            # if char5 == "r" :   
                                # SiBe.renderMaya( 123 , 123 , outFile="P:\\SiB_MultipleShots\\fx\\"+schemaHack+"\\prevs\\01_010\\"+schemaHack+"__01_010__v002\\"+schemaHack+"__01_010__v002__.png"  )
                            # if char5 == "s" :
                                # SiBe.saveMaya( "P:\\SiB_MultipleShots\\fx\\"+schemaHack+"\\computed_setups\\01_010\\"+schemaHack+"__01_010__v001.mb" ) 

                            # if char5 == "r" :   
                                # SiBe.renderMaya( 123 , 123 , outFile="P:\\SiB_MultipleShots\\fx\\dwawda\\prevs\\01_005\\dwawda__01_005__v001\\dwawda__01_005__v001__.png"  )
                            # if char5 == "s" :
                                # SiBe.saveMaya( "P:\\SiB_MultipleShots\\fx\\dwawda\\computed_setups\\01_005\\dwawda__01_005__v001.mb" ) 

                
                
                    1
                if retJob[1] == 3: # "max":
                    maxScriptFile = self.generateMXS ( retJob[2], retJob[3], retJob[4] )                    
                    
                    # self.soCo.evalMaxScript ( ' include  "'+ maxScriptFile +'"' )
                    self.soCo.evalMaxScript ( ' filein  ("'+ maxScriptFile +'")' ) 
                    print "  [INF]  Done Job  " ,  retJob[2],  " \n"
                    
                    
                jobTime = str ( 0.1 * int ((  ( time.time() - self.jobStartTime )  ) * 10 )   )    
                self.setDone ( self.executeQueueID, "local" , self.serverID,  setTime = jobTime )    ##   withSave = True
                
                return 1
            else:
                print "  [ERR]  retJob \n"
                return -1
                
        else:
            print "  [INF] Nothing to do \n"
            return 0
            
            
            
    
            
    def run(self):
        self.loopsCounter += 1
        if self.loopsCounter <= self.loopsLimit  or  self.loopsLimit < 1 : 
            if self.dbMode == 1:
                if self.loopsLimit > 0 :
                    print " [db] ", self.getDate(), "loop:" , self.loopsCounter  # , "    time:",  self.timerSecondsCounter
                else:
                    print " [db] ", self.getDate()
          
            ############   MAIN EXECUTION    ##########
            
            
            self.currentSimNodeState = self.n.getNodeState(  self.serverDir + self.stateFileName )
            if self.currentSimNodeState == 9 :
                self.addToLog("[ERR] file state not exist: " + file) 
                print "[ERR] file state not exist: ", file 
            
            
            if self.currentSimNodeState == 8 or self.currentSimNodeState == 2 :  # 2  server run (WAITIG)
            
                if self.currentSimNodeState == 8 :  # 8 off(HOLD)  
                    self.currentSimNodeState = 2
                    # self.setSimNodeState(1)
                    self.setSimNodeState(2) 
                self.q.clearAllQueueItems()
                self.readQueueFile()
            
            
                retToDo = self.isSomethingToDo( forceSoftware = self.forceSoftware  )   ####    currentSoftware
                
                if retToDo == 1 :
                
                    # lock file !!!
                    self.currentSimNodeState = 20
                    # self.setSimNodeState(2) 
                    self.setSimNodeState(20) 
                    
                    self.setWorking ( self.executeQueueID, self.serverName, self.serverID )
                    self.saveUpdatedQueue()
                    
                        ##   set task !!!!
                        # self.setWorking ( self.executeQueueID, "local" , self.serverID )  ##   withSave = True
                    
                    retJob = self.getJobFromQueue( self.executeQueueID )
                    
                    # afterExecuteState = -1
                    
                    if retJob[0] == 1:
                        self.currentSimNodeState = 3
                        # self.setSimNodeState(3)   #  -1 ERR   0 off        1  server run          2 server exeutor           3 proces run      4 process done    9 err
                        self.setSimNodeState(4)  # 23 OFFLINE   8 off(HOLD)  2  server run (WAITIG) 20 server exeutor(ACTIVE)  4 proces run  (WORKING)   11 process done   9 err 

                        
                        
                        
                        if retJob[1] == 1 :   # "hou":
                            self.executeHoudini ( retJob[2],retJob[3], retJob[4]  )  ###  jobScript , jobDescription, jobID
                            # afterExecuteState = 11 ###   tu du !!!!!  HACK
                            
                        if retJob[1] == 2 :   #"maya":
                            self.executeMaya ( retJob[2],retJob[3], retJob[4]  )  ###  jobScript , jobDescription, jobID
                            
                            
                        if retJob[1] == 3 :   #"max":
                            self.executeMAX ( retJob[2],retJob[3], retJob[4]  )
                            # afterExecuteState = 11 ###   tu du !!!!!  HACK
                    else:
                        self.currentSimNodeState = 9
                        self.setSimNodeState(9)  
                        print "\n\n SIM NODE ERR !!!\n\n"
                        
                        
                        
                        
                    ######      afterExecuteState      STATE CHANGED BY EXERCUTOR
                    # if afterExecuteState > 0 and afterExecuteState != 9 :  
                        # self.setDone ( self.executeQueueID, self.serverName, self.serverID )
                    # else: 
                        # self.setError( self.executeQueueID, self.serverName, self.serverID )
                else:
                    print "  [INF] Nothing to do ......   " ,  self.getDate(), "\n"
            else:
                if self.currentSimNodeState == 9 :
                    print "  [INF] sim node ERROR [err_code:23] !!! \n"
                else :
                    print "  [INF] sim node looks bussy \n"
                
            
            ############   MAIN EXECUTION  FIN  ##########
            checkBreak = self.comfun.fileExists(self.serverDir+"break.txt", "")
            # print "checkBreak ", checkBreak
            if checkBreak :
                #####  BREAK LOOP
                print " [INF]  BREAK MAIN LOOP !"
                os.rename(self.serverDir+"break.txt", self.serverDir+"break___.txt")                
            else:
                threading.Timer(    self.timerDelaySeconds    ,   self.run ).start() 
            
            
            
        else :   # exit 
            self.finish()
        
        