from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

class AdhesiveWindow(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(AdhesiveWindow, self).__init__(parent)
        self.setWindowTitle("Adhesive Window")
        self.setGeometry(300, 300, 300, 200)

        # 创建一个垂直布局
        layout = QtWidgets.QVBoxLayout()

        # 添加一些控件，例如按钮和文本字段
        button1 = QtWidgets.QPushButton("Button 1")
        layout.addWidget(button1)
        text_field1 = QtWidgets.QLineEdit()
        layout.addWidget(text_field1)
        button2 = QtWidgets.QPushButton("Button 2")
        layout.addWidget(button2)
        text_field2 = QtWidgets.QLineEdit()
        layout.addWidget(text_field2)

        # 创建一个中心部件，并设置布局
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setWidget(central_widget)
        

def create_adhesive_window():
    maya_main_window = get_maya_main_window()
    adhesive_window = AdhesiveWindow(parent=maya_main_window)
    maya_main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, adhesive_window)
    adhesive_window.show()

# 在Maya中运行此脚本
create_adhesive_window()