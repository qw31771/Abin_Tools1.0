from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import os
import treeWidgetScript
import MYMAYA
import custom_ui

class MainTreeWidget(QWidget):
    
    def __init__(self, parent):
        super(MainTreeWidget,self).__init__(parent)
        #获取父窗口
        self.get_parent=parent
        self.hb_layout=QHBoxLayout(self)

        self.tree_weight=Tree_Weight() 

        self.hb_layout.addWidget(self.tree_weight)
        self.hb_layout.setContentsMargins(0,0,0,0)

    def searchFile(self,text):
        self.tree_weight.searchFile(text)

class Tree_Weight(QTreeWidget):
    mainMaxCount=100
    subMaxCount=100

    def __init__(self, parent=None):
        super(Tree_Weight,self).__init__(parent)
        
        self.settings=MYMAYA.SAVE.TQSETTING
        self.settings2=MYMAYA.SAVE.TQICONSETTING
        self.prefix=" "
        self.get_parent=parent
        # 连接 itemChanged 信号到自定义重命名槽函数
        self.itemChanged.connect(self.on_item_changed)


        self.script=treeWidgetScript.Script(self)

        # print(MYMAYA.MYSCREEN.WIDTH)
        if MYMAYA.MYSCREEN.WIDTH==1920:
            with open(MYMAYA.PATH.PREFS+"/scripts/qss/subWin_treeWidgetQss24.qss","r") as f:
                self.treeW=f.read()
        else:
            with open(MYMAYA.PATH.PREFS+"/scripts/qss/subWin_treeWidgetQss.qss","r") as f:
                self.treeW=f.read()

        self.setFrameStyle(QFrame.NoFrame)
        self.setRootIsDecorated(False)
        self.setStyleSheet(self.treeW)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.RightPopMenu=self.initRightMenu()
        self.setExpandsOnDoubleClick(False)
        self.initConfig()
        self.timer=QTimer(self)
        self.itemClicked['QTreeWidgetItem*','int'].connect(self.script.itemLeftSingClicked)
        self.itemDoubleClicked['QTreeWidgetItem*','int'].connect(self.mouseDoubleClickEvent)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested['QPoint'].connect(self.popMenu)
        self.setDragEnabled(True) #开启拖拽
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeWidget.InternalMove)#限定拖拽在内部fitemLeftSingClicked
        
        # self.setDefaultDropAction(Qt.MoveAction)#设置移动模式
    def mouseDoubleClickEvent(self,event):
        return

    #根据保存文件初始化
    def initTree(self,config,itemExpanded=None):
        for i in range(0,len(config[0])):
            pItem = self.getTreeItemMsg(str(i))
            mainItem=QTreeWidgetItem(self)
            mainItem.setText(0, self.prefix+pItem[0])
            icon=QIcon(pItem[1])
            mainItem.setIcon(0, icon)
            mainItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable |Qt.ItemIsDragEnabled )
            for j in range(0,len(config[1][i])):
                index=str(i)+"/"+str(j)
                item=self.getTreeItemMsg(index)
                subItem=QTreeWidgetItem(mainItem)
                subItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable  )
                subItem.setText(0, self.prefix+item[0])
                icon=QIcon(item[1])
                subItem.setIcon(0, icon)
                self.setSubItemQss(subItem)

                # # print(item)
        
    #获取itme的名字和icon地址
    def getTreeItemMsg(self,index):
        name=self.settings.value(index+"/name")
        # print("treeWidgetUI_getTreeItemMsg:"+name)
        icon=self.settings2.value("/"+name)

        path=MYMAYA.PATH.IOCONS+"/"
        try:
            if not os.path.exists(path+icon):
                icon="/空.png"  
        except:
            icon="/空.png"
        iconName=path+icon
        return (name,iconName)

    #子元素UI样式
    def setSubItemQss(self,item:QTreeWidgetItem):
        if MYMAYA.MYSCREEN.WIDTH==1920:
            item.setSizeHint(0,QSize(10,28))
            font=QFont("楷体",10,False)
        else:
            item.setSizeHint(0,QSize(10,40))
            font=QFont("楷体",10,False)
        item.setFont(0,font)

    #初始化右键菜单
    def initRightMenu(self):
        popMenuu = QMenu(self)
        
        popMenuu.setStyleSheet("QMenu{\
                                    border: 2px solid rgb(40,40,40);\
                                    background: rgb(40,40,40);\
                                    border-radius: 2px;\
                                    }\
                           QMenu::item:selected{\
                                    border: 1px solid rgb(197,147,251);\
                                    background-color:rgb(130,107,180);\
                                    }")
        popMenuu.setAttribute(Qt.WA_TranslucentBackground)

        return popMenuu

    #右键弹出菜单
    def popMenu(self,point):
        item=self.itemAt(point)

        if item:
            parent=item.parent()
            
            if not parent:
                actions=self.treeW_AddMenu(self.RightPopMenu,["   重命名","   新建","   打开","   删除","   图标"])
                actions[0].triggered.connect(lambda:self.script.itemRename(item))
                actions[1].triggered.connect(lambda:self.script.itemNewFile(item))
                actions[2].triggered.connect(lambda:self.script.openFile(MYMAYA.PATH.TOOLS+"/"+self.script.getItemName(item)))
                actions[3].triggered.connect(lambda:self.script.itemDelete(item))
                actions[4].triggered.connect(lambda:self.script.itemIcon(item))

            else:
                actions=self.treeW_AddMenu(self.RightPopMenu,["   重命名","   删除","   图标","   收藏","   删除脚本"])
                actions[0].triggered.connect(lambda:self.script.itemRename(item))
                actions[1].triggered.connect(lambda:self.script.itemDelete(item))
                actions[2].triggered.connect(lambda:self.script.itemIcon(item))
                actions[3].triggered.connect(lambda:self.script.addCollect(item))
                actions[4].triggered.connect(lambda:self.script.deleteScript(self.script.getItemName(item)))

            
        else:
            actions=self.treeW_AddMenu(self.RightPopMenu,["   新建","   打开"," 脚本目录"," 图标目录"])
            actions[0].triggered.connect(lambda:self.script.itemNewFile())
            actions[1].triggered.connect(lambda:self.script.openFile(MYMAYA.PATH.TOOLS))
            actions[2].triggered.connect(lambda:self.script.openFile(MYMAYA.PATH.SCRIPTS))
            actions[3].triggered.connect(lambda:self.script.openFile(MYMAYA.PATH.IOCONS))

        self.RightPopMenu.exec_(QCursor.pos())

    #给弹出菜单添加词条
    def treeW_AddMenu(self,popMenu,nameArray):
        popMenu.clear()
        actions=[]
        for i in nameArray:
            action=QAction(i, self)

            icon=i.strip()+".png"
            # print(i.strip())
            action.setIcon(QIcon(MYMAYA.PATH.PREFS+"/icons/"+icon))

            actions.append(action)
            popMenu.addAction(action)
            popMenu.addSeparator()

        return actions

    #测试初始写入文件夹中的文件目录（顺序电脑默认
    def initConfig(self):
        if  os.path.exists(MYMAYA.SAVE.WIN_TINFO):
            print("初始化步骤1：已有配置表:")
            self.script.Refresh()
            return
        
        print("初始化步骤1：已有配置表:\n ----------配置表初始化")
        self.settings.clear()
        self.settings2.clear()
        files=os.listdir(MYMAYA.PATH.TOOLS)
        print(files)
        for i in range(0,len(files)):
            subFiles=os.listdir(MYMAYA.PATH.TOOLS+"/"+files[i])
            print(MYMAYA.PATH.TOOLS+"/"+files[i])
            self.settings.beginGroup(str(i))

            icon=files[i]+".png"
            self.settings.setValue("name",files[i])
            self.settings2.setValue(files[i],icon)

            for j in range(0,len(subFiles)):
                self.settings.beginGroup(str(j))
                icon=subFiles[j]+".png"
                self.settings.setValue("name",subFiles[j])
                self.settings2.setValue(subFiles[j],icon)
                self.settings.endGroup()
            
            self.settings.endGroup()
        config=self.script.getSettringLength(self.settings)
        self.initTree(config)
    
    # #开始拖拽
    def dragEnterEvent(self, event):
        currentSelect=self.currentItem() 
        if not currentSelect and currentSelect.parent():
            return
        
        count=self.topLevelItemCount()
        super(Tree_Weight, self).dragEnterEvent(event)
        
    #拖拽结束
    def dropEvent(self,event):
        item = self.itemAt(event.pos())
        # super(Tree_Weight, self).dropEvent(event)
        if item  :
           
            super(Tree_Weight, self).dropEvent(event)
            self.script.resetConfig()

        else:
            event.ignore()

    #搜索文件
    def searchFile(self,text):
        # print(text)
        print(self.script.find_and_expand_item(text))

    #重命名
    def on_item_changed(self, item, column):
        if not  item.data(1, Qt.EditRole):
            item.setData(1, Qt.EditRole, item.text(column))
            return
        
        if column == 0 :
            if item.text(column).strip() != item.data(1, Qt.EditRole).strip() and item.data(1, Qt.EditRole):
                if item.parent():
                    path=MYMAYA.PATH.TOOLS+"/"+item.parent().text(0).strip()
                else:
                    path=MYMAYA.PATH.TOOLS
                files=os.listdir(path)
                if item.text(column).strip() in files  or item.text(column).strip() == "":
                    # print("文件夹已存在",item.data(1, Qt.EditRole))
                    item.setText(column, item.data(1, Qt.EditRole))
                    dialog= custom_ui.popMsg("错误","名字不能重复或为空",parent=self)
                    if dialog.exec_():
                        print('用户点击了"确定"按钮。')
                    else:
                        print('用户点击了"取消"按钮。')
                else:
                    text = item.text(column)
                    if not text.startswith(self.prefix):
                        # print("没有前缀添先添加前缀")
                        item.setText(column, self.prefix + text)
                    else:
                        # print("重命名已经添加前缀")
                        # files=os.listdir(MYMAYA.PATH.TOOLS)
                        # if item.data(1, Qt.EditRole).strip() in files :
                            # print(item.data(1, Qt.EditRole),"重命名-->",item.text(column))
                        self.script.fileRename(item.data(1, Qt.EditRole).strip(),item.text(column).strip(),item.parent())

                item.setData(1, Qt.EditRole, item.text(column))

    def show_input_dialog(self,title):
        # 创建一个 LongTextDialog 实例，并显示对话框
        dialog = custom_ui.LongTextDialog(parent=self,text=title)
        if dialog.exec_():
            # 如果用户点击了确定按钮
            code = dialog.get_text()
            typ=dialog.get_type()
            fileName=MYMAYA.PATH.SCRIPTS+"/"+title+typ
            # print(fileName)
            # 写入文件
            if ".py" in typ:
                source_file=MYMAYA.PATH.PREFS+"/scripts/startCode.py"
                with open(source_file, 'r', encoding='utf-8') as source_file:
                    startCode = source_file.read()

                lines = code.splitlines()
                content=""
                for i in lines:
                    line="    "+i+'\n'
                    content+=line
                

                startCode=startCode.replace("repleceCode",content)

                with open(fileName, 'w', encoding='utf-8') as f:
                    f.write(startCode)
            else:
                with open(fileName, 'w', encoding='ANSI') as f:
                    f.write(code)
            # print('用户输入的长文本是:\n'+ code)

    #通过名字获得item
    def getParentItem(self,name):
        count=self.topLevelItemCount()
        for i in range(0,count):
            item=self.topLevelItem(i)
            if name == item.text(0).strip():
                if item.isExpanded():
                    return True
        return False

    #item展开
    def setItemExpanded(self,itemList):
        count=self.topLevelItemCount()
        for name in itemList:
            for i in range(0,count):
                item=self.topLevelItem(i)
                if name == item.text(0).strip():
                    item.setExpanded(True)
                
 