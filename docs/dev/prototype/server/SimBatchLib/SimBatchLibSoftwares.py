from SimBatchLibCommon import * 

# from SimBatchUiWidgets import *

try:
    import MaxPlus
except ImportError:
    # print "i45  MaxPlus not loaded"
    pass
    
try:
    import hou
except ImportError:
    # print "i46  HOU not loaded"
    pass
    
import os
    
    

# print "softlib" 
    
class SoftwaresConnector():   ##  soCo = SoftwaresConnector()

    currentSoft = -1
    
    def __init__(self, currentSoft ):
        self.currentSoft = currentSoft
        
        #####  HACK SOFT   currentSoft
        # self.currentSoft = 3
        
    def evalPyHou_getCurrentSceneFile (self):
        houScenePath = hou.hipFile.path()
        houSceneBasename = hou.hipFile.basename()
        houScenePath = houScenePath.replace("/", "\\")        
        retsplitfile = houSceneBasename.split(".")
        print "\nzzzzzz   A"
        print houScenePath
        print houSceneBasename
        print   houScenePath[:-1*len(houSceneBasename) -1] + "\\" 
        print "zzzzzz  B "
        
        return [ houScenePath[:-1*len(houSceneBasename) -1] + "\\"  , houSceneBasename , retsplitfile[0] ]
            
    def evalPyHou_saveCurrentScene (self):
    
        return 1
        
    def evalPyHou_getCurrentFramerange (self):
        start_frame = 40
        end_frame = 70
        # setGobalFrangeExpr ="tset `({0}-1)/$FPS` `{1}/$FPS`".format(start_frame,end_frame)
        setGobalFrangeExpr ="tset"
        ret = hou.hscript(setGobalFrangeExpr)
        print " evalPyHou_getCurrentFramerange A "
        print ret 
        print " evalPyHou_getCurrentFramerange B "
        return "10;40"
    def evalPyHou_setCurrentFramerange (self):
        start_frame = 40
        end_frame = 70
        # setGobalFrangeExpr ="tset `({0}-1)/$FPS` `{1}/$FPS`".format(start_frame,end_frame)
        setGobalFrangeExpr ="tset `({0}-1)/$FPS` `{1}/$FPS`".format(start_frame,end_frame)
        ret = hou.hscript(setGobalFrangeExpr)
        print " evalPyHou_setCurrentFramerange A "
        print ret 
        print " evalPyHou_setCurrentFramerange B "
        return "10;40"
        
    def evalPyHou_getObjectNamesFromCurrentScene (self, selectionOnly = 0, onlyType = 0 ):
        if selectionOnly < 1 :
            if selectionOnly == 1 :
                x = []
                for nod in hou.selectedNodes() :
                    x.append(nod)
                print x[0].path()
                return (  str(x[0]) + ";" )
                
        else :
            if selectionOnly == 1 :   #   !!!! to do  !!!
                x = []
                for nod in hou.selectedNodes() :
                    x.append(nod)
                print x[0].path()
                return (  str(x[0]) + ";" )
        return ""
        
    def evalPyHou_getTypeOf (self):
    
        return 1
        
        
    def evalMaxScript (self, mxs): #  ????   file ??? 
        # MaxPlus   
        # if self.currentSoft == 3 :
        print "\n evalMaxScript : " , mxs
        
        if "MaxPlus" not in sys.modules:
            print '[ERR]You have not imported module MaxPlus !' 
            return ""
        else:
            res = MaxPlus.FPValue()
            ret = MaxPlus.Core.EvalMAXScript( mxs, res ) 
            print "retoxio ___  ", ret 
            print " mxsxioo ___  ", mxs 
            # print "resyo ___  ", res 
            # print "retssssy ___  ",   res.Get()   #,  "   __   ",   MaxPlus.FPTypeGetName(res.GetType()),   "   __   ", res.Get()
            return  res.Get()
                
                
        # print '[ERR] softID is  wrong !' ,  self.currentSoft
        return "" 
                 
        # for i in sys.modules :
            # print "mooo" , i  
        
        
    def getCurrentSceneFile(self, lowerCase=False ):
        print " getCurrentSceneFile  currentSoft : " ,  self.currentSoft 
    
        if self.currentSoft == 1:
            ret = self.evalPyHou_getCurrentSceneFile ()
            return ret
        if self.currentSoft == 2:
            import maya.cmds as cmx
            # print cmx.file
            
            fi =  cmx.file ( query=True, sceneName=True)
            fi = fi.replace('/', '\\')
            basename = os.path.basename(fi)
             
            outDir = fi[:-1*len(basename)]
            outFileHeader = basename.split(".")[0]
            outFileExt = basename.split(".")[1]
        
            return [ outDir  , basename , outFileHeader ]  # getFilenameFile
        if self.currentSoft == 3:
            # ret = self.evalMaxScript ( " fn a   = (return maxFilePath + maxFileName) ; a() " )
            ret = self.evalMaxScript ( ' maxFilePath + ";"+maxFileName ' )
            
            if lowerCase:
                ret=ret.lower()
            
            retsplit = ret.split(";")
            retsplitfile = retsplit[1].split(".")
            return [ retsplit[0] , retsplit[1] , retsplitfile[0] ]   # getFilenameFile
        return ["","",""] 


    def loadScene (self, target ):
        print " loadScene  currentSoft : " ,  self.currentSoft 
        if self.currentSoft == 1:
            ret = hou.hipFile.load(  target, suppress_save_prompt=True, ignore_load_warnings=True )
            return ret
            
        if self.currentSoft == 2:
            import maya.cmds as cmx
            # fi =  cmx.file ( query=True, sceneName=True)
            print " [db] loadScene target", target
            ret = cmx.file ( target  , o=True , force=True)  ####  mayaAscii
            print " [db] loadScene target", target , ret
            
            # ret = self.evalMaxScript ( ' saveMaxFile  "' + target + '"  quiet:True ' )  
            return ret
        if self.currentSoft == 3: 
            ret = self.evalMaxScript ( ' loadMaxFile  "' + target + '"  quiet:True ' )  
            return ret 
        return False
        
    def saveCurentSceneAs (self, target ):
        # print "\n  ee e ee e"
        if self.currentSoft == 1:
            # print "\n  ee e ee e4"
            ret = hou.hipFile.save( file_name = target)
            # print "\n  ee e ee e3"
            return ret
            
        if self.currentSoft == 2:
            import maya.cmds as cmx
            # fi =  cmx.file ( query=True, sceneName=True)
            print " [db] target", target
            ret1 = cmx.file ( rename = target )
            ret2 = cmx.file ( save=True, type="mayaBinary")  ####  mayaAscii
            print " [db] target", target , ret1, ret2
            # ret = self.evalMaxScript ( ' saveMaxFile  "' + target + '"  quiet:True ' )  
            return ret1
            
        if self.currentSoft == 3: 
            ret = self.evalMaxScript ( ' saveMaxFile  "' + target + '"  quiet:True ' )  
            return ret 
            
        return False
        
    def getCurentFrameRange (self ):
        if self.currentSoft == 1:
            ret = self.evalPyHou_getCurrentFramerange()                
            # return ret         
            return [1,240]
            
        if self.currentSoft == 2:
            import maya.cmds as cmx
            orgMin = cmx.playbackOptions ( query = True, minTime = True  )
            orgMax = cmx.playbackOptions ( query = True, maxTime = True  )
            return [ orgMin , orgMax]
            
        if self.currentSoft == 3: 
            ret = self.evalMaxScript ( ' (1*animationrange.start) as string +";"+ (1*animationrange.end) as string ' )  
            ret = ret.split ( ";" )
            return ret 
        return None
         
        
    def getObject ( self, soft, type, subtype ) : #  "MAX","engine","fume"   ###SiB###  scene_objects
        print "  getObject: " ,  soft, type, subtype
        
        
        
        if type == "HouSimulate":   # !!!!!  HACK 
            return [1,"pyro1"]
        
        if type == "MaxSimulate":
            if subtype == "FumeFx":
                return [1,"FFX_engine_def"]
            if subtype == "Cloth":
                return [1,"def_clo_obj"]    
        return [0,"null"]
        
        
    def getObjectsFromScene (self, lowerCase = False):  ###SiB###  scene_objects
        if self.currentSoft == 1:
            ret = self.evalPyHou_getObjectNamesFromCurrentScene()
            if lowerCase:
                ret=ret.lower()
            retsplit = ret.split(";")[:-1]
            return retsplit
        if self.currentSoft == 2:
            import maya.cmds as cmx
            sel = cmx.ls ( )
            print  " [db] getSceneSelection ", sel
            return sel
        if self.currentSoft == 3: 
            ret = self.evalMaxScript ( ' objNames=""; for o in ($* as array) do  objNames+=o.name+";";objNames ' )
            if lowerCase:
                ret=ret.lower()
            retsplit = ret.split(";")[:-1]
            return retsplit
        return []
        
        
        
    def getSceneSelection(self):  ###SiB###  scene_objects
        if self.currentSoft == 1:
            ret = self.evalPyHou_getObjectNamesFromCurrentScene( selectionOnly = 1 )
            return ret.split(";")[:-1] 
        if self.currentSoft == 2:
            import maya.cmds as cmx
            sel = cmx.ls ( selection = True )
            print  " [db] getSceneSelection ", sel
            return sel
        if self.currentSoft == 3:
            ret = self.evalMaxScript ( ' objNames=""; for o in (selection as array) do  objNames+=o.name+";";objNames ' )
            retsplit = ret.split(";")[:-1]
            return retsplit 
        return []
        
        
    def getSceneSelectionType(self):
        if self.currentSoft == 1:
            ret = self.evalPyHou_getObjectNamesFromCurrentScene( selectionOnly = 1, onlyType = 1 )
            # return ret.split(";")[:-1]
            return "pyro_sim"
        return []
        
    
    
    
    

        
        
class ImportOption():
    importID = 0
    importName = ""
    description = ""
    defVal = ""
    
    def __init__(self, importName, defVal, description):
        self.importID  = -1  
        self.importName  = importName  
        self.description  = description 
        self.defVal = defVal
        
class ScriptActionTemplate():  
    scriptType = ""
    paramsArray = []
    engineName = ""
    engineParam = ""
    description = ""
    
    compiledScript = ""
    
    def __init__(self, scriptType, paramsArray,  engineName = "", engineParam = "" , description = ""):
        self.scriptType = scriptType
        self.paramsArray   =   paramsArray
        self.engineName   =   engineName
        self.engineParam   =   engineParam
        self.description   =   description
        
    def compileScript (self):  #mark_evo
        self.compiledScript = "make script "  + self.scriptType + "done"
    
class SoftwareAction(): 
    actionID = 0 
    softwareID = 0
    
    actionType = ""
    actionSubType = ""
    editVal ="<test>"
    description= ""
    actionWidget = None
    # scriptActionTemplate = None   #   old!!!!
    scriptActionTemplates = None
    
    comboValArr = []
    
    comfun = CommonFunctions()
    
    soCo = None
    
    
    def __init__(self,  softwareID , scriptActionTemplates , actionType, actionSubType, editVal,   description, combo="", comboVal="",  ): 
        self.softwareID = softwareID 
        self.actionType = actionType
        self.actionSubType = actionSubType # new 
        self.description = description
        self.editVal = editVal
        self.combo = combo
        self.comboVal = comboVal
        self.scriptActionTemplates = scriptActionTemplates
        # print " new  scriptActionTemplate " ,softwareID , actionType ,  scriptActionTemplates[0],  len(scriptActionTemplates)
        
        self.soCo = SoftwaresConnector( softwareID )
        
        if len (comboVal) > 0:
            self.comboValArr = comboVal.split(",")
            # print "db comboValArr  : " , self.comboValArr

        
        
    def generateScript(self, scriptActionTemplates, vals, subType):    #  action.generateScript 
        script= ""
        scriptActionTemplate = scriptActionTemplates[0]
        # print "\n\n kuuukewwee 1 ",  scriptActionTemplate.paramsArray.count , scriptActionTemplate.paramsArray
        for sAT in scriptActionTemplates :
            if sAT.engineName ==  subType :    ###   "FumeFx", ...     ####  and  len(subType) > 0 
                scriptActionTemplate = sAT
                # print "\n\n kuuukewwee ",  sAT.engineName , len(subType)
            # print " ___ terst sAT ", sAT.engineName  , "_______", subType
        # print "\n\n kuuukewwee 2 ",  scriptActionTemplate.paramsArray.count , scriptActionTemplate.paramsArray
        
        if  ( scriptActionTemplate.paramsArray.count ) > 0:     # ["MXS",["loadMaxFile ","<f>", " quiet:True"] ] 
            for el in scriptActionTemplate.paramsArray :
                isElVar = 0
                if el[0] =="<" :
                    if el[1] == "o": #<o> object 
                        isElVar = 1
                        script += vals['o'] 
                    if el[1] == "p": #<p> paramProperties
                        isElVar = 1
                        script += vals['p'] 
                    if el[1] == "v": #<v> value
                        isElVar = 1
                        script += vals['v'] 
                    if el[1] == "f": #<f> filename_string
                        isElVar = 1
                        script += vals['f']  
                    if el[1] == "t" and el[2] == "s" : #<ts> time start
                        isElVar = 1
                        script += str( vals['ts'] )
                    if el[1] == "t" and el[2] == "e" : # time end
                        isElVar = 1
                        script += str( vals['te'] ) 
                    if el[1] == "c": #<c> camera
                        isElVar = 1
                        script += vals['c'] 
                        
                    if isElVar == 0 :
                        script += el
                else:
                    script += el
        else:
            print " WRN empty scriptActionTemplate in generateScript "
        
        print "  [ db ] generateScript : " , script
        return script
        
        
    
        
        
    def comboOnChange___OLD (self, index ):
        print " [db]  SoftwareAction  comboOnChange : ", index
        self.actionWidget.actionSubType = self.actionWidget.combo.currentText()
        if len(self.comboValArr) > index: 
            self.actionWidget.edit.setText( self.comboValArr[index] )
            # widgetAction.actionSubType
        else:
            print "ERR comboOnChange  "   ,  len(self.comboValArr), ">", index
        
        
        
    def getSelectedObjectsSoAct( self, editLine, initDir, actionType ):   ###SiB###  scene_objects
    
        print " [db] getSelectedObjectsSoAct " ,  self.softwareID 
    
        # if self.currentSoft == 1:   # self.softwareID
        if self.softwareID == 1:   # self.softwareID
            ret = self.soCo.getSceneSelection()
            editLine.setText ( ret )
        
        # if self.currentSoft == 1:   # self.softwareID
        if self.softwareID == 2:   # self.softwareID
            
            
            ret = self.soCo.getSceneSelection()
            
            editLineText = editLine.text()
            
            indexCut =  editLineText.find( "\[" )
            if indexCut > 0 :
                editLineText = editLineText [:indexCut]
                
            if len (ret ) == 0 :
                return [- 1, ""]
            else:
                editLine.setText( editLineText  +"\\["+  self.comfun.arrayAsSrting ( ret, separator =" " ) +"]" )   ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!
                return [1,  self.comfun.arrayAsSrting ( ret, separator ="   " ) ]
            
        # if self.currentSoft == 3:
        if self.softwareID == 3:
            if  len(   self.soCo.getSceneSelection()  ) > 2 :   ####  HACK !!!!  
                editLine.setText(   editLine.text()[:-1]+" Transilvanian_gun_L Transilvanian_gun_R Transilvanian_head]"   )   ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!
            else:
                editLine.setText(   editLine.text()+"\\[Transilvanian_body]"   )   ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!  ####  HACK !!!!
        
        return [0 , ""]
    
    
    
    # def getGetDirectory  ( self, editLine ):
        # self.comfun.getGetDirectory(editLine, QFileDialog) 
        
    def getGetFile  ( self, editLine, initDir, actionType , QFileDialog ):
    

        if actionType == "HouSimulate"  or  actionType == "MaySimulate"  or  actionType == "MaxSimulate"    :    
            
            if actionType == "HouSimulate":
                ret = self.soCo.getSceneSelection()
                if len(ret) > 0 :
                    editLine.setText( ret[0] )
                    
                    classof = self.soCo.getSceneSelectionType()
                    
                    print "  classof ", classof 
                    
                    # if classof =="pyro_sim"  : 
                        # self.actionWidget.combo.setCurrentIndex(2)
                    self.actionWidget.combo.setCurrentIndex(2)
                else:
                    editLine.setText(   " [WRN] SELECT OBJECT FIRST !"   )
                    print (  " [WRN] SELECT OBJECT FIRST !"   )
                    
                    
            if actionType == "MaySimulate":
                ret = self.soCo.getSceneSelection()
                if len(ret) > 0 :
                    editLine.setText(   self.comfun.arrayAsSrting ( ret, separator =" " )      ) 
                    classof = self.soCo.getSceneSelectionType() 
                    print "  classof ", classof  
                    # if classof =="pyro_sim"  : 
                        # self.actionWidget.combo.setCurrentIndex(2)
                    self.actionWidget.combo.setCurrentIndex(1)
                else:
                    editLine.setText(   " [WRN] SELECT OBJECT FIRST !"   )
                    print (  " [WRN] SELECT OBJECT FIRST !"   )
                    
                    
            if actionType == "MaxSimulate":
                ret = self.soCo.getSceneSelection()
                if len(ret) > 0 :
                    editLine.setText( ret[0] )
                        
                    classof = self.soCo.evalMaxScript ( " ( classof $'"+ret[0] + "'  )  as string " )
                    print "  classof " , classof
                    print "  classof " , classof
                    print "  classof " , classof
                    if classof =="Editable_mesh"  or classof =="Editable_Poly" :  ###  TP  PF   Fume
                        self.actionWidget.combo.setCurrentIndex(4)
                    else :
                        if classof =="PF_Source" :
                            self.actionWidget.combo.setCurrentIndex(2)
                        else:
                            self.actionWidget.combo.setCurrentIndex(0)
                    if len(ret) > 1 :
                        sel = self.comfun.arrayAsSrting( ret, onlyFirst=1 )
                        # self.infoTop.setTopInfo(  " [INF] Used  first object from selection : " + sel , 7   )
                        print ( " [INF] Used  first object from selection : " + sel   )
                else:
                    editLine.setText(   " [WRN] SELECT OBJECT FIRST !"   )
                    # self.infoTop.setTopInfo(  " [WRN] SELECT OBJECT FIRST !"  , 8   )
                    print (  " [WRN] SELECT OBJECT FIRST !"   )
        
        else:            
            
            if actionType == "MaxSave"   or   actionType =="MaxPrev"  or   actionType == "HouSave"   or   actionType =="HouPrev"  or   actionType == "MaySave"   or   actionType =="MayPrev"  :
                self.comfun.getGetDirectory(editLine, QFileDialog , initDir)
            else:
                self.comfun.getGetFile(editLine, QFileDialog, initDir)  
        
        
        
class SoftwareEngineParam():
    script = ""
    def __init__(self, paramAbbreviation, paramName, paramProperties, parmDefVal, description, template):
        self.paramAbbreviation = paramAbbreviation
        self.paramName   =   paramName
        self.paramProperties   =   paramProperties
        self.parmDefVal   =   parmDefVal
        self.description   =   description
        
    def compileScript (self):  #mark_evo
        self.script = "make script "  + self.paramName + "done"
        

class SoftwareEngine(): 
    engineName = ""
    engineID = 0
    softwareName = ""
    totalParams = 0
    engineParams = [] 
    description = ""
     
    # maxEngineID = 0
    
    def __init__(self, engineName,   engineParams ,  description):  # softwareName   ,
        # self.maxEngineID +=1
        self.engineID  = -1 #self.maxEngineID
        self.engineName  = engineName
        # self.softwareName  = softwareName
        self.engineParams  = engineParams 
        self.description  = description 

    def appendParam (self, param):
        self.totalParams += 1
        self.engineParams.append(param)
        
    def clearParams (self):
        self.totalParams = 0
        self.engineParams = []
        
    def getParamByAbbrev(self, abbrev ):
        for p in self.engineParams:
            # print "looko abbrev "  ,   p.paramAbbreviation ,  abbrev 
            if p.paramAbbreviation == abbrev :
                return p
        return None
    
        
  
class Software():

    softwareID = -1
    softwareName = ""
    
    softwareEngines = []
    softwareActions = []
    softwareImports = []
    
    testedSoftwareVersions = ""
    description = ""
    
    # maxSoftwareID = 0
    maxSoftwareEnginesID = 0
    maxSoftwareActionID = 0
    maxImportOptionsID = 0
    
    def __init__(self, softwareID, softwareName , softwareEngines , testedSoftwareVersions,    description):
        self.softwareID   = softwareID
        self.softwareName   =  softwareName
        self.softwareEngines   =  softwareEngines
        self.testedSoftwareVersions  = testedSoftwareVersions
        self.description = description
        self.softwareActions = []
        
    def appendEngine (self, engine ):
        if engine.engineID <= 0:
            self.maxSoftwareEnginesID +=1
            engine.engineID = self.maxSoftwareEnginesID 
        else:
            if self.maxSoftwareEnginesID < engine.engineID:
                self.maxSoftwareEnginesID = engine.engineID
        self.softwareEngines.append(engine)
        
    def appendImportOption (self, importOption ):
        if importOption.importID <= 0:
            self.maxImportOptionsID +=1
            importOption.importID = self.maxImportOptionsID 
        else:
            if self.maxImportOptionsID < importOption.importID:
                self.maxImportOptionsID = importOption.importID
        self.softwareImports.append(importOption) 
        
    def appendAction(self, action):
        if action.actionID <= 0:
            self.maxSoftwareActionID +=1
            action.actionID = self.maxSoftwareActionID 
        else:
            if self.maxSoftwareActionID < action.actionID:
                self.maxSoftwareActionID = action.actionID
                
        action.actionID = self.maxSoftwareActionID
        self.softwareActions.append(action)
        # print "append action ", self.softwareName
        # for so in self.softwareActions:
            # print "totla: ", so.actionType
        
        #   ["Houdini","Maya","3dsMAX","RealFlow","stand-alone"]
        
    def getEngineByName(self, name):
        for e in self.softwareEngines:
            # print "looko eng name "  ,   e.engineName ,  name 
            if e.engineName == name:
                return e
        return None;

# class SimBatchLibSoftwares():
    # self.so = None
    # def __init__(self,globalSettings):
        # so = Softwares(globalSettings)
    # def  retso():
        # return so

class Softwares(): 
    softwaresArray =[]
    totalSoftwares = 0
    currentSoftware = ""
    currentSoftwareID = 0
    
    soCo = None

    
    def __init__(self,globalSettings):
        self.s = globalSettings
        
        self.soCo = SoftwaresConnector( self.s.currentSoft )
        
        self.initHoudini()
        self.initMaya()
        self.initMax()
        self.initRealflow()
        self.initStandalone()
        # print "init softwraersyy"
        
    def initHoudini (self):
        self.totalSoftwares +=  1 
        softID = 1
        houSoft = Software( softID, "Houdini", [], "15.5,16.0", "hou")
        
        
        
        # houImportOptionAni = ImportOption ( "ANI", "<project_cache_dir>", "animation cache") # <shot_animation_cache>
        # houSoft.appendImportOption (houImportOptionAni)
        # houImportOptionCam = ImportOption ( "CAM", "<project_camera_dir>", "camera object")
        # houSoft.appendImportOption (houImportOptionCam)
        # houImportOptionGeo = ImportOption ( "GEO", "","geometry file")
        # houSoft.appendImportOption (houImportOptionGeo)
        # houImportOptionMax = ImportOption ( "HIP", "","MAX scene")
        # houSoft.appendImportOption (houImportOptionMax) 
        # houImportOptionEnv = ImportOption ( "ENV", "<project_env_dir>", "enviroment objects")  # <shot_env_file>
        # houSoft.appendImportOption (houImportOptionEnv)
        
        
        # scriptParamTemplate = "$" , "<o>"  , "." , "<p>" , "=" , "<v>"    #  <o> object  <p> paramProperties  <v> value 
        scriptParamTemplate = "hou.node(\"", "<o>" ,"\").setParms({\"" ,  "<p>"    ,   "\" :",  "<v>", "})" 
        houEngineFlip = SoftwareEngine ( "Flip" , [], "Flip for Houdini" )
        houEngineFlip.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        houSoft.appendEngine (houEngineFlip)
        
        houEngineCloth = SoftwareEngine ( "Cloth" , [], "cloth for Houdini" )
        houEngineCloth.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        houEngineCloth.appendParam ( SoftwareEngineParam("DRG", "drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        houEngineCloth.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        houSoft.appendEngine (houEngineCloth)
        
        houEnginePyro = SoftwareEngine ( "Pyro" , [], "pyro for Houdini" )
        #                                    (self, paramAbbreviation, paramName, paramProperties, parmDefVal, description, template):
        houEnginePyro.appendParam ( SoftwareEngineParam("BRN", "burn rate", "burn", 0.9, "pyro burn rate", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("TIM", "time scale", "timescale", 1.0, "pyro time scale", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("DIF", "temp diffusion", "temp_diffusion", 0.1, "temp diffusion", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("IGN", "ignition temp", "ignitiontemp", 1, "pyro ignitiontemp", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("COL", "cooling rate", "cooling_rate", 0.8, "pyro cooling rate", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("LFT", "lift", "lift", 4, "pyro lift", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("GAS", "gasrelease", "gasrelease", 4, "pyro gas release", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("FIN", "fuel inefficiency", "fuelinefficiency", 0.2, "pyro fuelinefficiency", scriptParamTemplate )   )
        houEnginePyro.appendParam ( SoftwareEngineParam("BOX", "buoyancy X", "buoyancy_dirx", 0, "pyro buoyancy_dirx", scriptParamTemplate )   ) 
        houEnginePyro.appendParam ( SoftwareEngineParam("BOY", "buoyancy Y", "buoyancy_diry", 1, "pyro buoyancy_diry", scriptParamTemplate )   ) 
        houEnginePyro.appendParam ( SoftwareEngineParam("BOZ", "buoyancy Z", "buoyancy_dirz", 0, "pyro buoyancy_dirz", scriptParamTemplate )   ) 
        houSoft.appendEngine (houEnginePyro)
        
        
        houEngineBullet = SoftwareEngine ( "Bullet" , [], "bullet for Houdini" )
        houEngineBullet.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        houSoft.appendEngine (houEngineBullet)
        
        houEngineCrowd = SoftwareEngine ( "Crowd" , [], "bullet for Houdini" )
        houEngineCrowd.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        houSoft.appendEngine (houEngineCrowd)
        
        
        
        houEnginesNames = self.enginesNamesToStr( softID , soArr=[houSoft])
        # maxEnginesNames = self.enginesNamesToStr( softID , soArr=[maxSoft])
        
        
        
        # scriptActionTemplate = ScriptActionTemplate ("null",[])
        scriptActionTemplates = [ScriptActionTemplate ("null",[])]
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["SiBe.loadHoudini(\"","<f>", "\")"] )]
        houSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "HouOpen","Open", "<schema_base_setup>", "hip open") )
        
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["SiBe.importHoudini(\"","OKzzzOKzzzOK","<f>", "\")"] )] 
        houSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "HouImport","Import", "<shot_animation_cache>", "hip Import") )
        
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["print \"","OK1 OK OK _","<o>", "\"  "], engineName = "Flip", engineParam = "sim" )] 
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["print \"","OK OK2 OK_ ","<o>", "\"  "], engineName = "Cloth", engineParam = "sim" )   )
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["print \"","OK OK3 OK_ ","<o>", "\"  "], engineName = "Bullet", engineParam = "sim" )  )
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["SiBe.simulateHoudini(\"","<o>","\",","<ts>",",","",")"], engineName = "Pyro", engineParam = "sim" )    )
                                                                                       
        
        houSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "HouSimulate","Simulate",  "<scene_object>",  "hou Simulate", combo = houEnginesNames ) ) 

        scriptActionTemplates = [ScriptActionTemplate ("PYH",["SiBe.renderHoudini(","<ts>",",","",",outFile=\"","<f>","\")"]  )] ###  prev
        
        houSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "HouPrev", "Prev", "<schema_prevs_dir>", "Prev hou") )  
        
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["SiBe.saveHoudini(\"","<f>","\")"] )] 
        houSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "HouSave", "Save", "<schema_scenes_dir>", "hip py") )  
        houSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "HouPython", "Python", "<scripts_dir>", "hip py") ) 
        
        self.softwaresArray.append (houSoft)
        
        
        
        
        
        
    def initMaya  (self):
        self.totalSoftwares +=  1 
        softID = 2
        mayaSoft = Software( softID, "Maya", [], "2012", "maya")
        
        
        mayaImportOptionAni = ImportOption ( "ANI", "<project_cache_dir>", "animation cache") # <shot_animation_cache>
        mayaSoft.appendImportOption (mayaImportOptionAni)
        mayaImportOptionCam = ImportOption ( "CAM", "<project_camera_dir>", "camera object")
        mayaSoft.appendImportOption (mayaImportOptionCam)
        mayaImportOptionGeo = ImportOption ( "GEO", "","geometry file")
        mayaSoft.appendImportOption (mayaImportOptionGeo)
        # mayaImportOptionMax = ImportOption ( "MAX", "","MAX scene")
        # mayaSoft.appendImportOption (mayaImportOptionMax) 
        mayaImportOptionEnv = ImportOption ( "ENV", "<project_env_dir>", "enviroment objects")  # <shot_env_file>
        mayaSoft.appendImportOption (mayaImportOptionEnv)
        
        
        scriptParamTemplate = "maya set param (\"", "<o>" ,"\").setParms({\"" ,  "<p>"    ,   "\" :",  "<v>", "})" 
        
        mayaEngineNucleus = SoftwareEngine ( "nParticle" , [], "nucleus particles" )
        mayaEngineNucleus.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 40, "cloth stretch", scriptParamTemplate ) )
        mayaEngineNucleus.appendParam ( SoftwareEngineParam("DRG", "drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        mayaEngineNucleus.appendParam ( SoftwareEngineParam("BND", "bend res", "bend", 1, "bend resistant", scriptParamTemplate )   )
        mayaSoft.appendEngine (mayaEngineNucleus)
        
        mayaEngineParticles = SoftwareEngine ( "nCloth" , [], "nucleus cloth engine" ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("STR", "Stretch Resistance", "stretch", 40, "Stretch Resistance", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("CMP", "Compression Resistance", "stretch", 40, "Compression Resistance", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("BND", "Bend Resistance", "bbbbb", 40, "Bend Resistance", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRP", "Bend Angle Dropoff", "stretch", 40, "Bend Angle Dropoff", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("SHR", "Shear Resistance", "stretch", 40, "Shear Resistance", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("RIG", "Rigridity", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DEF", "Deform Resistance", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("MSH", "Input Mesh Attract", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("MAS", "Mass", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("LFT", "Lift", "stretch", 40, "cloth stretch", scriptParamTemplate )   ) 
        
        
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRG", "Drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRT", "Tangental Drag", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DMP", "Damp", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("SMP", "Stretch Damp", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("PRE", "Pressure", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("PMP", "Pressure Damping", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("THC", "Thickness", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("COS", "Colide Scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("BNC", "Bonuce", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("FRI", "Friction", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("STI", "Stickness", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("MSC", "Max Self Colide Iterations", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("MIT", "Max Iterations", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("TIM", "Time Scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("SSC", "Space Scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("SUB", "Substeps", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaEngineParticles.appendParam ( SoftwareEngineParam("MCI", "Max Collision Iterations", "time", 1, "cloth time scale", scriptParamTemplate )   )  
        
        '''    
        STR Stretch Resistance
        CMP Compression Resistance
        BND Bend Resistance
        DRP Bend Angle Dropoff
        SHR Shear Resistance

        RIG Rigridity
        DEF Deform Resistance
        MSH Input Mesh Attract

        MAS Mass
        LFT Lift
        DRG Drag
        DRT Tangental Drag
        DMP Damp
        SMP Stretch Damp

        PRE Pressure
        PMP Pressure Damping

        THC Thickness
        COS Colide Scale
        BNC Bonuce
        FRI Friction
        STI Stickness 
        
        MSC Max Self Colide Iterations
        MIT Max Iterations

        TIM Time Scale
        SSC Space Scale

        SUB Substeps
        MCI Max Collision Iterations
        '''      
        
        
        mayaSoft.appendEngine (mayaEngineParticles)
        
        mayaEngineParticles = SoftwareEngine ( "nHair" , [], "nucleus hair engine" )  
        mayaEngineParticles.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRG", "drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaSoft.appendEngine (mayaEngineParticles)
        
        mayaEngineParticles = SoftwareEngine ( "Fluid" , [], "   Fluid engine" )  
        mayaEngineParticles.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRG", "drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaSoft.appendEngine (mayaEngineParticles)
        
        mayaEngineParticles = SoftwareEngine ( "FumeFx" , [], "  FumeFx engine" )  
        mayaEngineParticles.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRG", "drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaSoft.appendEngine (mayaEngineParticles)
        
        mayaEngineParticles = SoftwareEngine ( "Bifrost" , [], "  Bifrost engine" )  
        mayaEngineParticles.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 40, "cloth stretch", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("DRG", "drag", "drag", 40, "cloth drag", scriptParamTemplate )   )
        mayaEngineParticles.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "cloth time scale", scriptParamTemplate )   ) 
        mayaSoft.appendEngine (mayaEngineParticles)
        
         
         
        mayaImportNames = self.importNamesToStr( softID , soArr=[mayaSoft])
        mayaImportDefVals = self.importDefValsToStr( softID , soArr=[mayaSoft])
        mayaEnginesNames = self.enginesNamesToStr( softID , soArr=[mayaSoft])
        
        # scriptActionTemplates = [ScriptActionTemplate ("MEL",["file -f   -typ \"mayaBinary\" -o \"","<f>", "\"; "] )]  # "D:/test_01_mqs/test_01__testShot_clothSim_00.mb";
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["SiBe.openMaya( \"","<f>", "\" )  "] )] 
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MayOpen", "Open", "<schema_base_setup>", "maya open") )
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["SiBe.importMaya( \"","<o>", "\" )  "] )] 
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MayImport", "Import", "<shot_animation_cache>", "maya import",   combo = mayaImportNames,  comboVal=mayaImportDefVals   ) )
        
        
        
        
        
        scriptActionTemplates = [ScriptActionTemplate ("PYH",["print \"","OK1 OK OK _","<o>", "\"  "], engineName = "nParticle", engineParam = "sim" )] 
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["SiBe.nClothSim( \"","<o>", "\",","<ts>",",","","  ) "], engineName = "nCloth", engineParam = "sim" )   )
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["print \"","OK OK3 OK_ ","<o>", "\"  "], engineName = "nHair", engineParam = "sim" )  )
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["print \"","OK OK3 OK_ ","<o>", "\"  "], engineName = "Fluid", engineParam = "sim" )  )
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["print \"","OK OK3 OK_ ","<o>", "\"  "], engineName = "FumeFx", engineParam = "sim" )  )
        scriptActionTemplates.append( ScriptActionTemplate ("PYH",["print \"","OK OK3 OK_ ","<o>", "\"  "], engineName = "Bifrost", engineParam = "sim" )  )
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MaySimulate", "Simulate", "<scene_object>", "maya Simulate" ,   combo = mayaEnginesNames) )
        
        
        scriptActionTemplates = [ScriptActionTemplate ("MAY",["SiBe.renderMaya( ","<ts>", " , ",""," , outFile=\"","<f>", "\"  )"]  )] ###  prev
        mayaPrevNames = "Playblast,Render"
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MayPrev", "Prev", "<schema_prevs_dir>", "maya Prev", combo = mayaPrevNames ) )
        
        
        scriptActionTemplates = [ScriptActionTemplate ("MAY",["SiBe.saveMaya( \"","<f>", "\" ) "] )] 
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MaySave", "Save", "<schema_scenes_dir>", "maya save") ) 
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MayMEL", "MEL", "<scripts_dir>", "maya MEL") )
        mayaSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates, "MayPython", "Python", "<scripts_dir>", "maya Python") )
        
        self.softwaresArray.append (mayaSoft)
        
        
        
        
        
        
        
        
        
        
        
        
        
    def initMax  (self):
        self.totalSoftwares += 1
        
        softID = 3
        
        maxSoft = Software( softID, "3dsMax", [], "2016", "max")
        
        maxEngineFume = SoftwareEngine ( "FumeFx" , [], "fume fx" )
        scriptParamTemplate = "$" , "<o>"  , "." , "<p>" , "=" , "<v>"    #  <o> object  <p> paramProperties  <v> value
        maxEngineFume.appendParam ( SoftwareEngineParam("SPC", "spacing", "GridSpacing", 4, "Grid Spaceing", scriptParamTemplate )   )
        # maxEngineFume.appendParam ( SoftwareEngineParam("SUB", "substeps", "GridSpacing", 4, "substeps", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("SQL", "solver quality", "SolverQuality", 4, "Solver Quality", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("TIM", "time scale", "TimeScale", 1.0, "Time Scalew", scriptParamTemplate)   ) 
        maxEngineFume.appendParam ( SoftwareEngineParam("BRN", "burn rate", "FuelBurnRate", 40, "Burn Rate", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("EXP", "fuel expand", "FuelExpand", 1.3, "Fuel Expand", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("HET", "heat", "HeatProduction", 40, "Heat Production", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("VRT", "vorticity", "Vorticity", 0.75, "Vorticity", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("BOY", "buoyancy", "Buoyancy", 0.75, "Buoyancy", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("TUX", "turb X", "XAxisTurbulence", 0.2, "XAxisTurbulence", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("TUY", "turb Y", "YAxisTurbulence", 0.2, "YAxisTurbulence", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("TUZ", "turb Z", "ZAxisTurbulence", 0.2, "ZAxisTurbulence", scriptParamTemplate)   )
        maxEngineFume.appendParam ( SoftwareEngineParam("TUS", "turb Scale", "TurbulenceScale", 0.2, "turbulenceScale", scriptParamTemplate)   )   
        maxEngineFume.appendParam ( SoftwareEngineParam("DRG", "motion drag", "MotionDrag", 40, "MotionDrag", scriptParamTemplate)   )
        
        #### EMITER  FUME FX 
        scriptParamTemplate = "$" , "<o>"  , "." , "<p>" , "=" , "<v>"    #  <o> object  <p> paramProperties  <v> value 
        maxEngineFume.appendParam ( SoftwareEngineParam("RAD", "emiter radius", "radius", 40, "emiter radius", scriptParamTemplate )   )
        maxEngineFume.appendParam ( SoftwareEngineParam("SVO", "s emiter obj vel", "ObjectVelocity", 40, "simple emiter ObjectVelocity", scriptParamTemplate )   )
        maxEngineFume.appendParam ( SoftwareEngineParam("SVD", "s emiter dir vel", "DirectionalVelocity", 40, "simple emiter Directional Velocity", scriptParamTemplate )   )
        maxEngineFume.appendParam ( SoftwareEngineParam("SVR", "s emiter rad vel", "RadialVelocity", 40, "simple emiter Radial Velocity", scriptParamTemplate )   )
        maxEngineFume.appendParam ( SoftwareEngineParam("PVM", "p emiter vel multip", "VelocityMultiplier", 40, "particle emiter vel multip", scriptParamTemplate )   )

        maxSoft.appendEngine (maxEngineFume)
        
        
        #### FUME  FX  WT !!!!
        maxEngineFumeWT = SoftwareEngine ( "FumeFxWT" , [], "fume fx" )
        scriptParamTemplate = "$" , "<o>"  , "." , "<p>" , "=" , "<v>"    #  <o> object  <p> paramProperties  <v> value
        maxEngineFumeWT.appendParam ( SoftwareEngineParam("SPC", "spacing", "GridSpacing", 4, "Grid Spaceing", scriptParamTemplate )   )
        maxSoft.appendEngine (maxEngineFumeWT)
        
        
        
        
        
        
        scriptParamTemplate = []
        
        # maxEnginePhonix = SoftwareEngine ( "PhonixFD" , [], "PhonixFD" )
        # maxEnginePhonix.appendParam ( SoftwareEngineParam("BRN", "burn rate", "burn", 40, "burn", scriptParamTemplate )   )
        # maxEnginePhonix.appendParam ( SoftwareEngineParam("TIM", "time scale", "time", 1, "time", scriptParamTemplate )   ) 
        # maxSoft.appendEngine (maxEnginePhonix)
        
        
        maxEnginePF = SoftwareEngine ( "PF" , [], "particle flow" )
        maxEnginePF.appendParam ( SoftwareEngineParam("RAT", "particle rate", "rate", 40, "rate", scriptParamTemplate )   )
        maxEnginePF.appendParam ( SoftwareEngineParam("ELE", "element name", "element", 1, "element", scriptParamTemplate )   )
        maxSoft.appendEngine (maxEnginePF)
        
        maxEnginePF = SoftwareEngine ( "TP" , [], "particle flow" )
        maxEnginePF.appendParam ( SoftwareEngineParam("RAT", "particle rate", "rate", 40, "rate", scriptParamTemplate )   )
        maxEnginePF.appendParam ( SoftwareEngineParam("ELE", "element name", "element", 1, "element", scriptParamTemplate )   )
        maxSoft.appendEngine (maxEnginePF)
        
        
        scriptParamTemplate = "$" , "<o>"  , "." , "<p>" , "=" , "<v>"    #  <o> object  <p> paramProperties  <v> value 
        
        maxEnginePF = SoftwareEngine ( "Cloth" , [], "cloth" )
        maxEnginePF.appendParam ( SoftwareEngineParam("DMP", "dump", "dump", 40, "dump", scriptParamTemplate )   )
        maxEnginePF.appendParam ( SoftwareEngineParam("BND", "bend", "bend", 1, "bend", scriptParamTemplate )   )
        maxEnginePF.appendParam ( SoftwareEngineParam("STR", "stretch", "stretch", 1, "stretch", scriptParamTemplate )   )
        maxSoft.appendEngine (maxEnginePF)
        
        
        
        ###   param FIN
        
        
        #### actions 
        
        
        maxImportOptionAni = ImportOption ( "ANI", "<project_cache_dir>", "animation cache") # <shot_animation_cache>
        maxSoft.appendImportOption (maxImportOptionAni)
        maxImportOptionCam = ImportOption ( "CAM", "<project_camera_dir>", "camera object")
        maxSoft.appendImportOption (maxImportOptionCam)
        maxImportOptionGeo = ImportOption ( "GEO", "","geometry file")
        maxSoft.appendImportOption (maxImportOptionGeo)
        maxImportOptionMax = ImportOption ( "MAX", "","MAX scene")
        maxSoft.appendImportOption (maxImportOptionMax) 
        maxImportOptionEnv = ImportOption ( "ENV", "<project_env_dir>", "enviroment objects")  # <shot_env_file>
        maxSoft.appendImportOption (maxImportOptionEnv)
         
         
        maxImportNames = self.importNamesToStr( softID , soArr=[maxSoft])
        maxImportDefVals = self.importDefValsToStr( softID , soArr=[maxSoft])
        maxEnginesNames = self.enginesNamesToStr( softID , soArr=[maxSoft])
        
        
        scriptActionTemplates = [ScriptActionTemplate ("MXS",["loadMaxFile @\"","<f>", "\" quiet:True"] )]   #  <f> filename_string
        maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates,"MaxOpen","Open", "<schema_base_setup>",  "max open") )
        
        
        
        
        scriptActionTemplates = [ ScriptActionTemplate ("MXS",["SiBe.actionANI \"","<f>", "\" "], engineName = "ANI", engineParam = "load cache" ) ]
        scriptActionTemplates.append(  ScriptActionTemplate ("MXS",["mergeMAXFile \"","<f>", "\" "], engineName = "CAM", engineParam = "cam" )   )
        scriptActionTemplates.append(  ScriptActionTemplate ("MXS",["mergeMAXFile \"","<f>", "\" "], engineName = "GEO", engineParam = "cam" )   )
        scriptActionTemplates.append(  ScriptActionTemplate ("MXS",["mergeMAXFile \"","<f>", "\" "], engineName = "MAX", engineParam = "max" )   ) 
        scriptActionTemplates.append(  ScriptActionTemplate ("MXS",["mergeMAXFile \"","<f>", "\" "], engineName = "ENV", engineParam = "env" )   ) 
        
        maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates,"MaxImport","Import", "<shot_animation_cache>",  "max import", combo = maxImportNames,  comboVal=maxImportDefVals ) )
        

        
        scriptActionTemplates = [ ScriptActionTemplate ("MXS",[ "$","<o>",".runsimulation( 0 )"], engineName = "FumeFx", engineParam = "sim" )  ]
        scriptActionTemplates.append( ScriptActionTemplate ("MXS",[ "$","<o>",".runsimulation( 2 )"], engineName = "FumeFxWT", engineParam = "sim" )  )
        scriptActionTemplates.append( ScriptActionTemplate ("MXS",[ "$","<o>",".export() "], engineName = "TP", engineParam = "sim" )  )
        scriptActionTemplates.append( ScriptActionTemplate ("MXS",[ " SiBe.injectHackFraamerange  \"","<f>","\" | SiBe.clothSimRun \"","<o>","\""], engineName = "Cloth", engineParam = "sim" )  )
        maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates,"MaxSimulate","Simulate", "sim",  "max Simulate", combo = maxEnginesNames ) )
        
        scriptActionTemplates = [ScriptActionTemplate ("MXS",["render fromframe:","<ts>"," toframe:","", " outputfile:@\"","<f>", "\" vfb:false"] ) ] #    camera:$","<c>", "  camera:_cameras[ic] vfb:false
        maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates,"MaxPrev","Prev", "<schema_prevs_dir>",  "max Prev") )  # [0:100]
        
        scriptActionTemplates = [ScriptActionTemplate ("MXS",["saveMaxFile @\"","<f>", "\" quiet:True"] )]   # saveMaxFile <filename_string> [saveAsVersion:<integer>] [clearNeedSaveFlag:<bool>] [useNewFile:<bool>] [quiet:<bool>] 
        maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates,"MaxSave","Save", "<schema_scenes_dir>",  "max Save") )
        
        ###  ???   Export
        # scriptActionTemplate = ["MXS",["saveMaxFile \"","<f>", "\" quiet:True"] ] 
        # maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplate,"MaxExport","Export", "<schema_scenes_dir>",  "max Save") )
        
        scriptActionTemplates = [ScriptActionTemplate ("MXS",["include ( \"","<f>", "\")"] ) ] 
        maxSoft.appendAction ( SoftwareAction(softID,scriptActionTemplates,"MaxScript","Scripti", "<scripts_dir>",  "max Script", combo = "MXS,PY" ) )
         
        
        self.softwaresArray.append (maxSoft)


    def initRealflow  (self):
        self.totalSoftwares +=  1 
        
        realflowSoft = Software( 4, "Realflow", [], "2016", "max")
        
        scriptActionTemplates = [ScriptActionTemplate ("null",[])]
        realflowSoft.appendAction ( SoftwareAction(4,scriptActionTemplates,"rfOpen","Open", "", "realflow open") )
        realflowSoft.appendAction ( SoftwareAction(4,scriptActionTemplates,"rfSim","Simulate", "", "realflow sim") )
        realflowSoft.appendAction ( SoftwareAction(4,scriptActionTemplates,"rfPrev","Prev", "", "realflow prev") )
        
        self.softwaresArray.append (realflowSoft)
        
    
    def initStandalone (self):
        self.totalSoftwares +=  1 
        
        standaloneSoft = Software( 5, "Standalone", [], "null", "sa")
        
        scriptActionTemplates = [ScriptActionTemplate ("null",[])]

        standaloneSoft.appendAction ( SoftwareAction(5,scriptActionTemplates,"saPython", "Python", "", "py") )
        standaloneSoft.appendAction ( SoftwareAction(5,scriptActionTemplates,"saShell", "Shell", "", "sys") )
        
        self.softwaresArray.append (standaloneSoft)
        
        
        

        
        

    #      evoStr     "TIM 0.5 2 1, DRG 1 4, BRN 2 4 "
    def checkEvo (self, soft, evoStr = "" ):     #     evoStr ="BRN 0.5 2 1"
        if len(evoStr) > 0:
            evoArr = evoStr.split(" ")
        return 
        
    def getEvoParamArry(self,softwareID, softwareEngine):
        paramArr = []
        for so in self.softwaresArray:
            # print "ee so so  ",  so.softwareID , softwareID
            if so.softwareID == softwareID:
                # print "ENERET "
                for se in so.softwareEngines:
                    # print "eeene ",se, se.engineName
                    if se.engineName == softwareEngine :
                        
                        for param in se.engineParams :
                            #   
                            paramArr.append( param.paramAbbreviation + "    "+param.paramName )
                        
                # for se in 
        # print "  zzeezr   ", softwareID, softwareEngine , len(paramArr) , paramArr
        return paramArr
    # softwareID = ""
    # softwareName = ""
    
    # softwareEngines = []
    
    
    
    def importNamesToStr (self,softID, soArr=None):
        if soArr==None:
            soArr = self.softwaresArray
        names = ""
        for so in soArr :
            if so.softwareID == softID:
                for si in so.softwareImports: 
                    names += si.importName +"," 

        if names > 1:
            names = names[:-1]
        return names
        
    def importDefValsToStr(self,softID, soArr=None):
        if soArr==None:
            soArr = self.softwaresArray
        names = ""
        for so in soArr :
            if so.softwareID == softID:
                for si in so.softwareImports: 
                    names += si.defVal +"," 

        if names > 1:
            names = names[:-1]
        return names  
        
    def enginesNamesToStr (self,softID, soArr=None):
        if soArr==None:
            soArr = self.softwaresArray
        names = ""
        for so in soArr :
            if so.softwareID == softID:
                for se in so.softwareEngines: 
                    names += se.engineName +"," 

        if names > 1:
            names = names[:-1]
        return names
        
        
        
    def getSoftwareIndexByID (self, id):
        counter = 0
        for s in self.softwaresArray :
            # print "  ... softwaresArray ", counter, s.softwareID ,  " nnmee " , s.softwareName
            if s.softwareID  == id :
                # print "  ... softwaresArray   return  ! ", counter, s.softwareID ,  " nnmee " , s.softwareName
                return counter
            counter += 1
            
        print " WRN getSoftwareIndexByID -1 , id: " , id
        return -1
        
    def getSoftwareEngineByName(self, name, softIndex):
        counter = 0
        for s in self.softwaresArray[softIndex].softwareEngines :
        
            if s.softwareID  == id :
                return counter
            counter += 1
            
        print " WRN getSoftwareEngineByName -1 , name: " , name, "   softIndex: " , softIndex
        return -1
         
        
    def getSoftwareActionByType(self, type, softIndex):
        counter = 0
        for s in self.softwaresArray[softIndex].softwareActions :
            # print " test " ,  s.actionType , "___",  type , counter
            if s.actionType  == type :
                # print " ret test " ,  counter
                return counter
            counter += 1
            
        print "\n\n ERR getSoftwareActionByType -1 , type: " , type, "   softIndex: " , softIndex, "\n"
        return -1
    
        
    def getScriptAction (self, type , subType, vals , softID):    #  type =  MaxOpen
        scriptType="EXT"
        softIndex = self.getSoftwareIndexByID ( softID )
        softActionIndex = self.getSoftwareActionByType ( type , softIndex )
        action = self.softwaresArray[softIndex].softwareActions[softActionIndex]
        
        #vals = {'f':'def_val','o':'def_o','c':'def_c','v':'def_v','ts':'123','te':'123'}
        # print " [db]  softID , softIndex  , softActionIndex :  " ,  softID , softIndex  , softActionIndex
        print " [db]getScriptAction type :", type
        # print " [db]getScriptAction subType :", subType
        # print " [db]getScriptAction softIndex :", softIndex
        # print " [db]getScriptAction softActionIndex :", softActionIndex
        # print " [db]getScriptAction val :", action.scriptActionTemplates[0].paramsArray
        # print " [db]getScriptAction T0 :", action.scriptActionTemplates[0]
        # print " [db]getScriptAction val :", action.scriptActionTemplates[0].paramsArray
        # print " [db]getScriptAction val :", vals
        # print " [db] self.softwaresArray[softIndex]....  "  , self.softwaresArray[softIndex].softwareName
        # print " [db] \n" 
        
        genScript  = action.generateScript ( action.scriptActionTemplates, vals, subType ) 
        # print "   ___genScript  " , genScript
        
        return [ scriptType ,  genScript   ]   #   [scriptType,script]
        
        

        
    def generateEvoScriptsX(self,  evos, softwareID ): #mark_evo
        # i.evosArrClean
        print "evosy:", evos   , "\n"     # evolutions
        evosScriptsArray = []
        #evosArr = evos.split(",")
        # if len(evosArr) : 
        for evo in evos :  # evosArr:
            #   cleanEvo = " ".join(evo.split())
            print "oco mmm " , evo
            cleanEvo = " "#.join(evo)
            evoFirst3 = cleanEvo[:3]
            # print "  [db] evo ", evo,   "   3: ", evoFirst3, "     softwareID ", softwareID
            for so in self.softwaresArray[softwareID-1].softwareEngines :
                for pa in so.engineParams :
                    if evoFirst3 == pa.paramAbbreviation :
                        pa.compileScript()
                        evosScriptsArray.append ( pa.script )
            
        
        if len(evosScriptsArray) == 0 :
            print "  [db]  no evos"
            evosScriptsArray = [""]
        else:
            print "  [db]     evos: ", evosScriptsArray
            
        return evosScriptsArray
        
            
            
            

    def getParamFromAbbrev(self, softID, engineName, abbrev):
        so = self.softwaresArray[  self.getSoftwareIndexByID(softID) ]
        # so.softwareEngines[]
        en = so.getEngineByName (engineName)
        param = en.getParamByAbbrev (abbrev)
        # print "param param " , param 
        return param.paramProperties
        
        
        
        
        
        
        
        
        
