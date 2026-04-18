from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.mel as mel
 
#动态加载
from importlib import reload
import custom_ui
import MYMAYA
reload(custom_ui)
reload(MYMAYA)

class TitleBar(QWidget):
    windowMoved=Signal(QPoint)
    
    def __init__(self, parent):
        super(TitleBar,self).__init__(parent)
        self.resize(173,50)
        self.setFixedHeight(50)
        self.mPos=None
        self.offset=QPoint(10, 10)
        #获取父窗口
        self.get_parent=parent
        #按钮
        closeUrl=MYMAYA.PATH.PREFS+"/icons/close_base.png"
        closeHUrl=MYMAYA.PATH.PREFS+"/icons/close_hover.png"
        setUrl=MYMAYA.PATH.PREFS+"/icons/last_base.png"
        setHUrl=MYMAYA.PATH.PREFS+"/icons/last_hover.png"
        self.close_btn=custom_ui.PicBtn(30,closeUrl,closeHUrl,parent=self)
        self.set_btn=custom_ui.PicBtn(32,setUrl,setHUrl,parent=self)
        # self.close_btn=custom_ui.RoundBtn(radius =25, grcolor=[150,45,45],parent=self)
        # self.min_btn=custom_ui.RoundBtn(radius =20, grcolor=[70,140,0],parent=self)
        # self.max_btn=custom_ui.RoundBtn(radius =20, grcolor=[50,100,150],parent=self)
        #图标
        self.iconLable=QLabel(self)
        #添加按钮进布局
        self.hb_layout=QHBoxLayout(self)
        self.hb_layout.setSpacing(5)
        self.hb_layout.setContentsMargins(5,5,5,5)
        self.hb_layout.addWidget(self.iconLable,0,Qt.AlignLeft)
        self.hb_layout.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding,QSizePolicy.Fixed))
        # self.hb_layout.addWidget(self.min_btn,0,Qt.AlignRight)
        # self.hb_layout.addWidget(self.max_btn,0,Qt.AlignRight)
        self.hb_layout.addWidget(self.set_btn,0,Qt.AlignRight)
        self.hb_layout.addWidget(self.close_btn,0,Qt.AlignRight)
        self.hb_layout.setAlignment(Qt.AlignHCenter)
        self.setting=MYMAYA.SAVE.QSETTING
        #连接
        self.close_btn.clicked.connect(self.get_parent.close)
        self.set_btn.clicked.connect(self.runLastScript)
        # self.min_btn.clicked.connect(self.__toggleMinState)
        # self.max_btn.clicked.connect(self.__toggleMaxState)
        #最小化
        self.get_parent_width=None
        self.get_parent_high=None
        self._is_min=False

        self.get_parent.installEventFilter(self)

    def setIcon(self,icon):
        self.iconLable.setPixmap(icon.pixmap(70,50))

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar,self).enterEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        self.__toggleMaxState()

    #鼠标左键按下
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDragRegion(event.pos()):
            return
        self.mPos=event.pos()
        event.accept()
        # self.oldPosition=event.globalPos()

    #鼠标左键拖拽
    def mouseMoveEvent(self, event):
        if not self._isDragRegion(event.pos()):
            return
        if event.button() != Qt.LeftButton and self.mPos:

            self.windowMoved.emit(self.mapToGlobal(event.pos()-self.mPos)-self.offset)

        event.accept()

        # delta = QPoint(event.globalPos()-self.oldPosition)
        # self.move(self.x()+delta.x(),self.y()+delta.y())
        # self.oldPosition=event.globalPos()
    
    # 鼠标左键抬起    
    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        self.mPos=None
        event.accept()

    #切换窗口大小切换图标
    def __toggleMinState(self):
        if self.get_parent.isMaximized():
            self.get_parent.showNormal()
        else:
            self.get_parent.showMaximized()

    #窗口大小化具体操作
    def __toggleMaxState(self):
        if self._is_min:
            self.get_parent.resize(self.get_parent_width,self.get_parent_high)
            # self.get_parent.setWMagins(15)

            self._is_min=not self._is_min
        else:
            self.get_parent_width=self.get_parent.width()
            self.get_parent_high=self.get_parent.height()
            self.get_parent.resize(173,self.height())
            
            # self.get_parent.setWMagins(5)

            self._is_min=not self._is_min
        self.get_parent.showHideLayout()
    #判断移动是否超出范围
    def _isDragRegion(self,pos):
        # print( 0 < pos.x() < self.width() -20 *3)
        # return 0 < pos.x() < self.width() -20 *3
        return True
    
    def runLastScript(self):
        scritp=self.setting.value("last")
        stf=scritp[scritp.rfind("."):len(scritp)]
        if "py" in stf:
            exec(open(scritp, encoding='utf-8').read(),locals())
        else:
            mel.eval(' source \"{}\" '.format(scritp))