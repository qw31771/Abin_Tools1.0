# -*- coding: utf-8 -*-
from operator import index
import maya.cmds as cmds
from maya import mel as ml
import winreg

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

selFBXjnt=[]
@make_undo
def bakeAnimation(bake = True,delete = True,take = [0,100],ctrl = True,pre="model",remove=1,offTime=0):
    matchTransSkeleton(pre=pre)

    # 设置 FKIK 混合属性
    attrs_to_set = [
            #通用
            "FKIKLeg_R.FKIKBlend", "FKIKLeg_L.FKIKBlend",
            "FKIKArm_L.FKIKBlend", "FKIKArm_R.FKIKBlend",
            "FKIKSpine_M.FKIKBlend",
            #四足动物
            "FKIKLegFront2_R.FKIKBlend","FKIKLegFront2_L.FKIKBlend",
            "FKIKLegBack2_R.FKIKBlend","FKIKLegBack2_L.FKIKBlend",
        ]
    


    for attr in attrs_to_set:
        if cmds.objExists(attr):
            cmds.setAttr(attr, 0)

    sourceJnts = getADVFKCtrl([],ctrl=ctrl,pre=pre)
    bakeCtrllist = []
    sourceList=[]
    cosList = []
    rotList = []
    posList = []
    disScale=[]

    twist_to_set = [
            "Hip_R.twistAmount", "Hip_L.twistAmount",
            "Shoulder_L.twistAmount", "Shoulder_R.twistAmount",
            # 'Elbow_R.twistAmount','ElbowPart1_R.twistAmount','Elbow_L.twistAmount','ElbowPart1_L.twistAmount',
            # 'Hip_R.twistAmount','Hip_L.twistAmount','HipPart1_L.twistAmount','HipPart1_R.twistAmount',
        ]
    for twist in twist_to_set:
        if cmds.objExists(twist):
            cmds.setAttr(twist, 1)
    

    for i, j in enumerate(sourceJnts):
        try:
            if j[0] != "VFX_Camera_FK_ctrl" :
                if j[0] == "FKExtraHip_L":
                    rot = cmds.orientConstraint(j[1],"FKHip_L",mo = True)
                    pos = cmds.pointConstraint(j[1], j[0], mo=True)
                    rotList.append(rot[0])
                    posList.append(pos[0])
                    bakeCtrllist.append("FKHip_L")
                    sourceList.append(j[1])
                elif j[0] == "FKExtraHip_R":
                    rot = cmds.orientConstraint(j[1], "FKHip_R", mo = True)
                    pos = cmds.pointConstraint(j[1], j[0], mo=True)
                    rotList.append(rot[0])
                    posList.append(pos[0])
                    bakeCtrllist.append("FKHip_R")
                    sourceList.append(j[1])
                elif j[0] == "FKExtraShoulder_L":
                    rot = cmds.orientConstraint(j[1], "FKShoulder_L", mo = True)
                    pos = cmds.pointConstraint(j[1], j[0], mo=True)
                    rotList.append(rot[0])
                    posList.append(pos[0])
                    bakeCtrllist.append("FKShoulder_L")
                    sourceList.append(j[1]) 
                elif j[0] == "FKExtraShoulder_R":
                    rot = cmds.orientConstraint(j[1], "FKShoulder_R",mo =  True)
                    pos = cmds.pointConstraint(j[1], j[0], mo=True)
                    rotList.append(rot[0])
                    posList.append(pos[0])
                    bakeCtrllist.append("FKShoulder_R")
                    sourceList.append(j[1])

                else:
                    cos = cmds.parentConstraint(j[1], j[0], mo=True)
                    cosList.append(cos[0])
                    # connect=['FKSpine1_M','FKSpine2_M','FKSpine3_M']
                    connect=[]
                    try:
                        if j[0] not in connect:
                            cmds.matchTransform(j[0],j[1],scl=1,pos=0,rot=0)
                            # if 'Fish' not in j[0] or 'Main' in j[0]:
                            cos2 = cmds.scaleConstraint(j[1], j[0], mo=1)
                            cosList.append(cos2[0])

                        else:
                            cmds.connectAttr(j[1]+".scale",j[0]+".scale",f=1)
                            disScale.append(j[1]+".scale")
                            disScale.append(j[0]+".scale")
                    except:
                        print(j[0])
                        pass
                    # try:
                    #     cmds.connectAttr(j[1]+".scale",j[0]+".scale",f=1)
                    #     disScale.append(j[1]+".scale")
                    #     disScale.append(j[0]+".scale")
                    # except:
                    #     print(j[0])
                    #     pass
                bakeCtrllist.append(j[0])
                sourceList.append(j[1])
                
                
        except ValueError:
            continue

        

    
    if bake == True:
        if remove:
            cmds.bakeResults(bakeCtrllist, sm=True, t=(take[0], take[1]))
            if rotList:
                cmds.delete(rotList)
            if posList:
                cmds.delete(posList)
            if cosList:
                cmds.delete(cosList)
        else:
            currentT=offTime
            targetT=int(take[0]) 
            tList=[]
            rList=[]
            sList=[]
            cmds.currentTime(targetT)
            for i in range(len(bakeCtrllist)):
                target=sourceList[i]
                ctrl=bakeCtrllist[i]
                t=cmds.getAttr(ctrl+".translate")[0]
                tList.append(t)
                r=cmds.getAttr(ctrl+".rotate")[0]
                rList.append(r)
                s=cmds.getAttr(target+".scale")[0]
                sList.append(s)
            
            if rotList:
                cmds.delete(rotList)
            if posList:
                cmds.delete(posList)
            if cosList:
                cmds.delete(cosList)

            cmds.currentTime(currentT)

            for i in range(len(bakeCtrllist)):
                t=tList[i]
                r=rList[i]
                s=sList[i]
                ctrl=bakeCtrllist[i]
                cmds.setAttr(ctrl+'.translate',t[0],t[1],t[2])
                cmds.setAttr(ctrl+'.rotate',r[0],r[1],r[2])
                try:
                    cmds.setAttr(ctrl+'.scale',s[0],s[1],s[2])
                except:
                    print("xxxx",ctrl)
            
            cmds.setKeyframe(bakeCtrllist)

        
    index=0
    for i in range(int(len(disScale)/2)):
        print("断开:"+disScale[index]+"<------------->"+disScale[index+1])
        cmds.disconnectAttr(disScale[index],disScale[index+1])
        index+=2
        
    if delete ==True:
        FilepathList = cmds.file(q=True, r=True, str=True) #获取renfence路径
        #rint(FilepathList)
        if len(FilepathList) == 2:
            Filepath = cmds.file(q=True, r=True, str=True)
            cmds.file(Filepath[1], rr=True) #删除renfence
        else:
            Filepath = cmds.file(q=True, r=True, str=True)
            cmds.file(Filepath[0], rr=True)  # 删除renfence
    try:
        if cmds.objExists("FKHead_M"):
            cmds.parentConstraint("FKHead_M","Head",mo=True)
    except:
        pass

# def getMode():
#     ModeList = cmds.ls(type="mesh")
#     modeSel = []
#     for i in ModeList:
#         if len(i.split(":")) > 1:
#             modeSel.append(i)
#     return cmds.listRelatives(modeSel, p=True)
@make_undo
def get_Align_target(obj, objs):
    matrixs = cmds.xform(obj, q=True, ws=True, m=True)
    getAttrPos = cmds.getAttr(objs + ".translate")
    getAttrRot = cmds.getAttr(objs + ".rotate")
    getAttrSca = cmds.getAttr(objs + ".scale")
    return matrixs, getAttrPos, getAttrRot, getAttrSca

# def CodeV_T_pose():
#     SourceJointList = getFbxJnt(["Root"])
#     for j in SourceJointList:
#         try:
#             tra = cmds.getAttr(j + ".translate")
#             rot = cmds.getAttr(j + ".rotate")
#             sca = cmds.getAttr(j + ".scale")
#             cmds.setAttr("model:" + j + ".translate", tra[0][0], tra[0][1], tra[0][2])
#             cmds.setAttr("model:" + j + ".rotate", rot[0][0], rot[0][1], rot[0][2])
#             cmds.setAttr("model:" + j + ".scale", sca[0][0], sca[0][1], sca[0][2])
#         except:
#             continue

    '''renameList = ["Root", "Spine1", "Spine2", "Spine3", "Spine4", "Neck", "Head"]
    for i in renameList:
        try:
            tra = cmds.getAttr(i + ".translate")
            rot = cmds.getAttr(i + ".rotate")
            sca = cmds.getAttr(i + ".scale")
            cmds.setAttr("model:" + i.split("_")[0] + ".translate", tra[0][0], tra[0][1], tra[0][2])
            cmds.setAttr("model:" + i.split("_")[0] + ".rotate", rot[0][0], rot[0][1], rot[0][2])
            cmds.setAttr("model:" + i.split("_")[0] + ".scale", sca[0][0], sca[0][1], sca[0][2])
        except:
            continue'''

def getFbxJnt(sel,pre="model"):
    '''
    获取当前选择节点的所有子集
    :param sel: 当前选择的节点
    :return: 返回所有的子集
    '''
    
    for i in sel:
        if cmds.nodeType(i) == "joint" or i == pre+":Skeleton" or i == pre+":Char:Skeleton":

            selFBXjnt.append(i)
            getchilds = cmds.listRelatives(i, c=1)
            if (getchilds) != None:
                getFbxJnt(getchilds,pre)
    return list(set(selFBXjnt))


def getADVFKCtrl(ADVFkCtrl=[],ctrl = True,pre="model"):
    global selFBXjnt
    selFBXjnt.clear()
    # selFBXjnt = []
    if ctrl == False:
        if cmds.objExists(pre+":Head"):
            HeadFBXjnt = getFbxJnt([pre+":Head"],pre)
            for i in HeadFBXjnt:
                if i != pre+":Head":
                    ctrl = i.split(":")[1] + "_FK_ctrl"
                    if not cmds.objExists(ctrl):
                        ctrl = i.split(":")[1] + "_ctrl"
                    if not cmds.objExists(ctrl):
                        lis = (i.split(":")[1], i)
                        #print(lis)
                        ADVFkCtrl.append(lis)
    # return list(set(ADVFkCtrl))
    # selFBXjnt = []     
    ske=[pre+":Skeleton"]
    if cmds.objExists(pre+":Char:Skeleton"):
        ske=[pre+":Char:Skeleton"]

    selFBXjnts = getFbxJnt(ske,pre)

    for i in selFBXjnts:
        ctrl = i.split(":")[1] + "_FK_ctrl"
        if cmds.objExists(ctrl):
            lis = (ctrl, i)
            ADVFkCtrl.append(lis)
        else:
            ctrl= i.split(":")[1] + "_ctrl"
            if cmds.objExists(ctrl):
                lis = (ctrl, i)
                ADVFkCtrl.append(lis)
            # else:
            #      ctrl= i.split(":")[1]
            #      if cmds.objExists(ctrl):
            #         lis = (ctrl, i)
            #         ADVFkCtrl.append(lis)


    
    #GE道具特殊
    geFkCtrl=[
            ("Main_root", pre + ":Skeleton"),("Main", pre + ":Root"),
            ("FKSpine1_M", pre + ":Spine_01"),
            ("FKChest_M", pre + ":Spine_02"),
            ("FKElbow_L", pre + ":L_Elbow"),("FKElbow_R", pre + ":R_Elbow"),
            ("FKShoulder_L  ", pre + ":L_Arm"),("FKShoulder_R  ", pre + ":R_Arm"),
            ("FKHip_L  ", pre + ":L_Upper_Leg"),("FKHip_R  ", pre + ":R_Upper_Leg"),
        ]
    SpineFkCtrl = [

                   ("FKExtraHip_L", pre + ":L_Hip"), ("FKKnee_L", pre + ":L_Knee"), ("FKAnkle_L", pre + ":L_Foot"),
                   ("FKToes_L", pre + ":L_Toe"), ("FKExtraHip_R", pre + ":R_Hip"), ("FKKnee_R", pre + ":R_Knee"),
                    ("FKToes_R", pre + ":R_Toe"),("FKAnkle_R", pre + ":R_Foot"),
                   ("RootX_M", pre + ":Splitter"),
                    ("FKSpine1_M", pre + ":Spine1"), 
                   ("FKSpine2_M", pre + ":Spine2"),
                   ("FKSpine3_M", pre + ":Spine3"), ("FKChest_M", pre + ":Spine4"),
                   ("FKScapula_L", pre + ":L_Clavicle"), ("FKExtraShoulder_L", pre + ":L_Shoulder"),
                   ("FKElbow_L", pre + ":L_Elbow"), ("FKWrist_L", pre + ":L_Hand"),
                   ("FKScapula_R", pre + ":R_Clavicle"), ("FKExtraShoulder_R", pre + ":R_Shoulder"),
                   ("FKWrist_R", pre + ":R_Hand"), ("FKElbow_R", pre + ":R_Elbow"), 
                   ("FKNeck_M", pre + ":Neck"),
                   ("FKNeck1_M", pre + ":Neck_Mid"),
                   ("FKHead_M", pre + ":Head"),

                    ("FKThumbFinger1_L", pre + ":L_Thumb1"),
                   ("FKThumbFinger2_L", pre + ":L_Thumb2"), ("FKThumbFinger3_L", pre + ":L_Thumb3"),
                   ("FKIndexFinger1_L", pre + ":L_Index1"), ("FKIndexFinger2_L", pre + ":L_Index2"),
                   ("FKIndexFinger3_L", pre + ":L_Index3"), ("FKMiddleFinger1_L", pre + ":L_Middle1"),
                   ("FKMiddleFinger2_L", pre + ":L_Middle2"), ("FKMiddleFinger3_L", pre + ":L_Middle3"),
                   ("FKRingFinger1_L", pre + ":L_Ring1"),
                   ("FKRingFinger2_L", pre + ":L_Ring2"), ("FKRingFinger3_L", pre + ":L_Ring3"),
                   ("FKPinkyFinger1_L", pre + ":L_Pinky1"), ("FKPinkyFinger2_L", pre + ":L_Pinky2"),
                   ("FKPinkyFinger3_L", pre + ":L_Pinky3"),
                   ("FKThumbFinger1_R", pre + ":R_Thumb1"), ("FKThumbFinger2_R", pre + ":R_Thumb2"),
                   ("FKThumbFinger3_R", pre + ":R_Thumb3"), ("FKIndexFinger1_R", pre + ":R_Index1"),
                   ("FKIndexFinger2_R", pre + ":R_Index2"),
                   ("FKIndexFinger3_R", pre + ":R_Index3"), ("FKMiddleFinger1_R", pre + ":R_Middle1"),
                   ("FKMiddleFinger2_R", pre + ":R_Middle2"), ("FKMiddleFinger3_R", pre + ":R_Middle3"),
                   ("FKRingFinger1_R", pre + ":R_Ring1"),
                   ("FKRingFinger2_R", pre + ":R_Ring2"), ("FKRingFinger3_R", pre + ":R_Ring3"),
                   ("FKPinkyFinger1_R", pre + ":R_Pinky1"), ("FKPinkyFinger2_R", pre + ":R_Pinky2"),
                   ("FKPinkyFinger3_R", pre + ":R_Pinky3"),("FKCup4_L", pre + ":L_Index0"),
                   ("FKCup3_L", pre + ":L_Middle0"),("FKCup2_L", pre + ":L_Ring0"),
                   ("FKCup1_L", pre + ":L_Pinky0"),("FKCup4_R", pre + ":R_Index0"),
                   ("FKCup3_R", pre + ":R_Middle0"),("FKCup2_R", pre + ":R_Ring0"),("Main",pre + ":Root"),
                   ("FKCup1_R", pre + ":R_Pinky0"),("IKXOffsetHip_L","FKExtraHip_L"),("IKXOffsetHip_R","FKExtraHip_R"),
                   ("IKXOffsetShoulder_L","FKExtraShoulder_L"),("IKXOffsetShoulder_R","FKExtraShoulder_R"),

                   ]
    
    HorseFkCtrl=[
        ("FKRoot_M", pre + ":Hip"),("FKChest_M", pre + ":Spine2"),

        ("FKScapula_R", pre + ":R_Scapula"),("FKShoulder_R", pre + ":R_Fore_Humerus"),
        ("FKElbow_R", pre + ":R_Fore_Radius"),("FKWrist_R", pre + ":R_Fore_Carpus"),
        ("FKFingers1_R", pre + ":R_Fore_Knee"),("FKFingers3_R", pre + ":R_Fore_Toe"),

        ("FKHip_R", pre + ":R_Back_Humerus"),("FKKnee_R", pre + ":R_Back_Radius"),
        ("FKAnkle_R", pre + ":R_Back_Carpus"),("FKToes1_R", pre + ":R_Back_Knee"),
        ("FKToes2_R", pre + ":R_Back_Toe"),

        ("FKScapula_L", pre + ":L_Scapula"),("FKShoulder_L", pre + ":L_Fore_Humerus"),
        ("FKElbow_L", pre + ":L_Fore_Radius"),("FKWrist_L", pre + ":L_Fore_Carpus"),
        ("FKFingers1_L", pre + ":L_Fore_Knee"),("FKFingers3_L", pre + ":L_Fore_Toe"),

        ("FKHip_L", pre + ":L_Back_Humerus"),("FKKnee_L", pre + ":L_Back_Radius"),
        ("FKAnkle_L", pre + ":L_Back_Carpus"),("FKToes1_L", pre + ":L_Back_Knee"),
        ("FKToes2_L", pre + ":L_Back_Toe"),
    ]

    FishFkCtrl=[
        ("Fish2:Main",pre + ":Fish2_Root"),("Fish2:FKHead_M",pre + ":Fish2_head"),
        ("Fish2:RootX_M",pre + ":Fish2_spine01"),("Fish2:FKRoot_M",pre + ":Fish2_spine01"),
        ("Fish2:FKBackA_M",pre + ":Fish2_spine02"),
        ("Fish2:FKBackB_M",pre + ":Fish2_spine03"),("Fish2:FKBackC_M",pre + ":Fish2_spine04"),
        ("Fish2:FKBackD_M",pre + ":Fish2_spine05"),("Fish2:FKBackE_M",pre + ":Fish2_spine06"),

        ("Fish2:FKBodyFinUpperA_M",pre + ":Fish2_finup01"),("Fish2:FKBodyFinUpperB_M",pre + ":Fish2_finup02"),
        ("Fish2:FKBodyFinSide1_L",pre + ":Fish2_finfront01_L"),("Fish2:FKBodyFinSide2_L",pre + ":Fish2_finfront02_L"),
        ("Fish2:FKBodyFinSide3_L",pre + ":Fish2_finfront03_L"),
        ("Fish2:FKBodyFinSide1_R",pre + ":Fish2_finfront01_R"),("Fish2:FKBodyFinSide2_R",pre + ":Fish2_finfront02_R"),
        ("Fish2:FKBodyFinSide3_R",pre + ":Fish2_finfront03_R"),
        ("Fish2:FKBodyFinLowerB1_L",pre + ":Fish2_finback01_L"),("Fish2:FKBodyFinLowerB2_L",pre + ":Fish2_finback02_L"),
        ("Fish2:FKBodyFinLowerB1_R",pre + ":Fish2_finback01_R"),("Fish2:FKBodyFinLowerB2_R",pre + ":Fish2_finback02_R"),

        ("Fish1:Main",pre + ":Fish1_Root"),("Fish1:FKHead_M",pre + ":Fish1_head"),
        ("Fish1:RootX_M",pre + ":Fish1_spine01"),("Fish1:FKRoot_M",pre + ":Fish1_spine01"),
        ("Fish1:FKBackA_M",pre + ":Fish1_spine02"),
        ("Fish1:FKBackB_M",pre + ":Fish1_spine03"),("Fish1:FKBackC_M",pre + ":Fish1_spine04"),
        ("Fish1:FKBackD_M",pre + ":Fish1_spine05"),("Fish1:FKBackE_M",pre + ":Fish1_spine06"),

        ("Fish1:FKBodyFinUpperA_M",pre + ":Fish1_finup01"),("Fish1:FKBodyFinUpperB_M",pre + ":Fish1_finup02"),
        ("Fish1:FKBodyFinSide1_L",pre + ":Fish1_finfront01_L"),("Fish1:FKBodyFinSide2_L",pre + ":Fish1_finfront02_L"),
        ("Fish1:FKBodyFinSide3_L",pre + ":Fish1_finfront03_L"),
        ("Fish1:FKBodyFinSide1_R",pre + ":Fish1_finfront01_R"),("Fish1:FKBodyFinSide2_R",pre + ":Fish1_finfront02_R"),
        ("Fish1:FKBodyFinSide3_R",pre + ":Fish1_finfront03_R"),
        ("Fish1:FKBodyFinLowerB1_L",pre + ":Fish1_finback01_L"),("Fish1:FKBodyFinLowerB2_L",pre + ":Fish1_finback02_L"),
        ("Fish1:FKBodyFinLowerB1_R",pre + ":Fish1_finback01_R"),("Fish1:FKBodyFinLowerB2_R",pre + ":Fish1_finback02_R"),
    ]

    _1017Ctrl=[
        ("Chain2_bind1_ctrl", pre + ":Chain_jnt_2"),
        ("Chain_bind1_ctrl", pre + ":Chain_jnt_2"),("Chain_bind2_ctrl", pre + ":Chain_jnt_5"),("Chain_bind3_ctrl", pre + ":Chain_jnt_8"),
        ("Chain2_bind2_ctrl", pre + ":Chain_jnt_9"),
        ("Chain2_bind3_ctrl", pre + ":Chain_jnt_12"),
        ("Chain2_bind4_ctrl", pre + ":Chain_jnt_15"),

    ]
    
    #GE道具特殊
    shapesList = cmds.ls(type="mesh")
    transformList = cmds.listRelatives(shapesList,parent=True,type="transform")
    isGe_Q=False
    isHorse=False
    isFish=False
    is1017=False
    for i in transformList:
        if "CHA_AGT_GE_AbilityQ" in i:
            print("ge技能Q道具")
            isGe_Q=True
            break
        elif "Horse" in i:
            print("马")
            isHorse=True
            break
        elif "Fish" in i:
            print("鱼")
            isFish=True
            break
        elif "MEL_1017" in i:
            print("MEL_1017")
            is1017=True
            break

    if isGe_Q:
        resetCtrl = SpineFkCtrl+ADVFkCtrl + geFkCtrl 
    else:
        resetCtrl = SpineFkCtrl+ ADVFkCtrl 

    if isHorse:
        resetCtrl=HorseFkCtrl+ADVFkCtrl

    if isFish:
        resetCtrl=ADVFkCtrl+FishFkCtrl
    
    if is1017:
        resetCtrl= _1017Ctrl+ADVFkCtrl



    return list(set(resetCtrl))


@make_undo
def GetAnimaInto():
    """
    获取当前文件的开始时间以及结束时间
    :return:
    """
    stratTime = cmds.playbackOptions(q=True, min=True)  # 查询当前时间滑块
    endTime = cmds.playbackOptions(q=True, max=True)
    return str(int(stratTime)),str(int(endTime))




#递归查找所有子集并匹配所有变换（世界坐标）
@make_undo
def matchTransSkeleton(sel=["Skeleton"],pre="model"):
    for i in sel:
        i=i.replace("Char:","")
        if i.replace("Char:","") =="Skeleton"  or cmds.nodeType(i) == "joint":
            try:
                cmds.matchTransform(pre + ":"+i,i)
            except:
                pass
            
            getchilds = cmds.listRelatives(i, c=1)
            if (getchilds) != None:
                matchTransSkeleton(getchilds,pre)




#选中控制器
@make_undo
def selectCtrl(sel="Group"):

    cmds.select(sel,hi=1)

    allList=cmds.ls(sl=1)

    ctrlList=cmds.ls(sl=1,type="nurbsCurve",s=0)
    ctrl = cmds.listRelatives(ctrlList,parent=True,type="transform")

    grp=getSpecialList(allList)

    selectList=grp+ctrl
    

    cmds.select(selectList)
    print(selectList)
    return(selectList)

@make_undo
def getSpecialList(select:list):

    specialList=["IKXOffsetShoulder_L","IKXOffsetHip_L","IKXOffsetHip_R","IKXOffsetShoulder_R","FKExtraShoulder_R","FKExtraHip_R","FKExtraHip_L","FKExtraShoulder_L"]

    grp=[]
    try:
        parent=cmds.listRelatives(select[0],p=1)[0]
        select.append(parent)
    except:
        pass
        
    for i in specialList:
        if i in select:
            grp.append(i)

    return grp

@make_undo
def bindPose(sel="Group"):
    obj=selectCtrl(sel)
    select=[]
    for i in obj:
        keys = cmds.keyframe(i, query=True)
        if keys:
            select.append(i)
            totryZero(i+".translateX",0)
            totryZero(i+".translateY",0)
            totryZero(i+".translateZ",0)
            totryZero(i+".rotateX",0)
            totryZero(i+".rotateY",0)
            totryZero(i+".rotateZ",0)
            totryZero(i+".scaleX",1)
            totryZero(i+".scaleY",1)
            totryZero(i+".scaleZ",1)

    cmds.matchTransform("FKExtraShoulder_L","Shoulder_L")
    cmds.matchTransform("IKXOffsetShoulder_L","Shoulder_L")
    cmds.matchTransform("FKExtraHip_L","Hip_L")
    cmds.matchTransform("IKXOffsetHip_L","Hip_L")
    cmds.matchTransform("IKXOffsetShoulder_R","Shoulder_R")
    cmds.matchTransform("FKExtraShoulder_R","Shoulder_R")
    cmds.matchTransform("IKXOffsetHip_R","Hip_R")
    cmds.matchTransform("FKExtraHip_R","Hip_R")


    cmds.select(select)
    
def totryZero(att,value):
    try:
        cmds.setAttr(att,value)
    except:
        pass
@make_undo
def referenceFiles(path,pre):
    suffix=path.split('.')[-1]
    print(suffix)
    if suffix=="ma":
        typ="mayaAscii"
    elif suffix=="mb":
        typ="mayaBinary"
    elif suffix=="fbx":
        typ="fbx"

    file_path = cmds.ls(type="reference")
    index=0
    if "model" in file_path:
        inde+=1
        name=pre+str(index)
    else:
        name=pre
    cmds.file(path,r=1,type=typ,namespace=name,options="v=0")
