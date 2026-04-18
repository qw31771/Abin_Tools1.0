# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore, QtWidgets
import sys
import winreg
from imp import reload
import maya.cmds as cmds

string = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, string)
location, _type = winreg.QueryValueEx(handle, 'Personal')
# path = location + u"\maya\2022\zh_CN\scripts\对齐工具"
# sys.path.append(path)
import aligns as al

reload(al)
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class anign_UI(MayaQWidgetDockableMixin, QWidget):
    def __init__(self, ):
        super(anign_UI, self).__init__()
        self.initUI()
        self.groups()
        self.posCheck()
        self.rotCheck()
        self.scaCheck()
        self.OkButton()

    def initUI(self):  # 创建窗口
        try:
            cmds.deleteUI('alignWorkspaceControl')
        except RuntimeError:
            pass
        self.setWindowTitle(u"对齐工具")  # 设置窗口的名字
        self.resize(300, 500)
        self.setMinimumWidth(300)  # 限制最小的宽度
        self.setMinimumHeight(500)  # 限制最小的高度
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 让窗口悬浮在最上层
        # self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.setObjectName('align')
        self.show(dockable=True)

    def groups(self):
        self.posGroup = QGroupBox(self)
        self.posGroup.setTitle(u"位置对齐")
        self.rotGroup = QGroupBox(self)
        self.rotGroup.setTitle(u"旋转对齐")
        self.scaGroup = QGroupBox(self)
        self.scaGroup.setTitle(u"缩放对齐")
        self.OKGroup = QGroupBox(self)
        self.OKGroup.setTitle(u"对齐")
        self.grouplayout = QVBoxLayout(self)
        self.grouplayout.addWidget(self.posGroup)
        self.grouplayout.addWidget(self.rotGroup)
        self.grouplayout.addWidget(self.scaGroup)
        self.grouplayout.addWidget(self.OKGroup)

    def posCheck(self):
        self.posXcheck = QCheckBox(self.posGroup)
        self.posXcheck.setText(u"X_位置")
        self.posYcheck = QCheckBox(self.posGroup)
        self.posYcheck.setText(u"Y_位置")
        self.posZcheck = QCheckBox(self.posGroup)
        self.posZcheck.setText(u"Z_位置")
        self.posXcheck.setChecked(True)
        self.posYcheck.setChecked(True)
        self.posZcheck.setChecked(True)
        self.posChecklayout = QHBoxLayout(self.posGroup)
        self.posChecklayout.addWidget(self.posXcheck)
        self.posChecklayout.addWidget(self.posYcheck)
        self.posChecklayout.addWidget(self.posZcheck)

    def rotCheck(self):
        self.rotXcheck = QCheckBox(self.rotGroup)
        self.rotXcheck.setText(u"X_旋转")
        self.rotYcheck = QCheckBox(self.rotGroup)
        self.rotYcheck.setText(u"Y_旋转")
        self.rotZcheck = QCheckBox(self.rotGroup)
        self.rotZcheck.setText(u"Z_旋转")
        self.rotXcheck.setChecked(True)
        self.rotYcheck.setChecked(True)
        self.rotZcheck.setChecked(True)
        self.rotChecklayout = QHBoxLayout(self.rotGroup)
        self.rotChecklayout.addWidget(self.rotXcheck)
        self.rotChecklayout.addWidget(self.rotYcheck)
        self.rotChecklayout.addWidget(self.rotZcheck)

    def scaCheck(self):
        self.scaXcheck = QCheckBox(self.scaGroup)
        self.scaXcheck.setText(u"X_缩放")
        self.scaYcheck = QCheckBox(self.scaGroup)
        self.scaYcheck.setText(u"Y_缩放")
        self.scaZcheck = QCheckBox(self.scaGroup)
        self.scaZcheck.setText(u"Z_缩放")
        self.scaChecklayout = QHBoxLayout(self.scaGroup)
        self.scaChecklayout.addWidget(self.scaXcheck)
        self.scaChecklayout.addWidget(self.scaYcheck)
        self.scaChecklayout.addWidget(self.scaZcheck)

    def OkButton(self):
        self.OkButton = QPushButton(self.OKGroup)
        self.OkButton.setText(u"对齐")
        self.OkButtonlayout = QHBoxLayout(self.OKGroup)
        self.OkButtonlayout.addWidget(self.OkButton)
        self.OkButton.clicked.connect(self.click)

    def click(self):
        al.set_Align_target(posX=self.posXcheck.isChecked(), posY=self.posYcheck.isChecked(),
                            posZ=self.posZcheck.isChecked(),
                            rotX=self.rotXcheck.isChecked(), rotY=self.rotYcheck.isChecked(),
                            rotZ=self.rotZcheck.isChecked(),
                            scaX=self.scaXcheck.isChecked(), scaY=self.scaYcheck.isChecked(),
                            scaZ=self.scaZcheck.isChecked())


