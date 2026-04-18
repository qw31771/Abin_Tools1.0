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
    import maya.cmds as cmds
    
    def normalize_rotation_smart():
        """
        智能规范化旋转值到-180到180度范围，避免偏差
        """
        selected_objects = cmds.ls(selection=True)
        
        if not selected_objects:
            cmds.warning("请先选择要处理的对象")
            return
        
        for obj in selected_objects:
            print(f"处理对象: {obj}")
            
            # 方法1: 使用Maya内置的欧拉过滤器（最安全）
            try:
                cmds.select(obj)
                # 在曲线图编辑器中应用欧拉过滤器
                cmds.filterCurve()
                print(f"已对 {obj} 应用欧拉过滤器")
            except Exception as e:
                print(f"欧拉过滤器应用失败: {e}")
            
            # 方法2: 使用四元数插值避免万向锁问题
            # normalize_rotation_quaternion_safe(obj)
        
        print("旋转值智能规范化完成！")
        
    def normalize_rotation_quaternion(obj):
        anim_curves = []
        for axis in ['X', 'Y', 'Z']:
            curves = cmds.listConnections(f"{obj}.rotate{axis}", type="animCurve")
            if curves:
                anim_curves.extend(curves)
        
        if not anim_curves:
            print(f"对象 {obj} 没有旋转动画，使用单帧规范化")
            return normalize_rotation_quaternion_safe(obj)

        # 获取所有关键帧时间
        all_key_times = set()
        for curve in anim_curves:
            key_times = cmds.keyframe(curve, query=True, timeChange=True) or []
            all_key_times.update(key_times)
        
        # 按时间排序
        all_key_times = sorted(all_key_times)
        

        firstTime=cmds.currentTime(q=True)

        # 处理每个关键帧
        for time in all_key_times:
            # 设置到关键帧时间
            cmds.currentTime(time)
            
            # 使用四元数规范化当前帧
            normalize_rotation_quaternion_safe(obj)

        cmds.currentTime(firstTime)


    def normalize_rotation_quaternion_safe(obj):
        """
        使用四元数方法安全地规范化旋转值
        """
        try:
            # 获取当前旋转（欧拉角）
            current_rotation = cmds.getAttr(obj + ".rotate")[0]
            cmds.select(cl=1)
            # 创建临时对象
            temp_obj = cmds.group(empty=True, name="temp_rotation_advanced")
            
            # 设置相同旋转
            cmds.setAttr(temp_obj + ".rotate", *current_rotation)
            
            # 方法2: 通过矩阵转换来规范化
            # 获取世界变换矩阵
            matrix = cmds.xform(temp_obj, query=True, matrix=True, worldSpace=True)
            
            # 重新应用相同的矩阵（这会触发Maya的内部规范化）
            cmds.xform(temp_obj, matrix=matrix, worldSpace=True)
            
            # 获取规范化后的旋转
            normalized_rotation = cmds.getAttr(temp_obj + ".rotate")[0]
            
            # 应用到原始对象
            cmds.setAttr(obj + ".rotate", *normalized_rotation)
            
            # 清理
            cmds.delete(temp_obj)
            
            
        except Exception as e:
            print(f"高级四元数规范化失败: {e}")
    
    def normalize_rotation_basic(obj):
        """
        基本规范化方法，处理每个轴
        """
        for axis in ['X', 'Y', 'Z']:
            attr_name = f"{obj}.rotate{axis}"
            
            # 检查是否有动画曲线
            anim_curves = cmds.listConnections(attr_name, type="animCurve")
            
            if anim_curves:
                # 处理动画曲线
                process_animated_rotation_smart(anim_curves[0], axis)
            else:
                # 处理静态值
                current_value = cmds.getAttr(attr_name)
                normalized_value = smart_normalize_angle(current_value)
                cmds.setAttr(attr_name, normalized_value)
    
    def smart_normalize_angle(angle):
        """
        智能角度规范化，避免偏差
        """
        # 先规范化到0-360范围
        angle = angle % 360
        
        # 处理负角度
        if angle < 0:
            angle += 360
        
        # 转换到-180到180范围
        if angle > 180:
            angle -= 360
        
        return angle
    
    def process_animated_rotation_smart(anim_curve, axis):
        """
        智能处理动画曲线，保持动画连续性
        """
        # 获取所有关键帧
        key_times = cmds.keyframe(anim_curve, query=True, timeChange=True)
        
        if not key_times:
            return
        
        # 按时间排序
        key_times.sort()
        
        # 处理第一个关键帧
        first_value = cmds.keyframe(anim_curve, time=(key_times[0], key_times[0]), 
                                   query=True, valueChange=True)[0]
        normalized_first = smart_normalize_angle(first_value)
        cmds.keyframe(anim_curve, time=(key_times[0], key_times[0]), 
                     valueChange=normalized_first, absolute=True)
        
        # 处理后续关键帧，保持相对旋转
        prev_value = normalized_first
        for i in range(1, len(key_times)):
            time = key_times[i]
            current_value = cmds.keyframe(anim_curve, time=(time, time), 
                                         query=True, valueChange=True)[0]
            
            # 计算相对旋转
            relative_rotation = current_value - first_value
            
            # 应用相对旋转到规范化后的第一个关键帧
            new_value = normalized_first + relative_rotation
            
            # 规范化新值
            new_value = smart_normalize_angle(new_value)
            
            cmds.keyframe(anim_curve, time=(time, time), 
                         valueChange=new_value, absolute=True)
            prev_value = new_value
    
   
    
    def normalize_rotation_with_ui():
        """
        带UI的旋转规范化工具
        """
        if cmds.window("rotationNormalizerUI", exists=True):
            cmds.deleteUI("rotationNormalizerUI")
        
        window = cmds.window("rotationNormalizerUI", title="旋转规范化工具", width=400)
        main_layout = cmds.columnLayout(adjustableColumn=True)
        
        cmds.text(label="旋转规范化工具", height=30, font="boldLabelFont")
        cmds.separator(height=10)
        
        cmds.text(label="选择规范化方法:", align="left")
        method_radio = cmds.radioButtonGrp(
            numberOfRadioButtons=3,
            labelArray3=["智能规范化", "四元数方法", "基本方法"],
            select=1
        )
        
        cmds.separator(height=10)
        
        cmds.button(
            label="执行规范化",
            command=lambda x: execute_normalization(method_radio),
            height=40
        )
        
        cmds.separator(height=5)
        
        
        cmds.button(
            label="关闭",
            command=lambda x: cmds.deleteUI(window)
        )
        
        cmds.showWindow(window)
    
    def execute_normalization(method_radio):
        """
        执行选择的规范化方法
        """
        method = cmds.radioButtonGrp(method_radio, query=True, select=True)
        
        
        if method == 1:
            normalize_rotation_smart()
        elif method == 2:
            selected_objects = cmds.ls(selection=True)
            for obj in selected_objects:
                normalize_rotation_quaternion(obj)
        elif method == 3:
            selected_objects = cmds.ls(selection=True)
            for obj in selected_objects:
                normalize_rotation_basic(obj)
        
        cmds.inViewMessage(
            amg='旋转值已规范化到-180到180度范围',
            pos='topCenter',
            fade=True
        )
    
    normalize_rotation_with_ui()


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