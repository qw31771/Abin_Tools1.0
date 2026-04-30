# Export_ModelScript.py
import maya.cmds as cmds
import maya.mel as mel
import os
import AB_Maya

class Export:
    def __init__(self,data):
        self.data=data

    def model(self,names,exports,skeletons):
        self.set_MayaExport()

        path = self.data.path.toPlainText().strip()
        self.exists_path(path)

        xzyy=int(self.data.xzyy.isChecked())
        
        count = len(names)
        for i in range(count):
            name = names[i]
            
            # --- 1. 准备导出列表 (你原有的逻辑) ---
            if count == 1:
                export = []    
                for j in exports:
                    if isinstance(j, list): export += j
                    else: export.append(j)
            else:
                export = exports[i]

            if skeletons and i < len(skeletons) and skeletons[i]:
                if isinstance(export, list):
                    export.append(skeletons[i])
                else:
                    export = [export, skeletons[i]]
            cmds.select(export, r=True)
            try:
                with AB_Maya.StripNamespace(export,enabled=xzyy) as stripped_nodes:
                    se=cmds.ls(sl=1)
                    # 拼接完整路径
                    # 计算百分比并更新
                    current_progress = int((i / float(count)) * 100)
                    AB_Maya.update_progress(current_progress, f"正在导出: {name}")
                    full_path = f"{path}/{name}.fbx"
                    cmds.file(full_path, force=True, options="v=0;", type="FBX export", exportSelected=True)
                    
            except Exception as e:
                print(f"导出过程中发生错误 [{name}]: {e}")
            
        AB_Maya.update_progress(100, "所有模型导出成功!", True)
                

    def exists_path(self,path):
        path = self.data.path.toPlainText().strip()
        path = path.replace('\\', '/') # 统一斜杠格式
        
        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print(f"已创建新目录: {path}")
        except Exception as e:
            print(f"创建目录失败: {e}")

    def set_MayaExport(self):
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
        zx=self.data.zx.combo.currentText()

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
        mel.eval(f"FBXExportUpAxis {zx}")
