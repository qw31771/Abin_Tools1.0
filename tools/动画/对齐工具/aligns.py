# -*- coding: utf-8 -*-
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
def get_Align_target(obj, objs):
    #获得第一个世界坐标
    matrixs = cmds.xform(obj, q=True, ws=True, m=True)
    #获取第二个的相对坐标
    getAttrPos = cmds.getAttr(objs + ".translate")
    getAttrRot = cmds.getAttr(objs + ".rotate")
    getAttrSca = cmds.getAttr(objs + ".scale")
    return matrixs, getAttrPos, getAttrRot, getAttrSca

@make_undo
def set_Align_target(posX=True, posY=True, posZ=True, rotX=True, rotY=True, rotZ=True, scaX=True, scaY=True, scaZ=True):
    sel = cmds.ls(sl=True, fl=True)
    data = get_Align_target(sel[0], sel[1])
    #设置第二个的世界坐标
    cmds.xform(sel[1], ws=True, m=data[0])
    #获取的第二个的相对坐标
    offset_pos = cmds.getAttr(sel[1] + ".translate")
    offset_rot = cmds.getAttr(sel[1] + ".rotate")
    offset_sca = cmds.getAttr(sel[1] + ".scale")

    # 位置对齐
    try:
        if posX == True and posY != True and posZ != True:
            cmds.setAttr(sel[1] + ".translate", offset_pos[0][0], data[1][0][1], data[1][0][2])

        elif posY == True and posX != True and posZ != True:
            cmds.setAttr(sel[1] + ".translate", data[1][0][0], offset_pos[0][1], data[1][0][2])

        elif posZ == True and posX != True and posY != True:
            cmds.setAttr(sel[1] + ".translate", data[1][0][0], data[1][0][1], offset_pos[0][2])

        elif posX == True and posY == True and posZ == True:
            cmds.setAttr(sel[1] + ".translate", offset_pos[0][0], offset_pos[0][1], offset_pos[0][2])

        elif posX == True and posY == True and posZ != True:
            cmds.setAttr(sel[1] + ".translate", offset_pos[0][0], offset_pos[0][1], data[1][0][2])

        elif posX == True and posZ == True and posY != True:
            cmds.setAttr(sel[1] + ".translate", offset_pos[0][0], data[1][0][1], offset_pos[0][2])

        elif posY == True and posZ == True and posX != True:
            cmds.setAttr(sel[1] + ".translate", data[1][0][0], offset_pos[0][1], offset_pos[0][2])
        else:
            cmds.setAttr(sel[1] + ".translate", 0, 0, 0)
    except:
        cmds.error("当前控制器位移属性被锁定或隐藏,请解锁位移属性或不勾选位移对齐")

    # 旋转对齐
    try:
        if rotX == True and rotY != True and rotZ != True:
            cmds.setAttr(sel[1] + ".rotate", offset_rot[0][0], data[2][0][1], data[2][0][2])

        elif rotY == True and rotX != True and rotZ != True:
            cmds.setAttr(sel[1] + ".rotate", data[2][0][0], offset_rot[0][1], data[3][0][2])

        elif rotZ == True and rotX != True and rotY != True:
            cmds.setAttr(sel[1] + ".rotate", data[2][0][0], data[2][0][1], offset_rot[0][2])

        elif rotX == True and rotY == True and rotZ == True:
            cmds.setAttr(sel[1] + ".rotate", offset_rot[0][0], offset_rot[0][1], offset_rot[0][2])

        elif rotX == True and rotY == True and rotZ != True:
            cmds.setAttr(sel[1] + ".rotate", offset_rot[0][0], offset_rot[0][1], data[2][0][2])

        elif rotX == True and rotZ == True and rotY != True:
            cmds.setAttr(sel[1] + ".rotate", offset_rot[0][0], data[2][0][1], offset_rot[0][2])

        elif rotY == True and rotZ == True and rotX != True:
            cmds.setAttr(sel[1] + ".rotate", data[2][0][0], offset_rot[0][1], offset_rot[0][2])
        else:
            cmds.setAttr(sel[1] + ".rotate", 0, 0,  0)

    except:
        cmds.error("当前控制器旋转属性被锁定或隐藏,请解锁旋转属性或不勾选旋转对齐")

    # try:
    if scaX == True and scaY != True and scaZ != True:
        cmds.setAttr(sel[1] + ".scale", offset_sca[0][0], data[3][0][1], data[3][0][2])

    elif scaY == True and scaX != True and scaZ != True:
        cmds.setAttr(sel[1] + ".scale", data[3][0][0], offset_sca[0][1], data[3][0][2])

    elif scaZ == True and scaX != True and scaY != True:
        cmds.setAttr(sel[1] + ".scale", data[3][0][0], data[3][0][1], offset_sca[0][2])

    elif scaX == True and scaY == True and scaZ == True:
        cmds.setAttr(sel[1] + ".scale", offset_sca[0][0], offset_sca[0][1], offset_sca[0][2])

    elif scaX == True and scaY == True and scaZ != True:
        cmds.setAttr(sel[1] + ".scale", offset_sca[0][0], offset_sca[0][1], data[3][0][2])

    elif scaX == True and scaZ == True and scaY != True:
        cmds.setAttr(sel[1] + ".scale", offset_sca[0][0], data[3][0][1], offset_sca[0][2])

    elif scaY == True and scaZ == True and scaX != True:
        cmds.setAttr(sel[1] + ".scale", data[3][0][0], offset_sca[0][1], offset_sca[0][2])

    else:
        cmds.setAttr(sel[1] + ".scale", data[3][0][0], data[3][0][1], data[3][0][2])
    # except:
        # cmds.error("当前控制器缩放属性被锁定或隐藏,请解锁缩放属性或不勾选缩放对齐")



