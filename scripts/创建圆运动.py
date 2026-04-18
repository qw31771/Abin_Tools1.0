from functools import wraps
import maya.cmds as cmds

# 装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds.undoInfo(closeChunk=True)
        return result
    return wrap


@make_undo
def script():
    import maya.cmds as cmds
    import math
    import numpy as np
    import common

    def fit_3d_circle(points):
        """通过最小二乘法拟合三维空间中的最佳圆"""
        # 转换为numpy数组
        points = np.array(points)
        
        # 步骤1：计算最佳拟合平面
        centroid = np.mean(points, axis=0)
        shifted = points - centroid
        U, S, Vt = np.linalg.svd(shifted)
        normal = Vt[2]  # 第三个奇异向量对应法线
        
        # 步骤2：投影到平面
        basis_u = Vt[0]
        basis_v = np.cross(normal, basis_u)
        proj_points = np.dot(shifted, np.array([basis_u, basis_v]).T)
        
        # 步骤3：二维圆拟合（最小二乘法）
        x = proj_points[:,0]
        y = proj_points[:,1]
        A = np.vstack([x, y, np.ones(len(x))]).T
        b = x**2 + y**2
        c = np.linalg.lstsq(A, b, rcond=None)[0]
        
        # 解析圆心和半径
        xc = c[0]/2
        yc = c[1]/2
        radius = np.sqrt(c[2] + xc**2 + yc**2)
        
        # 转换回三维坐标
        center_3d = centroid + xc*basis_u + yc*basis_v
        
        return {
            "center": center_3d,
            "radius": radius,
            "normal": normal,
            "basis": (basis_u, basis_v),
            "projected": proj_points,
            "error": np.mean(np.abs(np.sqrt((x-xc)**2 + (y-yc)**2) - radius))
        }

    def create_adaptive_circle():
        selected = cmds.ls(orderedSelection=True, flatten=True)
        
        if len(selected) < 3:
            cmds.warning("至少需要选择3个点！")
            return
        
        # 获取所有点坐标
        points = [np.array(cmds.xform(p, q=True, ws=True, t=True)) for p in selected]
        
        # 自动拟合圆
        result = fit_3d_circle(points)
        
        # 错误处理
        if result["error"] > 0.1:  # 误差阈值
            cmds.warning(f"拟合误差较大 ({result['error']:.3f})，建议检查点分布")
        
        # 创建圆形
        circle_shape = cmds.circle(
            # normal=result["normal"].tolist(),
            radius=result["radius"],
            center=result["center"].tolist(),
            sections=50,
            constructionHistory=True,
            n="circle_normal"
        )[0]

        common.rebuild(circle_shape,u=50)
        
        polyPoint=[]
        for i in (selected[0:3]):
            pos=cmds.xform(i,ws=1,q=1,t=1)
            polyPoint.append(pos)
        poly=cmds.polyCreateFacet(p=polyPoint)
        tempLoc=cmds.spaceLocator()[0]  
        up=common.getWorldAxisInfo("up",v=1)
        cmds.normalConstraint(poly,tempLoc,w=1,aimVector=(-1*up[0],-1*up[1],-1*up[2]),upVector=up)
        
        # 列出所有CV组件
        cvs = cmds.ls(f"{circle_shape}.cv[*]", flatten=True)
        if not cvs:
            raise RuntimeError("无法获取CV列表，请检查NURBS圆形创建")

        positions = []
        for cv in cvs:
            pos = cmds.xform(cv, q=True, t=True, ws=True)
            positions.append(pos)

        mid_point = [
        sum(coords)/len(positions) 
        for coords in zip(*positions)
        ]

        cmds.xform(circle_shape,ws=1,piv=mid_point)

        cir_normal_rad=cmds.group(em=1,n="cir_normal_rad")
        cmds.matchTransform(cir_normal_rad,tempLoc)
        cmds.xform(cir_normal_rad,ws=1,piv=mid_point)
        cmds.parent(circle_shape,cir_normal_rad)
        cmds.setAttr(circle_shape+".rotate",0,0,0)

        
        loft_surface = common.loft("surface_circle", circle_shape, 0.1)


        #创建定位毛囊
        uList=common.getU_Point(loft_surface,selected)
        print(uList)
        nameLsit=[]
        for name in selected:
            nameLsit.append(name+"_fol")
        fols=common.createFolicle(loft_surface,uList,nameLsit,0,"",False)
        common.parent(loft_surface,"cir_normal_rad")
        common.parent(fols,"selectFol_grp")

        for i in range(len(selected)):
            cmds.parentConstraint(fols[i],selected[i],mo=1)

        setMotion(cir_normal_rad,fols,selected)
        cmds.delete(poly)
        cmds.delete(tempLoc)

        return loft_surface

    def setMotion(circle,fols,selected):
    #     selected = cmds.ls(orderedSelection=True, flatten=True)
    #     circle=create_adaptive_circle()
    #     shape=cmds.listRelatives(circle,c=1)[0]
    #     mps=cmds.listConnections(shape,d=1,t="motionPath")  
        # rad=cmds.spaceLocator(n=circle+"_Rad")[0]
        # cmds.matchTransform(rad,circle)
        # common.parent(rad,"cir_normal_rad")
    #     sorted_mps = sorted(mps, key=lambda mp: cmds.getAttr(mp + ".u"))
        
    #     uList=[]
    #     uList.append(sorted_mps[0])
    #     uList.append(sorted_mps[len(sorted_mps)-1])

    #     print(sorted_mps)

        upAxis=common.getWorldAxisInfo('up',v=1)
        for i in range(len(fols)):
            cmds.select(cl=1)
            se=selected[i]
            fol=fols[i]
            u=cmds.getAttr(fol+"Shape.parameterU")
            rp=cmds.shadingNode("remapValue",au=1)
            cmds.setAttr(rp+".inputMax",360)
            cmds.setAttr(rp+".outputMin",0)
            cmds.setAttr(rp+".outputMax",1)
            rad=cmds.spaceLocator(n=se+"_Rad")[0]
            grp=cmds.group(n=rad+"_grp")
            cmds.matchTransform(grp,circle)
            aim=cmds.aimConstraint(se,grp,aimVector=(1,0,0),upVector=upAxis,worldUpObject=se,skip='x')[0]
            cmds.delete(aim)
            cmds.connectAttr(rad+".rotateZ",rp+".inputValue")
            pm=cmds.shadingNode("plusMinusAverage",au=1)
            cmds.connectAttr(rp+".outValue",pm+".input1D[0]")
            cmds.setAttr(pm+".input1D[1]",u)
            cmds.connectAttr(pm+".output1D",fol+"Shape.parameterU")
            break


    create_adaptive_circle()

    # def _expose_to_global():
    #     import __main__  # 获取 Maya 主模块
    #     main_globals = __main__.__dict__
    #     for func in list_user_functions():
    #         main_globals[func.__name__] = func  # 注入到 Maya 全局作用域
    #         # globals()[func.__name__] = func     # 同时注入当前模块（可选）
    # def list_user_functions():
    #     functions = []
    #     import inspect
    #     for name, obj in globals().items():
    #         if inspect.isfunction(obj) and obj.__module__ == __name__:
    #             functions.append(obj)  # 改为返回函数对象而非名称
    #     return functions
    # _expose_to_global()

script()

    


