#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-08-22
import maya.cmds as cmds
import fantabox.common
from fantabox.modeling import k002_check_novertPolo
from fantabox.rendering import k015_check_displink
def cleanUp_mod(cleanscrpts,chname):
    if cleanscrpts!=[]:
        try:
            cmds.delete(cleanscrpts)
            print chname+u"清理完毕!",
        except:
            cmds.warning(chname+u'清理失败！！')
    
def cleanUp_main():
    unknowncb_value=cmds.checkBox("unknowncb" ,q=True,v=True)
    wkheadcb_value=cmds.checkBox("wkheadcb" ,q=True,v=True)
    unrefcb_value=cmds.checkBox("unrefcb" ,q=True,v=True)
    oigcb_value=cmds.checkBox("oigcb" ,q=True,v=True)
    tsmcb_value=cmds.checkBox("tsmcb" ,q=True,v=True)
    srefnodecb_value=cmds.checkBox("srefnodecb" ,q=True,v=True)
    clnoppcb_value=cmds.checkBox("clnoppcb" ,q=True,v=True)
    clbaddiscb_value=cmds.checkBox("clbaddiscb" ,q=True,v=True)
    clbadmatcb_value=cmds.checkBox("clbadmatcb" ,q=True,v=True)
    if tsmcb_value==1:
        fantabox.common.cleanUp_mod(fantabox.common.SJ_TSM_cleanup.TSM_menuCleanup(),u"TSM残留script节点")
    if oigcb_value==1:
        fantabox.common.cleanUp_mod(fantabox.common.k016_check_uuoig(),u"多余Oig节点")
    if unrefcb_value==1:
        fantabox.common.cleanUp_mod(fantabox.common.k007_check_UNKNOWNREF(),u"UNKNOWNREF节点")
    if wkheadcb_value==1:
        fantabox.common.cleanUp_mod(fantabox.common.k005_check_wkHeadsUp(),u"wkHeadsUp节点")
    if srefnodecb_value==1:
        fantabox.common.cleanUp_mod(fantabox.common.k009_check_sharedRef(),u"shareReferenceNode节点")
    if unknowncb_value==1:
        fantabox.common.cleanUp_mod(fantabox.common.k008_check_unknown(),u"未知节点")
    if clnoppcb_value==1:
        fantabox.common.cleanUp_mod(k002_check_novertPolo(),u"无点的Plolygons")
    if clbaddiscb_value==1:
        fantabox.common.cleanUp_mod(k015_check_displink(),u"连接断了的置换节点")
    if clbadmatcb_value==1:
        from maya.mel import eval as meleval
        meleval('hyperShadePanelMenuCommand("hyperShadePanel", "deleteUnusedNodes");') 


def SJ_cleanUpTool():
    u'''
    {'load':'maya_common','defaultOption':1,'CNname':'清理无用节点'}
    '''
    if cmds.window('cleanupToolwd',ex=True):
        cmds.deleteUI('cleanupToolwd',wnd=True)
    cmds.window('cleanupToolwd',t='cleanUp_Tool')
    cmds.columnLayout(adj=True,w=372)
    cmds.text(l=u'清理无用节点工具', fn='fixedWidthFont',h=50,ann="" )
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("unknowncb" ,label=u'未知节点',v=1,ann="",w=100,h=30)
    cmds.checkBox("wkheadcb" ,label=u'wkHeadsUp节点',v=1,ann="",w=120,h=30)
    cmds.checkBox("unrefcb" ,label=u'UNKNOWNREF节点',v=1,ann="",w=120,h=30)
    
    cmds.setParent( '..' ) 
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("oigcb" ,label=u'多余Oig节点',v=1,ann="",w=100,h=30)
    cmds.checkBox("tsmcb" ,label=u'TSM残留script节点',v=1,ann="",w=120,h=30)
    cmds.checkBox("srefnodecb" ,label=u'shareReferenceNode节点',v=1,ann="",w=150,h=30)
    
    cmds.setParent( '..' ) 
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("clbadmatcb" ,label=u'无用渲染节点',v=1,ann="",w=100,h=30)
    cmds.checkBox("clnoppcb" ,label=u'无点的Plolygons',v=1,ann="",w=120,h=30)
    cmds.checkBox("clbaddiscb" ,label=u'连接断了的置换节点',v=1,ann="",w=150,h=30)
    
    cmds.setParent( '..' )
    cmds.button(l=u'清理多余节点',c=u'fb.com.cleanUp_main()',h=50,ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_cleanUpTool()