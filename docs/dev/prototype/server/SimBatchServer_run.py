#  hack update
from os import path
def fileExists (  checkFile, fileType ) :
    if path.exists ( checkFile ):
        return True 
    else:
        if len(fileType) > 0:
            print " [ERR] 52 ", fileType, "not exist !  (",  checkFile ,")\n"
        return False
        
from shutil import copyfile
forceLibCopy = True
if forceLibCopy:
    src_dir = "S:\\sib_src\\SimBatch\\"
    dest_dir = "S:\\sib_src\\SimBatch_server\\SimBatchLib\\"
    f="SimBatchLibCommon.py"
    if fileExists(src_dir+f, f) :
        copyfile(src_dir+f,dest_dir+f)
    f="SimBatchLibQueue.py"
    if fileExists(src_dir+f, f) :
        copyfile(src_dir+f,dest_dir+f)
    f="SimBatchLibNodes.py"
    if fileExists(src_dir+f, f) :
        copyfile(src_dir+f,dest_dir+f)
    f="SimBatchLibSettings.py"
    if fileExists(src_dir+f, f) :
        copyfile(src_dir+f,dest_dir+f)
    f="SimBatchLibServer.py" ###  SimBatchLibSimulate
    if fileExists(src_dir+f, f) :
        copyfile(src_dir+f,dest_dir+f)
    f="SimBatchLibSoftwares.py"
    if fileExists(src_dir+f, f) :
        copyfile(src_dir+f,dest_dir+f)
        
#  hack update FIN


# import sys
# sys.path.append ('S:\\sib_src\\PyLibs\\win32')
# sys.path.append ('S:\\sib_src\\PyLibs\\win32\\lib')

# import os
import subprocess
import threading
import time
# import win32api
# import wmi
# c = wmi.WMI()
# for process in c.Win32_Process (name="maya.exe")      prnt process.ProcessId

# from SimBatchLib import SimBatchLibSettings
from SimBatchLib import SimBatchLibCommon
# from SimBatchLib import SimBatchLibQueue

# from SimBatchLib.SimBatchLibCommon import *
from SimBatchLib.SimBatchLibSettings import Settings
from SimBatchLib.SimBatchLibQueue import *
from SimBatchLib.SimBatchLibNodes import *
from SimBatchLib.SimBatchLibSoftwares import *
from SimBatchLib.SimBatchLibServer import SimBatchServer  ### SimBatchLibSimulate




# settings = SimBatchLibSettings.Settings(2)
settings = Settings(0)
# settings.storeDataMode = 1
settings.loadSettings ("S:\\sib_src\\dataStore.ini") 
    
soCo = SoftwaresConnector( 0 )


SBS = SimBatchServer( settings ,  Queue( settings ) ,  SimNodes( settings ),  soCo )


SBS.run()



