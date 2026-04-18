from functools import wraps

#装饰器
# def make_undo(func):
#     @wraps(func)
#     def wrap(*args,**kwargs):
#         cmds.undoInfo(openChunk=True )
#         result = func(*args,**kwargs)
#         cmds.undoInfo(closeChunk=True)
#         return result
#     return wrap


# @make_undo
# def script():
import maya.cmds as cmds

def CopyKyelUI():
    winds = 'CopyKyelUI'
    if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)
        
    cmds.window(winds , t = u'test')
    cmds.columnLayout("c1", columnAttach=('both', 5), rowSpacing=3, columnWidth=400 )

    cmds.text("-------关键帧跟随-------\n1、选择两个对象记录当前帧的相对位置,后选烘焙对象",h=50)
    cmds.rowLayout("r1", numberOfColumns=4,ad4=4)
    cmds.checkBox("缩放",h=35,w=50)
    cmds.button("烘焙帧",h=35,w=100,c="setAllKeys()",bgc=[0.9,0.7,0.7],ann='逐步每帧烘焙')
    cmds.button("帧对应",h=35,w=100,c="setKeys()",bgc=[0.9,0.7,0.7],ann='只烘焙对应和首尾帧,方便修改动画但是复杂动画可能会有问题')
    cmds.button("修复偏差",h=35,w=60,c="fix_setKeys()",bgc=[0.8,0.5,0.5],ann='对选中对象修复烘焙动画前后帧偏差过大问题')
    
    cmds.setParent("..")

    items=[]

    if cmds.objExists("setKeys_Temp"):
        childs=cmds.listRelatives("setKeys_Temp",c=1)
        for i in childs:
            index1=i.find("____")
            index2=i.rfind("____")
            item=i[0:index1]+" , " + i[index1+4:index2]+"  >>>>>>>>  开始帧:"+str(i[index2+4:len(i)])
            items.append(item)
    
        hh=30+(len(items)-1)*20
    else:
        hh=30
    cmds.textScrollList("jlmb",h=hh,pma=0,ams=1,a=items,sc="selectSource()")

    cmds.rowLayout(numberOfColumns=4,ad4=4)
    cmds.checkBox("保持偏移",h=35,w=70)
    cmds.button("记录",h=35,w=100,c="getLine()",bgc=[0.8,0.9,0.8],ann='记录位置,和约束类似的选中方法')
    cmds.button("清除全部",h=35,w=100,c="removeAllScroll()",ann='清除场景中的所有约束记录')
    cmds.button("删除选中",h=35,w=100,c="removeSelect()",ann='只删除选中的约束记录')
    cmds.setParent("..")
    

    cmds.text("-------复制单个动画-------\n1、第一个选择复制对象\n2、第二个选择粘贴随的对象",h=70)
    anim_start = int(cmds.playbackOptions(q=True, animationStartTime=True))
    anim_end = int(cmds.playbackOptions(q=True, animationEndTime=True))
    
    cmds.button("复制动画曲线",h=50,c="copytKey()",bgc=[0.9,0.4,0.4])
    
    cmds.text("-------复制旋转对象动画片段-------\n1、选择复制对象(带前缀)粘贴到对应的无前缀的对象",h=70)
    cmds.button("点击自动获取层级对象",h=50,c="selectCtrl()",bgc=[0.5,0.5,0.5])

    cmds.rowLayout(numberOfColumns=2,ad2=2)
    cmds.text('复制对象的动画开始帧 :')
    cmds.textField("copyStratTime",pht="复制开始时间",tx=anim_start)
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=2,ad2=2)
    cmds.text('复制对象的动画结束帧 :')
    cmds.textField("copyEndTime",pht="复制结束时间",tx=anim_end)
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=2,ad2=2)
    cmds.text('粘贴起始帧(默认为复制起始帧) :')
    cmds.textField("copyTragetStartTime",pht="粘贴开始时间",tx=anim_start)
    cmds.setParent("..")

    cmds.button("复制多个动画曲线",h=50,c="copytSelectKey()",bgc=[0.9,0.4,0.4])
    
    cmds.text("-------复制全部动画-------\n1、选择要复制的控制器最上面的组",h=50)
    cmds.rowLayout("r3", numberOfColumns=2,ad2=1)
    cmds.textField("traget_pre",h=35,pht="目标控制器前缀，没有则不填写")
    cmds.button("识取",h=35,w=50,c="getpre()")
    cmds.setParent("..")
    cmds.button("复制所有控制器",h=50,c="copyAllKeys()",bgc=[0.9,0.4,0.4])

    cmds.text("-------关键帧偏移-------\n1、选择要复制的控制器最上面的组",h=50)

    cmds.text(label="时间偏移（帧）:")
    cmds.intField("time_field",value=0)

    # 数值偏移输入
    cmds.text(label="数值偏移:")
    cmds.floatField("value_field",value=0)


    cmds.button(label="应用偏移", h=50,command="apply_offset()",bgc=[0.2,0.6,1])
    
    cmds.showWindow()


CopyKyelUI()



def handCons(model):
    sl=cmds.ls(sl=1)
    
    if sl and len(sl)<2:
        cmds.error("至少选择2个对象")
        return


    off=cmds.createNode("transform",n=sl[1]+"_offset")
    try:
        p=cmds.listRelatives(sl[1],p=1)[0]
        cmds.parent(off,p)
    except:
        pass


    cmds.matchTransform(off,sl[1])
    cmds.parent(sl[1],off)
    ps=cmds.parentConstraint(sl[0],off,mo=1)
    cmds.rename(ps[0]+"."+sl[0]+"W0",ps[0]+".left_off")



    cmds.select(ps[0])
    cmds.sets(n="offConstraint")
    
def getpre():
    sl=cmds.ls(sl=1)
    if not sl:
        cmds.error("请选择对象")
    else:
        source=sl[0]
    
    index=source.rfind(":")
    pre=source[0:index+1]
    cmds.textField("traget_pre",e=1,text=pre)
        
def copytKey(sl=[]):
    if not sl:
        sl=cmds.ls(sl=1)
    
    if len(sl)<2:
        cmds.error("至少选择2个对象")
    
    try:
        cmds.copyKey(sl[0])
        cmds.pasteKey(sl[1])
    except:
        pass

def copytSelectKey():
    sl=cmds.ls(sl=1)
    if not sl:
        cmds.error("请选择对象")
    copyStart=int(cmds.textField("copyStratTime",q=1,tx=1))
    copyEnd=int(cmds.textField("copyEndTime",q=1,tx=1))
    targetStart=int(cmds.textField("copyTragetStartTime",q=1,tx=1))
    for source in sl:
        index=source.rfind(":")
        traget=source[index+1:len(source)]
        if not cmds.objExists(traget):
            cmds.warning("没找到粘贴对象")
        else:
            
            try:
                cmds.copyKey(source,time=(copyStart, copyEnd))
                cmds.pasteKey(traget,time=(targetStart, targetStart + (copyEnd - copyStart)),option="replace")
            except:
                pass
    

def copyAllKeys():
    sl=cmds.ls(sl=1)
    if not sl:
        cmds.error("请选择对象")
    else:
        grp=sl[0]


    sl=selectCtrl(grp)
    pre=cmds.textField('traget_pre',q=1,tx=1)
    for source in sl:
        index=source.rfind(":")
        traget=pre+source[index+1:len(source)]
        copytKey([source,traget])



def selectCtrl(sel=""):
    if not sel:
        sl=cmds.ls(sl=1)
        if not sl:
            cmds.error("请选择对象")
        else:
            sel=sl[0]


    cmds.select(sel,hi=1)


    allList=cmds.ls(sl=1)


    ctrlList=cmds.ls(sl=1,type="nurbsCurve",s=0)
    ctrl = cmds.listRelatives(ctrlList,parent=True,type="transform")


    grp=getSpecialList(allList)

    try:
        selectList=grp+ctrl
        cmds.select(selectList)
    except:
        selectList=[]

    return selectList


def getSpecialList(select:list):


    specialList=["IKXOffsetShoulder_L","IKXOffsetHip_L","IKXOffsetHip_R","IKXOffsetShoulder_R","FKExtraShoulder_R","FKExtraHip_R","FKExtraHip_L","FKExtraShoulder_L"]


    grp=[]
    try:
        parent=cmds.listRelatives(select[0],p=1)[0]
        select.append(parent)
    except:
        pass
        
    for i in specialList:
        if i in select:
            grp.append(i)


    return grp


def getLine():
    sl=cmds.ls(sl=1)
    
    if len(sl)<2:
        cmds.error("至少选择2个对象")
        return


    time=int(cmds.currentTime(q=1))  
    grp="setKeys_Temp"

    mo=cmds.checkBox("保持偏移",q=1,v=1)
    scale=cmds.checkBox("缩放",q=1,v=1)

    if cmds.objExists(sl[0]+"_"+sl[1]+"_"+str(time)):
        cmds.warning("记录已存在,刷新位置")
        cmds.delete(sl[0]+"_"+sl[1]+"_"+str(time))
        point=cmds.createNode( "transform",n=sl[0]+"_"+sl[1]+"_"+str(time))
        if not mo:
            cmds.matchTransform(sl[1],sl[0],pos=1,rot=1,scl=0)
        cmds.matchTransform(point,sl[1])
        cmds.parentConstraint(sl[0],point,mo=1)
        cmds.scaleConstraint(sl[0],point,mo=0)
        cmds.parent(point,grp)
        return

    print(sl[0],sl[1])
    cmds.textScrollList("jlmb",e=1,a=sl[0]+" , " + sl[1]+"  >>>>>>>>  开始帧:"+str(time))
    point=cmds.createNode( "transform",n=sl[0]+"____"+sl[1]+"____"+str(time))
    if not mo:
        cmds.matchTransform(sl[1],sl[0],pos=1,rot=1,scl=0)
    cmds.matchTransform(point,sl[1])
    cmds.parentConstraint(sl[0],point,mo=1)
    cmds.scaleConstraint(sl[0],point,mo=0)
    if not cmds.objExists(grp):
        cmds.createNode( "transform",n=grp)
    cmds.parent(point,grp)
    upScrollLlist()


def removeAllScroll():
    cmds.textScrollList("jlmb",e=1,ra=1)
    cmds.delete("setKeys_Temp")
    upScrollLlist()


def removeSelect():
    objList=getKeyObj()
    for i in objList:
        name=i[0]+"_"+i[1]+"_"+str(i[2])
        print(i[0])
        if cmds.objExists(name):
            cmds.delete(name)


    se=cmds.textScrollList("jlmb",q=1,sii=1)
    count=len(se)
    for i in range(count):
        index=se[i]
        cmds.textScrollList("jlmb",e=1,rii=index-i)


    upScrollLlist()


def getKeyObj():
    se=cmds.textScrollList("jlmb",q=1,si=1)
    selList=[]
    for i in se:
        index1=i.find(',')
        index2=i.find('>')
        index3=i.find('帧')
        end=len(i)


        source=i[0:index1-1]
        target=i[index1+2:index2-2]
        time=int(i[index3+2:end])
        loc=source+"____"+target+"____"+str(time)
        selList.append([source,target,time,loc])


    return selList


def setKeys():
    objList=getKeyObj()
    for i in objList:
        source=i[0]
        target=i[1]
        startTime=i[2]
        loc=i[3]
        endTime=cmds.currentTime(q=1)


        # print("源:"+source,"目标:"+target,"开始:"+startTime,"结束:"+endTime)


        targetKeys=get_keyframe_times(source)
        keys=[]
        keys.append(startTime)
        for i in targetKeys:
            time=int(i)
            print(time)
            if (time > startTime) and (time < endTime):
                keys.append(time)


        keys.append(endTime)

        scale=cmds.checkBox("缩放",q=1,v=1)
        for key in (keys):
            cmds.currentTime(key)
            cmds.matchTransform(target,loc,pos=1,rot=1,scl=scale)
            cmds.setKeyframe(target)


def setAllKeys():
  objList=getKeyObj()
  startTime=objList[0][2]
  endTime=cmds.currentTime(q=1)
  if startTime<=endTime:
    time=int(endTime-startTime+1)
    dir=1
    targetTime=startTime
  else:
    time=int(startTime-endTime+1)
    dir=-1
    targetTime=startTime

  print(time,dir,targetTime)
  scale=cmds.checkBox("缩放",q=1,v=1)
  for i in range(time):
    current=targetTime+(i*dir)
    cmds.currentTime(current)
    for obj in objList:
      target=obj[1]
      loc=obj[3]
      cmds.matchTransform(target,loc,pos=1,rot=1,scl=scale)
      cmds.setKeyframe(target)


def get_keyframe_times(object_name):
    # 初始化一个空列表来存储关键帧时间
    keyframe_times = []


    # 查询对象的所有可设置关键帧的属性
    keyable_attributes = cmds.listAttr(object_name, keyable=True)


    # 遍历所有可设置关键帧的属性
    for attr in keyable_attributes:
        # 构造属性的完整名称（包括对象名称）
        full_attr_name = f"{object_name}.{attr}"
        
        # 查询该属性上的关键帧时间
        times = cmds.keyframe(full_attr_name, query=True, timeChange=True)
        
        # 如果找到关键帧时间，则将它们添加到列表中
        if times:
            keyframe_times.extend(times)
    
    # 去除重复的关键帧时间（如果需要）
    keyframe_times = list(set(keyframe_times))
    
    # 返回关键帧时间列表
    return sorted(keyframe_times) 


def upScrollLlist():
    se=cmds.textScrollList("jlmb",q=1,ai=1)
    if not se:
        hh=30
    else:
        hh=30+(len(se)-1)*20
    cmds.textScrollList("jlmb",e=1,h=hh)


def selectSource():
    obj=getKeyObj()
    select=[]
    for i in obj:
        select.append(i[0])


    cmds.select(select)



import maya.cmds as cmds


def offset_keyframes(time_offset=0, value_offset=0):
    """
    偏移所有选中动画曲线的时间和数值
    :param time_offset: 时间偏移量（帧数，正数向右，负数向左）
    :param value_offset: 数值偏移量
    """
    # 获取所有选中的动画曲线
    selected_curves = cmds.ls(selection=True, type='animCurve')
    
    if not selected_curves:
        cmds.warning("未选中任何动画曲线！")
        return


    # 遍历每条动画曲线
    for curve in selected_curves:
        # 获取所有关键帧的时间列表
        key_times = cmds.keyframe(curve, query=True, timeChange=True) or []
        # 获取所有关键帧的数值列表
        key_values = cmds.keyframe(curve, query=True, valueChange=True) or []
        
        if not key_times:
            continue


        # 计算新的时间和数值
        new_times = [t + time_offset for t in key_times]
        new_values = [v + value_offset for v in key_values]


        # 批量更新关键帧（高效方式）
        cmds.keyframe(
            curve,
            edit=True,
            time=key_times,  # 原始时间作为索引
            timeChange=new_times,
            valueChange=new_values
        )

def fix_setKeys():
        """
        智能规范化旋转值到-180到180度范围，避免偏差
        """
        selected_objects = cmds.ls(selection=True)
        
        if not selected_objects:
            cmds.warning("请先选择要处理的对象")
            return
        
        for obj in selected_objects:
            print(f"处理对象: {obj}")
            
            # 方法1: 使用Maya内置的欧拉过滤器（最安全）
            try:
                cmds.select(obj)
                # 在曲线图编辑器中应用欧拉过滤器
                cmds.filterCurve()
                print(f"已对 {obj} 应用欧拉过滤器")
            except Exception as e:
                print(f"欧拉过滤器应用失败: {e}")
            
        
        print("偏差修复完成！")

def apply_offset(*_):
    # 获取偏移值
    time_offset = cmds.intField("time_field", query=True, value=True)
    value_offset = cmds.floatField("value_field", query=True, value=True)

    if not time_offset and not value_offset:
        cmds.warning("没有需要修改的数据")
        return


    # 获取选中的关键帧曲线及索引
    selected_curves = cmds.keyframe(query=True, selected=True, name=True)
    maxP=0
    for curve in list(set(selected_curves)):
        selected_indices = cmds.keyframe(curve, query=True, selected=True, indexValue=True) or []
        value=len(selected_indices)
        maxP+=value
    

    
    if not selected_curves:
        cmds.warning("请先在曲线编辑器中选择关键帧！")
        return

    # 开始撤消块
    cmds.undoInfo(openChunk=True)
    
    try:
        setkeysOffsetWins()
        cmds.progressBar("keys_progressControl", edit=True,endProgress=1)
        cmds.progressBar("keys_progressControl", edit=True,minValue=0,maxValue=maxP)
        # 遍历所有选中曲线
        for curve in list(set(selected_curves)):
            # 获取选中关键帧的索引
            selected_indices = cmds.keyframe(curve, query=True, selected=True, indexValue=True) or []
            if time_offset>0:
                selected_indices=reversed(selected_indices)

            # 按倒序处理避免索引变化
            for index in selected_indices:
                # 获取原始时间和数值
                original_times = cmds.keyframe(curve, query=True,index=(index,), timeChange=True)
                original_values = cmds.keyframe(curve, query=True,index=(index,),valueChange=True)

                if not original_times or not original_values:
                    continue
                original_time=original_times[0]
                original_value=original_values[0]

                # 计算新值
                new_time = original_time + time_offset
                new_value = original_value + value_offset
                
                # 获取目标属性,通过属性连接判断
                attr = cmds.listConnections(f"{curve}.output", destination=True, plugs=True)[0] if cmds.listConnections(f"{curve}.output") else ""
                cmds.progressBar("keys_progressControl", edit=True, step=1)
                # 数值有效性检查
                if attr:
                    if not is_value_valid(attr, new_value):
                        cmds.warning(f"跳过 {curve} 的关键帧：数值超出允许范围 " f"({round(new_value, 2)})")
                        continue
                # 检查时间冲突
                existing_times = cmds.keyframe(curve, query=True, timeChange=True) or []
                
                if new_time in existing_times and time_offset:
                    cmds.warning(f"时间 {new_time} 已存在关键帧，自动合并")
                    # 删除原有关键帧
                    cmds.cutKey(curve, time=(new_time, new_time))

                # 移动关键帧（直接修改现有关键帧）
                cmds.keyframe(curve,edit=True,index=(index,),timeChange=new_time,valueChange=new_value)

        # 整理曲线关键帧
        # for curve in list(set(selected_curves)):
        #     tc=cmds.keyframe(curve, q=True, timeChange=True)
        #     print(tc)
        #     cmds.keyframe(curve, edit=True, timeChange=cmds.keyframe(curve, q=True, timeChange=True))
        if cmds.window("setAnim_UI",ex = True):
            cmds.deleteUI("setAnim_UI")
    finally:
        # 关闭撤消块
        cmds.undoInfo(closeChunk=True)
        cmds.refresh()

def is_value_valid(attr, value):
    """属性值有效性检查"""
    node, attr_name = attr.split('.')
    
    # 检查锁定状态
    if cmds.getAttr(attr, lock=True):
        return False
    
    # 根据属性类型检查
    attr_type = cmds.attributeQuery(attr_name, node=node, attributeType=True)
    
    # 布尔类型检查
    if attr_type == "bool":
        return value in (0, 1)
    
    # 枚举类型检查
    if attr_type == "enum":
        enums = cmds.attributeQuery(attr_name, node=node, listEnum=True)[0].split(':')
        return int(value) < len(enums)
    
    # 角度类型检查（自动取模）
    if attr_type in ["doubleAngle", "floatAngle"]:
        return True  # Maya会自动处理角度循环
    
    # 其他数值类型检查最小值
    try:
        min_value = cmds.attributeQuery(attr_name, node=node, minimum=True)
        if min_value and value < min_value:
            return False
    except:
        pass
    
    # 检查最大值
    try:
        max_value = cmds.attributeQuery(attr_name, node=node, maximum=True)
        if max_value and value > max_value:
            return False
    except:
        pass
    
    return True

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

def setkeysOffsetWins():
    if cmds.window("setAnim_UI",ex = True):
        cmds.deleteUI("setAnim_UI")
        
    cmds.window("setAnim_UI" , t = u'关键帧偏移')
    cmds.columnLayout( adjustableColumn=True,rowSpacing=10,w=200)
    cmds.progressBar("keys_progressControl",maxValue=10, width=200)
    cmds.showWindow("setAnim_UI")

_expose_to_global()

# script()