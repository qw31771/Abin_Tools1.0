import maya.cmds as cmds
import maya.mel as mel
plug=advPath
script=cmds.internalVar(userScriptDir=True)  #C:/Users/v_jbinyu/Documents/maya/2022/zh_CN/scripts/


melLsit=[
[script+"/Abin_Tools/scripts/AdvancedSkeleton5.mel","source \"{}\";AdvancedSkeleton5;".format(plug+"AdvancedSkeleton5.mel")],
[script+"/Abin_Tools/scripts/Biped.mel","source \"{}\";".format(plug+"AdvancedSkeleton5Files/Selector/biped.mel")],
[script+"/Abin_Tools/scripts/Face.mel","source \"{}\";".format(plug+"AdvancedSkeleton5Files/Selector/face.mel")],
[script+"/Abin_Tools/scripts/Picker.mel","source \"{}\";".format(plug+"AdvancedSkeleton5Files/picker/picker.mel")]
]
for p,c in melLsit:
    with open(p, 'w', encoding='ANSI') as f:
                    f.write(c)


