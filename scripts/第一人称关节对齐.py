import maya.cmds as cmds
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
def setJoint():
    sl=["Scapula","Shoulder","Elbow","Wrist"]
    target=["R_Clavicle","R_Shoulder","R_Elbow","R_Hand"]
    for i in range(len(target)):
        pos=cmds.xform(target[i],q=1,ws=1,t=1)
        cmds.xform(sl[i],ws=1,t=pos)
        # cmds.matchTransform(sl[i],target[i])
    cmds.parent(["PinkyFinger1","RingFinger1"],"Wrist")
    cmds.rename("Cup","Cup_R")

    loc=cmds.spaceLocator()[0]
    cmds.parent(loc,"R_Hand")
    cmds.matchTransform(loc,"R_Hand")
    cmds.setAttr(loc+".translateX",-3)
    cmds.matchTransform("Cup_R",loc)
    cmds.delete(loc)
    cmds.makeIdentity("Cup_R",apply=1,t=1,r=1,s=1,n=0,pn=1)

    finger=["IndexFinger","MiddleFinger","RingFinger","PinkyFinger"]
    for i in finger:
        jnt=cmds.duplicate(i+"1",rr=1)[0]
        cmds.delete(jnt+"|"+i+"2")
        pa=cmds.rename(jnt,i+"0")
        cmds.parent(i+"1",pa)
        
    sl=["ThumbFinger","IndexFinger","MiddleFinger","RingFinger","PinkyFinger"]
    target=["R_Thumb","R_Index","R_Middle","R_Ring","R_Pinky"]
    for i in range(len(target)):
        s=sl[i]
        t=target[i]
        for j in range(5):
            try:
                cmds.matchTransform(s+str(j),t+str(j))
            except:
                pass
                if j==4:
                    cmds.matchTransform(s+str(j),t+str(j-1))
                    cmds.setAttr(s+str(j)+".translateX",-0.3)
                    if "Thumb" in s:
                        cmds.setAttr(s+str(j)+".translateX",-2)

    cmds.reorder("Cup_R",r=-1)

setJoint()