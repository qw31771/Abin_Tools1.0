# -*- coding: utf-8 -*-
import os
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore, QtWidgets
# import winreg
import maya.mel as ml
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class ExportUI(MayaQWidgetDockableMixin, QWidget):
    def __init__(self):
        super(ExportUI, self).__init__()
        self.initUI()
        self.GetCurrentfile()
        self.SavePathUI()
        self.SavePathString()
        self.SetingUI()
        self.ExportButton()
        self.GetFileNameSeting()
        self.GetFileName()
        self.ExportLayout()
        self.FBXSkiningSeting()
        self.FBXSmothGruopSeting()
        self.FBXBlendshpaesSeting()
        self.FBXTriangulationSeting()
        self.FBXTurboSmoothSeting()
        self.FBXTangentsBinormalsSeting()
        self.FBXAxisSeting()
        self.FBXEmbedMEdiaSeting()
        self.GetInputName()
        cmds.FBXExportInputConnections ("-v", False)

    def initUI(self):
        try:
            cmds.deleteUI('modleWorkspaceControl')
        except RuntimeError:
            pass
        self.setWindowTitle(u"模型导出工具 VS:周文")  # 设置窗口的名字
        self.resize(800, 500)
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 让窗口悬浮在最上层
        self.setObjectName('modle')
        self.show(dockable=True)

    def SavePathUI(self):
        self.SavePathGourp = QGroupBox(self)
        self.SavePathGourp.setTitle(u"导出路径")
        self.SavePathLineEdit = QLineEdit(self.SavePathGourp)
        # key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        # r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')

        self.SavePathLineEdit.setText(self.SaveCurrentFile)  # 获取桌面路径
        # self.SavePathLineEdit.setPlaceholderText(u"设置导出路径")
        self.SavePathLineEdit.setReadOnly(True)
        self.SavePathLineEdit.textChanged.connect(self.SavePathString)
        self.SaveButton = QPushButton(self.SavePathGourp)
        self.SaveButton.setText(u"获取路径")
        self.SaveButton.clicked.connect(self.ClickSavePathButton)
        self.SaveLaoyt = QHBoxLayout(self.SavePathGourp)
        self.SaveLaoyt.addWidget(self.SavePathLineEdit)
        self.SaveLaoyt.addWidget(self.SaveButton)

    def ClickSavePathButton(self):
        self.sender = QFileDialog.getExistingDirectory()
        # 解决中文路径报错问题
        a = (self.sender)
        self.SavePathLineEdit.setText((self.sender))

    def SavePathString(self):
        self.PathString = self.SavePathLineEdit.text()
        self.PathString = (self.PathString)
        self.PathString = self.PathString + u"\FBX文件"
        self.mkdir(self.PathString)
        # print(self.PathString)

    # 获取当前文件的路径
    def GetCurrentfile(self):
        openFilePath = ml.eval("file -q -location")
        filePath = os.path.split((openFilePath))
        self.SaveCurrentFile = filePath[0]
        self.SaveCurrentFile = os.path.abspath(os.path.join(self.SaveCurrentFile, ".."))  # 获取上一级目录

    # 设置导出的名字
    def GetFileName(self):
        self.GetFileNameGroup = QGroupBox(self)
        self.GetFileNameGroup.setTitle(u"导出名字")
        self.GetFileNameLabel = QLabel(self.GetFileNameGroup)
        self.GetFileNameLabel.setText(u"导出名字：")
        self.GetFileNameLineEdite = QLineEdit(self.GetFileNameGroup)
        self.GetFileNameLineEdite.setText(self.ExportName)
        self.GetFileNameLineEdite.textChanged.connect(self.GetInputName)
        self.CheckFileName = QCheckBox(self.GetFileNameGroup)
        self.CheckFileName.setText(u"选择导出")
        self.CheckFileName.clicked.connect(self.isCheckExoprt)
        self.CheckFileName.setChecked(False)
        self.GetFileNameLyout = QHBoxLayout(self.GetFileNameGroup)
        self.GetFileNameLyout.addWidget(self.GetFileNameLabel)
        self.GetFileNameLyout.addWidget(self.GetFileNameLineEdite)
        self.GetFileNameLyout.addWidget(self.CheckFileName)

    def GetFileNameSeting(self):
        try:
            openFilePath = ml.eval("file -q -location")
            filePath = os.path.split((openFilePath))
            self.ExportName = filePath[-1]
            self.ExportName = self.ExportName.split(".")[0]
            self.ExportName = self.ExportName.strip("_Rig")
        except IndexError:
            self.ExportName = u"请对导出的文件命名"

    def GetInputName(self):
        self.InputName = self.GetFileNameLineEdite.text()  # 获取用户输入的名字
        # print(self.InputName)

    def SetingUI(self):
        self.SetingGourp = QGroupBox(self)
        self.SetingGourp.setTitle(u"导出设置")

        self.SmothGruop = QCheckBox(self.SetingGourp)
        self.SmothGruop.setChecked(True)
        self.SmothGruop.setText(u"平滑组")
        self.SmothGruop.clicked.connect(self.FBXSmothGruopSeting)

        self.triangulation = QCheckBox(self.SetingGourp)
        self.triangulation.setText(u"三角化")
        self.triangulation.clicked.connect(self.FBXTriangulationSeting)

        self.TurboSmooth = QCheckBox(self.SetingGourp)
        self.TurboSmooth.setText(u"平滑网格")
        self.TurboSmooth.clicked.connect(self.FBXTurboSmoothSeting)

        self.TangentsBinormals = QCheckBox(self.SetingGourp)
        self.TangentsBinormals.setText(u"切线和法线")
        self.TangentsBinormals.setChecked(True)
        self.TangentsBinormals.clicked.connect(self.FBXTangentsBinormalsSeting)

        self.Skining = QCheckBox(self.SetingGourp)
        self.Skining.setText(u"蒙皮")
        self.Skining.setChecked(True)
        self.Skining.clicked.connect(self.FBXSkiningSeting)

        self.Blendshpaes = QCheckBox(self.SetingGourp)
        self.Blendshpaes.setText(u"融合变形")
        self.Blendshpaes.clicked.connect(self.FBXBlendshpaesSeting)

        self.AxisText = QLabel(self.SetingGourp)
        self.AxisText.setText(u"上方向轴")

        self.Axis = QComboBox(self.SetingGourp)
        self.Axis.setEditable(False)
        self.Axis.addItem("Z")
        self.Axis.addItem("Y")
        self.Axis.currentIndexChanged[str].connect(self.FBXAxisSeting)  # 条目发生改变，发射信号，传递条目内容

        self.EmbedMEdia = QCheckBox(self.SetingGourp)
        self.EmbedMEdia.setText(u"嵌入媒体")
        self.EmbedMEdia.clicked.connect(self.FBXEmbedMEdiaSeting)

        self.SetingLayout = QGridLayout(self.SetingGourp)
        # self.SetingLayout.setHorizontalSpacing(220)
        self.SetingLayout.setColumnStretch(0, 0)
        self.SetingLayout.setColumnStretch(1, 1)
        self.SetingLayout.setColumnStretch(2, 0)
        self.SetingLayout.setColumnStretch(3, 0)
        self.SetingLayout.addWidget(self.SmothGruop, 0, 0)
        self.SetingLayout.addWidget(self.triangulation, 0, 2)
        self.SetingLayout.addWidget(self.TurboSmooth, 1, 0)
        self.SetingLayout.addWidget(self.TangentsBinormals, 1, 2)
        self.SetingLayout.addWidget(self.Skining, 2, 0)
        self.SetingLayout.addWidget(self.Blendshpaes, 2, 2)
        self.SetingLayout.addWidget(self.Axis, 3, 0)
        self.SetingLayout.addWidget(self.AxisText, 3, 1)
        self.SetingLayout.addWidget(self.EmbedMEdia, 3, 2)
        self.SetingLayout.setRowStretch(0, 1)

    # 设置蒙皮
    def FBXSkiningSeting(self):
        if self.Skining.isChecked():
            ml.eval("FBXExportSkins -v  true")
            print("true")
        else:
            ml.eval("FBXExportSkins -v  false")
            print("false")

    # 设置平滑组
    def FBXSmothGruopSeting(self):
        if self.SmothGruop.isChecked():
            ml.eval("FBXExportSmoothingGroups -v true")
            print("true")
        else:
            ml.eval("FBXExportSmoothingGroups -v false")
            print("false")

    # 设置融合变形
    def FBXBlendshpaesSeting(self):
        if self.Blendshpaes.isChecked():
            ml.eval("FBXExportShapes -v true")
            print("true")
        else:
            ml.eval("FBXExportShapes -v false")
            print("false")

    # 设置三角化
    def FBXTriangulationSeting(self):
        if self.triangulation.isChecked():
            ml.eval("FBXExportColladaTriangulate  true")
            print("true")
        else:
            ml.eval("FBXExportColladaTriangulate  false")
            print("false")

    # 设置平滑网格
    def FBXTurboSmoothSeting(self):
        if self.TurboSmooth.isChecked():
            ml.eval("FBXExportSmoothMesh -v true")
            print("true")
        else:
            ml.eval("FBXExportSmoothMesh -v false")
            print("false")

    # 设置切线和法线
    def FBXTangentsBinormalsSeting(self):
        if self.TangentsBinormals.isChecked():
            ml.eval("FBXExportTangents -v  true")
            print("true")
        else:
            ml.eval("FBXExportTangents -v  false")
            print("false")

    def FBXAxisSeting(self):
        if self.Axis.currentText() == "Y":
            ml.eval("FBXExportUpAxis y")
            print("y")
        else:
            ml.eval("FBXExportUpAxis z")
            print("z")

    def FBXEmbedMEdiaSeting(self):
        if self.EmbedMEdia.isChecked():
            ml.eval("FBXExportEmbeddedTextures -v true")
            print("true")
        else:
            ml.eval("FBXExportEmbeddedTextures -v false")
            print("false")

    def ExportButton(self):
        self.ExportButtonGourp = QGroupBox(self)
        self.ExportButtonGourp.setTitle(u"导出")
        self.batchButton = QPushButton(self.ExportButtonGourp)
        self.batchButton.setText(u"批量导出")
        self.batchButton.clicked.connect(self.BatchExport)
        self.LodButton = QPushButton(self.ExportButtonGourp)
        self.LodButton.setText(u"LOD导出")
        self.LodButton.clicked.connect(self.SavePathString)
        self.LodButton.clicked.connect(self.isCheckExoprtSeting)
        self.LodButton.clicked.connect(self.GetInputName)
        self.openFileButton = QPushButton(self.SavePathGourp)
        self.openFileButton.setText(u"打开输出文件夹")
        self.openFileButton.clicked.connect(self.openFileV)
        self.SingerButton = QPushButton(self.ExportButtonGourp)
        self.SingerButton.setText(u"导出一个文件")
        self.SingerButton.clicked.connect(self.isCheckExoprtSetings)
        self.ExportButtonGourpLaout = QHBoxLayout(self.ExportButtonGourp)
        self.ExportButtonGourpLaout.addWidget(self.batchButton)
        self.ExportButtonGourpLaout.addWidget(self.LodButton)
        self.ExportButtonGourpLaout.addWidget(self.SingerButton)
        self.ExportButtonGourpLaout.addWidget(self.openFileButton)

    def ExportLayout(self):
        self.ExportLayout = QVBoxLayout(self)
        self.ExportLayout.addWidget(self.SavePathGourp)
        self.ExportLayout.addWidget(self.GetFileNameGroup)
        self.ExportLayout.addWidget(self.SetingGourp)
        self.ExportLayout.addWidget(self.ExportButtonGourp)
        self.ExportLayout.setStretch(0, 1)
        self.ExportLayout.setStretch(1, 1)
        self.ExportLayout.setStretch(2, 3)
        self.ExportLayout.setStretch(3, 1)

    # 打开输出文件夹
    def openFileV(self):
        os.startfile(self.PathString)

    def SelectExport(self):
        if len(cmds.ls(selection=True)) != 0:
            for i in cmds.ls(selection=True):
                cmds.select(i)
                cmds.file(self.PathString + "\\" + i, force=True, type="FBX export",
                          exportSelected=True)
        else:
            QMessageBox.about(self, u"错误：", u"至少选择一个物体")
            pass

    def LODExport(self):
        self.LodDTMesh = cmds.ls("*DT*",type = "mesh")
        self.Lod0Mesh = cmds.ls("*LOD0*",type = "mesh")
        self.Lod1Mesh = cmds.ls("*LOD1*",type = "mesh")
        self.Lod2Mesh = cmds.ls("*LOD2*",type = "mesh")
        self.Lod3Mesh = cmds.ls("*LOD3*",type = "mesh")
        self.Lod4Mesh = cmds.ls("*LOD4*",type = "mesh")
        try:
            cmds.parent(self.LodDTMesh, w=True)
        except:
            pass
        try:
            cmds.parent(self.Lod0Mesh, w=True)
        except:
            pass
        try:
            cmds.parent(self.Lod1Mesh, w=True)
        except:
            pass
        try:
            cmds.parent(self.Lod2Mesh, w=True)
        except:
            pass
        try:
            cmds.parent(self.Lod3Mesh, w=True)
        except:
            pass
        try:
            cmds.parent(self.Lod4Mesh, w=True)
        except:
            pass
        self.ExportAllSkeletonList = cmds.ls("Skeleton")

        try:
            if len(cmds.ls(u'Skeleton')) != 0:
                cmds.parent("Skeleton", w=True)
        except ValueError:
            pass

        cmds.select(self.ExportAllSkeletonList, self.LodDTMesh)
        try:
            if len(self.LodDTMesh) != 0:
                cmds.file(self.PathString + "\\" + str(self.InputName) + "_DT", force=True, type="FBX export",
                          exportSelected=True)
        except RuntimeError:
            pass

        cmds.select(self.ExportAllSkeletonList, self.Lod0Mesh)
        if len(self.LodDTMesh) != 0:
            try:
                if len(self.Lod0Mesh) != 0:
                    cmds.file(self.PathString + "\\" + str(self.InputName) + "_LOD0", force=True,
                              type="FBX export",
                              exportSelected=True)
            except RuntimeError:
                pass
        else:
            try:
                if len(self.Lod0Mesh) != 0:
                    cmds.file(self.PathString + "\\" + str(self.InputName), force=True, type="FBX export",
                              exportSelected=True)
            except RuntimeError:
                pass

        cmds.select(self.ExportAllSkeletonList, self.Lod1Mesh)
        try:
            if len(self.Lod1Mesh) != 0:
                cmds.file(self.PathString + "\\" + str(self.InputName) + "_LOD1", force=True, type="FBX export",
                          exportSelected=True)
        except RuntimeError:
            pass

        if len(self.ExportAllSkeletonList) == 0:
            cmds.select(self.Lod2Mesh)
        else:
            cmds.select(self.ExportAllSkeletonList, self.Lod2Mesh)

        try:
            if len(self.Lod2Mesh) != 0:
                cmds.file(self.PathString + "\\" + str(self.InputName) + "_LOD2", force=True, type="FBX export",
                          exportSelected=True)
        except RuntimeError:
            pass

        cmds.select(self.ExportAllSkeletonList, self.Lod3Mesh)
        try:
            if len(self.Lod3Mesh) != 0:
                cmds.file(self.PathString + "\\" + str(self.InputName) + "_LOD3", force=True, type="FBX export",
                          exportSelected=True)
        except RuntimeError:
            pass

        cmds.select(self.ExportAllSkeletonList, self.Lod4Mesh)
        try:
            if len(self.Lod4Mesh) != 0:
                cmds.file(self.PathString + "\\" + str(self.InputName) + "_LOD4", force=True, type="FBX export",
                          exportSelected=True)
        except RuntimeError:
            pass

        try:
            cmds.parent(self.LodDTMesh, "Geometry")
        except:
            pass
        try:
            cmds.parent(self.Lod0Mesh, "Geometry")
        except:
            pass
        try:
            cmds.parent(self.Lod1Mesh, "Geometry")
        except:
            pass
        try:
            cmds.parent(self.Lod2Mesh, "Geometry")
        except:
            pass
        try:
            cmds.parent(self.Lod3Mesh, "Geometry")
        except:
            pass
        try:
            cmds.parent(self.Lod4Mesh, "Geometry")
        except:
            pass
            #cmds.parent("Skeleton", "Skin_jnt")

        try:
            cmds.parent("Skeleton", "Skin_jnt")
            cmds.parent("Geometry", "Group")
        except:
            pass

    # 判断按照选择导出还是根据规则自动导出LOD
    def isCheckExoprt(self):
        if self.CheckFileName.isChecked():
            # self.GetFileNameLineEdite.setEnabled(False)
            # self.GetFileNameLineEdite.setText(u"根据选择模型名字自动导出")
            # self.SelectExport()
            pass
        else:
            # self.GetFileNameLineEdite.setEnabled(True)
            self.GetFileNameLineEdite.setText(self.ExportName)
            # self.LODExport()

    def isCheckExoprtSeting(self):
        if self.CheckFileName.isChecked():
            self.SelectExport()
        else:
            self.LODExport()

    def isCheckExoprtSetings(self):
        if self.CheckFileName.isChecked():
            self.SingerSelExport()
        else:
            self.SingerAllExport()

    def SingerAllExport(self):
        if len(cmds.ls(selection=True)) == 0:
            cmds.file(self.PathString + "\\" + str(self.InputName), force=True, type="FBX export",
                      exportAll=True)

    def SingerSelExport(self):
        if len(cmds.ls(selection=True)) != 0:
            cmds.file(self.PathString + "\\" + str(self.InputName), force=True, type="FBX export",
                      exportSelected=True)
        else:
            QMessageBox.about(self, u"错误：", u"至少选择一个物体")

    def BatchExport(self):
        try:
            openFilePath = ml.eval("file -q -location")
            filePath = os.path.split((openFilePath))
            self.MBfileList = []
            for fileNmae in os.listdir(filePath[0]):
                try:
                    if fileNmae.split(".")[1] == "mb" or fileNmae.split(".")[1] == "ma":
                        self.MBfileList.append(fileNmae)
                except IndexError:
                    pass

            for i in self.MBfileList:
                cmds.file(filePath[0] + "/" + i, force=True, open=True)
                cmds.file(self.PathString + "/" + i, force=True, type="FBX export",
                          exportAll=True)
        except WindowsError:
            QMessageBox.about(self, u"错误：", u"未打开正确的MB或MA文件，不能批量导出")

    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True

"""if __name__ == '__main__':
    main = ExportUI()
    main.show()
"""

