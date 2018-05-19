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
		print "模型没有ＩＤ材质！！",
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
	cmds.window('hardwareC',t='模型颜色显示着色器_bySJ')
	cmds.columnLayout(adj=True)
	cmds.text(l="请选择模型，再点击相应颜色按钮生成",h=50,bgc=[0.8,0.8,0.8])
	cmds.button(l='眼睛_黑色',c=checkIDbyobj_black,bgc=[0,0,0],h=50,w=10)
	cmds.button(l='身体_红色',c=checkIDbyobj_Red,bgc=[1,0,0],h=50,w=10)
	cmds.button(l='鞋子_绿色',c=checkIDbyobj_green,bgc=[0,1,0],h=50,w=10)
	cmds.button(l='衣服_蓝色',c=checkIDbyobj_blue,bgc=[0,0,1],h=50,w=10)
	cmds.button(l='裤子_黄色',c=checkIDbyobj_yellow,bgc=[1,1,0],h=50,w=10)
	cmds.button(l='腰带_紫色',c=checkIDbyobj_purple,bgc=[1,0,1],h=50,w=10)
	cmds.button(l='配饰_青色',c=checkIDbyobj_cycan,bgc=[0,1,1],h=50,w=10)
	cmds.button(l='背包',c=checkIDbyobj_Reds,bgc=[1,0.5,0.5],h=50,w=10)
	cmds.button(l='内衣',c=checkIDbyobj_greens,bgc=[0.5,1,0.5],h=50,w=10)
	cmds.button(l='眼镜',c=checkIDbyobj_blues,bgc=[0.5,0.5,1],h=50,w=10)
	cmds.button(l='帽子',c=checkIDbyobj_yellows,bgc=[0.3,0.3,0],h=50,w=10)
	cmds.button(l='相机',c=checkIDbyobj_purples,bgc=[0.4,0.2,0.3],h=50,w=10)
	cmds.text(l="请选择模型，将相同材质球的模型分离",h=50,bgc=[0.8,0.8,0.8])
	cmds.button(l='分离',c=checkIDbyobj_break,bgc=[0.5,0.5,0.5],h=50,w=10)
	cmds.text(l="===========================",h=30)
	cmds.button(l='检查穿插版一键生成',c=checkVer,h=50,bgc=[0.5,0.6,0.8])
	cmds.showWindow()

