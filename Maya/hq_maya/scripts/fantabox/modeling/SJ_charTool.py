#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
def SJ_charToolwdUI():
	if cmds.window('charTool',ex=True):
	    cmds.deleteUI('charTool',wnd=True)
	cmds.window('charTool',t='CharToolV2.1')
	cmds.columnLayout(adj=True)
	cmds.text(l="角色工具集V2.1",fn='fixedWidthFont',h=50,w=30,ann="2.1更新说明：整合yeti工具和hair工具为毛发工具集")
	cmds.button(l='角色文件整理工具', c= "fb.mod.SJ_charcleanuptoolwdUI()",h=50)
	cmds.button(l='ArnoldID修改工具', c= "fb.mod.SJ_arnoldIDToolwdUI()",h=50)
	cmds.button(l='Arnold材质转换器', c= "fb.mod.SJ_transferShaderwdUI()",h=50)
	cmds.button(l='毛发工具集', c= "fb.mod.SJ_furToolwdUI()",h=50)
#	cmds.button(l='SJ实用小工具', c= "fb.com.pySource( 'O:/mocap/SJ_ToolBox/python_source_2015/sjlttool.pyc')",h=50)
	cmds.showWindow()
