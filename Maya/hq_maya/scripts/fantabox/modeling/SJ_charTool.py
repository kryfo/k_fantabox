#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
def SJ_charToolwdUI():
	if cmds.window('charTool',ex=True):
	    cmds.deleteUI('charTool',wnd=True)
	cmds.window('charTool',t='CharToolV2.1')
	cmds.columnLayout(adj=True)
	cmds.text(l="��ɫ���߼�V2.1",fn='fixedWidthFont',h=50,w=30,ann="2.1����˵��������yeti���ߺ�hair����Ϊë�����߼�")
	cmds.button(l='��ɫ�ļ�������', c= "fb.mod.SJ_charcleanuptoolwdUI()",h=50)
	cmds.button(l='ArnoldID�޸Ĺ���', c= "fb.mod.SJ_arnoldIDToolwdUI()",h=50)
	cmds.button(l='Arnold����ת����', c= "fb.mod.SJ_transferShaderwdUI()",h=50)
	cmds.button(l='ë�����߼�', c= "fb.mod.SJ_furToolwdUI()",h=50)
#	cmds.button(l='SJʵ��С����', c= "fb.com.pySource( 'O:/mocap/SJ_ToolBox/python_source_2015/sjlttool.pyc')",h=50)
	cmds.showWindow()
