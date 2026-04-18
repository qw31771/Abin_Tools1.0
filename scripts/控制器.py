from functools import wraps

#装饰器
# def make_undo(func):
#     @wraps(func)
#     def wrap(*args,**kwargs):
#         cmds.undoInfo(openChunk=True )
#         result = func(*args,**kwargs)
#         cmds.undoInfo(closeChunk=True)
#         return result
#     return wrap


# @make_undo
# def script():
import maya.cmds as cmds
import maya.mel as mel

def CreateCtrlUI():
    winds = 'CreateCtrl_UI'
    if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)
        
    cmds.window(winds , t = u'创建控制器v1.0')
    cmds.formLayout( "CreateCtrl_layout",nd=100,w=250)
    separator01=cmds.separator( style='out' )

    ctrlType=cmds.optionMenu("ctrlType",l="控制器: ")
    cmds.menuItem("cube" ,l="正方形")
    cmds.menuItem("circle",l="圆")

    # ctrlDir=cmds.optionMenu("ctrlDir",l="控制器方向: ")
    # cmds.menuItem("VH_H" ,l="水平")
    # cmds.menuItem("VH_V",l="垂直")

    ctrlColor=cmds.optionMenu("ctrlColor",l="控制器颜色: ")
    cmds.menuItem("color1" ,l="黄色")
    cmds.menuItem("colol2",l="红色")
    cmds.menuItem("colol3",l="深蓝")
    cmds.menuItem("colol4",l="浅蓝")
    cmds.menuItem("colol5",l="粉色")

    colorBtn=cmds.button("colorBtn",l="设置",w=40,h=20,c="setColor()")

    separator03=cmds.separator( style='out' )


    childBox=cmds.checkBox("childBox",l="向下延伸",cc="UIchange(\"childBox\")")

    parentBox=cmds.checkBox("parentBox",l="父子关系",cc="UIchange(\"parentBox\")")

    parentLine=cmds.optionMenu("parentLine",l="数量: ",en=0,cc="UIchange(\"parentLine\")")
    cmds.menuItem("count_1",l="全部")
    cmds.menuItem("count_2",l="2")
    cmds.menuItem("count_3",l="3")
    cmds.menuItem("count_4",l="4")
    cmds.menuItem("count_5",l="自定义")

    parentText=cmds.textField("parentText",en=0)

    separator04=cmds.separator( style='out' )

    mirBox=cmds.checkBox("mirBox",l="镜像",cc="UIchange(\"mirBox\")")
    mirColor=cmds.optionMenu("mirColor",l="颜色",en=0)
    cmds.menuItem("mirColor1" ,l="左蓝右红")
    cmds.menuItem("mirColor2",l="左红右蓝")
    mirOffset=cmds.optionMenu("mirOffset",l="偏移",en=0)
    cmds.menuItem("mirOffset1" ,l="-1")
    cmds.menuItem("mirOffset2",l="1")

    separator05=cmds.separator( style='out' )

    parentConst=cmds.checkBox("parentConst",l="父子约束  |  ",v=1)
    scaleConst=cmds.optionMenu("scaleConst",l="缩放约束: ")
    cmds.menuItem("scaleConst1" ,l="约束")
    cmds.menuItem("scaleConst2",l="连接")
    cmds.menuItem("scaleConst3" ,l="不约束")

    separator06=cmds.separator( style='out' )

    offset=cmds.text("offset",l="偏移 -----X-------Y-------Z-----")

    offsetTranslate=cmds.text("offsetTranslate",l="位移：")
    transX=cmds.textField("transX",w=50,tx=0)
    transY=cmds.textField("transY",w=50,tx=0)
    transZ=cmds.textField("transZ",w=50,tx=0)

    offsetRotate=cmds.text("offsetRotate",l="旋转：")
    rotX=cmds.textField("rotX",w=50,tx=0)
    rotY=cmds.textField("rotY",w=50,tx=0)
    rotZ=cmds.textField("rotZ",w=50,tx=0)

    offsetScale=cmds.text("offsetScale",l="缩放：")
    scaleX=cmds.textField("scaleX",w=50,tx=1)
    scaleY=cmds.textField("scaleY",w=50,tx=1)
    scaleZ=cmds.textField("scaleZ",w=50,tx=1)

    separator07=cmds.separator( style='out' )


    create=cmds.button("create",l="创建",h=40,bgc=[0.65,0.54,1],c="craeteCtrl()")
    
    cmds.formLayout("CreateCtrl_layout",e=1,
    af=[
        (separator01, "left", 5), (separator01, "top", 10),(separator01, "right", 5),
        (ctrlType, "left", 5),(ctrlType, "right", 5),
        (ctrlColor, "left", 5),(ctrlColor, "right", 70),(colorBtn, "right", 5),
        # (ctrlDir, "left", 5),(ctrlDir, "right", 5),
        (separator03, "left", 5),(separator03, "right", 5),
        (parentBox, "left", 10),(childBox, "right", 40),
        (parentText, "right", 5),(parentLine, "left", 10),
        (separator04, "left", 5),(separator04, "right", 5),
        (mirBox, "left", 5),(mirOffset, "right", 5),(mirColor, "right", 80),
        (separator05, "left", 5),(separator05, "right", 5),
        (parentConst, "left", 5),(parentConst, "right", 170),(scaleConst, "right", 5),
        (separator06, "left", 5),(separator06, "right", 5),
        (offset, "left", 5),(offset, "right", 5),
        (offsetTranslate, "left", 5),(offsetTranslate, "right", 200),
        (offsetRotate, "left", 5),(offsetRotate, "right", 200),
        (offsetScale, "left", 5),(offsetScale, "right", 200),
        (separator07, "left", 5),(separator07, "right", 5),

        (create, "left", 5),(create, "right", 5),(create, "bottom", 5),
    ],
    attachControl=[
        (ctrlType, "top", 10,separator01),
        # (ctrlDir, "top", 10,ctrlType),
        (ctrlColor, "top", 10,ctrlType),(colorBtn, "left", 10,ctrlColor),(colorBtn, "top", 10,ctrlType),
        (separator03, "top", 10,ctrlColor),
        (parentBox, "top", 10,separator03),(childBox, "top", 10,separator03),
        (parentLine, "top", 10,parentBox),
        (parentText, "top", 10,parentBox),(parentText, "left", 10,parentLine),
        (separator04, "top", 10,parentText),
        (mirBox, "top", 10,separator04),(mirColor, "left", 5,mirBox),(mirColor, "top", 10,separator04),
        (mirOffset, "top", 10,separator04),(mirOffset, "left", 5,mirColor),

        (separator05, "top", 10,mirColor),
        (parentConst, "top", 10,separator05),(scaleConst, "top", 10,separator05),(scaleConst, "left", 10,parentConst),
        (separator06, "top", 10,parentConst),
        (offset, "top", 10,separator06),
        (offsetTranslate, "top", 13,offset),
        (transX, "top", 10,offset),(transY, "top", 10,offset),(transZ, "top", 10,offset),
        (transX, "left", 10,offsetTranslate),(transY, "left", 10,transX),(transZ, "left", 10,transY),

        (offsetRotate, "top", 15,offsetTranslate),
        (rotX, "top", 10,offsetTranslate),(rotY, "top", 10,offsetTranslate),(rotZ, "top", 10,offsetTranslate),
        (rotX, "left", 10,offsetRotate),(rotY, "left", 10,rotX),(rotZ, "left", 10,rotY),

        (offsetScale, "top", 15,offsetRotate),
        (scaleX, "top", 10,offsetRotate),(scaleY, "top", 10,offsetRotate),(scaleZ, "top", 10,offsetRotate),
        (scaleX, "left", 10,offsetScale),(scaleY, "left", 10,scaleX),(scaleZ, "left", 10,scaleY),
        (separator07, "top", 15,offsetScale),
        
        (create, "top", 15,separator07),
    ],
    )

    cmds.showWindow(winds)

CreateCtrlUI()


L_mir=["L_","Left_","_L","_Left"]
R_mir=["R_","Right_","_R","_Right"]

def getColor(color):
    switcher = {
        "黄色":17,
        "红色":13,
        "深蓝":6,
        "浅蓝":18,
        "粉色":20,
        "左蓝右红":(6,13),
        "左红右蓝":(13,6),
    }
    
    return switcher.get(color, 'wrong value')

def getMirStr(arr):
    mirList=[]
    for ctrl in arr:
        isMir=False
        for i in range(0,len(L_mir)):
            l=L_mir[i]
            r=R_mir[i]
            if l in ctrl:
                mir=ctrl.replace(l,r)
                isMir=True
            elif r in ctrl:
                isMir=True
                mir=ctrl.replace(r,l)
        if isMir:
            mirList.append(mir)
    
    return mirList

def getCount(arr):
    count=len(arr)
    if cmds.optionMenu("parentLine",q=1,en=1):
        if cmds.textField("parentText",q=1,en=1):
            count=int(cmds.textField("parentText",q=1,tx=1))
        else:
            if cmds.optionMenu("parentLine",q=1,v=1)=="全部":
                count=len(arr)
            else:
                count=int(cmds.optionMenu("parentLine",q=1,v=1))
    
    return count

def craeteCtrl():
    #是否自动索取骨点
    iSAutoParent=cmds.checkBox("childBox",q=1,v=1)

    #镜像选择左边
    isMir=cmds.checkBox("mirBox",q=1,v=1)

    #形状
    shape=cmds.optionMenu("ctrlType",q=1,sl=1)

    #颜色
    color=getColor(cmds.optionMenu("ctrlColor",q=1,v=1))

    sl=cmds.ls(sl=1)


    if iSAutoParent:
            tp=cmds.nodeType(sl[0])
            temp=cmds.listRelatives(sl[0],ad=1,c=1,type=tp)
            if temp:
                temp.append(sl[0])
                temp.reverse()
                sl=temp
    
    #数量
    count=getCount(sl)

    if isMir:
        #镜像颜色
        color=getColor(cmds.optionMenu("mirColor",q=1,v=1))
        setCtrl(sl,shape,color[0],count)
        offset=int(cmds.optionMenu("mirOffset",q=1,v=1))
        setCtrl(getMirStr(sl),shape,color[1],count,offset)
    else:
        setCtrl(sl,shape,color,count)

def ctrlShape(model,color):
    if model==1:
        ctrl=mel.eval("curve -d 1 -p 1 1 1 -p 1 -1 1 -p -1 -1 1 -p -1 1 1 -p 1 1 1 -p 1 1 -1 -p -1 1 -1 -p -1 1 1 -p -1 1 -1 -p -1 -1 -1 -p -1 -1 1 -p -1 -1 -1 -p 1 -1 -1 -p 1 -1 1 -p 1 -1 -1 -p 1 1 -1 -p 1 1 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16;")
    elif model ==2:
        ctrl=cmds.circle(c=(0,0,0),nr=(1,0,0),sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1)[0]
    cmds.setAttr(ctrl+".overrideEnabled",1)
    cmds.setAttr(ctrl+".overrideColor",color)
    
    return ctrl

def setCtrl(arr,shape,color,count,offset=1):
    #是否前后为父子
    isParent=cmds.checkBox("parentBox",q=1,v=1)
    #父子约束
    parentConst=cmds.checkBox("parentConst",q=1,v=1)
    #缩放约束
    scaleConst=cmds.optionMenu("scaleConst",q=1,sl=1)
    print(scaleConst)

    last=""
    for i in range(0,count):
        obj=arr[i]
        ctrl=ctrlShape(shape,color)
        ctrl=cmds.rename(ctrl,obj+"_ctrl")
        grou=cmds.group(n=ctrl+"_grp",em=1)
        off=cmds.group(n=ctrl+"_offset",em=1)
        cmds.parent(off,grou)
        cmds.matchTransform(ctrl,obj)
        cmds.matchTransform(grou,obj)
        cmds.parent(ctrl,off)
        setCtrlShape(ctrl,offset)

        if parentConst:
            cmds.parentConstraint(ctrl,obj)
        if scaleConst == 1:
            cmds.scaleConstraint(ctrl,obj) 
        elif scaleConst == 2:
            cmds.connectAttr(ctrl+".scale",obj+".scale",f=1)
    

        if isParent:
            if last:
                
                cmds.parent(grou,last)
                
            last=ctrl

def setCtrlShape(ctrl , offset=1):
    tx=float(cmds.textField("transX",q=1,tx=1))
    ty=float(cmds.textField("transY",q=1,tx=1))
    tz=float(cmds.textField("transZ",q=1,tx=1))
    if not tx:
        tx=0
    
    if not ty:
        ty=0

    if not tz:
        tz=0

    cmds.setAttr(ctrl+".translate",tx*offset,ty*offset,tz*offset)
    

    rx=float(cmds.textField("rotX",q=1,tx=1))
    ry=float(cmds.textField("rotY",q=1,tx=1))
    rz=float(cmds.textField("rotZ",q=1,tx=1))
    if not rx:
        rx=0
    
    if not ry:
        ry=0

    if not rz:
        rz=0

    cmds.setAttr(ctrl+".rotate",rx*offset,ry*offset,rz*offset)

    sx=float(cmds.textField("scaleX",q=1,tx=1))
    sy=float(cmds.textField("scaleY",q=1,tx=1))
    sz=float(cmds.textField("scaleZ",q=1,tx=1))
    if not sx:
        sx=0
    
    if not sy:
        sy=0

    if not sz:
        sz=0

    cmds.setAttr(ctrl+".scale",sx,sy,sz)

    cmds.makeIdentity(ctrl,s=1,r=1,t=1,apply=1)
    if tx or ty or tz :
            cmds.setAttr(ctrl+".rotatePivot",0,0,0)
            cmds.setAttr(ctrl+".scalePivot",0,0,0)

def setColor():
    sl=cmds.ls(sl=1)
    color=getColor(cmds.optionMenu("ctrlColor",q=1,v=1))
    for i in sl:
        try:
            shapes=cmds.listRelatives(i,c=1,s=1)
            for s in shapes:
                cmds.setAttr(s+".overrideEnabled",1)
                cmds.setAttr(s+".overrideColor",color)
        except:
            cmds.setAttr(i+".overrideEnabled",1)
            cmds.setAttr(i+".overrideColor",color)

def UIchange(name):
    print(name)
    if name=="parentBox" or name=="childBox":
        cmds.optionMenu("parentLine",e=1,en=cmds.checkBox("parentBox",q=1,v=1) or cmds.checkBox("childBox",q=1,v=1))
    elif name=="parentLine":
        cmds.textField("parentText",e=1,en=cmds.optionMenu("parentLine",q=1,v=1)=="自定义")
    elif "mirBox":
        cmds.optionMenu("mirColor",e=1,en=not cmds.optionMenu("mirColor",q=1,en=1))
        cmds.optionMenu("mirOffset",e=1,en=not cmds.optionMenu("mirOffset",q=1,en=1))


def _expose_to_global():
    import __main__  # 获取 Maya 主模块
    main_globals = __main__.__dict__
    for func in list_user_functions():
        main_globals[func.__name__] = func  # 注入到 Maya 全局作用域
        # globals()[func.__name__] = func     # 同时注入当前模块（可选）
def list_user_functions():
    functions = []
    import inspect
    for name, obj in globals().items():
        if inspect.isfunction(obj) and obj.__module__ == __name__:
            functions.append(obj)  # 改为返回函数对象而非名称
    return functions
_expose_to_global()

# script()