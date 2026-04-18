import maya.cmds as cmds
import os
'''
by:abin
update:2026/1/28
1、Delete the vaccine module and SceneSaved callback
2、Add auto save
'''
current_shelf = cmds.tabLayout("ShelfLayout", q=True, st=True)
py_cmd = '''
import maya.cmds as cmds
import maya.mel as mel
import os
import sys

isNode=False

keywords=["vaccine","gene","breed","fuckVirus","leukocyte"]

path=mel.eval('getenv \\"MAYA_APP_DIR\\" ')
path=path+"/scripts"


if 'vaccine' in sys.modules:
    vaccine = sys.modules['vaccine']
    
    del sys.modules['vaccine']
    
    for path in list(sys.path):
        if 'vaccine' in str(path):
            sys.path.remove(path)

    import maya.cmds as cmds

    all_jobs = cmds.scriptJob(listJobs=True)
    
    for job_str in all_jobs:
        if "leukocyte.antivirus()" in job_str:
            job_id = int(job_str.split(':')[0])
            cmds.scriptJob(kill=job_id, force=True)
            print(f"SceneSaved ID: {job_id}")

    print("vaccine module cleared")

#maya
nodes=cmds.ls(type="script")
for node in nodes:
     for key in keywords:
          if key in node:
               cmds.delete(node)
               isNode=True
               break
          
#windows
for fpathe,dirs,fs in os.walk(path):
    for f in fs:
        file=os.path.join(fpathe,f)
        for key in keywords:
            if key in file:
                try:
                    isNode=True
                    os.remove(file)
                except:
                    cmd = 'del "'+ file + '" /F'
                    os.system(cmd)
                break

        if 'userSetup' in file:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    should_keep = True
                    for keyword in keywords:
                        if keyword in line:
                            should_keep = False
                            break
                    
                    if should_keep:
                        new_lines.append(line)
                
                with open(file, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
            except Exception as e:
                pass

               
scenceFile=mel.eval("file -q -location")
cmds.file( rename=scenceFile )
openFile=cmds.file(save=1)

if isNode:
     cmds.warning("success")
else:
     cmds.warning("no virus")
'''

def create_clean_button():
    existing_buttons = cmds.shelfLayout(current_shelf, q=True, childArray=True) or []
    for btn in existing_buttons:
        if cmds.shelfButton(btn, q=True, label=True) == "Clear Virus":
            return  
    
    icon_path = "mayaIcon.png"
    
    cmds.shelfButton(
        parent=current_shelf,
        enable=True,
        width=35,
        height=35,
        align="center",
        label="Clear Virus",
        annotation="Clear Virus",
        image=icon_path,
        command=py_cmd,
        sourceType="python",
        style="iconOnly"
    )

def onMayaDroppedPythonFile(*args, **kwargs):
    create_clean_button()