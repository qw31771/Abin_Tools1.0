from typing import Dict, Tuple
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from importlib import reload
import saveData
import matchTransform
reload(matchTransform)
import AB_Maya

class Tab_UI(QTabWidget):
    def __init__(self, parent):
        super(Tab_UI,self).__init__(parent)

        self._parent=parent
        self.checkbox_groups: Dict[str, Dict[str, QCheckBox]] = {}  # 存储所有复选框
        self.init()
        # self.create_layout()
        # self.create_connections()

    def init(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)  # 直接将布局关联到tab，减少层级
        layout.setContentsMargins(0, 0, 0, 0)  # 消除布局默认边距
        layout.setSpacing(0)  # 消除子部件间距
        # tab.setLayout(layout)
        self._parent.addTab(tab, '通用')
        self.box1=AB_Maya.setGroupBox("对齐",20,(255,15,15))
        self.box2=AB_Maya.setGroupBox("",20,(255,15,15))
        self.box3=AB_Maya.setGroupBox("",20,(255,15,15))

        layout.addWidget(self.box1, stretch = 1)
        layout.addWidget(self.box2, stretch = 2)
        layout.addWidget(self.box3, stretch = 3)
        
    
    def create_layout(self):
       box1_layout = QVBoxLayout()
       t_lay,self.t_btn=self.set_MatBox(["位移X","位移Y","位移Z"],H=1)
       r_lay,self.r_btn=self.set_MatBox(["旋转X","旋转Y","旋转Z"],H=1)
       s_lay,self.s_btn=self.set_MatBox(["缩放X","缩放Y","缩放Z"],H=1)
       box1_layout.addLayout(t_lay)
       box1_layout.addLayout(r_lay)
       box1_layout.addLayout(s_lay)
       self.all_btn=QPushButton("匹配全部变化")
       box1_layout.addWidget(self.all_btn)
       self.box1.setLayout(box1_layout)
       
       

    def create_connections(self):
        self.all_btn.clicked.connect(matchTransform.all_Match)
        self.t_btn.clicked.connect(lambda:self.getMatBoxVis("位移"))
        self.r_btn.clicked.connect(lambda:self.getMatBoxVis("旋转"))
        self.s_btn.clicked.connect(lambda:self.getMatBoxVis("缩放"))

    
    def set_MatBox(self,data,H=0,V=0)-> Tuple[QVBoxLayout, QPushButton]:
        if H+V==0 or H+V==2:
          return None,None
        if H:
          lay=QHBoxLayout()
        else:
          lay=QVBoxLayout()

        items={}
        name = data[0].split('X')[0]  # 获取组名，如 "位移", "旋转", "缩放"
        values=saveData.DQ.SETTING.value(name)
        for i in range(len(data)):
          try:
            if values[i] == "True":
              value=True
            else:
              value=False
          except:
            value=True

          
          item=data[i]
          checkbox=QCheckBox(item,checked=value)
          items[item] = checkbox
          lay.addWidget(checkbox)

        btn=QPushButton("匹配")
        lay.addWidget(btn)

        self.checkbox_groups[name] = items

        return lay,btn


    def getMatBoxVis(self,name):
        from tools.其他.CodeV.scripts.tabUI.tab1.matchTransform import att_Mtch
        """处理匹配按钮点击事件，显示指定组的所有复选框的可见性"""
        if name not in self.checkbox_groups:
            print(f"未找到名称为 '{name}' 的复选框组。")
            return
        
        items=[]
        for checkbox_name, checkbox in self.checkbox_groups[name].items():
            check = checkbox.isChecked()
            items.append(check)
            
        att_Mtch(name,items)

