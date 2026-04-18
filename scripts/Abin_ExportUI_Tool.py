import sys
import maya.cmds as cmds
import MYMAYA
from os import listdir
from importlib import reload

name="Abin_ExportUI_Tool"
toolPath=MYMAYA.PATH.TOOLS
files=listdir(toolPath)
path=""
for file in files:
    tools=listdir(toolPath+"/"+file)
    if name in tools:
        path=toolPath+"/"+file+"/"+name+"/scripts"
        # break

if path not in sys.path:
    sys.path.append(path)


import abin_ExportUI

load_ui=reload(abin_ExportUI)
load_ui.open_ui()
