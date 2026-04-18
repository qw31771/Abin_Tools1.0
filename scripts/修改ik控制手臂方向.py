import maya.cmds as cmds

ikctrl=["AlignIKToWrist_R","AlignIKToWrist_L"]


for i in ikctrl:
    if "Wrist" in i :
        target="Hand"
        ctrl="IKArm"
        
        
    if "_R" in i:
        target="R_"+target
        ctrl=ctrl+"_R"
    elif "_L" in i:
        target="L_"+target
        ctrl=ctrl+"_L"
    
    cmds.matchTransform(i,target)
    child=cmds.listRelatives(ctrl,c=1,s=0)
    cp=[]
    
    for cc in child:
        if "Shape" not in cc:
            cp.append(cc)
        
        
    cmds.parent(cp,w=1)
    p=cmds.listRelatives(ctrl,p=1)[0]
    cmds.matchTransform(p,target)
    cmds.parent(cp,ctrl)