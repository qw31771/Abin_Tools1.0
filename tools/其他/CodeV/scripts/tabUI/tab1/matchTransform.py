import maya.cmds as cmds
import saveData
from functools import wraps
#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds .undoInfo(closeChunk=True)
        return result
    return wrap

@make_undo
def all_Match():
    se=cmds.ls(sl=1)
    if len(se)<2:
        return 
    cmds.matchTransform(se[0],se[1])
    cmds.select(se)

@make_undo
def att_Mtch(attName,att):
    se=cmds.ls(sl=1)
    if len(se)<2:
        return 
 
    skip=[]
    if not att[0]:
        skip.append("x")
    
    if not att[1]:
        skip.append("y")
    
    if not att[2]:
        skip.append("z")


    loc=cmds.spaceLocator()
    cmds.matchTransform(loc,se[0])

    if attName=="位移":
        ps=cmds.pointConstraint(se[1],loc,mo=0,skip=skip)[0]
        cmds.delete(ps)
    
    if attName=="旋转":
        ps=cmds.orientConstraint(se[1],loc,mo=0,skip=skip)[0]
        cmds.delete(ps)
    
    if attName=="缩放":
        ps=cmds.scaleConstraint(se[1],loc,mo=0,skip=skip)[0]
        cmds.delete(ps)

    # saveData.DQ.SETTING.setValue(attName,att)


    cmds.matchTransform(se[0],loc)
    cmds.delete(loc)
    cmds.select(se)


