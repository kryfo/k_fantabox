#!/usr/bin/python
##coding:utf-8
#--author--:xusijian
#--date--:2017-08-25
import maya.cmds as cmds
def SJ_fixedShadermodToolUI():
    '''
    {'load':'maya_common','defaultOption':1,'CNname':'�޸�ģ�Ͳ��ʹ���'}
    '''
    if cmds.window('fixedshadermodwd',ex=True):
        cmds.deleteUI('fixedshadermodwd',wnd=True)
    cmds.window('fixedshadermodwd',t='fixedshadermod_Tool')
    cmds.columnLayout(adj=True,w=400)
    cmds.text(l='�޸�ģ�Ͳ��ʹ���', fn='fixedWidthFont',h=50,ann="" )
    cmds.flowLayout( columnSpacing=0)
    cmds.button(l='ѡ��ʧ����ģ��',c='from fantabox.modeling.SJ_faceShaderMod import *;fixedmisshader()',w=200,h=50,ann="")
    cmds.button(l='ѡ��û������arnold��ë���ڵ�',c='from fantabox.rendering import *;noAishaderhair()',w=200,h=50,ann="")
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.setParent( '..' )
    cmds.button(l='�޸����渳�����ģ��',c='from fantabox.modeling.SJ_faceShaderMod import *;fixedfaceshader()',h=50,ann="")
    cmds.button(l='�޸�Arnold��Ⱦϸ�ִ���3������',c='from fantabox.rendering import *;fixed_aiSubdiv()',h=50,ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_fixedShadermodToolUI()