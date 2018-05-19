#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
class excl():
    def exist(self,selis,attr):
        if  pm.objExists(selis+attr)==True:
            return True
        else:
            return False     

def yetidisplays(arg):
    vailctrlshape =["MainShape","move_ctrlShape"]
    vailctrl = ["Main","move_ctrl"]
    cballsw= pm.checkBox("allsw" ,q=True,v=True)
    #cballsw= 1
    cball= pm.checkBox("all" ,q=True,v=True)
    #cball= 0
    if cball==1:
        cballsw=1
    if cball ==1 and cballsw==1:
        cvsel = pm.ls(type="nurbsCurve")
        cvseled = [c for c in cvsel if c.split(":")[-1] in vailctrlshape]
        cved = pm.pickWalk(cvseled,d="up")
        for i in range(len(cved)):
            if "showMod" in pm.listAttr(cved[i]):
                disadj = pm.getAttr(cved[i]+".showMod")
                if disadj==1:
                    if excl().exist(cved[i],".hair")==True:
                        pm.setAttr(cved[i]+".hair",1)
                    elif excl().exist(cved[i],".yeti"):
                        pm.setAttr(cved[i]+".yeti",1)
                    elif excl().exist(cved[i],".hairYeti"):
                        pm.setAttr(cved[i]+".hairYeti",1)
                    print "已全部显示毛发！！",
    #    print "强制所有毛发显示 \n最终提交渲染模式"
    elif cball ==0 and cballsw ==0:
        sel = pm.ls(sl=1)
        for s in range(len(sel)):
            if sel[s].split(":")[-1]!=[]:
                if sel[s].split(":")[-1] in vailctrl:
                    disadj = pm.getAttr(sel[s]+".showMod")
                    if disadj ==1:
                        if excl().exist(sel[s],".hair")==True:
                            if pm.getAttr(sel[s]+".hair") ==0:
                                pm.setAttr(sel[s]+".hair",1)
                            else:
                                pm.setAttr(sel[s]+".hair",0)
                        elif excl().exist(sel[s],".yeti"):
                            if pm.getAttr(sel[s]+".yeti") ==0:
                                pm.setAttr(sel[s]+".yeti",1)
                            else:
                                pm.setAttr(sel[s]+".yeti",0)
                        elif excl().exist(sel[s],".hairYeti"):
                            if pm.getAttr(sel[s]+".hairYeti") ==0:
                                pm.setAttr(sel[s]+".hairYeti",1)
                            else:
                                pm.setAttr(sel[s]+".hairYeti",0)
                        print "已切换选中毛发的显示属性！！",
    elif cballsw==1 and cball==0:
        cvsel = pm.ls(type="nurbsCurve")
        cvseled = [c for c in cvsel if c.split(":")[-1] in vailctrlshape]
        cved = pm.pickWalk(cvseled,d="up")
        for i in range(len(cved)):
            if "showMod" in pm.listAttr(cved[i]):
                disadj = pm.getAttr(cved[i]+".showMod")
                if disadj==1:
                    if excl().exist(cved[i],".hair")==True:
                        if pm.getAttr(cved[i]+".hair") ==0:
                            pm.setAttr(cved[i]+".hair",1)
                        else:
                            pm.setAttr(cved[i]+".hair",0)
                    elif excl().exist(cved[i],".yeti"):
                        if pm.getAttr(cved[i]+".yeti") ==0:
                            pm.setAttr(cved[i]+".yeti",1)
                        else:
                            pm.setAttr(cved[i]+".yeti",0)
                    elif excl().exist(cved[i],".hairYeti"):
                        if pm.getAttr(cved[i]+".hairYeti") ==0:
                            pm.setAttr(cved[i]+".hairYeti",1)
                        else:
                            pm.setAttr(cved[i]+".hairYeti",0)
                    print "已切换全部毛发属性的显示属性！！",
def SJ_furDisplaySwitchwdUI():
	if pm.window('furdisplay',ex=True):
	    pm.deleteUI('furdisplay',wnd=True)
	pm.window('furdisplay',t='furDisplayToolV2.1')
	pm.columnLayout(adj=True)
	
	pm.text(l='毛发显隐V2.1',fn='fixedWidthFont',h=50,annotation="更新说明V2.1：增加hair和yeti混合情况的显隐切换",w=80)
	pm.flowLayout( columnSpacing=0)
	pm.checkBox("allsw" ,label='切换所有yeti毛发显隐',ann="",h=50,w=140)
	pm.checkBox("all" ,label='强制所有毛发显示 \n(最终提交渲染模式)',ann="",h=50,w=130)
	pm.setParent( '..' )
	pm.button(l='yeti毛发显隐切换',c=yetidisplays,h=50,w=80,ann="默认操作为切换选中目标显隐（无需选毛发节点，框选到控制器即可）！！")
	pm.showWindow()