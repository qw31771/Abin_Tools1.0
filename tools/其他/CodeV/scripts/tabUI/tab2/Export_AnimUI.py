from typing import Dict, Tuple
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import Export_AnimSettings
import AB_Maya
import maya.cmds as cmds
import saveData

class Tab_UI(QTabWidget):
    def __init__(self, parent):
        super(Tab_UI, self).__init__(parent)

        self._parent = parent.tab_widget
        self.init()
        self.settings =Export_AnimSettings.ExportSettings(self)

        self.create_connections()

    def init(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setMargin(0)
        tab.setLayout(layout)
        self._parent.addTab(tab, '动画')
        
        self.anim_layout1=QVBoxLayout()
        self.anim_layout2=QVBoxLayout()
        self.anim_layout3=QVBoxLayout()
        self.anim_layout1.setAlignment(Qt.AlignTop)
        self.anim_layout2.setAlignment(Qt.AlignTop)
        self.anim_layout3.setAlignment(Qt.AlignTop)

        layout.addLayout(self.anim_layout1, stretch=0)
        layout.addLayout(self.anim_layout2, stretch=0)
        layout.addLayout(self.anim_layout3, stretch=1)

        self.createBox1_layout()
        self.createBox2_layout()
        self.createBox3_layout()

    def createBox1_layout(self):
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10) 
        self.anim_export = QComboBox(self)
        item = ['场景选中', '表格选中']
        self.anim_export.addItems(item)

        self.joint_layout=QHBoxLayout()
        self.anim_export_jnt = QListWidget()
        self.anim_export_jnt.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.anim_skips_jnt = QListWidget()
        self.anim_skips_jnt.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.anim_skips_jnt.setFixedWidth(1)
        self.change_anims_btn=QPushButton('<')
        self.anim_skips_jnt.setFixedWidth(15)
        self.change_anims_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.joint_layout.addWidget(self.anim_export_jnt,1)
        self.joint_layout.addWidget(self.change_anims_btn,0)
        self.joint_layout.addWidget(self.anim_skips_jnt,0)

        content_layout.addWidget(self.anim_export)
        content_layout.addLayout(self.joint_layout)

        self.anim_Export_menu =AB_Maya.popWidgetMenu(" 导出 ⊿",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addLayout(self.anim_Export_menu)
        set_layout.addWidget(AB_Maya.hLine())
        self.anim_layout1.addLayout(set_layout)

    def change_Skips(self):
        if self.change_anims_btn.text() == '<':
            # 当前右侧列表是收缩的 → 展开右侧，收缩左侧
            self.anim_skips_jnt.setFixedWidth(0)          # 取消固定宽度，让它能拉伸
            self.anim_skips_jnt.setMaximumWidth(16777215) # 恢复默认最大宽度（也可以用 setMaximumWidth(9999)）
            self.anim_export_jnt.setFixedWidth(1)         # 左侧收缩
            self.change_anims_btn.setText('>')              # 箭头朝左，表示可以收起
        else:
            # 当前右侧列表是展开的 → 收缩右侧，展开左侧
            self.anim_export_jnt.setFixedWidth(0)         # 取消左侧固定宽度，恢复拉伸
            self.anim_export_jnt.setMaximumWidth(16777215)
            self.anim_skips_jnt.setFixedWidth(1)          # 右侧收起来
            self.change_anims_btn.setText('<')

    def createBox2_layout(self):
        grid = QGridLayout()
        grid.setContentsMargins(15, 0, 0, 0)

        self.anim_yd=AB_Maya.checkBox('移动到原点',True)
        self.anim_xzyy=AB_Maya.checkBox('烘焙动画',True)

        grid.addWidget(self.anim_yd, 0, 0)
        grid.addWidget(self.anim_xzyy, 0, 1)

        self.anim_zx = AB_Maya.titleComboBox('上方轴向',['Z','Y'],[20, 10, 20, 0])
        self.anim_pd = AB_Maya.titleComboBox('模式',['保存多个片段文件','将片段保存到单个文件'],[20, 10, 20, 0])
        
        content_layout = QVBoxLayout()
        content_layout.setMargin(0)
        content_layout.addLayout(grid)
        content_layout.addLayout(self.anim_zx)
        content_layout.addLayout(self.anim_pd)

        self.set_menu =AB_Maya.popWidgetMenu(" 设置 ⊿",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addLayout(self.set_menu)
        set_layout.addWidget(AB_Maya.hLine())
        self.anim_layout2.addLayout(set_layout)

    def createBox3_layout(self):
        content_layout = QVBoxLayout()
        content_layout.setSpacing(0)
        title_layout= QHBoxLayout()
        content_layout.setSpacing(20)
        name=QLabel('片段名称')
        self.all_Export=QCheckBox('')
        self.all_Export.setFixedWidth(35)
        title_layout.addWidget(name,1)
        self.add_anims_btn=AB_Maya.imgButton(30, saveData.PATH.icon + "/添加.png", "添加动画片段")
        self.delete_all_anims=AB_Maya.imgButton(30, saveData.PATH.icon + "/delete.png", "删除所有片段")
        title_layout.addWidget(self.add_anims_btn)
        title_layout.addWidget(self.all_Export)


        scroll_area = QScrollArea()
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidgetResizable(True) # 关键：让内部组件随滚动区自动调整宽度
        scroll_area.setFocusPolicy(Qt.NoFocus) # 移除虚线焦点框
        scroll_container = QWidget()
        scroll_container.setContentsMargins(0, 0, 0, 0)

        self.anims_layout = QVBoxLayout(scroll_container)
        self.anims_layout.setAlignment(Qt.AlignTop) 
        self.anims_layout.setSpacing(2)
        self.anims_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(scroll_container)
        content_layout.addLayout(title_layout)
        content_layout.addWidget(scroll_area)

        self.anim_menu =AB_Maya.popWidgetMenu(" 动画 ⊿",True,content_layout)

        self.anim_layout3.addLayout(self.anim_menu)

    def add_Anims(self):
        # 1. 创建包装容器（两排布局高度需要增加，建议 60-70）
        row_widget = QWidget()
        row_widget.setFixedHeight(100) 

        # 2. 主垂直布局（负责分出上下两排）
        main_row_layout = QVBoxLayout(row_widget)
        main_row_layout.setContentsMargins(0, 4, 0, 4)
        main_row_layout.setSpacing(2) 

        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        top_row.setContentsMargins(0, 0, 0, 0)
        name = QLineEdit()
        name.setPlaceholderText("片段名称...")
        Export=QCheckBox('')
        Export.setFixedWidth(30)
        top_row.addWidget(name,1)
        top_row.addWidget(Export,alignment=Qt.AlignRight)

        # --- 第二排：时间输入 + 功能按钮 ---
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10) 
        bottom_row.setContentsMargins(2, 0, 2, 0)
        start_label = QLabel("开始")
        start = QLineEdit()
        start.setFixedWidth(60)
        
        end_label = QLabel("结束")
        end = QLineEdit()
        end.setFixedWidth(60)

        # 弹性空间，把按钮推到右边
        bottom_row.addWidget(start_label)
        bottom_row.addWidget(start)
        bottom_row.addWidget(end_label)
        bottom_row.addWidget(end)

        # 功能按钮
        step_btn = AB_Maya.imgButton(22, saveData.PATH.icon + "/胶片.png", "将播放氛围设置为片段")
        run_btn = AB_Maya.imgButton(28, saveData.PATH.icon + "/播放.png", "播放")
        
        bottom_row.addWidget(step_btn)
        bottom_row.addWidget(run_btn)
        bottom_row.addStretch(1)
        delete_btn = AB_Maya.imgButton(30, saveData.PATH.icon + "/delete.png", "删除")
        bottom_row.addWidget(delete_btn)
        # 3. 将两排添加到主行布局
        main_row_layout.addLayout(top_row)
        main_row_layout.addLayout(bottom_row)

        # 4. 添加分割线（可选，让行与行之间更清晰）
        line = AB_Maya.hLine(1,'rgb(200,200,200)')
        self.anims_layout.addWidget(row_widget)
        self.anims_layout.addWidget(line)


    def create_connections(self):
        self.anim_Export_menu.toggle_button.clicked.connect(self.settings.save_Preset)
        self.anim_export.currentIndexChanged.connect(self.on_export_mode_changed)

        self.set_menu.toggle_button.clicked.connect(self.settings.save_Preset)

        self.anim_yd.stateChanged.connect(self.settings.save_Preset)
        self.anim_xzyy.stateChanged.connect(self.settings.save_Preset)
        self.anim_zx.combo.currentIndexChanged.connect(self.settings.save_Preset)
        self.anim_pd.combo.currentIndexChanged.connect(self.settings.save_Preset)

        self.add_anims_btn.clicked.connect(self.add_Anims)

        self.change_anims_btn.clicked.connect(self.change_Skips)
        self.anim_export_jnt.setContextMenuPolicy(Qt.CustomContextMenu)
        self.anim_skips_jnt.setContextMenuPolicy(Qt.CustomContextMenu)

        # 连接右键菜单信号
        self.anim_export_jnt.customContextMenuRequested.connect(self.on_add_skips_menu)
        self.anim_skips_jnt.customContextMenuRequested.connect(self.on_remove_skips_menu)
    
    def on_add_skips_menu(self,pos):
        """右侧列表的右键菜单：将选中项添加到左侧"""
        menu = QMenu(self)
        action = menu.addAction("添加跳过关节")
        action.triggered.connect(lambda: self.settings.add_SkipJoint(self.anim_export_jnt.selectedItems()))
        menu.exec_(self.anim_export_jnt.mapToGlobal(pos))

    def on_remove_skips_menu(self,pos):
        """左侧列表的右键菜单：同样执行从右侧移动到左侧的操作"""
        menu = QMenu(self)
        action = menu.addAction("从跳过关节中移除")
        action.triggered.connect(lambda: self.settings.remove_SkipJoint(self.anim_export_jnt.selectedItems()))
        menu.exec_(self.anim_skips_jnt.mapToGlobal(pos))

    def on_export_mode_changed(self):
        index=self.anim_export.currentIndex()
        # index 0 为 "场景选中"
        if index == 0:
            self.anim_export_jnt.clearSelection()
            self.anim_export_jnt.clearFocus()
            self.anim_export_jnt.setEnabled(False)
            self.anim_skips_jnt.clearSelection()
            self.anim_skips_jnt.clearFocus()
            self.anim_skips_jnt.setEnabled(False)
        else:
            self.anim_export_jnt.setEnabled(True)
            self.anim_skips_jnt.setEnabled(True)

        self.settings.save_Preset()

    def get_advanced_root_skeletons(self,skip_keywords):
        # 1. 获取场景中所有的骨骼节点
        all_joints = cmds.ls(type='joint', long=True) # 获取长路径
        root_skeletons = set()
        print(222222,skip_keywords)
        
        for jnt in all_joints:
            # --- 第一步：死磕关节链，找到这根链条的“最高级关节” ---
            highest_joint = jnt
            while True:
                # 只找类型为 joint 的父级
                parent_jnt = cmds.listRelatives(highest_joint, parent=True, type='joint', fullPath=True)
                if parent_jnt:
                    highest_joint = parent_jnt[0]
                else:
                    # 再往上不是关节了，到头了
                    break
            
            # 此时 highest_joint 绝对是这根链条最顶端的那个 joint 节点
            # 先拿到它的短名备用
            top_joint_name = highest_joint.split('|')[-1]

            # --- 第二步：看看这根链条顶端关节的“爹”是谁 ---
            parent_node = cmds.listRelatives(highest_joint, parent=True, fullPath=True)
            
            target_name = top_joint_name # 默认目标就是最高级关节
            
            if parent_node:
                p_name = parent_node[0].split('|')[-1]
                # 判断亲爹名字里有没有 Skeleton
                if "Skeleton" in p_name:
                    target_name = p_name # 有爹认爹（Skeleton节点）

            # --- 第三步：初步加入集合（这里先不管关键字，最后统一滤） ---
            root_skeletons.add(target_name)

        # --- 第四步：最终清算，把带跳过关键字的全部干掉 ---
        # 这一步保证了：只要名字里带 _skip，不管是 Skeleton 组还是最高级关节，统统不显示
        try:
            result = [r for r in root_skeletons if not any(k in r for k in skip_keywords)]
        except:
            result = list(root_skeletons)
        
        # --- 第五步：强制置顶 Skeleton 节点 ---
        special_node = "Skeleton"
        if cmds.objExists(special_node):
            if special_node in result:
                result.remove(special_node)
            result.insert(0, special_node)
                
        if result:
            self.anim_export_jnt.clear()
            self.anim_export_jnt.addItems(result)
        if skip_keywords:
            self.anim_skips_jnt.clear()
            self.anim_skips_jnt.addItems(skip_keywords)



        