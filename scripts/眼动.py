from functools import wraps

#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        import maya.cmds as cmds
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds.undoInfo(closeChunk=True)
        return result
    return wrap


@make_undo
def script():
    import maya.cmds as cmds
    import maya.mel as mel
    import common
    



    '''
    选择顺序，左眼,只选左眼及左眼皮，右眼通过"_R”获取

                1
            3   0   4   
                2
    '''

    
    se=cmds.ls(sl=1)
    #控制器
    crv=mel.eval("curve -d 3 -p -2.894477 1.432475 0 -p -2.882324 3.600636 0 -p -2.498579 5.443428 0 -p -0.056752 4.832929 0 -p 0.967415 4.19256 0 -p 2.085666 2.924469 0 -p 2.679471 0.935019 0 -p 2.322664 -1.535556 0 -p 1.855252 -3.347987 0 -p 1.25204 -4.4462 0 -p 0.749316 -5.154372 0 -p 0.345407 -5.37035 0 -p 0.00378206 -5.103397 0 -p -1.476449 -3.665953 0 -p -2.354817 -1.137648 0 -p -2.816621 1.363739 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 13 -k 13 ;")
    crv1=cmds.closeCurve(crv,ch=1,ps=2,rpo=0,bb=0.5,bki=0,p=0.1)[0]
    cmds.delete(crv)
    crv2=cmds.circle(c=(0,0,0),nr=(0,0,1),sw=360,r=2.233,d=3,ut=0,tol=0.01,s=8,ch=1)
    shape=cmds.listRelatives(crv2,c=1,s=1)[0]
    cmds.setAttr(crv1+".overrideEnabled",1)
    cmds.setAttr(crv1+".overrideColor",13)
    cmds.setAttr(shape+".overrideEnabled",1)
    cmds.setAttr(shape+".overrideColor",17)
    cmds.parent(shape,crv1,r=1,s=1)
    cmds.delete(crv2)
    leftEye=cmds.rename(crv1,"Left_Eye_ctrl")
    common.addFloatAttr(leftEye,"wink",range=(0,1))
    common.addFloatAttr(leftEye,"upWinkValue")
    common.addFloatAttr(leftEye,"dnWinkValue")
    common.addFloatAttr(leftEye,"winkHeight",range=(0,10))
    common.addFloatAttr(leftEye,"eyeInfluence",range=(0,1))
    leftGrp=cmds.group(n=leftEye+"_grp",em=1)
    cmds.parent(leftEye,leftGrp)
    cmds.setAttr(leftGrp+".rotateY",90)
    cmds.makeIdentity(leftGrp,r=1,s=1,apply=1,n=0,pn=1)
    
    
    rightEye=cmds.duplicate(leftEye,n="Right_Eye_ctrl")[0]
    rightGrp=cmds.group(n=rightEye+"_grp",em=1)
    cmds.parent(rightEye,rightGrp)
    cmds.setAttr(rightGrp+".scaleY",-1)
    cmds.makeIdentity(rightGrp,s=1,apply=1,n=0,pn=1)
    cmds.setAttr(rightEye+".overrideEnabled",1)
    cmds.setAttr(rightEye+".overrideColor",6)
    
    
    crv=mel.eval("curve -d 1 -p 0 -6 3 -p 0 -6 -3 -p 0 6 -3 -p 0 6 3 -p 0 -6 3 -k 0 -k 1 -k 2 -k 3 -k 4 ")
    eye=cmds.rename(crv,"Eye_ctrl")
    shape=cmds.listRelatives(eye,c=1,s=1)[0]
    cmds.setAttr(shape+".overrideEnabled",1)
    cmds.setAttr(shape+".overrideColor",17)
    eyeGrp=cmds.group(n=eye+"_grp",em=1)
    cmds.parent(eye,eyeGrp)
    
    
    eyeCtrlGrp=[leftGrp,rightGrp]
    eyeCtrl=[leftEye,rightEye]
    dis=23
    scale=0.55
    locTarget=[]
    
    
    aimVector=(0 ,0 ,1) 
    upVector=(0 ,1 ,0)
    
    
    
    mirR=se[0].replace("L_","R_")
    animTarget=[]
    animTarget.append(se[0])
    animTarget.append(mirR)
    
    
    for i in range(0,2):
        target=cmds.createNode('transform',n=animTarget[i]+"_dirve")
        try:
            p=cmds.listRelatives(animTarget[i],p=1)[0]
            cmds.matchTransform(target,animTarget[i])
            cmds.parent(target,p)
            cmds.parent(animTarget[i],target)
        except:
            cmds.matchTransform(target,animTarget[i])
            cmds.parent(animTarget[i],target)
            
        
        loc=cmds.spaceLocator()[0]
        locTarget.append(loc)
        cmds.matchTransform(loc,animTarget[i])
        x=cmds.getAttr(loc+".translateX")
        cmds.setAttr(loc+".translateX",x+dis)
        ps=cmds.pointConstraint(loc,eyeCtrlGrp[i])
        cmds.setAttr(eyeCtrlGrp[i]+".scale",scale,scale,scale)
        cmds.makeIdentity(eyeCtrlGrp[i],s=1,apply=1,n=0,pn=1)
        cmds.delete(ps)
        cmds.aimConstraint(eyeCtrl[i],target,mo=1,aimVector=aimVector,upVector=upVector,worldUpType="scene",w=1)
    
    
    ps=cmds.pointConstraint(eyeCtrlGrp,eyeGrp)
    cmds.delete(ps)
    cmds.setAttr(eyeGrp+".scale",scale+0.1,scale+0.1,scale+0.1)
    cmds.makeIdentity(eyeGrp,s=1,apply=1,n=0,pn=1)
    btw=cmds.shadingNode("distanceBetween",au=1)
    cmds.connectAttr(locTarget[0]+".worldMatrix[0]",btw+".inMatrix1")
    cmds.connectAttr(locTarget[1]+".worldMatrix[0]",btw+".inMatrix2")
    sy=cmds.getAttr(btw+".distance")
    cmds.delete(locTarget)
    cmds.setAttr(eyeGrp+".scaleY",sy*(scale)/2)
    cmds.parent(eyeCtrlGrp,eye)
    
    
    #眨眼
    target=cmds.createNode('transform',n="L_Eyelid_Up_Base_rot")
    cmds.matchTransform(target,se[0])
    p=cmds.listRelatives(se[1],p=1)[0]
    pp=cmds.listRelatives(p,p=1)[0]
    cmds.parent(target,pp)
    cmds.parent(p,target)
    
    
    target=cmds.createNode('transform',n="L_Eyelid_Bot_Base_rot")
    cmds.matchTransform(target,se[0].replace("L_","R_"))
    p=cmds.listRelatives(se[2],p=1)[0]
    pp=cmds.listRelatives(p,p=1)[0]
    cmds.parent(target,pp)
    cmds.parent(p,target)
    
    
    target=cmds.createNode('transform',n="R_Eyelid_Up_Base_rot")
    cmds.matchTransform(target,se[0])
    p=cmds.listRelatives(se[1].replace("L_","R_"),p=1)[0]
    pp=cmds.listRelatives(p,p=1)[0]
    cmds.parent(target,pp)
    cmds.parent(p,target)
    
    
    target=cmds.createNode('transform',n="R_Eyelid_Bot_Base_rot")
    cmds.matchTransform(target,se[0].replace("L_","R_"))
    p=cmds.listRelatives(se[2].replace("L_","R_"),p=1)[0]
    pp=cmds.listRelatives(p,p=1)[0]
    cmds.parent(target,pp)
    cmds.parent(p,target)
    
    
    
    
    sl=["L_Eyelid_Up_Base_rot","L_Eyelid_Bot_Base_rot"]
    
    
    for i in sl:
        mir=i.replace("L_","R_")
        
        mirList=[]
        mirList.append(i)
        mirList.append(mir)
        
        for m in mirList:
            grp=cmds.group(n=m+"_drive",em=1)
            cmds.matchTransform(grp,m)
            try:
                parnet=cmds.listRelatives(m,p=1)[0]
                cmds.parent(grp,parnet)
            except:
                pass
            cmds.parent(m,grp)
            
            sr=cmds.shadingNode("setRange",au=1,n=m+"_sr")
            cmds.setAttr(sr+".oldMaxX",10)
            rem=cmds.shadingNode("remapValue",au=1,n=m+"_rem")
            md=cmds.shadingNode("multiplyDivide",au=1,n=m+"_md")
            if "L_" in m:
                ctrl=leftEye
            elif "R_" in m:
                ctrl=rightEye
            
            if "_Up_" in sr:
                cmds.connectAttr(ctrl+".upWinkValue",sr+".minX",f=1)
            elif "_Bot_" in sr:
                cmds.connectAttr(ctrl+".dnWinkValue",sr+".maxX",f=1)
                
            cmds.connectAttr(ctrl+".winkHeight",sr+".valueX",f=1)
            cmds.connectAttr(sr+".outValueX",rem+".outputMax",f=1)
            cmds.connectAttr(rem+".outValue",md+".input2X",f=1)
            cmds.connectAttr(ctrl+".wink",rem+".inputValue",f=1)
            cmds.connectAttr(ctrl+".wink",md+".input1X",f=1)
            if "_Bot_" in sr:
                bmd=cmds.shadingNode("multiplyDivide",au=1,n=m+"_botMd")
                cmds.connectAttr(md+".outputX",bmd+".input1X",f=1)
                cmds.setAttr(bmd+".input2X",-1)
                md=bmd
    
    
            cmds.connectAttr(md+".outputX",m+".rotateX",f=1)
        
    
    
    
    influenceLid=["L_Eyelid_Up_Base_rot_drive","L_Eyelid_Bot_Base_rot_drive",se[3],se[4]]
    eyeJoint="L_Eyeball"
    drive=cmds.group(n=eyeJoint+"_rotLip_drive",em=1)
    grp=cmds.group(n=eyeJoint+"_rotLip_grp")
    cmds.matchTransform(grp,eyeJoint)
    
    
    parent=cmds.listRelatives(influenceLid[0],p=1)
    cmds.parent(influenceLid,drive)
    cmds.parent(grp,parent)
    
    
    pma=cmds.shadingNode("plusMinusAverage",au=1,n=eyeJoint+"_pma")
    md=cmds.shadingNode("multiplyDivide",au=1,n=eyeJoint+"_md")
    cmds.connectAttr(eyeJoint+".rotate",pma+".input3D[0]",f=1)
    pos=cmds.getAttr(pma+".input3D[0]")
    cmds.setAttr(pma+".input3D[1].input3Dx",pos[0][0])
    cmds.setAttr(pma+".input3D[1].input3Dy",pos[0][1])
    cmds.setAttr(pma+".input3D[1].input3Dz",pos[0][2])
    cmds.setAttr(pma+".operation",2)
    
    
    cmds.connectAttr(pma+".output3D",md+".input2",f=1)
    cmds.connectAttr(md+".output",drive+".rotate",f=1)
    cmds.connectAttr(leftEye+".eyeInfluence",md+".input1X",f=1)
    cmds.connectAttr(leftEye+".eyeInfluence",md+".input1Y",f=1)
    cmds.connectAttr(leftEye+".eyeInfluence",md+".input1Z",f=1)
    
    
    influenceLid=["R_Eyelid_Up_Base_rot_drive","R_Eyelid_Bot_Base_rot_drive",se[3].replace("L_","R_"),se[4].replace("L_","R_")]
    
    
    eyeJoint="R_Eyeball"
    drive=cmds.group(n=eyeJoint+"_rotLip_drive",em=1)
    grp=cmds.group(n=eyeJoint+"_rotLip_grp")
    cmds.matchTransform(grp,eyeJoint)
    
    
    parent=cmds.listRelatives(influenceLid[0],p=1)
    cmds.parent(influenceLid,drive)
    cmds.parent(grp,parent)
    
    
    pma=cmds.shadingNode("plusMinusAverage",au=1,n=eyeJoint+"_pma")
    md=cmds.shadingNode("multiplyDivide",au=1,n=eyeJoint+"_md")
    cmds.connectAttr(eyeJoint+".rotate",pma+".input3D[0]",f=1)
    pos=cmds.getAttr(pma+".input3D[0]")
    cmds.setAttr(pma+".input3D[1].input3Dx",pos[0][0])
    cmds.setAttr(pma+".input3D[1].input3Dy",pos[0][1])
    cmds.setAttr(pma+".input3D[1].input3Dz",pos[0][2])
    cmds.setAttr(pma+".operation",2)
    
    
    cmds.connectAttr(pma+".output3D",md+".input2",f=1)
    cmds.connectAttr(md+".output",drive+".rotate",f=1)
    cmds.connectAttr(leftEye+".eyeInfluence",md+".input1X",f=1)
    cmds.connectAttr(leftEye+".eyeInfluence",md+".input1Y",f=1)
    cmds.connectAttr(leftEye+".eyeInfluence",md+".input1Z",f=1)


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

script()