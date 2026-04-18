import maya.cmds as cmds
from functools import wraps

#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds.undoInfo(closeChunk=True)
        return result
    return wrap


@make_undo
def script():
    import maya.cmds as cmds
    import maya.mel as mel
    winds = 'setVtx_UI'
    def setVtxMainWins():
        if cmds.window(winds,ex = True):
            cmds.deleteUI(winds)
            
        cmds.window(winds , t = u'setVtx_Tool')
        cmds.columnLayout( adjustableColumn=True,rowSpacing=10,w=200)
        cmds.separator( style='out' )
        cmds.text("currentModel",l="model:")
        cmds.progressBar("progressControl",maxValue=10, width=200)
        cmds.showWindow(winds)
    setVtxMainWins()
    
    tvList=[]
    vtxs = cmds.ls(sl=True,fl=1)
    index=vtxs[0].rfind(".")
    name=vtxs[0][0:index]
    maxV=0
    
    
    source_model="source_"+name
    source_skinCls = mel.eval("findRelatedSkinCluster" +"(\""+ source_model +"\")")
    model=name
    skinCls = mel.eval("findRelatedSkinCluster" +"(\""+ model +"\")")

    for vtx in vtxs:
        skinJoint = cmds.skinCluster(skinCls, query=True, inf=vtx)
        maxV+=len(skinJoint)
    cmds.progressBar("progressControl", edit=True,endProgress=1)
    cmds.progressBar("progressControl", edit=True,minValue=0,maxValue=maxV)
    
    for vtx in vtxs:
        skinValue = cmds.skinPercent(skinCls, vtx, query=True, value=True)
        skinJoint = cmds.skinCluster(skinCls, query=True, inf=vtx)
        
        souece_skinJoint = cmds.skinCluster(source_skinCls, query=True, inf="souece_"+vtx)
        
        for i in range(0,len(skinJoint)):
            cmds.progressBar("progressControl", edit=True, step=1)
            if skinJoint[i] in souece_skinJoint :
                value=skinValue[i]-0.1
                tvList.append((skinJoint[i],value))
                
        cmds.skinPercent(source_skinCls,"source_"+vtx,tv=tvList)
        
    if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)


script()