from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import saveData
import maya.cmds as cmds
import AB_Maya
from EventManager import EventManager
import re
import Export_ModelSettings
import ExportScript 


class Tab_UI(QTabWidget):
    def __init__(self, parent):
        super(Tab_UI, self).__init__(parent)
        
        self._parent=parent
        self._parent.tab_widget = parent.tab_widget
        self.showState=None
        self.path=parent.path_edit
        self.init()
        # 初始化事件管理器
        self.event_manager = EventManager()
        # 初始化配置
        self.settings =Export_ModelSettings.ExportSettings(self)
        self.script =ExportScript.Export(self)
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

        self.createBox1_layout()
        self.createBox2_layout()
        self.createBox3_layout()    
        self.createBox4_layout()
        self.createBox5_layout()
        self.createBox6_layout()

    def createBox1_layout(self):
        save_layout=QHBoxLayout()
        save_layout.setSpacing(2)
        self.setting_combo_box = QComboBox(self)
        self.setting_combo_box.setMinimumHeight(35)
        self.setting_combo_box.setMaximumWidth(290)
        self.addBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/add.png","添加预设")
        self.renameBtn=AB_Maya.imgButton(25,saveData.PATH.icon+"/rename.png","重命名")
        self.deleteBtn=AB_Maya.imgButton(30,saveData.PATH.icon+"/delete.png","删除预设")
        save_layout.addWidget(self.setting_combo_box)
        save_layout.addWidget(self.addBtn)
        save_layout.addWidget(self.renameBtn)
        save_layout.addWidget(self.deleteBtn)

        self.layout1.addLayout(save_layout, alignment=Qt.AlignTop)

    def createBox2_layout(self):
        # 网格布局
        grid = QGridLayout()
        grid.setContentsMargins(15, 0, 0,0)

        self.phz=AB_Maya.checkBox('平滑组',True)
        self.sjh=AB_Maya.checkBox('三角化',False)
        self.phwl=AB_Maya.checkBox('平滑网格',False)
        self.qxfx=AB_Maya.checkBox('切线和次法线',True)
        self.fgfx=AB_Maya.checkBox('逐顶点分割法线',False)
        self.mp=AB_Maya.checkBox('蒙皮',False)

        grid.addWidget(self.phz, 0, 0)
        grid.addWidget(self.sjh, 0, 1)
        grid.addWidget(self.phwl, 1, 0)
        grid.addWidget(self.qxfx, 1, 1)
        grid.addWidget(self.fgfx, 2, 0)
        grid.addWidget(self.mp, 2, 1)
        

        content_layout = QVBoxLayout()
        content_layout.addLayout(grid)
        
        self.geometry_menu =AB_Maya.popWidgetMenu(" 几何体 ⊿",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addLayout(self.geometry_menu)


        set_layout.addWidget(AB_Maya.hLine())
        self.layout2.addLayout(set_layout)

    def createBox3_layout(self):
        grid = QGridLayout()
        grid.setContentsMargins(15, 0, 0, 0)

        self.yd=AB_Maya.checkBox('0帧导出',False)
        self.xzyy=AB_Maya.checkBox('删除引用名',True)
        self.srlj=AB_Maya.checkBox('输入连接',False)
        self.zdx=AB_Maya.checkBox('包括子对象',True)

        grid.addWidget(self.yd, 0, 0)
        grid.addWidget(self.xzyy, 0, 1)
        grid.addWidget(self.srlj, 1, 0)
        grid.addWidget(self.zdx, 1, 1)

        self.zx = AB_Maya.titleComboBox('上方轴向',['Z','Y'],[20, 10, 20, 0])
        
        content_layout = QVBoxLayout()
        content_layout.addLayout(grid)
        content_layout.addLayout(self.zx)
        

        self.set_menu =AB_Maya.popWidgetMenu(" 设置 ⊿",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addLayout(self.set_menu)
        set_layout.addWidget(AB_Maya.hLine())
        self.layout3.addLayout(set_layout)
    
    def createBox4_layout(self):
        content_layout=QVBoxLayout()
        content_layout.setSpacing(5)
        self.keys_content = QListWidget()
        self.keys_content.setSelectionMode(QListWidget.ExtendedSelection)  # 单选（可选：ExtendedSelection多选）
        self.keys_content.setEditTriggers(QListWidget.NoEditTriggers)    # 禁止编辑
        self.keys_content.setFixedHeight(200)
        self.keys_content.setStyleSheet(""" font-size: 20px;""")

        setting_layout=QHBoxLayout()
        setting_layout.setContentsMargins(0, 0, 0, 0)
        self.addKey_keys=AB_Maya.imgButton(27,saveData.PATH.icon+"/key.png","添加关键词")
        self.addKey_delete=AB_Maya.imgButton(30,saveData.PATH.icon+"/delete.png","删除")
        setting_layout.addStretch(1) 
        setting_layout.addWidget(self.addKey_keys)
        setting_layout.addWidget(self.addKey_delete)

        content_layout.addWidget(self.keys_content,alignment=Qt.AlignBottom)
        content_layout.addLayout(setting_layout, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.key_menu =AB_Maya.popWidgetMenu(" 删除关键词 ⊿",True,content_layout)
        set_layout = QVBoxLayout()
        set_layout.addLayout(self.key_menu)
        set_layout.addWidget(AB_Maya.hLine())
        self.layout4.addLayout(set_layout)

    def createBox5_layout(self):
        content_layout=QVBoxLayout()
        content_layout.setSpacing(5)
        self.sets_content=QVBoxLayout()

        setting_layout=QHBoxLayout()
        setting_layout.setContentsMargins(0, 0, 0, 0)
        self.addSets_select=AB_Maya.imgButton(27,saveData.PATH.icon+"/addSets.png","按选择添加")
        self.addSets_keys=AB_Maya.imgButton(27,saveData.PATH.icon+"/addSets_keys.png","按关键字添加")
        self.addSets_ref=AB_Maya.imgButton(27,saveData.PATH.icon+"/refresh.png","刷新重新识别设置")
        self.addSets_remove=AB_Maya.imgButton(35,saveData.PATH.icon+"/delete.png","删除全部集合")
        setting_layout.addStretch(1) 
        setting_layout.addWidget(self.addSets_select)
        setting_layout.addWidget(self.addSets_keys)
        setting_layout.addWidget(self.addSets_ref)
        setting_layout.addWidget(self.addSets_remove)

        
        content_layout.addLayout(self.sets_content,alignment= Qt.AlignBottom)
        content_layout.addLayout(setting_layout, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.sets_menu =AB_Maya.popWidgetMenu(" 集合 ⊿",True,content_layout)


        set_layout = QVBoxLayout()
        set_layout.addLayout(self.sets_menu)
        set_layout.addWidget(AB_Maya.hLine())
        self.layout4.addLayout(set_layout)

    def createBox6_layout(self):
        #内容
        content_layout=QVBoxLayout()

        #选择
        input_layout=QVBoxLayout()
        name_layout=QHBoxLayout()
        name_layout.setSpacing(0)
        self.export_input_prefix = QLineEdit()
        self.export_input_name = QLineEdit()
        self.export_input_suffix = QLineEdit()
        self.export_input_prefix.setFixedHeight(40)
        self.export_input_name.setFixedHeight(40)
        self.export_input_suffix.setFixedHeight(40)
        self.export_input_prefix.setPlaceholderText("前缀")
        self.export_input_name.setPlaceholderText("..输入名称.... ")
        self.export_input_suffix.setPlaceholderText("后缀")
        self.export_input_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        name_layout.addWidget(self.export_input_prefix)
        name_layout.addWidget(self.export_input_name)
        name_layout.addWidget(self.export_input_suffix)
        name_layout.setStretchFactor(self.export_input_prefix, 2)
        name_layout.setStretchFactor(self.export_input_name, 6)
        name_layout.setStretchFactor(self.export_input_suffix, 2)

        export_layout=QHBoxLayout()
        item=['导出当前选择','导出全部模型','集合导出']
        self.select_model = QComboBox(self)
        self.select_model.setMinimumHeight(35)
        self.select_model.addItems(item)
        item=['导出单个文件','导出多个文件']
        self.export_fils = QComboBox(self)
        self.export_fils.setMinimumHeight(35)
        self.export_fils.addItems(item)
        export_layout.addWidget(self.select_model)
        export_layout.addWidget(self.export_fils)
        input_layout.addLayout(name_layout)
        input_layout.addLayout(export_layout)

        #可视化操作
        self.export_label = QListWidget()
        self.export_label.setSelectionMode(QListWidget.ExtendedSelection)  # 单选（可选：ExtendedSelection多选）
        self.export_label.setEditTriggers(QListWidget.NoEditTriggers)    # 禁止编辑
        content_layout.addLayout(input_layout)
        content_layout.addWidget(self.export_label, stretch=1)  
        self.export_menu =AB_Maya.popWidgetMenu(" 导出 ⊿",True,content_layout)


        self.export_btn=QPushButton('导出')
        self.export_btn.setStyleSheet("color: rgb(0,0,0); font-size: 20px;background-color: rgb(200,200,200);font-weight: bold;")
        self.export_btn.setFixedHeight(60)
        self.layout4.addLayout(self.export_menu)
        self.layout4.addWidget(self.export_btn, alignment=Qt.AlignBottom)

    def create_connections(self):
        self.event_manager.register_observer("SelectionChanged", self.on_selection_changed)
        #预设
        self.setting_combo_box.currentIndexChanged.connect(self.settings.load_Preset)
        self.addBtn.clicked.connect(self.settings.add_Preset)
        self.renameBtn.clicked.connect(self.settings.rename_Preset)
        self.deleteBtn.clicked.connect(lambda: self.yes_no(self.settings.remove_Preset))

        #几何
        self.geometry_menu.toggle_button.clicked.connect(self.settings.change_menu)
        self.phz.stateChanged.connect(self.settings.save_Preset)
        self.sjh.stateChanged.connect(self.settings.save_Preset)
        self.phwl.stateChanged.connect(self.settings.save_Preset)
        self.qxfx.stateChanged.connect(self.settings.save_Preset)
        self.fgfx.stateChanged.connect(self.settings.save_Preset)
        self.mp.stateChanged.connect(self.settings.save_Preset)

        #设置
        self.set_menu.toggle_button.clicked.connect(self.settings.change_menu)
        self.yd.stateChanged.connect(self.settings.save_Preset)
        def _handle_xzyy_changed():
            self.settings.save_Preset()
            self.on_exportUI_update()
        self.xzyy.stateChanged.connect(_handle_xzyy_changed)
        self.srlj.stateChanged.connect(self.settings.save_Preset)
        self.zdx.stateChanged.connect(self.settings.save_Preset)
        self.zx.combo.currentIndexChanged.connect(self.settings.save_Preset)
        
        #关键词
        self.key_menu.toggle_button.clicked.connect(self.settings.change_menu)
        self.addKey_keys.clicked.connect(self.settings.add_Keys)
        self.keys_content.itemClicked.connect(self.settings.select_keys)
        self.addKey_delete.clicked.connect(lambda: self.yes_no(self.settings.remove_keys))

        #集合
        self.sets_menu.toggle_button.clicked.connect(self.settings.change_menu)
        self.addSets_select.clicked.connect(self.add_selectSets)
        self.addSets_keys.clicked.connect(self.get_KeySets)
        self.addSets_ref.clicked.connect(self.ref_KeySets)
        self.addSets_remove.clicked.connect(lambda: self.yes_no(self.delete_Sets))

        #导出
        self.export_menu.toggle_button.clicked.connect(self.settings.change_menu)
        self.select_model.currentIndexChanged.connect(self.on_export_changed)
        self.export_fils.currentIndexChanged.connect(self.on_export_changed)
        self.export_input_prefix.textChanged.connect(self.on_exportUI_update)
        self.export_input_name.textChanged.connect(self.on_exportUI_update)
        self.export_input_suffix.textChanged.connect(self.on_exportUI_update)
        self.export_btn.clicked.connect(self.export)


        self.on_exportUI_update()
 
    def get_Text(self,title,items,_text=''):
        while True:
            # text=self.pop_msgBox(title,'输入内容',_text)
            text, ok = QInputDialog.getText( self, title, '输入内容', text=_text )
            if not ok:
                return
            
            if not text:  # 用户输入为空
                QMessageBox.warning(self, "名称不能为空", "预设名称不能为空，请重新输入。")
                continue 
            text=text.strip()       
            if text in items:
                QMessageBox.warning( self, "名称已存在", f" '{text}' 已存在。")
                continue


            return text

    def yes_no(self,callback=None):
        reply = QMessageBox.question( self, '确认删除','确定要删除吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes and callback:
            callback()

    def get_KeySets(self):
        sets=self.get_SetsItems()
        items=[]
        for i in sets:
            items.append(i['key'])
        
        key=self.get_Text('集合关键词',items)
        if not key:
            return
        
        self.add_KeySets(key)
        self.settings.add_sets(key)

    def get_KeySkeleton(self,name):
        if not cmds.objExists(name):
            return 
        skin_clusters = cmds.ls(cmds.listHistory(name), type='skinCluster')
        if not skin_clusters:
            return 
        influences = cmds.skinCluster(skin_clusters[0], query=True, influence=True)
        root_joints = set()
        for inf in influences:
            if cmds.nodeType(inf) == 'joint':
                full_path = cmds.ls(inf, l=True)[0]
                path_nodes = [n for n in full_path.split('|') if n]
                for node in path_nodes:
                    if cmds.nodeType(node) == 'joint':
                        root_joints.add(node)
                        break
        
        if not root_joints:
            return 

        skeleton=list(root_joints)[0]
        parent=cmds.listRelatives(skeleton, parent=True)
        if parent:
            if 'Skeleton' in parent[0]:
                skeleton = parent[0]
        return skeleton            

    def see_outliner(self,name):
        cmds.select(name, r=True)
        all_panels = cmds.getPanel(allPanels=True)
        for panel in all_panels:
            panel_type = cmds.getPanel(typeOf=panel)
            if panel_type == "outlinerPanel":
                cmds.outlinerEditor(panel, edit=True,showSelected=1)

    def add_KeySets(self,key):
        shapesList = cmds.ls(type="mesh")
        if not shapesList:
            return
        
        transformList = cmds.listRelatives(shapesList,parent=True,type="transform")
        items=[]
        for mesh in transformList:
            if key in mesh:
                    items.append(mesh)
        
        AB_Maya.addSets(items,'CodeV/Export/'+key)
        self.create_KeySets(items,key)  

    def ref_KeySets(self):
        self._parent.setPath()
        shapesList = cmds.ls(type="mesh")
        if not shapesList:
                    return
        models = set(cmds.listRelatives(shapesList,parent=True,type="transform"))
        cotent=self.get_SetsItems()
        print(cotent)
        for i in cotent:
            if not i['key']:
                continue
            key=i['key']
            items=[]
            for mesh in models:
                if key in mesh:
                    items.append(mesh)

            combo=i['combo']
            combo.clear()
            combo.addItems(items)
            AB_Maya.addSets(items,'CodeV/Export/'+key,em=0)
            
    def add_selectSets(self):
        items = cmds.ls(sl=1)
        if not items:
            return
        self.create_KeySets(items)
    
    def create_KeySets(self,items,key=''):
        content=QHBoxLayout()      
        content.setSpacing(3) 
        content.setContentsMargins(0, 0, 0, 5)

        export=AB_Maya.checkBox(key,True,(255,30,20))

        combo_box = QComboBox()
        if items:
            combo_box.addItems(items)
        combo_box.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        # 必须设置一个最小宽度，否则在极端压缩情况下会消失
        combo_box.setMinimumWidth(80) 
        
        # --- 视图宽度设置 ---
        # 即使本体很窄，下拉列表展开后也会有足够的宽度（例如 300px）展示长名字
        combo_box.view().setMinimumWidth(300)

        setting=AB_Maya.imgButton(28,saveData.PATH.icon+"/使用.png","将选中物体重新设置到该集合")
        select=AB_Maya.imgButton(23,saveData.PATH.icon+"/搜索.png","选择并在大纲视图的浏览")
        skeleton=AB_Maya.imgButton(23,saveData.PATH.icon+"/骨骼.png","选择并高亮骨骼")
        delete=AB_Maya.imgButton(30,saveData.PATH.icon+"/delete.png","删除该集合")

        content.addWidget(export)
        content.addWidget(combo_box,1)
        content.addWidget(setting)
        content.addWidget(select)
        content.addWidget(skeleton)
        content.addWidget(delete)

        self.sets_content.addLayout(content,alignment= Qt.AlignCenter | Qt.AlignBottom)


        def set_Layout():
            se=cmds.ls(sl=1)
            combo_box.clear()
            combo_box.addItems(se)
            if key:
                cmds.sets(cl=key)
                cmds.sets(se,e=1,fe=key)
            self.on_exportUI_update()

        def select_Layout():
            items = [combo_box.itemText(i) for i in range(combo_box.count())]
            if items:
                self.see_outliner(items)
        
        def select_skeleton():
            skeleton=self.get_KeySkeleton(combo_box.currentText())
            if skeleton:
                self.see_outliner(skeleton)

        def delete_Layout():
            isDelete=content.count()
            while content.count(): 
                child = content.takeAt(0)
                if child is not None:
                    widget = child.widget()
                    if widget is not None:
                        widget.deleteLater()
            if isDelete:
                if key:
                    cmds.delete(key)
                    self.settings.remove_Sets(key)
            
            self.on_exportUI_update()

        self.on_exportUI_update()
        setting.clicked.connect(set_Layout)
        select.clicked.connect(select_Layout)
        skeleton.clicked.connect(select_skeleton)
        delete.clicked.connect(lambda: self.yes_no(delete_Layout))
        
        combo_box.currentIndexChanged.connect(self.on_exportUI_update)
        export.stateChanged.connect(self.on_exportUI_update)

    def get_SetsItems(self):
        contents=[]
        for i in range(self.sets_content.count()):
            item = self.sets_content.itemAt(i)
            if item is not None:
                layout = item.layout()
                if layout and isinstance(layout, QHBoxLayout):
                    try:
                        export=layout.itemAt(0).widget()
                        comboBox=layout.itemAt(1).widget()
                        isExport=export.isChecked()
                        name=comboBox.currentText()
                        skeleton=self.get_KeySkeleton(name)
                        items = [comboBox.itemText(i) for i in range(comboBox.count())]
                        msg={'export':isExport,'name':name,'content':items,'key':export.text(),'combo':layout.itemAt(1).widget(),'skeleton':skeleton}
                        contents.append(msg)
                    except Exception as e:
                        print(f"获取集合项时发生错误: {e}")
                    
        return contents

    def delete_Sets(self,load=False):
         # 清空self.sets_content布局中的所有子布局
        while self.sets_content.count():
            # 获取布局中的第一个子项
            item = self.sets_content.takeAt(0)
            if item is not None:
                layout = item.layout()
                if layout is not None:
                    if not load:
                        export=layout.itemAt(0).widget()
                        key=export.text()
                        cmds.delete(key)
                        self.settings.remove_Sets(key)
                    # 清空水平布局中的所有控件
                    while layout.count():
                        child = layout.takeAt(0)
                        if child is not None:
                            widget = child.widget()
                            if widget is not None:
                                widget.deleteLater()
                    # 删除水平布局
                    layout.deleteLater()
                else:
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
        # 更新布局
        self.sets_content.update()
            
    def on_selection_changed(self):
        self.on_exportUI_update()

    def on_export_changed(self):
        self.on_exportUI_update()
        self.settings.save_Preset()

    def on_exportUI_update(self):
        export=self.get_exportName()
        self.export_label.clear()
        if not export:
            return
        if '' not  in export['name']:
            self.export_label.addItems(export['name'])

    def get_exportName(self):
        model=self.select_model.currentText()
        files=self.export_fils.currentText()
        self.export_fils.setEnabled(True)

        names=[]
        export=[]
        skeletons=[]
        
        if model == '集合导出':
            contents=self.get_SetsItems()
            if not contents:
                return
            self.export_fils.setEnabled(False)
            
            for i in contents:
                if not i['export'] or not i['content']:
                    continue
                
                names.append(i['name'])
                export.append(i['content'])
                skeletons.append(i['skeleton'])

        else:
            if model == '导出当前选择':
                se=cmds.ls(sl=1)
                temp=se

            elif model == '导出全部模型':
                shapesList = cmds.ls(type="mesh")
                if not shapesList:
                    return
                temp = cmds.listRelatives(shapesList,parent=True,type="transform")

            if files == '导出单个文件':
                try:
                    sigle=temp[0]
                    skeletons.append(self.get_KeySkeleton(sigle))
                except:
                    sigle=''
                    skeletons=''
                names.append(sigle)
            else:
                names=temp
                for i in names:
                    skeletons.append(self.get_KeySkeleton(i))
            
            export=temp

        names=self.set_exportName(names)
        return {'name':names,'export':export,'skeletons':skeletons}
 
    def set_exportName(self,export):
        prefix=self.export_input_prefix.text().strip()
        text=self.export_input_name.text().strip()
        suffix=self.export_input_suffix.text().strip()
        removes=[self.keys_content.item(i).text() for i in range(self.keys_content.count())]
        xzyy=self.xzyy.isChecked()
        result=[]

        for i in range(len(export)):
            if xzyy:
                namespace = export[i].split(':')[0]+':'
                export[i]=export[i].replace(namespace,'')
            if text:
                temp=prefix+text+suffix
                parts= re.split(r'(\d+)', temp, 1)
                if i >0:
                    if len(parts)>1:
                        name=parts[0]+str(int(parts[1])+1*i)
                    else:
                        name=temp+str(i)
                else:
                    name=temp
            else:
                name=prefix+export[i]+suffix

            keys_to_remove = []
            for i in removes:
                if '√' in i:
                    key=i.replace('√','').strip()
                    if key in name:
                        keys_to_remove.append(key)


            for i in keys_to_remove:
                try:
                    name=name.replace(i,'')
                except:
                    pass

            result.append(name)
        
        return result
    
    def export(self):
        export=self.get_exportName()
        if not export:
            return
        name=export['name']
        exports=export['export']
        if self.mp.isChecked():
            sleleton=export['skeletons']
        else:    
            sleleton=''

        self.script.model(name, exports,sleleton)