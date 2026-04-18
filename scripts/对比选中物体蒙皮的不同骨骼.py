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
    sl=cmds.ls(sl=1)
    skinJointList=[]
    for mesh in sl:
        skin=mel.eval("findRelatedSkinCluster" +"(\""+ mesh +"\")")
        skinJoint = cmds.skinCluster(skin, query=True, weightedInfluence=1)
        skinJointList.append(skinJoint)

    uc=[]
    if skinJointList:
        common = set(skinJointList[0])
        for arr in skinJointList[1:]:
            common.intersection_update(arr)
        union = set()
        for arr in skinJointList:
            union.update(arr)


        uc= (union - common)
    
    if uc:
        print(uc)
        cmds.select(uc)
    else:
        cmds.warning("蒙皮骨骼相同")

script()