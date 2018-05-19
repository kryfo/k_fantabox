#!usr/bin/env python
#coding: utf-8

import maya.cmds as mc
import maya.mel as mm
def shuai_autoFacialRig():
    global path
    path=mc.getModulePath(moduleName='hq_maya')
    if mc.window('autoFacialRigWin',ex=1):
        mc.deleteUI('autoFacialRigWin')
    autoFacialWin=mc.window('autoFacialRigWin',t='Auto Facial Rig Window',w=300,h=200)
    mc.columnLayout(adjustableColumn=1)
    mc.button(l='导入表情控制器面板',c='fb.rig.FacialRig.autoFacialRig.importFacialTmp()')
    mc.text('选择做好设置的头部模型，获取到下面')
    mc.textFieldButtonGrp('getSouceObj',bl='获取',l='头部蒙皮模型：',adjustableColumn=2,bc='fb.rig.FacialRig.autoFacialRig.getSouceObjCmd()')
    mc.text('选择所有目标体，然后点击“连接blendshapes”按钮')
    mc.button(l='连接blendshapes',c='fb.rig.FacialRig.autoFacialRig.buildBlendshapeConnections()')
    mc.text('下面显示的目标体没有正确连接，可能是因为命名问题：')
    mc.textFieldButtonGrp('WrongObjsWin',ed=0,bl='选择',l='问题目标体：',adjustableColumn=2,bc='fb.rig.FacialRig.autoFacialRig.selectWrongObjCmd()')
    mc.separator(style="double")
    mc.button(l='导入dx11Shader节点网络',c='fb.rig.FacialRig.autoFacialRig.importDX11Shader()')
    mc.text('贴图路径，如：（ O:/LaMaChuanQi/Rigging/LuoCha/sourceimages/LuoCha ）')
    mc.textFieldButtonGrp('mapsPath',bl='浏览',l='绝对路径：',adjustableColumn=2,bc='fb.rig.FacialRig.autoFacialRig.getMapsPath()')
    mc.button(l='自动读取贴图',c='fb.rig.FacialRig.autoFacialRig.readMaps()')
    mc.separator(style="double")
    mc.textFieldButtonGrp('SGNodeWin',bl='获取',l='获取渲染SG节点：',adjustableColumn=2,bc='fb.rig.FacialRig.autoFacialRig.getSGNodeCmd()')
    mc.button(l='连接到SG节点',c='fb.rig.FacialRig.autoFacialRig.connectToSgNode()')
    mc.separator(style="double")
    mc.button(l='提取blendshapes',c='fb.rig.FacialRig.autoFacialRig.getBlendshapes()')
    mc.separator(style="double")
    mc.button(l='选择环线切头',c='fb.rig.FacialRig.autoFacialRig.getcuthead()')
    mc.showWindow(autoFacialWin)
def connectToSgNode():
    sgNode=mc.textFieldButtonGrp('SGNodeWin',q=1,tx=1)
    renderShader=mc.listConnections(sgNode+'.surfaceShader',p=1)
    if renderShader:
        mc.connectAttr(renderShader[0],sgNode+'.aiSurfaceShader',f=1)
        mc.connectAttr('dx11Shader4.outColor',sgNode+'.surfaceShader',f=1)
        mc.connectAttr('LaMa_AS101.displacement',sgNode+'.displacementShader',f=1)
    else:
        mc.warning('can not find the render shader !!')
def getSGNodeCmd():
    obj=mc.ls(sl=1)[0]
    mc.textFieldButtonGrp('SGNodeWin',e=1,tx=obj)
def getBlendshapes():
    mm.eval('source \"%s/blendshapeExport.mel\"'%(path+"/scripts/fantabox/rigging/FacialRig"))
def buildBlendshapeConnections():
    BSmesh=[u'BS_AU1_L', u'BS_AU1_R', u'BS_AU2_L', u'BS_AU2_R', u'BS_AU4_L', u'BS_AU4_R', u'BS_AU5_L', u'BS_AU5_R', u'BS_AU6_L', u'BS_AU6_R', u'BS_AU7_L', u'BS_AU7_R', u'BS_AU9_L', u'BS_AU9_R', u'BS_AU10_L', u'BS_AU10_R', u'BS_AU10O_L', u'BS_AU10O_R', u'BS_AU11_L', u'BS_AU11_R', u'BS_AU12_L', u'BS_AU12_R', u'BS_AU12O_L', u'BS_AU12O_R', u'BS_AU13_L', u'BS_AU13_R', u'BS_AU14_L', u'BS_AU14_R', u'BS_AU15_L', u'BS_AU15_R', u'BS_AU16_L', u'BS_AU16_R', u'BS_AU17_U', u'BS_AU17_D', u'BS_AU18_L', u'BS_AU18_R', u'BS_AU20_L', u'BS_AU20_R', u'BS_AU22_U', u'BS_AU22_D', u'BS_AU23_U', u'BS_AU23_D', u'BS_AU25_U', u'BS_AU25_D', u'BS_PUFF_L', u'BS_PUFF_R', u'BS_SHRINK_L', u'BS_SHRINK_R', u'BS_blinkFix_L', u'BS_blinkFix_R', u'BS_U', u'BS_SH', u'BS_E', u'BS_F', u'BS_M', u'BS_O', 'BS_AU24', 'BS_AU28_U', 'BS_AU28_D', 'BS_mouth_L', 'BS_mouth_R', 'BS_mouth_U', 'BS_mouth_D', 'BS_mouth_Out', 'BS_mouth_In']
    CtrlPlug=['Brow_L_001_CTRL.ty', 'Brow_R_001_CTRL.ty', 'Brow_L_002_CTRL.ty', 'Brow_R_002_CTRL.ty', 'Brow_L_001_CTRL.tx', 'Brow_R_001_CTRL.tx', 'UpperLid_L_001_CTRL.ty', 'UpperLid_R_001_CTRL.ty', 'EyeCorner_L_001_CTRL.tx', 'EyeCorner_R_001_CTRL.tx', 'LowerLid_L_001_CTRL.ty', 'LowerLid_R_001_CTRL.ty', 'Nosewing_L_001_CTRL.ty', 'Nosewing_R_001_CTRL.ty', 'Muzzle_L_001_CTRL.ty', 'Muzzle_R_001_CTRL.ty', 'UpperLip_L_001_CTRL.ty', 'UpperLip_R_001_CTRL.ty', 'Nosewing_L_001_CTRL.tx', 'Nosewing_R_001_CTRL.tx', 'MouthCorner_L_002_CTRL.tx', 'MouthCorner_R_002_CTRL.tx', 'LowerLip_L_001_CTRL.ty', 'LowerLip_R_001_CTRL.ty', 'MouthCorner_L_002_CTRL.ty', 'MouthCorner_R_002_CTRL.ty', 'MouthCorner_L_001_CTRL.tx', 'MouthCorner_R_001_CTRL.tx', 'MouthCorner_L_001_CTRL.ty', 'MouthCorner_R_001_CTRL.ty', 'Chin_L_001_CTRL.ty', 'Chin_R_001_CTRL.ty', 'UpperLip_C_001_CTRL.ty', 'LowerLip_C_001_CTRL.ty', 'MouthCorner_L_001_CTRL.tx', 'MouthCorner_R_001_CTRL.tx', 'Chin_L_002_CTRL.ty', 'Chin_R_002_CTRL.ty', 'UpperLip_C_001_CTRL.tz', 'LowerLip_C_001_CTRL.tz', 'UpperLip_C_001_CTRL.tz', 'LowerLip_C_001_CTRL.tz', 'Chin_C_001_CTRL.ty', 'Chin_C_001_CTRL.ty', 'Cheek_L_001_CTRL.tx', 'Cheek_R_001_CTRL.tx', 'Cheek_L_001_CTRL.tx', 'Cheek_R_001_CTRL.tx', 'UpperLid_L_001_CTRL.ty', 'UpperLid_R_001_CTRL.ty', 'Face_U_ctrl.tx', 'Face_SH_ctrl.tx', 'Face_E_ctrl.tx', 'Face_F_ctrl.tx', 'Face_M_ctrl.tx', 'Face_O_ctrl.tx', 'Chin_C_001_CTRL.ty', 'UpperLip_C_001_CTRL.ty', 'LowerLip_C_001_CTRL.ty', 'Mouth_C_001_CTRL.tx', 'Mouth_C_001_CTRL.tx', 'Mouth_C_001_CTRL.ty', 'Mouth_C_001_CTRL.ty', 'Mouth_C_001_CTRL.tz', 'Mouth_C_001_CTRL.tz']
    values=[1, 1, 1, 1, -1, -1, 0.5, 0.5, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -0.5, -0.5, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1]
    wrinkleAttr=["dx11Shader_ast.AU1_L","dx11Shader_ast.AU1_R","dx11Shader_ast.AU2_L","dx11Shader_ast.AU2_R","dx11Shader_ast.AU4_L","dx11Shader_ast.AU4_R","dx11Shader_ast.AU6_L","dx11Shader_ast.AU6_R","dx11Shader_ast.AU9_L","dx11Shader_ast.AU9_R","dx11Shader_ast.AU10_L","dx11Shader_ast.AU10_R","dx11Shader_ast.AU12_L","dx11Shader_ast.AU12_R","dx11Shader_ast.AU14_L","dx11Shader_ast.AU14_R","dx11Shader_ast.AU15_L","dx11Shader_ast.AU15_R","dx11Shader_ast.AU17_D","dx11Shader_ast.AU20_L","dx11Shader_ast.AU20_R"]
    wrinkleIndex=[0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 14, 15, 20, 21, 26, 27, 28, 29, 33, 36, 37]
                                                                                                                                                                                                                                                                            
    skinObj=mc.textFieldButtonGrp('getSouceObj',q=1,tx=1)
    inputs=mm.eval('findRelatedDeformer(\"%s\")'%skinObj)
    BSNode='Facial_BS'
    if not BSNode in inputs:
        mc.blendShape(skinObj,frontOfChain=1,n='Facial_BS')[0]
    FacialMeshes=mc.ls(sl=1)
    WrongMeshes=[]
    for i in FacialMeshes:
        weights=mc.listAttr(BSNode+'.weight',m=1)
        if not weights:
            weights=[]
        if not i in BSmesh:
            WrongMeshes.append(i)
        elif i in weights:
            id=weights.index(i)
            mc.blendShape(BSNode,e=1,tc=0,ib=1,t=[skinObj,id,i,1])
        else:
            lastID=len(weights)
            mc.blendShape(BSNode,e=1,tc=0,t=[skinObj,lastID,i,1])
    for i in BSmesh:
        driverId=BSmesh.index(i)
        if mc.attributeQuery(i,node=BSNode,ex=1):
            mc.setDrivenKeyframe(BSNode,cd=CtrlPlug[driverId],at=i,dv=0.0,v=0.0)
            mc.setDrivenKeyframe(BSNode,cd=CtrlPlug[driverId],at=i,dv=values[driverId],v=1)
        if mc.objExists('dx11Shader_ast'):
            if driverId in wrinkleIndex:
                [drivenNode,drivenAttr]=wrinkleAttr[wrinkleIndex.index(driverId)].split('.')
                mc.setDrivenKeyframe(drivenNode,cd=CtrlPlug[driverId],at=drivenAttr,dv=0.0,v=0.0)
                mc.setDrivenKeyframe(drivenNode,cd=CtrlPlug[driverId],at=drivenAttr,dv=values[driverId],v=1)
    wrongText=''
    for i in WrongMeshes:
        wrongText+=i+','
    if len(wrongText)>0:
        newText=wrongText[:-1]
        mc.textFieldButtonGrp('WrongObjsWin',e=1,tx=newText)
    else:
        mc.textFieldButtonGrp('WrongObjsWin',e=1,tx='')
def readMaps():
    
    mapNodes=[ u'AU1_L_Mask', u'AU1_R_Mask',  u'AU2_L_Mask', u'AU2_R_Mask', u'AU4_L_Mask', u'AU4_R_Mask', u'AU6_L_Mask', u'AU6_R_Mask', u'AU9_L_Mask', u'AU9_R_Mask',u'AU10_L_Mask', u'AU10_R_Mask', u'AU12_L_Mask', u'AU12_R_Mask', u'AU14_L_Mask', u'AU14_R_Mask', u'AU15_L_Mask', u'AU15_R_Mask', u'AU17_D_Mask',u'AU20_L_Mask', u'AU20_R_Mask',  u'faceBase_N',u'faceA_N',u'faceB_N', u'faceC_N', u'faceE_N', u'faceBase_D',u'faceA_D',  u'faceB_D',  u'faceC_D', u'faceE_D',u'env_Hdr']
    mapName=['Mask_AU1_L.jpg','Mask_AU1_R.jpg','Mask_AU2_L.jpg','Mask_AU2_R.jpg','Mask_AU4_L.jpg','Mask_AU4_R.jpg','Mask_AU6_L.jpg','Mask_AU6_R.jpg','Mask_AU9_L.jpg','Mask_AU9_R.jpg','Mask_AU10_L.jpg','Mask_AU10_R.jpg','Mask_AU12_L.jpg','Mask_AU12_R.jpg','Mask_AU14_L.jpg','Mask_AU14_R.jpg','Mask_AU15_L.jpg','Mask_AU15_R.jpg','Mask_AU17_D.jpg','Mask_AU20_L.jpg','Mask_AU20_R.jpg','NormalBase.tif','NormalA.tif','NormalB.tif','NormalC.tif','NormalE.tif','DisplacementBase.exr','DisplacementA.exr','DisplacementB.exr','DisplacementC.exr','DisplacementE.exr','IBL.hdr']
    CtrlPlug=['Brow_L_001_CTRL.ty', 'Brow_R_001_CTRL.ty', 'Brow_L_002_CTRL.ty', 'Brow_R_002_CTRL.ty', 'Brow_L_001_CTRL.tx', 'Brow_R_001_CTRL.tx', 'UpperLid_L_001_CTRL.ty', 'UpperLid_R_001_CTRL.ty', 'EyeCorner_L_001_CTRL.tx', 'EyeCorner_R_001_CTRL.tx', 'LowerLid_L_001_CTRL.ty', 'LowerLid_R_001_CTRL.ty', 'Nosewing_L_001_CTRL.ty', 'Nosewing_R_001_CTRL.ty', 'Muzzle_L_001_CTRL.ty', 'Muzzle_R_001_CTRL.ty', 'UpperLip_L_001_CTRL.ty', 'UpperLip_R_001_CTRL.ty', 'Nosewing_L_001_CTRL.tx', 'Nosewing_R_001_CTRL.tx', 'MouthCorner_L_002_CTRL.tx', 'MouthCorner_R_002_CTRL.tx', 'LowerLip_L_001_CTRL.ty', 'LowerLip_R_001_CTRL.ty', 'MouthCorner_L_002_CTRL.ty', 'MouthCorner_R_002_CTRL.ty', 'MouthCorner_L_001_CTRL.tx', 'MouthCorner_R_001_CTRL.tx', 'MouthCorner_L_001_CTRL.ty', 'MouthCorner_R_001_CTRL.ty', 'Chin_L_001_CTRL.ty', 'Chin_R_001_CTRL.ty', 'UpperLip_C_001_CTRL.ty', 'LowerLip_C_001_CTRL.ty', 'MouthCorner_L_001_CTRL.tx', 'MouthCorner_R_001_CTRL.tx', 'Chin_L_002_CTRL.ty', 'Chin_R_002_CTRL.ty', 'UpperLip_C_001_CTRL.tz', 'LowerLip_C_001_CTRL.tz', 'UpperLip_C_001_CTRL.tz', 'LowerLip_C_001_CTRL.tz', 'Chin_C_001_CTRL.ty', 'Chin_C_001_CTRL.ty', 'Cheek_L_001_CTRL.tx', 'Cheek_R_001_CTRL.tx', 'Cheek_L_001_CTRL.tx', 'Cheek_R_001_CTRL.tx', 'UpperLid_L_001_CTRL.ty', 'UpperLid_R_001_CTRL.ty', 'Face_U_ctrl.tx', 'Face_SH_ctrl.tx', 'Face_E_ctrl.tx', 'Face_F_ctrl.tx', 'Face_M_ctrl.tx', 'Face_O_ctrl.tx', 'Chin_C_001_CTRL.ty', 'UpperLip_C_001_CTRL.ty', 'LowerLip_C_001_CTRL.ty', 'Mouth_C_001_CTRL.tx', 'Mouth_C_001_CTRL.tx', 'Mouth_C_001_CTRL.ty', 'Mouth_C_001_CTRL.ty', 'Mouth_C_001_CTRL.tz', 'Mouth_C_001_CTRL.tz']
    values=[1, 1, 1, 1, -1, -1, 0.5, 0.5, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -0.5, -0.5, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1]
    
    wrinkleAttr=["dx11Shader_ast.AU1_L","dx11Shader_ast.AU1_R","dx11Shader_ast.AU2_L","dx11Shader_ast.AU2_R","dx11Shader_ast.AU4_L","dx11Shader_ast.AU4_R","dx11Shader_ast.AU6_L","dx11Shader_ast.AU6_R","dx11Shader_ast.AU9_L","dx11Shader_ast.AU9_R","dx11Shader_ast.AU10_L","dx11Shader_ast.AU10_R","dx11Shader_ast.AU12_L","dx11Shader_ast.AU12_R","dx11Shader_ast.AU14_L","dx11Shader_ast.AU14_R","dx11Shader_ast.AU15_L","dx11Shader_ast.AU15_R","dx11Shader_ast.AU17_D","dx11Shader_ast.AU20_L","dx11Shader_ast.AU20_R"]
    wrinkleIndex=[0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 14, 15, 20, 21, 26, 27, 28, 29, 33, 36, 37]
    path=mc.textFieldButtonGrp('mapsPath',q=1,tx=1)
    for i in mapNodes:
        nodeId=mapNodes.index(i)
        mapType=i.split('_')[-1]
        if mapType=='Mask':
            map=path+'/maskMaps/'+mapName[nodeId]
        if mapType=='N':
            map=path+'/normalMaps/'+mapName[nodeId]
        if mapType=='D':
            map=path+'/displacementMaps/'+mapName[nodeId]
        if mapType=='Hdr':
            map=path+'/'+mapName[nodeId]
        mc.setAttr(i+'.fileTextureName',map,type='string')
    for driverId in wrinkleIndex:
        [drivenNode,drivenAttr]=wrinkleAttr[wrinkleIndex.index(driverId)].split('.')
        mc.setDrivenKeyframe(drivenNode,cd=CtrlPlug[driverId],at=drivenAttr,dv=0.0,v=0.0)
        mc.setDrivenKeyframe(drivenNode,cd=CtrlPlug[driverId],at=drivenAttr,dv=values[driverId],v=1)
def getMapsPath():
    path=mc.fileDialog2(fm=3,okc='Select')
    if path:
        mc.textFieldButtonGrp('mapsPath',e=1,tx=path[0])
def importFacialTmp():
    mc.file(path+"/scripts/fantabox/rigging/FacialRig/facial_ctrl.mb",i=1,type="mayaBinary",ignoreVersion=1,mergeNamespacesOnClash=0,rpr="facial_ctrl" ,options="v=0;",pr=1)
def importDX11Shader():
    mc.file(path+"/scripts/fantabox/rigging/FacialRig/dx11shaderGroup.mb",i=1,type="mayaBinary",ignoreVersion=1,mergeNamespacesOnClash=0,rpr="facial_ctrl" ,options="v=0;",pr=1)
def selectWrongObjCmd():
    WrongText=mc.textFieldButtonGrp('WrongObjsWin',q=1,tx=1)
    mc.select(WrongText.split(','),r=1)
def getSouceObjCmd():
    obj=mc.ls(sl=1)[0]
    mc.textFieldButtonGrp('getSouceObj',e=1,tx=obj)
def getcuthead():
    seledge=mc.ls(sl=True)
    basename=seledge[0].split('.')
    if len(basename)>1:
        if basename[1].find('e')>-1:
            basevtx=mc.polyEvaluate(basename[0],v=True)
            mc.DetachEdgeComponent()
            mc.select(basename[0])
            mc.ExtractFace()
            cuts=mc.ls(sl=True)
            mc.duplicate(cuts[0],n='cuthead',rr=True)
            mc.move(1,0,0,'cuthead')
            mc.select(cuts[0],cuts[1])
            mc.CombinePolygons()
            newbase=mc.ls(sl=True)
            mc.polyMergeVertex(newbase[0]+'.vtx[0:99999]',d=.00001,am=1,ch=1)
            mc.select(newbase)
            mc.DeleteHistory()
            if basevtx==mc.polyEvaluate(newbase,v=True):
                mm.eval('print "/////点数一致，切头成功"')
            else:
                mc.warning("点数不一致，切头失败！！！")
        else:
            mc.warning("请选择模型环线执行！！！")
    else:
        mc.warning("请选择模型环线执行！！！")
#shuai_autoFacialRig()