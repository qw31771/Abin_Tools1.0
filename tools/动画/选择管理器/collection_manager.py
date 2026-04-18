import os
import json
import common
from maya import cmds
from PySide2 import QtWidgets, QtCore, QtGui

class CollectionManager(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CollectionManager, self).__init__(parent)
        self.setWindowTitle("集合管理器")
        try:
            _w=common.scaled_size(600)
            _h=common.scaled_size(600)
        except:
            _w=600
            _h=600

        self.setMinimumSize(_w, _h)
        self.resize(_w,_h)
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)

        # 初始化配置
        self.config_path = os.path.join(script_directory, "collection_config.json")
        self.collections = {}  # 数据结构：{"集合名": {"objects": [], "tags": {}}}
        self.window_settings = {}
        
        # 窗口属性
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMinimizeButtonHint
        )
        
        # 初始化界面
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.load_data()
        self.load_window_settings()

    def create_widgets(self):
        """创建界面控件"""
        # 集合列表
        self.collection_list = QtWidgets.QListWidget()
        self.collection_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        # 对象树（支持拖拽排序）
        self.object_tree = QtWidgets.QTreeWidget()
        self.object_tree.setHeaderLabels(["对象名称", "标签"])
        self.object_tree.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.object_tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.object_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        total_width = self.object_tree.width()
        fixed_width = int(total_width * 0.55)  # 20% 宽度给标签列
        self.object_tree.setColumnWidth(0, fixed_width)

        
        # 操作按钮
        self.btn_add_col = QtWidgets.QPushButton("新建集合")
        self.btn_del_col = QtWidgets.QPushButton("删除集合")
        self.btn_rename_col = QtWidgets.QPushButton("重命名")
        self.btn_add_objs = QtWidgets.QPushButton("添加选中对象")
        self.btn_del_objs = QtWidgets.QPushButton("删除选中对象")
        self.btn_clean = QtWidgets.QPushButton("清理无效对象")
        self.btn_select_all = QtWidgets.QPushButton("选择全部")  # 新增按钮
        # self.btn_save_path = QtWidgets.QPushButton("设置路径")
        
        # 标签控件
        self.tag_edit = QtWidgets.QLineEdit()
        self.tag_edit.setPlaceholderText("输入标签（多个用逗号分隔）")
        self.btn_add_tag = QtWidgets.QPushButton("添加标签")
        
        # 路径显示
        # self.path_label = QtWidgets.QLabel(f"保存路径: {self.config_path}")
        # self.path_label.setMinimumWidth(400)

    def create_layout(self):
        """布局管理"""
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # 顶部路径设置
        path_layout = QtWidgets.QHBoxLayout()
        # path_layout.addWidget(self.path_label)
        path_layout.addStretch()
        # path_layout.addWidget(self.btn_save_path)
        main_layout.addLayout(path_layout)
        
        # 主体内容
        content_layout = QtWidgets.QHBoxLayout()
        
        # 左侧面板
        left_panel = QtWidgets.QVBoxLayout()
        left_panel.addWidget(QtWidgets.QLabel("集合列表"))
        left_panel.addWidget(self.collection_list)
        
        # 集合操作按钮
        col_btn_layout = QtWidgets.QHBoxLayout()
        col_btn_layout.addWidget(self.btn_add_col)
        col_btn_layout.addWidget(self.btn_del_col)
        col_btn_layout.addWidget(self.btn_rename_col)
        left_panel.addLayout(col_btn_layout)
        
        # 右侧面板
        right_panel = QtWidgets.QVBoxLayout()
        right_panel.addWidget(QtWidgets.QLabel("集合内容"))
        right_panel.addWidget(self.object_tree)
        
        # 标签操作
        tag_layout = QtWidgets.QHBoxLayout()
        tag_layout.addWidget(self.tag_edit)
        tag_layout.addWidget(self.btn_add_tag)
        right_panel.addLayout(tag_layout)
        
        # 对象操作按钮
        obj_btn_layout = QtWidgets.QHBoxLayout()
        obj_btn_layout.addWidget(self.btn_add_objs)
        obj_btn_layout.addWidget(self.btn_del_objs)
        obj_btn_layout.addWidget(self.btn_clean)
        obj_btn_layout.addWidget(self.btn_select_all)
        right_panel.addLayout(obj_btn_layout)
        
        content_layout.addLayout(left_panel, stretch=0)
        content_layout.addLayout(right_panel, stretch=10)
        main_layout.addLayout(content_layout, stretch=1)

    def create_connections(self):
        """信号连接"""
        # 基础功能
        self.btn_add_col.clicked.connect(self.add_collection)
        self.btn_del_col.clicked.connect(self.delete_collection)
        self.btn_rename_col.clicked.connect(self.rename_collection)
        self.btn_add_objs.clicked.connect(self.add_objects)
        self.btn_del_objs.clicked.connect(self.delete_objects)
        self.btn_clean.clicked.connect(self.clean_invalid_objects)
        # self.btn_save_path.clicked.connect(self.set_save_path)
        self.collection_list.itemSelectionChanged.connect(self.refresh_object_list)
        self.collection_list.itemDoubleClicked.connect(self.select_all_objects)
        
        # 新增功能
        self.object_tree.itemSelectionChanged.connect(self.select_scene_objects)
        self.object_tree.model().rowsMoved.connect(self.handle_drag_drop)
        self.object_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.btn_add_tag.clicked.connect(self.add_tags)
        self.btn_select_all.clicked.connect(self.select_all_objects)
        
        # 窗口事件
        self.destroyed.connect(self.save_window_settings)

    # region 核心功能方法
    def add_collection(self):
        """添加新集合"""
        selected = [obj for obj in cmds.ls(selection=True) if cmds.objExists(obj)]
        name, ok = QtWidgets.QInputDialog.getText(self, "新建集合", "输入集合名称:")
        if ok and name:
            if name not in self.collections:
                self.collections[name] = {"objects": [], "tags": {}}
                self.collection_list.addItem(name)
                current_row = self.collection_list.count() - 1
                self.collection_list.setCurrentRow(current_row)
                
                self.add_objects(selected)
                self.save_data()
            else:
                cmds.warning(f"集合 {name} 已存在！")

    def delete_collection(self):
        """删除当前选中集合"""
        current_item = self.collection_list.currentItem()
        if current_item:
            name = current_item.text()
            reply = QtWidgets.QMessageBox.question(
                self, "确认删除", f"确定要删除集合 '{name}' 吗？",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                del self.collections[name]
                self.collection_list.takeItem(self.collection_list.row(current_item))
                self.save_data()

    def rename_collection(self):
        """重命名集合"""
        current_item = self.collection_list.currentItem()
        if current_item:
            old_name = current_item.text()
            new_name, ok = QtWidgets.QInputDialog.getText(
                self, "重命名集合", "新名称:", text=old_name
            )
            if ok and new_name and new_name != old_name:
                if new_name in self.collections:
                    cmds.warning(f"集合 {new_name} 已存在！")
                    return
                self.collections[new_name] = self.collections.pop(old_name)
                current_item.setText(new_name)
                self.save_data()

    def add_objects(self,sel=None):
        """添加选中对象到当前集合"""
        current_col = self.collection_list.currentItem()
        
        if not current_col:
            cmds.warning("请先选择一个集合！")
            return
        if sel:
            selected=sel
        else:
            selected = [obj for obj in cmds.ls(selection=True) if cmds.objExists(obj)]
        if not selected:
            cmds.warning("没有有效的选中对象！")
            return
        
        cmds.select(selected, replace=True)
        col_name = current_col.text()
        
        for obj in selected:
            if obj not in self.collections[col_name]["objects"]:
                self.collections[col_name]["objects"].append(obj)
                if obj not in self.collections[col_name]["tags"]:
                    self.collections[col_name]["tags"][obj] = []
        
        self.refresh_object_list()
        self.save_data()

    def delete_objects(self):
        """删除选中对象"""
        current_col = self.collection_list.currentItem()
        if not current_col:
            return
        
        selected_items = self.object_tree.selectedItems()
        if not selected_items:
            return
        
        remove_objs = [item.text(0) for item in selected_items]
        col_name = current_col.text()
        self.collections[col_name]["objects"] = [
            obj for obj in self.collections[col_name]["objects"]
            if obj not in remove_objs
        ]
        
        # 清理标签
        for obj in remove_objs:
            if obj in self.collections[col_name]["tags"]:
                del self.collections[col_name]["tags"][obj]
        
        self.refresh_object_list()
        self.save_data()

    def refresh_object_list(self):
        """刷新对象列表显示"""
        self.object_tree.clear()
        current_col = self.collection_list.currentItem()
        if current_col:
            col_name = current_col.text()
            for obj in self.collections[col_name]["objects"]:
                item = QtWidgets.QTreeWidgetItem(self.object_tree)
                item.setText(0, obj)
                item.setText(1, ", ".join(self.collections[col_name]["tags"].get(obj, [])))
                
                if not cmds.objExists(obj):
                    item.setForeground(0, QtGui.QColor(255, 0, 0))
                    item.setToolTip(0, "场景中不存在该对象")
    # endregion

    # region 新增功能方法
    def select_scene_objects(self):
        """选中场景中的对应对象"""
        selected_items = self.object_tree.selectedItems()
        valid_objects = []
        
        for item in selected_items:
            obj_name = item.text(0)
            if cmds.objExists(obj_name):
                valid_objects.append(obj_name)
        
        if valid_objects:
            cmds.select(valid_objects, replace=True)

    def select_all_objects(self):
        """选择集合内全部有效对象"""
        current_col = self.collection_list.currentItem()
        if not current_col:
            return
        
        col_name = current_col.text()
        valid_objects = [obj for obj in self.collections[col_name]["objects"] if cmds.objExists(obj)]
        
        if valid_objects:
            cmds.select(valid_objects, replace=True)
            self.object_tree.selectAll()
        else:
            cmds.warning("当前集合中没有有效对象")



    def handle_drag_drop(self):
        """处理拖拽排序（仅限同级排序）"""
        current_col = self.collection_list.currentItem()
        if current_col:
            col_name = current_col.text()
            # 确保所有项目都是顶层项
            new_order = [self.object_tree.topLevelItem(i).text(0) 
                       for i in range(self.object_tree.topLevelItemCount())]
            self.collections[col_name]["objects"] = new_order
            self.save_data()
    # endregion

    # region 其他功能方法
    def clean_invalid_objects(self):
        """清理无效对象"""
        current_col = self.collection_list.currentItem()
        if not current_col:
            return
            
        col_name = current_col.text()
        valid_objects = []
        removed = 0
        
        for obj in self.collections[col_name]["objects"]:
            if cmds.objExists(obj):
                valid_objects.append(obj)
            else:
                removed += 1
                if obj in self.collections[col_name]["tags"]:
                    del self.collections[col_name]["tags"][obj]
                
        self.collections[col_name]["objects"] = valid_objects
        self.refresh_object_list()
        self.save_data()
        cmds.warning(f"已清理 {removed} 个无效对象")

    def add_tags(self):
        """添加标签"""
        selected = self.object_tree.selectedItems()
        tags = [t.strip() for t in self.tag_edit.text().split(",") if t.strip()]
        
        if not selected or not tags:
            return
            
        current_col = self.collection_list.currentItem()
        col_name = current_col.text()
        
        for item in selected:
            obj_name = item.text(0)
            current_tags = set(self.collections[col_name]["tags"].get(obj_name, []))
            current_tags.update(tags)
            self.collections[col_name]["tags"][obj_name] = list(current_tags)
            item.setText(1, ", ".join(current_tags))
        
        self.save_data()
        self.tag_edit.clear()

    def show_context_menu(self, pos):
        """右键菜单"""
        menu = QtWidgets.QMenu()
        remove_tag_action = menu.addAction("移除标签")
        action = menu.exec_(self.object_tree.mapToGlobal(pos))
        
        if action == remove_tag_action:
            self.remove_tags()

    def remove_tags(self):
        """移除标签"""
        selected = self.object_tree.selectedItems()
        if not selected:
            return
            
        current_col = self.collection_list.currentItem()
        col_name = current_col.text()
        
        for item in selected:
            obj_name = item.text(0)
            if obj_name in self.collections[col_name]["tags"]:
                del self.collections[col_name]["tags"][obj_name]
                item.setText(1, "")
        
        self.save_data()
    # endregion

    # region 数据持久化
    def set_save_path(self):
        """设置保存路径"""
        new_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "选择保存文件", self.config_path, "JSON Files (*.json)"
        )
        if new_path:
            self.config_path = new_path
            self.path_label.setText(f"保存路径: {self.config_path}")
            self.save_data()

    def save_data(self):
        """保存所有数据"""
        data = {
            "collections": self.collections,
            "window": self.window_settings
        }
        try:
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            cmds.warning(f"保存失败: {str(e)}")

    def load_data(self):
        """加载数据"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.collections = data.get("collections", {})
                    # 兼容旧版本数据格式
                    for col in self.collections.values():
                        if "tags" not in col:
                            col["tags"] = {}
                    self.collection_list.addItems(self.collections.keys())
            except Exception as e:
                cmds.warning(f"加载失败: {str(e)}")
    # endregion

    # region 窗口设置记忆
    def load_window_settings(self):
        """加载窗口设置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    if "window" in data:
                        window_settings = data["window"]
                        # 设置窗口位置
                        if "x" in window_settings and "y" in window_settings:
                            self.move(
                                int(window_settings["x"]), 
                                int(window_settings["y"])
                            )
                        # 设置窗口尺寸
                        if "width" in window_settings and "height" in window_settings:
                            self.resize(
                                int(window_settings["width"]),
                                int(window_settings["height"])
                            )
            except Exception as e:
                print(f"加载窗口设置失败: {str(e)}")

    def save_window_settings(self):
        """保存窗口设置"""
        try:
            # 获取当前窗口几何数据
            self.window_settings = {
                "x": self.x(),
                "y": self.y(),
                "width": self.width(),
                "height": self.height()
            }
        except Exception as e:
            print(f"保存窗口设置失败: {str(e)}")

    def closeEvent(self, event):
        """窗口关闭事件（增强版）"""
        # 确保窗口在正常状态下保存尺寸
        if not self.isMaximized() and not self.isMinimized():
            self.save_window_settings()
        else:
            # 如果处于最大化/最小化状态，恢复常规状态后获取尺寸
            self.showNormal()
            self.save_window_settings()
        self.save_data()
    # endregion

def show():
    """显示窗口"""
    global dialog
    
    # 获取Maya主窗口
    maya_window = next(
        w for w in QtWidgets.QApplication.topLevelWidgets() 
        if w.objectName() == "MayaWindow"
    )
    
    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass
        
    dialog = CollectionManager(parent=maya_window)
    dialog.show()

# 使用方法：
# 1. 将代码保存为 collection_manager.py
# 2. 在Maya脚本编辑器中运行：
# import collection_manager
# collection_manager.show()