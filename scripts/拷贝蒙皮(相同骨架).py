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
    vtxs = cmds.ls(sl=True,fl=1)
    index=vtxs[0].rfind(".")
    name=vtxs[0][0:index]
    maxV=0
    cmds.progressBar("progressControl", edit=True,endProgress=1)
    cmds.progressBar("progressControl", edit=True,minValue=0,maxValue=len(vtxs))
    cmds.text("currentModel",e=1,l=name)
    
    for vtx in vtxs:
        cmds.select(vtx)
        mel.eval("CopyVertexWeights;")
        cmds.select("source_"+vtx)
        mel.eval("PasteVertexWeights;")
        cmds.progressBar("progressControl", edit=True, step=1)
    
    if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)


script()