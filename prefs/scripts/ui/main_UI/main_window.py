from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


#动态加载
from importlib import reload
import custom_ui
reload(custom_ui)

import MYMAYA
reload(MYMAYA)

import treeWidgetUI
reload(treeWidgetUI)

import titlebar
reload(titlebar)

import treeWidgetScript
reload(treeWidgetScript)

import frameless_win
# reload(frameless_win)

import start_loadScript
reload(start_loadScript)

def maya_main_window():
  main_window_ptr = omui.MQtUtil.mainWindow()
  return wrapInstance(int(main_window_ptr), QWidget)
# (229,160,80)
#(80,160,170)
mainWinColor=QColor(210,210,210)
titleColor=QColor(210,210,210)
mainLaout=(MYMAYA.MYSCREEN.getScreenPx(10),MYMAYA.MYSCREEN.getScreenPx(10),MYMAYA.MYSCREEN.getScreenPx(10),MYMAYA.MYSCREEN.getScreenPx(5))

#主布局-开始和结尾
class MainWidget(QWidget):

    def __init__(self, parent=None):
        super(MainWidget,self).__init__(parent)

        # self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.main_layout=None
        self.sub_layout=None
        self.create_widgets()
        self.create_layouts()

    #控件
    def create_widgets(self):
        
        self.titleLine = QFrame()
        self.titleLine.setFrameShape(QFrame.HLine)
        self.titleLine.setLineWidth(2)

        font=QFont("幼圆",11,False)
        self.serch=QLineEdit(self)
        self.serch.setFont(font)
        self.serch.setFixedHeight(41)
        self.serch.setPlaceholderText("输入插件关键词..")

        
        # Toolfont=QFont("Terminal",15,True)
        # self.toolMassage=QLabel("By: Abin | V_1.0")
        # self.toolMassage.setStyleSheet("QLabel { color: rgb(255,255,255); }") 
        # self.toolMassage.setFont(Toolfont)
        # self.toolMassage.setFixedHeight(18)
        self.toolMassage=custom_ui.ClickableLabel("Terminal",15,"By: Abin | V_1.1.5",18,parent=self)
        self.toolMassage.clicked.connect(self.show_update_dialog)

        # self.subScrollArea=QScrollArea(self)

    def addLayout(self,widget):
        self.sub_layout.addWidget(widget)
   
    def create_layouts(self): 
       #主布局
        self.main_layout=QVBoxLayout(self)
        self.main_layout.setContentsMargins(mainLaout[0],mainLaout[1],mainLaout[2],mainLaout[3])


        serchLaout=QVBoxLayout(self)
        # serchLaout.addWidget(self.titleLine)
        serchLaout.addWidget(self.serch)
        serchLaout.setContentsMargins(10,0,10,10)

        titleLayout=QVBoxLayout(self)
        titleLayout.addWidget(self.titleLine)
        titleLayout.addLayout(serchLaout)

        self.main_layout.addLayout(titleLayout)

        #次布局
        self.sub_layout=QVBoxLayout(self)
        self.g_layout=QVBoxLayout(self)
        self.sub_layout.setContentsMargins(5,MYMAYA.MYSCREEN.getScreenPx(10),5,0)
        self.g_layout.addWidget(self.toolMassage)

        self.main_layout.addLayout(self.sub_layout)

        self.main_layout.addLayout(self.g_layout)


        wid=subWidget(self)
        self.connect(self.serch, SIGNAL("returnPressed()"), lambda:wid.searchText(self.serch.text()))

    def show_update_dialog(self):
        # 创建一个 LongTextDialog 实例，并显示对话框
        dialog = custom_ui.UpdateText(self)
        dialog.exec_()
                
    def paintEvent(self, event):
        super(MainWidget,self).paintEvent(event)
        BorderColor     = QColor(0, 0, 0, 0)     
        BackgroundColor = mainWinColor

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)   

        rectPath = QPainterPath()                      
        height = self.height() - 8                     
        rectPath.addRoundedRect(QRectF(2, 2, self.width()-4, height), 15, 15)
        painter.setPen(QPen(BorderColor, 2, Qt.SolidLine,
                                 Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(BackgroundColor)
        painter.drawPath(rectPath)
        painter.setPen(QPen(BackgroundColor, 2,
                                 Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.end()

    
        
#次布局- 中间内容布局
class subWidget(QWidget):
    def __init__(self, parent=None):
        super(subWidget,self).__init__(parent)

        self.setContentsMargins(0,0,0,0)
        parent.addLayout(self)  
        self.tree_weight=None
        self.create_widgets()
        self.create_layouts()
    
    def create_widgets(self):
        self.tree_weight=treeWidgetUI.MainTreeWidget(self)

    def create_layouts(self):
        self.main_layout=QVBoxLayout(self)
        self.main_layout.setContentsMargins(3,0,2,5)
        self.main_layout.addWidget(self.tree_weight)

    def searchText(self,text):
        self.tree_weight.searchFile(text)


    # def getTreeList(self):
    #     child :MYMAYA.ToolWinMsg= []
    #     tree:QTreeWidgetItem=self.tree_weight.invisibleRootItem()
    #     signal_count = tree.childCount()
    #     for i in range(signal_count):
    #         signal = tree.child(i)
    #         name=signal.text(0).strip()
    #         msg:MYMAYA.ToolWinMsg={'name':name,'index':i,'icon':(name+".png")}
    #         child.append(msg)
        
    #     return(child)

    def paintEvent(self, event):
        super(subWidget,self).paintEvent(event)
        BorderColor     = QColor(40, 40, 40, 255)     
        BackgroundColor = QColor(40, 40, 40, 255)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)   

        rectPath = QPainterPath()                      
        height = self.height() - 8                     
        rectPath.addRoundedRect(QRectF(2, 2, self.width()-4, height), 10, 10)
        painter.setPen(QPen(BorderColor, 2, Qt.SolidLine,
                                 Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(BackgroundColor)
        painter.drawPath(rectPath)
        painter.setPen(QPen(BackgroundColor, 2,
                                 Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        painter.end()


class MainFLWin(frameless_win.FramelessWindow):
    def __init__(self, parent=maya_main_window()):
        super(MainFLWin,self).__init__(parent)


        self.setWindowTitle("ABin_Tools")
        url=MYMAYA.PATH.PREFS+"/icons/abin_icon.png"
        
        width=(447*MYMAYA.MYSCREEN.WIDTH)/3840
        height = (665*MYMAYA.MYSCREEN.HEIGHT)/2160 
        print(width,height)

        self.resize(width, height)
        
        self.initTitle()
        
        self.setWidget(widget=MainWidget(self),color=mainWinColor)
        self.initWin(MYMAYA.SAVE.WIN_INFO,MYMAYA.SAVE.QSETTING,MYMAYA.SAVE.WIN_SIZE,MYMAYA.SAVE.WIN_POS)

        self.setWIcon(url)
        self.setTitleColor(titleColor)
        self.title_bar.raise_()

        
#显示
def Show():
  global AbinTools_UI
  try:
    AbinTools_UI.close()
    AbinTools_UI.deleteLater()
  except:
    pass

  AbinTools_UI = MainFLWin()
  AbinTools_UI.show()    