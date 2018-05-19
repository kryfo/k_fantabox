#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:lingyc
#--date--:2017-06-09
import maya.cmds as cmds
def check_renderLayer():
    u'''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查无用渲染层'}
    '''
    allRenderLayer= set(cmds.ls(typ= 'renderLayer'))
    normalRendeLayer= [a for a in cmds.ls(typ='renderLayer',rn=1) if 'defaultRenderLayer' in a]
    normalRendeLayer.append('defaultRenderLayer')
    otherRenderLayer= list(allRenderLayer.difference(normalRendeLayer))
    return otherRenderLayer