from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import maya.cmds as cmds
import os
import MYMAYA
import maya.mel as mel
from sys import path
import custom_ui
import stat
import shutil

class Script(QTreeWidget):
    def __init__(self, parent):
        self.tree=parent
        self.winSetting=MYMAYA.SAVE.QSETTING
        self.settings=MYMAYA.SAVE.TQSETTING
        self.settings2=MYMAYA.SAVE.TQICONSETTING
        self.mainMax=self.tree.mainMaxCount
        self.subMax=self.tree.subMaxCount

    #获得元素名称
    def getItemName(self,item:QTreeWidgetItem):
            name=item.text(0).strip()
            return name

    # lastTimer=None
    #单击展开
    def itemLeftSingClicked(self,item:QTreeWidgetItem,column):
            
            name=self.getItemName(item)
            parent=item.parent()
            if not parent:
                print('左键单击[{}]->展开/收缩'.format(name))
                item.setExpanded(not item.isExpanded())
            else:
                self.itemLeftClickedScript(item)

    #单击运行
    def itemLeftClickedScript(self,item:QTreeWidgetItem):
        name=self.getItemName(item)
        
        #找自己
        files=os.listdir(MYMAYA.PATH.SCRIPTS)

        isRun=False
        _path=""
        ispy=False
        for file in files:
            f=file[0:file.rfind('.')]
            if name == f:
                isRun=True
                _path=MYMAYA.PATH.SCRIPTS+"/"+file
                if 'py' in file:
                    ispy=True
        # print(_path)

        if not isRun:
            print("需要添加启动脚本")
            self.tree.show_input_dialog(item.text(0).strip())
        else:
            print('左键单击子[{}]->运行'.format(name))
            if ispy:
                # self.addSysPath(item)
                exec(open(_path, encoding='utf-8').read(),globals())
            else:
                # with open(_path, 'r', encoding='utf-8') as _path:
                #      content = _path.read()
                mel.eval(' source \"{}\" '.format(_path))
                # mel.eval(' {} '.format(content))
            self.winSetting.setValue("last",_path)
            # mel.eval('source \"{}\"'.format(_path))


                   
        #新建元素
    
    #新建文件夹
    def itemNewFile(self,item=None):
        _path = MYMAYA.PATH.TOOLS
        if item:
            file="/"+item.text(0).strip()+"/"
        else:
            file="/"

        _path = MYMAYA.PATH.TOOLS+file
        files=os.listdir(_path)
        print(files)

        # 创建新文件夹
        new_folder = "新建文件夹"
        number=""
        for i in range(1,self.mainMax):
            index=0
            for f in files:
                if new_folder in f:
                    #相同，退出循环
                    if str(i) in f:
                        break
                index+=1
            
            if index == len(files):
                number=" ("+str(i)+")"
                break
        


        # print(_path+new_folder+number)
        os.makedirs(_path+new_folder+number)
        self.Refresh()
        # if item:
        #     item.setExpanded(True)

    #打开文件
    def openFile(self,_path):
        os.startfile(_path)

    def deleteScript(self,_path):
        filenames=os.listdir(MYMAYA.PATH.SCRIPTS)
        deletePath=""
        for i in filenames:
            if _path in i :
                deletePath=MYMAYA.PATH.SCRIPTS+"/"+i
                break
        try:
            os.remove(deletePath)
        except:
            pass

    #更换图标
    def itemIcon(self,item:QTreeWidgetItem):
        multipleFilters = "png (*.png);;jpg (*.jpg);;"
        filepath = cmds.fileDialog2(fileFilter=multipleFilters,
                                    dialogStyle=1, fileMode=1, returnFilter=True,cap="选择图标",
                                    dir=MYMAYA.PATH.IOCONS,okc="选择")

        
        if filepath:
            icon=QIcon(filepath[0])
            item.setIcon(0,icon)
            index=filepath[0].rfind("/")
            png=filepath[0][index+1:len(filepath[0])]
            self.resetConfig(item.text(0).strip(),png)

    #添加到收藏
    def addCollect(self,item:QTreeWidgetItem):
        name=item.text(0).strip()
        _path=MYMAYA.PATH.TOOLS+"/收藏/"+name
        try:
            os.makedirs(_path)
            self.Refresh()
        except:
            pass

    #删除
    def itemDelete(self,item:QTreeWidgetItem):
        print("删除")
        name=item.text(0).strip()
        _path = MYMAYA.PATH.TOOLS
        try:
            parent=item.parent().text(0).strip()
        except:
            parent=""

        try:
            os.rmdir(_path+"/"+parent+"/"+name)
            if parent!="":
                isDelete=True
                config=self.getSettringLength(self.settings)
                index=config[0].index(parent)
                # print(config,index)
                for i in range(len(config[1])):
                    if i != index:
                        if name in config[1][i]:
                            isDelete=False
                            break
                if isDelete:
                    filenames=os.listdir(MYMAYA.PATH.SCRIPTS)
                    stf=""
                    for i in filenames:
                        stf_Index=i.rfind('.')
                        if name == i[0:stf_Index]:
                            stf=i[stf_Index:len(i)]
                            os.remove(MYMAYA.PATH.SCRIPTS+"/"+name+stf)
                            break
            self.Refresh()
        except:
            dialog= custom_ui.popMsg("警告","文件夹内有插件本体文件\n删除后其他同名插件不可使用",parent=self.tree)
            if dialog.exec_():
                try:
                    dir_path=_path+"/"+parent+"/"+name
                    shutil.rmtree(dir_path)
                    self.Refresh()
                except:
                    try:
                        #修改权限
                        os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                        # 再次尝试删除
                        shutil.rmtree(dir_path)
                        self.Refresh()
                    except:
                        pass
    
    #Item重命名
    def itemRename(self,item:QTreeWidgetItem):
        item.setFlags(item.flags() |  Qt.ItemIsEditable)
        self.tree.editItem(item)
    
    #文件夹重命名
    def fileRename(self,original_dirname,new_dirname,parent):
        # 原始文件夹名和路径
        original_path = MYMAYA.PATH.TOOLS
        parentName=""
        if parent:
            parentName=parent.text(0).strip()
            original_path = MYMAYA.PATH.TOOLS+"/"+parentName

        # 完整的原始文件夹路径和新的文件夹路径
        original_full_path = os.path.join(original_path, original_dirname)
        new_full_path = os.path.join(original_path, new_dirname)

        # 使用os.rename函数来重命名文件夹
        try:
            print(parent,original_dirname,new_dirname)

            config=self.getSettringLength(self.settings)
            png=self.settings2.value("/"+original_dirname)
            if parentName:
                pareintIndex=config[0].index(parentName)
                childIndex=config[1][pareintIndex].index(original_dirname)
                
                self.settings.beginGroup(str(pareintIndex))
                self.settings.beginGroup(str(childIndex))
                self.settings.setValue("name",new_dirname)
                self.settings.endGroup()
                self.settings.endGroup()
                #同时修改启动文件的名字
                filenames=os.listdir(MYMAYA.PATH.SCRIPTS)
                stf=""
                for i in filenames:
                    if original_dirname in i :
                        stf=i[i.rfind('.'):len(i)]
                        original_full_path2 = os.path.join(MYMAYA.PATH.SCRIPTS, original_dirname+stf)
                        new_full_path2 = os.path.join(MYMAYA.PATH.SCRIPTS, new_dirname+stf)
                        os.rename(original_full_path2, new_full_path2)
                        break
                    
            else:
                parentName=original_dirname
                pareintIndex=config[0].index(parentName)
                self.settings.beginGroup(str(pareintIndex))
                self.settings.setValue("name",new_dirname)
                self.settings.endGroup()

            self.settings2.setValue(new_dirname,png)
            os.rename(original_full_path, new_full_path)

            print(f"文件夹 {original_dirname} 已被重命名为 {new_dirname}")
        except FileNotFoundError:
            print(f"文件夹 {original_dirname} 不存在。")
        except OSError as e:
            print(f"发生错误: {e.strerror}")

    # 查找并展开特定的项（这里只是一个示例，你需要根据自己的条件来查找）
    def find_and_expand_item(self,name):
        for index in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(index)
            for i in range(item.childCount()):
                if name.lower() in item.child(i).text(0).lower():
                    item.setExpanded(True)
                    self.tree.setCurrentItem(item.child(i))
                    self.tree.scrollToItem(item.child(i))
                    return True
                
        return False

    #刷新
    def Refresh(self):
        print(" ----------刷新")
        files=os.listdir(MYMAYA.PATH.TOOLS)
        config=self.getSettringLength(self.settings)
        itemExpanded=[]
        icons=[]
        self.settings.clear() 
        index=0
        #先写入存在的文件夹
        for main in config[0]:
            if main in files:
                self.settings.beginGroup(str(index))
                self.settings.setValue("name",main)
                icons.append([main,self.settings2.value(main)])
                subFiles=os.listdir(MYMAYA.PATH.TOOLS+"/"+main)
                #判断是否展开
                if self.tree.getParentItem(main):
                    itemExpanded.append(main)

                for i in range(0,len(subFiles)):
                    self.settings.beginGroup(str(i))
                    self.settings.setValue("name",subFiles[i])
                    icons.append([subFiles[i],self.settings2.value(subFiles[i])])
                    self.settings.endGroup()
                self.settings.endGroup()
                index+=1
        #找出不存在的文件夹
        for main in files:
            if not main in config[0]:
                self.settings.beginGroup(str(index))
                self.settings.setValue("name",main)
                subFiles=os.listdir(MYMAYA.PATH.TOOLS+"/"+main)
                icons.append([main,main+".png"])
                for i in range(0,len(subFiles)):
                    self.settings.beginGroup(str(i))
                    self.settings.setValue("name",subFiles[i])
                    icons.append([subFiles[i],subFiles[i]+".png"])
                    self.settings.endGroup()
                self.settings.endGroup()
                index+=1
        self.settings2.clear()
        for name,png in icons:
            self.settings2.setValue(name,png)
            
        self.tree.clear()
        self.tree.initTree(self.getSettringLength(self.settings),itemExpanded)
        self.tree.setItemExpanded(itemExpanded)

    #将窗口的自定义顺序写入,改变顺序触发
    def resetConfig(self,_name="",_icon=""):
        # newName=self.tree.currentItem().text(0).strip()
        # if  not newName:
        #     cmds.warning("名字不能为空")
        #     return
        self.settings.clear()
        print("重新写入配置表")
        count=self.tree.topLevelItemCount()
        for i in range(0,count):
            pItem=self.tree.topLevelItem(i)
            childCount=pItem.childCount()
            pName=pItem.text(0).strip()
            print(pName)
            self.settings.beginGroup(str(i))
            self.settings.setValue("name",pName)
            for j in range(0,childCount):
                item=pItem.child(j)
                name=item.text(0).strip()
                print(name)
                self.settings.beginGroup(str(j))
                self.settings.setValue("name",name)
                self.settings.endGroup()
            self.settings.endGroup()
        
        if _name == "":
            return
        # if self.tree.currentItem().parent():
        #     pName=self.tree.currentItem().parent().text(0).strip()
        #     self.settings2.setValue(pName+"/"+_name,_icon)
        # else:   
        self.settings2.setValue(_name,_icon)
        #改名
        # os.rename(os.path.join(MYMAYA.PATH.TOOLS,self.oldName),os.path.join(MYMAYA.PATH.TOOLS,newName))

    #获取setting配置
    def getSettringLength(self,setting):
        mainName=[]
        subName=[]
        for index in range(0,self.mainMax):
            name=setting.value(str(index)+"/name")
            sub=[]
            if name:
                mainName.append(name)
                for subIndex in range(0,self.subMax):
                    name=setting.value(str(index)+"/"+str(subIndex)+"/name")
                    if name:
                        sub.append(name)
                    else:
                        break
                subName.append(sub)
            else:
                # count=index
                break
                
        return [mainName,subName]
    
    #通过路径解析名字
    def filePathToName(self,_path):
        index=_path.rfind("/")
        name=_path[index+1:len(_path)]
        return name
  
    #添加到变量环境
    def addSysPath(self,item):
        name=item.text(0).strip()
        # _path=MYMAYA.PATH.TOOLS+"/"+item.parent().text(0).strip()+"/"+name
        _path=MYMAYA.PATH.TOOLS
        # folders_with_py=[]
        for dirpath, dirnames, filenames in os.walk(_path):
            # 检查文件夹中是否有.py文件
            if any(filename.endswith('.py') for filename in filenames):
                # 如果是，则将文件夹路径添加到结果列表中
                # folders_with_py.append(dirpath)
                if dirpath not in path:
                    path.append(dirpath)
                    print("添加到环境变量",name)
                else:
                    print("已经添加到环境变量",name)

        