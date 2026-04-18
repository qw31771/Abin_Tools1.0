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
    import maya.cmds as cmds
    import common
    from importlib import reload
    reload(common)
    sel=cmds.ls(sl=1)
    if not sel:
        cmds.warning("选择关节")
    else:
        sl=sel[0]
    
        
        index=sl.find(':')
        pre=sl[0:index+1]
        name=sl[index+1:len(sl)]
    
        if not cmds.objExists(name):
            cmds.warning("关节链不相等")
        else:
            child1=common.get_ChildList(name,True,"joint")
            print(child1)
            child2=common.get_ChildList(sl,True,"joint")
            print(child2)
            
            if len(child1) != len(child2):
                cmds.warning("关节链不相等")
            else:
                noList=[]
                for i in child1:
                    pos1=common.get_point_position(i)
                    pos2=common.get_point_position(pre+i)
                    # print(i,common.points_are_same(pos1,pos2))
                    if not common.points_are_same(pos1,pos2):
                        noList.append(i)
                
                if noList:
                    cmds.warning(f"关节链不相等 , 不同点为 ：{noList}")
                    cmds.select(noList)
                else:
                    cmds.warning(f"关节链相等")

script()