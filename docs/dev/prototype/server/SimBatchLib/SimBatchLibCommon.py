
import sys
from os import path
from os import makedirs
from datetime import datetime

class CommonFunctions():

    def printArray (self, arr, checkIsFloat = False ):
        counter = 0
        for ai in arr :
            if checkIsFloat :
                print "     ", counter, " : " , ai, "   ___  ", self.isfloat(ai)
            else:
                print "     ", counter, " : " , ai
            counter +=1
            
            
    def arrayAsSrting ( self, arr, onlyFirst=0 , fromItem=0, separator =";"):
        counter = 0
        retStr = ""
        if len (arr) == 1 or onlyFirst == 1 :
            if len (arr) > 0: # empty only first
                return str(arr[0])
            else:
                return ""
        else:
            for a in arr:
                if counter >= fromItem:
                    retStr += str(a) + separator
        return retStr

    def createEmptyFile(self, file):
        textFile = open(file, "w")
        textFile.write("")
        textFile.close()
        
    def loadFromFile(self, file ):
        textFile = open(file, "r")
        content = textFile.readlines()
        content = [x.strip() for x in content]
        textFile.close()
        return content
        
    def saveToFile(self, file, content ):
        textFile = open(file, "w")
        textFile.write(content)
        textFile.close()
        
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
        
        
        
    def pathExists ( self, checkPath, dirType ) :
        if path.exists ( checkPath ):
            return True
        else:
            if len(dirType) > 0:
                print " [ERR_78] ", dirType ," dont exist"
            return False
            
    def getProperPatch ( self, path ):
        if len( path ) > 3:
            if path[len(path)-1] != "\\":
                path = path + "\\"
        return path
        
    def fileExists ( self, checkFile, fileTypeMessage ) :
        if path.exists ( checkFile ):
            return True 
        else:
            if len(checkFile) > 0 :
                if len(fileTypeMessage) > 0:
                    print " [ERR_94]  ", fileTypeMessage, "not exist !  (",  checkFile ,")\n"
            else:
                print " [ERR_98] [fileExists] checkFile  empty! \n"
            return False
            
    # def createDirectoryIfNotExist ( self , dir ):
        # if len( dir ) > 3:
            # if not path.exists(dir):
                # makedirs(dir)
        # else:
            # print " [ERR] directory not created  (",  dir ,")\n"
            
            
            
    def currentScriptsPath( self ):
        # print " [DB] currentScriptsPath ", path.dirname( path.realpath(sys.argv[0]) )
        return (   path.dirname( path.realpath(sys.argv[0]) ) +"\\" )
            
    def addWigdets ( self, lay, arr ):
        for ar in arr:
            lay.addWidget(ar)
            
    def addLayouts ( self, lay, arr ):
        for ar in arr:
            lay.addLayout(ar)
            
    def strWithZeros (self, number, zeros=3 ):
        stri = str(number)
        while len(stri)<zeros:
            stri="0"+stri
        return stri
        
    def isStringInArray( self, stringsArray , wantedString ,  exactly=True, starting = False, db = True ):
        counter = 0 
        if len(wantedString ) < 2:
            starting = True
        for sa in stringsArray:
            # if db :
                # print " [INF db ] TEST: " ,    sa , wantedString ,   exactly , starting
            if exactly:
                if sa == wantedString:
                    if db :
                        print " [INF db ] isStringInArray : exactly " ,    sa , wantedString
                    return counter
            else:
                if starting :
                    if sa.startswith(wantedString):
                        if db :
                            print " [INF db ] isStringInArray :  starting " ,    sa , wantedString
                        return counter
                else:
                    ret = sa.find(wantedString)
                    if ret >=0:
                        if db :
                            print " [INF db ] isStringInArray :  substring " ,    sa , wantedString
                        return counter
                    ret = wantedString.find(sa)
                    if ret >=0:
                        if db :
                            print " [INF db ] isStringInArray :  substring " ,    sa , wantedString
                        return counter
                    
            counter +=1
        return -1
        
        
    def getCurrentTime(self, filenameMode = False, onlyTime=False):
        if filenameMode :
            return datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        else:
            if onlyTime :
                return datetime.now().strftime('%H:%M:%S')
            else:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    # def getDate (self):
        # return time.strftime("%Y-%m-%d_%H:%M:%S")
        
        
    def isAbsolute (self,path):
        if len(path) > 2 :
            if path[1] == ":" and path[2] == "\\" :
                return 1
            if path[0] == "\\" and path[1] == "\\" :
                return 1
        return 0
        
    def getGetDirectory (self, editLine, QFileDialog, forceStartDir="P:\\"):
        StartDir=""
        if len(forceStartDir) >0 :
            StartDir = forceStartDir
        else:
            if len( editLine.text() ) > 0 :
                StartDir = editLine.text()
        
        getDirectory =  QFileDialog.getExistingDirectory( dir = StartDir )  #caption="caroo"
        getDirectory = getDirectory.replace("/","\\")
        print ' [INF] selected_directory:', getDirectory
        if len(getDirectory) > 0 :
            editLine.setText( getDirectory + "\\" )
            return (getDirectory + "\\")
        return ""
        
    def getGetFile (self, editLine, QFileDialog, initDir):
        getDirectory =  QFileDialog.getOpenFileName( dir=initDir )
        # print ' [INF] selected_file:', getDirectory
        # print ' [INF] selected_file:', getDirectory[0]
        getDir = getDirectory[0].replace("/","\\")        
        
        if len ( getDir ) > 0 :
            editLine.setText( getDir  )
        
    def getSaveFile (self, editLine, QFileDialog):
        getDirectory =  QFileDialog.getSaveFileName()
        # getDirectory[0] = getDirectory[0].replace("/","\\")
        # print ' [INF] fileToSave:', getDirectory
        getDir = getDirectory[0].replace("/","\\")
        if len ( getDir ) > 0 :
            editLine.setText( getDir + "\\" )
        
                
        
    def getIncrementName ( self, nameIn, db = False ):   
        lastNotDigit = next (( i for i,j in list(enumerate(nameIn,1))[::-1] if not j.isdigit()  ) , -1 )
        
        if (len(nameIn) - lastNotDigit) > 0:
            if db:
                print "\n lastNotDigit " , len(nameIn) - lastNotDigit,   nameIn[:-(len(nameIn) - lastNotDigit)] , "  ___  " ,    nameIn[-(len(nameIn) - lastNotDigit):]
        else:
            if db:
                print "\n empty"
        
        if (len(nameIn) - lastNotDigit) > 0:
            head = nameIn[:-(len(nameIn) - lastNotDigit)]
            number  = self.strWithZeros(     int(nameIn[-(len(nameIn) - lastNotDigit):])+1 ,    len(nameIn[-(len(nameIn) - lastNotDigit):]) )
        else :
            head = nameIn
            number = "_02"
            
        if db:
            print  "_______",head , number
            
        return (head+number)
        
        
            
        
    
    
    
    
    
    
    
    
    