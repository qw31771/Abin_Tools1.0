from typing import Dict, Tuple
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import saveData
import maya.cmds as cmds
import maya.mel as mel
import common
from EventManager import EventManager
import ExportSettings_test 
import tools.其他.CodeV.scripts.tabUI.tab2.ExportScript as ExportScript 
from importlib import reload
reload(ExportScript)
reload(ExportSettings_test)

class Tab_UI(QTabWidget):
    def __init__(self, parent):
        super(Tab_UI, self).__init__(parent)
        
        self._parent=parent
        self._parent.tab_widget = parent.tab_widget
        self._event_manager = parent.event_manager
        self.name_map={}
        self.init()
        # 初始化事件管理器
        self.event_manager = EventManager()
        self.createBox1_layout()
        self.createBox2_layout()
        self.createBox3_layout()    
        self.createBox4_layout()
        self.settings =ExportSettings_test.ExportSettings(self)
        self.create_connections()

    def init(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setMargin(0)
        
        tab.setLayout(layout)
        self._parent.tab_widget.addTab(tab, '模型')
        
        self.layout1=QVBoxLayout()
        self.layout1.setMargin(5)
        self.layout2=QVBoxLayout()
        self.layout3=QVBoxLayout()
        self.layout4=QVBoxLayout()
        self.layout1.setAlignment(Qt.AlignTop)  # 关键设置
        self.layout2.setAlignment(Qt.AlignTop)
        self.layout3.setAlignment(Qt.AlignTop)
        self.layout4.setAlignment(Qt.AlignTop)

        layout.addLayout(self.layout1, stretch=0)
        layout.addLayout(self.layout2, stretch=0)
        layout.addLayout(self.layout3, stretch=0)
        layout.addLayout(self.layout4, stretch=1)
    
    def createBox1_layout(self):
        save_layout=QHBoxLayout()
        save_layout.setSpacing(2)
        self.setting_combo_box = QComboBox(self)
        self.setting_combo_box.setMinimumHeight(35)
        # item=['默认设置']
        # self.setting_combo_box.addItems(item)
        self.addBtn=common.imgButton(30,saveData.PATH.icon+"/add.png","添加预设")
        self.renameBtn=common.imgButton(30,saveData.PATH.icon+"/rename.png","重命名")
        self.deleteBtn=common.imgButton(30,saveData.PATH.icon+"/delete.png","删除预设")
        save_layout.addWidget(self.setting_combo_box)
        save_layout.addWidget(self.addBtn)
        save_layout.addWidget(self.renameBtn)
        save_layout.addWidget(self.deleteBtn)

        self.layout1.addLayout(save_layout, alignment=Qt.AlignTop)

    def createBox2_layout(self):
        # 网格布局
        grid = QGridLayout()
        grid.setContentsMargins(15, 0, 0,0)

        self.phz=common.checkBox('平滑组',True)
        self.sjh=common.checkBox('三角化',False)
        self.phwl=common.checkBox('平滑网格',False)
        self.qxfx=common.checkBox('切线和次法线',True)
        self.fgfx=common.checkBox('逐顶点分割法线',False)

        grid.addWidget(self.phz, 0, 0)
        grid.addWidget(self.sjh, 0, 1)
        grid.addWidget(self.phwl, 1, 0)
        grid.addWidget(self.qxfx, 1, 1)
        grid.addWidget(self.fgfx, 2, 0)


        # 将网格布局包装在一个垂直布局中（如果需要）
        content_layout = QVBoxLayout()
        content_layout.addLayout(grid)

        separator = common.hLine()
        
        self.geometry_menu =common.popWidgetMenu("几何体",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addWidget(separator)
        set_layout.addLayout(self.geometry_menu)
        self.layout2.addLayout(set_layout)

    def createBox3_layout(self):
        grid = QGridLayout()
        grid.setContentsMargins(15, 0, 0, 0)

        self.yd=common.checkBox('0帧导出',False)
        self.xzyy=common.checkBox('删除引用名',True)
        self.srlj=common.checkBox('输入连接',False)
        self.zdx=common.checkBox('包括子对象',True)

        grid.addWidget(self.yd, 0, 0)
        grid.addWidget(self.xzyy, 0, 1)
        grid.addWidget(self.srlj, 1, 0)
        grid.addWidget(self.zdx, 1, 1)

        self.zx = common.titleComboBox('上方轴向',['Z','Y'],[20, 10, 20, 0])
        
        content_layout = QVBoxLayout()
        content_layout.addLayout(grid)
        content_layout.addLayout(self.zx)
        
        separator = common.hLine()

        self.set_menu =common.popWidgetMenu("设置",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addLayout(self.set_menu)
        set_layout.addWidget(separator)
        

        self.layout3.addLayout(set_layout)

    def createBox4_layout(self):
        remove_layout=QHBoxLayout()
        remove_layout.setSpacing(5)
        remove_lab=QLabel(' | 删除关键词:')
        remove_lab.setStyleSheet("color: rgb(255,255,255);") 
        remove_lab.setFixedSize(105,35)
        self.remove_box = QComboBox(self)
        self.remove_box.setMinimumHeight(35)
        # item=['','无','全选','_LOD0','Head','Hair']
        # self.remove_box.addItems(item)
        self.add_RemoveKey=common.imgButton(30,saveData.PATH.icon+"/outKey.png","添加剔除关键词")
        self.remove_RemoveKey=common.imgButton(30,saveData.PATH.icon+"/delete.png","删除关键词")
        remove_layout.addWidget(remove_lab)
        remove_layout.addWidget(self.remove_box)
        remove_layout.addWidget(self.add_RemoveKey)
        remove_layout.addWidget(self.remove_RemoveKey)
        self.remove_key=common.titleTextEdit(65,pht="  剔除的关键词......",margins=[5,0,5,0],edit=False)
        self.key_menu =common.popWidgetMenu("剔除关键词",True,self.remove_key)
        item=['导出当前选择','导出全部','关键词导出']
        self.select_model = QComboBox(self)
        self.select_model.setMinimumHeight(35)
        self.select_model.addItems(item)

        model_layout=QHBoxLayout()
        model_layout.setSpacing(5)
        export_lab=QLabel(' | 导出关键词:')
        export_lab.setStyleSheet("color: rgb(255,255,255);") 
        export_lab.setFixedSize(105,35)
        self.model_box = QComboBox(self)
        self.model_box.setMinimumHeight(35)
        # item=['_LOD0','_LOD1','_LOD2','_LOD3','_DT','_LOD']
        # self.model_box.addItems(item)
        self.add_ExportKey=common.imgButton(30,saveData.PATH.icon+"/outKey.png","添加导出关键词")
        self.remove_ExportKey=common.imgButton(30,saveData.PATH.icon+"/delete.png","删除关键词")
        self.export_key=common.titleTextEdit(65,pht="  导出的关键词......",margins=[5,0,5,0],edit=False)
        self.export_menu =common.popWidgetMenu("导出关键词",True,self.export_key)
        model_layout.addWidget(export_lab)
        model_layout.addWidget(self.model_box)
        model_layout.addWidget(self.add_ExportKey)
        model_layout.addWidget(self.remove_ExportKey)


        self.export_fils = common.titleComboBox('导出',['导出单个文件','导出多个文件'],[5, 5, 5, 3])
        self.ds_combo = self.export_fils.itemAt(1).widget()  # 获取QComboBox实例
        # 输入框
        input_layout=QHBoxLayout()
        input_layout.setSpacing(5)
        self.export_input = QLineEdit()
        self.export_input.setFixedHeight(40)
        self.export_input.setPlaceholderText("< 输入名称 >   ● 多文件导出「 , 」分割前后缀")
        input_layout.addWidget(self.export_input)


        self.export_btn=QPushButton('导出')
        self.export_btn.setFixedHeight(80)

         # 创建QListWidget并设置属性
        self.export_label = QListWidget()
        self.export_label.setSelectionMode(QListWidget.ExtendedSelection)  # 单选（可选：ExtendedSelection多选）
        self.export_label.setEditTriggers(QListWidget.NoEditTriggers)    # 禁止编辑
        

        self.layout4.addLayout(remove_layout, alignment=Qt.AlignTop)
        self.layout4.addLayout(self.key_menu, alignment=Qt.AlignTop)
        self.layout4.addWidget(self.select_model, alignment=Qt.AlignTop)
        self.layout4.addLayout(model_layout, alignment=Qt.AlignTop)
        self.layout4.addLayout(self.export_menu, alignment=Qt.AlignTop)
        self.layout4.addLayout(self.export_fils, alignment=Qt.AlignTop)

        self.layout4.addLayout(input_layout, alignment=Qt.AlignTop)
        self.layout4.addWidget(self.export_btn, alignment=Qt.AlignBottom)
        self.layout4.addWidget(self.export_label, stretch=1)


    def create_connections(self):
        # 信号连接
        self.ds_combo.currentIndexChanged.connect(self.update_ui)
        self.select_model.currentIndexChanged.connect(self.update_ui)
        self.export_input.textChanged.connect(self.update_ui)
        # 将 Maya 事件回调连接到信号
        try:
            if hasattr(self, 'event_manager'):
                self.event_manager.register_observer("SelectionChanged", self.on_selection_changed)
                self.event_manager.register_maya_event("SelectionChanged", "SelectionChanged")
        except:
            pass

        #checekBox
        self.phz.stateChanged.connect(lambda:self.settings.change_Checked(self.phz,'phz'))
        self.sjh.stateChanged.connect(lambda:self.settings.change_Checked(self.sjh,'sjh'))
        self.phwl.stateChanged.connect(lambda:self.settings.change_Checked(self.phwl,'phwl'))
        self.qxfx.stateChanged.connect(lambda:self.settings.change_Checked(self.qxfx,'qxfx'))
        self.fgfx.stateChanged.connect(lambda:self.settings.change_Checked(self.fgfx,'fgfx'))
        self.yd.stateChanged.connect(lambda:self.settings.change_Checked(self.yd,'yd'))
        self.xzyy.stateChanged.connect(lambda:self.settings.change_Checked(self.xzyy,'xzyy'))
        self.srlj.stateChanged.connect(lambda:self.settings.change_Checked(self.srlj,'srlj'))
        self.zdx.stateChanged.connect(lambda:self.settings.change_Checked(self.zdx,'zdx'))
        self.zx.combo.currentIndexChanged.connect(lambda:self.settings.change_combo(self.zx.combo,'zx'))
        self.select_model.currentIndexChanged.connect(lambda:self.settings.change_combo(self.select_model,'select_model'))
        self.export_fils.combo.currentIndexChanged.connect(lambda:self.settings.change_combo(self.export_fils.combo,'export_fils'))

        #预设相关
        self.setting_combo_box.currentIndexChanged.connect(self.settings.change_Preset)
        self.renameBtn.clicked.connect(self.rename_preset_item)
        self.addBtn.clicked.connect(self.add_preset_item)
        self.deleteBtn.clicked.connect(self.remove_preset_item)

        #弹出菜单
        self.geometry_menu.toggle_button.clicked.connect(self.settings.saveMenu_Vis)
        self.set_menu.toggle_button.clicked.connect(self.settings.saveMenu_Vis)
        self.key_menu.toggle_button.clicked.connect(self.settings.saveMenu_Vis)
        self.export_menu.toggle_button.clicked.connect(self.settings.saveMenu_Vis)

        #剔除关键词
        self.remove_box.currentIndexChanged.connect(lambda:self.change_remove_Key(self.remove_box,self.remove_key.textE))
        self.add_RemoveKey.clicked.connect(lambda:self.add_RemoveKey_item(self.remove_box))
        self.remove_RemoveKey.clicked.connect(lambda:self.remove_RemoveKey_item(self.remove_box,self.remove_key.textE))

        #导出关键词
        self.add_ExportKey.clicked.connect(lambda:self.add_RemoveKey_item(self.model_box))
        self.model_box.currentIndexChanged.connect(lambda:self.change_remove_Key(self.model_box,self.export_key.textE))
        self.remove_ExportKey.clicked.connect(lambda:self.remove_RemoveKey_item(self.model_box,self.export_key.textE))

        #导出文本
        self.export_label.itemClicked.connect(self.on_export_item_clicked)
        self.update_ui()
        
        #导出
        self.export_btn.clicked.connect(self.FBX_Export)

    # region 剔除关键词
    def add_RemoveKey_item(self,combo):
        text, ok = QInputDialog.getText(
            self, 
            "添加剔除关键词", 
            "请输入关键词：", 
            text=""  # 初始输入框内容（可选）
        )

        # 若用户点击"确定"且输入非空，则添加到下拉框
        if ok and text.strip():  # text.strip() 过滤首尾空格
            combo.addItem(text.strip())  # 添加新选项 
            self.settings.saveSetting()

    def change_remove_Key(self,combo,textEdit):
        key=combo.currentText()
        if not key:
            return
            
        all_keys=[]
        if key == '无':
            all_keys=[]
        elif key == '全选':
            for i in range(3,combo.count()):
                item = combo.itemText(i)
                all_keys.append(item)
        else:
            current_text=textEdit.toPlainText().strip()
            all_keys = [item for item in current_text.split(' , ') if item]
            if key in all_keys:
                # 选中项已存在，移除
                all_keys.remove(key)
            else:
                # 选中项不存在，添加
                all_keys.append(key)

        textEdit.setPlainText(' , '.join(all_keys))
        self.settings.savePre()
        self.update_ui()


    def remove_RemoveKey_item(self,combo,textEdit):
        if combo.currentIndex() <=2:
            return
        
        key=combo.currentText()
        current_index=combo.currentIndex()
        combo.setCurrentIndex(0)
        combo.removeItem(current_index)

        current_text=textEdit.toPlainText().strip()
        all_keys = [item for item in current_text.split(' , ') if item]
        if key in all_keys:
                # 选中项已存在，移除
                all_keys.remove(key)
                textEdit.setPlainText(' , '.join(all_keys))

        self.settings.saveSetting()
        
    # endregion 剔除关键词


    # region 预设相关
    def add_preset_item(self):
        """按钮点击事件处理：弹出输入框并添加选项"""
        # 弹出输入对话框（父窗口为 self，标题"添加预设"，提示语"请输入预设名称："）
        text, ok = QInputDialog.getText(
            self, 
            "添加预设", 
            "请输入预设名称：", 
            text=""  # 初始输入框内容（可选）
        )

        # 若用户点击"确定"且输入非空，则添加到下拉框
        if ok and text.strip():  # text.strip() 过滤首尾空格
            self.setting_combo_box.addItem(text.strip())  # 添加新选项 
            self.setting_combo_box.setCurrentText(text.strip())
            self.settings.add_Preset()

    def rename_preset_item(self):
        combo=common.get_all_item_texts(self.setting_combo_box)
        items=combo['items']
        current_name=combo['currentName']

        text, ok = QInputDialog.getText(
            self, 
            "重命名", 
            "重命名名称：", 
            text=current_name  # 初始输入框内容（可选）
        )

        if ok and text.strip():
             # 可选：检查新名称是否与其他项重复（避免重复）
            if text.strip() in items:
                QMessageBox.critical(self, "错误", "重命名失败！该名称已存在")
                return

            self.settings.renamePre(current_name,text.strip())

    def remove_preset_item(self):
        if self.setting_combo_box.count() <=1:
            QMessageBox.critical(self, "错误", "至少保留一项设置")
            return
        self.settings.removePre()

    # endregion 预设相关

    def on_selection_changed(self,*args, **kwargs):
        select_model_index = self.select_model.currentIndex() #关键词
        if not select_model_index :
            self.update_ui()

    def update_ui(self,*args, **kwargs):
        select_model_index = self.select_model.currentText() #关键词
        if select_model_index == "导出当前选择":
            se=cmds.ls(sl=1)
            if not se:
                self.export_label.clear()
                return
            
            self.getExportName(se)

        else:
            shapesList = cmds.ls(type="mesh")
            if not shapesList:
                return
            transformList = cmds.listRelatives(shapesList,parent=True,type="transform")
            unique_dict = dict.fromkeys(transformList)
            # 将字典的键转换为列表（保持原顺序）
            unique_list = list(unique_dict.keys())
            if not shapesList:
                self.export_label.clear()
                return
            
            if  select_model_index == "导出全部":
                self.getExportName(unique_list)
            else:
                original_text = self.export_key.textE.toPlainText().strip()
                split_parts = original_text.split(',')
                keys = [part.strip() for part in split_parts]

                export_List=[]
                for obj in unique_list:
                    for key in keys:
                        if key in obj:
                            export_List.append(obj)
                            continue

                self.getExportName(export_List)

            
        if not self.name_map:
            return
        names=self.name_map["n"]
        self.export_label.clear()
        self.export_label.addItems(names)

    def getExportName(self,nameList):
        export_type = self.ds_combo.currentIndex()  #单个，多个
        input_text = self.export_input.text() #输入名称
        # self.name_map={}
        if export_type == 0:  # 单个文件
            if input_text:
                names = [f"{input_text}.fbx"]
            else:
                names = [f"{nameList[0]}.fbx"]
            
            prefix=""
            suffix=""
        else:
            # 多个文件处理
            parts = [p.strip() for p in input_text.split(',', 1)]
            prefix = parts[0] if len(parts) > 0 else ""
            suffix = parts[1] if len(parts) > 1 else ""
            names = [f"{prefix}{obj}{suffix}.fbx" for obj in nameList]

        original_text = self.remove_key.textE.toPlainText().strip()
        split_parts = original_text.split(',')
        keys = [part.strip() for part in split_parts]
        
        replace_names=[]
        if keys:
            for name in names:
                isRe=''
                for key in keys:
                    if key in name:
                        isRe=key
                        break
                if isRe:
                    name=name.replace(isRe,'')
                replace_names.append(name)


        self.name_map["n"]=replace_names
        self.name_map["p"]=prefix
        self.name_map["s"]=suffix
        self.name_map['obj']=nameList
        return self.name_map

    def on_export_item_clicked(self):
        select_items=self.export_label.selectedItems()
        if not self.name_map or not select_items:
            return
        
        select_index = self.export_label.currentRow()
        print(select_index)
        count=len(select_items)
        se=self.get_export_label_obj(select_index)
        if count==1:
            cmds.select(se)
        else:
            cmds.select(se,add=1)


    def get_export_label_obj(self,index):
        export_type = self.ds_combo.currentIndex()
        if not export_type:
            se=self.name_map['obj']
        else:
            se=self.name_map['obj'][index]
        return se


    def FBX_Export(self):
        phz=self.phz.isChecked()
        sjh=self.sjh.isChecked()
        phwl=self.phwl.isChecked()
        qxfx=self.qxfx.isChecked()
        fgfx=self.fgfx.isChecked()
        yd=self.yd.isChecked()
        xzyy=self.xzyy.isChecked()
        srlj=self.srlj.isChecked()
        zdx=self.zdx.isChecked()
        zx=self.zx.combo.currentText()

        if not self.name_map or not self.export_label.count():
            return
        
        # Export_ModelScript.set_Export_model(phz,sjh,phwl,qxfx,fgfx,yd,xzyy,srlj,zdx,zx)
        path=self._parent.path_edit.toPlainText()+'/'

        print(path)
        for i in range(self.export_label.count()):
            item = self.export_label.item(i)
            if item:
                name = item.text()
                obj=self.get_export_label_obj(i)
                # Export_ModelScript.export_fbx(path+name,obj)
        


