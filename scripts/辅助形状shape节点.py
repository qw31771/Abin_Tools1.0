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
    import maya.mel as mel
    
    class ShapeTransferUI:
        def __init__(self):
            self.window_name = "shapeTransferWindow"
            
        def create_ui(self):
            # 如果窗口已存在，则删除
            if cmds.window(self.window_name, exists=True):
                cmds.deleteUI(self.window_name)
            
            # 创建窗口
            cmds.window(self.window_name, title="形状复制工具", width=300, height=200)
            cmds.columnLayout(adjustableColumn=True)
            
            # 添加说明文本
            cmds.text(label="选择顺序: 先选源对象(有形状的)，再选目标对象", align="left")
            cmds.separator(height=10)
            
            # 添加选项框
            self.delete_toggle = cmds.checkBox(
                label="删除目标对象原有形状",
                value=1,
            )
            
            cmds.separator(height=10)
            
            # 添加按钮
            cmds.button(label="复制形状", command=self.transfer_shapes)
            
            # 显示窗口
            cmds.showWindow(self.window_name)
        
        def transfer_shapes(self, *args):
            """复制形状的主要函数"""
            selection = cmds.ls(selection=True, type="transform")
            
            if len(selection) < 2:
                cmds.confirmDialog(title="错误", message="请先选择两个对象：源对象和目标对象")
                return
            
            source_obj = selection[0]
            target_obj = selection[1]
            
            try:
                # 获取源对象的形状节点
                source_shapes = cmds.listRelatives(source_obj, shapes=1, c=1) 
                print(source_shapes)
                
                if not source_shapes:
                    cmds.confirmDialog(title="错误", message=f"源对象 {source_obj} 没有形状节点")
                    return
                    
                delete_target_shapes=cmds.checkBox(self.delete_toggle,q=1,v=1)
                if delete_target_shapes:
                    target_shapes = cmds.listRelatives(target_obj, shapes=True, fullPath=True) or []
                    cmds.delete(target_shapes)
                
                cmds.matchTransform(source_obj,target_obj)
                cmds.makeIdentity(source_obj)
                cmds.parent(source_shapes, target_obj, shape=True, relative=True)
                cmds.delete(source_obj)
                
                # # 重命名形状节点以保持整洁
                self.rename_shapes(target_obj)
                
                # # 显示成功消息
                cmds.warning('复制成功')
                
            except Exception as e:
                cmds.error('复制失败')
        
        
        def rename_shapes(self, target_obj):
            """重命名形状节点以匹配目标对象"""
            target_shapes = cmds.listRelatives(target_obj, shapes=True, fullPath=True) or []
            
            for idx, shape in enumerate(target_shapes):
                # 获取形状类型
                shape_type = cmds.objectType(shape)
                
                # 根据类型和索引创建新名称
                if idx == 0:
                    new_name = f"{target_obj}Shape"
                else:
                    new_name = f"{target_obj}Shape{idx+1}"
                
                # 重命名形状节点
                try:
                    cmds.rename(shape, new_name)
                except:
                    # 如果重命名失败，可能因为名称冲突，跳过
                    pass
        
    
    # 创建并显示UI
    def show_shape_transfer_ui():
        ui = ShapeTransferUI()
        ui.create_ui()
    
    # 直接执行函数（无需选择对象）
    show_shape_transfer_ui()


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