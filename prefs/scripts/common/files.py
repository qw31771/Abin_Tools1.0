import maya.cmds as cmds
from functools import wraps
import maya.mel as mel
import os
'''
maya文件处理类
update: 2024.12.13
by:余杰滨
'''

#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds .undoInfo(closeChunk=True)
        return result
    return wrap

class ScenceInfo():
    scenceFile=mel.eval("file -q -location")
    currentPath=os.path.split((scenceFile))[0]
    scencePath=currentPath[0:currentPath.rfind("/")]