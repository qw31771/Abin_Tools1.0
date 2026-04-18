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
    
    
    def mirror_controller_shape(flip_axes=['x']):
        """
        镜像控制器形状，支持自由组合轴翻转
        :param flip_axes: 翻转轴列表 (['x'], ['x','y'], ['x','z'], etc.)
        """
        # 获取当前选择的控制器
        sel = cmds.ls(selection=True, type='transform')
        if not sel:
            cmds.warning("请选择一个控制器")
            return
        
        source_ctrl = sel[0]
        
        # 检查是否为有效控制器
        shapes = cmds.listRelatives(source_ctrl, shapes=True, type='nurbsCurve')
        if not shapes:
            cmds.warning("选择的物体不是曲线控制器")
            return
        
        # 获取控制器名称（不含命名空间）
        ctrl_name = source_ctrl.split('|')[-1].split(':')[-1]
        
        # 识别左右标识（支持大小写）
        is_left = any([k.lower() in ctrl_name.lower() for k in ['_L', 'L_', '_l', 'l_']])
        is_right = any([k.lower() in ctrl_name.lower() for k in ['_R', 'R_', '_r', 'r_']])
        
        if not (is_left or is_right):
            cmds.warning("控制器名称不包含L/R标识符")
            return
        
        # 构建镜像控制器名称（保留原始大小写）
        mirror_name = None
        if is_left:
            # 按优先级替换
            if '_L' in ctrl_name:
                mirror_name = ctrl_name.replace('_L', '_R')
            elif '_l' in ctrl_name:
                mirror_name = ctrl_name.replace('_l', '_r')
            elif 'L_' in ctrl_name:
                mirror_name = ctrl_name.replace('L_', 'R_')
            elif 'l_' in ctrl_name:
                mirror_name = ctrl_name.replace('l_', 'r_')
            elif 'L' in ctrl_name:
                mirror_name = ctrl_name.replace('L', 'R')
            elif 'l' in ctrl_name:
                mirror_name = ctrl_name.replace('l', 'r')
        else:
            if '_R' in ctrl_name:
                mirror_name = ctrl_name.replace('_R', '_L')
            elif '_r' in ctrl_name:
                mirror_name = ctrl_name.replace('_r', '_l')
            elif 'R_' in ctrl_name:
                mirror_name = ctrl_name.replace('R_', 'L_')
            elif 'r_' in ctrl_name:
                mirror_name = ctrl_name.replace('r_', 'l_')
            elif 'R' in ctrl_name:
                mirror_name = ctrl_name.replace('R', 'L')
            elif 'r' in ctrl_name:
                mirror_name = ctrl_name.replace('r', 'l')
        
        # 查找镜像控制器
        target_ctrl = None
        for obj in cmds.ls(type='transform'):
            clean_name = obj.split('|')[-1].split(':')[-1]
            if mirror_name == clean_name:
                target_ctrl = obj
                break
        
        if not target_ctrl:
            cmds.warning(f"找不到镜像控制器: {mirror_name}")
            return
        
        # 镜像形状节点（不复制整个控制器）
        mirror_shape_only(target_ctrl, source_ctrl, flip_axes)
    
    
    def mirror_shape_only(target_ctrl, source_ctrl, flip_axes=['x']):
        """
        只镜像形状节点，不复制整个控制器
        :param target_ctrl: 目标控制器
        :param source_ctrl: 源控制器
        :param flip_axes: 翻转轴列表 (['x'], ['x','y'], etc.)
        """
        # 记录源控制器的形状属性
        target_shapes  = cmds.listRelatives(target_ctrl, shapes=True, path=True) or []
        target_colors  = []
        target_widths  = []
        
        for shape in target_shapes :
            # 记录颜色
            if cmds.objExists(f"{shape}.overrideColor"):
                color_val = cmds.getAttr(f"{shape}.overrideColor")
            else:
                color_val = 0
            target_colors.append(color_val)
            
            # 记录线宽
            if cmds.objExists(f"{shape}.lineWidth"):
                width_val = cmds.getAttr(f"{shape}.lineWidth")
            else:
                width_val = 1.0
            target_widths.append(width_val)
        
        # 删除目标控制器原有形状
        if target_shapes:
            cmds.delete(target_shapes)
    
    
        # 获取源控制器形状
        source_shapes = cmds.listRelatives(source_ctrl, shapes=True, path=True) or []
    
    
        # 确定翻转轴索引
        axis_map = {'x': 0, 'y': 1, 'z': 2}
        flip_indices = [axis_map[axis.lower()] for axis in flip_axes if axis.lower() in axis_map]
        
        # 复制源形状到目标控制器（仅形状节点）
        for i, shape in enumerate(source_shapes):
            # 复制形状节点（不复制整个控制器）
            dup_shape = cmds.duplicate(shape, returnRootsOnly=False, name="tempShape")[0]
            
            # 获取复制后的形状节点
            dup_shapes = cmds.listRelatives(dup_shape, shapes=True, path=True) or []
            if not dup_shapes:
                cmds.delete(dup_shape)
                continue
                
            dup_shape_node = dup_shapes[0]
            
            # 父对象形状到目标控制器
            cmds.parent(dup_shape_node, target_ctrl, shape=True, relative=True)
            
            # 删除临时组
            cmds.delete(dup_shape)
            
            # 重命名形状节点
            new_shape = cmds.rename(dup_shape_node, f"{target_ctrl}Shape")
            
            # 应用源控制器的颜色和线宽
            if i < len(target_colors):
                color_val = target_colors[i]
                width_val = target_widths[i]
            else:
                # 如果没有记录则使用默认值
                color_val = target_colors[0] if target_colors else 0
                width_val = target_widths[0] if target_widths else 1.0
            
            # 确保启用覆盖颜色
            cmds.setAttr(f"{new_shape}.overrideEnabled", 1)
            cmds.setAttr(f"{new_shape}.overrideColor", color_val)
            cmds.setAttr(f"{new_shape}.lineWidth", width_val)
            
            # 镜像控制点（多轴翻转）
            cvs = f"{new_shape}.cv[*]"
            cv_list = cmds.ls(cvs, flatten=True)
            
            for cv in cv_list:
                pos = cmds.pointPosition(cv, local=True)
                new_pos = list(pos)
                
                # 翻转指定轴
                for idx in flip_indices:
                    new_pos[idx] *= -1
                
                cmds.xform(cv, translation=new_pos, objectSpace=True)
        
        # 清理变换属性
        cmds.makeIdentity(target_ctrl, apply=True, translate=False, rotate=False, scale=True)
        cmds.select(target_ctrl)
    
    
    # 创建UI让用户选择翻转轴
    def create_mirror_ui():
        if cmds.window("mirrorUI", exists=True):
            cmds.deleteUI("mirrorUI")
        
        cmds.window("mirrorUI", title="控制器镜像工具", widthHeight=(300, 150))
        cmds.columnLayout(adjustableColumn=True)
        
        cmds.text("选择翻转轴:")
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(80, 80, 80), adjustableColumn=3)
        x_cb = cmds.checkBox(label="X轴", value=True)
        y_cb = cmds.checkBox(label="Y轴")
        z_cb = cmds.checkBox(label="Z轴")
        cmds.setParent("..")
        
        cmds.separator(height=10)
        cmds.button(label="镜像控制器形状", command=lambda *args: run_mirror(x_cb, y_cb, z_cb), height=40)
        cmds.showWindow("mirrorUI")
    
    
    def run_mirror(x_cb, y_cb, z_cb, *args):
        # 获取选择的轴
        flip_axes = []
        if cmds.checkBox(x_cb, query=True, value=True):
            flip_axes.append('x')
        if cmds.checkBox(y_cb, query=True, value=True):
            flip_axes.append('y')
        if cmds.checkBox(z_cb, query=True, value=True):
            flip_axes.append('z')
        
        if not flip_axes:
            cmds.warning("请至少选择一个翻转轴")
            return
        
        # 执行镜像
        mirror_controller_shape(flip_axes)
    
    
    # 执行UI
    create_mirror_ui()


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