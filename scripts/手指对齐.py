from functools import wraps
import maya.cmds as cmds
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
    fingerList=["L_Thumb","L_Index","L_Middle","L_Ring","L_Pinky"]
    L_thumb=["FKOffsetThumbFinger1_L","FKOffsetThumbFinger2_L","FKOffsetThumbFinger3_L"]
    L_Index=["FKOffsetIndexFinger0_L","FKOffsetIndexFinger1_L","FKOffsetIndexFinger2_L","FKOffsetIndexFinger3_L"]
    L_Middle=["FKOffsetMiddleFinger0_L","FKOffsetMiddleFinger1_L","FKOffsetMiddleFinger2_L","FKOffsetMiddleFinger3_L"]
    L_Ring=["FKOffsetRingFinger0_L","FKOffsetRingFinger1_L","FKOffsetRingFinger2_L","FKOffsetRingFinger3_L"]
    L_Pinky=["FKOffsetPinkyFinger0_L","FKOffsetPinkyFinger1_L","FKOffsetPinkyFinger2_L","FKOffsetPinkyFinger3_L"]
    
    L_SourceList=[L_thumb,L_Index,L_Middle,L_Ring,L_Pinky]

    L_thumbCtrl=["FKThumbFinger1_L","FKThumbFinger2_L","FKThumbFinger3_L"]
    L_IndexCtrl=["FKIndexFinger0_L","FKIndexFinger1_L","FKIndexFinger2_L","FKIndexFinger3_L"]
    L_MiddleCtrl=["FKMiddleFinger0_L","FKMiddleFinger1_L","FKMiddleFinger2_L","FKMiddleFinger3_L"]
    L_RingCtrl=["FKRingFinger0_L","FKRingFinger1_L","FKRingFinger2_L","FKRingFinger3_L"]
    L_PinkyCtrl=["FKPinkyFinger0_L","FKPinkyFinger1_L","FKPinkyFinger2_L","FKPinkyFinger3_L"]

    L_SourceCtrlList=[L_thumbCtrl,L_IndexCtrl,L_MiddleCtrl,L_RingCtrl,L_PinkyCtrl]
    
    for i in range(0,5):
        if cmds.objExists((fingerList[i]+"0")):
            finger=fingerList[i]+"0"
            L_Source=L_SourceList[i]
            L_SourceCtrl=L_SourceCtrlList[i]
        else:
            finger=fingerList[i]+"1"
            start=1
            if "Thumb" in finger:
                start=0
            L_Source=L_SourceList[i][start:len(L_SourceList[i])]
            L_SourceCtrl=L_SourceCtrlList[i][start:len(L_SourceCtrlList[i])]
        
        L_Target=cmds.listRelatives(finger,ad=1,c=1,type="joint")
        L_Target.append(finger)
        L_Target.reverse()
        R_Target=[]
        for target in L_Target:
            right=target.replace("L_","R_")
            R_Target.append(right)
        
        
        R_Source=[]
        R_SourceCtrl=[]
        for source in L_Source:
            right=source.replace("_L","_R")
            R_Source.append(right)

        for source in L_SourceCtrl:
            right=source.replace("_L","_R")
            R_SourceCtrl.append(right)
        

        rang=len(L_Source)
        for j in range(0,rang):
            if cmds.objExists(L_Source[j]):
                cmds.matchTransform(L_Source[j],L_Target[j])
                cmds.parentConstraint(L_SourceCtrl[j],L_Target[j])
                cmds.scaleConstraint(L_SourceCtrl[j],L_Target[j])
                
                cmds.matchTransform(R_Source[j],R_Target[j])
                cmds.parentConstraint(R_SourceCtrl[j],R_Target[j])
                cmds.scaleConstraint(R_SourceCtrl[j],R_Target[j])

    
    for i in range(0,5):
        if cmds.objExists((fingerList[i]+"0")):
            L_Source=L_SourceList[i]
        else:
            finger=fingerList[i]
            start=1
            if "Thumb" in finger:
                start=0
            L_Source=L_SourceList[i][start:len(L_SourceList[i])]
        R_Source=[]

        print(L_Source)
        print(R_Source)

        for source in L_Source:
            right=source.replace("_L","_R")
            R_Source.append(right)
            
        for j in range(0,len(L_Source)):
            L_child=cmds.listRelatives(L_Source[j],c=1)[0]
            rotY="bw"+L_child+"_rotateY"
            rotZ="bw"+L_child+"_rotateZ"
            if cmds.objExists(rotY):
                ry=cmds.listConnections(rotY+".output")[0]
                cmds.disconnectAttr(rotY+".output",ry+".input")
                cmds.delete(ry)
                md=cmds.createNode("multiplyDivide",n=L_child+"_Y2Z")
                cmds.setAttr(md+".input2X",-1)
                cmds.connectAttr(rotY+".output",md+".input1X")
                cmds.connectAttr(md+".outputX",L_child+".rotateZ",f=1)
                cmds.keyframe(L_child+"_rotateY",index=(0,0),absolute=1,valueChange=-35)
            if cmds.objExists(rotZ):
                rz=cmds.listConnections(rotZ+".output")[0]
                cmds.disconnectAttr(rotZ+".output",rz+".input")
                cmds.delete(rz)
                cmds.connectAttr(rotZ+".output",L_child+".rotateY",f=1)
            

            R_child=cmds.listRelatives(R_Source[j],c=1)[0]
            rotY="bw"+R_child+"_rotateY"
            rotZ="bw"+R_child+"_rotateZ"
            if cmds.objExists(rotY):
                ry=cmds.listConnections(rotY+".output")[0]
                cmds.disconnectAttr(rotY+".output",ry+".input")
                cmds.delete(ry)
                md=cmds.createNode("multiplyDivide",n=R_child+"_Y2Z")
                cmds.setAttr(md+".input2X",-1)
                cmds.connectAttr(rotY+".output",md+".input1X")
                cmds.connectAttr(md+".outputX",R_child+".rotateZ",f=1)
                cmds.keyframe(R_child+"_rotateY",index=(0,0),absolute=1,valueChange=-35)
            if cmds.objExists(rotZ):
                rz=cmds.listConnections(rotZ+".output")[0]
                cmds.disconnectAttr(rotZ+".output",rz+".input")
                cmds.delete(rz)
                cmds.connectAttr(rotZ+".output",R_child+".rotateY",f=1)






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