import os
import saveData
import maya.cmds as cmds
from PySide2.QtCore import QSettings
from saveData import  导出配置键, 导出预设配置键
import AB_Maya


class ExportSettings:
    def __init__(self,data):
        config_path = os.path.join(saveData.PATH.setting, '导出设置_动画.ini')
        self.set_config=AB_Maya.getConfig('导出设置_动画')
        self.data=data
        if not os.path.isfile(config_path):
            self.init()
        else:
            self.load()

    def init(self):
        self.set_config.setValue(导出配置键.导出弹窗_动画.value, False)
        self.set_config.setValue(导出配置键.设置弹窗_动画.value, False)

        self.set_config.setValue(导出预设配置键.导出选择.value,0)
        self.set_config.setValue(导出预设配置键.移动到原点.value,1)
        self.set_config.setValue(导出预设配置键.烘焙动画.value,1)
        self.set_config.setValue(导出预设配置键.上方轴向_动画.value,0)
        self.set_config.setValue(导出预设配置键.模式_动画.value,0)

    def load(self):
        self.Loading = True
        self.data.anim_Export_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.导出弹窗_动画.value)))
        self.data.set_menu.setVis_ChageArrow(int(self.set_config.value(导出配置键.设置弹窗_动画.value)))
        skips=self.get_SkipJoint()
        self.data.get_advanced_root_skeletons(skips)
        self.data.anim_export.setCurrentIndex(int(self.set_config.value(导出预设配置键.导出选择.value)))
        self.data.anim_yd.setChecked(int(self.set_config.value(导出预设配置键.移动到原点.value)))
        self.data.anim_xzyy.setChecked(int(self.set_config.value(导出预设配置键.烘焙动画.value)))
        self.data.anim_zx.combo.setCurrentIndex(int(self.set_config.value(导出预设配置键.上方轴向_动画.value))) 
        self.data.anim_pd.combo.setCurrentIndex(int(self.set_config.value(导出预设配置键.模式_动画.value))) 
        self.Loading = False

    
    def save_Preset(self):
        if self.Loading:
            return
        
        self.set_config.setValue(导出配置键.导出弹窗_动画.value,int(self.data.anim_Export_menu.geometry_content.isVisible()))
        self.set_config.setValue(导出配置键.设置弹窗_动画.value,int(self.data.set_menu.geometry_content.isVisible()))

        self.set_config.setValue(导出预设配置键.导出选择.value,int(self.data.anim_export.currentIndex()))
        self.set_config.setValue(导出预设配置键.移动到原点.value,int(self.data.anim_yd.isChecked()))
        self.set_config.setValue(导出预设配置键.烘焙动画.value,int(self.data.anim_xzyy.isChecked()))
        self.set_config.setValue(导出预设配置键.上方轴向_动画.value,int(self.data.anim_zx.combo.currentIndex()))
        self.set_config.setValue(导出预设配置键.模式_动画.value,int(self.data.anim_pd.combo.currentIndex()))


    def get_Times(self):
        # 1. 获取当前时间（当前滑块所在帧）
        current_time = cmds.currentTime(query=True)

        # 2. 获取时间轴范围（滑块可见范围）
        start_time = cmds.playbackOptions(query=True, minTime=True)
        end_time = cmds.playbackOptions(query=True, maxTime=True)

        # 3. 获取动画全长范围（整个场景的限制范围）
        animation_start = cmds.playbackOptions(query=True, animationStartTime=True)
        animation_end = cmds.playbackOptions(query=True, animationEndTime=True)

        print(f"当前时间: {current_time}")
        print(f"播放范围: {start_time} 到 {end_time}")
        print(f"动画全长: {animation_start} 到 {animation_end}")

    def get_SkipJoint(self):
        try:
            temp=self.set_config.value(导出预设配置键.跳过骨骼.value)
            skips=AB_Maya.toList(temp)
        except:
            skips=[]    
        return skips 

    def add_SkipJoint(self,items):
        skips=self.get_SkipJoint()
        names = [item.text() for item in items]
        for joint in names:
            if joint not in skips:
                skips.append(joint)
                self.set_config.setValue(导出预设配置键.跳过骨骼.value,skips)

        self.data.get_advanced_root_skeletons(skips)

    def remove_SkipJoint(self,items):
        skips=self.get_SkipJoint()
        names = [item.text() for item in items]
        for joint in names:
            if joint in skips:
                skips.remove(joint)
        self.set_config.setValue(导出预设配置键.跳过骨骼.value,skips)
        self.data.get_advanced_root_skeletons(skips)