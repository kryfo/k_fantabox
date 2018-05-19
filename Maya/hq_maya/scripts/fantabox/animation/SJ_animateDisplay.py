#coding=cp936
#coding=utf-8
import maya.cmds as cmds

def AnDisplayon(arg):
    allmesh = cmds.ls(type="mesh")
    allmeshape = cmds.pickWalk(allmesh,d="down")
    for i in range(0,len(allmeshape)):
        cmds.setAttr(allmeshape[i]+".overrideEnabled",1)
        cmds.setAttr(allmeshape[i]+".overrideDisplayType",1)
def objDs(arg):
    sel = cmds.ls(sl=1)
    namps= sel[0].split(":")
    namp = namps[0]
    selshape= cmds.ls(namp+":*",type="mesh")
    for i in range(0,len(selshape)):
        selOE = cmds.getAttr(selshape[i]+".overrideEnabled")
        if selOE ==False:
            cmds.setAttr(selshape[i]+".overrideEnabled",1)
            cmds.setAttr(selshape[i]+".overrideDisplayType",1)
        else:
            cmds.setAttr(selshape[i]+".overrideEnabled",0)
            cmds.setAttr(selshape[i]+".overrideDisplayType",0)
def AnDisplayoff(arg):
    allmesh = cmds.ls(type="mesh")
    allmeshape = cmds.pickWalk(allmesh,d="down")
    for i in range(0,len(allmeshape)):
        cmds.setAttr(allmeshape[i]+".overrideEnabled",0)
        cmds.setAttr(allmeshape[i]+".overrideDisplayType",0)

def SJ_animateDisplaywdUI():
	if cmds.window('AnDisplay',ex=True):
	    cmds.deleteUI('AnDisplay',wnd=True)
	cmds.window('AnDisplay',t='AnDisplayV1.0')
	cmds.columnLayout(adj=True)
	cmds.text(l="���Զ���",h=50)
	cmds.button(l='�����߿�ģʽ', c=AnDisplayon,h=50,ann="�������ڵ�����ģ���л����߿���ʾ")
	cmds.button(l='��ʵ�л�', c=objDs,h=50,ann="ѡ����Ҫ�л��߿�ģʽ��ʵ��ģʽ��ģ�Ϳ�����")
	cmds.button(l='�ر��߿�ģʽ', c=AnDisplayoff,h=50,ann="�������ڵ�����ģ�ͻָ���ʵ����ʾ")
	cmds.showWindow()


