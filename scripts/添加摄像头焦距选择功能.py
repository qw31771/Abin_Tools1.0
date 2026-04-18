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
    if not cmds.objExists("Camera_FK_ctrl"):
        cmds.warning("该场景不适用")
        return

    if cmds.objExists("Camera_FK_ctrl.focalLength"):
        cmds.warning("不能重复添加")
        return
        

    try:
        cmds.setAttr("FPCameraShape.focalLength",l=0)
        cmds.addAttr("Camera_FK_ctrl",ln="focalLength",at="enum",en="70:56")
        cmds.setAttr("Camera_FK_ctrl.focalLength",e=1,keyable=1)
        cond=cmds.shadingNode("condition",n="Camera_focalLength_select",au=1)
        cmds.connectAttr("Camera_FK_ctrl.focalLength",cond+".firstTerm")
        cmds.setAttr(cond+".colorIfTrueR",25.025)
        cmds.setAttr(cond+".colorIfFalseR",32.956)
        cmds.connectAttr(cond+".outColorR","FPCameraShape.focalLength")
        cmds.select("Camera_FK_ctrl")
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