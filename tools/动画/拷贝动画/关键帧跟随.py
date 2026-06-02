import maya.cmds as cmds

# ============================================================
#   关键帧跟随工具  v1.1
#   功能：记录两个对象的相对位置，并将源对象的运动烘焙到目标对象上
#   作者：Abin
# ============================================================

# ------------------------------------------------------------------ #
#  常量 / 配置
# ------------------------------------------------------------------ #
TEMP_GRP = "setKeys_Temp"          # 场景中存放约束记录节点的组名
WIN_ID   = "KeyFollowUI"           # 主窗口 ID


# ================================================================== #
#  UI
# ================================================================== #

def KeyFollowUI():
    """打开关键帧跟随主窗口"""
    if cmds.window(WIN_ID, ex=True):
        cmds.deleteUI(WIN_ID)

    cmds.window(WIN_ID, t=u"关键帧跟随", w=420, sizeable=True)
    cmds.columnLayout("kf_main", columnAttach=('both', 8), rowSpacing=5, columnWidth=420, adj=True)

    # ---- 说明 ----
    cmds.text(
        label="① 选源对象 + 目标对象，到起始帧点【记录】\n② 填写起止帧，点【逐帧烘焙】",
        align="left", h=40, fn="smallPlainLabelFont"
    )

    cmds.separator(h=6, style="in")

    # ---- 选项行 ----
    cmds.rowLayout("kf_opt_row", numberOfColumns=2, columnWidth2=(120, 120),
                   columnAttach2=("left", "left"))
    cmds.checkBox("kf_cb_scale",  label="包含缩放", h=30, v=False)
    cmds.checkBox("kf_cb_offset", label="保持偏移", h=30, v=True)
    cmds.setParent("..")

    # ---- 定位器 + 记录操作行 ----
    cmds.rowLayout("kf_rec_row", numberOfColumns=5, adj=5,
                   columnWidth5=(85, 75, 75, 90, 90),
                   columnAttach5=("both", "both", "both", "both", "both"))
    cmds.button("kf_btn_locator",  label="创建定位器", h=35,
                c="KeyFollowTool.createLocator()",
                bgc=[0.5, 0.7, 0.9],
                ann="无选中：创建定位器到世界原点\n有选中：创建定位器并对齐到选中对象的位移和旋转")
    cmds.button("kf_btn_align",    label="对齐",       h=35,
                c="KeyFollowTool.alignTransform()",
                bgc=[0.5, 0.8, 1.0],
                ann="先选源对象，再选目标对象\n将目标对齐到源的位置和旋转")
    cmds.button("kf_btn_record",   label="记录",       h=35,
                c="KeyFollowTool.getLine()",
                bgc=[0.8, 0.9, 0.8],
                ann="先选源对象，再选目标对象，点此记录当前帧位置")
    cmds.button("kf_btn_clearAll", label="清除全部",   h=35,
                c="KeyFollowTool.removeAllScroll()",
                ann="清空列表并删除场景中所有记录节点")
    cmds.button("kf_btn_clearSel", label="删除选中",   h=35,
                c="KeyFollowTool.removeSelect()",
                ann="只删除列表中当前选中的记录")
    cmds.setParent("..")

    # ---- 记录列表 ----
    items = _build_scroll_items()
    hh = max(60, 60 + len(items) * 20) if items else 60
    cmds.textScrollList("kf_scroll", h=hh, pma=0, ams=1,
                        a=items, sc="KeyFollowTool.selectSource()")

    cmds.separator(h=6, style="in")

    # ---- 烘焙按钮行 ----
    # ---- 帧范围输入行 ----
    anim_start = int(cmds.playbackOptions(q=True, animationStartTime=True))
    anim_end   = int(cmds.playbackOptions(q=True, animationEndTime=True))
    cmds.rowLayout("kf_range_row", numberOfColumns=4,
                   columnWidth4=(60, 80, 60, 80),
                   columnAttach4=("both","both","both","both"))
    cmds.text(label="起始帧", align="right")
    cmds.intField("kf_start_frame", v=anim_start, w=80, ann="烘焙起始帧")
    cmds.text(label="结尾帧", align="right")
    cmds.intField("kf_end_frame",   v=anim_end,   w=80, ann="烘焙结尾帧")
    cmds.setParent("..")

    # ---- 烘焙按钮行 ----
    cmds.rowLayout("kf_bake_row", numberOfColumns=2, adj=2,
                   columnWidth2=(200, 180),
                   columnAttach2=("both", "both"))
    cmds.button("kf_btn_bakeAll", label="逐帧烘焙", h=35,
                c="KeyFollowTool.setAllKeys()",
                bgc=[0.9, 0.7, 0.7],
                ann="在起止帧范围内每帧打关键帧")
    cmds.button("kf_btn_fix",     label="欧拉角过滤",  h=35,
                c="KeyFollowTool.fix_setKeys()",
                bgc=[0.8, 0.5, 0.5],
                ann="修复烘焙后旋转抖动/翻转问题")
    cmds.setParent("..")

    cmds.showWindow(WIN_ID)


# ================================================================== #
#  核心逻辑
# ================================================================== #

def alignTransform():
    """对齐：先选源对象，再选目标对象，将目标的位置和旋转对齐到源"""
    sl = cmds.ls(sl=1)
    if len(sl) < 2:
        cmds.error("至少选择2个对象（先选源，后选目标）")
        return
    cmds.undoInfo(openChunk=True)
    try:
        for target in sl[1:]:
            cmds.matchTransform(target, sl[0], pos=1, rot=1, scl=0)
            print(f"{target} 已对齐到 {sl[0]}")
    finally:
        cmds.undoInfo(closeChunk=True)


def createLocator():
    """创建定位器：无选中则在原点创建；有选中则创建后对齐到选中对象"""
    sl = cmds.ls(sl=1)
    cmds.undoInfo(openChunk=True)
    try:
        loc = cmds.spaceLocator(n="locator#")[0]
        # 设置局部显示比例为 10
        cmds.setAttr(loc + ".localScaleX", 10)
        cmds.setAttr(loc + ".localScaleY", 10)
        cmds.setAttr(loc + ".localScaleZ", 10)
        if sl:
            cmds.matchTransform(loc, sl[0], pos=1, rot=1, scl=0)
            print(f"定位器 {loc} 已对齐到 {sl[0]}")
        else:
            print(f"定位器 {loc} 已创建在世界原点")
        cmds.select(loc)
    finally:
        cmds.undoInfo(closeChunk=True)


def getLine():
    """记录两个对象当前帧的相对位置，创建约束节点"""
    sl = cmds.ls(sl=1)
    if len(sl) < 2:
        cmds.error("至少选择2个对象（先选源对象，后选目标对象）")
        return

    source = sl[0]
    target = sl[1]
    time   = int(cmds.currentTime(q=1))
    grp    = TEMP_GRP
    mo     = cmds.checkBox("kf_cb_offset", q=1, v=1)
    scale  = cmds.checkBox("kf_cb_scale",  q=1, v=1)

    node_name = source + "____" + target + "____" + str(time)

    # 已存在则刷新
    if cmds.objExists(node_name):
        cmds.warning("记录已存在，刷新位置")
        cmds.delete(node_name)

    if not mo:
        cmds.matchTransform(target, source, pos=1, rot=1, scl=0)

    point = cmds.createNode("transform", n=node_name)
    cmds.matchTransform(point, target)
    cmds.parentConstraint(source, point, mo=1)
    if scale:
        cmds.scaleConstraint(source, point, mo=0)

    if not cmds.objExists(grp):
        cmds.createNode("transform", n=grp)
    cmds.parent(point, grp)

    # 刷新列表
    _refresh_scroll()


def setAllKeys():
    """逐帧烘焙：在输入框指定的起止帧范围内逐帧打关键帧"""
    obj_list = _getKeyObj()
    if not obj_list:
        cmds.warning("列表为空，请先记录对象")
        return

    start_time = cmds.intField("kf_start_frame", q=1, v=1)
    end_time   = cmds.intField("kf_end_frame",   q=1, v=1)
    scale      = cmds.checkBox("kf_cb_scale", q=1, v=1)

    if start_time <= end_time:
        total     = int(end_time - start_time + 1)
        direction = 1
    else:
        total     = int(start_time - end_time + 1)
        direction = -1

    cmds.undoInfo(openChunk=True)
    try:
        for i in range(total):
            current = start_time + i * direction
            cmds.currentTime(current)
            for obj in obj_list:
                target = obj[1]
                loc    = obj[3]
                cmds.matchTransform(target, loc, pos=1, rot=1, scl=scale)
                cmds.setKeyframe(target)
    finally:
        cmds.undoInfo(closeChunk=True)




def fix_setKeys():
    """对选中对象应用欧拉过滤器，修复旋转偏差"""
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("请先选择要处理的对象")
        return

    cmds.undoInfo(openChunk=True)
    try:
        for obj in selected:
            try:
                cmds.select(obj)
                cmds.filterCurve()
                print(f"已对 {obj} 应用欧拉过滤器")
            except Exception as e:
                print(f"欧拉过滤器应用失败 [{obj}]: {e}")
    finally:
        cmds.undoInfo(closeChunk=True)

    print("偏差修复完成！")


def removeAllScroll():
    """清除列表及场景中所有约束记录"""
    cmds.textScrollList("kf_scroll", e=1, ra=1)
    if cmds.objExists(TEMP_GRP):
        cmds.delete(TEMP_GRP)
    _update_scroll_height()


def removeSelect():
    """删除列表中选中的约束记录"""
    obj_list = _getKeyObj()
    for item in obj_list:
        node = item[0] + "____" + item[1] + "____" + str(item[2])
        if cmds.objExists(node):
            cmds.delete(node)

    sel_indices = cmds.textScrollList("kf_scroll", q=1, sii=1) or []
    for i, idx in enumerate(sel_indices):
        cmds.textScrollList("kf_scroll", e=1, rii=idx - i)

    _update_scroll_height()


def selectSource():
    """在列表中选中条目时，同步选中场景中的源对象"""
    obj_list = _getKeyObj()
    select = [item[0] for item in obj_list]
    if select:
        cmds.select(select)


# ================================================================== #
#  内部辅助函数（以 _ 开头，不暴露到全局）
# ================================================================== #

def _getKeyObj():
    """解析列表中选中的条目，返回 [source, target, time, loc_node] 列表"""
    items = cmds.textScrollList("kf_scroll", q=1, ai=1) or []
    result = []
    for item in items:
        idx1   = item.find(',')
        idx2   = item.find('>')
        idx3   = item.find('帧')
        end    = len(item)
        source = item[0:idx1 - 1]
        target = item[idx1 + 2:idx2 - 2]
        time   = int(item[idx3 + 2:end])
        loc    = source + "____" + target + "____" + str(time)
        result.append([source, target, time, loc])
    return result


def _get_keyframe_times(object_name):
    """获取对象所有属性上的关键帧时间（去重排序）"""
    keyframe_times = []
    keyable_attrs = cmds.listAttr(object_name, keyable=True) or []
    for attr in keyable_attrs:
        times = cmds.keyframe(f"{object_name}.{attr}", query=True, timeChange=True)
        if times:
            keyframe_times.extend(times)
    return sorted(set(keyframe_times))


def _build_scroll_items():
    """从场景中读取已有的约束记录，构建列表条目"""
    items = []
    if cmds.objExists(TEMP_GRP):
        childs = cmds.listRelatives(TEMP_GRP, c=1) or []
        for node in childs:
            i1 = node.find("____")
            i2 = node.rfind("____")
            if i1 == -1 or i1 == i2:
                continue
            src  = node[0:i1]
            tgt  = node[i1 + 4:i2]
            time = node[i2 + 4:]
            items.append(f"{src} , {tgt}  >>>>>>>>  pose帧:{time}")
    return items


def _refresh_scroll():
    """重新构建列表内容"""
    items = _build_scroll_items()
    cmds.textScrollList("kf_scroll", e=1, ra=1)
    if items:
        cmds.textScrollList("kf_scroll", e=1, a=items)
    _update_scroll_height()


def _update_scroll_height():
    """根据条目数量动态调整列表高度"""
    items = cmds.textScrollList("kf_scroll", q=1, ai=1) or []
    hh = max(60, 60 + len(items) * 20)
    cmds.textScrollList("kf_scroll", e=1, h=hh)


# ================================================================== #
#  全局注入（供 UI 按钮字符串命令调用）
# ================================================================== #

class _ModuleProxy:
    """代理对象，让 UI 按钮可以用 KeyFollowTool.xxx() 的方式调用"""
    alignTransform  = staticmethod(alignTransform)
    createLocator   = staticmethod(createLocator)
    getLine         = staticmethod(getLine)
    setAllKeys      = staticmethod(setAllKeys)
    fix_setKeys     = staticmethod(fix_setKeys)
    removeAllScroll = staticmethod(removeAllScroll)
    removeSelect    = staticmethod(removeSelect)
    selectSource    = staticmethod(selectSource)


def _expose_to_global():
    """将代理对象注入 Maya 全局作用域，避免污染全局命名空间"""
    import __main__
    __main__.__dict__["KeyFollowTool"] = _ModuleProxy()


_expose_to_global()

# ---- 启动 ----
KeyFollowUI()


