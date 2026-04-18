import os
import saveData
import common
from PySide2.QtCore import QSettings

class ExportSettings:
    def __init__(self,data):
        config_path = os.path.join(saveData.PATH.setting, "model_export_settings.ini")
        self.config=QSettings(config_path, QSettings.IniFormat)
        self.config.setIniCodec('UTF-8')
        self.data=data

        if not os.path.isfile(config_path):
            self.init()
        else:
            self.ininSetting()
            self.change_Preset()
       
    def init(self):
        pre_item=['默认设置']
        self.data.setting_combo_box.addItems(pre_item)
        self.config.setValue('presets', pre_item)
        self.config.setValue('current_preset', pre_item[0])

        self.config.setValue('geometry_pop', 1)
        self.config.setValue('set_pop', 1)

        remove_item=['','无','全选','_LOD0','_Head','_Hair']
        self.data.remove_box.addItems(remove_item)
        self.config.setValue('remove_pop', 1)
        self.config.setValue('remove_keys', remove_item)

        export_item=['','无','全选','_LOD0','_LOD1','_LOD2','_LOD3','_DT','_LOD']
        self.data.model_box.addItems(export_item)
        self.config.setValue('export_pop', 1)
        self.config.setValue('export_keys', export_item)

        self.config.setValue('select_model', 0)
        self.config.setValue('export_fils', 0)

        self.add_Preset()
    
    def add_Preset(self):
        self.reset_Default()
        self.saveAll()
    
    def change_Preset(self):
        pre=self.data.setting_combo_box.currentText()
        currentConfig=self.getConfig(pre)
        try:
            phz=    int(currentConfig.value('phz'))
            sjh=    int(currentConfig.value('sjh'))
            phwl=   int(currentConfig.value('phwl'))
            qxfx=   int(currentConfig.value('qxfx'))
            fgfx=   int(currentConfig.value('fgfx'))
            yd=     int(currentConfig.value('yd'))
            xzyy=   int(currentConfig.value('xzyy'))
            srlj=   int(currentConfig.value('srlj'))
            zdx=    int(currentConfig.value('zdx'))
            zx=     int(currentConfig.value('zx'))
            select_model=     int(currentConfig.value('select_model'))
            export_fils=     int(currentConfig.value('export_fils'))
            remove_key=currentConfig.value('remove_key')
            export_key=currentConfig.value('export_key')

            self.data.phz.setChecked(phz)
            self.data.sjh.setChecked(sjh)
            self.data.phwl.setChecked(phwl)
            self.data.qxfx.setChecked(qxfx)
            self.data.fgfx.setChecked(fgfx)
            self.data.yd.setChecked(yd)
            self.data.xzyy.setChecked(xzyy)
            self.data.srlj.setChecked(srlj)
            self.data.zdx.setChecked(zdx)
            self.data.zx.combo.setCurrentIndex(zx) 
            self.data.select_model.setCurrentIndex(select_model) 
            self.data.export_fils.combo.setCurrentIndex(export_fils) 
            self.data.remove_key.textE.setPlainText(' , '.join(remove_key))
            self.data.export_key.textE.setPlainText(' , '.join(export_key))
            self.saveAll()
            print(pre,"加载预设成功")
        except:
            print(pre,"加载预设失败")
            pass

    def ininSetting(self):
        preset=self.config.value('presets')
        presets=self.getListItems(preset)
        self.data.setting_combo_box.addItems(presets)
        current_pre=self.config.value('current_preset')
        index = self.data.setting_combo_box.findText(current_pre)
        self.data.setting_combo_box.setCurrentIndex(index)

        geometry_pop=int(self.config.value('geometry_pop'))
        self.data.geometry_menu.setVis_ChageArrow(geometry_pop)

        set_pop=int(self.config.value('set_pop'))
        self.data.set_menu.setVis_ChageArrow(set_pop)


        remove_pop=int(self.config.value('remove_pop'))
        self.data.key_menu.setVis_ChageArrow(remove_pop)
        remove_key=self.config.value('remove_keys')
        remove_keys=self.getListItems(remove_key)
        self.data.remove_box.addItems(remove_keys)

        export_pop=int(self.config.value('export_pop'))
        self.data.export_menu.setVis_ChageArrow(export_pop)
        export_key=self.config.value('export_keys')
        export_keys=self.getListItems(export_key)
        self.data.model_box.addItems(export_keys)
        
    def saveAll(self):
        self.saveSetting()
        self.savePre()

    def saveSetting(self):
        pre_combo=common.get_all_item_texts(self.data.setting_combo_box)
        presets=pre_combo['items']
        current_preset=pre_combo['currentName']

        remove_combo=common.get_all_item_texts(self.data.remove_box)
        remove_keys=remove_combo['items']

        
        export_combo=common.get_all_item_texts(self.data.model_box)
        export_keys=export_combo['items']

        self.config.setValue('presets',presets)
        self.config.setValue('current_preset',current_preset)
        self.config.setValue('remove_keys',remove_keys)
        self.config.setValue('export_keys',export_keys)

    def saveMenu_Vis(self):
        remove_pop=1 if self.data.key_menu.geometry_content.isVisible() else 0
        export_pop=1 if self.data.export_menu.geometry_content.isVisible() else 0
        geometry_pop=1 if self.data.geometry_menu.geometry_content.isVisible() else 0
        set_pop=1 if self.data.set_menu.geometry_content.isVisible() else 0

        self.config.setValue('remove_pop',remove_pop)
        self.config.setValue('export_pop',export_pop)
        self.config.setValue('geometry_pop',geometry_pop)
        self.config.setValue('set_pop',set_pop)

    def savePre(self):
        current_preset=self.data.setting_combo_box.currentText()
        currentConfig=self.getConfig(current_preset)
        currentConfig.setValue('phz',   self.checked(self.data.phz))
        currentConfig.setValue('sjh',   self.checked(self.data.sjh))
        currentConfig.setValue('phwl', self.checked(self.data.phwl))
        currentConfig.setValue('qxfx', self.checked(self.data.qxfx))
        currentConfig.setValue('fgfx', self.checked(self.data.fgfx))
        currentConfig.setValue('yd',     self.checked(self.data.yd))
        currentConfig.setValue('xzyy',     self.checked(self.data.xzyy))
        currentConfig.setValue('srlj', self.checked(self.data.srlj))
        currentConfig.setValue('zdx',   self.checked(self.data.zdx))
        currentConfig.setValue('zx', self.data.zx.combo.currentIndex() )
        currentConfig.setValue('select_model', self.data.select_model.currentIndex() )
        currentConfig.setValue('export_fils', self.data.export_fils.combo.currentIndex() )

        remove_text=self.data.remove_key.textE.toPlainText().strip()
        remove_keys = [item for item in remove_text.split(' , ') if item]
        currentConfig.setValue('remove_key', remove_keys)

        export_text=self.data.export_key.textE.toPlainText().strip()
        export_keys = [item for item in export_text.split(' , ') if item]
        currentConfig.setValue('export_key', export_keys)

    def checked(self,data):
        result=1
        if not data.isChecked():
           result=0

        return result

    def reset_Default(self):
        self.data.phz.setChecked(1)
        self.data.sjh.setChecked(0)
        self.data.phwl.setChecked(0)
        self.data.qxfx.setChecked(1)
        self.data.fgfx.setChecked(0)
        self.data.yd.setChecked(0)
        self.data.xzyy.setChecked(1)
        self.data.srlj.setChecked(0)
        self.data.zdx.setChecked(1)
        self.data.zx.combo.setCurrentIndex(0) 
        self.data.select_model.setCurrentIndex(0) 
        self.data.export_fils.combo.setCurrentIndex(0) 
        self.data.remove_key.textE.setText('')
        self.data.export_key.textE.setText('')

    def change_Checked(self,data,att):
        pre=self.data.setting_combo_box.currentText()
        Config=os.path.join(saveData.PATH.enport_presets, pre+".ini")
        currentConfig=QSettings(Config, QSettings.IniFormat)
        currentConfig.setValue(att, self.checked(data))
   
    def change_combo(self,data,att):
        pre=self.data.setting_combo_box.currentText()
        currentConfig=self.getConfig(pre)
        currentConfig.setValue(att, data.currentIndex())

    def getConfig(self,name):
        path=os.path.join(saveData.PATH.enport_presets, name+".ini")
        config=QSettings(path, QSettings.IniFormat)
        config.setIniCodec('UTF-8')
    
        return config
    
    def renamePre(self,name,newname):
       current_index=self.data.setting_combo_box.currentIndex()
       self.data.setting_combo_box.setItemText(current_index, newname)
       path_name=os.path.join(saveData.PATH.enport_presets, name+".ini")
       path_newName=os.path.join(saveData.PATH.enport_presets, newname+".ini")
       os.rename(path_name, path_newName)
       self.saveSetting()

    def removePre(self):
        current=self.data.setting_combo_box.currentText()
        current_index=self.data.setting_combo_box.currentIndex()
        self.data.setting_combo_box.removeItem(current_index)
        path_name=os.path.join(saveData.PATH.enport_presets, current+".ini")
        os.remove(path_name)
        self.saveSetting()
    
    def getListItems(self,items):
        if isinstance(items, list):
            return items  # 已为列表，直接返回
        else:
            return [items] 