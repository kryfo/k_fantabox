#coding=cp936
#coding=utf-8
import pymel.core as pm
import maya.mel as mel
def buttoncol ():
    pm.button(l='uvset重置工具',w=180,h=50,ann="",c=r'fb.mod.SJ_uvsetToolwdUI()')
    pm.button(l='多个物体传递uv工具',w=180,h=50,ann="",c=r'mel.eval("multiTransferUVWindow")')
    pm.button(l='uv材质传递工具（原ZZ01）',w=180,h=50,ann="",c=r'mel.eval("zzUvtransfer")')
def UVToolwdUI():
	if pm.window('uvToolwd',ex=True):
	    pm.deleteUI('uvToolwd',wnd=True)
	pm.window('uvToolwd',t='UVToolV1.0')
	pm.columnLayout(adj=True)
	pm.text(l='uv工具集V1.0',fn='fixedWidthFont',annotation="",w=250,h=50,ann="")
	buttoncol()
	pm.showWindow()