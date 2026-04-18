from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import MYMAYA
import os
import maya.mel as mel

class RoundBtn(QAbstractButton):
    NORMAL,HOVER,PRESS=range(3)
    clicked=Signal()

    def __init__(self,radius=None,grcolor=None,parent=None):
        super(RoundBtn,self).__init__(parent)
        self.rgb_v=grcolor   
        self._stage=self.NORMAL
        self._radius=radius
        self.setFixedSize(self._radius,self._radius)
        # self.setCheckable(True)
    def sideHint(self):
        return QSize(self._radius,self._radius)

    def __setLuminance(self,rgb):
        r,g,b=rgb

        y=((66*r+ 129 * g + 25 * b + 128) >> 8) + 16
        u=((-38*r - 74 * g +112 * b + 128) >> 8) + 128
        v=((112*r -94 *g -18 * b + 128) >> 8) + 128
        outcolor  = QColor(r,g, b)
        if self._stage == self.HOVER:
            ud_y = min(235,y + 50)
            c= ud_y -16
            d=u-128
            e=v-128

            ud_r = (298*c + 409*e + 128) >> 8
            ud_g = (298*c - 100*d - 208 *e + 128 ) >> 8
            ud_b = (298*c + 516*d + 128) >> 8
        
            outcolor =QColor(ud_r, ud_g, ud_b)
        elif self._stage == self.PRESS:
            ud_y = max(16,y + 50) 
            c= ud_y - 80
            d=u-128
            e=v-128

            ud_r = (298*c + 409*e +128) >> 8
            ud_g = (298*c - 100*d - 208 * e + 128) >> 8
            ud_b = (298*c + 516*d + 128) >>8
            outcolor = QColor(ud_r, ud_g, ud_b)
        return outcolor
    
    def set_state(self,enum):
        self._stage=enum
        self.update()

    #鼠标左键按下
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        
        self.set_state(self.PRESS)

    
    #鼠标左键抬起    
    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            self.set_state(self.HOVER)
        else:
            self.set_state(self.NORMAL)
        if event.button()==Qt.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()

    def enterEvent(self,event):
        self.set_state(self.HOVER)
        super(RoundBtn,self).enterEvent(event)
    
    def leaveEvent(self,event):
        self.set_state(self.NORMAL)
        super(RoundBtn,self).leaveEvent(event)

    def paintEvent(self,event):
        background_color=self.__setLuminance(self.rgb_v)
        pain = QPainter()
        pain.begin(self)
        pain.setPen(Qt.NoPen)
        #抗锯齿
        pain.setRenderHint(QPainter.Antialiasing)
        pain.setBrush(QBrush(background_color))
        pain.drawEllipse(QRectF(QPoint(0,0),QSizeF(self.width(),self.height())))

        pain.end()

class SliderBtn(QAbstractButton):
    clicked=Signal(bool)

    def __init__(self, **kwargs):
        u"""""
    
        :param w: 宽
        :param h: 高
        :param grcoff: 关闭状态下背景的颜色(89,89,89)
        :param grcon: 打开状态下背景的颜色(200,222,255)
        :param slcoff: 关闭状态下按钮的颜色(193,205,205)
        :param slcon: 打开状态下按钮的颜色(50,155,255)

        """""
        super(SliderBtn,self).__init__()

        self._grcolor_off=QColor(89,89,89)
        self._grcolor_on=QColor(200,222,255)

        self._slidercolor_off=QColor(193,205,205)
        self._slidercolor_on=QColor(50,155,255)

        for key in kwargs:
            if key == "w":
                self.w=kwargs.get(key)
                continue
            if key == "h":
                self.h=kwargs.get(key)
                continue
            if key == "grcoff":
                self._grcolor_off=QColor(kwargs.get(key)[0],kwargs.get(key)[1],kwargs.get(key)[2])
                continue
            if key == "grcon":
                self._grcolor_on=QColor(kwargs.get(key)[0],kwargs.get(key)[1],kwargs.get(key)[2])
                continue
            if key == "slcoff":
                self._slidercolor_off=QColor(kwargs.get(key)[0],kwargs.get(key)[1],kwargs.get(key)[2])
                continue
            if key == "slcon":
                self._slidercolor_on=QColor(kwargs.get(key)[0],kwargs.get(key)[1],kwargs.get(key)[2])
                continue
        
        # 改变布局中显示的问题，设置下面这个属性固定按键大小，或重写siezeHint方法
        self.setFixedSize(self.w,self.h)
        #self.resize(50,25)
        self._checked=False
        #内部圈直径
        self._innerDiamater=self.height()*0.75
        #内部圈与背景的边距
        self._innerMargin=(self.height()-self._innerDiamater)/2
        #x坐标的偏移值
        self._offset=self._innerMargin
        #定时器
        self._time=None
    
    def sizeHint(self):
        return QSize(self.w,self.h)
    
    def paintEvent(self,event):
        pain=QPainter()
        pain.begin(self)
        pain.setPen(Qt.NoPen)
        #抗锯齿
        pain.setRenderHint(QPainter.Antialiasing)
        #颜色状态
        if self._checked:
            grcolor=self._grcolor_on
            slidercolor=self._slidercolor_on
        else:
            grcolor=self._grcolor_off
            slidercolor=self._slidercolor_on
        
        #画个圆角矩阵
        pain.setBrush(QBrush(grcolor))
        pain.drawRoundedRect(self.rect(),self.height()/2,self.height()/2)
        
        #画个圈
        pain.setBrush(QBrush(slidercolor))
        pain.drawEllipse(QRectF(self._offset,self._innerMargin,self._innerDiamater,self._innerDiamater))

        pain.end()
    
    def timerEvent(self,event):
        if self._checked:
            self._offset+=1
            if self._offset>(self.width-self._innerDiamater-self._innerMargin):
                self.killTimer(self._time_id)
        else:
            self._offset-=1
            if self._offset<=self._innerMargin:
                self.killTimer(self._time_id)

        self.update()


    def killTimer(self,time_id):
        super(SliderBtn,self).killTimer(time_id)
        self._time_id=None
    
    def mouseReleaseEvent(self,event):
        if event.button()==Qt.LeftButton:
            self._checked = not self._checked
            self.clicked.emit(self._getChecked)      
            if self._time_id:
                self.killTimer(self._time_id)
            self._time_id=self.startTimer(5)

    def _getChecked(self):
        return self._checked      

class PicBtn(QAbstractButton):
    NORMAL,HOVER,PRESS=range(3)
    clicked=Signal()

    def __init__(self,radius=None,url=None,hoverUrl=None,parent=None):
        super(PicBtn,self).__init__(parent)
        self._stage=self.NORMAL
        self.pixmap=QPixmap(url)
        self.pixmap_hover=QPixmap(hoverUrl)
        self._radius=radius

    def sizeHint(self):
        return QSize(self._radius,self._radius)
    
    def set_state(self,enum):
        self._stage=enum
        self.update()

    #鼠标左键按下
    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        
        self.set_state(self.PRESS)
    
    #鼠标左键抬起    
    def mouseReleaseEvent(self, event):
        if self.rect().contains(event.pos()):
            self.set_state(self.HOVER)
        else:
            self.set_state(self.NORMAL)
        if event.button()==Qt.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()
    #鼠标进入
    def enterEvent(self,event):
        self.set_state(self.HOVER)
        super(PicBtn,self).enterEvent(event)
    #鼠标离开
    def leaveEvent(self,event):
        self.set_state(self.NORMAL)
        super(PicBtn,self).leaveEvent(event)

    def paintEvent(self,event):
        if self._stage == self.NORMAL:
            pix = self.pixmap
        elif self._stage == self.HOVER:
            pix = self.pixmap_hover
        elif self._stage == self.PRESS:
            pix = self.pixmap_hover

        pain = QPainter(self)
        pain.setRenderHint(QPainter.Antialiasing)

        pain.drawPixmap(event.rect(), pix)

        pain.end()

class LongTextDialog(QDialog):
    def __init__(self, text=None, parent=None):
        super(LongTextDialog, self).__init__(parent)

        with open(MYMAYA.PATH.PREFS+"/scripts/qss/LongTextDialogQSS.qss","r") as f:
            self.treeW=f.read()
        self.setStyleSheet(self.treeW)
        # 设置自定义图标
        icon_path = MYMAYA.PATH.PREFS+'/icons/重命名.png'  # 替换为你的图标文件路径
        self.setWindowIcon(QIcon(icon_path))
        # 创建一个QTextEdit用于显示或编辑长文本
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("...输入启动脚本代码")
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 创建一个按钮框，包含确定和取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    
        self.radio_button1 = QRadioButton('Mel', self)
        self.radio_button2 = QRadioButton('Python', self)
        self.radio_button1.setChecked(True)  # 默认选中选项1
        self.radio_button1.toggled.connect(lambda: self.radio_button2.setChecked(False))
        self.radio_button2.toggled.connect(lambda: self.radio_button1.setChecked(False))
        radio_box=QHBoxLayout()
        radio_box.addWidget(self.radio_button1)
        radio_box.addWidget(self.radio_button2)

        # 创建一个布局，并将控件添加到布局中
        layout = QVBoxLayout(self)
        button_box.setContentsMargins(10,10,10,10)
        # 将单选按钮添加到布局中
        layout.addLayout(radio_box)
        layout.addWidget(self.text_edit)
        layout.addWidget(button_box)

        # 设置窗口标题
        if text:
            self.setWindowTitle(" "+text)
        else:
            self.setWindowTitle('Start Code')

    #获取输入类型
    def get_type(self):
        if self.radio_button1.isChecked():
            return ".mel"
        else:
            return ".py"

    # 获取输入的文本（如果对话框被接受）
    def get_text(self):
        if self.result() == QDialog.Accepted:
            return self.text_edit.toPlainText()
        return None
 
class popMsg(QDialog):
    def __init__(self,typ, text=None, parent=None):
        super(popMsg, self).__init__(parent)

        with open(MYMAYA.PATH.PREFS+"/scripts/qss/popMsg.qss","r") as f:
            self.treeW=f.read()
        self.setStyleSheet(self.treeW)
        # 设置窗口标题
        self.setWindowTitle(" ")
        # 设置自定义图标
        icon_path = MYMAYA.PATH.PREFS+'/icons/{}.png'.format(typ)  # 替换为你的图标文件路径
        self.setWindowIcon(QIcon(icon_path))
        # 创建一个QTextEdit用于显示或编辑长文本
        self.text_edit = QLabel(self)
        self.text_edit.setText(text)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 创建一个按钮框，包含确定和取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    

        # 创建一个布局，并将控件添加到布局中
        layout = QVBoxLayout(self)
        button_box.setContentsMargins(10,10,10,10)
        # 将单选按钮添加到布局中
        layout.addWidget(self.text_edit)
        layout.addWidget(button_box)


class ClickableLabel(QLabel):
    clicked = Signal()  # 定义一个信号，用于在点击时发出

    def __init__(self,font,fontSize,text ,height,parent=None):
        super().__init__(parent)

        Toolfont=QFont(font,fontSize,True)
        self.setText(text)
        self.setStyleSheet("QLabel { color: rgb(20,20,20); }") 
        self.setFont(Toolfont)
        self.setFixedHeight(height)
        self.setMouseTracking(True)  # 启用鼠标跟踪

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 发出点击信号
        super().mousePressEvent(event)  # 调用基类的 mousePressEvent

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.setCursor(QCursor(Qt.PointingHandCursor))  # 鼠标进入时设置手形光标
        self.setStyleSheet("QLabel { color: rgb(150,50,50); }") 


    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.setCursor(QCursor(Qt.ArrowCursor))  # 鼠标离开时设置默认光标
        self.setStyleSheet("QLabel { color: rgb(20,20,20); }") 


class UpdateText(QDialog):
    def __init__(self, parent=None):
        super(UpdateText, self).__init__(parent)

        # 创建一个文本编辑器
        self.text_edit = QTextEdit(self)
        source_file=MYMAYA.PATH.TOOLPATH+"/更新日志.py"
        with open(source_file, 'r', encoding='utf-8') as source_file:
            content = source_file.read()
        self.text_edit.setPlainText(content)

        # 创建一个布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

        # 添加一个按钮用于关闭对话框（可选）
        close_button = QPushButton("关闭", self)
        update_button = QPushButton("更新", self)
        update_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(150,50,50);
                color: white;
                padding: 10px 20px;
                transition: background-color 0.3s, border-color 0.3s;
            }
            QPushButton:hover {
                background-color: darkred;  /* 悬停时改变背景颜色 */
                border-color: white;         /* 悬停时边框颜色保持白色 */
            }
            QPushButton:pressed {
                background-color: rgb(150,150,150);   /* 按下时改变背景颜色 */
            }
        """)
        close_button.clicked.connect(self.close)
        update_button.clicked.connect(self.on_update_click)
        layout.addWidget(close_button)
        layout.addWidget(update_button)

        # 设置对话框的大小和标题
        self.setWindowTitle(" 更新日志")
        self.resize(MYMAYA.MYSCREEN.getScreenPx(250), MYMAYA.MYSCREEN.getScreenPx(350))
        # 设置自定义图标
        icon_path = MYMAYA.PATH.PREFS+'/icons/{}.png'.format('更新')  # 替换为你的图标文件路径
        self.setWindowIcon(QIcon(icon_path))

    def on_update_click(self):
        mel_script_path = MYMAYA.SAVE.QSETTING.value(MYMAYA.SAVE.SOURCE)
        print(mel_script_path)
        if not os.path.isfile(mel_script_path):
            QMessageBox.warning(None, "文件未找到", f"无法找到 MEL 文件: {mel_script_path}")
            return
        mel.eval(' source \"{}\" '.format(mel_script_path))
        self.close()

        


