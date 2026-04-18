import maya.cmds as cmds
import common
import FaceScript2
import FaceScript
import FaceSetting
from importlib import reload
reload(common)
reload(FaceScript2)
reload(FaceSetting)


def setFace_UI():
    winds = 'setFace_UI'
    if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)
    
    cmds.window(winds , t = u'表情绑定v1.0')
    cmds.formLayout( "setFace_UIForm",nd=100,w=300)

    separator01=cmds.separator(  )
    separator02=cmds.separator(  )
    separator03=cmds.separator(  )
    separator04=cmds.separator(  )
    separator05=cmds.separator(  )

    
    Lib_cornerTitle=cmds.text("Lib_cornerTitle",l="设置边角 .    .   .   .  . .  ")
    R_Lib_corner=cmds.checkBox("R_Lib_corner",l="右边角",w=55,cc="import FaceUI;FaceUI.selsectLipPoint(0,\'R_Lib_corner\')")
    R_Lib_cornerName=cmds.text("R_Lib_cornerName",l="")
    L_Lib_corner=cmds.checkBox("L_Lib_corner",l="左边角",w=55,cc="import FaceUI;FaceUI.selsectLipPoint(1,\'L_Lib_corner\')")
    L_Lib_cornerName=cmds.text("L_Lib_cornerName",l="")
    SkinJointScroll=cmds.textScrollList(FaceSetting.SETTING.drive,h=30,ams=1,dcc="import FaceUI;FaceUI.selectItem()")
    SkinJointScrollBtn=cmds.button(FaceSetting.SETTING.drive+"Btn",l="选取驱动对象",w=80,h=30,c="import FaceUI;FaceUI.showDrivejoint()",bgc=[0.55,0.34,1])

    setUpLip=cmds.button("setUpLip",l="设置上方丝带",w=90,c="import FaceUI;FaceUI.setUpLip()",bgc=[0.2,0.84,1])
    setLowLip=cmds.button("setLowLip",l="设置下方丝带",w=90,c="import FaceUI;FaceUI.setLowLip()",bgc=[0.2,0.64,1])
    setRotLip=cmds.button("setRotLip",l="设置特殊变形",w=90,c="import FaceUI;FaceUI.setLipChange()",bgc=[1,0.3,0.6])
    winInit()
    


    cmds.formLayout("setFace_UIForm",e=1,
    af=[
        (separator01, "left", 5), (separator01, "top", 10),(separator01, "right", 5),
        (separator02, "left", 5), (separator02, "top", 10),(separator02, "right", 5),
        (separator03, "left", 5), (separator03, "top", 10),(separator03, "right", 5),
        (separator04, "left", 5), (separator04, "top", 10),(separator04, "right", 5),
        (separator05, "left", 5), (separator05, "top", 10),(separator05, "right", 5),
        (Lib_cornerTitle, "left", 10),
        (L_Lib_corner, "left", 10),
        (R_Lib_corner, "left", 10),

        (SkinJointScroll, "left", 10),(SkinJointScroll, "right", 95),(SkinJointScrollBtn, "right", 10),
        (setUpLip, "left", 15),(setUpLip, "right", 15),
        (setLowLip, "left", 15),(setLowLip, "right", 15),
        (setRotLip, "left", 15),(setRotLip, "right", 15),
        
    ],
    attachControl=[
       (Lib_cornerTitle, "top", 10,separator01),
       (L_Lib_corner, "top", 10,Lib_cornerTitle),(L_Lib_cornerName, "left", 10,L_Lib_corner),(L_Lib_cornerName, "top", 12,Lib_cornerTitle),
       (R_Lib_corner, "top", 10,L_Lib_corner),(R_Lib_cornerName, "left", 10,L_Lib_corner),(R_Lib_cornerName, "top", 12,L_Lib_corner),

       (SkinJointScroll, "top", 10,R_Lib_corner),(SkinJointScrollBtn, "top", 10,R_Lib_corner),
       (setUpLip, "top", 10,SkinJointScroll),
       (setLowLip, "top", 10,setUpLip),
       (setRotLip, "top", 10,setLowLip),
       (separator02, "top", 10,setLowLip),
        
        ],
    )

    cmds.showWindow(winds)

def winInit():
    Rc="R_Lib_corner"
    if cmds.objExists(Rc+"_point"):
        cmds.checkBox(Rc,e=1,v=1)
        cmds.text(Rc+"Name",e=1,l=Rc+"_point")
    
    Lc="L_Lib_corner"
    if cmds.objExists(Lc+"_point"):
        cmds.checkBox(Lc,e=1,v=1)
        cmds.text(Lc+"Name",e=1,l=Lc+"_point")

    result=common.getSetsItem(FaceSetting.Sets.driveJoinSets)
    showDrivejoint(result,1)

def setUpLip():
    FaceScript2.setup_lip_rig(FaceSetting.LIP.LibName[0])

def setLowLip():
    FaceScript2.setup_lip_rig(FaceSetting.LIP.LibName[1])

def setLipChange():
    FaceScript.setLipChange2()

def selsectLipPoint(model,name):

    if not cmds.checkBox(name,q=1,v=1):
        cmds.text(name+"Name",e=1,l=" ")
        return
    sl=cmds.ls(sl=1)

    if len(sl)==1:
        cmds.text(name+"Name",e=1,l=name+"_point")
        poly=cmds.polySphere(r=0.1,n=name+"_point")[0]
        pos=cmds.xform(sl[0],q=1,ws=1,t=1)
        cmds.xform(poly,ws=1,t=pos)
        common.parent(poly,"lipPoint_temp")
    else:
        if "L_" in name:
            mirName=name.replace("L_","R_")
        elif "R_" in name:
            mirName=name.replace("R_","L_")

        cmds.text(name+"Name",e=1,l=name+"_point")
        cmds.text(mirName+"Name",e=1,l=mirName+"_point")
        cmds.checkBox(mirName,e=1,v=1)

        poly1=cmds.polySphere(r=0.1,n=name+"_point")[0]
        pos=cmds.xform(sl[0],q=1,ws=1,t=1)
        cmds.xform(poly1,ws=1,t=pos)
        poly2=cmds.polySphere(r=0.1,n=mirName+"_point")[0]
        pos=cmds.xform(sl[1],q=1,ws=1,t=1)
        cmds.xform(poly2,ws=1,t=pos)
        common.parent([poly1,poly2],"lipPoint_temp")

def showDrivejoint(item=[],init=0):
    if item:
       selectList=item
    else:
        if init:
            return
        selectList=cmds.ls(sl=1)
    
    if len(selectList)<=1:
        h=30
    else:
        h=len(selectList)*20

    if not selectList:
        cmds.textScrollList(FaceSetting.SETTING.drive,e=1,removeAll=1,h=h)
        return

    result=FaceScript2.sortedDriveJoint(selectList)

    cmds.textScrollList(FaceSetting.SETTING.drive,e=1,removeAll=1,append=result,h=h)
    cmds.button(FaceSetting.SETTING.drive+"Btn",e=1,h=h)
    common.sets(result,FaceSetting.Sets.driveJoinSets,em=1)
    common.sets(FaceSetting.Sets.driveJoinSets,FaceSetting.Sets.faceSets)


def selectItem():
    result = cmds.textScrollList(FaceSetting.SETTING.drive, q=True, selectItem=True)
    cmds.select(result)