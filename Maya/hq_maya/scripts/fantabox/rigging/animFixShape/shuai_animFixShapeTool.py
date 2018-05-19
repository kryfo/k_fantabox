#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
def shuai_animFixShapeTool():
	if mc.window('animFixWin',ex=1):
		mc.deleteUI('animFixWin')
	mc.window('animFixWin',t='�������͹���',h=300,w=302,sizeable=0)
	mc.columnLayout(rowSpacing=5)
	mc.text('���裺',al='left',font='fixedWidthFont')
	mc.text('     1������һ��ģ�ͳ���',font='fixedWidthFont',al='left')
	mc.text('     2���������Ƴ�����ģ�͵���״',font='fixedWidthFont',al='left')
	mc.text('     3����ѡ������õĸ���ģ�ͣ��ټ�ѡԭʼģ��',font='fixedWidthFont',al='left')
	mc.text('     4��������������������һ���������֣�Ȼ���\n        ����������������ϵͳ��',font='fixedWidthFont',al='left')
	mc.separator()
	mc.text('helpText',l='����һ���������ƣ���ס��Ҫ������',ww=1,h=40,w=300,font='fixedWidthFont')
	mc.textField('attrNameField',h=20,w=300)
	mc.button('animFixButton',l='������������ϵͳ',h=40,w=300,c='fb.rig.animFixShape.animFixButtonCmd()')
	mc.button('deleteAllTargetsButton',l='ɾ������Ŀ����',h=40,w=300,c='fb.rig.animFixShape.deleteAllTargetsCmd()')
	mc.button('bakeAndDeleteCtrlButton',l='�決�����ɾ������ϵͳ',h=40,w=300,c='fb.rig.animFixShape.bakeAndDeleteCtrlCmd()')
	mc.setParent('..')
	mc.showWindow('animFixWin')
def animFixButtonCmd():
	fixShape=mc.textField('attrNameField',q=1,tx=1)
	animFixShape(fixShape)
def animFixShape(fixShape):
	objs=mc.ls(sl=1)
	numVtx=mc.polyEvaluate(objs[1],v=1)
	skinMeshShapes=mc.listRelatives(objs[1],s=1,pa=1)
	skinMeshShapes1=mc.listRelatives(objs[1],s=1,ni=1,pa=1)
	fixMeshShape=mc.listRelatives(objs[0],s=1,ni=1,pa=1)[0]
	inputs=mc.listHistory(objs[1])
	for i in skinMeshShapes:
		if not i in skinMeshShapes1:
			intermediateShape=i
			break
	BSNode=None
	for n in inputs:
		if 'animFixBS' in n and mc.nodeType(n)=='blendShape':
			BSNode=n
	if not BSNode:
	    BSNode=mc.blendShape(objs[1],parallel=1,n='animFixBS')[0]
	if not mc.objExists('animFixCtrl'):
		createCtrl()
		
	mc.addAttr('animFixCtrl',ln=fixShape,at='double',min=0,max=1,dv=0,k=1)
	weightAttrs=mc.listAttr(BSNode+'.weight',m=1)
	weightListNum=0
	if weightAttrs:
	    weightListNum=len(weightAttrs)
	beforeFixMesh=mc.duplicate(objs[1],n='beforeFixMesh')[0]
	buildBSMesh=mc.duplicate(objs[1],n='buildBlendShapeMesh')[0]
	mc.hide(buildBSMesh)
	buildBSMeshShapes=mc.listRelatives(buildBSMesh,s=1,pa=1)
	buildBSMeshShapes1=mc.listRelatives(buildBSMesh,s=1,ni=1,pa=1)
	for i in buildBSMeshShapes:
		if not i in buildBSMeshShapes1:
			buildBSMeshShape=i
			break
	mc.setAttr(buildBSMeshShape+'.intermediateObject',0)
	mc.delete(buildBSMeshShapes1)
	
	buildBSNode=mc.blendShape(beforeFixMesh,objs[0],buildBSMesh,foc=1,w=[(0,-1),(1,1)],n='buildFixBs')[0]
	
	mc.blendShape(BSNode,e=1,t=[objs[1],weightListNum,buildBSMesh,1])
	
	BSTargets=mc.listAttr(BSNode+'.weight',m=1)
	mc.connectAttr('animFixCtrl.'+fixShape,BSNode+'.'+BSTargets[-1])
	
	'''for i in range(0,numVtx):
		ipos=mc.xform(intermediateShape+'.vtx[%d]'%i,q=1,os=1,t=1)
		tPos=mc.xform(objs[0]+'.vtx[%d]'%i,q=1,os=1,t=1)
		bPos=mc.xform(objs[1]+'.vtx[%d]'%i,q=1,os=1,t=1)
		mc.xform(objs[0]+'.vtx[%d]'%i,os=1,t=[(ipos[0]+tPos[0]-bPos[0]),(ipos[1]+tPos[1]-bPos[1]),(ipos[2]+tPos[2]-bPos[2])])'''
	mc.delete(beforeFixMesh)
	#mc.deleteUI('animFixWin')
	mc.setAttr('animFixCtrl.'+fixShape,1)
	if not mc.objExists('targetShapesGrp'):
	    targetGrp=mc.group(em=1,n='targetShapesGrp')
	    mc.parent(targetGrp,'animFixGrp')
	shapeTmpGrp=mc.group(buildBSMesh,objs[0],n=fixShape+'_TmpGrp')
	mc.parent(shapeTmpGrp,'targetShapesGrp')
def createCtrl():
	animFixCtrl=mc.textCurves(ch=0,o=1,f='Times New Roman|w400|h-1',t='AnimFixCtrl',n='Ctrl_AnimFix')
	curveShapes=mc.listRelatives(animFixCtrl,allDescendents=1,type='nurbsCurve')
	children=mc.listRelatives(animFixCtrl,children=1)
	makeCurve=mc.listConnections(children[0],s=1)
	mc.delete(makeCurve)
	mc.makeIdentity(animFixCtrl,apply=1)
	for i in curveShapes:
		mc.parent(i,animFixCtrl,s=1,add=1)
	mc.delete(children)
	animFixCtrl=mc.rename(animFixCtrl,'animFixCtrl')
	mc.setAttr(animFixCtrl+".overrideEnabled",1)
	mc.setAttr(animFixCtrl+".overrideColor",17)
	mc.setAttr("animFixCtrl.tx",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.ty",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.tz",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.rx",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.ry",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.rz",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.sx",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.sy",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.sz",keyable=0,channelBox=1)
	mc.setAttr("animFixCtrl.v",keyable=0,channelBox=1)
	activeCam=mc.lookThru(q=1)
	ctrlGrp=mc.group(animFixCtrl,n='animFixCtrlGRP')
	mainGrp=mc.group(em=1,n='animFixGrp')
	mc.parent(ctrlGrp,activeCam)
	mc.xform(ctrlGrp,a=1,os=1,t=[0.3,0.7,-5],ro=[0,0,0])
	mc.parent(ctrlGrp,mainGrp)
	mc.parentConstraint(activeCam,ctrlGrp,mo=1)
	mc.select(animFixCtrl,r=1)
def deleteAllTargetsCmd():
    if not mc.objExists('targetShapesGrp'):
        mc.warning('û�п�ɾ����Ŀ���壡��')
    else:
        mc.delete('targetShapesGrp')
        mc.warning('����Ŀ�����Ѿ�ȫ��ɾ��')
def bakeAndDeleteCtrlCmd():
    bakeStart=mc.playbackOptions(q=1,min=1)
    bakeEnd=mc.playbackOptions(q=1,max=1)
    mc.bakeResults((mc.ls('animFixBS*',type='blendShape')),simulation=True,t=(bakeStart,bakeEnd),sampleBy=1,disableImplicitControl=True,preserveOutsideKeys=True,sparseAnimCurveBake=False,removeBakedAttributeFromLayer=False,removeBakedAnimFromLayer=False,bakeOnOverrideLayer=False,minimizeRotation=True,controlPoints=False,shape=True)
    if mc.objExists('animFixCtrlGRP'):
        mc.delete('animFixCtrlGRP')
        mc.warning('����ϵͳ��animFixCtrl���Ѿ�ɾ������')
    else:
        mc.warning('δ����Ҫɾ���ġ�animFixCtrlGRP���飡��')