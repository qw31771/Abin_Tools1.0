import sys
import MYMAYA
from os import listdir
from importlib import reload

tool="CodeV"
toolPath=MYMAYA.PATH.TOOLS
files=listdir(toolPath)
names=["/ui","/scripts"]
paths=[]
for file in files:
    tools=listdir(toolPath+"/"+file)
    if tool in tools:
        for name in names:
            path=toolPath+"/"+file+"/"+tool+name
            paths.append(path)

for path in paths:
    if path not in sys.path:
        sys.path.append(path)
    
import AbinCodeV_UI
reload(AbinCodeV_UI)
AbinCodeV_UI.Show()