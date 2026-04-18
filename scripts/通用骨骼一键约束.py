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
    advArm=["Scapula_L","Shoulder_L","Elbow_L","Wrist_L"]
    arm=["L_Clavicle","L_Shoulder","L_Elbow","L_Hand"]
    adv=Finger=["ThumbFinger","IndexFinger","MiddleFinger","RingFinger","PinkyFinger"]
    finger=["L_Thumb","L_Index","L_Middle","L_Ring","L_Pinky"]
    
    advLeg=["Hip_L","Knee_L","Ankle_L","Toes_L"]
    leg=["L_Hip","L_Knee","L_Foot","L_Toe"]
    
    advRoot=["Main_root","Main","Root_M","Spine1_M","Spine2_M","Spine3_M","Chest_M","Neck_M","Head_M"]
    root=["Skeleton","Root","Splitter","Spine1","Spine2","Spine3","Spine4","Neck","Head"]
    
    
    
    def constraint(sour,target):
        cmds.parentConstraint(sour,target,mo=1)
        cmds.scaleConstraint(sour,target,mo=1)
        
        try:
            LS=sour.replace("R","L")
            LT=target.replace("R","L")
            cmds.parentConstraint(LS,LT,mo=1)
            cmds.scaleConstraint(LS,LT,mo=1)
        except:
            pass
            
        try:
            RS=sour.replace("L","R")
            RT=target.replace("L","R")
            cmds.parentConstraint(RS,RT,mo=1)
            cmds.scaleConstraint(RS,RT,mo=1)
        except:
            pass
        
    
    try:
        for i in range(0,len(advArm)):
            if cmds.objExists(arm[i]):
                constraint(advArm[i],arm[i])
    except:
        pass
    try:
        for i in range(0,len(advLeg)):
            if cmds.objExists(leg[i]):
                constraint(advLeg[i],leg[i])
    except:
        pass
    try:
        for i in range(0,len(advRoot)):
            if cmds.objExists(root[i]):
                constraint(advRoot[i],root[i])
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