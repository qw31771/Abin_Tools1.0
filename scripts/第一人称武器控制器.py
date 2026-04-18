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
    
    
    R_wepList=["MasterWeapon_FK_ctrl","World_Pos","R_MoveablePivot_FK_ctrl","L_Hand_Weapon_Traget"]
    L_wepList=["MasterWeapon_FK_ctrl","World_Pos","L_MoveablePivot_FK_ctrl","R_Hand_Weapon_Traget"]
    
    
    
    cmds.matchTransform("MasterWeapon_FK_Pos","MasterWeapon",pos=1) 
    cmds.parentConstraint("MasterWeapon_FK_ctrl","MasterWeapon",mo=1)[0]
    cmds.scaleConstraint("MasterWeapon_FK_ctrl","MasterWeapon",mo=1)[0]
   
    R_ps=cmds.parentConstraint(R_wepList,"R_WeaponPoint_FK_Pos",mo=1)[0]
    L_ps=cmds.parentConstraint(L_wepList,"L_WeaponPoint_FK_Pos",mo=1)[0]

    cmds.parentConstraint("R_Weapon_FK_ctrl","R_WeaponPoint",mo=1)[0]
    cmds.scaleConstraint("R_Weapon_FK_ctrl","R_WeaponPoint",mo=1)[0]
    cmds.parentConstraint("L_Weapon_FK_ctrl","L_WeaponPoint",mo=1)[0]
    cmds.scaleConstraint("L_Weapon_FK_ctrl","L_WeaponPoint",mo=1)[0]

 

    cmds.matchTransform("Camera_FK_Pos","Camera")
    cmds.parentConstraint("Camera_FK_ctrl","Camera",mo=1)[0]
    cmds.scaleConstraint("Camera_FK_ctrl","Camera",mo=1)[0]

    cmds.matchTransform("VFX_Camera_FK_Pos","VFX_Camera")
    cmds.parentConstraint("VFX_Camera_FK_ctrl","VFX_Camera",mo=1)[0]
    cmds.scaleConstraint("VFX_Camera_FK_ctrl","VFX_Camera",mo=1)[0]

    cmds.matchTransform("WeaponADS_FK_Pos","WeaponADS")
    cmds.parentConstraint("WeaponADS_FK_ctrl","WeaponADS",mo=1)[0]
    cmds.scaleConstraint("WeaponADS_FK_ctrl","WeaponADS",mo=1)[0]

    cmds.parentConstraint("L_Hand","L_Weapon_HandOffset",mo=1)[0]
    cmds.scaleConstraint("L_Hand","L_Weapon_HandOffset",mo=1)[0]
    cmds.parentConstraint("R_Hand","R_Weapon_HandTarget",mo=1)[0]
    cmds.scaleConstraint("R_Hand","R_Weapon_HandTarget",mo=1)[0]

    try:
        cmds.parentConstraint("L_WeaponPoint","L_WeaponMaster",mo=1)[0]
        cmds.scaleConstraint("L_WeaponPoint","L_WeaponMaster",mo=1)[0]
        cmds.parentConstraint("R_WeaponPoint","R_WeaponMaster",mo=1)[0]
        cmds.scaleConstraint("R_WeaponPoint","R_WeaponMaster",mo=1)[0]
    except:
        pass

    
    
    
    
    
    
    for i in range(len(L_wepList)):
        cmds.setAttr("L_WeaponPoint_FK_ctrl.parentPoint",i)
        cmds.setAttr("R_WeaponPoint_FK_ctrl.parentPoint",i)
        for j in range(len(L_wepList)):
            if i == j:
                key=1
            else:
                key=0
                
            cmds.setAttr(L_ps+'.'+L_wepList[j]+"W"+str(j),key)
            cmds.setDrivenKeyframe(L_ps+'.'+L_wepList[j]+"W"+str(j),cd="L_WeaponPoint_FK_ctrl.parentPoint")
            
            cmds.setAttr(R_ps+'.'+R_wepList[j]+"W"+str(j),key)
            cmds.setDrivenKeyframe(R_ps+'.'+R_wepList[j]+"W"+str(j),cd="R_WeaponPoint_FK_ctrl.parentPoint")
    
    

    cmds.matchTransform("R_Hand_Weapon_Pos","R_Hand")
    cmds.matchTransform("L_Hand_Weapon_Pos","L_Hand")
    cmds.parentConstraint("R_Hand","R_Hand_Weapon_Pos")
    cmds.parentConstraint("L_Hand","L_Hand_Weapon_Pos")
    
    
    cmds.setAttr("L_Hand_Weapon_loc_offset.rotate",90,0,90)
    cmds.setAttr("L_Hand_Weapon_Loc.translate",-5,0,8)
    cmds.setAttr("R_Hand_Weapon_loc_offset.rotate",-90,0,90)
    cmds.setAttr("R_Hand_Weapon_Loc.translate",5,0,8)
    
    cmds.parentConstraint("RootX_M","Controls",mo=1)[0]
    cmds.scaleConstraint("RootX_M","Controls",mo=1)[0]


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