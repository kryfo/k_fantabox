#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-08-22
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import fantabox.common
import os
def getrepeatName():
    global rpnamedict
    rpnamedict = fantabox.common.rpname()
    cmds.textScrollList("rpnamelists",e=1,ra=1,a=rpnamedict.keys())
def getWrongShape():
    global rpnamedict
    rpnamedict={}
    wrongshapelist= fantabox.common.k004_check_vshapeNode()
    cmds.textScrollList("rpnamelists",e=1,ra=1,a=wrongshapelist)
def rpnameselect():
    rpnamekeys = cmds.textScrollList("rpnamelists",q=1,si=1)
    rpnamesels =[]   
    for  rpnamekey in rpnamekeys:
        if rpnamedict.get(rpnamekey)!=None:
            rpnamesels+=rpnamedict.get(rpnamekey)
        else:
            rpnamesels.append(rpnamekey)
    pm.select(rpnamesels,r=1) 

def renamerpnode():
    newname = cmds.textField('rpnames',tx=1,q=1)
    rplists = pm.ls(sl=1,l=1)
    errormesh ={}
    rnamelists = []
    for r in range(len(rplists)):
        if  pm.nodeType(rplists[r])=="transform":
            childs = [a for a in  rplists[r].getChildren() if pm.nodeType(a)=="mesh"] 
            if len(childs)<=1 :
                rnamelists.append(rplists[r])
            else:
                errormesh[rplists[r]]= childs
        else:
            try:
                rplistpa = rplists[r].getParent()
            except:
                rplistpa=None
            if rplistpa!=None:
                childs = [a for a in  rplistpa.getChildren() if pm.nodeType(a)=="mesh"]
                if len(childs)<=1 :
                    rnamelists.append(rplistpa)
                else:
                    errormesh[rplists[r]]= childs
            else:
                rplists[r].rename(newname+str(r))
    if rnamelists!=[]:
        w=0
        rnamelist = list(set(rnamelists))
        for t in range(len(rnamelist)):
            if pm.objExists(newname+str(w))==False:
                rnamelist[t].rename(newname+str(w))
                rnamelist[t].getShape().rename(newname+str(w)+"Shape")
                w=w+1
            else:
                print rnamelist[t]
                rnamelist[t].rename("tmp")
                while pm.objExists(newname+str(w))==True:
                    w=w+1
                rnamelist[t].rename(newname+str(w))
                rnamelist[t].getShape().rename(newname+str(w)+"Shape")
                    
    pm.select(cl=1)
    if errormesh.keys()!=[]:
        pm.select(errormesh.values(),r=1)
        pm.warning("已选中拥有多个shape节点的错误模型！！")
    
def SJ_repeatNameToolUI():
    '''
    {'load':'maya_common','defaultOption':1,'CNname':'检查重名工具'}
    '''
    if cmds.window('SJ_repeatName_wd',ex=True):
        cmds.deleteUI('SJ_repeatName_wd',wnd=True)
    cmds.window('SJ_repeatName_wd',t='SJ_repeatNameToolV1.0')
    cmds.columnLayout(adj=True,w=400)
    cmds.text(l='检查重名工具', fn='fixedWidthFont',h=30,ann="")
    cmds.textScrollList("rpnamelists",allowMultiSelection=1,h=80,sc="fb.com.rpnameselect()")
    cmds.flowLayout( columnSpacing=0)
    cmds.button(l='检查重名节点',c="fb.com.getrepeatName()",h=40,w=200,ann="")
    cmds.button(l='检查不正确Shape节点',c='fb.com.getWrongShape()',h=40,w=200,ann="")
    cmds.setParent('..')
    cmds.textField('rpnames',tx="newName",h=30)
    cmds.button(l='重命名所选节点',c="fb.com.renamerpnode()",h=40,ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_repeatNameToolUI()