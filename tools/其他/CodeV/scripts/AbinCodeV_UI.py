from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import Qt,QSize
from importlib import reload
from EventManager import EventManager
import AB_Maya
reload(AB_Maya)
import GeneralFunc
reload(GeneralFunc)
import ExportUI
reload(ExportUI)
import saveData
reload(saveData)
from saveData import  常用配置

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

class AdhesiveWindow(QtWidgets.QDockWidget):
    def __init__(self, parent=get_maya_main_window()):
        super(AdhesiveWindow, self).__init__(parent)
        parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.config=AB_Maya.getConfig('AB_Tool')
        self.init_ui()
        # 初始化事件管理器
        self.event_manager = EventManager()

        #创建布局
        self.create_layout()

        self.create_connections()

    def init_ui(self):
        self.setWindowTitle("Abin_CodeV")
        self.resize(450, 500)
        self.setMinimumWidth(450)
        self.setMaximumWidth(600)
        
    def create_layout(self):
        main_container = QWidget()
        self.main_layout = QVBoxLayout(main_container)
        self.main_layout.setSpacing(0)
        main_container.setContentsMargins(0, 0, 0, 0)

        self.setTopLayout()
        self.setMidLayout()
        self.setBottomLayout()

        self.setWidget(main_container)


    def setTopLayout(self):
        top_widget = QWidget()
        top_widget.setFixedHeight(120)  
        top_layout = QtWidgets.QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)  
        top_layout.setSpacing(0)  
        
        self.img_btn = QPushButton()
        url = saveData.PATH.icon+'/CodeV.png'
        pixmap = QPixmap(url).scaled(
            430,  # 初始宽度（后续会随布局自动扩展）
            110, # 初始高度（固定200）
            QtCore.Qt.KeepAspectRatioByExpanding,  # 按扩展比例缩放（保持宽高比）
            QtCore.Qt.SmoothTransformation  # 平滑缩放（避免模糊）
        )
        self.img_btn.setIcon(QIcon(pixmap))
        self.img_btn.setIconSize(pixmap.size())  # 设置图标尺寸

        self.img_btn.setStyleSheet("QPushButton { border: none; background: transparent; }")  # 去除边框并设置背景透明
        # 将图片按钮添加到顶部布局（自动铺满）
        top_layout.addWidget(self.img_btn)

        self.main_layout.addWidget(top_widget)
       
    def setMidLayout(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
        QTabBar::tab {
        width: 100px;  /* 设置标签页的宽度 */
        height: 40px; /* 设置标签页的高度 */
        font-size: 22px; /* 默认字体大小 */
        margin-right: 2px; 
        background-color: rgb(65, 59, 59);                                                               
        }
        QTabBar::tab:selected {
            font-size: 25px; /* 选中标签页的字体大小 */
            color: rgb(255,255,255)
        }
        """)
        self.tab1=GeneralFunc.Tab_UI(self.tab_widget)
        self.tab2=ExportUI.Tab_UI(self.tab_widget)
        
        try:
            self.tab_widget.setCurrentIndex(int(self.config.value(常用配置.表头.value)))
        except:
            self.save_tab_memory(0)
        self.main_layout.addWidget(self.tab_widget)


    def setBottomLayout(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(50)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFormat("准备就绪")
        AB_Maya.register_progress_bar(self.progress_bar)
        self.main_layout.addWidget(self.progress_bar)


    def closeEvent(self, event):
        """窗口关闭时注销所有事件监听"""
        if hasattr(self, 'event_manager'):
            self.event_manager.unregister_all_observers()  # 确保注销所有回调

    def create_connections(self):
        self.tab_widget.currentChanged.connect(self.save_tab_memory)
  

    def save_tab_memory(self,index):
        self.config.setValue(常用配置.表头.value,index)

def Show():
  global AbinCodeV_UI
  try:
    AbinCodeV_UI.close()
    AbinCodeV_UI.deleteLater()
  except:
    pass

  AbinCodeV_UI = AdhesiveWindow()
  AbinCodeV_UI.show()