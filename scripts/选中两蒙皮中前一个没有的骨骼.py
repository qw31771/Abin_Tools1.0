from functools import wraps

#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        import maya.cmds as cmds
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds.undoInfo(closeChunk=True)
        return result
    return wrap


@make_undo
def script():
    import maya.mel as mel   
    se=cmds.ls(sl=1)
    mesh1=se[0]
    mesh2=se[1]
    skin1=mel.eval("findRelatedSkinCluster" +"(\""+ mesh1 +"\")")
    skinJoint1 = cmds.skinCluster(skin1, query=True,influence=1)
    
    skin2=mel.eval("findRelatedSkinCluster" +"(\""+ mesh2 +"\")")
    skinJoint2 = cmds.skinCluster(skin2, query=True,influence=1)
    
    print(skinJoint1,skinJoint2)
    
    difference = list(set(skinJoint2) - set(skinJoint1))
    
    cmds.select(difference)


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