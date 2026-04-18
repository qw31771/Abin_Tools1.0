from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import os
import titlebar

#无边框
class FramelessWindow(QWidget):

    Margins =10
    RectRadius=15
    Left,Right,Top,Bottom,RightTop,RightBottom,LeftTop,LeftBottom =range(8)
    def __init__(self, parent=None):
        super(FramelessWindow,self).__init__(parent)
        self._pressed=False
        self.Direction=None
        self.minWidth=173
        self.minHeight=70
        self.setMinimumWidth(173)
        self.setMinimumHeight(70)

        self._gc=QColor(65,65,65)
        self._settings_obj=None

        #去除边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.Window |Qt.Tool)

        #背景透明
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.setContentsMargins(0,0,0,5)
        #布局
        self.Wlayout = QVBoxLayout(self,spacing=0)
        
        #预留边
        self.Wlayout.setContentsMargins(self.Margins,self.Margins,self.Margins,self.Margins)

        self.setMouseTracking(True)

    #设置标题颜色
    def setTitleColor(self,qcolor):
        self.title_bar.setAttribute(Qt.WA_StyledBackground,True)
        self.title_bar.setAutoFillBackground(True)
        palette=self.title_bar.palette()
        palette.setColor(palette.Window,qcolor)
        self._gc=qcolor
        self.title_bar.setPalette(palette)
        self.title_bar.setContentsMargins(2,2,2,2)

    #窗口初始化
    def initWin(self,path,set,size,pos):
        self._settings_obj=set
        self._sizePath=size
        self._posPath=pos

        if os.path.exists(path):
            try:
                size=QSize(self._settings_obj.value(self._sizePath))
            except:
                size=QSize(500,1000)
            try:
                pos=QPoint(self._settings_obj.value(self._posPath))
            except:
                pos=QPoint(500,500)
                
            self.setGeo(size,pos)

    #设置窗口位置大小
    def setGeo(self,size=None,pos=None):
        x,y,w,h=self.geometry().x(),self.geometry().y(),self.geometry().width(),self.geometry().height() 

        if size:
            w,h=size.width(),size.height()
        if pos:
            x,y=pos.x(),pos.y()

        self.setGeometry(x,y,w,h)

    #设置内间距
    def setWMagins(self,bord):
        self.Margins=bord
        self.Wlayout.setContentsMargins(self.Margins,self.Margins,self.Margins,self.Margins)

    #自定义icon
    def setWIcon(self,path):
        self.title_bar.setIcon(QIcon(path))

    #自定义控件
    def setWidget(self,widget,color):
        if hasattr(self,'_widget'):
            return
        self._widget=widget
        #设置默背景颜色
        grcolor=color
        self._widget.setAutoFillBackground(True)
        palette=self._widget.palette()
        palette.setColor(palette.Window,grcolor)
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)
    
    #显示隐藏
    def showHideLayout(self):
        self._widget.setVisible(not self._widget.isVisible())

    #初始化标题布局
    def initTitle(self):
        self.title_bar= titlebar.TitleBar(self)
        self.Wlayout.addWidget(self.title_bar)
        self.title_bar.windowMoved.connect(self.move)

    #自定义标题布局
    def setTitleBar(self,title_bar):
            self.title_bar.deleteLater()
            self.title_bar=title_bar
            self.title_bar.setParent(self)
            self.title_bar.raise_()

    #删除标题布局
    def deleteTitleBar(self):
        self.title_bar.deleteLater()

    #最大化
    def showMaxmized(self):
        #最大化，要减去上下左右边界
        super(FramelessWindow,self).showMaximized()
        self.layout().setContentsMargins(0,0,0,0)

    #还原
    def showNormal(self):
        super(FramelessWindow,self).showNormal()
        self.layout().setContentsMargins(
            self.Margins,self.Margins,self.Margins,self.Margins
        )
    
    def eventFilter(self,obj,event):
        if event.type() == QEvent.Enter:
            self.setCursor(Qt.ArrowCursor)
        return super(FramelessWindow,self).eventFilter(obj,event)
    
    def paintEvent(self,event): 
        super(FramelessWindow,self).paintEvent(event)
        painter=QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        BorderColor     = QColor(60, 60, 60, 180)      
        BackgroundColor = self._gc

        # painter.setBrush(QBrush(fillColor))
        # painter.drawRoundedRect(self.rect(),17,17)
        radius=self.RectRadius
        rectPath = QPainterPath() 
        height = self.height() - 8                     
        rectPath.addRoundedRect(QRectF(2, 2, self.width()-4, height), radius, radius)
        painter.setPen(QPen(BorderColor, 2, Qt.SolidLine,
                                 Qt.RoundCap, Qt.RoundJoin))
        
        painter.setBrush(BackgroundColor)
        painter.drawPath(rectPath)

        painter.end()

    #监听鼠标点击事件
    def mousePressEvent(self,event):
        super(FramelessWindow,self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos=event.pos()
            self._pressed=True

            pos=event.pos()
            xPos,yPos=pos.x(),pos.y()
            wm,hm=self.width()-self.Margins,self.height()-self.Margins

            if self.Margins < xPos < wm-5 and self.Margins < yPos < hm-5:
                self._pressed=False
        
    #监听鼠标抬起事件
    def mouseReleaseEvent(self,event):
        super(FramelessWindow,self).mouseReleaseEvent(event)
        self._pressed=False
        self.Direction=None
    
    #监听鼠标拖动事件
    def mouseMoveEvent(self,event):
        super(FramelessWindow,self).mouseMoveEvent(event)
        pos=event.pos()
        xPos,yPos=pos.x(),pos.y()
        wm,hm=self.width()-self.Margins,self.height()-self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction=None
            self.setCursor(Qt.ArrowCursor)
            return

        if   event.buttons() == Qt.LeftButton  and self._pressed:
            self._resizeWidget(pos)
            return
        
        if xPos <=self.Margins and yPos <= self.Margins:
            #左上
            self.Direction = self.LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm-5<=xPos<=self.width()+3 and hm-5 <=yPos<=self.height()+3:
            #右下
            self.Direction=self.RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm<=xPos and yPos<= self.Margins:
            #右下
            self.Direction=self.RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos<=self.Margins and hm <=yPos:
            #左下
            self.Direction=self.LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0<= xPos<=self.Margins and self.Margins <= yPos<=hm:
            #左
            self.Direction=self.Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm<=xPos<=self.width() and self.Margins<= yPos < hm:
            #右
            self.Direction=self.Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.Margins<=xPos<=wm and 0<=yPos<=self.Margins:
            #上
            self.Direction=self.Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <=xPos<=wm and hm<=yPos<=self.height():
            #下
            self.Direction=self.Bottom
            self.setCursor(Qt.SizeVerCursor)
            
    #根据鼠标位置设置大小
    def _resizeWidget(self,pos):
        if self.Direction == None:
            return

        mpos=pos-self._mpos
        xPos,yPos=mpos.x(),mpos.y()
        geometry = self.geometry()
        x,y,w,h=geometry.x(),geometry.y(),geometry.width(),geometry.height()     

        if self.Direction == self.LeftTop: #左上
            if w-xPos>self.minimumWidth():
                x+=xPos
                w-=xPos
            if h-yPos>self.minimumHeight(): 
                y+=yPos
                h-=yPos
        elif self.Direction == self.RightBottom: #右下
            if w+xPos>self.minimumWidth():
                w+=xPos
                self._mpos=pos
            if h+yPos>self.minimumHeight():
                h+=yPos
                self._mpos=pos
        elif self.Direction == self.RightTop: #右上
            if h-yPos>self.minimumHeight():
                y+=yPos
                h-=yPos
            if w+xPos>self.minimumWidth():
                w+=xPos
                self._mpos.setX(pos.x())
        elif self.Direction == self.LeftBottom:#左下
            if w-xPos>self.minimumWidth():
                x+=xPos
                w-=xPos
            if h+yPos>self.minimumHeight():
                h+=yPos
                self._mpos.setY(pos.y())
        elif self.Direction == self.Left:#左
            if w-xPos>self.minimumWidth():
                x+=xPos
                w-=xPos
            else:
                return
        elif self.Direction == self.Right:#右
            if w+xPos>self.minimumWidth():
                w+=xPos
                self._mpos=pos
            else:
                return
        elif self.Direction == self.Top:#上
            if h- yPos>self.minimumHeight():
                y+=yPos
                h-=yPos

            else:
                return
        elif self.Direction == self.Bottom:#下
            if h+yPos>self.minimumHeight():
                h+=yPos
                self._mpos=pos
            else:
                return
        self.setGeometry(x,y,w,h)

    # 监听关闭事件
    def closeEvent(self, event):
        if not self._settings_obj:
            return
        if not self.title_bar._is_min:
                self._settings_obj.setValue(self._sizePath, self.size())
                self._settings_obj.setValue(self._posPath, self.pos())
        else:
                self._settings_obj.setValue(self._posPath, self.pos())

           