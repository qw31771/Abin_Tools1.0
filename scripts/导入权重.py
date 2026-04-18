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
    sl=cmds.ls(sl=1)
    path="E:/skin/test/"
    export=0
    for i in sl:
        name=i+".xml"
        mode="XML"
        method="index"
        skinCls = mel.eval("findRelatedSkinCluster" +"(\""+ i +"\")")
        if export:
            mel.eval(f"deformerWeights -export -deformer \"{skinCls}\" -format \"{mode}\" -path \"{path}\" \"{name}\";")
        else:
            try:
                mel.eval(f"deformerWeights -import -method \"{method}\" -deformer \"{skinCls}\" -format \"{mode}\" -path \"{path}\" \"{name}\";skinCluster -e -forceNormalizeWeights \"{skinCls}\";")
                cmds.warning("导入成功")
            except:
                cmds.warning("导入失败")


script()