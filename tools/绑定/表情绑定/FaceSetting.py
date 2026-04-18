import common

class SETTING():
    #主轴
    upAxis=common.getWorldAxisInfo('up')
    worldUpVector=common.getWorldAxisInfo('up',v=1)
    #次轴
    subAxis=common.getWorldAxisInfo('sub')
    subVector=common.getWorldAxisInfo('sub',v=1)
    #前轴
    sceneFore=common.getWorldAxisInfo('fore')
    foreVector=common.getWorldAxisInfo('fore',v=1)
    
    drive="SkinJointScroll"

    faceRig="face_rig_grp"

class LIP():
    Lib_corner=["R_Lib_corner","L_Lib_corner"]
    LibName=["upperLip","lowerLip"]
    crvLibName=["upperLipCrv","lowerLipCrv"]
    m_LibCtrl=["M_"+LibName[0]+"_ctrl","M_"+LibName[1]+"_ctrl"]
    drive_grp="lipDrive_grp"
    drive_fol_grp="lipDrive_fol_grp"
    drive_joint_grp="lipDrive_joint_grp"
    ctrl_grp="lipCtrl_grp"
    ctrlJoint_grp="lipCtrlJoint_grp"


class Sets():
    faceSets="faceSets"
    driveJoinSets="driveJoinSets"




