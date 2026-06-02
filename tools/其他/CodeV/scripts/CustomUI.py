from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

def setGroupBox(title="",size=16,color=(255,255,255))-> QGroupBox:
    box=QGroupBox(title)
    box.setStyleSheet(f"QGroupBox {{ font-size: {size}px; color: rgb{color}; }}")
    return box

class ImageButton(QPushButton):
    def __init__(self, size, url, tips="",parent=None):
        """
        初始化 ImageButton。

        :param size: 按钮的大小（宽度和高度相同）
        :param url: PNG 图片的路径
        :param parent: 父控件
        """
        super().__init__(parent)
        self.setIcon(QIcon(url))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")  # 去除边框并设置背景透明
        self.setToolTip(tips)  # 设置提示文本
        self._pressed = False
        self._hovered = False  # 新增属性，用于跟踪鼠标是否悬停

    def paintEvent(self, event):
        """
        重写 paintEvent 以实现自定义绘制，包括按下和悬停效果。
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 获取当前图标
        icon = self.icon()
        if icon.isNull():
            return

        # 开始绘制图标
        painter.save()
        
        # 根据状态调整透明度
        if self._pressed:
            painter.setOpacity(0.3)  # 按下时半透明
        elif self._hovered:
            painter.setOpacity(1.0)  # 悬停时半透明
        else:
            painter.setOpacity(0.7)   # 正常状态不透明

        # 绘制图标
        icon.paint(painter, self.rect(), Qt.AlignCenter)
        
        painter.restore()

    def mousePressEvent(self, event):
        """
        处理鼠标按下事件。
        """
        self._pressed = True
        self.update()  # 触发重绘
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        处理鼠标释放事件。
        """
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        """
        处理鼠标进入按钮区域事件。
        """
        self._hovered = True
        self.update()  # 触发重绘
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        处理鼠标离开按钮区域事件。
        """
        self._hovered = False
        self.update()
        super().leaveEvent(event)

class popWidgetMenu(QHBoxLayout):
    def __init__(self,title,vis,content,parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setMargin(0)
        self.addLayout(layout)

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("""
            QToolButton { 
                border: none; 
                background-color: rgb(220,220,220); 
                font-size: 19px;
                font-weight: bold;
                color: rgb(30,40,50); 
            }
                                         
        """)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setFixedHeight(33)
        self.toggle_button.clicked.connect(self.toggle_geometry_settings)
        


        self.geometry_content = QWidget()
        self.setVis_ChageArrow(vis)

        self.geometry_content.setLayout(content)
        
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.geometry_content)


    def toggle_geometry_settings(self):
        """切换几何体设置面板的显示状态"""
        is_visible = not self.geometry_content.isVisible()
        self.geometry_content.setVisible(is_visible)
        
        # 更新箭头方向
        arrow = Qt.DownArrow if is_visible else Qt.RightArrow
        self.toggle_button.setArrowType(arrow)
    
    def setVis_ChageArrow(self,vis):
        self.geometry_content.setVisible(vis)  # 初始显示

        arrow = Qt.DownArrow if vis else Qt.RightArrow 
        self.toggle_button.setArrowType(arrow)


class Line(QFrame):
    def __init__(self,px,color='rgb(0,0,0)',parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)  # 设置为水平线
        self.setStyleSheet(f"background-color: {color};")  # 设置线条颜色为黑色
        self.setFixedHeight(px)

class titleComboBox(QHBoxLayout):
    def __init__(self,title,menu,margins,parent=None):
        super().__init__(parent)
        self.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        label = QLabel(title)
        label.setStyleSheet("font-weight: bold;")
        self.combo = QComboBox()
        self.combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 设置水平扩展
        item=menu
        self.combo.addItems(item)
        self.addWidget(label)
        self.addWidget(self.combo)


class titleTextEdit(QHBoxLayout):
    def __init__(self,height,title,pht,margins,edit=True,parent=None):
        super().__init__(parent)
        self.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        self.textE = QTextEdit()
        self.textE.setFixedHeight(height)
        self.textE.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 设置水平扩展
        self.textE.setPlaceholderText(pht)
        if not edit:
            self.textE.setTextInteractionFlags(Qt.NoTextInteraction)  # 禁止选择
            self.textE.setFocusPolicy(Qt.NoFocus)
        if title:
            label = QLabel(title)
            label.setStyleSheet("font-weight: bold;")
            self.addWidget(label)
        self.addWidget(self.textE)

def scaled_size(size):
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        base_width = 3840
        base_height = 2160
        width_ratio = screen_size.width() / base_width
        height_ratio = screen_size.height() /base_height

        return int(size * min(width_ratio, height_ratio))

class checkBox(QCheckBox):
    def __init__(self,name,checked,text_color=None,parent=None):
        super().__init__(parent)
        self.setText(name)
        self.setChecked(checked) 
        font = self.font()
        font.setBold(True)
        self.setFont(font)
        if text_color:
            self.setStyleSheet(f"color: rgb{text_color};")

def get_all_item_texts(obj:QComboBox):
    """获取QComboBox中所有选项的文本"""
    map={}
    name=obj.objectName()
    currentName=obj.currentText()
    item_texts = []
    for index in range(obj.count()):  # count() 返回总项数
        item_text = obj.itemText(index)  # 获取指定索引的文本
        item_texts.append(item_text)
    
    map['name']=name
    map['currentName']=currentName
    map['items']=item_texts
    return map