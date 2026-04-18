import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import re

class FollicleUVGenerator(MayaQWidgetDockableMixin,QWidget):
    def __init__(self):
        super(FollicleUVGenerator, self).__init__()
        
        self.setWindowTitle("毛囊点UV生成器")
        self.setObjectName("FollicleUVGenerator")
        self.resize(500, 700)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # 设置窗口标志，使其成为Maya的子窗口
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 让窗口悬浮在最上层
        
        self.selected_object = None
        self.object_type = None
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    def create_widgets(self):
        # 第一行：选择获取
        self.selection_label = QtWidgets.QLabel("当前选择:")
        self.selection_text = QtWidgets.QLineEdit()
        self.selection_text.setPlaceholderText("请选择曲面或曲线")
        self.selection_text.setReadOnly(True)
        self.get_selection_btn = QtWidgets.QPushButton("获取选择")
        
        # 第二行：数字输入
        self.count_label = QtWidgets.QLabel("毛囊点数量:")
        self.count_spinbox = QtWidgets.QSpinBox()
        self.count_spinbox.setRange(1, 100)
        self.count_spinbox.setValue(10)

        ## 第二行：手动
        self.selectLoc=QCheckBox('手动选择')
        self.selectLoc.setChecked(1)
        
        # 第三行：间距选项
        self.spacing_label = QtWidgets.QLabel("间距类型:")
        self.spacing_group = QtWidgets.QButtonGroup(self)
        
        self.average_radio = QtWidgets.QRadioButton("平均")
        self.increasing_radio = QtWidgets.QRadioButton("递增")
        self.decreasing_radio = QtWidgets.QRadioButton("递减")
        
        self.spacing_group.addButton(self.average_radio, 0)
        self.spacing_group.addButton(self.increasing_radio, 1)
        self.spacing_group.addButton(self.decreasing_radio, 2)
        
        self.average_radio.setChecked(True)
        
        # 程度控制 - 改为浮点数
        self.intensity_label = QtWidgets.QLabel("程度:")
        self.intensity_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(1, 100)  # 扩大范围以支持小数
        self.intensity_slider.setValue(50)  # 默认值设为50，对应0.5
        self.intensity_value = QtWidgets.QLabel("5")
        self.intensity_slider.setEnabled(False)  # 默认禁用，只有非平均时启用
        
        # 生成按钮
        self.generate_btn = QtWidgets.QPushButton("生成毛囊点UV")
        
        # 结果显示框
        self.result_label = QtWidgets.QLabel("生成结果:")
        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        
        # 复制按钮
        self.clear_btn = QtWidgets.QPushButton("清除结果")
        
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 第一行布局
        selection_layout = QtWidgets.QHBoxLayout()
        selection_layout.addWidget(self.selection_label)
        selection_layout.addWidget(self.selection_text, 1)
        selection_layout.addWidget(self.get_selection_btn)
        
        # 第二行布局
        count_layout = QtWidgets.QHBoxLayout()
        count_layout.addWidget(self.count_label)
        count_layout.addWidget(self.count_spinbox)
        count_layout.addWidget(self.selectLoc)
        count_layout.addStretch()
        
        # 第三行布局 - 间距选项
        spacing_layout = QtWidgets.QHBoxLayout()
        spacing_layout.addWidget(self.spacing_label)
        spacing_layout.addWidget(self.average_radio)
        spacing_layout.addWidget(self.increasing_radio)
        spacing_layout.addWidget(self.decreasing_radio)
        spacing_layout.addStretch()
        
        # 程度控制布局
        intensity_layout = QtWidgets.QHBoxLayout()
        intensity_layout.addWidget(self.intensity_label)
        intensity_layout.addWidget(self.intensity_slider, 1)
        intensity_layout.addWidget(self.intensity_value)
        
        # 按钮布局
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.generate_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_btn)
        
        # 主布局添加
        main_layout.addLayout(selection_layout)
        main_layout.addLayout(count_layout)
        main_layout.addLayout(spacing_layout)
        main_layout.addLayout(intensity_layout)
        main_layout.addWidget(self.generate_btn)
        main_layout.addSpacing(5)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.result_text, 1)
        main_layout.addLayout(button_layout)
        
    def create_connections(self):
        self.get_selection_btn.clicked.connect(self.get_selection)
        self.generate_btn.clicked.connect(self.generate_follicle_uvs)
        # self.copy_btn.clicked.connect(self.copy_results)
        self.clear_btn.clicked.connect(self.clear_results)
        self.selectLoc.clicked.connect(self.update_result_in_select)
        
        # 修改滑块值变化连接，使用浮点数并实时更新结果
        self.intensity_slider.valueChanged.connect(self.on_intensity_changed)
        
        # 连接单选按钮信号
        self.average_radio.toggled.connect(self.toggle_intensity_control)
        self.increasing_radio.toggled.connect(self.toggle_intensity_control)
        self.decreasing_radio.toggled.connect(self.toggle_intensity_control)
        
        # 连接数量变化信号，实现实时更新
        self.count_spinbox.valueChanged.connect(self.update_result_in_realtime)
        
        # 连接间距类型变化信号，实现实时更新
        self.spacing_group.buttonToggled.connect(self.update_result_in_realtime)
        
    def on_intensity_changed(self, value):
        """滑块值变化时的处理，转换为浮点数并实时更新结果"""
        # 将整数值转换为浮点数 (1-100 映射到 0.1-10.0)
        float_value = value / 10.0
        self.intensity_value.setText(f"{float_value:.1f}")
        self.update_result_in_realtime()
        
    def toggle_intensity_control(self, checked):
        """根据选择的间距类型启用/禁用程度控制"""
        if checked:
            if self.average_radio.isChecked():
                self.intensity_slider.setEnabled(False)
            else:
                self.intensity_slider.setEnabled(True)
            self.update_result_in_realtime()
        
    def get_selection(self):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning("请先选择曲面或曲线")
            return
            
        self.selected_object = selection[0]
        shape_node = cmds.listRelatives(self.selected_object, shapes=True)
        
        if not shape_node:
            cmds.warning("选择的对象没有形状节点")
            return
            
        shape_type = cmds.objectType(shape_node[0])
        
        if shape_type in ["nurbsSurface", "mesh"]:
            self.object_type = "surface"
            self.selection_text.setText(f"{self.selected_object} (曲面)")
        elif shape_type in ["nurbsCurve"]:
            self.object_type = "curve"
            self.selection_text.setText(f"{self.selected_object} (曲线)")
        else:
            cmds.warning("请选择曲面或曲线")
            self.selected_object = None
            self.object_type = None
            self.selection_text.clear()
        
        # 选择改变后实时更新结果
        self.update_result_in_realtime()
            
    def generate_uv_distribution(self, count, spacing_type, intensity):
        """生成UV分布"""
        uvs = []
        
        if spacing_type == 0:  # 平均
            for i in range(count):
                u = i / max(1, count - 1)
                uvs.append((u, 0.5))
                
        elif spacing_type == 1:  # 递增
            factor = intensity  # 现在intensity已经是浮点数
            for i in range(count):
                t = i / max(1, count - 1)
                u = (1 - (1 - t) ** (1 + factor))
                uvs.append((u, 0.5))
                
        else:  # 递减
            factor = intensity  # 现在intensity已经是浮点数
            for i in range(count):
                t = i / max(1, count - 1)
                u = t ** (1 + factor)
                uvs.append((u, 0.5))
                
        return uvs
    
    def generate_follicle_uvs(self):
        """生成毛囊点UV（保持原有功能）"""
        if not self.selected_object or not self.object_type:
            cmds.warning("请先选择有效的曲面或曲线")
            return
        
        if self.selectLoc.isChecked():
            self.generate_follicle_select()
            return
        
        cmds.undoInfo(openChunk=True )
        count = self.count_spinbox.value()
        spacing_type = self.spacing_group.checkedId()
        intensity = self.intensity_slider.value() / 10.0  # 转换为浮点数

        uvs = self.generate_uv_distribution(count, spacing_type, intensity)
        shape=cmds.listRelatives(self.selected_object,c=1)[0]
        grp=cmds.listRelatives(self.selected_object,p=1) or []
        for i, (u, v) in enumerate(uvs):
            name=self.selected_object+'_'+str(i)
            if self.object_type == "surface":
                #创建毛囊shape
                newFolicleShape = cmds.createNode('follicle', n=name+"_drive_md")
                #获取毛囊节点
                newFolicle = cmds.listRelatives(newFolicleShape, p=True)[0]
                cmds.connectAttr(shape + ".local", newFolicleShape + ".inputSurface")
                cmds.connectAttr(shape + ".worldMatrix[0]", newFolicleShape + ".inputWorldMatrix")
                cmds.connectAttr(newFolicleShape + ".outRotate", newFolicle + ".rotate")
                cmds.connectAttr(newFolicleShape + ".outTranslate", newFolicle + ".translate")
                cmds.setAttr(newFolicle + ".parameterU", u)
                cmds.setAttr(newFolicle + ".parameterV", v)
                # loc=cmds.spaceLocator()[0]
                # cmds.matchTransform(loc,newFolicle)
                # cmds.parent(loc,newFolicle)
                # if grp:
                #     cmds.parent(newFolicle,grp)
                pos=cmds.xform(newFolicle,q=1,ws=1,t=1)
                rot=cmds.xform(newFolicle,q=1,ws=1,ro=1)
                cmds.select(cl=1)
                off=cmds.joint(n=name+'_drive',p=pos,o=rot)
                cmds.parent(off,newFolicle)
                if grp:
                        cmds.parent(newFolicle,grp)
                newFolicle=cmds.rename(newFolicle,name+"_fol")

            elif self.object_type == "curve":
                md=cmds.createNode('motionPath',n=name+'_drive_md')
                cmds.setAttr(md+".fractionMode",1)
                cmds.connectAttr(shape+".worldSpace[0]",md+".geometryPath",f=1,na=False)
                cmds.setAttr(md+".uValue",u)
                drive=cmds.spaceLocator(n=name+'_loc')[0]
                # drive=cmds.createNode('transform',n=name+'_loc')
                cmds.connectAttr(md+".allCoordinates",drive+".translate",f=1)
                cmds.connectAttr(md+".rotate",drive+".rotate",f=1)
                if grp:
                    cmds.parent(drive,grp)

        cmds.undoInfo(closeChunk=True )
        
    def update_result_in_realtime(self):
        """实时更新结果文本"""
        if not self.selected_object or not self.object_type :
            return
        
        if ( self.selectLoc.isChecked()):
            return
        
        count = self.count_spinbox.value()
        spacing_type = self.spacing_group.checkedId()
        intensity = self.intensity_slider.value() / 10.0  # 转换为浮点数
        
        # 生成UV分布
        uvs = self.generate_uv_distribution(count, spacing_type, intensity)
    
        # 显示结果
        self.display_results(uvs)
        
                
    def update_result_in_select(self):
        if not self.selected_object or not self.object_type or (not self.selectLoc.isChecked()):
            return
        
        se=cmds.ls(sl=1) 
        cmds.undoInfo(openChunk=True )
        result_text=''
        shape=cmds.listRelatives(self.selected_object,c=1)[0]
        value = 0.0001

        if self.object_type == "surface":
            for i in se:
                closestPoint=cmds.shadingNode("closestPointOnSurface",au=1)
                cmds.connectAttr(shape+".worldSpace[0]",closestPoint+".inputSurface",f=1)
                locatorPosition = cmds.xform(i, t=True, q=True, ws=True)
                cmds.setAttr(closestPoint + ".inPosition", locatorPosition[0],locatorPosition[1],locatorPosition[2])
                u=cmds.getAttr(closestPoint+".result.parameterU")
                v=cmds.getAttr(closestPoint+".result.parameterV")
                cmds.delete(closestPoint)
                result_text += f" {i}: U = {u} | V = {v}\n"

            self.result_text.setText(result_text)

            pass
        elif self.object_type == "curve":
            for i in se:
                ne=cmds.createNode('nearestPointOnCurve')
                point=cmds.xform(i,q=1,ws=1,t=1)
                cmds.connectAttr(shape+'.worldSpace[0]',ne+'.inputCurve',f=1)
                cmds.setAttr(ne+'.inPosition',point[0],point[1],point[2])
                u=cmds.getAttr(ne+'.parameter')
                if u<value:
                    u=0.0
                cmds.delete(ne)
                result_text += f" {i}: U = {u}\n"
        
            self.result_text.setText(result_text)
            
        cmds.undoInfo(closeChunk=True )

    def generate_follicle_select(self):
        """从结果文本中获取每行的U和V值"""
        result_text = self.result_text.toPlainText().strip()
        
        if not result_text:
            cmds.warning("结果文本为空")
            return []
        
        uv_values = []
        lines = result_text.split('\n')
        se=cmds.ls(sl=1)
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 使用正则表达式提取U和V值
            # 匹配模式：U = 数字, V = 数字 或 U = 数字
            u_pattern = r"U\s*=\s*([\d.]+)"
            v_pattern = r"V\s*=\s*([\d.]+)"
            
            u_match = re.search(u_pattern, line)
            v_match = re.search(v_pattern, line)
            
            if u_match:
                u_value = float(u_match.group(1))
                v_value = float(v_match.group(1)) if v_match else 0.5  # 如果没有V值，默认为0.5
                uv_values.append((u_value, v_value))
                

        cmds.undoInfo(openChunk=True)

        shape=cmds.listRelatives(self.selected_object,c=1)[0]
        grp=cmds.listRelatives(self.selected_object,p=1) or []
        for i, (u, v) in enumerate(uv_values):
            name=self.selected_object+'_'+str(i)
            if self.object_type == "surface":
                #创建毛囊shape
                newFolicleShape = cmds.createNode('follicle')
                #获取毛囊节点
                newFolicle = cmds.listRelatives(newFolicleShape, p=True)[0]

                cmds.connectAttr(shape + ".local", newFolicleShape + ".inputSurface")
                cmds.connectAttr(shape + ".worldMatrix[0]", newFolicleShape + ".inputWorldMatrix")
                cmds.connectAttr(newFolicleShape + ".outRotate", newFolicle + ".rotate")
                cmds.connectAttr(newFolicleShape + ".outTranslate", newFolicle + ".translate")
                cmds.setAttr(newFolicle + ".parameterU", u)
                cmds.setAttr(newFolicle + ".parameterV", v)
                pos=cmds.xform(newFolicle,q=1,ws=1,t=1)
                rot=cmds.xform(newFolicle,q=1,ws=1,ro=1)
                cmds.select(cl=1)
                off=cmds.joint(n=name+'_drive',p=pos,o=rot)
                cmds.parent(off,newFolicle)
                try:
                    target=se[i]
                    cmds.matchTransform(off,target)
                    cmds.parentConstraint(off,target)
                except:
                    pass

                if grp:
                        cmds.parent(newFolicle,grp)
                newFolicle=cmds.rename(newFolicle,name+"_fol")

            elif self.object_type == "curve":
                md=cmds.createNode('motionPath',n=name+'_drive_md')
                cmds.setAttr(md+".fractionMode",1)
                cmds.connectAttr(shape+".worldSpace[0]",md+".geometryPath",f=1,na=False)
                try:
                    cmds.setAttr(md+".uValue",u)
                except:
                    print(u)
                drive=cmds.createNode('transform',n=name+'_loc')
                cmds.connectAttr(md+".allCoordinates",drive+".translate",f=1)
                cmds.connectAttr(md+".rotate",drive+".rotate",f=1)
                pos=cmds.xform(drive,q=1,ws=1,t=1)
                rot=cmds.xform(drive,q=1,ws=1,ro=1)
                cmds.select(cl=1)
                off=cmds.joint(n=name+'_drive',p=pos,o=rot)
                cmds.parent(off,drive)

                try:
                    target=se[i]
                    # off=cmds.joint(n=target+'_drive',p=pos,o=rot)
                    # cmds.createNode('transform',n=target+'_drive')
                    # cmds.parent(off,drive)
                    cmds.matchTransform(off,target)
                    # pp1=cmds.listRelatives(target,p=1)
                    # if pp1:
                    #     pp2=cmds.listRelatives(pp1[0],p=1)
                    #     if pp2:
                    #         target=pp2[0]
                    #     else:
                    #         target=pp1[0]

                    cmds.parentConstraint(off,target)
                    
                except:
                    pass
                
                if grp:
                    cmds.parent(drive,grp)

        cmds.undoInfo(closeChunk=True )




        # return uv_values


    def display_results(self, uvs):
        result_text=''
        for i, (u, v) in enumerate(uvs):
            if self.object_type == "curve":
                result_text += f"点 {i+1:2d}: U = {u:.4f}\n"
            else:
                result_text += f"点 {i+1:2d}: U = {u:.4f}, V = {v:.4f}\n"
                
        self.result_text.setText(result_text)
            
        

    def clear_results(self):
        """清除结果显示"""
        self.result_text.clear()


def show_ui():
    """
    显示UI窗口，如果已存在则先关闭
    """
    # 关闭已存在的窗口
    for widget in QtWidgets.QApplication.allWidgets():
        if widget.objectName() == "FollicleUVGenerator":
            widget.close()
            widget.deleteLater()
            
    # 创建新窗口
    dialog = FollicleUVGenerator()
    dialog.show()
    return dialog