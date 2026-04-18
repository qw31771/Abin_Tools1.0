import maya.cmds as cmds
'''
maya对象处理类
update: 2024.12.13
by:余杰滨
'''

#父子关系
def parent(obj,name):
    lipGrp=name
    if not cmds.objExists(lipGrp):
        lipGrp=cmds.createNode('transform',n=name)

    if isinstance(obj, list):
        for i in obj:
            if isinstance(i, list):
                for j in i:
                    p=cmds.listRelatives(j,p=1)
                    if not p :
                        cmds.parent(j,name)
                    else:
                        if p[0] not in name:
                            cmds.parent(j,name)
            else:
                p=cmds.listRelatives(i,p=1)
                if not p:
                    cmds.parent(i,name)
                else:
                    if p[0] not in name:
                        cmds.parent(i,name)
    else:
        p=cmds.listRelatives(obj,p=1)
        if not p:
            cmds.parent(obj,name)
        else:
            if p[0] not in name:
                cmds.parent(obj,name)

#获取子集
def get_AllList(data,c=True,self=False,t="",result=None):
    '''
    data:对象名称
    c:1为子, 0为父
    s:1包括自己,0不包括
    t:类型 默认全部
    result:返回结果
    Skeleton:如果第一个对象是Skeleton无视其类型
    '''
    #如果local_var是None，初始化它为一个空列表
    if result is None:
        result = []

    for i in data:
        if cmds.nodeType(i) == t  or t=="":
            if self:
                result.append(i)
            else:
                self = True

            if c:
                getLsit = cmds.listRelatives(i, c=1)
            else:
                getLsit = cmds.listRelatives(i, p=1)

            if (getLsit) != None:
                get_AllList(getLsit,c,self,t,result)
    return result

#通过索引获得子或父对象
def listRelatives_Index(name,index,c=1,t=""):
    data=get_AllList([name],c=c,t=t)
    return(data[index-1])

#获取关系中最顶端的对象
def getTop_listRelatives(name,c=0,t=""):
    data=get_AllList([name],c=c,t=t)
    count=len(data)
    return(data[count-1])

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

def nodeType(obj):
    shape=cmds.listRelatives(obj,c=1)
    if not shape:
        return cmds.nodeType(obj)
    return cmds.nodeType(shape[0])

def sets(name,sets,em=0):
    try:
        cmds.sets(sets,q=1)
    except:
        cmds.sets(name,n=sets)
    if em:
        clearAllSets(sets)

    # if not cmds.sets(name,ii=sets):
    cmds.sets(name,add=sets)

def clearAllSets(sets):
    try:
        items=cmds.sets(sets,q=1)
        for i in items:
            rmSets(i,sets)
    except:
        pass
    
def rmSets(name,sets):
    try:
        cmds.sets(sets,q=1)
    except:
        return

    tp=nodeType(name)
    if tp=="objectSet":
        cmds.delete(name)
    else:
        cmds.sets(name,rm=sets)

def setsItem(name):
    try:
        result=cmds.sets(name,q=1)
        return result
    except:
        return ""
    
def addSets(obj,path,em=0):
    paths=path.split('/')
    last=''
    for i in paths:
        try:
            cmds.sets(i,q=1)
        except:
            cmds.sets(n=i,em=1)
        if last:
            cmds.sets(i,e=1,fe=last)
        last=i
    if em:
        cmds.sets(cl=last)
    
    cmds.sets(obj,e=1,fe=last)


#获得父约束对象
def getConnect(obj,tp="parentConstraint"):
    
    # 获取对象的所有约束节点（包括父约束）
    constraint_nodes = cmds.listConnections(obj,type=tp) or []  # 如果没有约束则返回空列表
    
    if not constraint_nodes:
        cmds.warning(f"对象 {obj} 没有父约束")
        return
    else:
        sources = set()  # 使用集合避免重复
    
    # 遍历每个约束节点，获取其目标（targets）
    for constraint in constraint_nodes:
        # 获取约束的所有目标（target）对象
        targets = cmds.parentConstraint(constraint, query=True, targetList=True) or []
        sources.update(targets)
    
    if not sources:
        cmds.warning("未找到约束源对象")
        return 
    
    return (list(sources))
