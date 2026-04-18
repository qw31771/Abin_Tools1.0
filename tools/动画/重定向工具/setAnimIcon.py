import maya.cmds as cmds
source=getPlace

# 1. 获取当前工具架名称（如 "Polygons"）
current_shelf = cmds.tabLayout("ShelfLayout", query=True, selectTab=True)

# 2. 创建按钮并指定图标
cmds.shelfButton(
     parent=current_shelf,  # 当前工具架
    label="动画重定向",
    command='''import sys
source = "{}"
if source not in sys.path: 
	sys.path.append(source)
import newBakeAnimationUI
newBakeAnimationUI.bake_Animation_UI()'''.format(source),

    image=source+"/icon.png",  
)
