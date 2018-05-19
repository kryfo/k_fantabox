#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
def SJ_transferShaderwdUI():
	if cmds.window('transfercom',ex=True):
	    cmds.deleteUI('transfercom',wnd=True)
	cmds.window('transfercom',t='transfershaderTool_V2.0')
	cmds.columnLayout(adj=True)
	cmds.text(l="材质转换工具集V2.0",fn='fixedWidthFont',h=50,w=30,ann="V2.0更新说明：根据官方资料优化转换方法，增加了对vray材质的支持")
	cmds.button(l='通用材质转Arnold', c= "fb.com.pySource( 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/comtransAi.pyc')",h=50,ann="适用于'VRayMtl', 'lambert', 'blinn', 'phong', 'mia_material_x_passes', 'mia_material_x', 'dielectric_material'类型节点转换为arnold材质")
	cmds.button(l='Arnold转卡通材质', c= "fb.com.pySource( 'O:/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/ArexCtoon.pyc')",h=50)
	cmds.showWindow()