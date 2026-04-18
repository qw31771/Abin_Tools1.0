import os
from PySide2 import QtCore 
from PySide2 import QtUiTools 
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import abin_ExportScript
import importlib
import abin_ExportCommon
myName=importlib.reload(abin_ExportCommon).ExportName

Code :abin_ExportScript=importlib.reload(abin_ExportScript)

import maya.OpenMayaUI as omui
import maya.cmds as cmds



def maya_main_window():
    main_window_ptr=omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr),QtWidgets.QWidget)
    
class ModelExport_UI(QtWidgets.QDialog):
    def __init__(self,ui_path=None,parent=maya_main_window()):
        super(ModelExport_UI,self).__init__(parent)
        #保存信息到环境变量
        self.settings_path = os.path.join(os.getenv('HOME'), myName.uiName.iniName)
        
        self.init_ui(ui_path)
        self.maya_init()
        self.create_layout()
        self.create_connections()

        self.setTip()

    #ui初始化
    def init_ui(self,ui_path):
        self.setWindowTitle("abin_ModelExport UI")
        self.resize(700, 820)
        self.setMinimumWidth(700)
        self.setMinimumHeight(820)
        self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowFlags/(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.6)

        # radius=30

        # self.setStyleSheet(
        #     """
        #     backgroud:rgb(255,255,0);
        #     borde-top-left-radius:(0)px;
        #     borde-bottom-left-radius:(0)px;
        #     borde-top-right-radius:(0)px;
        #     borde-bottom-right-radius:(0)px;
        #     """.format(radius)
        # )

        #获取窗口布局位置信息
        if os.path.exists(self.settings_path):
            settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
            self.restoreGeometry(settings_obj.value(myName.uiName.windowGeometry))

        #获取.ui文件路径
        if not ui_path:
            ui_path=myName.Path.ui

        #加载窗口
        f=QtCore.QFile(ui_path)
        loader=QtUiTools.QUiLoader()
        self.ui=loader.load(f,parentWidget=None)

    #maya信息初始化
    def maya_init(self):
        ref_dir=myName.Path.referencePath
        if (os.path.exists(ref_dir)):
                files=os.listdir(ref_dir)
                if  files:
                    files.sort(key=lambda fn: os.path.getmtime(ref_dir + "\\" + fn)
                                    if not os.path.isdir(ref_dir + "\\" + fn) else 0)
                    print('最新的文件为： ' + files[-1])
                    ref_dir=myName.Path.referencePath+"/"+files[-1]

        self.ui.refPath_Ld.setText(ref_dir)
        self.ui.savePath_Ld.setText(myName.Path.exportLodPath)
        Code.init(self.ui)
        

    #监听关闭事件
    def closeEvent(self, event):
        # Save window's geometry
        settings_obj = QtCore.QSettings(self.settings_path, QtCore.QSettings.IniFormat)
        settings_obj.setValue(myName.uiName.windowGeometry, self.saveGeometry())

    #设置布局
    def create_layout(self):
        main_layout=QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.ui)
        self.ui.sl_RefPath_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.ui.sl_SavePath_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        # self.ui.layout().setContentsMargins(6,6,6,6)

    #创建控件连接
    def create_connections(self):
        u=self.ui
        #复制蒙皮按钮
        u.copy_skin_btn.clicked.connect(lambda:Code.cppy_Skin(u.copyJnt.currentIndex(),u.coptSuf.currentIndex(),u.copyInf.currentIndex()))

        # #选择按钮   btn
        u.jnt_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.skeletonSetsName]))
        u.lod0_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.lod0SetsName]))
        u.lod1_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.lod1SetsName]))
        u.lod2_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.lod2SetsName]))
        u.lod3_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.lod3SetsName]))
        u.lod4_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.lod4SetsName]))

        u.all_sl_btn.clicked.connect(lambda :Code.selectSets([myName.SetsName.lod0SetsName,myName.SetsName.lod1SetsName,myName.SetsName.lod2SetsName,myName.SetsName.lod3SetsName,myName.SetsName.lod4SetsName]))

        # # #设置按钮   btn
        u.jnt_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.skeletonSetsName,None))
        u.lod0_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.lod0SetsName,u.lod0_showType_box))
        u.lod1_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.lod1SetsName,u.lod1_showType_box))
        u.lod2_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.lod2SetsName,u.lod2_showType_box))
        u.lod3_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.lod3SetsName,u.lod3_showType_box))
        u.lod4_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.lod4SetsName,u.lod4_showType_box))

        u.all_set_btn.clicked.connect(lambda:Code.resetSets(myName.SetsName.allSetName,[u.lod0_showType_box,u.lod1_showType_box,u.lod2_showType_box,u.lod3_showType_box,u.lod4_showType_box]))

        # # #显示按钮  box
        u.lod0_showType_box.currentIndexChanged.connect(lambda :Code.changeShowType(myName.SetsName.lod0SetsName,u.lod0_showType_box.currentIndex()))
        u.lod1_showType_box.currentIndexChanged.connect(lambda :Code.changeShowType(myName.SetsName.lod1SetsName,u.lod1_showType_box.currentIndex()))
        u.lod2_showType_box.currentIndexChanged.connect(lambda :Code.changeShowType(myName.SetsName.lod2SetsName,u.lod2_showType_box.currentIndex()))
        u.lod3_showType_box.currentIndexChanged.connect(lambda :Code.changeShowType(myName.SetsName.lod3SetsName,u.lod3_showType_box.currentIndex()))
        u.lod4_showType_box.currentIndexChanged.connect(lambda :Code.changeShowType(myName.SetsName.lod4SetsName,u.lod4_showType_box.currentIndex()))

        # #调试   btn
        u.getCtrl_btl.clicked.connect(lambda:Code.selectCtrl(u.ctrlParent_box.isChecked()))
        u.reset0_btn.clicked.connect(lambda:Code.setZero(u.ctrlParent_box.isChecked()))
        u.all_vtx_box.clicked.connect(lambda:Code.vtxColorShow(u.all_vtx_box.isChecked()))
        u.check_vtx_btn.clicked.connect(lambda:Code.check4Vtx(u))
        u.reset_vtx_btn.clicked.connect(lambda:Code.reset4Vtx(u))
        u.testType_btn.clicked.connect(lambda:Code.testAim(u.testType_box.currentIndex()))
        

        #选择路径
        u.sl_RefPath_btn.clicked.connect(lambda:self.searchForFiles(1))
        u.sl_SavePath_btn.clicked.connect(lambda:self.searchForFiles(2))
        u.open_savePath_btn.clicked.connect(lambda:os.startfile(u.savePath_Ld.text()))

        #引用
        u.ref_btn.clicked.connect(lambda:Code.refFile(u.refPath_Ld.text()))

        #导入
        u.import_btn.clicked.connect(lambda:Code.importFile(u))

        #导出
        u.export_btn.clicked.connect(lambda:self.exportM())

        #弹窗
        u.add_RemoveStr_Btn.clicked.connect(lambda:Code.expoetLod(u))

        #权重1
        u.addBtn1.clicked.connect(lambda:Code.weight1(u))

        #剪切权重
        u.addBtn2.clicked.connect(lambda:self.show_geo_selection_dialog(u))

        #设置颜色
        u.addBtn3.clicked.connect(Code.setColor)

        #改大写并添加_LOD0
        u.addBtn4.clicked.connect(Code.changeName)

        #扩选
        u.addBtn5.clicked.connect(Code.PolySelectTraverse)

        # pass

    def exportM(self):
        success=Code.expoetLod(self.ui)
        if success:
            QtWidgets.QMessageBox.information(self,"通知", "   \n      导出成功      \n   ")


        else:
            QtWidgets.QMessageBox.critical(self,"通知", "   \n      导出失败      \n   ")
    

    #设置控件提示信息
    def setTip(self):
        self.ui.copy_skin_btn.setToolTip("选择模型,执行复制模型并蒙皮")
        self.ui.getCtrl_btl.setToolTip("框选全部控制器,自动选出可被关键帧的控制器,如果勾选父,则会加选控制器的父级,在控制器归零不完整时使用")
        self.ui.reset0_btn.setToolTip("将选择的对象位移和旋转置零")
        self.ui.testType_btn.setToolTip("人物直接点击,枪械选择根骨骼,自动k一段动画以供测试")
        self.ui.import_btn.setToolTip("导入全部所选对象,路径为选择路径中的路径")
        self.ui.add_RemoveStr_Btn.setToolTip("导出的名字中需要剔除的关键字")


    #选择路径
    def searchForFiles(self,typ):    
        multipleFilters = "All Files (*.*);;Maya Files (*.ma *.mb);;Maya ASCII (*.FBX);;"
        
        if typ==1:
            title="选择引用"
            dir=myName.Path.referencePath
            if not (os.path.exists(dir)):
                dir=myName.Path.scencePath
        else:
            title="保存路径"
            dir=myName.Path.scencePath

        #地址选择
        filepath = cmds.fileDialog2(fileFilter=multipleFilters,
                                    dialogStyle=2, fileMode=typ, returnFilter=True,cap=title,dir=dir,okc="保存")
        
        # print(filepath[0])
        #将所选择的地址填入
        if filepath:
            if typ==1:
                self.ui.refPath_Ld.setText(filepath[0])
            else:
                self.ui.savePath_Ld.setText(filepath[0])


    def show_geo_selection_dialog(self,ui):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("选择要剪切的模型")
        dialog.setMinimumSize(400, 500)
            # 创建布局
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # 创建按钮组
        button_layout = QtWidgets.QHBoxLayout()
        
        # 全选按钮
        select_all_btn = QtWidgets.QPushButton("全选")
        
        # 反选按钮
        re_se_btn = QtWidgets.QPushButton("反选")
        
        # 确定按钮
        ok_btn = QtWidgets.QPushButton("确定")
        ok_btn.setDefault(True)
        
        # 取消按钮
        cancel_btn = QtWidgets.QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(re_se_btn)
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

         # 创建模型列表
        list_widget = QtWidgets.QListWidget()
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        selected_joints = cmds.ls(selection=True, type='joint')
    
        # 检查选择数量
        if len(selected_joints) < 2:
            cmds.warning("请至少选择两个骨骼（最后一个为接收权重的目标骨骼）")
            return
        
        # 获取所有皮肤簇节点
        skin_geo_map  = {}
        for joint in selected_joints[0:len(selected_joints)-1]:
            # 查找连接到此骨骼的皮肤簇
            skin_clusters = cmds.listConnections(joint, type='skinCluster') or []
            
            for skin_cluster in set(skin_clusters):
            # 获取皮肤簇关联的几何体
                geoShape = cmds.skinCluster(skin_cluster, query=True, geometry=True)[0]
                geo = cmds.listRelatives(geoShape, parent=True, type='transform')[0]
                skin_geo_map[geo]=skin_cluster
        
        if not skin_geo_map:
            cmds.warning("未找到关联的皮肤簇")
            return
        
        # 添加模型到列表
        for geo in skin_geo_map.keys() :
            item = QtWidgets.QListWidgetItem(geo)
            list_widget.addItem(item)

        # 默认选中所有项
        list_widget.selectAll()

        def invert_selection():
            # 创建索引列表
            selected_indexes = [index.row() for index in list_widget.selectedIndexes()]
            
            # 反选：未选中的变为选中，选中的变为未选中
            for i in range(list_widget.count()):
                if i in selected_indexes:
                    list_widget.item(i).setSelected(False)
                else:
                    list_widget.item(i).setSelected(True)

        def on_button_clicked():
            # 获取当前选中的所有项目（返回QListWidgetItem列表）
            selected_items = list_widget.selectedItems()
            
            # 提取项目的文本内容
            selected_texts = [skin_geo_map[item.text()] for item in selected_items]
            
            dialog.close()

            Code.transfer_skin_weights(ui,selected_texts)

        select_all_btn.clicked.connect(lambda: list_widget.selectAll())
        re_se_btn.clicked.connect(invert_selection)
        ok_btn.clicked.connect(on_button_clicked)
        
            # 添加到主布局
        layout.addWidget(list_widget)
        layout.addLayout(button_layout)


        parent_rect = self.frameGeometry()
        dialog_rect = dialog.frameGeometry()
        dialog.move(
            parent_rect.center() - dialog_rect.center()
        )
        
        # 显示对话框
        dialog.exec_()


def open_ui():

    global designer_ui
    try:
        designer_ui.close()
        designer_ui.deleteLater()
    except:
        pass
    designer_ui=ModelExport_UI()
    designer_ui.show()
    #情况1
    # if not designer_ui:
    #     designer_ui = ModelExport_UI()
    #     designer_ui.show()
	# # 情况2
    # if designer_ui.isHidden():
    #     designer_ui.show()
	# # 情况3
    # else:
    #     # 设置控件在最上层 
    #     designer_ui.raise_()
    #     designer_ui.activateWindow()








