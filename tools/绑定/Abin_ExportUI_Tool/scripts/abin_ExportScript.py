from functools import wraps
import maya.cmds as cmds
import maya.mel as mel
import abin_ExportCommon
import os
import random


#装饰器
def make_undo(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        cmds.undoInfo(openChunk=True )
        result = func(*args,**kwargs)
        cmds .undoInfo(closeChunk=True)
        return result
    return wrap

#初始化
def init(ui):
    shapesList = cmds.ls(type="mesh")
    transformList = cmds.listRelatives(shapesList,parent=True,type="transform")

    #判断是否符合条件
    isInit=False
    if transformList and cmds.objExists(abin_ExportCommon.ExportName.objectName.skeleton):
        for i in transformList:
            if (i.find('LOD') or i.find('DT'))>0:
                isInit=True
                break

    if isInit:
        skeName=abin_ExportCommon.ExportName.SetsName.skeletonSetsName
        lodList=[abin_ExportCommon.ExportName.SetsName.lod0SetsName,abin_ExportCommon.ExportName.SetsName.lod1SetsName,
                 abin_ExportCommon.ExportName.SetsName.lod2SetsName,abin_ExportCommon.ExportName.SetsName.lod3SetsName,abin_ExportCommon.ExportName.SetsName.lod4SetsName]
        try:
            #判断是否存在集合
            cmds.getAttr(abin_ExportCommon.ExportName.SetsName.allSetName+".nodeState")
        except:
            #创建sets集
            cmds.select(cl=1)
            lod0Sets=cmds.sets(name=lodList[0])
            lod1Sets=cmds.sets(name=lodList[1])
            lod2Sets=cmds.sets(name=lodList[2])
            lod3Sets=cmds.sets(name=lodList[3])
            lod4Sets=cmds.sets(name=lodList[4])
            skeletonSets=cmds.sets(name=skeName)
            cmds.sets(abin_ExportCommon.ExportName.objectName.skeleton,e=1,fe=skeletonSets)
            cmds.sets(lod0Sets,lod1Sets,lod2Sets,lod3Sets,lod4Sets,skeletonSets,name=abin_ExportCommon.ExportName.SetsName.allSetName)

            for i in set(transformList):
                if i.find('LOD1')>0:
                    lod=lod1Sets
                elif i.find('LOD2')>0:
                    lod=lod2Sets
                elif i.find('LOD3')>0:
                    lod=lod3Sets
                elif i.find('DT')>0:
                    lod=lod4Sets
                else:
                    lod=lod0Sets
                try:
                    cmds.setAttr(i+".overrideEnabled",1)
                except:
                    pass
                cmds.sets(i,e=1,fe=lod)

            cmds.select(cmds.sets(lodList[0],q=1),cmds.sets(lodList[1],q=1),cmds.sets(lodList[2],q=1),cmds.sets(lodList[3],q=1),cmds.sets(lodList[4],q=1))
            cmds.showHidden(a=1)

        #ui根据集合成员初始化
        for i in range(len(lodList)):
            if not (cmds.sets(lodList[i],q=1)):
                break
            index=int(cmds.getAttr(cmds.sets(lodList[i],q=1)[0]+".visibility"))
            if index:
                index=cmds.getAttr(cmds.sets(lodList[i],q=1)[0]+".overrideDisplayType")+1
            exec('ui.lod{}_showType_box.setCurrentIndex({})'.format(i,index))
            child=cmds.sets(lodList[i],q=1)
            for lod in child:
                try:
                    cmds.setAttr(lod+".visibility",cmds.getAttr(cmds.sets(lodList[i],q=1)[0]+".visibility"))
                    cmds.setAttr(lod+".overrideDisplayType",cmds.getAttr(cmds.sets(lodList[i],q=1)[0]+".overrideDisplayType"))
                except:
                    pass

        
        
        
        ui.skeletonName.setText(cmds.sets(skeName,q=1)[0])
            
#复制蒙皮
@make_undo
def cppy_Skin(jntType,sufType,InfType):
    sl=cmds.ls(sl=1,type="transform")
    if sufType==0:
        suf="closestPoint"
    elif sufType==1:
        suf="rayCast"
    elif sufType==2:
        suf="closestComponent"
    else:
        suf="uvSpace"

    if InfType==0:
        inf="closestJoint"
    elif InfType==1:
        inf="closestBone"
    elif InfType==2:
        inf="oneToOne"
    elif InfType==3:
        inf="label"
    else:
        inf="name"
        
    if jntType==0:
        for i in sl:
            shape=cmds.listRelatives(i,c=True,type="mesh")
            if (len(shape)) > 0:
                name=i[i.rfind("|")+1:len(i)]
                source=cmds.rename(i,"source_"+i)
                copy=cmds.duplicate(source,rr=1,n=name)[0]
                skin= mel.eval("findRelatedSkinCluster" +"(\""+ source +"\")")
                skinJoint=cmds.skinCluster(skin,query=True,inf=True)
                bm=cmds.skinCluster(skin,q=1,bm=1)
                sm=cmds.skinCluster(skin,q=1,sm=1)
                nw=cmds.skinCluster(skin,q=1,nw=1)
                mi=cmds.skinCluster(skin,q=1,mi=1)
                omi=cmds.skinCluster(skin,q=1,omi=1)
                wd=cmds.skinCluster(skin,q=1,wd=1)
                skin2=cmds.skinCluster(skinJoint,copy,bm=bm,sm=sm,nw=nw,mi=mi,omi=omi,wd=wd,tsb=True)[0]
                cmds.copySkinWeights(ss=skin, ds=skin2,noMirror=1,surfaceAssociation=suf,influenceAssociation=inf)
                cmds.setAttr(copy+".visibility",1)
    else:
        len2=int(len(sl)/2)
        for i in range(len2):
                skin= mel.eval("findRelatedSkinCluster" +"(\""+ sl[i] +"\")")
                skinJoint=cmds.skinCluster(skin,query=True,inf=True)

                bm=cmds.skinCluster(skin,q=1,bm=1)
                sm=cmds.skinCluster(skin,q=1,sm=1)
                nw=cmds.skinCluster(skin,q=1,nw=1)
                mi=cmds.skinCluster(skin,q=1,mi=1)
                omi=cmds.skinCluster(skin,q=1,omi=1)
                wd=cmds.skinCluster(skin,q=1,wd=1)

                skin2=cmds.skinCluster(skinJoint,sl[len2+i],bm=bm,sm=sm,nw=nw,mi=mi,omi=omi,wd=wd,tsb=True)[0]

                cmds.copySkinWeights(ss=skin, ds=skin2,noMirror=1,surfaceAssociation=suf,influenceAssociation=inf)

#选择集成员
@make_undo
def selectSets(setsNameList):
    cmds.select(setsNameList[0])
    for i in range(1,len(setsNameList)):
        cmds.select(setsNameList[i],add=1)

#改变显示模式
@make_undo
def changeShowType(setsName,type):
    child=cmds.sets(setsName,q=1)
    if not child:
        return
    for i in child:
        vis=not type
        cmds.setAttr(i+".visibility",not vis)
        if type>=1:
            cmds.setAttr(i+".overrideDisplayType",type-1)

#设置顶点颜色
@make_undo
def vtxColorShow(vis):
    if  (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod0SetsName,q=1)):
        for i in (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod0SetsName,q=1)):
            shapeList=cmds.listRelatives(i,s=1,type="mesh")
            for s in shapeList:
                try:
                    cmds.setAttr(s+".displayColors",vis)
                except:
                    pass

    if  (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod1SetsName,q=1)):
        for i in (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod1SetsName,q=1)):
            shapeList=cmds.listRelatives(i,s=1,type="mesh")
            for s in shapeList:
                try:
                    cmds.setAttr(s+".displayColors",vis)
                except:
                    pass

    if  (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod2SetsName,q=1)):
        for i in (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod2SetsName,q=1)):
            shapeList=cmds.listRelatives(i,s=1,type="mesh")
            for s in shapeList:
                try:
                    cmds.setAttr(s+".displayColors",vis)
                except:
                    pass

    if  (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod3SetsName,q=1)):
        for i in (cmds.sets(abin_ExportCommon.ExportName.SetsName.lod3SetsName,q=1)):
            shapeList=cmds.listRelatives(i,s=1,type="mesh")
            for s in shapeList:
                try:
                    cmds.setAttr(s+".displayColors",vis)
                except:
                    pass

#重新设置lod集合
@make_undo
def resetSets(setsName,control):
    sl=cmds.ls(sl=1)
    lodList=[abin_ExportCommon.ExportName.SetsName.lod0SetsName,abin_ExportCommon.ExportName.SetsName.lod1SetsName,
                 abin_ExportCommon.ExportName.SetsName.lod2SetsName,abin_ExportCommon.ExportName.SetsName.lod3SetsName,abin_ExportCommon.ExportName.SetsName.lod4SetsName]

    if setsName==abin_ExportCommon.ExportName.SetsName.skeletonSetsName:
        if len(sl)>1:
            print("超过数量，选择要导出主关节即可")
            return
        
        nodeType=cmds.nodeType(sl[0])
        if nodeType!="joint":
            print("必须全部都是joint类型")
            return
    else:
        for i in range(0,len(sl)):
            shape = cmds.listRelatives(sl[i],c=True,type="mesh")
            if not shape:
                print("必须全部都是mesh类型")
                return
            try:
                cmds.setAttr(sl[i]+".overrideEnabled",1)
            except:
                pass
            
            if setsName==abin_ExportCommon.ExportName.SetsName.allSetName:
                index=int(cmds.getAttr(sl[i]+".visibility"))
                if index:
                    index=cmds.getAttr(sl[i]+".overrideDisplayType")+1
                control[i].setCurrentIndex(index) 
                cmds.sets(cl=lodList[i])
                cmds.sets(sl[i],e=1,fe=lodList[i])


    if setsName==abin_ExportCommon.ExportName.SetsName.allSetName:
        return
    elif setsName!=abin_ExportCommon.ExportName.SetsName.skeletonSetsName:
    
        index=int(cmds.getAttr(sl[0]+".visibility"))

        if index:
            index=cmds.getAttr(sl[0]+".overrideDisplayType")+1
    
        control.setCurrentIndex(index) 
    cmds.sets(cl=setsName)
    cmds.sets(sl,e=1,fe=setsName)



#测试
@make_undo
def testAim(typ):
    if typ==2:
        #枪
        sl=cmds.ls(sl=1)
        se=[]
        for mesh in sl:
            skin=mel.eval("findRelatedSkinCluster" +"(\""+ mesh +"\")")
            # skinJoint = cmds.skinCluster(skin, query=True, inf=sl)weightedInfluence
            skinJoint = cmds.skinCluster(skin, query=True, weightedInfluence=1)

            rangeAtt=['translateY','translateX']
            rangeNumber=[-26,-35,-20,-40,25,34,47,20]

            for i in range(len(skinJoint)):
                if (skinJoint[i]=="Skeleton" ) | (skinJoint[i]=="Root"):
                    continue

                number=random.choice(rangeNumber)
                axis=random.choice(rangeAtt)
                key=skinJoint[i]+"."+axis
                start=cmds.getAttr(key)
                end=number+start
                if(cmds.getAttr(key,k=1)):
                    cmds.setKeyframe(skinJoint[i], attribute=axis)
                    cmds.setKeyframe(skinJoint[i], attribute=axis,v=end,t=10)
                    se.append(skinJoint[i])


        cmds.select(se)
    elif typ==1:
        #人物
        array=abin_ExportCommon.ExportAnimetion.human_FKctrl().fkMsgList
        axis=['.rotateX','.rotateY','.rotateZ']
        for i in array:
            for name in i['name']:
                for j in range(3):
                    att=name+axis[j]
                    if(cmds.getAttr(att,k=1)):
                        cmds.setKeyframe(name, attribute=axis[j],t=i['time'][0])
                        cmds.setKeyframe(name, attribute=axis[j],v=i['value'][j],t=i['time'][1])

#检查顶点信息
global fourVtx 
@make_undo
def check4Vtx(ui):
    sel = cmds.ls(sl=True)
    if sel == []:
        print(' =========================未选择物体 =======================')
        return
    else:
        isSuccess=True
        global fourVtx
        fourVtx=[]

        maxV=0
        for se in sel:
            skinCls = mel.eval("findRelatedSkinCluster" +"(\""+ se +"\")")
            if skinCls:
                vtxs = cmds.ls('%s.vtx[*]'%se, fl=1)
            else:
                vtxs=0
            maxV+=len(vtxs)
        print(maxV)

        ui.check_vtx_pro.setRange(0,maxV)

        ui.check_vtx_pro.reset()
        # cmds.progressBar("progressControl", edit=True,
        #         endProgress=1)
        
        # cmds.progressBar("progressControl", edit=True,
		# 		# beginProgress=True,
		# 		# isInterruptable=True,
		# 		# status='Example Calculation ...', 
        #         minValue=0,
        #         maxValue=maxV)

        proValue=0

        for se in sel:
            
            vtxs = cmds.ls('%s.vtx[*]'%se, fl=1)
            skinCls = mel.eval("findRelatedSkinCluster" +"(\""+ se +"\")")
            valueList = []
            geoOK=True
            tempList=[]
            # cmds.text("currentModel",e=1,l=se)
            ui.currentCheckModel.setText(se)
            for vtx in  vtxs:
                skinValue = cmds.skinPercent(skinCls, vtx, query=True, value=True)
                skinJoint = cmds.skinCluster(skinCls, query=True, inf=vtx)
                valueList = []
                jointList = []

                for i in range(len(skinValue)):
                    if skinValue[i] != 0.0:
                        valueList.append(skinValue[i])
                        jointList.append(skinJoint[i])
                if len(valueList) > 4:
                    msg : abin_ExportCommon.ExportName.vtxMsg = {'name':vtx,'skincluter':skinCls,'values':valueList,'joints':jointList}
                    fourVtx.append(msg)
                    tempList.append(vtx)
                    isSuccess=False
                    geoOK=False
                
                proValue+=1
                ui.check_vtx_pro.setValue(proValue)

            if  not geoOK:
                print(se+': ================= * 有超过4个骨骼的权重点 * ================= ' )
                cmds.setAttr(se+".outlinerColor",255,0,0)
                cmds.setAttr(se+".useOutlinerColor",1)   
        print(proValue)

        cmds.select(cl=1)
        cmds.select(tempList)
        if isSuccess:
            print("================= * 模型符合 * =================")

#修复顶点
@make_undo
def reset4Vtx(ui):
    #全部超过4的顶点
    global fourVtx 
    model=""
    mode=ui.reset_vtx_model.currentIndex()

    if  len(fourVtx)<=0:
        return
    
    maxV=0
    proValue=0
    if mode==2:
        for i in fourVtx:
            vtx :abin_ExportCommon.ExportName.vtxMsg=i
            count=len(vtx['values'])
            Sn=int(count*(count-1)/2)
            maxV+=(Sn+count-4)

        print(maxV)
        ui.check_vtx_pro.setRange(0,maxV)
        ui.check_vtx_pro.reset()
        
        for i in fourVtx:
            vtx :abin_ExportCommon.ExportName.vtxMsg=i
            name :str = vtx['name']
            skincluter = vtx['skincluter']
            values = vtx['values']
            joints = vtx['joints']
            model=name[0:name.find('.')]
            cmds.setAttr(model+".useOutlinerColor",0)  
            ui.currentCheckModel.setText(name)

            for n in range(len(values)-1):
                for m in range(n+1,len(values)):
                    if values[n]>values[m]:
                        temp=joints[m]
                        joints[m]=joints[n]
                        joints[n]=temp
                        
                        temp=values[m]
                        values[m]=values[n]
                        values[n]=temp
                    proValue+=1
                    # ui.check_vtx_pro.setValue(proValue)
            # print(proValue)
            for index in range(len(values)):
                if (len(values)-index)== 4:
                    break
                    # print(joints[index])
                cmds.skinPercent(skincluter,name,tv=(joints[index],0))
                proValue+=1
                ui.check_vtx_pro.setValue(proValue)
    else:
        if not mode:
            for i in fourVtx:
                vtx :abin_ExportCommon.ExportName.vtxMsg=i
                count=len(vtx['values'])-4
                maxV+=count

            print(maxV)
            ui.check_vtx_pro.setRange(0,maxV)
            ui.check_vtx_pro.reset()

            for i in fourVtx:
                vtx :abin_ExportCommon.ExportName.vtxMsg=i
                name :str = vtx['name']
                skincluter = vtx['skincluter']
                values = vtx['values']
                joints = vtx['joints']
                model=name[0:name.find('.')]
                cmds.setAttr(model+".useOutlinerColor",0)  
                ui.currentCheckModel.setText(name)

                sorted_id=sorted(range(len(values)),key=lambda k:values[k],reverse=True) 

                jointList=[]
                for index in range(4,len(sorted_id)):
                    j=sorted_id[index]
                    jointList.append((joints[j],0))
                    proValue+=1
                    ui.check_vtx_pro.setValue(proValue)
                
                cmds.skinPercent(skincluter,name,tv=jointList)
        else:
            maxV=len(fourVtx)*4
            print(maxV)
            ui.check_vtx_pro.setRange(0,maxV)
            ui.check_vtx_pro.reset()
            
            for i in fourVtx:
                vtx :abin_ExportCommon.ExportName.vtxMsg=i
                name :str = vtx['name']
                skincluter = vtx['skincluter']
                values = vtx['values']
                joints = vtx['joints']
                model=name[0:name.find('.')]
                cmds.setAttr(model+".useOutlinerColor",0)  
                ui.currentCheckModel.setText(name)

                sorted_id=sorted(range(len(values)),key=lambda k:values[k],reverse=True) 
                total=values[sorted_id[0]]+values[sorted_id[1]]+values[sorted_id[2]]+values[sorted_id[3]]
                rev=1-total

                jointList=[]
                for index in range(0,4):
                    item=sorted_id[index]
                    w=(rev*values[item]/total)+values[item]
                    j=joints[item]
                    jointList.append((j,w))
                    proValue+=1
                    ui.check_vtx_pro.setValue(proValue)
                    cmds.skinPercent(skincluter,name,tv=(j,w))
                



    if model:
        fourVtx=[]
        cmds.select(model)
        cmds.select(cl=1)
        print("================= * 修复完成 * =================")
    else:
        print(u': ================= * 未检查模型或无需修复 * ================= ' )

#选择控制器
@make_undo
def selectCtrl(isParent):
    selectList=[]
    sl=cmds.ls(sl=1,type="transform")
    if not sl:
        cmds.error("请框选全部控制器")
        return
    attList=["translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ"]
    for name in set(sl):
        for att in attList:
            state=cmds.getAttr(name+"."+att,se=1)
            if state:
                # cmds.setAttr(name+"."+att,0)
                selectList.append(name)
                break
        if isParent:
            parent=cmds.listRelatives(name,p=1,type="transform")[0]
            consConn=cmds.listConnections(parent,sh=1)
            for i in consConn:
                if i.find("Constraint")<=0:
                    conn=cmds.listConnections(parent,sh=1,type="animCurveTL")
                    if  conn:
                        for i in conn:
                            if i.find(att)>0:
                                state=cmds.getAttr(parent+"."+att,se=1)
                                if state:
                                    #cmds.setAttr(parent+"."+att,0)
                                    selectList.append(parent)
                                    break

    cmds.select(set(selectList))                               
    return  selectList                      

#控制器归零
@make_undo
def setZero(isParent):
    slList=selectCtrl(isParent)
    attList=["translateX","translateY","translateZ","rotateX","rotateY","rotateZ","scaleX","scaleY","scaleZ"]
    for name in set(slList):
        for att in attList:
            state=cmds.getAttr(name+"."+att,se=1)
            if state:
                if "scale" in att:
                    cmds.setAttr(name+"."+att,1) 
                else:
                    cmds.setAttr(name+"."+att,0)
        
#导出文件
@make_undo
def expoetLod(ui):
    path=ui.savePath_Ld.text()
    #判断是否存在文件夹，如果没有就创建
    if not (os.path.exists(path)):
        (os.makedirs(path))

    # 设置平滑组
    mel.eval("FBXExportSmoothingGroups -v true")
    # 设置平滑网格
    mel.eval("FBXExportSmoothMesh -v false")
    # 设置逐顶点分割法线
    mel.eval("FBXExportHardEdges -v  false")
    # 设置切线和法线
    mel.eval("FBXExportTangents -v  true")
    #设置三角化
    mel.eval("FBXExportColladaTriangulate  false")
    # 设置蒙皮
    mel.eval("FBXExportSkins -v  true")
    # 设置融合变形
    mel.eval("FBXExportShapes -v false")
    # 设置约束
    mel.eval("FBXExportConstraints -v false")
    # 设置包含子对象
    mel.eval("FBXExportIncludeChildren -v true")
    # 设置输入连接
    mel.eval("FBXExportInputConnections -v false")
    # 设置轴向
    axis=(ui.Axis_box.currentText()[0]).lower()
    mel.eval("FBXExportUpAxis {}".format(axis))
    # 设置引用资源内容
    mel.eval("FBXExportReferencedAssetsContent -v true")
    
    #输出名字中要剔除的字段
    removeList=["AT_","Hair_","Head_","Mergedout_",":","|","_LOD0","_DECALS"]

    #顶点色
    vtxColorShow(False)

    #是否成功
    success=0
    
    #骨架
    skeleton=cmds.sets(abin_ExportCommon.ExportName.SetsName.skeletonSetsName,q=1)[0]

    for i in range(5):

        isExport=(eval('(ui.export_lod{}.isChecked())'.format(i)))
        print(isExport)
        if not isExport:
            continue
        lodName=(eval('(abin_ExportCommon.ExportName.SetsName.lod{}SetsName)'.format(i)))

        # sl:list=cmds.sets(lodName,q=1)
        if not cmds.sets(lodName,q=1):
            continue
        try:
            with abin_ExportCommon.ExportMothon.StripNamespace("model") as stripped_nodes:
               success= exportFBX(lodName,path,skeleton,removeList)
               if not success:
                return success
        except:
            print("没有引入资源")
            success=exportFBX(lodName,path,skeleton,removeList)
            if not success:
                return success
        
            
    return success

#导出文件具体操作
def exportFBX(lodName,path,skeleton,removeList):
    sl:list=cmds.sets(lodName,q=1)
    sl.append(skeleton)
    name=sl[0]
    
    for re in removeList:
        name=name.replace(re,"")
    
    parentList=[]
    for i in sl:
        p=cmds.listRelatives(i,p=1)
        if p:
            parentList.append(p[0])
            cmds.parent(i,w=1)

    exportName=path+"\\"+name

    # print(parentList)
    # print(sl)
    # print(exportName)
    try:
        cmds.select(sl)
        cmds.file(exportName,force=1,type="FBX export",exportSelected=True)
        for j in range(len(parentList)):
            cmds.parent(sl[j],parentList[j])
        print("导出成功： "+name)
        return 1
    except RuntimeError:
        for j in range(len(parentList)):
            cmds.parent(sl[j],parentList[j])
        print("导出失败： "+name)
        return 0

#导入文件
@make_undo
def importFile(ui):
    typ=ui.ImportType_btn.currentText()
    path=path=ui.savePath_Ld.text()
    if not (os.path.exists(path)):
        cmds.error("文件夹不存在,点击选择路径重新选择")
        return
    files=os.listdir(path)
    for f in files:
        data=os.path.join(path,f)
        suffix=f.split('.')[-1]
        if suffix==typ:
            try:
                cmds.file(data,ns='ns',i=True,rnn=True)
                print("导入成功")
            except:
                cmds.error("导入失败")

#引用文件
@make_undo
def refFile(path):
    
    suffix=path.split('.')[-1]
    print(suffix)
    if suffix=="ma":
        typ="mayaAscii"
    elif suffix=="mb":
        typ="mayaBinary"
    elif suffix=="fbx":
        typ="fbx"
    
    isSave=1
    if isSave:
        cmds.file(path, r=1, type=typ, namespace=":", options="v=0")
    else:
    # cmds.file(path,r=1,type=typ,ignoreVersion=1,gl=1,shd="shadingNetworks",mergeNamespacesOnClash=1,namespace=":",options="v=0")
        cmds.file(path,r=1,type=typ,ignoreVersion=1,gl=1,shd="shadingNetworks",mergeNamespacesOnClash=1,namespace=":model",options="v=0")

#权重1
@make_undo
def weight1(ui):
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning("请先选择面/顶点和骨骼")
        return

    # 分离面、顶点和骨骼（修正顶点后缀为.vtx[）
    faces = [s for s in selection if ".f[" in s]          # 面组件（如"pCube1.f[0]"）
    vertices = [s for s in selection if ".vtx[" in s]     # 顶点组件（如"pCube1.vtx[0]"）
    joints = [s for s in selection if not (".f[" in s or ".vtx[" in s)]  # 骨骼（非面/顶点组件）

    # 检查是否选择了面或顶点
    if not faces and not vertices:
        cmds.warning("请至少选择一个面或顶点")
        return

    # 获取网格对象（优先使用面/顶点的父对象）
    if faces:
        mesh = faces[0].split('.')[0]
    elif vertices:
        mesh = vertices[0].split('.')[0]
    else:
        cmds.warning("无有效选择")  # 理论上不会触发，因前面已检查
        return

    # 检查皮肤簇
    skin_cluster = mel.eval('findRelatedSkinCluster "{}"'.format(mesh))
    if not skin_cluster:
        cmds.warning("网格未绑定蒙皮: {}".format(mesh))
        return

    # 初始化进度条
    ui.check_vtx_pro.setMaximum(100)
    ui.check_vtx_pro.setValue(0)

    autoWeight=[]

     # 确定要处理的顶点（面转顶点 或 直接选顶点）
    if faces:
        vertices_to_process = set()
        for face in faces:
            face_verts = cmds.polyListComponentConversion(face, fromFace=True, toVertex=True)
            vertices_to_process.update(cmds.ls(face_verts, flatten=True))
            autoWeight.append(face_verts)
        vertices_to_process = list(vertices_to_process)
    else:
        vertices_to_process = set()
        for vtx in vertices:
            vertices_to_process.update(cmds.ls(vtx, flatten=True))
            autoWeight.append(vtx)
        vertices_to_process = list(set(vertices_to_process))  # 去重

    total_vertices = len(vertices_to_process)
    if total_vertices == 0:
        cmds.warning("没有找到可处理的顶点")
        return
    
    # 自动选择骨骼模式（未手动选骨骼）
    if not joints:
        processed_vertices = 0
        total_vertices=total_vertices*len(autoWeight)
        for face_verts in autoWeight:
            vtxs=set(cmds.ls(face_verts, flatten=True))
            # 统计权重最高的骨骼
            bone_counter ={}
            # 处理每个顶点（自动找权重最高的骨骼）
            for i, vtx in enumerate(vtxs):
                # 获取当前顶点的权重信息
                weights = cmds.skinPercent(skin_cluster, vtx, query=True, value=True)
                skin_joints = cmds.skinPercent(skin_cluster, vtx, query=True, transform=None)

                max_value = max(weights)
                max_index = weights.index(max_value)

                jnt=skin_joints[max_index]
                bone_counter[jnt]=bone_counter.get(jnt, 0) + 1
                

            target_joint = max(bone_counter, key=bone_counter.get)

            for i, vtx in enumerate(vtxs):
                # 获取当前顶点的权重信息
                skin_jnts = cmds.skinPercent(skin_cluster, vtx, query=True, transform=None)
                jointList=[]
                for jnt in skin_jnts:
                    cmds.setAttr(jnt+'.liw',0)
                    jointList.append((jnt,0))

                jointList.append((target_joint,1))

                cmds.skinPercent(skin_cluster,vtx,tv=(target_joint,1))

                processed_vertices += 1
                progress = int((processed_vertices / total_vertices) * 100)
                ui.check_vtx_pro.setValue(progress)


    # 手动选择骨骼模式（已手动选骨骼）
    else:
        if len(joints) > 1:
            cmds.warning("手动模式只能选择一个骨骼")
            return

        target_joint = joints[0]

        # 检查骨骼是否在蒙皮影响列表中
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
        if target_joint not in influences:
            cmds.warning("骨骼 {} 不是蒙皮影响对象".format(target_joint))
            return

        # 处理每个顶点（强制权重给指定骨骼）
        for i, vtx in enumerate(vertices_to_process):
            # 获取当前顶点的权重信息
            skin_jnts = cmds.skinPercent(skin_cluster, vtx, query=True, transform=None)
            jointList=[]
            for jnt in skin_jnts:
                cmds.setAttr(jnt+'.liw',0)
                jointList.append((jnt,0))

            jointList.append((target_joint,1))

            cmds.skinPercent(skin_cluster,vtx,tv=(target_joint,1))

            # 更新进度条
            progress = int(((i + 1) / total_vertices) * 100)
            ui.check_vtx_pro.setValue(progress)

    # 恢复选择（原始选择：面/顶点）
    cmds.select(faces if faces else vertices)
    print("权重转移成功！顶点权重已转移到骨骼: {}".format(target_joint))

    

    # 处理完成
    ui.check_vtx_pro.setValue(100)
    cmds.refresh()
    cmds.select(faces if faces else vertices)  # 恢复原始选择（面/顶点）

#剪切权重
@make_undo
def transfer_skin_weights(ui,skin_clusters):
    """
    将选中骨骼的权重转移到最后一个选择的骨骼
    源骨骼权重清零但保留在绑定中
    选择顺序：先选源骨骼，最后选目标骨骼
    """
    # 获取当前选择的骨骼
    selected_joints = cmds.ls(selection=True, type='joint')
    
    # 确定源骨骼和目标骨骼
    source_joints = selected_joints[:-1]  # 除最后一个外的所有骨骼
    target_joint = selected_joints[-1]    # 最后一个骨骼
    
    
    # 计算总顶点数用于进度条
    total_vertices = 0
    for skin_cluster in skin_clusters:
        geometries = cmds.skinCluster(skin_cluster, query=True, geometry=True) or []
        for geo in geometries:
            total_vertices += cmds.polyEvaluate(geo, vertex=True)
    
    # 如果没有顶点需要处理
    if total_vertices == 0:
        cmds.warning("未找到需要处理的顶点")
        return
    
    # 初始化进度条
    ui.check_vtx_pro.setMaximum(100)  # 设置最大值为100%
    ui.check_vtx_pro.setValue(0)      # 初始值为0
    processed_vertices = 0
    # 处理每个皮肤簇
    for skin_cluster in skin_clusters:
        # 获取受影响的几何体
        geometries = cmds.skinCluster(skin_cluster, query=True, geometry=True) or []
        name = cmds.listRelatives(geometries[0], parent=True, type='transform')[0]
        ui.currentCheckModel.setText(f"处理 {name} 中...")
        # 备份当前选择
        original_selection = cmds.ls(selection=True)
        
        for geo in geometries:
            
            # 确保目标骨骼在皮肤簇影响列表中
            influences = cmds.skinCluster(skin_cluster, query=True, influence=True) or []
            if target_joint not in influences:
                cmds.skinCluster(skin_cluster, edit=True, addInfluence=target_joint, weight=0)
            
            # 获取顶点数量
            vtx_count = cmds.polyEvaluate(geo, vertex=True)
            
            # 处理每个顶点
            for vtx_id in range(vtx_count):
                
                # 更新进度条
                processed_vertices += 1
                progress_percent = int((processed_vertices / total_vertices) * 100)
                ui.check_vtx_pro.setValue(progress_percent)
                
                vtx = f"{geo}.vtx[{vtx_id}]"

                # 获取当前权重值
                weights = cmds.skinPercent(skin_cluster, vtx, query=True, value=True)
                influences = cmds.skinPercent(skin_cluster, vtx, query=True, transform=None)
                
                # 创建权重字典
                weight_dict = dict(zip(influences, weights))
                
                # 计算要转移的总权重
                transfer_weight = 0.0
                for joint in source_joints:
                    if joint in weight_dict:
                        transfer_weight += weight_dict[joint]
                
                # 如果有权重要转移
                if transfer_weight > 0:
                    # 获取目标骨骼当前权重
                    target_current = weight_dict.get(target_joint, 0.0)
                    
                    # 设置新的目标骨骼权重
                    new_target_weight = target_current + transfer_weight
                    
                    # 准备权重设置列表
                    transform_values = [(target_joint, new_target_weight)]
                    
                    # 添加源骨骼（权重设为0）
                    for joint in source_joints:
                        if joint in weight_dict:
                            transform_values.append((joint, 0.0))
                    
                    # 应用新的权重（Maya会自动归一化）
                    cmds.skinPercent(
                        skin_cluster, 
                        vtx, 
                        transformValue=transform_values,
                        normalize=True
                    )
            
        
        # 恢复原始选择
        cmds.select(original_selection, replace=True)
        ui.currentCheckModel.setText(f"成功将 {len(source_joints)} 个骨骼的权重转移到 {target_joint}")


#设置颜色
@make_undo
def setColor():
    sl=cmds.ls(sl=1)
    color=17
    for i in sl:
        try:
            shapes=cmds.listRelatives(i,c=1,s=1)
            for s in shapes:
                cmds.setAttr(s+".overrideEnabled",1)
                cmds.setAttr(s+".overrideColor",color)
        except:
            cmds.setAttr(i+".overrideEnabled",1)
            cmds.setAttr(i+".overrideColor",color)


#改大写并添加_LOD0
@make_undo
def changeName():
    sl=cmds.ls(sl=1)
    for i in sl:
        temp=i.upper()

        if '_LOD0' not in sl:
            temp=temp+'_LOD0'

        cmds.rename(i,temp)
#改大写并添加_LOD0
@make_undo
def PolySelectTraverse():
    mel.eval("select `ls -sl`;PolySelectTraverse 1;select `ls -sl`;")