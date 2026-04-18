from functools import wraps

# 装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        import maya.cmds as cmds
        cmds.undoInfo(openChunk=True)
        result = func(*args, **kwargs)
        cmds.undoInfo(closeChunk=True)
        return result
    return wrap

@make_undo
def script():
    import maya.cmds as cmds
    
    def transfer_skin_weights_remove_source_weights():
        """
        将选中骨骼的权重转移到最后一个选择的骨骼
        源骨骼权重清零但保留在绑定中
        选择顺序：先选源骨骼，最后选目标骨骼
        """
        # 获取当前选择的骨骼
        selected_joints = cmds.ls(selection=True, type='joint')
        
        # 检查选择数量
        if len(selected_joints) < 2:
            cmds.warning("请至少选择两个骨骼（最后一个为接收权重的目标骨骼）")
            return
        
        # 确定源骨骼和目标骨骼
        source_joints = selected_joints[:-1]  # 除最后一个外的所有骨骼
        target_joint = selected_joints[-1]    # 最后一个骨骼
        
        # 获取所有皮肤簇节点
        skin_clusters = set()
        for joint in selected_joints:
            # 查找连接到此骨骼的皮肤簇
            connections = cmds.listConnections(joint, type='skinCluster') or []
            skin_clusters.update(connections)
        
        if not skin_clusters:
            cmds.warning("未找到关联的皮肤簇")
            return
        
        # 计算总顶点数用于进度条
        total_vertices = 0
        for skin_cluster in skin_clusters:
            geometries = cmds.skinCluster(skin_cluster, query=True, geometry=True) or []
            for geo in geometries:
                total_vertices += cmds.polyEvaluate(geo, vertex=True)
        
        # 如果没有顶点需要处理
        if total_vertices == 0:
            cmds.warning("未找到需要处理的顶点")
            return
        
        # 创建进度条
        progress_title = "转移蒙皮权重"
        cmds.progressWindow(
            title=progress_title,
            progress=0,
            max=total_vertices,
            status="正在准备...",
            isInterruptable=True
        )
        
        processed_vertices = 0
        canceled = False
        
        # 处理每个皮肤簇
        for skin_cluster in skin_clusters:
            # 获取受影响的几何体
            geometries = cmds.skinCluster(skin_cluster, query=True, geometry=True) or []
            
            # 备份当前选择
            original_selection = cmds.ls(selection=True)
            
            for geo in geometries:
                # 确保目标骨骼在皮肤簇影响列表中
                influences = cmds.skinCluster(skin_cluster, query=True, influence=True) or []
                if target_joint not in influences:
                    cmds.skinCluster(skin_cluster, edit=True, addInfluence=target_joint, weight=0)
                
                # 获取顶点数量
                vtx_count = cmds.polyEvaluate(geo, vertex=True)
                
                # 处理每个顶点
                for vtx_id in range(vtx_count):
                    # 检查是否取消
                    if cmds.progressWindow(query=True, isCancelled=True):
                        canceled = True
                        break
                    
                    # 更新进度条
                    processed_vertices += 1
                    progress_percent = int((processed_vertices / total_vertices) * 100)
                    cmds.progressWindow(
                        edit=True,
                        progress=processed_vertices,
                        status=f"处理中: {geo} ({progress_percent}%)"
                    )
                    
                    vtx = f"{geo}.vtx[{vtx_id}]"
                    
                    # 获取当前权重值
                    weights = cmds.skinPercent(skin_cluster, vtx, query=True, value=True)
                    influences = cmds.skinPercent(skin_cluster, vtx, query=True, transform=None)
                    
                    # 创建权重字典
                    weight_dict = dict(zip(influences, weights))
                    
                    # 计算要转移的总权重
                    transfer_weight = 0.0
                    for joint in source_joints:
                        if joint in weight_dict:
                            transfer_weight += weight_dict[joint]
                    
                    # 如果有权重要转移
                    if transfer_weight > 0:
                        # 获取目标骨骼当前权重
                        target_current = weight_dict.get(target_joint, 0.0)
                        
                        # 设置新的目标骨骼权重
                        new_target_weight = target_current + transfer_weight
                        
                        # 准备权重设置列表
                        transform_values = [(target_joint, new_target_weight)]
                        
                        # 添加源骨骼（权重设为0）
                        for joint in source_joints:
                            if joint in weight_dict:
                                transform_values.append((joint, 0.0))
                        
                        # 应用新的权重（Maya会自动归一化）
                        cmds.skinPercent(
                            skin_cluster, 
                            vtx, 
                            transformValue=transform_values,
                            normalize=True
                        )
                
                if canceled:
                    break
            
            # 恢复原始选择
            cmds.select(original_selection, replace=True)
            
            if canceled:
                break
        
        # 关闭进度条
        cmds.progressWindow(endProgress=True)
        
        if canceled:
            cmds.warning("操作已取消")
        else:
            print(f"成功将 {len(source_joints)} 个骨骼的权重转移到 {target_joint}（源骨骼权重清零）")
    
    # 执行函数
    transfer_skin_weights_remove_source_weights()

    def _expose_to_global():
        import __main__  # 获取 Maya 主模块
        main_globals = __main__.__dict__
        for func in list_user_functions():
            main_globals[func.__name__] = func  # 注入到 Maya 全局作用域
    
    def list_user_functions():
        functions = []
        import inspect
        for name, obj in globals().items():
            if inspect.isfunction(obj) and obj.__module__ == __name__:
                functions.append(obj)
        return functions
    
    _expose_to_global()

script()