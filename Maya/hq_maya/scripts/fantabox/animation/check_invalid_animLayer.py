#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-08-23
import maya.cmds as cmds
def check_invalid_animLayer():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'�����ද����'}
    '''
    delete_animlayer=cmds.ls(typ="animLayer")
    return delete_animlayer