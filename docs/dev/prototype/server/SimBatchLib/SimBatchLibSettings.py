
# import sys
try:
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtGui import *
    
    
    
# from SimBatchLib import CommonFunctions
from SimBatchLibCommon import CommonFunctions

class Settings():
    # version
    version = "v0.1.81  "
    # mode
    storeDataMode = 1   #  1 text file   2  sqlite  3 MySQL
    colorsMode = 2      #  1 graysclae   2 pastel   4 dark    4 custom
    currentSoft = -1     #  1 Houdini,   2 Maya,  3 3dsmax,   4  RF,  5 standalone,  6 blender , cinema 4d        currentSoftwareMode
    currentSoftName = ""
    # data files
    batchDataPath = "null"
    schemasFileName = "data_Schemas.txt"
    tasksFileName = "data_Tasks.txt"
    queueFileName =  "data_Queue.txt"
    nodesFileName = "data_Nodes.txt"
    projectsFileName = "data_Projects.txt"
    sqliteFileName = "data_sqlite.db"
    # mysql setting 
    mysqlHost="127.0.0.1"
    mysqlUser="default"
    mysqlPass="default"
    mysqlPort="3306"
    #
    userName = "Default"
    userSign = "D"
    userPass = "def"
    
    #
    loadedSettingsState = -1       #   -1 err base ini  0  def null    1 from def file  2 from custom file   > 10 loaded data STQNPS
    
    checkWindowPosOnStart = 0
    
    # simNodesStates = ["offline","waiting","loading","simulating","rendering","saving cache", "saving scene"]
    
    stateColors = []
    stateColorsUp = []
    
    comfun = None
    forceDataStorePath = ""
    
    ###  DEFAULT VALS 
    defQueuePrior = 50 
    
    def __init__(self, softID, forceDataStorePath ="" ):
        
        self.currentSoft = softID
        
        self.forceDataStorePath = forceDataStorePath
        
        self.comfun = CommonFunctions()
         
        self.loadDefColors( self.stateColors , self.stateColorsUp ) 
    
    # def getSettingsPath (self,file):
        # 1
        
    def setCurrentSoftName (self):
        # currentSoft = -1     #  1 Houdini,   2 Maya,  3 3dsmax,   4  RF,  5 standalone,  6 blender , cinema 4d        currentSoftwareMode
        if self.currentSoft == 1 :
            self.currentSoftName = "Houdini"
        elif self.currentSoft == 2 :
            self.currentSoftName = "Maya"
        elif self.currentSoft == 3 :
            self.currentSoftName = "3dsMAX"
        elif self.currentSoft == 4 :
            self.currentSoftName = "RealFlow"
        elif self.currentSoft == 5 :
            self.currentSoftName = ":>"
            
        
      
        
    def loadSettings (self,file):
        settingsArr=["null"]
        settingsArr.append( ["user",["name","Default"],["sign","D"],["pass","def"] ] )
        settingsArr.append( ["mode",["value", 1 ] ] )
        settingsArr.append( ["txtdata",["Data",""],["Schemas","def_Schemas.txt"],["Tasks","def_Tasks.txt"],["Queue","def_Queue.txt"],["Nodes","def_Nodes.txt"],["Projects","def_Projects.txt"] ] )
        settingsArr.append( ["sqlite",["dbfile","def_sqlite.db"] ] )
        settingsArr.append( ["MySQL",["host","127.0.0.1"],["username","default"],["password","default"],["port","3306"] ] )
        settingsArr.append( ["window",["posx","220"],["posy","40"],["sizex","220"],["sizey","750"] ] )
        #settingsArr.append( ["colors",["def","M"] ] )
        settingsFile=""
        
        
        comfun = self.comfun
        
        if len(self.forceDataStorePath)==0 :
            settingsIniFile = comfun.currentScriptsPath()+"dataStore.ini"
        else :
            settingsIniFile = self.forceDataStorePath+"dataStore.ini"
        
        if len(file)==0:
            if comfun.fileExists ( settingsIniFile, "default data store" ) :
                content = comfun.loadFromFile( settingsIniFile )
                self.loadedSettingsState = 1
            else:
                settingsFile="def"
                self.loadedSettingsState = 0
                print " WRN [default data store] not exist : " , settingsIniFile
        else:
            if comfun.fileExists ( file ,"data store" ) :
                content = comfun.loadFromFile( file )
                self.loadedSettingsState = 2
            else:
                self.loadedSettingsState = -1
                print " WRN [file data store] not exist : " , file
            
        if self.loadedSettingsState > 0 :            
            arrIndex=0
            arrIndexSub=0
            for line in content :
                li = line.split("=")
                if li[0][0] == "[":
                    arrIndexSub=0
                    if li[0][1] == "u" : arrIndex = 1 #user
                    if li[0][1] == "m" : arrIndex = 2 #mode
                    if li[0][1] == "t" : arrIndex = 3 #paths
                    if li[0][1] == "s" : arrIndex = 4 #sqlite
                    if li[0][1] == "M" : arrIndex = 5 #MySQL
                    if li[0][1] == "w" : arrIndex = 6 #window
                else:
                    arrIndexSub+=1
                    # print li[0], arrIndexSub
                    # lix = li[1].split("\n")   #tudu FIX \n
                    settingsArr[arrIndex][arrIndexSub][1]=li[1]
                
            
            # print settingsArr
            
            ###self.setSettingsFromFile (settingsArr)
            
            #print settingsArr[3]

            test = comfun.isfloat ( (settingsArr[2][1][1]) )
            if test :
                self.storeDataMode = int(settingsArr[2][1][1])
                if self.storeDataMode == 1:
                    print " [INF] store data mode: txt files "
                if self.storeDataMode == 2:
                    print " [INF] store data mode: sqlite "
                if self.storeDataMode == 3:
                    print " [INF] store data mode: MySQL "
            else :
                print " [ERR] mode value unexpected : ", settingsArr[2][1][1]
     
            self.batchDataPath = settingsArr[3][1][1]
            self.schemasFileName = settingsArr[3][2][1]
            self.tasksFileName = settingsArr[3][3][1]
            self.queueFileName =  settingsArr[3][4][1]
            self.nodesFileName = settingsArr[3][5][1]
            self.projectsFileName = settingsArr[3][6][1]            
            
            self.sqliteFileName=settingsArr[4][1][1]
            
            self.mysqlHost=settingsArr[5][1][1]
            self.mysqlUser=settingsArr[5][2][1]
            self.mysqlPass=settingsArr[5][3][1]
            self.mysqlPort=settingsArr[5][4][1]
            
            self.wnd = [   int(settingsArr[6][1][1]) ,  int( settingsArr[6][2][1] ) ,   int( settingsArr[6][3][1]),   int(settingsArr[6][4][1])     ] 
            
            self.updateColors( )
            
            self.loadedSettingsState = 1 
          
          
        # self.printSettings()  
            



    def saveSettings (self,file=""):
        comfun = self.comfun
        dataPath =  self.batchDataPath   
        
        content = """[mode]
(1-txt, 2-sqlite, 3-MySQL)="""+str(self.storeDataMode)+"""
[txtdata]
Data="""+self.batchDataPath+"""
Schemas="""+self.schemasFileName+"""
Tasks="""+self.tasksFileName+"""
Queue="""+self.queueFileName+"""
Nodes="""+self.nodesFileName+"""
Projects="""+self.projectsFileName+"""
[sqlite]
file and path="""+self.sqliteFileName+"""
[MySQL]
db="""+self.mysqlHost+"""
user="""+self.mysqlUser+"""
pass="""+self.mysqlPass+"""
port="""+self.mysqlPort+"""
[user]
name="""+self.userName+"""
sign="""+self.userSign+"""
pass="""+self.userPass+"""
[window]
posx="""+str(self.wnd[0])+"""
posy="""+str(self.wnd[1])+"""
sizex="""+str(self.wnd[2])+"""
sizey="""+str(self.wnd[3])+"""
"""
        if len(file) == 0:
            file = comfun.currentScriptsPath()+"dataStore.ini"
        comfun.saveToFile(  file , content )
        print ' [INF] settings saved to: ' , file
                 
        
        if self.storeDataMode == 1:   #  1 text file   2  sqlite  3 MySQL 
            
            if comfun.fileExists ( dataPath + self.schemasFileName, "" ) == False :
                comfun.createEmptyFile ( dataPath + self.schemasFileName )
            
            if comfun.fileExists ( dataPath + self.tasksFileName, "" ) == False :
                comfun.createEmptyFile ( dataPath + self.tasksFileName )
            
            if comfun.fileExists ( dataPath + self.queueFileName, "" ) == False :
                comfun.createEmptyFile ( dataPath + self.queueFileName )
            
            if comfun.fileExists ( dataPath + self.nodesFileName, "" ) == False :
                comfun.createEmptyFile ( dataPath + self.nodesFileName )
            
            if comfun.fileExists ( dataPath + self.projectsFileName, "" ) == False :
                comfun.createEmptyFile ( dataPath + self.projectsFileName )
        
        if self.storeDataMode == 2:   #  1 text file   2  sqlite  3 MySQL
            1
        if self.storeDataMode == 3:   #  1 text file   2  sqlite  3 MySQL
            1
            
    def updateColors (self): 
        paletteID = self.colorsMode
        if paletteID == 1 :
            file = self.batchDataPath+"colors_gray.ini"
        if paletteID == 2 :
            file = self.batchDataPath+"colors_pastel.ini"
        if paletteID == 3 :
            file = self.batchDataPath+"colors_dark.ini"
        if paletteID == 4 :
            file = self.batchDataPath+"colors_custom.ini"
            
        print " [INF] loading colors: " + file
        
        if self.comfun.fileExists (file, "colors file" ) :
            self.stateColors = []
            self.stateColorsUp = []
            for i in range (0, 40):
                # print "a " , i
                self.stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
                self.stateColorsUp.append ( QBrush( QColor.fromRgb(  140, 140, 140, a=255) ) )
                
            f = open(file, 'r')
            liCounter = 0
            for line in f.readlines() :
                li = line.split(";")
                if len ( li ) > 7 :
                    self.stateColors[liCounter] = QBrush( QColor.fromRgb( self.comfun.intOrVal(li[2], 40), self.comfun.intOrVal(li[3], 40), self.comfun.intOrVal(li[4], 40),        a=255) )
                    self.stateColorsUp[liCounter] = QBrush( QColor.fromRgb( self.comfun.intOrVal(li[6], 140), self.comfun.intOrVal(li[7], 140), self.comfun.intOrVal(li[8], 140),        a=255) )
                    
                liCounter +=1
            f.close()
        else :
            for i in range (0, 40):
                self.stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
                self.stateColorsUp.append ( QBrush( QColor.fromRgb(  140, 140, 140, a=255) ) )
            
    
    def printSettings (self):
        print "\n[printSettings]\n"
        print "mode: "+ str( self.storeDataMode )   #  1 text file   2 SQL
        print "dir: "+self.batchDataPath
        print "schemas: ",self.schemasFileName
        print "tasks: ",self.tasksFileName
        print "queue: ", self.queueFileName
        print "nodes: ",self.nodesFileName
        print "projects: ",self.projectsFileName
        print "sqlite: ", self.sqliteFileName
        print "MySQL host: ", self.mysqlHost
        print "MySQL user: ", self.mysqlUser
        print "MySQL pass: ", self.mysqlPass
        print "MySQL port: ", self.mysqlPort
        
        
        
    def loadDefColors (self, stateColors , stateColorsUp ):
        # self
        # stateColors = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColors.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        
        stateColors[0] = QBrush( QColor.fromRgb(  40, 40, 40, a=255) )    # None  GRAY
        stateColors[1] =  QBrush( QColor.fromRgb(  220, 211, 202, a=255) )    #   Yellow INIT        T Q N
        stateColors[2] =  QBrush( QColor.fromRgb(  255, 220, 130, a=255) )    #   Yellow WAIT        T Q N
        stateColors[3] =  QBrush( QColor.fromRgb(  130, 202, 220, a=255) )      #   BLUEa   QUEUED      T
        stateColors[4] =  QBrush( QColor.fromRgb(  108, 130, 220, a=255) )     #   BLUEb   WORKING     T Q N
        stateColors[5] =  QBrush( QColor.fromRgb(  130, 202, 240, a=255) )      #   BLUEa  DONE        T Q
        stateColors[6] =  QBrush( QColor.fromRgb(  108, 130, 240, a=255) )      #   BLUEb    ERR         T Q N
        stateColors[7] =  QBrush( QColor.fromRgb(  130, 202, 250, a=255) )      #   BLUEa    ERR         T Q N
        stateColors[8] =  QBrush( QColor.fromRgb(  108, 130, 250, a=255) )      #   BLUEb    ERR         T Q N
        stateColors[9] =  QBrush( QColor.fromRgb(  220, 70, 70, a=255) )      #   RED    ERR         T Q N
        stateColors[10] =  QBrush( QColor.fromRgb(  22, 220, 70, a=255) )      #   Green  OK        T Q
        stateColors[11] =  QBrush( QColor.fromRgb(  22, 220, 70, a=255) )      #   Green  DONE        T Q
        stateColors[12] =  QBrush( QColor.fromRgb(  22, 220, 70, a=255) )      #   Green  ACCEPTED        T Q
        stateColors[13] =  QBrush( QColor.fromRgb(  220, 130, 70, a=255) )      #   xRED    REJECTED         T Q N
        
        addUp = 20
        # stateColorsUp = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        stateColorsUp.append ( QBrush( QColor.fromRgb(  40, 40, 40, a=255) ) )
        
        stateColorsUp[0] = QBrush( QColor.fromRgb(  40 + addUp, 40 + addUp, 40 + addUp, a=255) )    # None  GRAY
        stateColorsUp[1] =  QBrush( QColor.fromRgb(  220 + addUp, 211 + addUp, 202 + addUp, a=255) )    #   Yellow INIT        T Q N
        stateColorsUp[2] =  QBrush( QColor.fromRgb(  255, 220 + addUp, 130 + addUp, a=255) )    #   Yellow WAIT        T Q N
        stateColorsUp[3] =  QBrush( QColor.fromRgb(  130 + addUp, 202 + addUp, 220, a=255) )      #   BLUEa   QUEUED      T
        stateColorsUp[4] =  QBrush( QColor.fromRgb(  108 + addUp, 130 + addUp, 220, a=255) )     #   BLUEb   WORKING     T Q N
        stateColorsUp[5] =  QBrush( QColor.fromRgb(  130 + addUp, 202 + addUp, 240, a=255) )      #   BLUEa  DONE        T Q
        stateColorsUp[6] =  QBrush( QColor.fromRgb(  108 + addUp + addUp, 130, 240, a=255) )      #   BLUEb    ERR         T Q N
        stateColorsUp[7] =  QBrush( QColor.fromRgb(  130 + addUp, 202, 250, a=255) )      #   BLUEa    ERR         T Q N
        stateColorsUp[8] =  QBrush( QColor.fromRgb(  108 + addUp + addUp, 130, 250, a=255) )      #   BLUEb    ERR         T Q N
        stateColorsUp[9] =  QBrush( QColor.fromRgb(  220, 70 + addUp + addUp, 70 + addUp + addUp, a=255) )      #   RED    ERR         T Q N
        stateColorsUp[10] =  QBrush( QColor.fromRgb(  22 + addUp + addUp, 220, 70 + addUp, a=255) )      #   Green  OK        T Q
        stateColorsUp[11] =  QBrush( QColor.fromRgb(  22 + addUp + addUp, 220, 70 + addUp, a=255) )      #   Green  DONE        T Q
        stateColorsUp[12] =  QBrush( QColor.fromRgb(  22 + addUp + addUp, 220, 70 + addUp, a=255) )      #   Green  ACCEPTED        T Q
        stateColorsUp[13] =  QBrush( QColor.fromRgb(  220, 130 + addUp, 70 + addUp, a=255) )      #   xRED    REJECTED         T Q N
    