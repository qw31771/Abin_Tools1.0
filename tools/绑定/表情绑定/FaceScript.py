import maya.cmds as cmds
import FaceSetting
import common
import maya.mel as mel

def setCrv(name):
    p2Crv=common.polyToCurve(name)
    #曲线曲面的名字

    
    #创建曲线相关
    crv=name+"Crv"
    crv=cmds.duplicate(p2Crv,n=crv)[0]
    crv=common.rebuild(crv,4)

    jointName=["R_"+name+"_joint1","R_"+name+"_joint2","R_"+name+"_joint3","R_"+name+"_joint4",
               "L_"+name+"_joint4","L_"+name+"_joint3","L_"+name+"_joint2","L_"+name+"_joint1",
               ]
    nofollow= [item + "_noFollow" for item in jointName]
    follow= [item + "_follow" for item in jointName]

    tempCrv=cmds.duplicate(p2Crv)[0]
    tempCrv=common.rebuild(tempCrv,5)
    crvPoint=common.getCrv_AllPoint(tempCrv)
    uList=common.getU_Point(tempCrv,crvPoint)
    cmds.delete(tempCrv)
    NoFollowPoint=common.createFolicle(crv,uList,nofollow,0,FaceSetting.LIP.drive_grp)
    FollowPoint=common.createFolicle(crv,uList,follow,1,FaceSetting.LIP.drive_grp)
    for i in range(len(jointName)):
        cmds.select(cl=1)
        bc=cmds.shadingNode("blendColors",au=1,n=jointName[i]+"_bc")
        grp=cmds.group(n=jointName[i]+"_drive",em=1)
        cmds.connectAttr(NoFollowPoint[i]+".translate" ,bc+".color2",f=1)
        cmds.connectAttr(FollowPoint[i]+".translate" ,bc+".color1",f=1)
        cmds.connectAttr( bc+".output",grp+".translate",f=1)
        jnt=cmds.joint(n=jointName[i])
        cmds.matchTransform(jnt,grp)
        common.parent(grp,FaceSetting.LIP.drive_grp)
    
    #创建曲面相关
    surface=name+"Ribbon"
    sufCrv=cmds.duplicate(p2Crv)[0]
    sufCrv=common.rebuild(sufCrv,5)
    surface=common.loft(surface,sufCrv,0.1)
    cmds.skinCluster(jointName,surface,bm=0,sm=0,nw=1,mi=1,tsb=True)
    common.parent([crv,surface],FaceSetting.LIP.drive_grp)
    cmds.delete(p2Crv)

    return crv,surface,jointName

def setLip(name):
    crv,lipSuf,jointName=setCrv(name)
    crvName=[FaceSetting.LIP.Lib_corner[0] , "R_"+name ,"M_"+name, "L_"+name , FaceSetting.LIP.Lib_corner[1]]
    crvUlist=[0,0.25,0.5,0.75,1]
    count=len(crvUlist)
    jntTrs,jntRot=common.getPoint_U(crv,crvUlist)
    sl=cmds.textScrollList("SkinJointScroll",q=1,allItems=1)

    if not sl:
        sl=crvName
    else:
        #根据要驱动的关节设置位置和方向
        slCount=len(sl)
        mid=int((slCount-1)/2)

        leftMid=[]
        rightMid=[]

        for i in range(1,mid):
            leftMid.append(sl[i])
            rightMid.append(sl[slCount-1-i])

        pointLsit=[sl[0],leftMid,sl[mid],rightMid,sl[slCount-1]]

        jntRot=[]
        # jntTrs=[]
        for i in pointLsit:
            loc=cmds.spaceLocator()
            ps=cmds.parentConstraint(i,loc,mo=0)[0]
            cmds.delete(ps)
            rot=cmds.xform(loc,q=1,ws=1,ro=1)
            trs=cmds.xform(loc,q=1,ws=1,t=1)
            jntRot.append(rot)
            # jntTrs.append(trs)
            cmds.delete(loc)

    for i in range(len(crvName)):
        if cmds.objExists(crvName[i]):
            continue

        cmds.select(cl=1)
        p=jntTrs[i]
        o=jntRot[i]

        if i==0 or  i==(count-1):
            p=cmds.xform(crvName[i]+"_point",q=1,ws=1,t=1)
        
        cmds.joint(n=crvName[i],p=p,o=o)
        _ctrl,_grp=setCtrl(crvName[i]+"_ctrl",17,r=0.6,h=1,off=2)
        cmds.matchTransform(_grp,crvName[i])
        if i>2:
            cmds.matchTransform(_grp,crvName[count-i-1]+"_ctrl")
            _offset=cmds.group(n=_ctrl+'_offset',em=1)
            cmds.parent(_grp,_offset)
            cmds.setAttr(_offset+".scale"+FaceSetting.SETTING.subAxis,-1)
            _grp=_offset
        common.parent(_grp,FaceSetting.LIP.ctrl_grp)
        cmds.parentConstraint(_ctrl,crvName[i],mo=1)
        common.parent(crvName[i],FaceSetting.LIP.ctrlJoint_grp)

        
    skin=cmds.skinCluster(crvName,crv,bm=0,sm=0,nw=1,tsb=True)[0]
    cmds.skinPercent(skin,crv+".cv[0]",tv=[crvName[0],1])
    cmds.skinPercent(skin,crv+".cv[1]",tv=[(crvName[0],0.4),( crvName[1],0.6)])
    cmds.skinPercent(skin,crv+".cv[2]",tv=[(crvName[0],0.2 ),( crvName[1],0.7 ),( crvName[2],0.1)])
    cmds.skinPercent(skin,crv+".cv[3]",tv=[(crvName[1],0),( crvName[2],1 ),( crvName[3],0)])
    cmds.skinPercent(skin,crv+".cv[4]",tv=[(crvName[2],0.1 ),( crvName[3],0.7 ),( crvName[4],0.2)])
    cmds.skinPercent(skin,crv+".cv[5]",tv=[(crvName[3],0.6),( crvName[4],0.4 ),])
    cmds.skinPercent(skin,crv+".cv[6]",tv=[(crvName[4],1)])

    common.addFloatAttr(crvName[2]+"_ctrl","lipFollow",dv=1,range=(0,1))
    for i in range(len(jointName)):
        cmds.connectAttr(crvName[2]+"_ctrl.lipFollow",jointName[i]+"_bc.blender",f=1)


    uList=common.getU_Point(lipSuf,sl)
    folList=common.createFolicle(lipSuf,uList,sl,grp=FaceSetting.LIP.drive_fol_grp)
    if FaceSetting.SETTING.upAxis=="Z":
        cmds.setAttr(FaceSetting.LIP.drive_fol_grp+".rotate",90,0,90)
    
    if not (cmds.textScrollList(FaceSetting.SETTING.drive,q=1,allItems=1)):
        return

    count=len(sl)
    for i in range(count):
        cmds.select(cl=1)
        dre=cmds.group(n=crv+sl[i]+"_drive",em=1)
        off=cmds.group(n=crv+sl[i]+"_offset")
        common.parent(off,FaceSetting.LIP.drive_joint_grp)
        if i==0 or i ==count-1:
            common.sets(sl[i],'ConnerDriveSets')
        else:
            common.sets(sl[i],name+'DriveSets')

        #方法1：
        # cmds.matchTransform(off,sl[i])
        # pma=cmds.shadingNode("plusMinusAverage",au=1,n=dre+"_pma")
        # cmds.connectAttr(folList[i]+".translate",pma+".input3D[0]",f=1)
        # ft=cmds.getAttr(folList[i]+".translate")[0]
        # cmds.setAttr(pma+".input3D[1]",-ft[0],-ft[1],-ft[2])
        # md=cmds.shadingNode("multiplyDivide",au=1,n=dre+"_pma")
        # cmds.connectAttr(pma+".output3D",md+".input1")

        # # cmds.connectAttr(md+".outputX",dre+".translateX")
        # # cmds.connectAttr(md+".outputY",dre+".translateY")
        # cmds.connectAttr(md+".output",dre+".translate")
        # axis=common.getAxisDir(dre)
        # cmds.setAttr(md+".input2X",axis[0])
        # cmds.setAttr(md+".input2Y",axis[1])
        # cmds.setAttr(md+".input2Z",axis[2])
        # cmds.pointConstraint(dre,sl[i])
        # cmds.pointConstraint(dre,sl[i])
        # 方法2
        cmds.matchTransform(off,sl[i])
        ps=cmds.pointConstraint(sl[i],off)[0]
        cmds.delete(ps)

        cmds.pointConstraint(folList[i],dre,mo=1)
        cmds.pointConstraint(dre,sl[i])

    common.sets([crvName[1]+"_ctrl" ,crvName[2]+"_ctrl", crvName[3]+"_ctrl"],name+'Sets',em=1)
    common.sets([crvName[0]+"_ctrl" ,crvName[4]+"_ctrl"],'ConnerSets',em=1)
    common.sets(['ConnerSets' ,name+'Sets','ConnerDriveSets',name+'DriveSets'],FaceSetting.Sets.faceSets)
    common.parent(FaceSetting.LIP.drive_fol_grp,FaceSetting.LIP.drive_grp)
    common.parent(FaceSetting.LIP.ctrl_grp,FaceSetting.SETTING.faceRig)
    common.parent(FaceSetting.LIP.ctrlJoint_grp,FaceSetting.SETTING.faceRig)
    common.parent(FaceSetting.LIP.drive_grp,FaceSetting.SETTING.faceRig)
    common.parent(FaceSetting.LIP.drive_joint_grp,FaceSetting.SETTING.faceRig)

def setLipChange():
    r_conner=FaceSetting.LIP.Lib_corner[0]+"_ctrl"
    l_conner=FaceSetting.LIP.Lib_corner[1]+"_ctrl"
    fore=FaceSetting.SETTING.foreVector
    sceneFore=FaceSetting.SETTING.sceneFore

    dis=common.distance(r_conner,l_conner,0)
    pos=common.get_more_position([r_conner,l_conner])
    posStart=(pos[0]-(fore[0]*dis),pos[1]-(fore[1]*dis),pos[2]-(fore[2]*dis))
    start=cmds.joint(n=FaceSetting.LIP.drive_grp+"_rot_start",p=posStart)
    end=cmds.joint(n=FaceSetting.LIP.drive_grp+"_rot_end",p=pos)
    ik=cmds.ikHandle(sj=start,ee=end)

    
    ctrl,grp=setCtrl("lipCtrl",18,r=0.5,v=1)
    subCtrl,subGrp=setCtrl("subLipCtrl",17,r=0.4,v=1)
    cmds.parent(subGrp,ctrl)
    cmds.setAttr(ctrl+".translate"+sceneFore,1)
    cmds.makeIdentity(apply=1,t=1,r=1,s=1,n=0,pn=1)
    ps=cmds.pointConstraint(FaceSetting.LIP.m_LibCtrl,grp)[0]
    cmds.setAttr(ctrl+".scale",2,2,2)
    cmds.delete(ps)
    cmds.parent(ik[0],ctrl)


def setLipChange2():
    #创建定位点
    r_conner=FaceSetting.LIP.Lib_corner[0]+"_ctrl"
    l_conner=FaceSetting.LIP.Lib_corner[1]+"_ctrl"
    sceneFore=FaceSetting.SETTING.sceneFore
    worldUpVector=FaceSetting.SETTING.worldUpVector
    m_LibCtrl=FaceSetting.LIP.m_LibCtrl
    upAxis=FaceSetting.SETTING.upAxis
    mirAxis=FaceSetting.SETTING.subAxis
    dis=common.distance(r_conner,l_conner,0)
    _grpR=cmds.group(n="lipDriveRot_grp",em=1)
    _offR=cmds.group(n="lipDriveRot_offset")
    ps=cmds.pointConstraint(r_conner,l_conner,_offR)[0]
    cmds.delete(ps)
    fore=cmds.getAttr(_offR+".translate"+sceneFore)
    cmds.setAttr(_offR+".translate"+sceneFore,fore-dis)

    grpT=cmds.group(n="lipDriveTrs_grp",em=1)
    _offT=cmds.group(n="lipDriveTrs_offset")
    # ps=cmds.pointConstraint(m_LibCtrl,_offT)[0]
    # cmds.delete(ps)
    cmds.matchTransform(_offT,_grpR)
    common.parent(_offT,_grpR)

    child=cmds.listRelatives("lipCtrl_grp",c=1)
    # common.parent(_offR,"LipRibbon_ctrl_grp")
    # common.parent(child,grpT)

    ctrl=cmds.circle(n="lipCtrl",r=0.5,nr=worldUpVector)[0]
    _shape=cmds.listRelatives(ctrl,c=1)[0]
    cmds.setAttr(_shape+".overrideEnabled",1)
    cmds.setAttr(_shape+".overrideColor",18)
    grp=cmds.group(n=ctrl+'_grp')
    subCtrl=cmds.circle(n="subLipCtrl",r=0.4,nr=worldUpVector)[0]
    cmds.parent(subCtrl,ctrl)
    _shape=cmds.listRelatives(subCtrl,c=1)[0]
    cmds.setAttr(_shape+".overrideEnabled",1)
    cmds.setAttr(_shape+".overrideColor",17)
    cmds.setAttr(ctrl+".translate"+sceneFore,1)
    cmds.makeIdentity(apply=1,t=1,r=1,s=1,n=0,pn=1)
    ps=cmds.pointConstraint(m_LibCtrl,grp)[0]
    cmds.setAttr(ctrl+".scale",2,2,2)

    cmds.delete(ps)

    common.addFloatAttr(ctrl,"followRotDegree",dv=5)
    mdA=cmds.shadingNode("multiplyDivide",au=1,n=ctrl+"_DegreeMD_A")
    mdB=cmds.shadingNode("multiplyDivide",au=1,n=ctrl+"_DegreeMD_B")
    cmds.connectAttr(ctrl+".translateY",mdA+".input1Y")
    cmds.connectAttr(ctrl+".translateZ",mdA+".input1Z")
    cmds.connectAttr(ctrl+".followRotDegree",mdA+".input2Y")
    cmds.connectAttr(ctrl+".followRotDegree",mdB+".input1Z")
    cmds.connectAttr(mdB+".outputZ",mdA+".input2Z")
    cmds.setAttr(mdB+".input2Z",-1)
    cmds.connectAttr(mdA+".outputY",_grpR+".rotateZ")
    cmds.connectAttr(mdA+".outputZ",_grpR+".rotateY")

    cmds.connectAttr(ctrl+".translate"+sceneFore,_offT+".translate"+sceneFore)
    
    rotLoc=grpT
    driveCtrl=ctrl
    base=cmds.xform(rotLoc,q=1,ws=1,t=1)
    if upAxis=="Y":
        baseFore=(base[0],base[1],base[2]+0.1)
    else:
        baseFore=(base[0]+0.1,base[1],base[2])

    for i in child:
        cmds.select(cl=1)
        _off=cmds.joint(n=i+"_rot_offset",p=base)
        cmds.joint(n=i+"_rot_drive",p=baseFore)
        temp=common.get_ChildList(i,t="transform")
        i=temp[len(temp)-1]
        drive=cmds.xform(i,q=1,ws=1,t=1)
        rot=cmds.joint(n=i+"_rot_loc",p=drive)
        if upAxis=="Y":
            cmds.joint(_off,e=1,oj="zxy",secondaryAxisOrient="yup",ch=1,zso=1)
        else:
            cmds.joint(_off,e=1,oj="xyz",secondaryAxisOrient="zup",ch=1,zso=1)
        common.parent(_off,rotLoc)
        
        common.addFloatAttr(i,"openMounth_UD_Dergee",dv=10)
        common.addFloatAttr(i,"openMounth_LR_Dergee",dv=10)
        pma=cmds.shadingNode("plusMinusAverage",au=1,n=_off+"_pma")
        cmds.setAttr(pma+".input3D[1]",2,2,2)
        cmds.setAttr(pma+".operation",2)
        cmds.connectAttr(driveCtrl+".scale",pma+".input3D[0]")
        md=cmds.shadingNode("multiplyDivide",au=1,n=_off+"_md")
        cmds.connectAttr(pma+".output3D",md+".input1")
        cmds.connectAttr(md+".output"+upAxis,_off+".rotate"+upAxis)
        cmds.connectAttr(i+".openMounth_UD_Dergee",md+".input2"+upAxis,f=1)
        cmds.connectAttr(i+".openMounth_LR_Dergee",md+".input2"+mirAxis,f=1)
        
        if "corner" not in i:
            pma2=cmds.shadingNode("plusMinusAverage",au=1)
            cmds.connectAttr(subCtrl+".translate"+sceneFore,pma2+".input3D[0].input3D"+sceneFore.lower())
            f=cmds.getAttr(rot+".translate"+sceneFore)
            cmds.setAttr(pma2+".input3D[1].input3D"+sceneFore.lower(),f)
            cmds.connectAttr(pma2+".output3D"+sceneFore.lower(),rot+'.translate'+sceneFore)
        else:
            pma2=cmds.shadingNode("plusMinusAverage",au=1)
            md2=cmds.shadingNode("multiplyDivide",au=1)
            cmds.connectAttr(subCtrl+".translate"+sceneFore,md2+".input1"+sceneFore)
            cmds.setAttr(md2+".input2"+sceneFore,0.5)
            cmds.connectAttr(md2+".output"+sceneFore,pma2+".input3D[0].input3D"+sceneFore.lower())
            f=cmds.getAttr(rot+".translate"+sceneFore)
            cmds.setAttr(pma2+".input3D[1].input3D"+sceneFore.lower(),f)
            md2=cmds.shadingNode("multiplyDivide",au=1)
            cmds.connectAttr(pma2+".output3D"+sceneFore.lower(),rot+'.translate'+sceneFore)
    

        if "M_" not in i:
            cmds.connectAttr(md+".output"+mirAxis,_off+".rotate"+mirAxis)

        if "up" in i:
            cmds.setAttr(i+".openMounth_LR_Dergee",5)

        if "up"or "low" in i:
            cmds.setAttr(i+".openMounth_UD_Dergee",5)
        
        if "corner" in i:
            cmds.setAttr(i+".openMounth_LR_Dergee",5)
            cmds.setAttr(i+".openMounth_UD_Dergee",5)

        
        if "R_" in i:
            cmds.setAttr(i+".openMounth_LR_Dergee",-cmds.getAttr(i+".openMounth_LR_Dergee"))
        
        if "low" in i:
            cmds.setAttr(i+".openMounth_UD_Dergee",-cmds.getAttr(i+".openMounth_UD_Dergee"))
        
        
        grp=cmds.group(n=i+"_scaleDrive",em=1)
        cmds.matchTransform(grp,i)
        p=cmds.listRelatives(i,p=1)
        cmds.parent(grp,p)
        cmds.parent(i,grp)
        cmds.pointConstraint(rot,grp,mo=1)

    skinJnt=cmds.textScrollList("SkinJointScroll",q=1,allItems=1)
    for i in skinJnt:
        if "Corner" in i:
            continue

        md=cmds.shadingNode("multiplyDivide",au=1,n=i+"_Lip_md")
        cmds.connectAttr(subCtrl+".translate"+sceneFore,md+".input1"+sceneFore)
        if "Corner" in i:
            cmds.setAttr(md+".input2"+sceneFore,-15)
        else:
            cmds.setAttr(md+".input2"+sceneFore,-30)

        try:
            cmds.connectAttr(md+".output"+sceneFore,i+".rotate"+sceneFore)
        except:
            pass

        if "R_" in i:
            cmds.setAttr(md+".input2"+sceneFore,-cmds.getAttr(md+".input2"+sceneFore))
    
def sortedDriveJoint(list):
    result = common.sortedAxis(list,FaceSetting.SETTING.subAxis)
    return result

def setCtrl(name,color=-1,r=1,v=0,h=0,off=0):
    if h+v>2 or h+v==0:
        return
    if h:
        ctrl=cmds.circle(n=name,r=r,nr=FaceSetting.SETTING.worldUpVector)[0]
    else:
        ctrl=cmds.circle(n=name,r=r,nr=FaceSetting.SETTING.worldUpVector)[0]
        cmds.setAttr(ctrl+".rotateY",90)
        cmds.makeIdentity(ctrl,s=1,r=1,t=1,apply=1)

    grp=cmds.group(n=ctrl+'_grp')
    if color >=0:
        shape=cmds.listRelatives(ctrl,c=1)[0]

        cmds.setAttr(shape+".overrideEnabled",1)
        cmds.setAttr(shape+".overrideColor",color)

    return ctrl,grp
    


