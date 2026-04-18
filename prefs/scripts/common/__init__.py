import maya.cmds as cmds
from functools import wraps
from importlib import reload
from . import vertex,info,object,mayaUI,files
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
reload(vertex)
reload(info)
reload(object)
reload(mayaUI)
reload(files)
#添加浮点属性
def addFloatAttr(obj,att,key=1,lock=0,dv=0,range=("","")):
    if (range[0]!="" and range[1]!=""):
        cmds.addAttr(obj,ln=att,at="double",min=int(range[0]),max=int(range[1]),dv=dv)
    elif (range[0]=="" and range[1]!=""):
        cmds.addAttr(obj,ln=att,at="double",max=int(range[1]),dv=dv)
    elif (range[1]=="" and range[0]!=""):
        cmds.addAttr(obj,ln=att,at="double",min=int(range[0]),dv=dv)
    else:
        print(range[0])
        cmds.addAttr(obj,ln=att,at="double",dv=dv)
    
    cmds.setAttr(obj+"."+att,e=1,k=key,l=lock,cb=not key)
    
#添加提示标题属性
def addTitleAttr(obj,att):
    cmds.addAttr(obj,ln=att+"Title",nn="===============",at="enum",en=att.upper())
    cmds.setAttr(obj+"."+att+"Title",e=1,k=False,l=True,cb=True)

#添加枚举属性
def addEnumAttr(obj,ln,att,key=1,lock=0):
        print(ln)
        print(att)
        cmds.addAttr(obj,ln=ln,at="enum",en=att)
        cmds.setAttr(obj+"."+ln,e=1,k=key,l=lock,cb=not key)



#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds .undoInfo(closeChunk=True)
        return result
    return wrap


'''
对象设置相关
'''
#获取全部子集
def get_ChildList(obj,self=False,t=""):
    listRelatives=object.get_AllList([obj],1,self,t)
    return listRelatives
#通过索引获得子对象
def get_ChildList_Index(name,index,t=""):
    data=object.listRelatives_Index([name],index,c=1,t=t)
    return(data)
#获取全部父集
def get_ParentList(obj,self=False,t=""):
    listRelatives=object.get_AllList([obj],0,self,t)
    return listRelatives
#通过索引获得子对象
def get_ChildList_Index(name,index,t=""):
    data=object.listRelatives_Index([name],index,c=0,t=t)
    return(data)
#获取关系中最顶端的对象
def getTopParent(name,t=""):
    data=object.getTop_listRelatives([name],c=0,t=t)
    count=len(data)
    return(data[count-1])
#获取关系中最末端的子对象
def getLowChild(name,t=""):
    data=object.getTop_listRelatives([name],c=1,t=t)
    count=len(data)
    return(data[count-1])
#父子设置
def parent(obj,name):
    object.parent(obj,name)
#集合设置
def sets(name,setsName,em=0):
    object.sets(name,setsName,em)
#清除集合
def rmmoveSets(name):
    object.clearAllSets(name)
#获得集合元素
def getSetsItem(name):
    result=object.setsItem(name)
    return result
#添加集合元素
def addSetsItem(obj,path,em=0):
    object.addSets(obj,path,em)

def getConnectParent(obj,ty="parent"):
    resultList=[]
    typeC=ty+"Constraint"
    for i in obj:
        result=object.getConnect(i,typeC)
        resultList.append(result)
    
    return resultList
#获得类型
def nodeType(name):
    result=object.nodeType(name)
    return result

'''
坐标点相关
'''
#计算2坐标点是否相同
def points_are_same(point1, point2, tolerance=1e-3):
    yes=vertex.points_are_same(point1, point2, tolerance)
    return yes

#获取物体坐标点
def get_point_position(obj,ws=1):
    pos=vertex.get_point_position(obj,ws)
    return pos

def getAxisDir(name):
    axis=vertex.getAxisDir(name)
    return(axis)


#获取世界轴向信息
def getWorldAxisInfo(axis,m=0,v=0):
    q=m+v
    if q>=2 or not axis:
        cmds.warning("参数错误")
        return

    if axis=='up':
        info=vertex.getWorldAxisInfo(w=1)
    elif axis=='fore':
        info=vertex.getWorldAxisInfo(f=1)
    elif axis=='sub':
        info=vertex.getWorldAxisInfo(s=1)
    else:
        info=vertex.getAxisInfo(axis)
    if not m and not v:
        return info[0]
    if m:
        return info[1]
    if v:
        return info[2]
#按某个轴向排序
def sortedAxis(objList,axis,reverse=False):
    result=vertex.sortedAxis(objList,axis,reverse)
    return result
#获取2点的距离
def distance(obj1,obj2,r=-1):
    dis=vertex.distance_3d(obj1,obj2)
    if r>=0:
        dis=round(dis,0)
    return dis
#获取多个物体的中心坐标点()
def get_more_position(objList):
    pos=vertex.get_more_position(objList)
    return pos

'''
曲线曲面等相关
'''
#边到线
def polyToCurve(name,step=0):
    CrvInfo=info.Cruve()
    crv=CrvInfo.polyToCurve(name,step)
    return crv
#重建
def rebuild(obj,u,v=1,d=3):
    type=object.nodeType(obj)
    if type=="nurbsCurve":
        Cruve=info.Cruve()
        name=Cruve.rebuild(obj,u,d)
    elif type=="nurbsSurface":
        Surface=info.Surface()
        name=Surface.rebuild(obj,u,v,d)
    
    return name 
#放样
def loft(name,crv,dis,reverse=False):
    Surface=info.Surface()
    s=Surface.loft(name,crv,dis,reverse)
    return s
#创建毛囊
def createFolicle(obj,uList,nameList,follow=0,grp="",auto=True):
    type=object.nodeType(obj)

    if type=="nurbsCurve":
        Cruve=info.Cruve()
        isLeft=Cruve.curveIsLeftStart(obj)
        points=Cruve.createFolicle(obj,uList,nameList,follow,isLeft,grp)
    elif type=="nurbsSurface":
        Surface=info.Surface()
        points=Surface.createFolicle(obj,uList,nameList,grp,auto)

    return points
#通过点获取u
def getU_Point(obj,points):
    type=object.nodeType(obj)
    if type=="nurbsCurve":
        Cruve=info.Cruve()
        uList=Cruve.getU_PointOnCurve(obj,points)

    elif type=="nurbsSurface":
        Surface=info.Surface()
        uList=Surface.getU_PointOnSurface(obj,points)
    
    elif type=="mesh":
        poly=info.Poly()
        uList=poly.getU_PointOnSurface(obj,points)

    return uList

#通过u获取点
def getPoint_U(obj,uList):
    type=object.nodeType(obj)
    if type=="nurbsCurve":
        Cruve=info.Cruve()
        translate,rotate=Cruve.getPoint_UOnCruve(obj,uList)

    elif type=="nurbsSurface":
        Surface=info.Surface()
        translate,rotate=Surface.getPoint_UOnSurface(obj,uList)
    
    return translate,rotate

#获取曲线上所有的点
def getCrv_AllPoint(crv):
    Cruve=info.Cruve()
    points=Cruve.getCrvPointInfo(crv)
    return points

def getCrv_Length(crv):
    Cruve=info.Cruve()
    len=Cruve.curveLength(crv)
    return len
'''
ui等相关
'''
def setGroupBox(title="",size=16,color=(255,255,255))-> QGroupBox:
    box=mayaUI.setGroupBox(title,size,color)
                        
    return box

def imgButton(size,url,tips="")-> QPushButton:
    button = mayaUI.ImageButton(size,url,tips)

    return button

def popWidgetMenu(title="",vis=False,content=None)-> QHBoxLayout:
    layout = mayaUI.popWidgetMenu(title,vis,content)

    return layout

def hLine(px=2,color='rgb(0,0,0)')-> QFrame:
    line=mayaUI.Line(px,color)
    return line

def titleComboBox(title,combo,margins=[0,0,0,0])-> QHBoxLayout:
    menu=mayaUI.titleComboBox(title,combo,margins)
    return menu

def titleTextEdit(height,title=None,pht="",margins=[0,0,0,0],edit=True)-> QHBoxLayout:
    
    textEdit=mayaUI.titleTextEdit(height,title,pht,margins,edit)
    return textEdit

def scaled_size(size):
    return mayaUI.scaled_size(size)

def checkBox(name,checked,color=None)-> QCheckBox:
    return mayaUI.checkBox(name,checked,color)

def get_all_item_texts(obj):
    """获取QComboBox中所有选项的文本"""
    return mayaUI.get_all_item_texts(obj)

'''
文件相关
'''
def scencePath():
    path=files.ScenceInfo.scencePath
    return path