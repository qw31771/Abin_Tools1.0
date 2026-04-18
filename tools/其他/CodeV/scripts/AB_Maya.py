import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os
from importlib import reload
import CustomUI
reload(CustomUI)

#Maya
def scencePath():
    scenceFile=mel.eval("file -q -location")
    currentPath=os.path.split((scenceFile))[0]
    path=currentPath[0:currentPath.rfind("/")]
    return path

def addSets(obj,path,em=0):
    paths=path.split('/')
    last=''
    for i in paths:
        try:
            cmds.sets(i,q=1)
        except:
            cmds.sets(n=i,em=1)
        if last:
            cmds.sets(i,e=1,fe=last)
        last=i
    if em or not obj:
        cmds.sets(cl=last)
    
    if obj:
        cmds.sets(obj,e=1,fe=last)

#UI
def setGroupBox(title="",size=16,color=(255,255,255))-> QGroupBox:
    box=CustomUI.setGroupBox(title,size,color)         
    return box

def imgButton(size,url,tips="")-> QPushButton:
    button = CustomUI.ImageButton(size,url,tips)
    return button

def checkBox(name,checked,color=None)-> QCheckBox:
    return CustomUI.checkBox(name,checked,color)

def popWidgetMenu(title="",vis=False,content=None)-> QHBoxLayout:
    layout = CustomUI.popWidgetMenu(title,vis,content)
    return layout

def hLine(px=2,color='rgb(0,0,0)')-> QFrame:
    line=CustomUI.Line(px,color)
    return line

def titleComboBox(title,combo,margins=[0,0,0,0])-> QHBoxLayout:
    menu=CustomUI.titleComboBox(title,combo,margins)
    return menu

