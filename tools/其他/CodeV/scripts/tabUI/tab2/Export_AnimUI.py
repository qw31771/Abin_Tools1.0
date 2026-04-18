from typing import Dict, Tuple
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import saveData
import AB_Maya

class Tab_UI(QTabWidget):
    def __init__(self, parent):
        super(Tab_UI, self).__init__(parent)

        self._parent = parent.tab_widget
        self.init()
        self.createBox1_layout()
    
    def init(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        self._parent.addTab(tab, '动画')
        
        # 创建三个分组框
        self.box1 = AB_Maya.setGroupBox("", 20, (200, 200, 200))  
        self.box2 = AB_Maya.setGroupBox("设置", 20, (200, 200, 200))

        # 使用分割器布局
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.box1)
        splitter.addWidget(self.box2)
        splitter.setSizes([5, 350])
        
        layout.addWidget(splitter)
    
    def createBox1_layout(self):
        layout = QVBoxLayout()

        set_layout=QHBoxLayout()
        set_layout.setSpacing(2)
        combo_box = QComboBox(self)
        combo_box.setMinimumHeight(35)
        item=['默认设置']
        combo_box.addItems(item)
        addBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/add.png","添加预设")
        renameBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/rename.png","重命名")
        deleteBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/delete.png","删除预设")
        set_layout.addWidget(combo_box)
        set_layout.addWidget(addBtn)
        set_layout.addWidget(renameBtn)
        set_layout.addWidget(deleteBtn)


        model_layout=QHBoxLayout()
        model_layout.setSpacing(5)
        model_box = QComboBox(self)
        model_box.setMinimumHeight(35)
        item=['导出当前选择','导出全部','_LOD']
        model_box.addItems(item)
        addSetsBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/addSets.png","添加集合")
        model_layout.addWidget(model_box)
        model_layout.addWidget(addSetsBtn)

        remove_layout=QHBoxLayout()
        remove_layout.setSpacing(5)
        remove_lab=QLabel('删除关键词:')
        remove_lab.setFixedSize(93,35)
        remove_box = QComboBox(self)
        remove_box.setMinimumHeight(35)
        item=['_LOD0']
        remove_box.addItems(item)
        outKeyBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/outKey.png","添加剔除关键词")
        outKeyRemoveBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/delete.png","删除关键词")
        remove_layout.addWidget(remove_lab)
        remove_layout.addWidget(remove_box)
        remove_layout.addWidget(outKeyBtn)
        remove_layout.addWidget(outKeyRemoveBtn)

        
        layout.addLayout(set_layout,alignment=Qt.AlignTop)
        layout.addLayout(model_layout,alignment=Qt.AlignTop)
        layout.addLayout(remove_layout,alignment=Qt.AlignTop)
        self.box1.setLayout(layout)
        
    def createBox2_layout(self):
        set_layout=QHBoxLayout()
        set_layout
        title=QLabel('设置')
        # 设置字体大小为30
        title.setStyleSheet("font-size: 30px;"
                            "color: rgb;"
                            )
        lockBtn=AB_Maya.imgButton(45,saveData.PATH.icon+"/addSets.png","添加集合")

        set_layout.addWidget(title)
        # 添加可伸缩的空间
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        set_layout.addItem(spacer)

        # 添加按钮到右侧
        set_layout.addWidget(lockBtn)

        self.laout2.addLayout(set_layout,alignment=Qt.AlignTop)