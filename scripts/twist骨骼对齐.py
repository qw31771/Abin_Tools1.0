import maya.cmds as cmds
import math
se=cmds.ls(sl=1)
if len(se)!=2:
    jt=cmds.ls(sl=1)[0]
    if(jt in "ShoulderPart1_R"):
        #肩膀1
        sl=["ShoulderPart1_R","R_Shoulder_Twst1"]
        ps=["ShoulderPart1_R_pointConstraint1.Shoulder_RW1","ShoulderPart1_L_pointConstraint1.Shoulder_LW1"]
    elif (jt in "ShoulderPart2_R"):
        #肩膀2
        if cmds.objExists("R_Shoulder_Twst2"):
            tw="R_Shoulder_Twst2"
        else: tw="R_Shoulder_Twst3"
        
        sl=["ShoulderPart2_R",tw]
        ps=["ShoulderPart2_R_pointConstraint1.Shoulder_RW1","ShoulderPart2_L_pointConstraint1.Shoulder_LW1"]
    elif (jt in "ShoulderPart3_R"):
        #肩膀3
        sl=["ShoulderPart3_R","R_Shoulder_Twst3"]
        ps=["ShoulderPart3_R_pointConstraint1.Shoulder_RW1","ShoulderPart3_L_pointConstraint1.Shoulder_LW1"]
    elif (jt in "ElbowPart1_R"):
        #肘1
        sl=["ElbowPart1_R","R_Elbow_Twst1"]
        ps=["ElbowPart1_R_pointConstraint1.Elbow_RW1","ElbowPart1_L_pointConstraint1.Elbow_LW1"]
    elif (jt in "ElbowPart2_R"):
        #肘2
        sl=["ElbowPart2_R","R_Elbow_Twst2"]
        ps=["ElbowPart2_R_pointConstraint1.Elbow_RW1","ElbowPart2_L_pointConstraint1.Elbow_LW1"]
    elif (jt in "ElbowPart3_R"):
        #肘3
        sl=["ElbowPart3_R","R_Elbow_Twst3"]
        ps=["ElbowPart3_R_pointConstraint1.Elbow_RW1","ElbowPart3_L_pointConstraint1.Elbow_LW1"]    
    elif (jt in "HipPart1_R"):
        #大腿1
        sl=["HipPart1_R","R_Hip_Twst1"]
        ps=["HipPart1_R_pointConstraint1.Hip_RW1","HipPart1_L_pointConstraint1.Hip_LW1"]
    elif (jt in "HipPart2_R"):
        #大腿2
        sl=["HipPart2_R","R_Hip_Twst2"]
        ps=["HipPart2_R_pointConstraint1.Hip_RW1","HipPart2_L_pointConstraint1.Hip_LW1"]
    elif (jt in "HipPart3_R1"):
        #大腿3
        sl=["HipPart3_R","R_Hip_Twst3"]
        ps=["HipPart3_R_pointConstraint1.Hip_RW1","HipPart3_L_pointConstraint1.Hip_LW1"]
    elif (jt in "KneePart1_R"):
    #小腿1
        sl=["KneePart1_R","R_Knee_Twist1"]
        ps=["KneePart1_R_pointConstraint1.Knee_RW1","KneePart1_L_pointConstraint1.Knee_LW1"]
    elif (jt in "KneePart2_R"):
        #小腿1
        sl=["KneePart2_R","R_Knee_Twist2"]
        ps=["KneePart2_R_pointConstraint1.Knee_RW1","KneePart2_L_pointConstraint1.Knee_LW1"]
    elif (jt in "KneePart3_R"):
        #小腿1
        sl=["KneePart3_R","R_Knee_Twist3"]
        ps=["KneePart3_R_pointConstraint1.Knee_RW1","KneePart3_L_pointConstraint1.Knee_LW1"]

    # p0=cmds.xform(sl[0],q=1,ws=1,t=1)
    # p1=cmds.xform(sl[1],q=1,ws=1,t=1)
    # x=(p0[0]-p1[0])
    # y=(p0[1]-p1[1])
    # z=(p0[2]-p1[2])
    # dis=math.sqrt(x*x+y*y+z*z)
    # offset1=1 if z < 0 else -1
    # offset2=1 if dis <8 else 10
    # for i in range(0,10000):
    #     p0=cmds.xform(sl[0],q=1,ws=1,t=1)
    #     p1=cmds.xform(sl[1],q=1,ws=1,t=1)
    #     x=(p0[0]-p1[0])
    #     y=(p0[1]-p1[1])
    #     z=(p0[2]-p1[2])
    #     kw=cmds.getAttr(ps[0])
    #     dis0=math.sqrt(x*x+y*y+z*z)
        
    #     if dis0>1:
    #         kw+=(0.00001*offset1*offset2)
    #     else:
    #         kw+=(0.00001*offset1*offset2)

    #     cmds.setAttr(ps[0],kw)
    #     dis=math.sqrt(x*x+y*y+z*z)
    #     if(dis)<=0.001:
    #         print(dis)
    #         cmds.setAttr(ps[1],kw)
    #         break
else:
    jt=se
    sl=[jt[0],jt[1]]

    if("Elbow" in jt[0]):
        ps=[jt[0]+"_pointConstraint1.Elbow_RW1",jt[0].replace("_R","_L")+"_pointConstraint1.Elbow_LW1"]
    elif ("Shoulder" in jt[0]):
        ps=[jt[0]+"_pointConstraint1.Shoulder_RW1",jt[0].replace("_R","_L")+"_pointConstraint1.Shoulder_LW1"]
    elif ("Hip" in jt[0]):
        ps=[jt[0]+"_pointConstraint1.Hip_RW1",jt[0].replace("_R","_L")+"_pointConstraint1.Hip_LW1"]
    elif ("Knee" in jt[0]):
        ps=[jt[0]+"_pointConstraint1.Knee_RW1",jt[0].replace("_R","_L")+"_pointConstraint1.Knee_LW1"]


# print(ps)
        
p0=cmds.xform(sl[0],q=1,ws=1,t=1)
p1=cmds.xform(sl[1],q=1,ws=1,t=1)
x=(p0[0]-p1[0])
y=(p0[1]-p1[1])
z=(p0[2]-p1[2])
dis=math.sqrt(x*x+y*y+z*z)
offset1=1 if z < 0 else -1
offset2=1 if dis <3 else 10
for i in range(0,10000):
    p0=cmds.xform(sl[0],q=1,ws=1,t=1)
    p1=cmds.xform(sl[1],q=1,ws=1,t=1)
    x=(p0[0]-p1[0])
    y=(p0[1]-p1[1])
    z=(p0[2]-p1[2])
    kw=cmds.getAttr(ps[0])
    dis0=math.sqrt(x*x+y*y+z*z)
    
    if dis0>1:
        kw+=(0.00001*offset1*offset2)
    else:
        kw+=(0.00001*offset1*offset2)
    cmds.setAttr(ps[0],kw)
    dis=math.sqrt(x*x+y*y+z*z)
    if(dis)<=0.001:
        print(dis)
        cmds.setAttr(ps[1],kw)
        break