#coding=cp936
#coding=utf-8
import maya.cmds as cmds
import pymel.core as pm
def checkIDbyobj_black(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0,0,0)
def checkIDbyobj_Red(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',1,0,0)
def checkIDbyobj_green(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0,1,0)
def checkIDbyobj_blue(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0,0,1)
def checkIDbyobj_yellow(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',1,1,0)
def checkIDbyobj_purple(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',1,0,1)
def checkIDbyobj_cycan(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0,1,1)

def checkIDbyobj_Reds(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',1,0.5,0.5)
def checkIDbyobj_greens(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0.5,1,0.5)
def checkIDbyobj_blues(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0.5,0.5,1)
def checkIDbyobj_yellows(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0.3,0.3,0)
def checkIDbyobj_purples(arg):
    selID = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(selID)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    for i in range(0,len(SG2WT2)):
        cmds.setAttr(SG2WT2[i]+'.hardwareColor',0.4,0.2,0.3)
def checkIDbyobj_break(arg):
    sel = cmds.ls(sl=True)
    obj2shapes = cmds.listRelatives(sel)
    shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
    shapes2SGnew = cmds.duplicate(shapes2SG,po=True)
    SG2AU = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
    SG2AW = cmds.listConnections(SG2AU,d=0,type='aiWriteColor')
    SG2AUnew = cmds.duplicate(SG2AU,po=True)
    for i in range(0,len(SG2AUnew)):
        cmds.connectAttr(SG2AW[0]+".outColor",SG2AUnew[0]+".color")
        cmds.connectAttr(SG2AUnew[0]+".outColor",shapes2SGnew[0]+".surfaceShader")
        cmds.defaultNavigation(source = SG2AUnew[0],destination = obj2shapes[0]+".instObjGroups[0]",connectToExisting=True)
def checkVer(arg):
	sel = cmds.ls(type = "aiUtility")
	selTarget = []
	selSource = []
	if len(sel)!= 0:
	    for i in range(0,len(sel)):
	        seladjust =cmds.listConnections(sel[i]+".color",d=0,type="aiWriteColor") 
	        if seladjust != None:
	            selTarget.append(sel[i])
	else:
		print "ģ��û�УɣĲ��ʣ���",
	for i in range(0,len(selTarget)):
	    AiWC = cmds.listConnections( selTarget[i]+".color", s=True )
	    for i in range(0,len(AiWC)):
	        selTSource = cmds.listConnections( AiWC[i]+".input", s=True )
	        selSource.append(selTSource[i])
	for t in range(0,len(selTarget)):
	    selTSColor = pm.getAttr(selSource[t]+".color")
	    if pm.listConnections(selTarget[t]+".hardwareColor",d=0)==[]:
		    pm.setAttr(selTarget[t]+".hardwareColor",selTSColor) 
		    
def SJ_hardwareDisplaySwitcherwdUI():
	if cmds.window('hardwareC',ex=True):
	    cmds.deleteUI('hardwareC',wnd=True)
	cmds.window('hardwareC',t='ģ����ɫ��ʾ��ɫ��_bySJ')
	cmds.columnLayout(adj=True)
	cmds.text(l="��ѡ��ģ�ͣ��ٵ����Ӧ��ɫ��ť����",h=50,bgc=[0.8,0.8,0.8])
	cmds.button(l='�۾�_��ɫ',c=checkIDbyobj_black,bgc=[0,0,0],h=50,w=10)
	cmds.button(l='����_��ɫ',c=checkIDbyobj_Red,bgc=[1,0,0],h=50,w=10)
	cmds.button(l='Ь��_��ɫ',c=checkIDbyobj_green,bgc=[0,1,0],h=50,w=10)
	cmds.button(l='�·�_��ɫ',c=checkIDbyobj_blue,bgc=[0,0,1],h=50,w=10)
	cmds.button(l='����_��ɫ',c=checkIDbyobj_yellow,bgc=[1,1,0],h=50,w=10)
	cmds.button(l='����_��ɫ',c=checkIDbyobj_purple,bgc=[1,0,1],h=50,w=10)
	cmds.button(l='����_��ɫ',c=checkIDbyobj_cycan,bgc=[0,1,1],h=50,w=10)
	cmds.button(l='����',c=checkIDbyobj_Reds,bgc=[1,0.5,0.5],h=50,w=10)
	cmds.button(l='����',c=checkIDbyobj_greens,bgc=[0.5,1,0.5],h=50,w=10)
	cmds.button(l='�۾�',c=checkIDbyobj_blues,bgc=[0.5,0.5,1],h=50,w=10)
	cmds.button(l='ñ��',c=checkIDbyobj_yellows,bgc=[0.3,0.3,0],h=50,w=10)
	cmds.button(l='���',c=checkIDbyobj_purples,bgc=[0.4,0.2,0.3],h=50,w=10)
	cmds.text(l="��ѡ��ģ�ͣ�����ͬ�������ģ�ͷ���",h=50,bgc=[0.8,0.8,0.8])
	cmds.button(l='����',c=checkIDbyobj_break,bgc=[0.5,0.5,0.5],h=50,w=10)
	cmds.text(l="===========================",h=30)
	cmds.button(l='��鴩���һ������',c=checkVer,h=50,bgc=[0.5,0.6,0.8])
	cmds.showWindow()

