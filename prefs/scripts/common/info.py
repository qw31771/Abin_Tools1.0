import maya.cmds as cmds
import common
'''
maya信息获取类
update: 2024.12.13
by:余杰滨
'''

#曲线
class Cruve():
    def __init__(self):
        
        #w 主轴
        self.sceneUp = common.getWorldAxisInfo('up')
        self.crvUpAxis= common.getWorldAxisInfo('up',m=1)
        self.worldUpVector=common.getWorldAxisInfo('up',v=1)
        #f 前轴
        self.sceneFore = common.getWorldAxisInfo('fore')
        #s 次轴
        self.crvForeAxis= common.getWorldAxisInfo('sub',m=1) 

        # if self.sceneUp=='Y':
        #     self.sceneFore='Z'
        #     self.crvUpAxis= 1 
        #     self.crvForeAxis =0 X
        #     self.worldUpVector=(0,1,0)
        # elif self.sceneUp=='Z':
        #     self.sceneFore='X'
        #     self.crvUpAxis= 2 
        #     self.crvForeAxis =1 Y
        #     self.worldUpVector=(0,0,1)



    def getPoint_UOnCruve(self,name,uList):
        """
        根据u值返回位置和旋转数据

        参数:
        name 曲线的名字
        u 再曲线上的值的百分比0~1                               
        rev 是否反转

        """
        #形状节点
        Shape=cmds.listRelatives(name,c=1)[0]
        translate=[]
        rotate=[]
        for u in uList:
            mp=cmds.shadingNode("motionPath",au=1)

            cmds.setAttr(mp+".upAxis",self.crvUpAxis)
            cmds.setAttr(mp+".frontAxis",self.crvForeAxis)
            cmds.setAttr(mp+".worldUpVector",self.worldUpVector[0],self.worldUpVector[1],self.worldUpVector[2])
            cmds.setAttr(mp+".inverseFront",0)
            cmds.connectAttr(Shape+".worldSpace[0]",mp+".geometryPath",f=1)
            cmds.select(cl=1)
            cmds.setAttr(mp+".uValue",u)
            t=cmds.getAttr(mp+".allCoordinates")[0]
            translate.append(t)
            r=cmds.getAttr(mp+".rotate")[0]
            rotate.append(r)

            cmds.delete(mp)
        return translate,rotate
    
    def createFolicle(self,name, uList, folicleName="follicle",follow=1,rev=False,grp=""):
        """
        根据uv创建曲面上的毛囊

        参数:
        name 曲线的名字
        u 再曲线上的值的百分比0~1
        folicleName 毛囊名称
        rev 是否反转

        """
        #形状节点
        Shape=cmds.listRelatives(name,c=1)[0]
        count=len(uList)
        pointList=[]
        for i in range(count):
            u=uList[i]
            fol= folicleName[i] if folicleName else name+"_fol"+str(i)

            point=cmds.group(n=fol+"_drive",em=1)
            mp=cmds.shadingNode("motionPath",au=1,n=fol+"_mp")
            pma=cmds.shadingNode("plusMinusAverage",au=1,n=fol+"_pma")
            if 1-uList[i]<=0.05 or uList[i]<=0.05:
                cmds.setAttr(mp+".fractionMode",0)
            else:
                cmds.setAttr(mp+".fractionMode",follow)
            cmds.setAttr(mp+".upAxis",self.crvUpAxis)
            cmds.setAttr(mp+".frontAxis",self.crvForeAxis)
            cmds.setAttr(mp+".worldUpVector",self.worldUpVector[0],self.worldUpVector[1],self.worldUpVector[2])
            
            cmds.setAttr(mp+".inverseFront",not rev)
            cmds.setAttr(mp+".uValue",u)
            cmds.connectAttr(Shape+".worldSpace[0]",mp+".geometryPath",f=1,na=False)
            cmds.connectAttr(mp+".allCoordinates",pma+".input3D[0]",f=1)
            cmds.connectAttr(pma+".output3D",point+".translate",f=1)
            # r=cmds.getAttr(mp+".rotate")[0]
            cmds.connectAttr(mp+".rotate",point+".rotate",f=1)
            # cmds.setAttr(point+".rotate",r[0],r[1],r[2])
            pointList.append(point)

        common.parent(pointList,grp)
        return pointList

    #根据点的位置获取在曲线上的uv值
    def getU_PointOnCurve(self,name,pointList):
        #形状节点
        Shape=cmds.listRelatives(name,c=1)[0]
        uList=[]
        for point in pointList:
            np=cmds.shadingNode("nearestPointOnCurve",au=1)
            cmds.connectAttr(Shape+".worldSpace[0]",np+".inputCurve",f=1)
            locatorPosition = cmds.xform(point, t=True, q=True, ws=True)
            cmds.setAttr(np + ".inPosition", locatorPosition[0],locatorPosition[1],locatorPosition[2])
            u=cmds.getAttr(np+".result.parameter")
            uList.append(u)
            cmds.delete(np)

        return uList
    
    #重建
    def rebuild(self,name,s,d=3):
        crvTemp=cmds.rename(name,"crv_Temp")
        cmds.rebuildCurve(crvTemp,ch=1,rpo=0 ,rt=0 ,end=1 ,kr=0 ,kcp=0 ,kt=0 ,s =s ,d =d ,tol= 0.01,n=name)
        cmds.delete(crvTemp)

        return name
    #反转
    def reverse(self,name):
        crvTemp=cmds.rename(name,"crv_Temp")
        cmds.reverseCurve(crvTemp,ch=1 ,rpo=0,n=name)
        cmds.delete(crvTemp)

        return name


    #获取曲线上所有的点
    def getCrvPointInfo(self,curve_name):
        # 检查曲线是否存在
        if not cmds.objExists(curve_name):
            raise ValueError(f"Curve '{curve_name}' does not exist.")

        # 获取曲线的形状节点
        curve_shape = cmds.listRelatives(curve_name, c=True,s=1)[0]

        # 获取曲线的控制点数量
        num_cvs = cmds.getAttr(curve_shape + '.controlPoints[*]', size=True)

        # 初始化一个空列表来存储点
        points = []

        # 遍历所有控制点并获取它们的位置
        for i in range(len(num_cvs)):
            point_position=curve_shape + '.cp[' + str(i) + ']'
            points.append(point_position)

        return points
    
    def curveIsLeftStart(self,name):
        point=self.getCrvPointInfo(name)
        start=cmds.xform(point[0],q=1,ws=1,t=1)
        end=cmds.xform(point[1],q=1,ws=1,t=1)
        if self.sceneUp=="Y":
            startPos=start[0]
            endPos=end[0]
        elif self.sceneUp=="Z":
            startPos=start[1]
            endPos=end[1]

        if startPos>=0:
            if startPos-endPos>0:
                return True
            else:
                return False
        else:
            if endPos-startPos>0:
                return False
            else:
                return True

    def polyToCurve(self,name,step=0,left=0):
        try:
            #曲面的放样曲线1
            crv=cmds.polyToCurve(form=2, degree=3, conformToSmoothMeshPreview=True,n=name)[0]
        except:
            return
            
        isLeft=self.curveIsLeftStart(crv)
        if isLeft:
            self.reverse(crv)
        
        if step:
            self.rebuild(crv,step)

        return crv
    
    def curveLength(self,name):
        #形状节点
        Shape=cmds.listRelatives(name,c=1)[0]

        info=cmds.shadingNode("curveInfo",au=1)

        cmds.connectAttr(Shape+".worldSpace[0]",info+".inputCurve")

        len=cmds.getAttr(info+".arcLength")

        cmds.delete(info)

        return len




#曲面
class Surface():
    def __init__(self):
        self.sceneUp = common.getWorldAxisInfo('up')
    
    #根据点的位置获取在曲面上的uv值
    def getU_PointOnSurface(self,name,pointList):
        #形状节点
        Shape=cmds.listRelatives(name,c=1)[0]
        uList=[]
        vList=[]
        for point in pointList:
            closestPoint=cmds.shadingNode("closestPointOnSurface",au=1)
            cmds.connectAttr(Shape+".worldSpace[0]",closestPoint+".inputSurface",f=1)
            locatorPosition = cmds.xform(point, t=True, q=True, ws=True)
            cmds.setAttr(closestPoint + ".inPosition", locatorPosition[0],locatorPosition[1],locatorPosition[2])
            u=cmds.getAttr(closestPoint+".result.parameterU")
            v=cmds.getAttr(closestPoint+".result.parameterV")
            uList.append(u)
            vList.append(v)
            
            cmds.delete(closestPoint)

        return uList
    
    #根据uv创建曲面上的毛囊
    def createFolicle(self,name, uList,folicleName,grp="",auto=True):

        newFolicleList=[]
        max_value = max(uList)
        min_value = min(uList)

        for i in range(len(uList)):
            u=uList[i]
            v=0.5
            fol=folicleName[i]

            #创建毛囊shape
            newFolicleShape = cmds.createNode('follicle', n=name+"_"+fol+"_folShape")
            #获取毛囊节点
            newFolicle = cmds.listRelatives(newFolicleShape, p=True)[0]

            cmds.connectAttr(name + ".local", newFolicleShape + ".inputSurface")
            if grp:
                common.parent(newFolicle,grp)
                cmds.connectAttr(grp + ".worldInverseMatrix[0]", newFolicleShape + ".inputWorldMatrix")
            else:
                cmds.connectAttr(name + ".worldMatrix[0]", newFolicleShape + ".inputWorldMatrix")
            cmds.connectAttr(newFolicleShape + ".outRotate", newFolicle + ".rotate")
            cmds.connectAttr(newFolicleShape + ".outTranslate", newFolicle + ".translate")
            
            if  auto:
                if u==min_value:
                    u=0
                elif u==max_value:
                    u=1
            cmds.setAttr(newFolicle + ".parameterU", u)
            cmds.setAttr(newFolicle + ".parameterV", v)

            newFolicleList.append(newFolicle)

        return newFolicleList

    #根据u值返回位置和旋转数据
    def getPoint_UOnSurface(self,name,u):
        translate=[]
        rotate=[]
        fol=self.createFolicle(name,u)
        for i in fol:
            t=cmds.xform(fol,q=1,ws=1,t=1)
            r=cmds.xform(fol,q=1,ws=1,ro=1)
            translate.append(t)
            rotate.append(r)
        cmds.delete(fol)
        return translate,rotate


    #放样构建曲线
    def loft(self,name,crv,dis=0.1,reverse=False):
        if reverse:
            crv1Temp=cmds.rename(crv,"crv_Temp")
            cmds.reverseCurve(crv1Temp,ch=1 ,rpo=0,n=crv)
            cmds.delete(crv1Temp)

        crv2=cmds.duplicate(crv)[0]
        cmds.setAttr(crv+'.translate'+self.sceneUp,-dis)
        cmds.setAttr(crv2+'.translate'+self.sceneUp,dis)

        try:
            surface=cmds.loft(crv,crv2,ch=1,u=1,c=0,d=3,ss=1,po=0,rn=True,rsn=True,ar=True,n=name)[0]
        except:
            cmds.lockNode('initialShadingGroup', l=0, lockUnpublished=0)
            surface=cmds.loft(crv,crv2,ch=1,u=1,c=0,d=3,ss=1,po=0,rn=True,rsn=True,ar=True,n=name)[0]

        cmds.delete(crv)
        cmds.delete(crv2)
        return surface

    #重建曲线
    def rebuild(self,name,u,v,d=3):
        sufTemp=cmds.rename(name,"surfaceTemp")
        cmds.rebuildSurface(sufTemp,ch=1,rpo=0 ,rt=0 ,end=1 ,kr=0 ,kcp=0 ,kc=0 ,su =u ,du =d ,sv =v ,dv= 1 ,tol= 0.01 ,fr= 0 ,dir=2,n=name)
        cmds.delete(sufTemp)
        return name

#多边形
class Poly():
    def __init__(self):
        self.sceneUp = common.getWorldAxisInfo('up')

    #根据点的位置获取在曲面上的uv值
    def getU_PointOnSurface(self,name,pointList):
        #形状节点
        Shape=cmds.listRelatives(name,c=1)[0]
        uList=[]
        vList=[]
        for point in pointList:
            closestPoint=cmds.shadingNode("closestPointOnMesh",au=1)
            cmds.connectAttr(Shape+".outMesh",closestPoint+".inMesh",f=1)

            locatorPosition = cmds.xform(point, t=True, q=True, ws=True)
            cmds.setAttr(closestPoint + ".inPosition", locatorPosition[0],locatorPosition[1],locatorPosition[2])
            u=cmds.getAttr(closestPoint+".result.parameterU")
            v=cmds.getAttr(closestPoint+".result.parameterV")
            uList.append(u)
            vList.append(v)
            
            cmds.delete(closestPoint)

        return uList