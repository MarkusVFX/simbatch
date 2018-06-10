
import datetime
import os
import time
import sys

import random


try:
    import hou
    import hou
except ImportError:
    print "no hou"
    pass




class SimBatchExecutor ():

    softID = 0 
    stateFile = "S:\\sib_src\\SimBatch_server\\state.txt"
    qFile = "S:\\sib_src\\SimBatchData\\data_Queue.txt"
    logHouFile = "S:\\sib_src\\SimBatch_server\\logHou.txt"
    logMayaFile = "S:\\sib_src\\SimBatch_server\\logMaya.txt" 
    
    hackSimNodeName = "SiNode_01"  ####   hack
    
    forceLocal = False
    
    q = None
    n = None
    
    executorQueueID = -1 
    
    jobStartTime = ""
    
    def __init__ ( self, softID, queueID,  forceLocal = False ):
        self.softID = softID
        self.forceLocal = forceLocal
        
        self.executorQueueID  = queueID
        
        self.jobStartTime = time.time()
        
        
        
        if forceLocal == False:
        
        
            # maya test  out  HACK
            # import sys, os
            # sys.path.append ("S:\\sib_src\\SimBatch_server\\")
            # maya test  out 


            
            from SimBatchLib.SimBatchLibSettings import Settings
            # from SimBatchLib.SimBatchLibQueue import *            
            # from SimBatchLib.SimBatchLibNodes import *
            
            from SimBatchLib.SimBatchLibQueue import Queue , QueueItem
            
            from SimBatchLib.SimBatchLibNodes import SimNodes, SingleNode
            Queue
            # from SimBatchLib.SimBatchLibSoftwares import *
            settings = Settings(0)
            settings.loadSettings ("S:\\sib_src\\dataStore.ini")
            self.q = Queue( settings )
            self.n = SimNodes( settings )
        
        
    def getCurrentTime(self, filenameMode = False):
        if filenameMode :
            return datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        else:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            
    def isfloat(self,value):
      try:
        float(value)
        return True
      except:
        return False  
        
            
    def intOrVal (self, inVal, defVal, db=False ):
        if self.isfloat ( inVal ):
            if db :
                print "[db intOrVal ] is float",  inVal, defVal
            return int(inVal)
        else:
            if db :
                print "[db intOrVal ] is float",  inVal, defVal
            return defVal 
            
    def strWithZeros (self, number, zeros=3 ):
        stri = str(number)
        while len(stri)<zeros:
            stri="0"+stri
        return stri
            
            
    
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
    

    def addToLogWithNewLine (self, logStr ):
        self.addToLog (logStr, withNewLine=True)


    def loadHoudini (self, fileName ) :
        print " \n loadHoudini : " , fileName
        fileName = fileName.replace('\\', '/')
        print " \n loadHoudini FIX : " , fileName
        print " \n\n\n " 
        hou.hipFile.load ( fileName , suppress_save_prompt=True, ignore_load_warnings=True )
        
        if self.forceLocal :
            time.sleep(1)
            hou.ui.triggerUpdate()
            time.sleep(1)
        
    def importHoudini (self, fileName ) :
        1
        
    def paramHoudini (self, obj, param, val ) :
        print "\n\n\n"
        print "  GET PARAM : ", obj, param, val
        print "\n\n\n"
        # SiBe.paramHoudini("pyro_import","burn","3.0")
        z = hou.node("/obj/pyro_sim/pyrosolver1/") 
        # print "\n", z.evalParm('temp_diffusion')
        # z.parm('lift').set(4)
        z.parm( param ).set( val )
        
    def simulateHoudini (self, objectName, ts , te ) :
        
        frStart  = self.intOrVal ( ts , 0 )
        frEnd  = self.intOrVal ( te , 0 )
        print "\n\n\n"
        print "  SIM : ", objectName ,  frStart , frEnd
        print "\n\n\n"
        
        setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (frStart,frEnd)
        setGobalFrangeExpr = 'tset `({0}-1)/$FPS` `{1}/$FPS`'.format(frStart,frEnd)
        hou.hscript(setGobalFrangeExpr)
        hou.playbar.setPlaybackRange( frStart, frEnd)
        hou.setFrame (frStart)
        
        hou.node('/obj/pyro_sim/output').parm("execute").pressButton()
        
        if self.forceLocal :
            time.sleep(1)
            hou.setFrame (frStart+ int(  (frStart - frEnd)/2  ) )
            hou.ui.triggerUpdate()
            time.sleep(1)
        
        ####   HACK   !!!!
        


    def renderHoudini (self, ts, te, outFile="" ) :
        print "\n\n\n"
        print "  REND : ",  ts, te, outFile , "_____!"
        print "\n\n\n"
        
        if len( outFile ) == 0 :
            print " renderHoudini no OUT FILE " , outFile
        else:
            basename = os.path.basename(outFile)
             
            outDir = outFile[:-1*len(basename)]
            outFileHeader = basename.split(".")[0]
            outFileExt = basename.split(".")[1]
            print "Pyro Rend !   ",  outDir ,  outFileHeader ,  outFileExt
            
            frStart  = self.intOrVal ( ts , 0 )
            frEnd  = self.intOrVal ( te , 0 )
            ma = hou.node('out/mantra_ipr')
            for fr in range (frStart, frEnd+1):
                frZeros = self.strWithZeros( fr , 4 )
                outputFile = "{}{}.{}.{}".format( outDir , outFileHeader, frZeros, outFileExt)
                ma.render( frame_range = (fr,fr) , output_file= outputFile )
                ####  to do  !!!
                import time 
                time.sleep(2)
        
        
    def saveHoudini (self, fileName) :
        print " \n saveHoudini : " , fileName
        fileName = fileName.replace('\\', '/')
        print " \n saveHoudini FIX : " , fileName
        print " \n\n\n " 
        hou.hipFile.setName(fileName)
        hou.hipFile.save( file_name = fileName )
        hou.hipFile.setName(fileName)
        
    def exitHoudini (self ) : 
        sys.exit()
        # hou.exit( exit_code=0, suppress_save_prompt=True)        
        # print " [INF] post HOU Exit  ;] " 
        
    def exitMaya(self ) : 
        sys.exit()        
        # print " [INF] post HOU Exit ;] " 
        
        
        
        
        
    def openMaya (self, fileName ) :
        print " \n openMaya : " , fileName
        # fileName = fileName.replace('\\', '/')
        # print " \n openMaya FIX : " , fileName
        # print " \n\n\n " 
        
        # file -open "fred.ma";
        import maya.cmds as cmx
        cmx.file ( modified=0 )
        cmx.file ( fileName , open=True )
        
        if self.forceLocal :
            cmx.refresh()
            time.sleep(1)
            # hou.ui.triggerUpdate()
            # time.sleep(1)
            
            
    def gaAttachCachePY( self, objName, xml_file_and_path ):
        print "[db] objName  :  "+objName+" xml_file_and_path  :   "  + xml_file_and_path	
        import maya.cmds as cmx
        obj = cmx.ls( objName ) 
        if len(obj) == 0 :
            print "\nNO OBJECT  ", objName
        else :
            import maya.mel as ml
            switch = ml.eval('createHistorySwitch("'+objName+'", false)');
            print "[db] " + switch
            ml.eval( 'string $cacheNode = `cacheFile -attachFile -f "'+xml_file_and_path+'" -cnm '+objName+' -ia ("'+switch+'.inp[0]")`; ')
            #ml.eval( 'string $cacheNode = `cacheFile -attachFile -f "'+xml_file_and_path+'" -cnm '+objName+' `; ')
            ml.eval( 'setAttr ("'+switch+'.playFromCache") true;  ')
    def importMaya (self, fileName ) :   # hack

        print "Himport"
        import maya.mel as ml
        import maya.cmds as cmx
        filesToImport = [["Ufok_T__body","Ufok_T__body.xml"], ["Ufok_T__head","Ufok_T__head.xml"] ]
        
        filesToImport.append ( ["Ufok_T__gun_R","Ufok_T__gun_R.xml"]  )
        filesToImport.append (  ["Ufok_T__gun_L","Ufok_T__gun_L.xml"]  )   ####   Transilvanian_gun_L
        filesToImport.append (  ["Ufok_T__cape","Ufok_T__cape.xml"]  )
        for fi in filesToImport:
            print " [DB] import : " , fi
            
            time.sleep( random.random()*0.5 + 0.4 )
            xml_file_and_path = "P:\\\\SiB_MultipleShots\\\\ani\\\\seq01\\\\seq01_sh010\\\\" + fi[1]
            objName = "Ufok_T__body"
            objName = "Ufok_T__bodyShape"
            objName = fi[0]
            ml.eval( ' select -r "'+objName+'"' )
            self.gaAttachCachePY( objName, xml_file_and_path ); 
            if fi[0][-1:] == "y":
                ml.eval( 'select -r Ufok_T__body Ufok_T_Point_Head  ; ')
                ml.eval(  'viewFit;' )  
                ml.eval( 'select -r Ufok_T__body   ; ')  
            cmx.refresh()
        ml.eval( 'select -r Ufok_T__body Ufok_T__head Ufok_T__cape Ufok_T__gun_L Ufok_T__gun_R ; ')
        #time.sleep( random.random()*0.5 + 0.4 )
        #ml.eval(  'viewFit;' )   

        
    def paramMaya (self, obj, param, val ) :
        print "\n\n\n"
        print "  GET PARAM : ", obj, param, val
        print "\n\n\n"
        # SiBe.paramHoudini("pyro_import","burn","3.0")
        # z = hou.node("/obj/pyro_sim/pyrosolver1/") 
        # print "\n", z.evalParm('temp_diffusion')
        # z.parm('lift').set(4)
        # z.parm( param ).set( val )
        
    def nClothSim (self, objectName, ts , te ) :
        

        
        frStart  = self.intOrVal ( ts , 0 )
        frEnd  = self.intOrVal ( te , 0 )
        print "\n\n\n"
        print "  SIM : ", objectName ,  frStart , frEnd
        print "\n\n\n"
        
        # setGobalFrangeExpr = 'tset `(%d-1)/$FPS` `%d/$FPS`' % (frStart,frEnd)
        # setGobalFrangeExpr = 'tset `({0}-1)/$FPS` `{1}/$FPS`'.format(frStart,frEnd)
        # hou.hscript(setGobalFrangeExpr)
        # hou.playbar.setPlaybackRange( frStart, frEnd)
        # hou.setFrame (frStart)
        
        # hou.node('/obj/pyro_sim/output').parm("execute").pressButton()
        
        if self.forceLocal :
            time.sleep(1)
            # hou.setFrame (frStart+ int(  (frStart - frEnd)/2  ) )
            # hou.ui.triggerUpdate()
            # time.sleep(1)
        
        ####   HACK   !!!!
        import maya.mel as ml
        import maya.cmds as cmx
        
        # ml.eval( 'select -r Ufok_T__cape ; ')
        # for fr in range ( 1, 70): 
            # time.sleep( random.random()*0.13 + 0.13 )
            # cmx.currentTime( fr )
        # ml.eval( 'select -r Ufok_T__body Ufok_T__head Ufok_T__gun_L Ufok_T__gun_R ; ')
        # time.sleep( random.random()*0.5 + 0.4 )
        # ml.eval(  'viewFit;' ) 
        
        
        ml.eval( 'select -r '+ objectName +' ; ')
        # for fr in range ( 1, 70):
            #ml.eval('currentTime fr' )
            # time.sleep( random.random()*0.13 + 0.13 )
            # cmx.currentTime( fr )
        # ml.eval( 'select -r Ufok_T__body Ufok_T__head Ufok_T__gun_L Ufok_T__gun_R ; ')
        time.sleep( random.random()*0.5 + 0.4 )
        ml.eval(  'viewFit;' ) 
        
        storeCacheDir = "D:\\SOBA\\ClothSim\\tmp\\"
        cacheSubsamples = "1"
        cacheMode = 1 
        if cacheMode == 1 :
            pcMode = "OneFile"
        if cacheMode == 2 :
            pcMode = "OneFilePerFrame"
        print "INF[runSim] store dir :  " + storeCacheDir   + " \n"
        cmd = ''
        cmd += 'doCreateNclothCache 4 { "2", "1", "10", "'+ pcMode +'", "1", ' 
        cmd += '"' + storeCacheDir + '"'
        cmd += ',"1","","0", "add", "1", "'+ cacheSubsamples +'", "1","0","1" } ;'
        
        statusAfterSim = 3
        try:
            pm.mel.eval(cmd)
            statusAfterSim = 4
        except KeyboardInterrupt:
            print 'INF[runSim]   canceled cloth simulation from keyboard button\n'
            statusAfterSim = 5
        except:
            statusAfterSim = 6
            
        print "   statusAfterSim " , statusAfterSim
        print "   statusAfterSim " , statusAfterSim , cmd
        print "   statusAfterSim " , statusAfterSim
        
        
        
        

    def renderMaya (self, ts, te, outFile="" ) :
        print "\n\n\n"
        print "  REND : ",  ts, te, outFile , "_____!"
        print "\n\n\n"
        
        if len( outFile ) == 0 :
            print " renderMaya no OUT FILE " , outFile
        else:
            basename = os.path.basename(outFile)
             
            outDir = outFile[:-1*len(basename)]
            outFileHeader = basename.split(".")[0]
            outFileExt = basename.split(".")[1]
            print " SimC Rend !   ",  outDir ,  outFileHeader ,  outFileExt
            
            frStart  = self.intOrVal ( ts , 0 )
            frEnd  = self.intOrVal ( te , 0 )
            # ma = hou.node('out/mantra_ipr')
            # for fr in range (frStart, frEnd+1):
                # frZeros = self.strWithZeros( fr , 4 )
                # outputFile = "{}{}.{}.{}".format( outDir , outFileHeader, frZeros, outFileExt)
                # ma.render( frame_range = (fr,fr) , output_file= outputFile ) 
                # import time 
                # time.sleep(2)
                
            import maya.cmds as cmx
            
            for fr in range ( 1, 70):   
                cmx.currentTime( fr )
                
                cmx.refresh()
                fi  = outFile[:-6] +"__"+ self.strWithZeros (fr, 3)   +".jpg"    ####  hack rend
                print  fi
                
                fi = fi.replace('\\', '/')
                print  fi
                
                
                
                #####  maya 16
                # editores = cmx.renderWindowEditor(q=True) #, editorName=True )
                # if( len(editores) == 0  ):
                    # editores = cmx.renderWindowEditor( "renderView" )
                #####  maya 16                  
                                
                editores = cmx.renderWindowEditor( "renderView", q=True )   #, editorName=True )
                if( editores == None  ):
                    editores = cmx.renderWindowEditor( "renderView", e=True )
                    
                cmx.render( 'persp', x=800, y=450 )
                    
                    
                cmx.setAttr ('defaultRenderGlobals.imageFormat', 8)
                
                
                cmx.renderWindowEditor(editores, e=True,  writeImage=fi )   #  currentCamera='persp',
                #cmx.renderWindowEditor( editor, e=True, snapshot=('persp', 256, 256) )
                #cmx.renderWindowEditor( editores, e=True, snapshot=('persp', 256, 256) , writeImage=fi )
        
        
    def saveMaya (self, fileName) :
        print " \n saveMaya : " , fileName
        fileName = fileName.replace('\\', '/')
        
        print " \n saveMaya B : " , fileName
        
        # print " \n saveMaya FIX : " , fileName
        print " \n\n\n "  
        import maya.cmds as cmx 
        
         
        cmx.file( rename=fileName )
        # cmx.file( save=True, defaultExtensions=False, type='mayaAscii' )
        cmx.file( save=True, defaultExtensions=False, type='mayaBinary' )
    def exitMaya (self ) : 
        sys.exit()
        # hou.exit( exit_code=0, suppress_save_prompt=True)
        
        # print " [INF] post HOU Exit  " 
        
        
        
        
        
    def saveUpdatedQueue (self, file=None):
        if file==None:
            file = self.qFile
        print " [INF] save queue : " + file
        self.q.saveQueueToFile(file = file )
        
    def setStateAndAddToLog (self, stateName, stateID, serverName, withSave=True, addCurrentTime = False , setTime=""):
    
        self.q.clearAllQueueItems()
        self.q.loadQueue()
        self.q.setState( self.executorQueueID , stateName, stateID, serverName=serverName, serverID=1, setTime=setTime, addCurrentTime = addCurrentTime )
        
        if self.q.getQueueIndexFromID(self.executorQueueID) > 0:
            qin = self.q.queueData[   self.q.getQueueIndexFromID(self.executorQueueID)   ].queueItemName
            self.addToLog( " set "+stateName+" [" +  str( self.executorQueueID ) +  "]   "+ qin +"   by server: " +  serverName  )
        else:
            self.addToLog( " set "+stateName+" [" +  str( self.executorQueueID ) +  "]   by server: " +  serverName  )
        if withSave == True:
            self.saveUpdatedQueue()
        
    def setQueueJobWorking (self, id, serverName,serverID, withSave = True  ):  # setStatus
        self.setStateAndAddToLog ("WORKING", 4, serverName,  withSave = withSave , addCurrentTime = True)
        
    def setQueueJobDone (self, id, serverName,serverID, withSave = True, setTime="" ):  # setStatus
        self.setStateAndAddToLog ("DONE", 11, serverName, withSave = withSave , setTime=setTime )
        
    def setQueueJobError (self, id, serverName,serverID, withSave = True ):  # setStatus
        self.setStateAndAddToLog ("ERR", 9, serverName, withSave = withSave , addCurrentTime = True )
        
            
            
    def setSimNodeState(self,state, dbMode = 0):   ####  setState
        # file  =  self.serverDir + self.stateFileName 
        
        self.n.setNodeState( self.stateFile ,  self.hackSimNodeName , state, dbMode = dbMode) 
             
            
    def finalizeQueueJob (self, soft = 1):
        # timePerFrame = str ( 0.01 * int ((  ( time.time() - self.jobStartTime )/( changedMax - orgMin )  ) * 100 )   )
        jobTime = str ( 0.1 * int ((  ( time.time() - self.jobStartTime )  ) * 10 )   )
        print " [INF] job time     " , jobTime
        self.setQueueJobDone( self.executorQueueID ,   self.hackSimNodeName, 123456 , setTime=jobTime )
       
        self.setSimNodeState( 2 )   # self.setSimNodeDone()
        
        if soft == 1 :
            # self.addToLog( "HOU Exit" )
            # print " [INF] HOU Exit  " 
            self.exitHoudini()
        else :  ###  maya !!
            self.addToLog( "Maya Exit" )
            print " [INF] Maya Exit  " 
            self.exitMaya()
        
        
        
    # def setState (self, stateID ):
        # 1
        
        

    # def setHoldNodeState db:False =

		# if doesFileExist stateFile then
		# (
            # currentState = "8;SiNode_01;" + get_date()
            
			# fi = openFile stateFile mode:"wt"   -------   open file 
			# if fi != undefined then
			# (
                # format currentState   to: fi 
				# close fi
			# )
			# else
			# (
				# format "eeeeerrror  write  % % \n " stateFile fi
			# )
        # )
        # else
            # format " ERR  file not EXIST % \n" stateFile
    

    # def setErrorNodeState db:False 

		# if doesFileExist stateFile then
		# (
            # currentState = "9;SiNode_01;" + get_date()
            
			# fi = openFile stateFile mode:"wt"   -------   open file 
			# if fi != undefined then
			# (
                # format currentState   to: fi 
				# close fi
			# )
			# else
			# (
				# format "eeeeerrror  write  % % \n " stateFile fi
			# )
        # )
        # else
            # format " ERR  file not EXIST % \n" stateFile
    

    
        
        
        
        
        
        
        
        
        
        
