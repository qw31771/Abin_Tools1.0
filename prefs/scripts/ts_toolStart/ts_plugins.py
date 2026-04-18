import maya.cmds as cmds
import maya.mel as mel
import os
import inspect
# plug=cmds.internalVar(mayaInstallDir=True)+"/plug-ins/" #C:/Program Files/Autodesk/Maya2022
script=cmds.internalVar(userScriptDir=True)  #C:/Users/v_jbinyu/Documents/maya/2022/zh_CN/scripts/
# '''
# adv5插件
# '''
# adv_plug=script+"Abin_Tools/scripts/AdvancedSkeleton5.mel"
# if not os.path.exists(adv_plug):
#     print("-------------------安装adv插件-----------------")
#     adv_path=current+"/AdvancedSkeleton5/install.mel"
#     print("aaaaaaaaaaaaaaaa",adv_path)
#     # mel.eval(' source \"{}\" '.format(adv_path))

# '''
# studiolibrary插件
# '''
# studiolibrary_plug=script+"Abin_Tools/scripts/studiolibrary.py"
# if not os.path.exists(studiolibrary_plug):
#     print("-------------------安装studiolibrary插件-----------------")
#     studiolibrary_path=current+"/studiolibrary-2.9.6.b3/install.mel"
#     # mel.eval(' source \"{}\" '.format(studiolibrary_path))

