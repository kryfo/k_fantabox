#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:libin
#--date--:2017-06-13
from maya.cmds import getPanel,modelEditor,modelPanel
def check_display_wireframe():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查提交文件的视窗是否为线框模式/边界框模式'}
    '''
    nowireframe =[]
    modelPanels_all = getPanel(type="modelPanel")
    cameradict = {u'Top View':"top",u'Side View':"side",u'Front View':"front",u'Persp View':"persp"}
    for currentPanel in modelPanels_all:
        displaytype = modelEditor(currentPanel,displayAppearance=1,q=1)
        zongshu = len(modelPanels_all)
        if displaytype=="wireframe" or displaytype=="boundingBox":
            pass
        else:
            camname =  cameradict.get(modelPanel(currentPanel,q=True, l=True ))
            if modelPanel(currentPanel,q=True, l=True ) in cameradict.keys():
                nowireframe.append(camname)
    return nowireframe
if __name__=='__main__':
    adj = check_display_wireframe()
    if adj ==[]:
        print "-------视图为线框显示-------\n",
    else:
        print "-------视图为非线框显示-------\n",
