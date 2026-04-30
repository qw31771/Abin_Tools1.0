import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import os
from importlib import reload
import CustomUI
reload(CustomUI)

#Maya
def scencePath():
    scenceFile=mel.eval("file -q -location")
    currentPath=os.path.split((scenceFile))[0]
    # path=currentPath[0:currentPath.rfind("/")]
    return currentPath

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



class StripNamespace(object):
    @classmethod
    def as_name(cls, uuid):
        names = cmds.ls(uuid)
        if names:
            for name in names:
                if ':' not in name:
                    return name
        else:
            return None

    def __init__(self, unparent,enabled=True):
        self.original_names = {}  # (UUID, name_within_namespace)
        self.parent = {}
        if enabled and unparent and unparent[0].find(':') != -1:
            namespace = unparent[0].split(':')[0]
            self.namespace = cmds.namespaceInfo(namespace, fn=True)
        else:
            self.namespace = ''

        self.unparent = unparent

    def toMObject(self, node):
        selList = om.MSelectionList()
        selList.add(str(node))
        mObject = om.MObject()
        selList.getDependNode(0, mObject)
        return mObject

    def __enter__(self):
        if self.unparent:
            for item in self.unparent:
                selList = om.MSelectionList()
                api_obj = om.MObject()
                om.MGlobal.getSelectionListByName(item, selList)
                selList.getDependNode(0, api_obj)
                dag_parent = cmds.listRelatives(item, p=1)
                if dag_parent:
                    self.parent[item] = dag_parent[0]

                dag_modi = om.MDagModifier()
                dag_modi.reparentNode(api_obj)
                dag_modi.doIt()
        if self.namespace:
            for absolute_name in cmds.namespaceInfo(self.namespace, listOnlyDependencyNodes=True, fullName=True):
                # Ensure node was *not* auto-renamed (IE: shape nodes)
                if cmds.objExists(absolute_name):
                    # get an api handle to the node
                    try:
                        selList = om.MSelectionList()
                        api_obj = om.MObject()
                        om.MGlobal.getSelectionListByName(absolute_name, selList)
                        selList.getDependNode(0, api_obj)
                        api_node = om.MFnDependencyNode(api_obj)

                        # remember the original name to return upon exit
                        uuid = api_node.uuid().asString()
                        self.original_names[uuid] = api_node.name()
                        
                        # strip namespace by renaming via api, bypassing read-only restrictions
                        without_namespace = api_node.name().replace(self.namespace, '', 1)
                        api_node.setName(without_namespace)
                    except:
                        pass

        return [self.as_name(uuid) for uuid in self.original_names]

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print(self.original_names)
        for uuid, original_name in self.original_names.items():
            try:
                current_name = self.as_name(uuid)
                selList = om.MSelectionList()
                api_obj = om.MObject()
                om.MGlobal.getSelectionListByName(current_name, selList)
                selList.getDependNode(0, api_obj)
                api_node = om.MFnDependencyNode(api_obj)
                api_node.setName(original_name)
            except:
                pass

        if self.parent:
            for absolute_name, parent in self.parent.items():
                dag_modi = om.MDagModifier()
                absolute_name_mobject = self.toMObject(absolute_name)
                parent_mobject = self.toMObject(parent)
                dag_modi.reparentNode(absolute_name_mobject, parent_mobject)
                dag_modi.doIt()


# GeneralFunc.py 

import maya.OpenMayaUI as omui
from PySide2 import QtWidgets

def update_progress(value, text=None, visible=True):
    """
    全局进度条更新接口
    :param value: 0-100 的整数
    :param text: 进度条显示的文本描述
    :param visible: 是否显示进度条
    """
    # 1. 获取 Maya 主窗口句柄
    main_window_ptr = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)
    
    # 2. 查找我们的 AdhesiveWindow (DockWidget)
    # 注意：这里查找的是类中定义的 QDockWidget 对象
    window = main_window.findChild(QtWidgets.QDockWidget, "Abin_CodeV") 
    # 如果你在 UI 类里没设置 ObjectName，可以根据 WindowTitle 找，
    # 或者在 AdhesiveWindow.__init__ 里加上 self.setObjectName("AbinCodeV_Main")
    
    if window and hasattr(window, 'progress_bar'):
        window.progress_bar.setVisible(visible)
        window.progress_bar.setValue(value)
        if text:
            window.progress_bar.setFormat(f"{text}  %p%")
        
        # 强制处理界面事件，防止 Maya 在计算时 UI 假死
        QtWidgets.QApplication.processEvents()