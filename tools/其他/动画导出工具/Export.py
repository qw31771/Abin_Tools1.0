# -*- coding: utf-8 -*-
import os
from maya import mel as ml
import maya.cmds as cmds
import maya.OpenMaya as om
"""
动画导出工具
"""
#sel = cmds.ls(sl = True)
class StripNamespace(object):
    @classmethod
    def as_name(cls, uuid):
        names = cmds.ls(uuid)
        if names:
            for name in names:
                if ':' not in name:
                    return name
        else:
            return None

    def __init__(self, namespace, unparent=[]):
        if cmds.namespace(exists=namespace):
            self.original_names = {}  # (UUID, name_within_namespace)
            self.parent = {}
            self.namespace = cmds.namespaceInfo(namespace, fn=True)
            if cmds.listRelatives(cmds.ls(sl =True,fl =True)[0],p =True) != None:
                self.unparent = cmds.ls(sl =True,fl =True)
            else:
                self.unparent = unparent
        else:
            raise ValueError('Could not locate supplied namespace, "{0}"'.format(namespace))




    def toMObject(self, node):
        selList = om.MSelectionList()
        selList.add(str(node))
        mObject = om.MObject()
        selList.getDependNode(0, mObject)
        return mObject

    def __enter__(self):
        if self.unparent:
            for item in self.unparent:
                selList = om.MSelectionList()
                api_obj = om.MObject()
                om.MGlobal.getSelectionListByName(item, selList)
                selList.getDependNode(0, api_obj)
                dag_parent = cmds.listRelatives(item, p=1)
                self.parent[item] = dag_parent[0]

                dag_modi = om.MDagModifier()
                dag_modi.reparentNode(api_obj)
                dag_modi.doIt()
        try:
            for absolute_name in cmds.namespaceInfo(self.namespace, listOnlyDependencyNodes=True, fullName=True):
                if cmds.objExists(absolute_name):
                    try:
                        selList = om.MSelectionList()
                        api_obj = om.MObject()
                        om.MGlobal.getSelectionListByName(absolute_name, selList)
                        selList.getDependNode(0, api_obj)
                        api_node = om.MFnDependencyNode(api_obj)


                        uuid = api_node.uuid().asString()
                        self.original_names[uuid] = api_node.name()

                        # 根据API更改命名控件
                        without_namespace = api_node.name().replace(self.namespace, '', 1)
                        api_node.setName(without_namespace)
                    except:
                        pass
        except:
            pass

        return [self.as_name(uuid) for uuid in self.original_names]

    def __exit__(self, exc_type, exc_val, exc_tb):
        for uuid, original_name in self.original_names.items():
            try:
                current_name = self.as_name(uuid)
                selList = om.MSelectionList()
                api_obj = om.MObject()
                om.MGlobal.getSelectionListByName(current_name, selList)
                selList.getDependNode(0, api_obj)
                api_node = om.MFnDependencyNode(api_obj)
                api_node.setName(original_name)
            except:
                pass

        if self.parent:
            for absolute_name, parent in self.parent.items():
                dag_modi = om.MDagModifier()
                absolute_name_mobject = self.toMObject(absolute_name)
                parent_mobject = self.toMObject(parent)
                dag_modi.reparentNode(absolute_name_mobject, parent_mobject)
                dag_modi.doIt()

class animationExport():
    def export(self,upAxis = "Y",animationOnly = False,bakeAnimation = True,ResampleAnimation = True,cameras = False,constraints = False,
               unit = "cm",includeChildren = True,intoTakes = [0,100],ExportPath = "",batch = True,ExportName = "",spilAni = True,connect = False):
        """
        FBX各种设置
        :param upAxis: 朝向
        :param animationOnly: 是否只导出动画
        :param bakeAnimation: 是否bake关键帧
        :param ResampleAnimation: 是否重采样
        :param cameras:是否导出摄像机
        :param constraints:是否导出约束
        :param unit:设置导出的系统单位
        :param includeChildren:设置是否导出选择物体的子集
        :param intoTakes:
        :return:
        """

        

        if animationOnly == True:
            cmds.FBXExportAnimationOnly("-v",True)
        else:
            cmds.FBXExportAnimationOnly("-v", False)


        axis=upAxis.lower()
        ml.eval("FBXExportUpAxis {}".format(axis))

        # if upAxis == "Y":
        #     cmds.FBXExportUpAxis("y")
        # else:
        #     cmds.FBXExportUpAxis("z")


        if bakeAnimation == True:
            cmds.FBXExportBakeComplexAnimation("-v",True)
        else:
            cmds.FBXExportBakeComplexAnimation("-v", False)

        if ResampleAnimation == True:
            cmds.FBXExportBakeResampleAnimation("-v",True)
        else:
            cmds.FBXExportBakeResampleAnimation("-v", False)

        if cameras == True:
            cmds.FBXExportCameras("-v",True)
        else:
            cmds.FBXExportCameras("-v", False)

        if constraints == True:
            cmds.FBXExportConstraints("-v",True)
        else:
            cmds.FBXExportConstraints("-v", False)

        if unit ==  "cm":
            cmds.FBXExportConvertUnitString("cm")
        elif unit == "mm":
            cmds.FBXExportConvertUnitString("mm")
        elif unit == "dm":
            cmds.FBXExportConvertUnitString("dm")
        elif unit == "m":
            cmds.FBXExportConvertUnitString("m")

        if connect == False:
            cmds.FBXExportInputConnections("-v",False)

        try:
            if includeChildren == True:
                cmds.FBXExportIncludeChildren("-v",True)
            else:
                cmds.FBXExportIncludeChildren("-v", False)
        except:
            cmds.error("版本过低，请使用2020及以上版本使用此功能")


        '''if spilAni == True:
            cmds.FBXExportSplitAnimationIntoTakes("-v","toto",intoTakes[0],intoTakes[1])
        else:
            cmds.FBXExportSplitAnimationIntoTakes("-v", "toto", intoTakes[0], intoTakes[1])'''


        if batch == True:
            self.BatchExport(ExportPath,batch,ExportName)
        else:
            self.BatchExport(ExportPath, batch, ExportName)


    def GetAnimationFilePath(self):
        if len(cmds.file(q=True, r=True, shn=True)) > 0:
            file_path = cmds.file(q=True, r=True, sn=True)[0]
        else:
            file_path = cmds.file(q = True,sn = True)
        filepath = os.path.split(file_path)
        return filepath



    def BatchExport(self,ExportPath,batch,ExportName):
        """
        :return:
        """
        isExists = os.path.exists(ExportPath+"/FBX")
        if not isExists:
            os.makedirs(ExportPath+"/FBX")

        if batch == True:
            sel = cmds.ls(sl =True)
            filepath = self.GetAnimationFilePath()
            try:
                for fileName in os.listdir(filepath[0]):
                    if fileName.split(".")[-1] == "mb" or fileName.split(".")[-1] == "ma":
                        cmds.file(filepath[0] + "/" + fileName, force=True, open=True)
                        cmds.select(sel)
                        cmds.FBXExport("-f",ExportPath+"/FBX"+"/" + fileName.split(".")[0]+".fbx","-s")
            except FileNotFoundError:
                cmds.error("未找到当前文件路径！！！！！")
        else:
            cmds.FBXExport("-f", ExportPath+"/FBX"+"/" + ExportName + ".fbx", "-s")

    def GetAnimaInto(self):
        """
        获取当前文件的开始时间以及结束时间
        :return:
        """
        stratTime = cmds.playbackOptions(q=True, min=True)  # 查询当前时间滑块
        endTime = cmds.playbackOptions(q=True, max=True)
        return str(int(stratTime)), str(int(endTime))

    def cameraData(self,selCamera, selCameraShpae):
        """
        解决导出摄像机是FOV动画不能导出的问题
        :return:
        """
        timeList = self.GetAnimaInto()
        if not cmds.objExists(selCamera + ".FieldOfView"):
            cmds.addAttr(selCamera, ln="FieldOfView", at="double", dv=10, min=2)
            cmds.setAttr(selCamera + ".FieldOfView", e=True, k=True)
            cmds.expression(s=selCamera + ".FieldOfView = `camera -q -hfv {my_price}`".format(my_price=selCameraShpae), o=selCamera, ae=1, uc="all")
            cmds.bakeResults(selCamera, sm=True, t=(timeList[0], timeList[1]), at="FieldOfView")
            cmds.selectKey(selCamera+"_FieldOfView", add=True, k=True)
            cmds.keyTangent(e=True, itt="auto", ott="auto")
        else:
            cmds.deleteAttr(selCamera + ".FieldOfView")
            cmds.addAttr(selCamera, ln="FieldOfView", at="double", dv=10, min=2)
            cmds.setAttr(selCamera + ".FieldOfView", e=True, k=True)
            cmds.expression(s=selCamera + ".FieldOfView = `camera -q -hfv {my_price}`".format(my_price=selCameraShpae),
                            o=selCamera, ae=1, uc="all")
            cmds.bakeResults(selCamera, sm=True, t=(timeList[0], timeList[1]), at="FieldOfView")
            cmds.selectKey(selCamera + "_FieldOfView", add=True, k=True)
            cmds.keyTangent( e=True, itt="auto", ott="auto")


    def createNewCamera(self,selCamera):
        """
        创建一个新的摄像机导出
        :param selCamera:
        :return: 返回新建摄像机的名字
        """
        timeList = self.GetAnimaInto()
        cam = cmds.camera()
        selCamShape = cmds.listRelatives(selCamera, s=True)
        axis=cmds.getAttr(selCamera+".rotateAxis")
        cmds.setAttr(cam[0]+".rotateAxis",axis[0][0],axis[0][1],axis[0][2])
        cos = cmds.parentConstraint(selCamera, cam[0], mo=False)
        sca = cmds.scaleConstraint(selCamera,cam[0],mo =False)
        cmds.copyKey(selCamShape[0] + ".focalLength")
        camShpes = cmds.listRelatives(cam, s=True)

        atBakeList = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY",
                      "scaleZ"]
        try:
            cmds.pasteKey(camShpes[0] + ".focalLength")
            atBakeList.append('focalLength')
        except:
            # pass
            f1=cmds.getAttr(selCamShape[0] + ".focalLength")
            cmds.setAttr(camShpes[0] + ".focalLength",f1)


        cmds.bakeResults(cam, sm=True, t=(timeList[0], timeList[1]),at="tansform")
        
        cmds.bakeResults(cam[0], sm=True, t=(timeList[0], timeList[1]), at=atBakeList)
        cmds.delete(cos)
        cmds.delete(sca)
        return cam




























