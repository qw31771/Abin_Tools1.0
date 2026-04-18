import maya.cmds as cmds
import maya.mel as mel

from functools import wraps

#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds.undoInfo(closeChunk=True)
        return result
    return wrap

@make_undo
def script():
    import common
    sl=cmds.ls(sl=1)
    # skinJointList=[]
    for mesh in sl:
        skin=mel.eval("findRelatedSkinCluster" +"(\""+ mesh +"\")")
        skinJoint = cmds.skinCluster(skin, query=True, weightedInfluence=1)
        common.sets(skinJoint,mesh+"_Sets")
        
    


script()



