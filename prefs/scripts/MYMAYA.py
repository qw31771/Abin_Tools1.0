import os
import maya.mel as mel
import maya.cmds as cmds
from PySide2.QtCore import *
from PySide2.QtWidgets import QApplication

#名字路径通用类
class PATH():
    #工具路径
    TOOLPATH=cmds.internalVar(usd=1)+"Abin_Tools"

    #初始化路径
    PREFS=TOOLPATH+"/prefs"

    #icon路径
    IOCONS=TOOLPATH+"/icons"

    #脚本路径
    SCRIPTS=TOOLPATH+"/scripts"

    #工具路径
    TOOLS=TOOLPATH+"/tools"

    #UI路径
    ui=TOOLPATH+"/ui"


class SAVE():
    #设置路径
    SETTING=PATH.PREFS+"/setting"

    #保存文件名称
    INIT_WIN="maya_abin_tools.ini"

    #树节点窗口文件名称
    INIT_TWIN="maya_tree_win.ini"

    #树节点Item对应icon
    INIT_TWINICON="maya_tree_win_icon.ini"

    #窗口信息
    WIN_INFO = os.path.join(SETTING, INIT_WIN)

    #树窗口信息
    WIN_TINFO = os.path.join(SETTING, INIT_TWIN)

    #树窗口Icon信息
    WIN_TICONINFO = os.path.join(SETTING, INIT_TWINICON)

    QSETTING=QSettings(WIN_INFO, QSettings.IniFormat)
    QSETTING.setIniCodec('utf-8')

    TQSETTING=QSettings(WIN_TINFO, QSettings.IniFormat)
    TQSETTING.setIniCodec('utf-8')

    TQICONSETTING=QSettings(WIN_TICONINFO, QSettings.IniFormat)
    TQICONSETTING.setIniCodec('GBK')
    #位置
    WIN_POS="win_pos"

    #大小
    WIN_SIZE="win_size"

    SOURCE="source_path"
    # #工具排序信息
    # TOOLS_TREE="tools_treeWidget"

    

class MYSCREEN():

    SCREEN =  QApplication.primaryScreen().geometry()

    WIDTH=SCREEN.width()

    HEIGHT=SCREEN.height()

    def getScreenPx(px):
        return (px*MYSCREEN.WIDTH)/2160
    

class ToolWinMsg():
    name:str=None
    index:int=None
    icon:str=None
    child:dict=None
