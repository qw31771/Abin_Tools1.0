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
    
    def transfer_weights_to_bone():
        # 获取当前选择
        selection = cmds.ls(selection=True)
        
        if not selection:
            cmds.warning("请先选择面和骨骼")
            return
        
        # 分离面和骨骼
        faces = [s for s in selection if ".f[" in s]
        joints = [s for s in selection if ".f[" not in s]
        
        
        if not faces or not joints:
            cmds.warning("选择无效：请同时选择面(组件)和骨骼(对象)")
            return
        
        if len(joints) > 1:
            cmds.warning("只能选择一个骨骼")
            return
        
        joint = joints[0]
        
        # 获取网格对象
        mesh = faces[0].split('.')[0]
        
        # 检查皮肤簇
        skin_cluster = mel.eval('findRelatedSkinCluster "{}"'.format(mesh))
        if not skin_cluster:
            cmds.warning("网格未绑定蒙皮: {}".format(mesh))
            return
        
        # 检查骨骼是否在影响列表中
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
        if joint not in influences:
            cmds.warning("骨骼不是蒙皮影响对象: {}".format(joint))
            return
        
        # 获取选定面的顶点
        vertices = set()
        for face in faces:
            face_vertices = cmds.polyListComponentConversion(face, fromFace=True, toVertex=True)
            vertices.update(cmds.ls(face_vertices, flatten=True))
        
        # 为选定顶点设置权重
        for vtx in vertices:
            # 获取当前权重信息
            weights = cmds.skinPercent(skin_cluster, vtx, query=True, value=True)
            trans = cmds.skinPercent(skin_cluster, vtx, query=True, transform=None)
            
            # 构建新权重字典（除目标骨骼外权重归零）
            new_weights = {}
            for inf, wt in zip(trans, weights):
                new_weights[inf] = 1.0 if inf == joint else 0.0
            
            # 应用新权重
            cmds.skinPercent(skin_cluster, vtx, transformValue=list(new_weights.items()))
        
        cmds.select(faces + [joint])
        print("权重转移成功! 面顶点权重已完全转移到骨骼: {}".format(joint))
    
    # 执行函数
    transfer_weights_to_bone()


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