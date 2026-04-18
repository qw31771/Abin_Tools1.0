import maya.cmds as cmds

cmds.lockNode('initialShadingGroup', l=0, lockUnpublished=0)

cmds.lockNode('defaultTextureList1', l=False, lockUnpublished=False)


print('Broken Lambert shader fixed')