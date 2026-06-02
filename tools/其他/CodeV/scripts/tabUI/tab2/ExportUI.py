from typing import Dict, Tuple
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.mel as mel
from importlib import reload
import Export_ModelUI
import Export_AnimUI
import ExportScript
import AB_Maya
import saveData
import os
import Export_ModelSettings
import Export_AnimSettings  
reload(Export_ModelUI)
reload(Export_AnimUI)
reload(ExportScript)
reload(Export_ModelSettings)
reload(Export_AnimSettings)
from saveData import  常用配置

class Tab_UI(QTabWidget):
    def __init__(self, parent):
        super(Tab_UI, self).__init__(parent)

        self._parent = parent
        self.scenceFile=AB_Maya.scencePath()
        self.config=AB_Maya.getConfig('AB_Tool')
        self.init()
        self.createBox1_layout()
        self.createBox2_layout()
        self.create_connections()

    def init(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        self._parent.addTab(tab, '导出')
        
        # 创建三个分组框
        self.box1 = AB_Maya.setGroupBox("路径", 20, (200, 200, 200))  
        self.box2 = AB_Maya.setGroupBox("设置", 20, (200, 200, 200))

        # 使用分割器布局
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.box1)
        splitter.addWidget(self.box2)
        splitter.setSizes([10, 220])
        
        layout.addWidget(splitter)

    def createBox1_layout(self):
        # 使用垂直布局
        layout = QVBoxLayout()
        layout.setSpacing(5)  # 减少控件间距
        layout.setContentsMargins(5, 5, 5, 5)  # 缩小边距
        # 路径输入框（允许垂直压缩）
        self.path_edit = QPlainTextEdit()
        self.path_edit.setPlaceholderText("'''请选择或输入路径'''")
        self.path_edit.setLineWrapMode(QPlainTextEdit.WidgetWidth)  # 自动换行
        self.path_edit.setWordWrapMode(QTextOption.WrapAnywhere)    # 任意位置换行
        self.path_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直滚动条
        self.path_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # 禁用水平滚动条
        self.path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        layout.addWidget(self.path_edit)
        self.path_edit.setPlainText(self.scenceFile)
        # 路径选择按钮（移除固定高度）
        self.path_btn = QPushButton("选择路径")
        self.ref_btn = QPushButton("刷新")
        self.open_btn = QPushButton("")
        icon = QIcon(saveData.PATH.icon+"/打开文件夹.png")
        self.open_btn.setIcon(icon)
        self.path_btn.setMinimumHeight(45)  # 仅设置最小高度
        self.ref_btn.setMinimumHeight(45)  # 仅设置最小高度
        self.open_btn.setMinimumHeight(45)  # 仅设置最小高度
        self.path_btn.setStyleSheet("color: rgb(0,0,0); font-size: 20px;background-color: rgb(200,200,200);font-weight: bold;")
        self.ref_btn.setStyleSheet("color: rgb(0,0,0); font-size: 20px;background-color: rgb(200,200,200);font-weight: bold;")
        self.open_btn.setStyleSheet("color: rgb(0,0,0); font-size: 20px;background-color: rgb(200,200,200);font-weight: bold;")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.path_btn,3)
        btn_layout.addWidget(self.ref_btn,1)
        btn_layout.addWidget(self.open_btn,0.7)
        layout.addLayout(btn_layout, alignment=Qt.AlignTop)  # 顶部对齐

        self.box1.setMinimumHeight(45)  # 设置合理的最小高度
        self.box1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # 组框本身可压缩
        self.box1.setLayout(layout)
    
    def createBox2_layout(self):
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
        QTabBar::tab {
        width: 80px;  /* 设置标签页的宽度 */
        height: 35px; /* 设置标签页的高度 */
        }
        QTabBar::tab {
            font-size: 17px; /* 默认字体大小 */
                                 
        }
        QTabBar::tab:selected {
            font-size: 19px; /* 选中标签页的字体大小 */
        }
        """)


        self.tab_anim=Export_ModelUI.Tab_UI(self)
        self.tab_model=Export_AnimUI.Tab_UI(self)

        try:
            self.tab_widget.setCurrentIndex(int(self.config.value(常用配置.模型_动画表头.value)))
        except:
            self.save_tab_memory(0)
        
        self.setPath()
        layout.addWidget(self.tab_widget)
        layout.setMargin(0)
        self.box2.setLayout(layout)

    def create_connections(self):
        # 连接路径选择按钮点击信号
        self.path_btn.clicked.connect(self.browse_path)
        self.ref_btn.clicked.connect(self.setPath)
        self.tab_widget.currentChanged.connect(self.setPath)
        self.open_btn.clicked.connect(lambda:os.startfile(self.path_edit.toPlainText()))
        self.tab_widget.currentChanged.connect(self.save_tab_memory)
        
    def browse_path(self):
        """打开路径选择对话框"""
        path = QFileDialog.getExistingDirectory(
            self._parent,
            "选择目录",
            QDir.homePath(),
            QFileDialog.ShowDirsOnly
        )
        if path:
            self.path_edit.setPlainText(path)
    
    def setPath(self):
        current_idx = self.tab_widget.currentIndex()
        if current_idx == 0 : 
            path=AB_Maya.scencePath()+'/FBX'
        else:
            path=AB_Maya.scencePath()+'/Anim'

        self.path_edit.setPlainText(path)

    def save_tab_memory(self,index):
        self.config.setValue(常用配置.模型_动画表头.value,index)
    