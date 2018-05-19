#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-10-26
import maya.cmds as cmds
def check_keyobj(checknum):
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查是否有Key帧物体'}
    '''
    if checknum in range(0,8):
        drsels = [cmds.listRelatives(a,f=1,p=1)[0] for a in cmds.ls(type=["nurbsCurve","camera"])]
        wrongobj =[]
        for drsel in drsels:
            animcvs = cmds.listConnections(drsel,d=0,type="animCurve")
            if animcvs!=None:
                for animcv in animcvs:
                    if cmds.listConnections(animcv,d=0)==None:
                        wrongobj.append(animcv)
        wrongobj =list(set(wrongobj))
        return wrongobj
    else:
        return []
if __name__=="__main__":
    check_keyobj()