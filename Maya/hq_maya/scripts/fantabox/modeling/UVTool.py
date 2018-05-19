#coding=cp936
#coding=utf-8
import pymel.core as pm
import maya.mel as mel
def buttoncol ():
    pm.button(l='uvset���ù���',w=180,h=50,ann="",c=r'fb.mod.SJ_uvsetToolwdUI()')
    pm.button(l='������崫��uv����',w=180,h=50,ann="",c=r'mel.eval("multiTransferUVWindow")')
    pm.button(l='uv���ʴ��ݹ��ߣ�ԭZZ01��',w=180,h=50,ann="",c=r'mel.eval("zzUvtransfer")')
def UVToolwdUI():
	if pm.window('uvToolwd',ex=True):
	    pm.deleteUI('uvToolwd',wnd=True)
	pm.window('uvToolwd',t='UVToolV1.0')
	pm.columnLayout(adj=True)
	pm.text(l='uv���߼�V1.0',fn='fixedWidthFont',annotation="",w=250,h=50,ann="")
	buttoncol()
	pm.showWindow()