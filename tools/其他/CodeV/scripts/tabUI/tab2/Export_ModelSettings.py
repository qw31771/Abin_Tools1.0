import os
import saveData
import maya.cmds as cmds
from PySide2.QtCore import QSettings
from saveData import  导出配置键, 导出预设配置键
import AB_Maya


class ExportSettings:
    def __init__(self,data):
        config_path = os.path.join(saveData.PATH.setting, '导出设置_模型.ini')
        self.set_config=AB_Maya.getConfig('导出设置_模型')
        self.data=data
        self.test=0
        if not os.path.isfile(config_path):
            self.init()
        else:
            self.load()

    def init(self):
        preset='默认设置'
        self.data.setting_combo_box.addItem(preset)
        self.set_config.setValue(导出配置键.预设列表.value, preset)
        self.set_config.setValue(导出配置键.几何弹窗.value, 1)
        self.set_config.setValue(导出配置键.设置弹窗.value, 1)
        self.set_config.setValue(导出配置键.移除弹窗.value, 0)
        self.set_config.setValue(导出配置键.集合弹窗.value, 0)
        self.set_config.setValue(导出配置键.导出弹窗.value, 1)
        config=AB_Maya.getConfig(preset,saveData.PATH.export_presets)
        config.setValue(导出预设配置键.平滑组.value,1)
        config.setValue(导出预设配置键.三角化.value,0)
        config.setValue(导出预设配置键.平滑网络.value,0)
        config.setValue(导出预设配置键.切线法线.value,1)
        config.setValue(导出预设配置键.切割法线.value,0)
        config.setValue(导出预设配置键.蒙皮.value,0)
        config.setValue(导出预设配置键.零帧导出.value,0)
        config.setValue(导出预设配置键.删除引用.value,1)
        config.setValue(导出预设配置键.输入连接.value,0)
        config.setValue(导出预设配置键.子对象.value,1)
        config.setValue(导出预设配置键.上方轴向_模型.value,0)
        config.setValue(导出预设配置键.导出模式.value,0)
        config.setValue(导出预设配置键.导出文件.value,0)

    
    def add_Preset(self):
        presets=self.get_Presets()
        name=self.data.get_Text('添加预设',presets)
        if not name:
            return
        config=AB_Maya.getConfig(name,saveData.PATH.export_presets)
        presets.append(name)
        self.set_config.setValue(导出配置键.预设列表.value, presets)
        config.setValue(导出预设配置键.平滑组.value,1)
        config.setValue(导出预设配置键.三角化.value,0)
        config.setValue(导出预设配置键.平滑网络.value,0)
        config.setValue(导出预设配置键.切线法线.value,1)
        config.setValue(导出预设配置键.切割法线.value,0)
        config.setValue(导出预设配置键.蒙皮.value,0)
        config.setValue(导出预设配置键.零帧导出.value,0)
        config.setValue(导出预设配置键.删除引用.value,1)
        config.setValue(导出预设配置键.输入连接.value,0)
        config.setValue(导出预设配置键.子对象.value,1)
        config.setValue(导出预设配置键.上方轴向_模型.value,0)
        config.setValue(导出预设配置键.导出模式.value,0)
        config.setValue(导出预设配置键.导出文件.value,0)

        self.current_prese=name
        self.data.setting_combo_box.addItem(name)
        self.data.setting_combo_box.setCurrentText(name)
        self.set_config.setValue(导出配置键.当前预设.value, name)

    def load_Preset(self):
        prese=self.data.setting_combo_box.currentText()
        currentConfig=AB_Maya.getConfig(prese,saveData.PATH.export_presets)
        self.Loading=True

        self.data.phz.setChecked(int(currentConfig.value(导出预设配置键.平滑组.value)))
        self.data.sjh.setChecked(int(currentConfig.value(导出预设配置键.三角化.value)))
        self.data.phwl.setChecked(int(currentConfig.value(导出预设配置键.平滑网络.value)))
        self.data.qxfx.setChecked(int(currentConfig.value(导出预设配置键.切线法线.value)))
        self.data.fgfx.setChecked(int(currentConfig.value(导出预设配置键.切割法线.value)))
        self.data.mp.setChecked(int(currentConfig.value(导出预设配置键.蒙皮.value)))
        self.data.yd.setChecked(int(currentConfig.value(导出预设配置键.零帧导出.value)))
        self.data.xzyy.setChecked(int(currentConfig.value(导出预设配置键.删除引用.value)))
        self.data.srlj.setChecked(int(currentConfig.value(导出预设配置键.输入连接.value)))
        self.data.zdx.setChecked(int(currentConfig.value(导出预设配置键.子对象.value)))
        self.data.zx.combo.setCurrentIndex(int(currentConfig.value(导出预设配置键.上方轴向_模型.value))) 
        self.data.select_model.setCurrentIndex(int(currentConfig.value(导出预设配置键.导出模式.value))) 
        self.data.export_fils.setCurrentIndex(int(currentConfig.value(导出预设配置键.导出文件.value)))
        self.data.delete_Sets(True)

        self.Loading=False
        self.current_prese=prese
        self.set_config.setValue(导出配置键.当前预设.value, prese)

        keys=self.get_Sets()
        for i in keys:
            try:
                sets=cmds.sets(i,q=1)
                self.data.create_KeySets(sets,i)
            except:
                self.data.add_KeySets(i)

    def save_Preset(self):
        if self.Loading:
            return
        
        currentConfig=AB_Maya.getConfig(self.current_prese,saveData.PATH.export_presets)
        currentConfig.setValue(导出预设配置键.平滑组.value,int(self.data.phz.isChecked()))
        currentConfig.setValue(导出预设配置键.三角化.value,int(self.data.sjh.isChecked()))
        currentConfig.setValue(导出预设配置键.平滑网络.value,int(self.data.phwl.isChecked()))
        currentConfig.setValue(导出预设配置键.切线法线.value,int(self.data.qxfx.isChecked()))
        currentConfig.setValue(导出预设配置键.切割法线.value,int(self.data.fgfx.isChecked()))
        currentConfig.setValue(导出预设配置键.蒙皮.value,int(self.data.mp.isChecked()))
        currentConfig.setValue(导出预设配置键.零帧导出.value,int(self.data.yd.isChecked()))
        currentConfig.setValue(导出预设配置键.删除引用.value,int(self.data.xzyy.isChecked()))
        currentConfig.setValue(导出预设配置键.输入连接.value,int(self.data.srlj.isChecked()))
        currentConfig.setValue(导出预设配置键.子对象.value,int(self.data.zdx.isChecked()))
        currentConfig.setValue(导出预设配置键.上方轴向_模型.value,self.data.zx.combo.currentIndex())
        currentConfig.setValue(导出预设配置键.导出模式.value,self.data.select_model.currentIndex())
        currentConfig.setValue(导出预设配置键.导出文件.value,self.data.export_fils.currentIndex())

    def get_Presets(self):
        temp=self.set_config.value(导出配置键.预设列表.value) or []
        values=AB_Maya.toList(temp)
        return values
    
    def rename_Preset(self):
        currentText=self.data.setting_combo_box.currentText()
        presets=self.get_Presets()
        newName=self.data.get_Text('重命名预设',presets,currentText)
        if not newName:
            return
        index=self.data.setting_combo_box.currentIndex()
        self.data.setting_combo_box.setItemText(index, newName)
        presets[index] = newName
        print(self.current_prese,newName)
        path_name=os.path.join(saveData.PATH.export_presets, self.current_prese+".ini")
        path_newName=os.path.join(saveData.PATH.export_presets, newName+".ini")
        print(path_name,path_newName)
        os.rename(path_name, path_newName)
        self.set_config.setValue(导出配置键.预设列表.value, presets)
        self.set_config.setValue(导出配置键.当前预设.value, newName)
        self.current_prese=newName

    def remove_Preset(self):
        presets=self.get_Presets()
        if len(presets) <=1:
            self.default_Preset()
            return
        presets.remove(self.current_prese)
        path=os.path.join(saveData.PATH.export_presets, self.current_prese+".ini")
        os.remove(path)
        current_index=self.data.setting_combo_box.currentIndex()
        self.data.setting_combo_box.removeItem(current_index)
        self.current_prese=self.data.setting_combo_box.currentText()
        self.set_config.setValue(导出配置键.预设列表.value,presets)
        self.set_config.setValue(导出配置键.当前预设.value,self.current_prese)

    def default_Preset(self):
        if self.current_prese != '默认设置':
            self.rename_Preset('默认设置')
        self.Loading=True
        self.data.phz.setChecked(1)
        self.data.sjh.setChecked(0)
        self.data.phwl.setChecked(0)
        self.data.qxfx.setChecked(1)
        self.data.fgfx.setChecked(0)
        self.data.mp.setChecked(0)
        self.data.yd.setChecked(0)
        self.data.xzyy.setChecked(1)
        self.data.srlj.setChecked(0)
        self.data.zdx.setChecked(1)
        self.data.zx.combo.setCurrentIndex(0) 
        self.data.select_model.setCurrentIndex(0) 
        self.data.export_fils.setCurrentIndex(0)
        self.Loading=False
        self.save_Preset()

    def change_menu(self):
        self.set_config.setValue(导出配置键.几何弹窗.value,int(self.data.geometry_menu.geometry_content.isVisible()))
        self.set_config.setValue(导出配置键.设置弹窗.value,int(self.data.set_menu.geometry_content.isVisible()))
        self.set_config.setValue(导出配置键.移除弹窗.value,int(self.data.key_menu.geometry_content.isVisible()))
        self.set_config.setValue(导出配置键.集合弹窗.value,int(self.data.sets_menu.geometry_content.isVisible()))
        self.set_config.setValue(导出配置键.导出弹窗.value,int(self.data.export_menu.geometry_content.isVisible()))

    def load_menu(self):
        self.data.geometry_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.几何弹窗.value)))
        self.data.set_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.设置弹窗.value)))
        self.data.key_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.移除弹窗.value)))
        self.data.sets_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.集合弹窗.value)))
        self.data.export_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.导出弹窗.value)))
        keys=self.get_Keys()
        self.data.keys_content.addItems(keys)

    def get_Keys(self):
        temp=self.set_config.value(导出配置键.关键词列表.value) or []
        values=AB_Maya.toList(temp)
        return values
     
    def add_Keys(self):
        keys=self.get_Keys()
        key=self.data.get_Text('添加剔除关键字',keys)
        self.data.keys_content.addItems([key])
        keys.append(key)
        self.set_config.setValue(导出配置键.关键词列表.value,keys)

    def select_keys(self):
        item=self.data.keys_content.currentItem()
        index=self.data.keys_content.currentRow()
        key=item.text()
        if '√' not in key:
            name=key+'  √'
        else:
            name=key.replace('√','')
        item.setText(name.strip())
        keys=self.get_Keys()
        keys[index]=name
        self.data.on_exportUI_update()
        self.set_config.setValue(导出配置键.关键词列表.value,keys)

    def remove_keys(self):
        selected_items = self.data.keys_content.selectedItems()
        keys=self.get_Keys()
        for item in selected_items:
            key=item.text()
            keys.remove(key)
            row = self.data.keys_content.row(item)
            self.data.keys_content.takeItem(row)

        self.set_config.setValue(导出配置键.关键词列表.value,keys)

    def add_sets(self,key):
        currentConfig=AB_Maya.getConfig(self.current_prese,saveData.PATH.export_presets)
        sets=self.get_Sets()
        sets.append(key)
        currentConfig.setValue(导出预设配置键.导出集合.value,sets)

    def get_Sets(self):
        currentConfig=AB_Maya.getConfig(self.current_prese,saveData.PATH.export_presets)
        temp=currentConfig.value(导出预设配置键.导出集合.value) or []
        values=AB_Maya.toList(temp)
        return values

    def remove_Sets(self,key=''):
        if not key:
            return
        currentConfig=AB_Maya.getConfig(self.current_prese,saveData.PATH.export_presets)
        sets=self.get_Sets()
        sets.remove(key)
        currentConfig.setValue(导出预设配置键.导出集合.value,sets)

    def load(self):
        #记录预设
        presets=self.get_Presets()
        #文件中的预设，去除拓展名
        files_items = os.listdir(saveData.PATH.export_presets)
        if len(presets)!=len(files_items):
            files_presets=[]
            for i in files_items:
                file, ext=os.path.splitext(i)
                files_presets.append(file)

            #新增
            if len(presets)<len(files_items):
                for add in files_presets:
                    if add not in presets:
                        presets.append(add)
            #减少
            else:
                for move in presets:
                    if move not in files_presets:
                        presets.remove(move)

        self.data.setting_combo_box.addItems(presets)
        self.set_config.setValue(导出配置键.预设列表.value,presets)
        self.load_menu()
        self.current_prese=self.set_config.value(导出配置键.当前预设.value)
        self.data.setting_combo_box.setCurrentText(self.current_prese)
        self.load_Preset()

    


