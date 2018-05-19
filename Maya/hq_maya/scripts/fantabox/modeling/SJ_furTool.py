#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
def SJ_furToolwdUI():
    if cmds.window('FurToolwd',ex=True):
        cmds.deleteUI('FurToolwd',wnd=True)
    cmds.window('FurToolwd',t='FurToolV1.0(bySJ)')
    cmds.columnLayout(adj=True)
    cmds.text(l='FurToolV1.0',fn='fixedWidthFont',h=50)
    cmds.button(l='YetiTool', c= "fb.com.pySource( 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/YetiTool.pyc')",h=50)
    cmds.button(l='HairTool', c= "fb.com.pySource( 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/HairTool.pyc')",h=50)
    cmds.showWindow()
    

