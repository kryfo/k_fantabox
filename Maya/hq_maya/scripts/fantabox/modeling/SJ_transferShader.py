#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
def SJ_transferShaderwdUI():
	if cmds.window('transfercom',ex=True):
	    cmds.deleteUI('transfercom',wnd=True)
	cmds.window('transfercom',t='transfershaderTool_V2.0')
	cmds.columnLayout(adj=True)
	cmds.text(l="����ת�����߼�V2.0",fn='fixedWidthFont',h=50,w=30,ann="V2.0����˵�������ݹٷ������Ż�ת�������������˶�vray���ʵ�֧��")
	cmds.button(l='ͨ�ò���תArnold', c= "fb.com.pySource( 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/comtransAi.pyc')",h=50,ann="������'VRayMtl', 'lambert', 'blinn', 'phong', 'mia_material_x_passes', 'mia_material_x', 'dielectric_material'���ͽڵ�ת��Ϊarnold����")
	cmds.button(l='Arnoldת��ͨ����', c= "fb.com.pySource( 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/ArexCtoon.pyc')",h=50)
	cmds.showWindow()