# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
from PySide2  import   QtGui,QtCore,QtWidgets
import maya.cmds as cmds
import sys
# sys.path.append(u"//9.134.116.75/CodeVTools/ZWTools/")
from imp import reload
import Export as ep
reload(ep)
import os
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMaya as om

class  ExportAniUI(MayaQWidgetDockableMixin, QWidget):
    def __init__(self):
        super(ExportAniUI, self).__init__()
        self.filepath = self.PathLineEditEvent()
        self.aniRg = self.GetAniRnage()
        self.initUI()
        self.ExportPathUI()
        self.ExportNameUI()
        self.ExportSetUI()
        #self.ExportAniIntoTakeUI()
        self.cameraFovEvent()
        self.ExportButtonUI()
        self.publicLayoutUI()
        print()


    def initUI(self):
        try:
            cmds.deleteUI('exportWorkspaceControl')
        except RuntimeError:
            pass
        self.setWindowTitle(u"动作导出工具 VS:周文")  # 设置窗口的名字
        self.resize(550, 350)
        self.setMinimumWidth(550)
        self.setMinimumHeight(350)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 让窗口悬浮在最上层
        self.setObjectName('export')
        self.show(dockable=True)

    def ExportPathUI(self):
        self.ExportPathGroup = QGroupBox(self)
        self.ExportPathGroup.setTitle(u"导出路径")
        self.ExportPathLayout = QHBoxLayout(self.ExportPathGroup)
        self.ExportPathlabel = QLabel(self.ExportPathGroup)
        self.ExportPathlabel.setText(u"路径:")
        self.ExportPathLineEdit = QLineEdit(self.ExportPathGroup)
        self.ExportPathButton = QPushButton(self.ExportPathGroup)
        self.ExportPathButton.setText(u"获取路径")
        self.ExportPathLayout.addWidget(self.ExportPathlabel)
        self.ExportPathLayout.addWidget(self.ExportPathLineEdit)
        self.ExportPathLayout.addWidget(self.ExportPathButton)

        self.ExportPathLineEdit.setText(self.filepath[0])
        self.ExportPathButton.clicked.connect(self.PathButtonEvent)



    def ExportSetUI(self):
        self.upAxisinfomation = ["Z", "Y"]
        self.unitInfomation = ["cm","mm","dm","m"]
        self.ExportSetGroup = QGroupBox(self)
        self.ExportSetGroup.setTitle("设置")
        self.ExportSetLayout = QGridLayout(self.ExportSetGroup)
        self.ExportSetBakeAni = QCheckBox(self.ExportSetGroup)
        self.ExportSetBakeAni.setText(u"烘焙动画")
        self.ExportSetBakeAni.setChecked(True)
        self.ExportSetResaAni = QCheckBox(self.ExportSetGroup)
        self.ExportSetResaAni.setText(u"重采样")
        self.ExportSetResaAni.setChecked(True)
        self.ExportSetCamera = QCheckBox(self.ExportSetGroup)
        self.ExportSetCamera.setText(u"摄像机")

        #self.ExportSetCamera.clicked.connect(self.cameraFovEvent)

        self.ExportSetZreo = QCheckBox(self.ExportSetGroup)
        self.ExportSetZreo.setText(u"移动到原点")

        self.ExportSetupAxisLabel = QLabel(self.ExportSetGroup)
        self.ExportSetupAxisLabel.setText(u"上方向轴:")

        self.ExportSetupAxis = QComboBox(self.ExportSetGroup)
        self.ExportSetupAxis.addItems(self.upAxisinfomation)

        self.ExportSetupunitLabel = QLabel(self.ExportSetGroup)
        self.ExportSetupunitLabel.setText(u"系统单位:")
        self.ExportSetupUnit = QComboBox(self.ExportSetGroup)
        self.ExportSetupUnit.addItems(self.unitInfomation)


        self.ExportSetLayout.addWidget(self.ExportSetBakeAni, 0, 0, 1, 1)
        self.ExportSetLayout.addWidget(self.ExportSetResaAni, 0, 1, 1, 1)
        self.ExportSetLayout.addWidget(self.ExportSetCamera, 0, 2, 1, 1)
        self.ExportSetLayout.addWidget(self.ExportSetZreo,0,3,1,1)
        self.ExportSetLayout.addWidget(self.ExportSetupAxisLabel, 1, 0, 1, 1)
        self.ExportSetLayout.addWidget(self.ExportSetupAxis, 1, 1, 1, 1)
        self.ExportSetLayout.addWidget(self.ExportSetupunitLabel, 1, 2, 1, 1)
        self.ExportSetLayout.addWidget(self.ExportSetupUnit, 1, 3, 1, 1)


    def ExportNameUI(self):
        self.ExportNameGroup = QGroupBox(self)
        self.ExportNameGroup.setTitle(u"导出名字")
        self.ExportNameLayout = QHBoxLayout(self.ExportNameGroup)
        self.ExportNameLabel = QLabel(self.ExportNameGroup)
        self.ExportNameLabel.setText(u"名字:")
        self.ExportNameLineEdit = QLineEdit(self.ExportNameGroup)
        self.ExportNameCheck = QCheckBox(self.ExportNameGroup)
        self.ExportNameCheck.setText(u"批量导出")
        self.ExportNameLayout.addWidget(self.ExportNameLabel)
        self.ExportNameLayout.addWidget(self.ExportNameLineEdit)
        self.ExportNameLayout.addWidget(self.ExportNameCheck)
        self.ExportNameLineEdit.setText(self.filepath[1].split(".")[0])

    def ExportAniIntoTakeUI(self):
        self.ExportAniIntoGroup = QGroupBox(self)
        self.ExportAniIntoGroup.setTitle(u"分片段导出")
        self.ExportAniIntoLayout = QHBoxLayout(self.ExportAniIntoGroup)
        self.ExportAniStartLabel = QLabel(self.ExportAniIntoGroup)
        self.ExportAniStartLabel.setText(u"开始帧:")
        self.ExportStartLineEdit = QLineEdit(self.ExportAniIntoGroup)
        self.ExportAniEndLabel = QLabel(self.ExportAniIntoGroup)
        self.ExportAniEndLabel.setText(u"结束帧:")
        self.ExportAniIntoCheck = QCheckBox(self.ExportAniIntoGroup)
        self.ExportAniIntoCheck.setText(u"动画分割")
        self.ExportAniIntoCheck.setChecked(True)
        self.ExportEndLineEdit = QLineEdit(self.ExportAniIntoGroup)
        self.ExportAniIntoLayout.addWidget(self.ExportAniStartLabel)
        self.ExportAniIntoLayout.addWidget(self.ExportStartLineEdit)
        self.ExportAniIntoLayout.addWidget(self.ExportAniEndLabel)
        self.ExportAniIntoLayout.addWidget(self.ExportEndLineEdit)
        self.ExportAniIntoLayout.addWidget(self.ExportAniIntoCheck)

        self.ExportStartLineEdit.setText(self.aniRg[0])
        self.ExportEndLineEdit.setText(self.aniRg[1])
        self.ExportAniIntoCheck.clicked.connect(self.AniIntoCheckEvent)


    def ExportButtonUI(self):
        self.ExportAniGroup = QGroupBox(self)
        self.ExportAniLayout = QHBoxLayout(self.ExportAniGroup)
        self.ExportAniButton = QPushButton(self.ExportAniGroup)
        self.ExportAniButton.setText(u"导出")
        self.ExportAniOpenFileButton = QPushButton(self.ExportAniGroup)
        self.ExportAniOpenFileButton.setText(u"打开文件夹")
        self.ExportAniOpenFileButton.clicked.connect(self.openFileV)




        self.ExportAniLayout.addWidget(self.ExportAniButton)
        self.ExportAniLayout.addWidget(self.ExportAniOpenFileButton)

        self.ExportAniButton.clicked.connect(self.cameraFovEvent)
        self.ExportAniButton.clicked.connect(self.ExportEvent)
        #self.ExportAniButton.clicked.connect(self.deleteFovAttr)

    def publicLayoutUI(self):
        self.publicLayout = QVBoxLayout(self)
        self.publicLayout.addWidget(self.ExportPathGroup)
        #self.publicLayout.addWidget(self.ExportAniIntoGroup)
        self.publicLayout.addWidget(self.ExportNameGroup)
        self.publicLayout.addWidget(self.ExportSetGroup)
        self.publicLayout.addWidget(self.ExportAniGroup)

    def PathLineEditEvent(self):
        at = ep.animationExport()
        path = at.GetAnimationFilePath()
        if len(path[0]) == 0:
            path = ["None","None"]
            return path
        else:
            return path

    def PathButtonEvent(self):
        self.sender = QFileDialog.getExistingDirectory()
        self.ExportPathLineEdit.setText(self.sender)
        return self.sender

    def GetAniRnage(self):
        at = ep.animationExport()
        rg = at.GetAnimaInto()
        return rg


    def AniIntoCheckEvent(self):
        if self.ExportAniIntoCheck.isChecked():
            self.ExportStartLineEdit.setEnabled(True)
            self.ExportEndLineEdit.setEnabled(True)
            self.ExportAniStartLabel.setEnabled(True)
            self.ExportAniEndLabel.setEnabled(True)
        else:
            self.ExportStartLineEdit.setEnabled(False)
            self.ExportEndLineEdit.setEnabled(False)
            self.ExportAniStartLabel.setEnabled(False)
            self.ExportAniEndLabel.setEnabled(False)


    def getNameSpace(self):
        sel = cmds.ls(sl=True, fl=True)[0]
        if ":" in sel:
            namespaces = sel.split(":")[0]
        else:
            namespaces = ""
        return namespaces,sel

    def toMObject(self,node):
        selList = om.MSelectionList()
        selList.add(str(node))
        mObject = om.MObject()
        selList.getDependNode(0, mObject)
        return mObject

    def ExportEvent(self):
        at = ep.animationExport()
        try:
            with ep.StripNamespace(self.getNameSpace()[0]):
                at.export(upAxis = self.ExportSetupAxis.currentText(),bakeAnimation =self.ExportSetBakeAni.isChecked(),ResampleAnimation = self.ExportSetResaAni.isChecked(),
                          cameras = self.ExportSetCamera.isChecked(),unit = self.ExportSetupUnit.currentText(),intoTakes = [int(self.aniRg[0]),int(self.aniRg[1])],
                          ExportPath = self.ExportPathLineEdit.text(),batch = self.ExportNameCheck.isChecked(),ExportName = self.ExportNameLineEdit.text(),spilAni = False)

            #print("1111")

        except:
            if cmds.listRelatives(cmds.ls(sl =True,fl =True)[0],p =True) != None:
                parent = {}
                selList = om.MSelectionList()
                api_obj = om.MObject()
                om.MGlobal.getSelectionListByName(self.getNameSpace()[1], selList)
                selList.getDependNode(0, api_obj)
                dag_parent = cmds.listRelatives(self.getNameSpace()[1], p=1)
                parent[self.getNameSpace()[1]] = dag_parent[0]
                dag_modi = om.MDagModifier()
                dag_modi.reparentNode(api_obj)
                dag_modi.doIt()

                at.export(upAxis=self.ExportSetupAxis.currentText(), bakeAnimation=self.ExportSetBakeAni.isChecked(),ResampleAnimation=self.ExportSetResaAni.isChecked(),
                          cameras=self.ExportSetCamera.isChecked(), unit=self.ExportSetupUnit.currentText(),intoTakes=[int(self.aniRg[0]), int(self.aniRg[1])],
                          ExportPath=self.ExportPathLineEdit.text(), batch=self.ExportNameCheck.isChecked(),ExportName=self.ExportNameLineEdit.text(), spilAni=False)

                for absolute_name, parent in parent.items():
                    dag_modi = om.MDagModifier()
                    absolute_name_mobject = self.toMObject(absolute_name)
                    parent_mobject = self.toMObject(parent)
                    dag_modi.reparentNode(absolute_name_mobject, parent_mobject)
                    dag_modi.doIt()
                #print("2222")
            else:
                at.export(upAxis=self.ExportSetupAxis.currentText(), bakeAnimation=self.ExportSetBakeAni.isChecked(),
                          ResampleAnimation=self.ExportSetResaAni.isChecked(),
                          cameras=self.ExportSetCamera.isChecked(), unit=self.ExportSetupUnit.currentText(),
                          intoTakes=[int(self.aniRg[0]), int(self.aniRg[1])],
                          ExportPath=self.ExportPathLineEdit.text(), batch=self.ExportNameCheck.isChecked(),
                          ExportName=self.ExportNameLineEdit.text(), spilAni=False)
                #print("3333")


    def openFileV(self):
        os.startfile(self.ExportPathLineEdit.text()+"/FBX")

    def cameraFovEvent(self):
        if self.ExportSetCamera.isChecked() == True:
            at = ep.animationExport()
            cam = at.createNewCamera(cmds.ls(sl =True)[0])
            cmds.select(cam[0])
            sel = cmds.ls(sl = True)
            if len(sel)>0:
                at.cameraData(sel[0],cmds.listRelatives(s=1)[0])
            else:
                cmds.error("请选择一个摄像机处理")
        else:
            pass

    def deleteFovAttr(self):
        if self.ExportSetCamera.isChecked() == True:
            # obj = pm.selected()[0]
            obj = cmds.ls(sl=1)[0]
            if obj.getShape().type() == 'camera':
                cmds.delete(obj)
        else:
            cmds.error("")




