import os
import maya.mel as mel
import maya.OpenMaya as om
import maya.cmds as cmds

#名字路径通用类
class ExportName():
    class uiName():
        iniName="maya_abin_exportWin_file.ini"
        windowGeometry="abin_export_windowGeometry"

    class SetsName():
        allSetName="exportSet"
        skeletonSetsName="skeletonSets"
        lod0SetsName="lod0Sets"
        lod1SetsName="lod1Sets"
        lod2SetsName="lod2Sets"
        lod3SetsName="lod3Sets"
        lod4SetsName="dtSets"

    class objectName():
        skeleton="Skeleton"
        
    class Path():
        script=os.path.dirname(__file__)
        ui=(script[0:script.rfind("scripts")])+"ui/ModelExpUI.ui"
        scenceFile=mel.eval("file -q -location")
        currentPath=os.path.split((scenceFile))[0]
        scencePath=currentPath[0:currentPath.rfind("/")]
        exportLodPath=scencePath+"/FBX"
        referencePath=scencePath+"/MODEL"

#自定义信息类
class ExportClass():

    class vtxMsg():
        name:str
        skincluter:str
        values:[]
        joints:[]

    class human_FKctrl_Msg:
            name:list
            value:[]
            time:[]

#自定义动画测试信息类
class ExportAnimetion():
    class human_FKctrl():

        fkMsgList=[]

        msg:ExportClass.human_FKctrl_Msg

        msg={'name':['FKScapula_R','FKScapula_L'],'value':[13,-33,-22],'time':[0,8]}
        fkMsgList.append(msg)

        msg={'name':['FKShoulder_R','FKShoulder_L'],'value':[17,-20,-30],'time':[8,15]}
        fkMsgList.append(msg)

        msg={'name':['FKElbow_R','FKElbow_L'],'value':[70,50,16],'time':[15,20]}
        fkMsgList.append(msg)

        msg={'name':['FKHip_R','FKHip_L'],'value':[17,-22,61],'time':[0,10]}
        fkMsgList.append(msg)

        msg={'name':['FKKnee_L','FKKnee_R'],'value':[0,0,-100],'time':[10,20]}
        fkMsgList.append(msg)

        msg={'name':['FKSpine3_M'],'value':[0,0,-30],'time':[20,26]}
        fkMsgList.append(msg)

        msg={'name':['FKSpine1_M'],'value':[0,0,-20],'time':[26,32]}
        fkMsgList.append(msg)

        msg={'name':['FKHead_M'],'value':[2,-20,-40],'time':[32,35]}
        fkMsgList.append(msg)

#自定义方法类
class ExportMothon():
    #命名空间剔除类
    class StripNamespace(object):
        """
        Usage:
            #方法1:将命名空间为someNamespace的对象全找出来
            with StripNamespace('someNamespace') as stripped_nodes:
                print cmds.ls(stripped_nodes)

            or
            #方法1:将命名空间为someNamespace的指定对象找出来
            with StripNamespace('someNamespace', unparent=['grp1', 'grp2']) as stripped_nodes:
                print stripped_nodes
        """

        @classmethod
        def as_name(cls, uuid):
            """
            Convenience method to extract the name from uuid

            :type uuid: basestring
            :rtype: unicode|None
            """
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

            for absolute_name in cmds.namespaceInfo(self.namespace, listOnlyDependencyNodes=True, fullName=True):
                # Ensure node was *not* auto-renamed (IE: shape nodes)
                if cmds.objExists(absolute_name):
                    # get an api handle to the node
                    try:
                        selList = om.MSelectionList()
                        api_obj = om.MObject()
                        om.MGlobal.getSelectionListByName(absolute_name, selList)
                        selList.getDependNode(0, api_obj)
                        api_node = om.MFnDependencyNode(api_obj)

                        # remember the original name to return upon exit
                        uuid = api_node.uuid().asString()
                        self.original_names[uuid] = api_node.name()
                        
                        # strip namespace by renaming via api, bypassing read-only restrictions
                        without_namespace = api_node.name().replace(self.namespace, '', 1)
                        api_node.setName(without_namespace)
                    except:
                        pass

            return [self.as_name(uuid) for uuid in self.original_names]

        def __exit__(self, exc_type, exc_val, exc_tb):
            # print(self.original_names)
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
