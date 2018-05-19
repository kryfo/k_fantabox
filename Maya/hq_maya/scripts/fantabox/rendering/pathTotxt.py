#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-07-31
import maya.cmds as cmds
import os
def CacheGetDirs(types,attrs):
    sels = cmds.ls(type=types)
    getdirslist = []
    for sel in sels:
        getpath = cmds.getAttr(sel+'.'+attrs )
        if getpath!=None:
            getdir = os.path.dirname(getpath)
            getdirslist.append(getdir)
    getdirslist = list(set(getdirslist))
    return getdirslist
def refGetDirs():        
    refpaths =cmds.file(q=1,r=1)
    refpathlist=[]
    for refpath in refpaths:
        refgetdir = os.path.dirname(refpath)
        refpathlist.append(refgetdir)
    refpathlist=list(set(refpathlist))
    return  refpathlist
def pathToTxt_main():
    path =cmds.textField('aistpath',tx=1,q=1).replace("\\","/")
    name = cmds.file(expandName=1,q=1).split("/")[-1].split(".")[0] 
    abccb_value=cmds.checkBox("abccb" ,q=True,v=True)
    Aistcb_value=cmds.checkBox("Aistcb" ,q=True,v=True)
    refcb_vlaue=cmds.checkBox("refcb" ,q=True,v=True)
    VRayMeshcb_value=cmds.checkBox("VRayMeshcb" ,q=True,v=True)
    clothCachecb_value=cmds.checkBox("clothCachecb" ,q=True,v=True)
    texFilecb_value=cmds.checkBox("texFilecb" ,q=True,v=True) 
    pathTotxtdicts={}
    if abccb_value ==1:
        abc_getdirs = CacheGetDirs('AlembicNode','abc_File')
        pathTotxtdicts['AlembicNode']= abc_getdirs
    if Aistcb_value ==1:
        AiST_getdirs = CacheGetDirs('aiStandIn','dso')
        pathTotxtdicts['aiStandIn']= AiST_getdirs
    if VRayMeshcb_value ==1:
        VRayMesh_getdirs = CacheGetDirs('VRayMesh','fileName')
        pathTotxtdicts['VRayMesh']= VRayMesh_getdirs
    if clothCachecb_value ==1:
        clothCache_getdirs = CacheGetDirs('cacheFile','cachePath')
        pathTotxtdicts['clothCache']= clothCache_getdirs
    if texFilecb_value ==1:
        texFile_getdir = CacheGetDirs('file','fileTextureName')
        aiTexFile_getdir = CacheGetDirs('aiImage','filename')
        texFile_getdirs = texFile_getdir+aiTexFile_getdir
        pathTotxtdicts['texFile']= texFile_getdirs
    if refcb_vlaue ==1:
        Ref_getdirs = refGetDirs()
        pathTotxtdicts['reference']= Ref_getdirs 
    files=open(path+"/"+name+'.txt', 'w')
    if pathTotxtdicts!={}:
        for pathTotxtdict in pathTotxtdicts:
            files.write(pathTotxtdict.upper() + ": \n"+len(pathTotxtdict)*"="+"\n")
            pathTotxtlists =  pathTotxtdicts[pathTotxtdict]
            for pathTotxtlist in pathTotxtlists:
                files.write(pathTotxtlist + "\n"+72*"-"+"\n")
        files.close()
    print "已输出路径到txt文件!",      

def pathTotxt():
    '''
    {'load':'maya_common','defaultOption':1,'CNname':'将路径输出到TXT文档'}
    '''
    if cmds.window('PathToTxtwd',ex=True):
        cmds.deleteUI('PathToTxtwd',wnd=True)
    cmds.window('PathToTxtwd',t='PathToTxt_Tool')
    cmds.columnLayout(adj=True,w=300)
    cmds.text(l='路径输出到Txt工具V1.0', fn='fixedWidthFont',h=50,ann="" )
    cmds.textField('aistpath',tx="D:/textest/fur",h=30)
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("abccb" ,label='输出abc路径',v=1,ann="",w=100,h=30)
    cmds.checkBox("Aistcb" ,label='输出Ass路径',v=1,ann="",w=120,h=30)
    cmds.checkBox("refcb" ,label='输出参考路径',v=1,ann="",w=120,h=30)
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("texFilecb" ,label='输出贴图路径',v=1,ann="",w=100,h=30)
    cmds.checkBox("VRayMeshcb" ,label='输出vray缓存路径',v=1,ann="",w=120,h=30)
    cmds.checkBox("clothCachecb" ,label='输出布料及几何体缓存路径',v=1,ann="",w=150,h=30)
    cmds.setParent( '..' )
    cmds.button(l='输出路径到txt',c='fb.ren.pathToTxt_main()',h=50,ann="")
    cmds.showWindow()