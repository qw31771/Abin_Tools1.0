import maya.cmds as cmds
import sys

FILE="Abin_Tools/prefs/scripts"
SOURCE=cmds.internalVar(usd=1)
PATH=SOURCE+FILE
if PATH not in sys.path:
    sys.path.append(PATH)
def init():
    cmds.evalDeferred('import setIcon')
    
if __name__ == "__main__":
    init()
