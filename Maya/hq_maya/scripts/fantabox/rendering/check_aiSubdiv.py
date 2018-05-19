#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:lingyc,xusijian
#--date--:2017-08-25
import maya.cmds as cmds
def check_aiSubdiv():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查Arnold渲染细分大于3的物体'}
    '''
    all_polymesh= cmds.ls(typ= 'mesh')
    aiSubdiv_soBig= []
    for i in range(len(all_polymesh)):
        try:        
            aiSubdiv_type= cmds.getAttr(all_polymesh[i]+'.aiSubdivType')
            aiSubdiv_iterations= cmds.getAttr(all_polymesh[i]+'.aiSubdivIterations')
            if aiSubdiv_type != 0:
                if aiSubdiv_type==2 or aiSubdiv_iterations> 3:
                    aiSubdiv_soBig.append(all_polymesh[i])
        except:
            pass
    return aiSubdiv_soBig

def fixed_aiSubdiv():
    fixed_aiSubdivsels = check_aiSubdiv()
    for fixed_aiSubdivsel in fixed_aiSubdivsels:
        cmds.setAttr(fixed_aiSubdivsel+'.aiSubdivType',1)
        cmds.setAttr(fixed_aiSubdivsel+'.aiSubdivIterations',3)
    cmds.warning("已重置了"+str(len(fixed_aiSubdivsels))+"个错误细分模型！！")
if __name__ =="__main__":
    fixed_aiSubdiv()
