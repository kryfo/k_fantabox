#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:huwenbin
#--date--:2017-06-13
import maya.cmds as cmds
def check_invalid_displayLayer(checknum):
    u'''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查多余显示层'}
    '''
    if checknum in range(0,8):
        if checknum in [7]:
            all_layer=[a for a in cmds.ls(typ="displayLayer")]
            remove_layers=[a for a in cmds.ls(typ="displayLayer",rn=1) if 'defaultLayer' in a or 'jointLayer' in a]
            k_remove_layers=["defaultLayer","ori_sim","NoRender","TX"]
            remove_layers=list(set(remove_layers).union(set(k_remove_layers)))
            delete_layers=list(set(all_layer).difference(set(remove_layers)))
            return delete_layers
        else:
            all_layer=[a for a in cmds.ls(typ="displayLayer")]
            remove_layers=[a for a in cmds.ls(typ="displayLayer",rn=1) if 'defaultLayer' in a or 'jointLayer' in a]
            k_remove_layers=["defaultLayer","ori_sim","NoRender","TX","jointLayer"]
            remove_layers=list(set(remove_layers).union(set(k_remove_layers)))
            delete_layers=list(set(all_layer).difference(set(remove_layers)))
            return delete_layers
    else:
        all_layer=[a for a in cmds.ls(typ="displayLayer")]
        remove_layers=[a for a in cmds.ls(typ="displayLayer",rn=1) if 'defaultLayer' in a or 'jointLayer' in a]
        k_remove_layers=["defaultLayer","ori_sim","NoRender","TX","jointLayer"]
        remove_layers=list(set(remove_layers).union(set(k_remove_layers)))
        delete_layers=list(set(all_layer).difference(set(remove_layers)))
        for remove_layer in k_remove_layers:
            if cmds.objExists(remove_layer):
                if cmds.getAttr(remove_layer+".visibility") and remove_layer!="defaultLayer":
                    delete_layers.append(remove_layer+":its visibility set wrong!!")

        return delete_layers