#!usr/bin/env python
#coding:utf-8
#--author-- : yujing
#--date-- : 2018.2.1
import maya.cmds as cmds
import maya.mel as mel
def lockCurveShapeNode():
	curveAllShapes = cmds.ls(type='nurbsCurve')
	for shapes in curveAllShapes:
		if not cmds.getAttr(shapes+'.rcurve',l = 1) or not cmds.getAttr(shapes+'.cwdth',l = 1) or not cmds.getAttr(shapes+'.srate',l = 1) or not cmds.getAttr(shapes+'.ai_curve_shaderr',l = 1) or not cmds.getAttr(shapes+'.ai_curve_shaderg',l = 1) or not cmds.getAttr(shapes+'.ai_curve_shaderb',l = 1):
			cmds.warning(u'！！！！！！！！！！！！ShapeNode:%s 短嗤迄協！！！！！！！！！！'%shapes)
