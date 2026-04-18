import maya.cmds as cmds
import FaceSetting
import common
import maya.mel as mel

# 常量定义
COLOR_MAP = {
    "main_ctrl": 18,
    "sub_ctrl": 17
}
AXIS_MAP = {
    "X": 0,
    "Y": 1,
    "Z": 2
}

def create_curve_system(name):
    """创建曲线系统
    Args:
        name (str): 系统名称
    Returns:
        tuple: (重建曲线, 曲面, 关节列表)
    """
    # 多边形转曲线
    poly_curve = common.polyToCurve(name)
    
    # 创建重建曲线
    rebuilt_curve = cmds.duplicate(poly_curve, n=f"{name}Crv")[0]
    rebuilt_curve = common.rebuild(rebuilt_curve, 4)
    
    # 创建临时曲线用于获取参数
    temp_curve = cmds.duplicate(poly_curve)[0]
    temp_curve = common.rebuild(temp_curve, 5)
    curve_points = common.getCrv_AllPoint(temp_curve)
    u_values = common.getU_Point(temp_curve, curve_points)
    cmds.delete(temp_curve)

    # 关节命名
    sides = ["R", "L"]
    joints = [f"{side}_{name}_joint{i}" for side in sides for i in (1,2,3,4)]
    
    # 创建follicle系统
    follicle_types = ["nofollow", "follow"]
    follicles = {}
    for ft in follicle_types:
        follicle_names = [f"{jnt}_{ft}" for jnt in joints]
        follicles[ft] = common.createFolicle(rebuilt_curve, u_values, follicle_names, follow=(ft == "follow"), grp=FaceSetting.LIP.drive_grp)

    # 创建混合颜色节点和驱动组
    for i, jnt in enumerate(joints):
        # 创建混合节点
        blend_node = cmds.shadingNode("blendColors", asUtility=True, name=f"{jnt}_bc")
        
        # 连接属性
        cmds.connectAttr(f"{follicles['nofollow'][i]}.translate", f"{blend_node}.color2")
        cmds.connectAttr(f"{follicles['follow'][i]}.translate", f"{blend_node}.color1")
        
        # 创建驱动组和关节
        drive_grp = cmds.group(em=True, name=f"{jnt}_drive")
        cmds.connectAttr(f"{blend_node}.output", f"{drive_grp}.translate")
        
        # 创建并定位关节
        new_jnt = cmds.joint(name=jnt)
        cmds.matchTransform(new_jnt, drive_grp)
        common.parent(drive_grp, FaceSetting.LIP.drive_grp)

    # 创建曲面系统
    surface_name = f"{name}Ribbon"
    surface_curve = cmds.duplicate(poly_curve)[0]
    surface_curve = common.rebuild(surface_curve, 5)
    loft_surface = common.loft(surface_name, surface_curve, 0.1)
    
    # 蒙皮绑定
    cmds.skinCluster(joints, loft_surface, bm=0, sm=0, nw=1, mi=1, tsb=True)
    
    # 整理层级
    common.parent([rebuilt_curve, loft_surface], FaceSetting.LIP.drive_grp)
    cmds.delete(poly_curve)

    return rebuilt_curve, loft_surface, joints

def setup_lip_rig(name):
    """创建完整的嘴唇绑定系统
    Args:
        name (str): 嘴唇部位名称（如：upperLip）
    """
    # 创建基础曲线系统
    curve, surface, joints = create_curve_system(name)
    
    # 获取控制关节配置
    corner_ctrls = FaceSetting.LIP.Lib_corner
    ctrl_names = [
        name+corner_ctrls[0], 
        f"R_{name}", f"M_{name}", f"L_{name}", 
        name+corner_ctrls[1]
    ]
    u_values = [0, 0.25, 0.5, 0.75, 1]
    dis=common.getCrv_Length(curve)
    # 获取曲线上的位置和旋转信息
    positions, rotations = common.getPoint_U(curve, u_values)

    sl=cmds.textScrollList("SkinJointScroll",q=1,allItems=1)
    if  sl:
        #根据要驱动的关节设置位置和方向
        slCount=len(sl)
        mid=int((slCount-1)/2)

        leftMid=[]
        rightMid=[]

        min=1
        max=mid

        if slCount==3:
            min=0
            max=mid+1

        for i in range(min,max):
            leftMid.append(sl[i])
            rightMid.append(sl[slCount-1-i])

        pointLsit=[sl[0],leftMid,sl[mid],rightMid,sl[slCount-1]]
        print(pointLsit,'1111111111')

        jntRot=[]
        jntTrs=[]  
        for i in pointLsit:
            loc=cmds.spaceLocator()
            ps=cmds.parentConstraint(i,loc,mo=0)[0]
            cmds.delete(ps)
            rot=cmds.xform(loc,q=1,ws=1,ro=1)
            trs=cmds.xform(loc,q=1,ws=1,t=1)
            jntRot.append(rot)
            jntTrs.append(trs)
            cmds.delete(loc)
        
        positions=jntTrs
        # rotations=jntRot
    
    

    
    # 创建控制关节和控制器
    for i, ctrl_name in enumerate(ctrl_names):
        # if cmds.objExists(ctrl_name):
        #     continue
        
        # 创建控制关节
        cmds.select(clear=True)
        jnt = cmds.joint(name=ctrl_name,position=positions[i],orientation=rotations[i])
        
        # 创建控制器
        ctrl, grp = create_controller(f"{ctrl_name}_ctrl", color=COLOR_MAP["main_ctrl"],radius=dis/10,width=2,offset=dis/20)
        cmds.matchTransform(grp, jnt)
        
        # 镜像处理
        if i > 2:  # 右侧控制器镜像到左侧
            cmds.matchTransform(grp,ctrl_names[len(ctrl_names)-i-1]+"_ctrl_grp")
            mirror_offset = cmds.group(name=f"{ctrl}_offset", empty=True)
            cmds.parent(grp, mirror_offset)
            cmds.setAttr(f"{mirror_offset}.scale{FaceSetting.SETTING.subAxis}", -1)
            grp=mirror_offset
        
        # 层级管理
        common.parent(grp, FaceSetting.LIP.ctrl_grp)
        cmds.parentConstraint(ctrl, jnt, maintainOffset=True)
        common.parent(jnt, FaceSetting.LIP.ctrlJoint_grp)

    # 设置皮肤权重
    skin_cluster = cmds.skinCluster(ctrl_names, curve, bm=0, sm=0, nw=1, tsb=True)[0]
    weight_map = {
        0: [(ctrl_names[0], 1)],
        1: [(ctrl_names[0], 0.4), (ctrl_names[1], 0.6)],
        2: [(ctrl_names[0], 0.2), (ctrl_names[1], 0.7), (ctrl_names[2], 0.1)],
        3: [(ctrl_names[1], 0), (ctrl_names[2], 1), (ctrl_names[3], 0)],
        4: [(ctrl_names[2], 0.1), (ctrl_names[3], 0.7), (ctrl_names[4], 0.2)],
        5: [(ctrl_names[3], 0.6), (ctrl_names[4], 0.4)],
        6: [(ctrl_names[4], 1)]
    }
    for cv_index, weights in weight_map.items():
        cmds.skinPercent(
            skin_cluster, 
            f"{curve}.cv[{cv_index}]", 
            transformValue=weights
        )

    # 添加跟随属性
    mid_ctrl = f"M_{name}_ctrl"
    common.addFloatAttr(mid_ctrl,"lipFollow",dv=1,range=(0,1))
    for jnt in joints:
        blend_node = f"{jnt}_bc"
        cmds.connectAttr(f"{mid_ctrl}.lipFollow", f"{blend_node}.blender")

    # 创建follicle驱动系统
    if not sl:
        drive=ctrl_names
    else:
        drive=sl
    follicle_u = common.getU_Point(surface, drive)
    follicles = common.createFolicle(surface, follicle_u, drive,  grp=FaceSetting.LIP.drive_fol_grp )
    
    # 轴向设置
    if FaceSetting.SETTING.upAxis == "Z":
        cmds.setAttr(f"{FaceSetting.LIP.drive_fol_grp}.rotate", 90, 0, 90)



    if not sl:
        return
    
    count=len(sl)
    for i in range(count):
        cmds.select(cl=1)
        dre=cmds.group(n=curve+sl[i]+"_drive",em=1)
        off=cmds.group(n=curve+sl[i]+"_offset")
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

        cmds.pointConstraint(follicles[i],dre,mo=1)
        cmds.orientConstraint(follicles[i],dre,mo=1)
        cmds.pointConstraint(dre,sl[i])
        cmds.orientConstraint(dre,sl[i])
    
        common.parent(FaceSetting.LIP.drive_fol_grp,FaceSetting.LIP.drive_grp)
    common.parent(FaceSetting.LIP.ctrl_grp,FaceSetting.SETTING.faceRig)
    common.parent(FaceSetting.LIP.ctrlJoint_grp,FaceSetting.SETTING.faceRig)
    common.parent(FaceSetting.LIP.drive_grp,FaceSetting.SETTING.faceRig)
    common.parent(FaceSetting.LIP.drive_joint_grp,FaceSetting.SETTING.faceRig)

    common.sets([ctrl_names[1]+"_ctrl" ,ctrl_names[2]+"_ctrl", ctrl_names[3]+"_ctrl"],name+'Sets',em=1)
    common.sets([ctrl_names[0]+"_ctrl" ,ctrl_names[4]+"_ctrl"],'ConnerSets',em=1)
    common.sets(['ConnerSets' ,name+'Sets','ConnerDriveSets',name+'DriveSets'],FaceSetting.Sets.faceSets)

def create_controller(name, color=17, radius=1.0,width=1.0,offset=0):
    """创建标准控制器
    Args:
        name (str): 控制器名称
        color (int): 颜色索引
        radius (float): 控制器半径
        offset (int): 偏移组数量
    Returns:
        tuple: (控制器, 顶层组)
    """
    # 创建圆形控制器
    ctrl = cmds.circle(
        name=name,
        radius=radius,
        normal=FaceSetting.SETTING.foreVector,
    )[0]
    
    # 创建层级组
    off=cmds.group(name=f"{name}_drive", empty=True)
    grp=cmds.group(name=f"{name}_grp", empty=True)
    cmds.parent(ctrl,off)
    cmds.parent(off,grp)
    cmds.setAttr(ctrl+".translate"+FaceSetting.SETTING.sceneFore,offset)
    cmds.makeIdentity(ctrl,t=1,a=1,n=0,pn=1)
    
    # 设置颜色
    shape = cmds.listRelatives(ctrl, shapes=True)[0]
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideColor", color)
    cmds.setAttr(f"{shape}.lineWidth",width)
    
    return ctrl, grp

# 以下函数需要根据实际项目需求进一步实现
def setup_lip_animation_controls():
    """设置嘴唇动画控制"""
    # 需要根据项目具体要求实现
    pass

def configure_driven_joints():
    """配置驱动关节"""
    # 需要根据项目具体要求实现
    pass

def sortedDriveJoint(list):
    result = common.sortedAxis(list,FaceSetting.SETTING.subAxis)
    return result