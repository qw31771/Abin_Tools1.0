import maya.cmds as cmds
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
    #global
    import maya.cmds as cmds
    target=["FKShoulder_R","FKShoulder_L"]
    
    for i in target:
        grp1="Global"+i
        grp2="GlobalOffset"+i
        
        if not cmds.objExists(grp1):
            cmds.group(n=grp1,em=1)
            try:
                cmds.parent(grp1,grp2)
                
            except:
                cmds.group(n=grp2,em=1)
                cmds.parent(grp1,grp2)
                cmds.parent(grp2,"GlobalSystem")
            
        
        
        
        if not cmds.objExists(i+".global"):
            cmds.addAttr(i,ln="global",at="double",min=0,max=10,dv=0)
            cmds.setAttr(i+".global",e=1,k=1,l=0)
            
        unit=cmds.shadingNode("unitConversion",n=i+"_unit",au=1)
        cmds.setAttr(unit+".conversionFactor",0.1)
        rev=cmds.shadingNode("reverse",n=i+"_rev",au=1)
        cmds.connectAttr(i+".global",unit+".input",f=1)
        cmds.connectAttr(unit+".output",rev+".inputX",f=1)
        
        glo=cmds.group(n="FKGlobal"+i,em=1)
        sta=cmds.group(n="FKGlobalStatic"+i,em=1)
        cmds.parent(glo,sta)
        
        par1=cmds.listRelatives(i,p=1)
        par2=cmds.listRelatives(par1,p=1)
        cmds.matchTransform(sta,par2)
        cmds.matchTransform(grp2,par2)
        cmds.parent(sta,par2)
        cmds.parent(par1,glo)
        ps=cmds.orientConstraint([sta,grp1],glo,mo=1)[0]
        
        fk=ps+"."+sta+"W0"
        world=ps+"."+grp1+"W1"
        
        
        
        cmds.connectAttr(unit+".output",world,f=1)
        cmds.connectAttr(rev+".outputX",fk,f=1)


script()