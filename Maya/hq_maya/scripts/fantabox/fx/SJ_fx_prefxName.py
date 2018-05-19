#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
def fx_prefixName(arg):
    name =pm.textField('fx_prefixNametxt',tx=1,q=1)
    selcbs = pm.checkBox("fx_prefixNamecb" ,q=True,v=True)
    readonlylist = pm.ls(ro=1,type="mesh")
    if selcbs==0:
        sels =pm.ls(sl=1,long=1)
        selall = pm.listRelatives(sels,ad=1)
        meshshapes =[a.getParent() for a in selall if a.nodeType()=="mesh"]
    else:
        meshshapes =[a for a in pm.ls(type="mesh",long=1) if a not in readonlylist]
    if selcbs==1:
        for m in range(len(meshshapes)):
            clothsels = pm.rename(meshshapes[m].getParent(),name+"_cloth_geo"+str(m+1))
            pm.rename(meshshapes[m],clothsels+"Shape")
    else:
        for m in range(len(meshshapes)):
            print 
            clothsels = pm.rename(meshshapes[m],name+"_cloth_geo"+str(m+1))
            pm.rename(clothsels.getShape(),clothsels+"Shape")
    geogrp = pm.group(meshshapes,name=name+"_cloth_geo")
    allgrp = pm.group(geogrp,name = name+"_all")
    pm.parent(allgrp,w=1)
def fx_prefixNameUI():
    '''
    {'load':'maya_fx','defaultOption':1,'CNname':'特效abc模型输出一键整理'}
    '''
    if pm.window('fx_prefixNamewd',ex=True):
        pm.deleteUI('fx_prefixNamewd',wnd=True)
    pm.window('fx_prefixNamewd',t='fx_prefixName_ToolV1.0')
    pm.columnLayout(adj=True)
    pm.text(l='特效abc模型输出一键整理',fn='fixedWidthFont',annotation="",w=400,h=50,ann="")
    pm.textField('fx_prefixNametxt',tx="PrefixName",h=30,w=100,ann ="重命名名字")
    pm.setParent( '..' )
    pm.flowLayout( columnSpacing=0)
    pm.checkBox("fx_prefixNamecb" ,label='是否对所有mesh执行规范',v=0,ann="默认不勾选为只针对选中大组内的模型进行规范",h=50,w=300)
    pm.setParent( '..' )
    pm.button(l='执行规范',c=fx_prefixName,w=200,h=50,bgc=[0.4,0.7,0.5],ann="选择大组，执行命令")
    pm.showWindow()