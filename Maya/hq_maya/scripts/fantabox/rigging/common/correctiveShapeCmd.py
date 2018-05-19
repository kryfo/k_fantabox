#!usr/bin/env python
#coding:utf-8
"""
@Amend Time: 2017.4.25

@author: wangzhi
"""
import maya.cmds as cmds
import sys
def correctiveShapeCmd():
    
    
    query=cmds.pluginInfo( 'shapeCorrect2015x64.mll', query=True ,loaded=True)
    if query == 0:
    	cmds.loadPlugin('shapeCorrect2015x64.mll')
    import shapeCorrect;reload(shapeCorrect)
    shapeCorrect.cort.correctiveShapeCmd()