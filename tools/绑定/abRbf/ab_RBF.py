"""
RBF变形器插件 - Maya版本 v2.0
作者: DeepSeek
版本: 2.0 - 支持所有对象属性和自定义属性编辑
"""

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import math
import json
import os
import re
from collections import OrderedDict
from functools import partial


class RBFDeformerPlugin(QtWidgets.QDialog):
    """RBF变形器插件主窗口"""
    
    def __init__(self, parent=None):
        super(RBFDeformerPlugin, self).__init__(parent)
        self.setWindowTitle("RBF变形器插件 v2.0")
        self.setMinimumSize(1000, 700)
        
        # 存储驱动和受驱动对象
        self.driver_objects = OrderedDict()  # {name: transform}
        self.driven_objects = OrderedDict()   # {name: transform}
        
        # 存储编辑状态
        self.edit_mode = False
        self.base_driver_states = {}  # 驱动对象的基准状态
        self.base_driven_states = {}  # 受驱动对象的基准状态
        
        # 存储RBF数据
        self.rbf_data = {
            'driver_weights': {},  # 驱动权重
            'driven_offsets': {}   # 受驱动偏移
        }
        
        # 存储所有对象的属性配置
        self.object_attributes = {}  # {object_name: {attr_name: attr_data}}
        
        # 自定义属性模板
        self.attribute_templates = {
            'transform': {
                '位移': [
                    {'name': 'translateX', 'label': '位移X', 'type': 'float', 'min': -100, 'max': 100},
                    {'name': 'translateY', 'label': '位移Y', 'type': 'float', 'min': -100, 'max': 100},
                    {'name': 'translateZ', 'label': '位移Z', 'type': 'float', 'min': -100, 'max': 100}
                ],
                '旋转': [
                    {'name': 'rotateX', 'label': '旋转X', 'type': 'float', 'min': -360, 'max': 360},
                    {'name': 'rotateY', 'label': '旋转Y', 'type': 'float', 'min': -360, 'max': 360},
                    {'name': 'rotateZ', 'label': '旋转Z', 'type': 'float', 'min': -360, 'max': 360}
                ],
                '缩放': [
                    {'name': 'scaleX', 'label': '缩放X', 'type': 'float', 'min': 0, 'max': 10},
                    {'name': 'scaleY', 'label': '缩放Y', 'type': 'float', 'min': 0, 'max': 10},
                    {'name': 'scaleZ', 'label': '缩放Z', 'type': 'float', 'min': 0, 'max': 10}
                ],
                '可见性': [
                    {'name': 'visibility', 'label': '可见性', 'type': 'bool'}
                ]
            },
            'blendShape': {
                '融合变形': [
                    # 动态获取融合变形权重
                ]
            }
        }
        
        # 防止选中时的递归调用
        self.block_selection_signal = False
        
        # 监听Maya选择变化
        self.selection_callback = None
        
        # 当前选中的对象
        self.current_selected_object = None
        
        self.setup_ui()
        self.setStyleSheet(self.get_stylesheet())
        
        # 设置选中同步
        self.setup_selection_sync()
        
    def setup_ui(self):
        """设置用户界面"""
        main_layout = QtWidgets.QHBoxLayout(self)
        
        # 左侧面板
        left_panel = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title_label = QtWidgets.QLabel("RBF变形器系统")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QtGui.QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        left_layout.addWidget(title_label)
        
        # 上下分割布局
        splitter = QtWidgets.QSplitter(Qt.Vertical)
        
        # 上部：对象列表区域
        objects_group = QtWidgets.QGroupBox("对象列表")
        objects_layout = QtWidgets.QVBoxLayout()
        
        # 对象类型标签
        type_tabs = QtWidgets.QTabWidget()
        
        # 驱动对象标签页
        driver_tab = QtWidgets.QWidget()
        driver_layout = QtWidgets.QVBoxLayout(driver_tab)
        driver_layout.setContentsMargins(5, 5, 5, 5)
        
        # 驱动对象工具栏
        driver_toolbar = QtWidgets.QHBoxLayout()
        self.driver_list = QtWidgets.QListWidget()
        self.driver_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        # 驱动对象按钮
        add_driver_btn = QtWidgets.QPushButton("添加为驱动")
        add_driver_btn.clicked.connect(self.add_as_driver)
        remove_driver_btn = QtWidgets.QPushButton("移除")
        remove_driver_btn.clicked.connect(self.remove_driver_objects)
        
        driver_toolbar.addWidget(add_driver_btn)
        driver_toolbar.addWidget(remove_driver_btn)
        driver_toolbar.addStretch()
        
        driver_layout.addLayout(driver_toolbar)
        driver_layout.addWidget(self.driver_list)
        
        # 受驱动对象标签页
        driven_tab = QtWidgets.QWidget()
        driven_layout = QtWidgets.QVBoxLayout(driven_tab)
        driven_layout.setContentsMargins(5, 5, 5, 5)
        
        # 受驱动对象工具栏
        driven_toolbar = QtWidgets.QHBoxLayout()
        self.driven_list = QtWidgets.QListWidget()
        self.driven_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        # 受驱动对象按钮
        add_driven_btn = QtWidgets.QPushButton("添加为受驱动")
        add_driven_btn.clicked.connect(self.add_as_driven)
        remove_driven_btn = QtWidgets.QPushButton("移除")
        remove_driven_btn.clicked.connect(self.remove_driven_objects)
        
        driven_toolbar.addWidget(add_driven_btn)
        driven_toolbar.addWidget(remove_driven_btn)
        driven_toolbar.addStretch()
        
        driven_layout.addLayout(driven_toolbar)
        driven_layout.addWidget(self.driven_list)
        
        # 添加标签页
        type_tabs.addTab(driver_tab, "驱动对象 (橙色)")
        type_tabs.addTab(driven_tab, "受驱动对象 (蓝色)")
        
        objects_layout.addWidget(type_tabs)
        objects_group.setLayout(objects_layout)
        
        # 下部：控制按钮区域
        control_group = QtWidgets.QGroupBox("控制面板")
        control_layout = QtWidgets.QVBoxLayout()
        
        # 编辑按钮
        self.edit_btn = QtWidgets.QPushButton("编辑模式: 关闭")
        self.edit_btn.setCheckable(True)
        self.edit_btn.setFixedHeight(40)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        control_layout.addWidget(self.edit_btn)
        
        # 开始/停止按钮
        self.start_btn = QtWidgets.QPushButton("开始录制")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.toggle_recording)
        control_layout.addWidget(self.start_btn)
        
        # 重置按钮
        reset_btn = QtWidgets.QPushButton("重置全部")
        reset_btn.setFixedHeight(40)
        reset_btn.clicked.connect(self.reset_all)
        control_layout.addWidget(reset_btn)
        
        # 添加对象到两边按钮
        dual_add_btn = QtWidgets.QPushButton("添加到驱动和受驱动")
        dual_add_btn.setFixedHeight(40)
        dual_add_btn.clicked.connect(self.add_as_both)
        control_layout.addWidget(dual_add_btn)
        
        control_group.setLayout(control_layout)
        
        splitter.addWidget(objects_group)
        splitter.addWidget(control_group)
        splitter.setSizes([400, 200])
        
        left_layout.addWidget(splitter)
        
        # 状态栏
        self.status_bar = QtWidgets.QLabel("就绪 - 在列表中点击选择场景中的对象")
        self.status_bar.setAlignment(Qt.AlignCenter)
        self.status_bar.setStyleSheet("background-color: #2d2d2d; padding: 5px;")
        left_layout.addWidget(self.status_bar)
        
        # 右侧面板 - 属性编辑器
        right_panel = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 属性编辑器标题
        self.attr_title = QtWidgets.QLabel("属性编辑器")
        self.attr_title.setAlignment(Qt.AlignCenter)
        title_font = QtGui.QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.attr_title.setFont(title_font)
        right_layout.addWidget(self.attr_title)
        
        # 当前选中对象显示
        self.current_object_label = QtWidgets.QLabel("未选中对象")
        self.current_object_label.setAlignment(Qt.AlignCenter)
        self.current_object_label.setStyleSheet("background-color: #3a3a3a; padding: 5px;")
        right_layout.addWidget(self.current_object_label)
        
        # 属性编辑器区域
        attr_scroll = QtWidgets.QScrollArea()
        attr_scroll.setWidgetResizable(True)
        attr_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.attr_container = QtWidgets.QWidget()
        self.attr_layout = QtWidgets.QVBoxLayout(self.attr_container)
        self.attr_layout.setAlignment(Qt.AlignTop)
        
        attr_scroll.setWidget(self.attr_container)
        right_layout.addWidget(attr_scroll)
        
        # 添加自定义属性区域
        add_attr_group = QtWidgets.QGroupBox("添加自定义属性")
        add_attr_layout = QtWidgets.QVBoxLayout()
        
        # 属性名称
        attr_name_layout = QtWidgets.QHBoxLayout()
        attr_name_label = QtWidgets.QLabel("属性名:")
        self.attr_name_input = QtWidgets.QLineEdit()
        self.attr_name_input.setPlaceholderText("例如: myCustomAttr")
        attr_name_layout.addWidget(attr_name_label)
        attr_name_layout.addWidget(self.attr_name_input)
        add_attr_layout.addLayout(attr_name_layout)
        
        # 属性标签
        attr_label_layout = QtWidgets.QHBoxLayout()
        attr_label_label = QtWidgets.QLabel("显示名:")
        self.attr_label_input = QtWidgets.QLineEdit()
        self.attr_label_input.setPlaceholderText("例如: 自定义属性")
        attr_label_layout.addWidget(attr_label_label)
        attr_label_layout.addWidget(self.attr_label_input)
        add_attr_layout.addLayout(attr_label_layout)
        
        # 属性类型
        attr_type_layout = QtWidgets.QHBoxLayout()
        attr_type_label = QtWidgets.QLabel("类型:")
        self.attr_type_combo = QtWidgets.QComboBox()
        self.attr_type_combo.addItems(["浮点型", "整数型", "布尔型", "向量型"])
        attr_type_layout.addWidget(attr_type_label)
        attr_type_layout.addWidget(self.attr_type_combo)
        add_attr_layout.addLayout(attr_type_layout)
        
        # 属性范围
        self.attr_range_group = QtWidgets.QGroupBox("数值范围")
        self.attr_range_group.setCheckable(True)
        self.attr_range_group.setChecked(False)
        range_layout = QtWidgets.QGridLayout()
        
        min_label = QtWidgets.QLabel("最小值:")
        self.attr_min_input = QtWidgets.QDoubleSpinBox()
        self.attr_min_input.setRange(-9999, 9999)
        self.attr_min_input.setValue(0)
        
        max_label = QtWidgets.QLabel("最大值:")
        self.attr_max_input = QtWidgets.QDoubleSpinBox()
        self.attr_max_input.setRange(-9999, 9999)
        self.attr_max_input.setValue(1)
        
        range_layout.addWidget(min_label, 0, 0)
        range_layout.addWidget(self.attr_min_input, 0, 1)
        range_layout.addWidget(max_label, 1, 0)
        range_layout.addWidget(self.attr_max_input, 1, 1)
        
        self.attr_range_group.setLayout(range_layout)
        add_attr_layout.addWidget(self.attr_range_group)
        
        # 添加属性按钮
        add_custom_attr_btn = QtWidgets.QPushButton("添加自定义属性")
        add_custom_attr_btn.clicked.connect(self.add_custom_attribute)
        add_attr_layout.addWidget(add_custom_attr_btn)
        
        # 刷新属性按钮
        refresh_attrs_btn = QtWidgets.QPushButton("刷新对象属性")
        refresh_attrs_btn.clicked.connect(self.refresh_object_attributes)
        add_attr_layout.addWidget(refresh_attrs_btn)
        
        add_attr_group.setLayout(add_attr_layout)
        right_layout.addWidget(add_attr_group)
        
        # 添加到布局
        main_layout.addWidget(left_panel, 3)
        main_layout.addWidget(right_panel, 2)
        
    def get_stylesheet(self):
        """返回样式表"""
        return """
        QDialog {
            background-color: #353535;
            color: #cccccc;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QListWidget {
            background-color: #2d2d2d;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px;
        }
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #444444;
        }
        QListWidget::item:selected {
            background-color: #4a6984;
        }
        QPushButton {
            background-color: #5a5a5a;
            border: 1px solid #666666;
            border-radius: 3px;
            padding: 5px 15px;
            color: white;
        }
        QPushButton:hover {
            background-color: #6a6a6a;
            border-color: #777777;
        }
        QPushButton:pressed {
            background-color: #4a4a4a;
        }
        QPushButton:checked {
            background-color: #8a1a1a;
            font-weight: bold;
        }
        QLabel {
            color: #cccccc;
        }
        QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {
            background-color: #2d2d2d;
            border: 1px solid #555555;
            color: white;
            padding: 3px;
            border-radius: 3px;
        }
        QScrollArea {
            border: 1px solid #555555;
            background-color: #2d2d2d;
            border-radius: 3px;
        }
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
        }
        """
    
    def setup_selection_sync(self):
        """设置选中同步"""
        # 连接列表选中变化信号
        self.driver_list.itemSelectionChanged.connect(self.on_driver_selection_changed)
        self.driven_list.itemSelectionChanged.connect(self.on_driven_selection_changed)
        
        # 设置Maya选择变化回调
        self.setup_maya_selection_callback()
    
    def setup_maya_selection_callback(self):
        """设置Maya选择变化回调"""
        # 移除已存在的回调
        if self.selection_callback:
            try:
                om.MEventMessage.removeCallback(self.selection_callback)
            except:
                pass
        
        # 创建新的回调
        try:
            self.selection_callback = om.MEventMessage.addEventCallback(
                "SelectionChanged", self.on_maya_selection_changed
            )
        except:
            print("无法创建Maya选择回调")
    
    def on_maya_selection_changed(self, *args):
        """Maya选择变化时的回调"""
        if self.block_selection_signal:
            return
            
        # 获取当前Maya中的选择
        selected_objects = cmds.ls(selection=True, transforms=True)
        if not selected_objects:
            return
            
        # 避免递归调用
        self.block_selection_signal = True
        
        try:
            # 清空列表选择
            self.driver_list.clearSelection()
            self.driven_list.clearSelection()
            
            # 根据选择的物体更新列表选择状态
            for obj in selected_objects:
                # 检查是否是驱动对象
                for i in range(self.driver_list.count()):
                    item = self.driver_list.item(i)
                    item_obj_name = self.extract_object_name(item.text())
                    if item_obj_name == obj:
                        item.setSelected(True)
                
                # 检查是否是受驱动对象
                for i in range(self.driven_list.count()):
                    item = self.driven_list.item(i)
                    item_obj_name = self.extract_object_name(item.text())
                    if item_obj_name == obj:
                        item.setSelected(True)
            
            # 更新属性编辑器
            if selected_objects:
                self.show_object_attributes(selected_objects[0])
                
        finally:
            self.block_selection_signal = False
    
    def extract_object_name(self, item_text):
        """从列表项文本中提取对象名称"""
        # 移除位置信息，只保留对象名称
        if "[" in item_text:
            return item_text.split("[")[0].strip()
        return item_text.strip()
    
    def on_driver_selection_changed(self):
        """驱动对象列表选中变化"""
        if self.block_selection_signal:
            return
            
        # 避免递归调用
        self.block_selection_signal = True
        
        try:
            selected_items = self.driver_list.selectedItems()
            if not selected_items:
                return
                
            # 获取选中的对象名称
            selected_objects = []
            for item in selected_items:
                obj_name = self.extract_object_name(item.text())
                if cmds.objExists(obj_name):
                    selected_objects.append(obj_name)
            
            # 在场景中选中这些对象
            if selected_objects:
                cmds.select(selected_objects, replace=True)
                self.update_status(f"已选中 {len(selected_objects)} 个驱动对象")
                
                # 显示第一个选中对象的属性
                self.show_object_attributes(selected_objects[0])
                
        finally:
            self.block_selection_signal = False
    
    def on_driven_selection_changed(self):
        """受驱动对象列表选中变化"""
        if self.block_selection_signal:
            return
            
        # 避免递归调用
        self.block_selection_signal = True
        
        try:
            selected_items = self.driven_list.selectedItems()
            if not selected_items:
                return
                
            # 获取选中的对象名称
            selected_objects = []
            for item in selected_items:
                obj_name = self.extract_object_name(item.text())
                if cmds.objExists(obj_name):
                    selected_objects.append(obj_name)
            
            # 在场景中选中这些对象
            if selected_objects:
                cmds.select(selected_objects, replace=True)
                self.update_status(f"已选中 {len(selected_objects)} 个受驱动对象")
                
                # 显示第一个选中对象的属性
                self.show_object_attributes(selected_objects[0])
                
        finally:
            self.block_selection_signal = False
    
    def add_as_driver(self):
        """添加选中对象为驱动对象"""
        selection = cmds.ls(selection=True, transforms=True)
        if not selection:
            cmds.warning("请选择至少一个变换对象")
            return
            
        for obj in selection:
            if obj not in self.driver_objects:
                self.driver_objects[obj] = {
                    'transform': obj,
                    'position': [0, 0, 0],
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1]
                }
                
                # 创建列表项
                item = QtWidgets.QListWidgetItem(obj)
                item.setIcon(QtGui.QIcon(":/transform.png"))
                self.driver_list.addItem(item)
                
                # 设置初始颜色
                self.update_object_color(obj, "driver")
                
                # 初始化对象属性
                self.initialize_object_attributes(obj)
        
        self.update_status(f"已添加 {len(selection)} 个驱动对象")
    
    def add_as_driven(self):
        """添加选中对象为受驱动对象"""
        selection = cmds.ls(selection=True, transforms=True)
        if not selection:
            cmds.warning("请选择至少一个变换对象")
            return
            
        for obj in selection:
            if obj not in self.driven_objects:
                self.driven_objects[obj] = {
                    'transform': obj,
                    'position': [0, 0, 0],
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1]
                }
                
                # 创建列表项
                item = QtWidgets.QListWidgetItem(obj)
                item.setIcon(QtGui.QIcon(":/transform.png"))
                self.driven_list.addItem(item)
                
                # 设置初始颜色
                self.update_object_color(obj, "driven")
                
                # 初始化对象属性
                self.initialize_object_attributes(obj)
        
        self.update_status(f"已添加 {len(selection)} 个受驱动对象")
    
    def add_as_both(self):
        """添加选中对象为驱动和受驱动对象"""
        selection = cmds.ls(selection=True, transforms=True)
        if not selection:
            cmds.warning("请选择至少一个变换对象")
            return
        
        added_driver = 0
        added_driven = 0
        
        for obj in selection:
            # 添加为驱动对象
            if obj not in self.driver_objects:
                self.driver_objects[obj] = {
                    'transform': obj,
                    'position': [0, 0, 0],
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1]
                }
                
                # 创建列表项
                item = QtWidgets.QListWidgetItem(obj)
                item.setIcon(QtGui.QIcon(":/transform.png"))
                self.driver_list.addItem(item)
                
                # 设置颜色
                self.update_object_color(obj, "driver")
                added_driver += 1
            
            # 添加为受驱动对象
            if obj not in self.driven_objects:
                self.driven_objects[obj] = {
                    'transform': obj,
                    'position': [0, 0, 0],
                    'rotation': [0, 0, 0],
                    'scale': [1, 1, 1]
                }
                
                # 创建列表项
                item = QtWidgets.QListWidgetItem(obj)
                item.setIcon(QtGui.QIcon(":/transform.png"))
                self.driven_list.addItem(item)
                
                # 设置颜色 - 受驱动覆盖驱动颜色
                self.update_object_color(obj, "both")
                added_driven += 1
            
            # 初始化对象属性
            self.initialize_object_attributes(obj)
        
        self.update_status(f"已添加 {added_driver} 个驱动对象，{added_driven} 个受驱动对象")
    
    def remove_driver_objects(self):
        """移除选中的驱动对象"""
        selected_items = self.driver_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            obj = self.extract_object_name(item.text())
            if obj in self.driver_objects:
                del self.driver_objects[obj]
                # 恢复对象颜色
                if obj in self.driven_objects:
                    self.update_object_color(obj, "driven")
                else:
                    cmds.setAttr(obj + ".overrideEnabled", 0)
            row = self.driver_list.row(item)
            self.driver_list.takeItem(row)
            
        self.update_status(f"已移除 {len(selected_items)} 个驱动对象")
    
    def remove_driven_objects(self):
        """移除选中的受驱动对象"""
        selected_items = self.driven_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            obj = self.extract_object_name(item.text())
            if obj in self.driven_objects:
                del self.driven_objects[obj]
                # 恢复对象颜色
                if obj in self.driver_objects:
                    self.update_object_color(obj, "driver")
                else:
                    cmds.setAttr(obj + ".overrideEnabled", 0)
            row = self.driven_list.row(item)
            self.driven_list.takeItem(row)
            
        self.update_status(f"已移除 {len(selected_items)} 个受驱动对象")
    
    def update_object_color(self, obj, obj_type):
        """更新对象显示颜色"""
        if not cmds.objExists(obj):
            return
            
        cmds.setAttr(obj + ".overrideEnabled", 1)
        cmds.setAttr(obj + ".overrideRGBColors", 1)
        
        if obj_type == "driver":
            color = [1, 0.5, 0]  # 橙色
        elif obj_type == "driven":
            color = [0, 0.7, 1]  # 蓝色
        elif obj_type == "both":
            color = [0.5, 0.8, 0.2]  # 绿色
        else:
            color = [0.7, 0.7, 0.7]  # 灰色
            
        cmds.setAttr(obj + ".overrideColorRGB", *color)
    
    def initialize_object_attributes(self, obj):
        """初始化对象的属性配置"""
        if obj not in self.object_attributes:
            self.object_attributes[obj] = {}
        
        # 获取对象类型
        obj_type = self.get_object_type(obj)
        
        # 添加默认变换属性
        if obj_type == "transform":
            self.add_default_transform_attributes(obj)
        
        # 检查融合变形
        self.add_blendshape_attributes(obj)
    
    def get_object_type(self, obj):
        """获取对象类型"""
        if not cmds.objExists(obj):
            return "unknown"
        
        # 检查是否为变换节点
        if cmds.objectType(obj, isType="transform"):
            return "transform"
        elif cmds.objectType(obj, isType="joint"):
            return "joint"
        elif cmds.objectType(obj, isType="nurbsCurve"):
            return "curve"
        elif cmds.objectType(obj, isType="mesh"):
            return "mesh"
        else:
            return "unknown"
    
    def add_default_transform_attributes(self, obj):
        """添加默认变换属性"""
        transform_attrs = [
            # 位移
            {"name": "translateX", "label": "位移 X", "type": "float", "min": -100, "max": 100},
            {"name": "translateY", "label": "位移 Y", "type": "float", "min": -100, "max": 100},
            {"name": "translateZ", "label": "位移 Z", "type": "float", "min": -100, "max": 100},
            # 旋转
            {"name": "rotateX", "label": "旋转 X", "type": "float", "min": -360, "max": 360},
            {"name": "rotateY", "label": "旋转 Y", "type": "float", "min": -360, "max": 360},
            {"name": "rotateZ", "label": "旋转 Z", "type": "float", "min": -360, "max": 360},
            # 缩放
            {"name": "scaleX", "label": "缩放 X", "type": "float", "min": 0, "max": 10},
            {"name": "scaleY", "label": "缩放 Y", "type": "float", "min": 0, "max": 10},
            {"name": "scaleZ", "label": "缩放 Z", "type": "float", "min": 0, "max": 10},
            # 可见性
            {"name": "visibility", "label": "可见性", "type": "bool"}
        ]
        
        for attr in transform_attrs:
            attr_full_name = f"{obj}.{attr['name']}"
            if cmds.objExists(attr_full_name):
                self.object_attributes[obj][attr['name']] = attr.copy()
                # 添加当前值
                self.object_attributes[obj][attr['name']]['current_value'] = self.get_attribute_value(obj, attr['name'])
    
    def add_blendshape_attributes(self, obj):
        """添加融合变形属性"""
        # 检查对象是否有融合变形
        blendshapes = cmds.listConnections(obj, type="blendShape")
        if blendshapes:
            for bs in blendshapes:
                # 获取所有权重属性
                weights = cmds.listAttr(f"{bs}.weight", multi=True)
                if weights:
                    for i, weight in enumerate(weights):
                        attr_name = f"{bs}.{weight}"
                        attr_label = f"融合变形 {i+1}: {weight}"
                        
                        self.object_attributes[obj][attr_name] = {
                            "name": attr_name,
                            "label": attr_label,
                            "type": "float",
                            "min": 0,
                            "max": 1,
                            "current_value": cmds.getAttr(attr_name)
                        }
    
    def get_attribute_value(self, obj, attr_name):
        """获取属性值"""
        attr_full_name = f"{obj}.{attr_name}"
        if cmds.objExists(attr_full_name):
            try:
                return cmds.getAttr(attr_full_name)
            except:
                return 0
        return 0
    
    def show_object_attributes(self, obj):
        """显示对象的属性编辑器"""
        self.current_selected_object = obj
        
        # 更新标题
        self.current_object_label.setText(f"当前对象: {obj}")
        
        # 清除旧的属性控件
        self.clear_attribute_widgets()
        
        # 检查对象是否有属性配置
        if obj not in self.object_attributes:
            self.initialize_object_attributes(obj)
        
        if obj in self.object_attributes:
            # 创建属性组
            self.create_attribute_groups(obj)
    
    def clear_attribute_widgets(self):
        """清除属性编辑器中的所有控件"""
        # 移除所有子控件
        while self.attr_layout.count():
            item = self.attr_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加提示标签
        if not self.current_selected_object:
            empty_label = QtWidgets.QLabel("请选择一个对象以查看和编辑属性")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #888888; padding: 20px;")
            self.attr_layout.addWidget(empty_label)
    
    def create_attribute_groups(self, obj):
        """为对象创建属性组"""
        attrs = self.object_attributes[obj]
        
        if not attrs:
            empty_label = QtWidgets.QLabel("该对象没有可编辑的属性")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #888888; padding: 20px;")
            self.attr_layout.addWidget(empty_label)
            return
        
        # 按属性类型分组
        attr_groups = {}
        for attr_name, attr_data in attrs.items():
            # 确定属性组
            group_name = "自定义属性"
            if "translate" in attr_name:
                group_name = "位移"
            elif "rotate" in attr_name:
                group_name = "旋转"
            elif "scale" in attr_name:
                group_name = "缩放"
            elif "visibility" in attr_name:
                group_name = "可见性"
            elif "blendShape" in attr_name:
                group_name = "融合变形"
            
            if group_name not in attr_groups:
                attr_groups[group_name] = []
            attr_groups[group_name].append((attr_name, attr_data))
        
        # 创建属性组
        for group_name, group_attrs in attr_groups.items():
            group_box = QtWidgets.QGroupBox(group_name)
            group_layout = QtWidgets.QVBoxLayout()
            
            for attr_name, attr_data in group_attrs:
                attr_widget = self.create_attribute_widget(obj, attr_name, attr_data)
                if attr_widget:
                    group_layout.addWidget(attr_widget)
            
            group_box.setLayout(group_layout)
            self.attr_layout.addWidget(group_box)
        
        self.attr_layout.addStretch()
    
    def create_attribute_widget(self, obj, attr_name, attr_data):
        """创建属性控件"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 属性标签
        label = QtWidgets.QLabel(attr_data.get('label', attr_name))
        label.setFixedWidth(120)
        layout.addWidget(label)
        
        # 根据类型创建不同的控件
        attr_type = attr_data.get('type', 'float')
        current_value = attr_data.get('current_value', 0)
        
        if attr_type == 'float':
            # 浮点型滑块
            slider = QtWidgets.QSlider(Qt.Horizontal)
            min_val = attr_data.get('min', 0)
            max_val = attr_data.get('max', 1)
            
            # 设置滑块范围
            slider.setRange(int(min_val * 100), int(max_val * 100))
            slider.setValue(int(current_value * 100))
            
            # 数值显示
            spinbox = QtWidgets.QDoubleSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setValue(current_value)
            spinbox.setSingleStep(0.01)
            spinbox.setDecimals(2)
            
            # 连接信号
            slider.valueChanged.connect(
                lambda v, s=spinbox: s.setValue(v / 100.0)
            )
            spinbox.valueChanged.connect(
                lambda v, s=slider, o=obj, a=attr_name: self.on_attr_value_changed(o, a, v, s)
            )
            
            layout.addWidget(slider)
            layout.addWidget(spinbox)
            
        elif attr_type == 'int':
            # 整型滑块
            slider = QtWidgets.QSlider(Qt.Horizontal)
            min_val = attr_data.get('min', 0)
            max_val = attr_data.get('max', 100)
            
            slider.setRange(min_val, max_val)
            slider.setValue(int(current_value))
            
            # 数值显示
            spinbox = QtWidgets.QSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setValue(int(current_value))
            
            # 连接信号
            slider.valueChanged.connect(spinbox.setValue)
            spinbox.valueChanged.connect(
                lambda v, s=slider, o=obj, a=attr_name: self.on_attr_value_changed(o, a, v, s)
            )
            
            layout.addWidget(slider)
            layout.addWidget(spinbox)
            
        elif attr_type == 'bool':
            # 布尔型复选框
            checkbox = QtWidgets.QCheckBox()
            checkbox.setChecked(bool(current_value))
            checkbox.stateChanged.connect(
                lambda state, o=obj, a=attr_name: self.on_attr_value_changed(o, a, state == Qt.Checked)
            )
            
            layout.addWidget(checkbox)
            layout.addStretch()
            
        elif attr_type == 'vector':
            # 向量型（三个数值）
            vector_layout = QtWidgets.QHBoxLayout()
            
            if isinstance(current_value, (list, tuple)) and len(current_value) == 3:
                for i in range(3):
                    spinbox = QtWidgets.QDoubleSpinBox()
                    spinbox.setRange(-1000, 1000)
                    spinbox.setValue(current_value[i])
                    spinbox.setSingleStep(0.1)
                    
                    spinbox.valueChanged.connect(
                        lambda v, idx=i, o=obj, a=attr_name: self.on_vector_attr_changed(o, a, idx, v)
                    )
                    
                    vector_layout.addWidget(spinbox)
            
            layout.addLayout(vector_layout)
        
        return widget
    
    def on_attr_value_changed(self, obj, attr_name, value, slider=None):
        """属性值改变时的处理"""
        try:
            # 更新Maya中的属性值
            attr_full_name = f"{obj}.{attr_name}" if "." not in attr_name else attr_name
            
            if cmds.objExists(attr_full_name):
                # 获取属性类型
                attr_type = cmds.getAttr(attr_full_name, type=True)
                
                if attr_type in ["doubleLinear", "float", "double"]:
                    cmds.setAttr(attr_full_name, float(value))
                elif attr_type == "bool":
                    cmds.setAttr(attr_full_name, bool(value))
                elif attr_type in ["long", "short", "byte"]:
                    cmds.setAttr(attr_full_name, int(value))
                
                # 更新当前值
                if obj in self.object_attributes and attr_name in self.object_attributes[obj]:
                    self.object_attributes[obj][attr_name]['current_value'] = value
                
                # 如果正在录制，应用RBF驱动
                if self.edit_mode and self.start_btn.text() == "停止录制":
                    self.apply_rbf_driver()
                    
        except Exception as e:
            print(f"设置属性值时出错: {e}")
    
    def on_vector_attr_changed(self, obj, attr_name, index, value):
        """向量属性值改变时的处理"""
        try:
            attr_full_name = f"{obj}.{attr_name}" if "." not in attr_name else attr_name
            
            if cmds.objExists(attr_full_name):
                # 获取当前向量值
                current_value = list(cmds.getAttr(attr_full_name))
                current_value[index] = value
                
                # 设置新值
                cmds.setAttr(attr_full_name, *current_value)
                
                # 如果正在录制，应用RBF驱动
                if self.edit_mode and self.start_btn.text() == "停止录制":
                    self.apply_rbf_driver()
                    
        except Exception as e:
            print(f"设置向量属性值时出错: {e}")
    
    def add_custom_attribute(self):
        """添加自定义属性"""
        if not self.current_selected_object:
            cmds.warning("请先选择一个对象")
            return
        
        obj = self.current_selected_object
        attr_name = self.attr_name_input.text().strip()
        attr_label = self.attr_label_input.text().strip()
        
        if not attr_name:
            cmds.warning("请输入属性名称")
            return
        
        if not attr_label:
            attr_label = attr_name
        
        # 检查属性是否已存在
        attr_full_name = f"{obj}.{attr_name}"
        if cmds.objExists(attr_full_name):
            cmds.warning(f"属性 {attr_name} 已存在")
            return
        
        # 获取属性类型
        attr_type_str = self.attr_type_combo.currentText()
        
        try:
            # 创建自定义属性
            if attr_type_str == "浮点型":
                min_val = self.attr_min_input.value() if self.attr_range_group.isChecked() else 0
                max_val = self.attr_max_input.value() if self.attr_range_group.isChecked() else 1
                
                cmds.addAttr(obj, ln=attr_name, at='float', min=min_val, max=max_val, dv=0)
                attr_data = {
                    'name': attr_name,
                    'label': attr_label,
                    'type': 'float',
                    'min': min_val,
                    'max': max_val,
                    'current_value': 0
                }
                
            elif attr_type_str == "整数型":
                min_val = int(self.attr_min_input.value()) if self.attr_range_group.isChecked() else 0
                max_val = int(self.attr_max_input.value()) if self.attr_range_group.isChecked() else 100
                
                cmds.addAttr(obj, ln=attr_name, at='long', min=min_val, max=max_val, dv=0)
                attr_data = {
                    'name': attr_name,
                    'label': attr_label,
                    'type': 'int',
                    'min': min_val,
                    'max': max_val,
                    'current_value': 0
                }
                
            elif attr_type_str == "布尔型":
                cmds.addAttr(obj, ln=attr_name, at='bool', dv=False)
                attr_data = {
                    'name': attr_name,
                    'label': attr_label,
                    'type': 'bool',
                    'current_value': False
                }
                
            elif attr_type_str == "向量型":
                cmds.addAttr(obj, ln=attr_name, at='float3')
                cmds.addAttr(obj, ln=f"{attr_name}X", at='float', p=attr_name)
                cmds.addAttr(obj, ln=f"{attr_name}Y", at='float', p=attr_name)
                cmds.addAttr(obj, ln=f"{attr_name}Z", at='float', p=attr_name)
                
                attr_data = {
                    'name': attr_name,
                    'label': attr_label,
                    'type': 'vector',
                    'current_value': [0, 0, 0]
                }
            
            # 设置属性为可设置关键帧
            cmds.setAttr(attr_full_name, edit=True, keyable=True)
            
            # 添加到对象属性配置
            if obj not in self.object_attributes:
                self.object_attributes[obj] = {}
            
            self.object_attributes[obj][attr_name] = attr_data
            
            # 刷新属性显示
            self.show_object_attributes(obj)
            
            self.update_status(f"已为 {obj} 添加自定义属性: {attr_label}")
            
            # 清空输入框
            self.attr_name_input.clear()
            self.attr_label_input.clear()
            
        except Exception as e:
            cmds.warning(f"添加属性失败: {str(e)}")
    
    def refresh_object_attributes(self):
        """刷新对象属性"""
        if not self.current_selected_object:
            cmds.warning("请先选择一个对象")
            return
        
        obj = self.current_selected_object
        
        # 重新初始化对象属性
        self.initialize_object_attributes(obj)
        
        # 刷新显示
        self.show_object_attributes(obj)
        
        self.update_status(f"已刷新 {obj} 的属性")
    
    def toggle_edit_mode(self, checked):
        """切换编辑模式"""
        self.edit_mode = checked
        
        if checked:
            # 进入编辑模式
            self.edit_btn.setText("编辑模式: 开启")
            self.edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #cc0000;
                    color: white;
                    font-weight: bold;
                    border: 2px solid #ff3333;
                }
            """)
            
            # 记录基准状态
            self.record_base_states()
            
            # 启用开始按钮
            self.start_btn.setEnabled(True)
            self.start_btn.setText("开始录制")
            
            self.update_status("编辑模式开启 - 已记录基准状态")
            
            # 高亮显示所有对象
            self.highlight_objects()
        else:
            # 退出编辑模式
            self.edit_btn.setText("编辑模式: 关闭")
            self.edit_btn.setStyleSheet("")
            
            # 停止录制
            self.start_btn.setChecked(False)
            self.start_btn.setText("开始录制")
            
            self.update_status("编辑模式关闭")
            
            # 恢复对象颜色
            self.restore_object_colors()
    
    def record_base_states(self):
        """记录基准状态"""
        self.base_driver_states.clear()
        self.base_driven_states.clear()
        
        # 记录驱动对象基准状态
        for obj_name, data in self.driver_objects.items():
            if cmds.objExists(obj_name):
                pos = cmds.xform(obj_name, query=True, translation=True, worldSpace=True)
                rot = cmds.xform(obj_name, query=True, rotation=True, worldSpace=True)
                scale = cmds.getAttr(obj_name + ".scale")[0]
                
                self.base_driver_states[obj_name] = {
                    'position': pos,
                    'rotation': rot,
                    'scale': scale
                }
        
        # 记录受驱动对象基准状态
        for obj_name, data in self.driven_objects.items():
            if cmds.objExists(obj_name):
                pos = cmds.xform(obj_name, query=True, translation=True, worldSpace=True)
                rot = cmds.xform(obj_name, query=True, rotation=True, worldSpace=True)
                scale = cmds.getAttr(obj_name + ".scale")[0]
                
                self.base_driven_states[obj_name] = {
                    'position': pos,
                    'rotation': rot,
                    'scale': scale
                }
    
    def toggle_recording(self):
        """开始/停止录制"""
        if not self.edit_mode:
            cmds.warning("请先开启编辑模式")
            return
            
        if self.start_btn.text() == "开始录制":
            # 开始录制
            self.start_btn.setText("停止录制")
            self.start_btn.setStyleSheet("""
                QPushButton {
                    background-color: #008800;
                    color: white;
                    font-weight: bold;
                    border: 2px solid #00aa00;
                }
            """)
            
            # 应用RBF驱动
            self.apply_rbf_driver()
            
            self.update_status("录制中... 修改驱动对象属性以影响受驱动对象")
        else:
            # 停止录制
            self.start_btn.setText("开始录制")
            self.start_btn.setStyleSheet("")
            
            # 记录新的状态
            self.record_new_states()
            
            self.update_status("录制停止 - 已记录新状态")
    
    def apply_rbf_driver(self):
        """应用RBF驱动"""
        if not self.base_driver_states or not self.base_driven_states:
            cmds.warning("未找到基准状态记录")
            return
        
        # 计算RBF权重
        self.calculate_rbf_weights()
        
        # 应用RBF驱动到受驱动对象
        for driven_name in self.driven_objects.keys():
            if not cmds.objExists(driven_name):
                continue
                
            # 获取基准位置
            base_driven_pos = self.base_driven_states[driven_name]['position']
            base_driven_rot = self.base_driven_states[driven_name]['rotation']
            
            # 计算加权平均值
            final_position = [0, 0, 0]
            final_rotation = [0, 0, 0]
            
            total_weight = 0
            for driver_name, weight in self.rbf_data['driver_weights'].items():
                if driver_name not in self.base_driver_states:
                    continue
                    
                # 获取驱动对象的当前状态
                current_pos = cmds.xform(driver_name, query=True, translation=True, worldSpace=True)
                current_rot = cmds.xform(driver_name, query=True, rotation=True, worldSpace=True)
                
                # 计算偏移
                base_pos = self.base_driver_states[driver_name]['position']
                base_rot = self.base_driver_states[driver_name]['rotation']
                
                pos_offset = [current_pos[i] - base_pos[i] for i in range(3)]
                rot_offset = [current_rot[i] - base_rot[i] for i in range(3)]
                
                # 应用权重
                weighted_pos = [pos_offset[i] * weight for i in range(3)]
                weighted_rot = [rot_offset[i] * weight for i in range(3)]
                
                # 累加
                final_position = [final_position[i] + weighted_pos[i] for i in range(3)]
                final_rotation = [final_rotation[i] + weighted_rot[i] for i in range(3)]
                total_weight += weight
            
            if total_weight > 0:
                # 平均化
                final_position = [final_position[i] / total_weight for i in range(3)]
                final_rotation = [final_rotation[i] / total_weight for i in range(3)]
                
                # 计算最终位置
                final_pos = [base_driven_pos[i] + final_position[i] for i in range(3)]
                final_rot = [base_driven_rot[i] + final_rotation[i] for i in range(3)]
                
                # 应用变换
                cmds.xform(driven_name, translation=final_pos, worldSpace=True)
                cmds.xform(driven_name, rotation=final_rot, worldSpace=True)
    
    def calculate_rbf_weights(self):
        """计算RBF权重"""
        self.rbf_data['driver_weights'].clear()
        
        if not self.driver_objects:
            return
            
        # 简单的距离权重计算
        driver_names = list(self.driver_objects.keys())
        
        # 为每个驱动对象分配初始权重
        for i, driver_name in enumerate(driver_names):
            # 基于列表顺序的简单权重分配
            weight = 1.0 / len(driver_names)
            self.rbf_data['driver_weights'][driver_name] = weight
    
    def record_new_states(self):
        """记录新的状态"""
        # 更新基准状态为当前状态
        self.record_base_states()
        
        # 更新显示
        self.update_object_display()
    
    def highlight_objects(self):
        """高亮显示对象"""
        # 驱动对象：红色高亮
        for obj_name in self.driver_objects.keys():
            if cmds.objExists(obj_name):
                cmds.setAttr(obj_name + ".overrideEnabled", 1)
                cmds.setAttr(obj_name + ".overrideRGBColors", 1)
                cmds.setAttr(obj_name + ".overrideColorRGB", 1, 0.2, 0.2)  # 红色
        
        # 受驱动对象：绿色高亮
        for obj_name in self.driven_objects.keys():
            if cmds.objExists(obj_name):
                cmds.setAttr(obj_name + ".overrideEnabled", 1)
                cmds.setAttr(obj_name + ".overrideRGBColors", 1)
                cmds.setAttr(obj_name + ".overrideColorRGB", 0.2, 1, 0.2)  # 绿色
    
    def restore_object_colors(self):
        """恢复对象颜色"""
        # 恢复驱动对象颜色
        for obj_name in self.driver_objects.keys():
            if cmds.objExists(obj_name):
                self.update_object_color(obj_name, "driver")
        
        # 恢复受驱动对象颜色
        for obj_name in self.driven_objects.keys():
            if cmds.objExists(obj_name):
                self.update_object_color(obj_name, "driven")
    
    def update_object_display(self):
        """更新对象显示"""
        # 更新驱动对象列表显示
        for i in range(self.driver_list.count()):
            item = self.driver_list.item(i)
            obj_name = self.extract_object_name(item.text())
            
            if obj_name in self.base_driver_states:
                # 添加状态信息
                pos = self.base_driver_states[obj_name]['position']
                info = f"  [位置: {pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}]"
                item.setText(obj_name + info)
        
        # 更新受驱动对象列表显示
        for i in range(self.driven_list.count()):
            item = self.driven_list.item(i)
            obj_name = self.extract_object_name(item.text())
            
            if obj_name in self.base_driven_states:
                # 添加状态信息
                pos = self.base_driven_states[obj_name]['position']
                info = f"  [位置: {pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}]"
                item.setText(obj_name + info)
    
    def reset_all(self):
        """重置所有"""
        # 重置UI状态
        self.edit_mode = False
        self.edit_btn.setChecked(False)
        self.edit_btn.setText("编辑模式: 关闭")
        self.edit_btn.setStyleSheet("")
        
        self.start_btn.setChecked(False)
        self.start_btn.setText("开始录制")
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("")
        
        # 清空数据
        self.base_driver_states.clear()
        self.base_driven_states.clear()
        self.rbf_data['driver_weights'].clear()
        self.rbf_data['driven_offsets'].clear()
        
        # 清空列表显示
        for i in range(self.driver_list.count()):
            item = self.driver_list.item(i)
            obj_name = self.extract_object_name(item.text())  # 移除状态信息
            item.setText(obj_name)
            
        for i in range(self.driven_list.count()):
            item = self.driven_list.item(i)
            obj_name = self.extract_object_name(item.text())  # 移除状态信息
            item.setText(obj_name)
        
        # 恢复对象颜色
        for obj_name in list(self.driver_objects.keys()) + list(self.driven_objects.keys()):
            if cmds.objExists(obj_name):
                cmds.setAttr(obj_name + ".overrideEnabled", 0)
        
        # 清空属性编辑器
        self.current_selected_object = None
        self.current_object_label.setText("未选中对象")
        self.clear_attribute_widgets()
        
        self.update_status("已重置全部 - 就绪")
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.setText(f"状态: {message}")
        
        # 根据消息类型设置不同颜色
        if "错误" in message or "warning" in message.lower():
            self.status_bar.setStyleSheet("background-color: #5a1a1a; padding: 5px; color: white;")
        elif "录制" in message:
            self.status_bar.setStyleSheet("background-color: #1a5a1a; padding: 5px; color: white;")
        elif "编辑模式开启" in message:
            self.status_bar.setStyleSheet("background-color: #5a1a1a; padding: 5px; color: white;")
        else:
            self.status_bar.setStyleSheet("background-color: #2d2d2d; padding: 5px; color: white;")
    
    def closeEvent(self, event):
        """关闭窗口时的清理工作"""
        # 移除Maya选择回调
        if self.selection_callback:
            try:
                om.MEventMessage.removeCallback(self.selection_callback)
            except:
                pass
        
        # 恢复所有对象的颜色覆盖
        for obj_name in list(self.driver_objects.keys()) + list(self.driven_objects.keys()):
            if cmds.objExists(obj_name):
                cmds.setAttr(obj_name + ".overrideEnabled", 0)
        
        event.accept()


def show_rbf_plugin():
    """显示RBF插件窗口"""
    # 关闭已存在的窗口
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.__class__.__name__ == "RBFDeformerPlugin":
            widget.close()
            widget.deleteLater()
    
    # 创建新窗口
    plugin_window = RBFDeformerPlugin()
    
    # 设置为Maya主窗口的子窗口
    try:
        from maya import OpenMayaUI as omui
        from shiboken2 import wrapInstance
        maya_window = omui.MQtUtil.mainWindow()
        maya_window_ptr = int(maya_window)
        maya_window = wrapInstance(maya_window_ptr, QtWidgets.QWidget)
        plugin_window.setParent(maya_window)
        plugin_window.setWindowFlags(Qt.Window)
    except:
        pass
    
    plugin_window.show()
    return plugin_window


# 创建Maya菜单项
def create_menu():
    """创建Maya菜单"""
    # 删除已存在的菜单
    if cmds.menu("RBFMenu", exists=True):
        cmds.deleteUI("RBFMenu")
    
    # 创建新菜单
    cmds.menu("RBFMenu", label="RBF工具", parent="MayaWindow")
    cmds.menuItem(label="打开RBF变形器", 
                  command="import rbf_plugin; rbf_plugin.show_rbf_plugin()",
                  parent="RBFMenu")


# 自动创建菜单
if __name__ == "__main__":
    # 直接运行时显示窗口
    plugin = show_rbf_plugin()
else:
    # 作为模块导入时创建菜单
    try:
        create_menu()
        print("RBF变形器插件 v2.0 加载成功!")
        print("功能: 属性编辑器、自定义属性、双向选中同步")
    except:
        pass