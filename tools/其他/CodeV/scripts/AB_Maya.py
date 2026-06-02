import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtWidgets
import os
import saveData
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

    def __init__(self, unparent,enabled=True,strip_prefix=None):
        self.original_names = {}  # (UUID, name_within_namespace)
        self.parent = {}
        if enabled and unparent and unparent[0].find(':') != -1:
            namespace = unparent[0].split(':')[0]
            self.namespace = cmds.namespaceInfo(namespace, fn=True)
        else:
            self.namespace = ''
        
        self.strip_prefix=strip_prefix
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
        
        if self.strip_prefix:
            # 收集所有目标节点（item + 后代）
            all_nodes = [item]
            descendants = cmds.listRelatives(item, allDescendents=True, fullPath=True)
            if descendants:
                all_nodes.extend(descendants)

            # 第一步：获取每个节点的 MObject 和当前短名
            node_data = []  # (mobj, short_name, full_path)
            for full_path in all_nodes:
                if not cmds.objExists(full_path):
                    continue
                try:
                    selList = om.MSelectionList()
                    mobj = om.MObject()
                    om.MGlobal.getSelectionListByName(full_path, selList)
                    selList.getDependNode(0, mobj)
                    api_node = om.MFnDependencyNode(mobj)
                    short_name = full_path.split('|')[-1]
                    if short_name.startswith(self.strip_prefix):
                        node_data.append((mobj, short_name, api_node))
                except:
                    pass

            # 第二步：统一重命名（此时所有节点都已通过 MObject 锁定）
            for mobj, short_name, api_node in node_data:
                try:
                    new_short = short_name[len(self.strip_prefix):]
                    if not new_short:
                        continue
                    uuid = api_node.uuid().asString()
                    if uuid not in self.original_names:
                        self.original_names[uuid] = api_node.name()
                    api_node.setName(new_short)
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

_UI_PROGRESS_BAR = None  # 你的插件界面进度条
_MAYA_PROGRESS_BAR = None # Maya 底层进度条

def register_progress_bar(bar_instance):
    global _UI_PROGRESS_BAR, _MAYA_PROGRESS_BAR
    _UI_PROGRESS_BAR = bar_instance
    # 同时获取 Maya 主进度条
    _MAYA_PROGRESS_BAR = mel.eval('$tmp = $gMainProgressBar')

def set_progress_range(min_val=0, max_val=100):
    global _UI_PROGRESS_BAR, _MAYA_PROGRESS_BAR
    # 设置插件 UI 范围
    if _UI_PROGRESS_BAR:
        _UI_PROGRESS_BAR.setRange(min_val, max_val)
    # 设置 Maya 状态栏范围
    if _MAYA_PROGRESS_BAR:
        cmds.progressBar(_MAYA_PROGRESS_BAR, edit=True, beginProgress=True, 
                         isInterruptable=True, minValue=min_val, maxValue=max_val)

def update_progress(value, text=None):
    global _UI_PROGRESS_BAR, _MAYA_PROGRESS_BAR
    
    # 更新插件界面上的进度条
    if _UI_PROGRESS_BAR:
        try:
            _UI_PROGRESS_BAR.setValue(int(value))
            if text:
                _UI_PROGRESS_BAR.setFormat(f"{text}  %p%")
        except: pass

    # 更新 Maya 状态栏进度条
    if _MAYA_PROGRESS_BAR:
        try:
            if cmds.progressBar(_MAYA_PROGRESS_BAR, query=True, isCancelled=True):
                cmds.progressBar(_MAYA_PROGRESS_BAR, edit=True, endProgress=True)
                raise RuntimeError("用户取消了操作")
            cmds.progressBar(_MAYA_PROGRESS_BAR, edit=True, progress=int(value))
            if text:
                cmds.progressBar(_MAYA_PROGRESS_BAR, edit=True, status=text)
        except: pass
        
    # 强制刷新 UI，这是进度条会动的核心
    QtWidgets.QApplication.processEvents()

def end_progress():
    global _MAYA_PROGRESS_BAR
    if _MAYA_PROGRESS_BAR:
        cmds.progressBar(_MAYA_PROGRESS_BAR, edit=True, endProgress=True)


def getConfig(name,path=saveData.PATH.setting)->QSettings:
    config_path=os.path.join(path, name+".ini")
    config=QSettings(config_path, QSettings.IniFormat)
    config.setIniCodec('UTF-8')
    return config

def toList(value):
        if isinstance(value, list):
            return value  
        else:
            return [value] 