#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-08-23
import maya.cmds as cmds
from fantabox.common.SJ_cleanLayerTool import *
from fantabox.rendering.check_renderLayer import *
from fantabox.animation.check_invalid_animLayer import *
from fantabox.common.check_invalid_displayLayer import *
def cleanLayerTool_layerdel(layers):
    if layers!=[]:
        for layer in layers:
            pirnt layer
            try:
                cmds.delete(layer)
            except:
                cmds.warning(layer+u"该层是否是参考或只读层，无法删除！！")   
        print  u"已完成删除多余层节点任务！！",
    else:
        print u"无多余层节点！！",

def cleanLayerTool_display(anifxcb_value=""):
    if anifxcb_value=="com":
        cleanLayerTool_layerdel(check_invalid_displayLayer(2))
    else:
        defaultlayers = check_invalid_displayLayer(8)
        if defaultlayers!=[]:
            for defaultlayer in defaultlayers:
                layername =  defaultlayer.split(":")[0]
                if defaultlayer.split(":")[-1] == 'its visibility set wrong!!':
                    if cmds.objExists(layername):
                        cmds.setAttr(layername+".visibility",0)
                else:
                    try:
                        cmds.delete(layername)
                    except:
                        cmds.warning(layername+u"该层是否是参考或只读层，无法删除！！")
            print u"已完成删除多余显示层任务！！",
        else:
            print u"无多余层节点！！",
            
def SJ_cleanLayerTool():
    u'''
    {'load':'maya_common','defaultOption':1,'CNname':'清理无用层'}
    '''
    if cmds.window('cleanLayerToolwd',ex=True):
        cmds.deleteUI('cleanLayerToolwd',wnd=True)
    cmds.window('cleanLayerToolwd',t='cleanLayer_Tool')
    cmds.columnLayout(adj=True,w=400)
    cmds.text(l=u'清理无用层工具', fn='fixedWidthFont',h=50,ann="" )
    cmds.flowLayout( columnSpacing=0)
    cmds.button(l=u'清理（通用）无用显示层',c=u'from fantabox.common.SJ_cleanLayerTool import *;cleanLayerTool_display("com")',w=200,h=50,ann="")
    cmds.button(l=u'清理(动画，特效)无用显示层',c=u'from fantabox.common.SJ_cleanLayerTool import *;cleanLayerTool_display()',w=200,h=50,ann="")
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.setParent( '..' )
    cmds.button(l=u'清理无用渲染层',c=u'cleanLayerTool_layerdel(check_renderLayer())',h=50,ann="")
    cmds.button(l=u'清理无用动画层',c=u'cleanLayerTool_layerdel(check_invalid_animLayer())',h=50,ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_cleanLayerTool()