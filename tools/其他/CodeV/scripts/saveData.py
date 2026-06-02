from PySide2.QtCore import *
import os
from enum import Enum

class PATH:
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(current_file_path)

    path=os.path.dirname(current_dir)

    icon=path+"/icons"

    setting=path+"/settings"

    export_presets=setting+"/导出预设"

class 常用配置(Enum):
    """常用配置枚举"""
    表头='bt'
    模型_动画表头='mxdh'

class 导出配置键(Enum):
    """配置文件键名枚举"""
    预设列表 = "presets"
    当前预设 = "current_preset"
    几何弹窗 = "geometry_pop"
    设置弹窗 = "set_pop"
    移除弹窗 = "remove_pop"
    关键词列表 = "keys"
    集合弹窗 = "sets_pop"
    导出弹窗 = "export_pop"

    导出弹窗_动画 = "export_pop"
    设置弹窗_动画 = "set_pop"

class 导出预设配置键(Enum):
    """预设配置键名枚举"""
    平滑组 = "phz"
    三角化 = "sjh"
    平滑网络 = "phwl"
    切线法线 = "qxfx"
    切割法线 = "qgfx"
    蒙皮 = "mp"
    
    零帧导出 = "lz"  
    删除引用 = "scyy"
    输入连接 = "srlj"
    子对象 = "zdx"
    上方轴向_模型 = "sfzx"

    导出集合 = "sets"

    导出模式 = "export_model"
    导出文件 = "export_files"

    #动画
    导出选择 = "export_select"
    移动到原点 = "yd"
    烘焙动画 = "hbdh"
    上方轴向_动画 = "sfzx"
    模式_动画 = "export_model"
    跳过骨骼 = "skip_joints"

