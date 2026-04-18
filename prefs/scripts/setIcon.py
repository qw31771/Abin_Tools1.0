import maya.cmds as cmds
from sys import path
from importlib import reload


FILE_LIST=["/scripts","/prefs/scripts/ui","/prefs/scripts/ts_toolStart","/prefs/scripts/common",
           "/prefs/scripts/ui/main_UI","/prefs/scripts/ui/custom_UI"]
SOURCE=cmds.internalVar(usd=1)+"Abin_Tools"
for FILE in FILE_LIST:
    PATH=SOURCE+FILE
    if PATH not in path:
        path.append(PATH)


if  (cmds.iconTextButton( "ABIN_TOOLS_ICONBUTTON",ex=1,q=1)):
    cmds.deleteUI("ABIN_TOOLS_ICONBUTTON")

file=cmds.internalVar(userScriptDir=True) +"/Abin_Tools"
logo_base = file+"/prefs/icons/abin_base.png" 
abin_hover = file+"/prefs/icons/abin_hover.png" 
parent=cmds.iconTextButton("statusFieldButton",q=1,p=1)
cmds.iconTextButton("ABIN_TOOLS_ICONBUTTON",i=logo_base,hi=abin_hover,ann="ABIN TOOLS",c="exec(open(\""+file+"/prefs/scripts/showUI.py\", encoding=\'utf-8\').read())",p=parent)
