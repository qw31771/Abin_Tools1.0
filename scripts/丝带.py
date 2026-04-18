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
    import Ribbon_UI
    from importlib import reload
    reload(Ribbon_UI)
    Ribbon_UI.setRibbon_UI()


script()