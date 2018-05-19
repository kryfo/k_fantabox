#!/usr/bin/python
##coding:utf-8
#--author--:xusijian
#--date--:2017-08-25
import maya.cmds as cmds
def SJ_fixedShadermodToolUI():
    '''
    {'load':'maya_common','defaultOption':1,'CNname':'修复模型材质工具'}
    '''
    if cmds.window('fixedshadermodwd',ex=True):
        cmds.deleteUI('fixedshadermodwd',wnd=True)
    cmds.window('fixedshadermodwd',t='fixedshadermod_Tool')
    cmds.columnLayout(adj=True,w=400)
    cmds.text(l='修复模型材质工具', fn='fixedWidthFont',h=50,ann="" )
    cmds.flowLayout( columnSpacing=0)
    cmds.button(l='选择丢失材质模型',c='from fantabox.modeling.SJ_faceShaderMod import *;fixedmisshader()',w=200,h=50,ann="")
    cmds.button(l='选择没有连接arnold的毛发节点',c='from fantabox.rendering import *;noAishaderhair()',w=200,h=50,ann="")
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.setParent( '..' )
    cmds.button(l='修复按面赋予材质模型',c='from fantabox.modeling.SJ_faceShaderMod import *;fixedfaceshader()',h=50,ann="")
    cmds.button(l='修复Arnold渲染细分大于3的物体',c='from fantabox.rendering import *;fixed_aiSubdiv()',h=50,ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_fixedShadermodToolUI()