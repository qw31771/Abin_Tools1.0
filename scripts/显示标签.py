from functools import wraps
import maya.cmds as cmds

# 装饰器
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

    sl=cmds.ls(sl=1)

    if sl:
        cmds.select(sl[0],hi=1)
        resuls=cmds.ls(sl=1)
        cmds.select(sl[0])
        for i in resuls:
            try:
                lable=cmds.getAttr(i+".drawLabel")
                cmds.setAttr(i+".drawLabel",not lable)
                cmds.setAttr(i+".type",18)
                cmds.setAttr(i+".otherType",i,type="string")
            except:
                pass


    def _expose_to_global():
        import __main__  # 获取 Maya 主模块
        main_globals = __main__.__dict__
        for func in list_user_functions():
            main_globals[func.__name__] = func  # 注入到 Maya 全局作用域
            # globals()[func.__name__] = func     # 同时注入当前模块（可选）
    def list_user_functions():
        functions = []
        import inspect
        for name, obj in globals().items():
            if inspect.isfunction(obj) and obj.__module__ == __name__:
                functions.append(obj)  # 改为返回函数对象而非名称
        return functions
    _expose_to_global()

script()