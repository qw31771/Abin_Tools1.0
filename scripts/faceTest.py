import maya.cmds as cmds
import math
from functools import wraps
import common

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
def create_bone_patches():
    # 获取选中的骨骼
    selected_bones = cmds.ls(selection=True)
    if not selected_bones:
        cmds.warning("请先选择对象！")
        return
    
    patches = []
    
    # 遍历每个骨骼
    for i, bone in enumerate(selected_bones):
        # 获取骨骼的世界坐标位置
        pos = cmds.xform(bone, query=True, worldSpace=True, translation=True)
        
        # 创建面片 (0.1x0.1)
        patch = cmds.polyPlane(
            width=0.1, 
            height=0.1, 
            sx=1, 
            sy=1, 
            axis=common.getWorldAxisInfo('fore',v=1),  
            name=f"{bone}_patch",
            constructionHistory=False
        )[0]
        
        # 移动面片到骨骼位置
        cmds.xform(patch, translation=pos, worldSpace=True)
        patches.append(patch)
        
        # 删除面片的历史记录
        cmds.delete(patch, constructionHistory=True)
    
    if not patches:
        return
    
    # 合并所有面片
    combined = cmds.polyUnite(patches, mergeUVSets=1, name="combined_patches")[0]

    #几何变形
    shape=cmds.listRelatives(combined,c=1)[0]
    
    # 清理场景 (删除原始面片)
    cmds.delete(patches)
    
    # 获取合并后网格的面数
    face_count = cmds.polyEvaluate(combined, face=True)
    
    polyList=[]
    uvList=[]
    u,v,precise_u,precise_v=0,0,0,0
    for i in range(face_count):
        poly=combined+".f["+str(i)+"]"
        polyList.append(poly)
        cmds.polyEditUV(poly,su=0.1,sv=0.1,u=precise_u,v=precise_v)
        uvList.append([precise_u,precise_v])
        u+=1
        precise_u = u / 10.0
        if precise_u>=1:
            u,precise_u=0,0
            v+=1
            precise_v=v / 10.0




# 执行函数
create_bone_patches()







# import common
# se=cmds.ls(sl=1)
# mesh='combined_patches'
# shape=cmds.listRelatives(mesh,c=1)[0]
# for i in se:
#     drive=cmds.createNode('transform',n=i+"_drive")
#     cmds.matchTransform(drive,i)
#     cpm=cmds.createNode('closestPointOnMesh')
#     cmds.connectAttr(shape+'.outMesh',cpm+'.inMesh',f=1)
#     cmds.connectAttr(drive+'.translate',cpm+'.inPosition',f=1)
#     u=cmds.getAttr(cpm+'.parameterU')
#     v=cmds.getAttr(cpm+'.parameterV')
#     print(u,v)
#     cmds.delete(cpm)
    
#     newFolicleShape=cmds.createNode('follicle',n=i+"_fol_shape")
#     newFolicle = cmds.listRelatives(newFolicleShape, p=True)[0]
    
#     cmds.connectAttr(shape + ".inMesh", newFolicleShape + ".inputMesh")
    
#     common.parent(newFolicle,'face_fol_grp')
    
    
#     cmds.connectAttr(shape+".worldMatrix[0]", newFolicleShape + ".inputWorldMatrix")
#     cmds.connectAttr(newFolicleShape + ".outRotate", newFolicle + ".rotate")
#     cmds.connectAttr(newFolicleShape + ".outTranslate", newFolicle + ".translate")
#     cmds.setAttr(newFolicle + ".parameterU", u)
#     cmds.setAttr(newFolicle + ".parameterV", v)
#     cmds.parentConstraint(newFolicle,drive,mo=1)
#     cmds.parentConstraint(drive,i)
    
    
#     break