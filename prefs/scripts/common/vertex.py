import maya.cmds as cmds
import math
'''
maya坐标处理类
update: 2024.12.13
by:余杰滨
'''


#获取世界轴向信息
def getWorldAxisInfo(w=0,f=0,s=0):
    axis=cmds.upAxis(q=True,axis=True).upper()
    '''
    返回主,次,前轴信息
    分别为 1轴向 2maya中设置属性的索引 3向量

    '''

    #上轴信息
    if w:
        if 'Z' == axis:
            return ['Z',2,(0,0,1)]
        elif 'Y' == axis:
            return ['Y',1,(0,1,0)]
        elif 'X' == axis:
            return ['X',0,(1,0,0)]
    
    #前轴信息
    if f:
        if 'Z' == axis:
            return ['X',0,(1,0,0)]
        elif 'Y' == axis:
            return ['Z',2,(0,0,1)]
        elif 'X' == axis:
            return ['Y',1,(0,1,0)]
    
    #次轴信息
    if s:
        if 'Z' == axis:
            return ['Y',1,(0,1,0)]
        elif 'Y' == axis:
            return ['X',0,(1,0,0)]
        elif 'X' == axis:
            return ['Z',2,(0,0,1)]
    
def getAxisInfo(axis):
    if axis=='X':
        return ['X',0,(1,0,0)]
    elif axis=='Y':
        return ['Y',1,(0,1,0)]
    elif axis=='Z':
        return ['Z',2,(0,0,1)]

    

#获得对象轴方向
def getAxisDir(name):
    #默认Y轴向上
    world=cmds.group(em=1)
    sceneUp = getWorldAxisInfo(w=1)[0]
    #如果Z轴向上，设置为Y轴向上
    if 'z'in sceneUp:
        cmds.setAttr(world+".rotate",90,0,90)
    #获取对象坐标
    obj=cmds.shadingNode("transform",au=1)
    grp=cmds.group()
    cmds.matchTransform(grp,name)
    x=cmds.getAttr(obj+".translateX")
    y=cmds.getAttr(obj+".translateY")
    z=cmds.getAttr(obj+".translateZ")

    #分别在xyz上位移1单位
    axis=[]
    cmds.setAttr(obj+".translateX",x+1)
    cmds.setAttr(obj+".translateY",y+1)
    cmds.setAttr(obj+".translateZ",z+1)
    cmds.parent(obj,grp,world)

    pos1=cmds.getAttr(obj+".translate")[0]
    pos2=cmds.getAttr(grp+".translate")[0]

    #判断方向正负
    for i in range(3):
        startPos1=pos1[i] #xyz
        startPos2=pos2[i] #xyz
        
        if startPos1-startPos2>0:
            axis.append(1)
        else:
            axis.append(-1)
    cmds.delete(world)
    return(axis)

#获取两物体的距离
def distance_3d(pointA, pointB):
    posA=cmds.xform(pointA,q=1,ws=1,t=1)
    posB=cmds.xform(pointB,q=1,ws=1,t=1)
    x1, y1, z1 = posA
    x2, y2, z2 = posB
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

#获取物体坐标点
def get_point_position(name,ws=1):
    """
    获取Maya中对象的世界空间位置
    """

    if ws:
        position = cmds.xform(name, query=True, translation=True, worldSpace=True)
    else:
        position = cmds.xform(name, query=True, translation=True, objectSpace=True)
    return tuple(position)

#计算2坐标点是否相同
def points_are_same(point1, point2, tolerance=1e-3):
    """
    判断两个三维点是否在同一位置

    :param point1: 第一个点，格式为(x, y, z)
    :param point2: 第二个点，格式为(x, y, z)
    :param tolerance: 容差值，默认值为1e-6
    :return: 如果点在同一位置返回True，否则返回False
    """
    return all(math.fabs(point1[i] - point2[i]) < tolerance for i in range(3))

#按某个轴向排序
def sortedAxis(objName,axis,reverse=False):
    posList=[]
    m=getAxisInfo(axis)[1]
    for i in objName:
        pos=get_point_position(i)
        posList.append(pos[m])
    
    sorted_id=sorted(range(len(posList)),key=lambda k:posList[k],reverse=reverse)

    sorted_List=[]
    for id in sorted_id:
        sorted_List.append(objName[id]) 

    return sorted_List

def get_more_position(objList):
    """
    获取Maya中对象的世界空间位置
    """
    loc=cmds.spaceLocator()
    cmds.pointConstraint(objList,loc)
    position = cmds.xform(loc, query=True, translation=True, worldSpace=True)
    cmds.delete(loc)
    return tuple(position)