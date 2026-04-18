# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore, QtWidgets
import sys
import winreg
import os
import maya.mel as mel

path = u"//9.134.116.75/CodeVTools/ZWTools/anim_to_ADV"
sys.path.append(path)
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
        self.setRefUI()

        self.BakeAnimUI()
        self.RootLayoutUI()

    def initUI(self):  # 创建窗口
        try:
            cmds.deleteUI('bakeWorkspaceControl')
        except RuntimeError:
            pass
        self.setWindowTitle(u"CodeV Fbx动画转ADV")  # 设置窗口的名字
        self.resize(700, 500)
        self.setMinimumWidth(700)  # 限制最小的宽度
        self.setMinimumHeight(500)  # 限制最小的高度
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 让窗口悬浮在最上层
        #self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.setObjectName('bake')
        self.show(dockable=True)
        scenceFile=mel.eval("file -q -location")
        currentPath=os.path.split((scenceFile))[0]
        self.path=currentPath
        
        self.fbxPath=self.path

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
        self.ctrlCheck.setChecked(1)
        self.skelttonButton = QPushButton(self.SetiingGroup)
        self.skelttonButton.setText(u"贴合源骨架")

        self.selectCtrlButton = QPushButton(self.SetiingGroup)
        self.selectCtrlButton.setText(u"选中全部控制器")

        self.toBindPose = QPushButton(self.SetiingGroup)
        self.toBindPose.setText(u"回到初始姿态")

        self.toStart = QPushButton(self.SetiingGroup)
        self.toStart.setText(u"目标尾帧  > > > >  当前首帧")

        self.toEnd = QPushButton(self.SetiingGroup)
        self.toEnd.setText(u"目标首帧  > > > >  当前尾帧")

        self.toStart.clicked.connect(lambda:self.bakeStartOrEnd(0))
        self.toEnd.clicked.connect(lambda:self.bakeStartOrEnd(1))

        self.prefixGroup = QGroupBox(self.SetiingGroup)
        self.prefixGroup.setTitle(u"前缀选项")
        self.defaultPrefixRadio = QRadioButton(self.prefixGroup)
        self.defaultPrefixRadio.setText(u"默认")
        self.selectedPrefixRadio = QRadioButton(self.prefixGroup)
        self.selectedPrefixRadio.setText(u"选中")
        self.defaultPrefixRadio.setChecked(1)  # 默认选中默认anim

        prefixLayout = QHBoxLayout(self.prefixGroup)
        prefixLayout.addWidget(self.defaultPrefixRadio)
        prefixLayout.addWidget(self.selectedPrefixRadio)

        self.SetiingLayout = QGridLayout(self.SetiingGroup)
        self.SetiingLayout.addWidget(self.BakeAnimationUI,0,0,1,1)
        self.SetiingLayout.addWidget(self.DeleteUI,0,1,1,1)
        self.SetiingLayout.addWidget(self.ctrlCheck,0,2,1,1)
        self.SetiingLayout.addWidget(self.skelttonButton,0,3,1,1)

        self.SetiingLayout.addWidget(self.startTake, 1, 0, 1, 1)
        self.SetiingLayout.addWidget(self.startTakeLineEdit, 1, 1, 1, 1)

        self.SetiingLayout.addWidget(self.startTake, 1, 0, 1, 1)
        self.SetiingLayout.addWidget(self.EndTake, 1, 2, 1, 1)
        self.SetiingLayout.addWidget(self.EndTakeLineEdit, 1, 3, 1, 1)

        self.SetiingLayout.addWidget(self.skelttonButton,2,0,1,1)
        self.SetiingLayout.addWidget(self.selectCtrlButton,2,1,1,1)
        self.SetiingLayout.addWidget(self.toBindPose,2,2,1,1)
        self.SetiingLayout.addWidget(self.prefixGroup,2,3,1,1)

        self.SetiingLayout.addWidget(self.toStart, 3, 0, 1, 2)
        self.SetiingLayout.addWidget(self.toEnd, 3, 2, 1, 4)

        
        
        

        times = ba.GetAnimaInto()
        self.startTakeLineEdit.setText(str(times[0]))
        self.EndTakeLineEdit.setText(str(times[1]))

    def setRefUI(self):
        self.referenceGroup = QGroupBox(self)
        self.referenceGroup.setTitle(u"引用")

        self.batchImportCheck = QCheckBox(self.referenceGroup)
        self.batchImportCheck.setText(u"批量引用")
        self.batchImportCheck.setChecked(1)
        self.batchImportCheck.stateChanged.connect(self.toggle_batch_import)
        


        self.hintLabel = QLabel(self.referenceGroup)
        self.hintLabel.setText(u"请选择文件夹，默认当前文件中的FBX文件")
        self.hintLabel.setStyleSheet("color: red;")

        self.fbxPathLineEdit = QLineEdit(self.referenceGroup)
        if not self.path:
            path=("默认FBX文件夹不存在-----------选择文件夹")
        else:
            path=self.fbxPath+"/FBX"
        self.fbxPathLineEdit.setText(path)

        self.browseButton = QPushButton(self.referenceGroup)
        self.browseButton.setText(u"浏览...")
        self.browseButton.clicked.connect(self.searchForFiles)

        self.importButton = QPushButton(self.referenceGroup)
        self.importButton.setText(u"引用")
        self.importButton.clicked.connect(self.referenceFiles)

        self.openFiletButton = QPushButton(self.referenceGroup)
        self.openFiletButton.setText(u"打开文件")
        self.openFiletButton.clicked.connect(self.openFile)

        referenceLayout = QGridLayout(self.referenceGroup)

         # 第一行：批量引用和提示文本
        referenceLayout.addWidget(self.batchImportCheck, 0, 0, 1, 1)
        referenceLayout.addWidget(self.hintLabel, 0, 1, 1, 4)
        
        # 第二行：路径相关控件
        referenceLayout.addWidget(self.fbxPathLineEdit, 1, 0, 1, 4)  # 路径显示占3格
        referenceLayout.addWidget(self.browseButton, 1, 4, 1, 1)
        
        # 第三行：引用按钮
        referenceLayout.addWidget(self.importButton, 2, 0, 1, 4)
        referenceLayout.addWidget(self.openFiletButton, 2, 4, 1, 1)

        self.batchImportCheck.setChecked(0)

    def openFile(self):
        path=self.fbxPathLineEdit.text()
        isFbx=path.find('.')
        if isFbx>=0:
            path=path[0:path.rfind('/')]
        
        os.startfile(path)

        

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
        self.RootLayout.addWidget(self.referenceGroup)
        self.RootLayout.addWidget(self.bakeButoonGroup)


    def searchForFiles(self):    
        multipleFilters = "All Files (*.ma *.mb *.FBX);;Maya Files (*.ma *.mb);;FBX (*.FBX);;"
        
        title="选择引用"

        typ=2 if self.batchImportCheck.isChecked() == True else 1
        

        #地址选择
        filepath = cmds.fileDialog2(fileFilter=multipleFilters,
                                    dialogStyle=1, fileMode=typ, returnFilter=True,cap=title,dir=self.fbxPath,okc="保存")
        
        # print(filepath[0])
        #将所选择的地址填入
        if filepath:
            self.fbxPathLineEdit.setText(filepath[0])
            self.fbxPath=filepath[0]
            self.path=filepath[0]
            print(filepath[0])
    
    def toggle_batch_import(self,state):
      

        if state == QtCore.Qt.Checked:
            self.hintLabel.setText(u"请选择文件夹，默认当前文件中的FBX文件")  # 设置初始文本
            
        else:
            self.hintLabel.setText(u"请选择文件，默认当前文件中的最新文件")  # 设置初始文本

        if not self.path:
            return
        
        temp=self.fbxPathLineEdit.text()
        isFbx=temp.find('.')
        if isFbx>=0:
            path=temp[0:temp.rfind('/')]
        else:
            path=temp
            


        if state == QtCore.Qt.Checked:
            self.fbxPathLineEdit.setText(path)
        else:
            
            ref_dir=path
            if (os.path.exists(ref_dir)):
                    files = [f for f in os.listdir(ref_dir) 
                    if os.path.isfile(os.path.join(ref_dir, f)) and 
                    f.lower().endswith(('.ma', '.mb', '.fbx'))]
                    
                    if  files:
                        files.sort(key=lambda fn: os.path.getmtime(ref_dir + "\\" + fn)
                                        if not os.path.isdir(ref_dir + "\\" + fn) else 0)
                        print('最新的文件为： ' + files[-1])
                        ref_dir=path+"/"+files[-1]
                        self.fbxPath=ref_dir
            
            self.fbxPathLineEdit.setText(ref_dir)
            
        
    def bakeStartOrEnd(self,start):
        pre,skeleton=self.getName()
        print(pre,skeleton)

        obj=pre+":"+skeleton
        all_times = []
        times = cmds.keyframe(obj, query=True, timeChange=True)
        all_times.extend(times)
        min_frame = int(min(all_times))
        max_frame = int(max(all_times))

        if start:
            #目标首
            targetT = [min_frame,min_frame]
        else:
            #目标尾
            targetT = [max_frame,max_frame]
        
        curernt_times = []
        curernt = cmds.keyframe("Main", query=True, timeChange=True)
        if curernt:
            curernt_times.extend(curernt)

            curernt_min_frame = int(max(curernt_times))
            curernt_max_frame = int(min(curernt_times))
        else:
            curernt_min_frame = max_frame
            curernt_max_frame = min_frame

        if start:
            curentT = curernt_min_frame
        else:
            curentT = curernt_max_frame

        print("目标帧",targetT)
        print("设置帧",curentT)
        

        ba.bakeAnimation(
            bake =  self.BakeAnimationUI.isChecked(),
            delete = self.DeleteUI.isChecked(),
            take = targetT,
                ctrl= self.ctrlCheck.isChecked(),
                pre=pre,
                remove=False,
                offTime=curentT
                )

    def Buttonevent(self):
        pre,name=self.getName()
        ba.bakeAnimation(
            bake =  self.BakeAnimationUI.isChecked(),
            delete = self.DeleteUI.isChecked(),
            take = [self.startTakeLineEdit.text(),
                    self.EndTakeLineEdit.text()],
                    ctrl= self.ctrlCheck.isChecked(),
                    pre=pre,
                    remove=True
                    )

    def Tpose(self):
        #输入要对应的骨架根骨骼名字默认Skeleton，前缀默认Model：
        pre,skeleton=self.getName()
        print(pre,skeleton)

        obj=pre+":"+skeleton
        all_times = []
        times = cmds.keyframe(obj, query=True, timeChange=True)
        if times:
            all_times.extend(times)
            min_frame = int(min(all_times))
            max_frame = int(max(all_times))
            cmds.playbackOptions(minTime=min_frame)
            cmds.playbackOptions(maxTime=max_frame)
            cmds.playbackOptions(animationStartTime=min_frame)
            cmds.playbackOptions(animationEndTime=max_frame)
        else:
            min_frame=cmds.currentTime(q=1)
            max_frame=cmds.currentTime(q=1)
    
        # 设置时间滑块到动画开始位置
        # cmds.currentTime(min_frame)
        self.startTakeLineEdit.setText(str(min_frame))
        self.EndTakeLineEdit.setText(str(max_frame))
        ba.matchTransSkeleton([skeleton],pre)

    def getName(self):
        if self.defaultPrefixRadio.isChecked():
            skeleton="Skeleton"
            pre="model"

        else:
            se=cmds.ls(sl=1)[0]
            skeleton=se[se.find(":")+1:len(se)]
            pre=se[0:se.find(":")]
        
        if not cmds.objExists(pre+":"+skeleton):
                skeleton="Char:"+skeleton
        
        return pre,skeleton

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


    def referenceFiles(self):
        path=self.fbxPathLineEdit.text()
        if not path:
            return
        if self.batchImportCheck.isChecked():
            if os.path.exists(path) and os.path.isdir(path):
                # 获取所有.ma/.mb/.fbx文件
                files = [f for f in os.listdir(path) 
                        if os.path.isfile(os.path.join(path, f)) and 
                        f.lower().endswith(('.ma', '.mb', '.fbx'))]
                if files:
                    index=1
                    stf=""
                    for file in files:
                        file_path = os.path.join(path, file)
                        ba.referenceFiles(file_path,"model"+stf)
                        stf=str(index)
                        index+=1

            
        else:

            ba.referenceFiles(path,"model")


