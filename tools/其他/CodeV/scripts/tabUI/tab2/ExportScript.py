# Export_ModelScript.py
import maya.cmds as cmds
import maya.mel as mel

class Export:
    def __init__(self,data):
        self.data=data

    def model(self,names,exports):
        phz=int(self.data.phz.isChecked())
        sjh=int(self.data.sjh.isChecked())
        phwl=int(self.data.phwl.isChecked())
        qxfx=int(self.data.qxfx.isChecked())
        fgfx=int(self.data.fgfx.isChecked())
        mp=int(self.data.mp.isChecked())
        yd=int(self.data.yd.isChecked())
        xzyy=int(self.data.xzyy.isChecked())
        srlj=int(self.data.srlj.isChecked())
        zdx=int(self.data.zdx.isChecked())
        zx=self.data.zx.combo.currentIndex()
        
        count=len(names)
        for i in range(count):
            name=names[i]
            if count== 1:
                export=[]
                for i in exports:
                    if isinstance(i, list):
                        export+=i
                    else:
                        export.append(i)
            else:
                export=exports[i]

            print(name,export)

        # 设置平滑组
        mel.eval(f"FBXExportSmoothingGroups -v {phz}")
        #设置三角化
        mel.eval(f"FBXExportColladaTriangulate  {sjh}")
        # 设置平滑网格
        mel.eval(f"FBXExportSmoothMesh -v {phwl}")
        #设置切线和法线
        mel.eval(f"FBXExportTangents -v  {qxfx}")
        # 设置逐顶点分割法线
        mel.eval(f"FBXExportHardEdges -v  {fgfx}")
        # 设置蒙皮
        mel.eval(f"FBXExportSkins -v  {mp}")

        # 设置融合变形
        mel.eval(f"FBXExportShapes -v {sjh}")
        # 设置约束
        mel.eval(f"FBXExportConstraints -v {sjh}")
        
        # 设置输入连接
        mel.eval(f"FBXExportInputConnections -v {srlj}")
        # 设置包含子对象
        mel.eval(f"FBXExportIncludeChildren -v {zdx}")

        # 设置轴向
        axis=(ui.Axis_box.currentText()[0]).lower()
        mel.eval("FBXExportUpAxis {}".format(axis))
        # 设置引用资源内容
        mel.eval("FBXExportReferencedAssetsContent -v true")

        
