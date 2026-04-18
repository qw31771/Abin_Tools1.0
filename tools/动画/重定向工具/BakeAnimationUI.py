# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore, QtWidgets
import sys
import winreg

# path = u"//9.134.116.75/CodeVTools/ZWTools/anim_to_ADV"
# sys.path.append(path)
import maya.cmds as cmds
import BakeAnimation as ba
from imp  import  reload
reload(ba)
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class bake_Animation_UI(MayaQWidgetDockableMixin, QWidget):
    def __init__(self):
        super(bake_Animation_UI, self).__init__()
        self.initUI()
        self.SetiingUI()
        self.BakeAnimUI()
        self.RootLayoutUI()

    def initUI(self):  # 创建窗口
        try:
            cmds.deleteUI('bakeWorkspaceControl')
        except RuntimeError:
            pass
        self.setWindowTitle(u"CodeV Fbx动画转ADV")  # 设置窗口的名字
        self.resize(600, 300)
        self.setMinimumWidth(600)  # 限制最小的宽度
        self.setMinimumHeight(300)  # 限制最小的高度
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 让窗口悬浮在最上层
        #self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.setObjectName('bake')
        self.show(dockable=True)


    def SetiingUI(self):
        self.SetiingGroup = QGroupBox(self)
        self.SetiingGroup.setTitle(u"设置")
        self.BakeAnimationUI = QCheckBox(self.SetiingGroup)
        self.BakeAnimationUI.setText(u"Bake动画")
        self.BakeAnimationUI.setChecked(True)
        self.DeleteUI = QCheckBox(self.SetiingGroup)
        self.DeleteUI.setText(u"删除动画文件")
        # self.DeleteUI.setChecked(True)
        self.startTake = QLabel(self.SetiingGroup)
        self.startTake.setText(u"开始帧:")
        self.startTakeLineEdit = QLineEdit(self.SetiingGroup)
        self.EndTake = QLabel(self.SetiingGroup)
        self.EndTake.setText(u"结束帧:")
        self.EndTakeLineEdit = QLineEdit(self.SetiingGroup)
        self.ctrlCheck = QCheckBox(self.SetiingGroup)
        self.ctrlCheck.setText("脸部是否有控制器")

        self.skelttonButton = QPushButton(self.SetiingGroup)
        self.skelttonButton.setText(u"贴合源骨架")

        self.selectCtrlButton = QPushButton(self.SetiingGroup)
        self.selectCtrlButton.setText(u"选中全部控制器")

        self.toBindPose = QPushButton(self.SetiingGroup)
        self.toBindPose.setText(u"回到初始姿态")

        self.SetiingLayout = QGridLayout(self.SetiingGroup)
        self.SetiingLayout.addWidget(self.BakeAnimationUI,0,0,1,1)
        self.SetiingLayout.addWidget(self.DeleteUI,0,1,1,1)
        self.SetiingLayout.addWidget(self.ctrlCheck,0,2,1,1)
        self.SetiingLayout.addWidget(self.skelttonButton,0,3,1,1)
        self.SetiingLayout.addWidget(self.skelttonButton,2,0,1,1)
        self.SetiingLayout.addWidget(self.selectCtrlButton,2,2,1,1)
        self.SetiingLayout.addWidget(self.toBindPose,2,3,1,1)

        self.SetiingLayout.addWidget(self.startTake, 1, 0, 1, 1)
        self.SetiingLayout.addWidget(self.startTakeLineEdit, 1, 1, 1, 1)
        self.SetiingLayout.addWidget(self.EndTake, 1, 2, 1, 1)
        self.SetiingLayout.addWidget(self.EndTakeLineEdit, 1, 3, 1, 1)

        
        
        

        times = ba.GetAnimaInto()
        self.startTakeLineEdit.setText(str(times[0]))
        self.EndTakeLineEdit.setText(str(times[1]))

    def BakeAnimUI(self):
        self.bakeButoonGroup = QGroupBox(self)
        self.bakeButoonGroup.setTitle(u"传递动画")
        self.bakeButton = QPushButton(self.bakeButoonGroup)
        self.bakeButton.setText(u"执行")
        self.bakeButtonLayout = QHBoxLayout(self.bakeButoonGroup)
        self.bakeButtonLayout.addWidget(self.bakeButton)
        self.bakeButton.clicked.connect(self.Buttonevent)
        self.skelttonButton.clicked.connect(self.Tpose)
        self.selectCtrlButton.clicked.connect(self.select)
        self.toBindPose.clicked.connect(self.bindPose)


    def RootLayoutUI(self):
        self.RootLayout = QVBoxLayout(self)
        self.RootLayout.addWidget(self.SetiingGroup)
        self.RootLayout.addWidget(self.bakeButoonGroup)

    def Buttonevent(self):
        ba.bakeAnimation(bake =  self.BakeAnimationUI.isChecked(),delete = self.DeleteUI.isChecked(),take = [self.startTakeLineEdit.text(),self.EndTakeLineEdit.text()],ctrl= self.ctrlCheck.isChecked())

    def Tpose(self):
        #输入要对应的骨架根骨骼名字默认Skeleton，前缀默认Model：
        ba.matchTransSkeleton()

    def select(self):
        #选中全部控制器
        sl=cmds.ls(sl=1)
        if sl:
            ba.selectCtrl(sl[0])
        else:
            ba.selectCtrl()

    def bindPose(self):
        #选中全部控制器
        sl=cmds.ls(sl=1)
        if sl:
            ba.bindPose(sl[0])
        else:
                ba.bindPose()

