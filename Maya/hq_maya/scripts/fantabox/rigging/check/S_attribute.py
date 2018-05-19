#!usr/bin/env python
#coding:utf-8
#--author-- : yujing
#--date-- : 2018.1.31
import maya.cmds as cmds
import maya.mel as mel
def Shapes_Lock():
    if  cmds.window("Curve Lock Attribute",q=1,ex=1):
        cmds.deleteUI("Curve Lock Attribute")
    window = cmds.window("Curve Lock Attribute" ,title="Curve Lock Attribute", iconName='Short Name', widthHeight=(280, 180) )
    cmds.columnLayout( adjustableColumn=True )
    texts = cmds.text(l = '' , h = 10)
    texts = cmds.text(l = '' , h = 5)
    texts = cmds.text(l = '���ڰ󶨽�����ͼ�鹤��һ��ʹ�õ������ڵ㹤��' , h = 10)
    texts = cmds.text(l = '' , h = 18)
    texts = cmds.text(l = '��������shape�ڵ�' , h = 10)
    cmds.button( label='Shape Lock Attribute',h=40,c = 'fb.rigging.check.S_attribute.lockAllCurveShapes()',bgc = (0.4,0,0) )
    texts = cmds.text(l = '' , h = 10)
    texts = cmds.text(l = '' , h = 5)
    texts = cmds.text(l = '��������shape�ڵ�' , h = 10)
    cmds.button( label='Shape Unlock Attribute',h=40,c = 'fb.rigging.check.S_attribute.UnlockAllCurveShapes()',bgc = (0.4,0.7,0) )
    cmds.setParent( '..' )
    cmds.showWindow( window )
def lockAllCurveShapes():
	curveShapes=cmds.ls(type='nurbsCurve')
	for i in curveShapes:
		cmds.setAttr(i+'.rcurve',lock=1)
		cmds.setAttr(i+'.cwdth',lock=1)
		cmds.setAttr(i+'.srate',lock=1)
		cmds.setAttr(i+'.ai_curve_shaderr',lock=1)
		cmds.setAttr(i+'.ai_curve_shaderg',lock=1)
		cmds.setAttr(i+'.ai_curve_shaderb',lock=1)
	cmds.warning( "��������������ִ����ϡ���������������")
def UnlockAllCurveShapes():
	curveShapes=cmds.ls(type='nurbsCurve')
	for i in curveShapes:
		cmds.setAttr(i+'.rcurve',lock=0)
		cmds.setAttr(i+'.cwdth',lock=0)
		cmds.setAttr(i+'.srate',lock=0)
		cmds.setAttr(i+'.ai_curve_shaderr',lock=0)
		cmds.setAttr(i+'.ai_curve_shaderg',lock=0)
	cmds.warning( "��������������ִ����ϡ���������������")
#def S_attribute():
if __name__=='__main__':    
    Shapes_Lock()