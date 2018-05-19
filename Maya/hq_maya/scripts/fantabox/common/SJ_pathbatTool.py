#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-08-22
import maya.cmds as cmds
import os
def CacheGetDirs(types,attrs):
    try:
        sels = cmds.ls(type=types)
    except:
        sels=[]
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
def replaceDirs(types,attrs,srtxt,trtxt):
    if types!="file":
        sels = cmds.ls(type=types)
        getdirslist = []
        for sel in sels:
            getpath = cmds.getAttr(sel+'.'+attrs )
            if getpath!=None:
                getdir = os.path.dirname(getpath).replace(srtxt,trtxt).replace("\\","/")
                filename = os.path.basename(getpath)
                cmds.setAttr(sel+'.'+attrs,getdir+"/"+filename,type="string")
                return sel+'.'+attrs
    else:
        sels = cmds.ls(type="file")
        getdirslist = []
        for sel in sels:
            getpath = cmds.getAttr(sel+'.'+attrs )
            if getpath!=None:
                getdir = os.path.dirname(getpath).replace(srtxt,trtxt).replace("\\","/")
                filename = os.path.basename(getpath)
                try:
                    cmds.setAttr(sel+'.'+attrs,getdir+"/"+filename,type="string")
                except:
                    pass
            if  cmds.listAttr(sel,ud=1)!=None:
                Texs =[a for a in cmds.listAttr(sel,ud=1) if a.find("Tex")!=-1]
            else:
                Texs =[]
            for Tex in Texs:
                getpath = cmds.getAttr(sel+'.'+Tex )
                if getpath!=None:
                    getdir = os.path.dirname(getpath).replace(srtxt,trtxt).replace("\\","/")
                    filename = os.path.basename(getpath)
                    try:
                        cmds.setAttr(sel+'.'+Tex,getdir+"/"+filename,type="string")
                    except:
                        pass
                return sel+'.'+attrs

def pathreplace_main():
    repalceA =cmds.textField('repalceA',tx=1,q=1)
    repalceB =cmds.textField('repalceB',tx=1,q=1)
    name = cmds.file(expandName=1,q=1).split("/")[-1].split(".")[0] 
    abccb_value=cmds.checkBox("abccb" ,q=True,v=True)
    Aistcb_value=cmds.checkBox("Aistcb" ,q=True,v=True)
    refcb_vlaue=cmds.checkBox("refcb" ,q=True,v=True)
    VRayMeshcb_value=cmds.checkBox("VRayMeshcb" ,q=True,v=True)
    clothCachecb_value=cmds.checkBox("clothCachecb" ,q=True,v=True)
    texFilecb_value=cmds.checkBox("texFilecb" ,q=True,v=True) 
    if abccb_value ==1:
        try:
            replaceDirs('AlembicNode','abc_File',repalceA,repalceB)
        except:
            pass
    if Aistcb_value ==1:
        try:
            replaceDirs('aiStandIn','dso',repalceA,repalceB)
        except:
            pass
    if VRayMeshcb_value ==1:
        try:
            replaceDirs('VRayMesh','fileName',repalceA,repalceB)
        except:
            pass
    if clothCachecb_value ==1:
        try:
            replaceDirs('cacheFile','cachePath',repalceA,repalceB)
        except:
            pass
    if texFilecb_value ==1:
        try:
            replaceDirs('file','fileTextureName',repalceA,repalceB)
        except:
            pass
        try:
            replaceDirs('aiImage','filename',repalceA,repalceB)
        except:
            pass
    if refcb_vlaue ==1:
        print "参考路径批量替换功能正在开发中..."
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
        if not cmds.pluginInfo( 'AbcExport', query=True, loaded=True ):
            cmds.loadPlugin('AbcExport')
        abc_getdirs = CacheGetDirs('AlembicNode','abc_File')
        pathTotxtdicts['AlembicNode']= abc_getdirs
    if Aistcb_value ==1:
        if not cmds.pluginInfo( 'mtoa', query=True, loaded=True ):
            cmds.loadPlugin('mtoa')
        abc_getdirs = CacheGetDirs('AlembicNode','abc_File')
        AiST_getdirs = CacheGetDirs('aiStandIn','dso')
        pathTotxtdicts['aiStandIn']= AiST_getdirs
    if VRayMeshcb_value ==1:
        if not cmds.pluginInfo( 'vrayformaya', query=True, loaded=True ):
            cmds.loadPlugin('vrayformaya')
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
    if os.path.exists(path)==True:
        files=open(path+"/"+name+'.txt', 'w')
        if pathTotxtdicts!={}:
            for pathTotxtdict in pathTotxtdicts:
                files.write(pathTotxtdict.upper() + ": \n"+len(pathTotxtdict)*"="+"\n")
                pathTotxtlists =  pathTotxtdicts[pathTotxtdict]
                for pathTotxtlist in pathTotxtlists:
                    files.write(pathTotxtlist + "\n"+72*"-"+"\n")
            files.close()
        print "已输出路径到txt文件!",      
    else:
        cmds.warning("目标路径不存在！！")

def SJ_pathbatTool():
    '''
    {'load':'maya_common','defaultOption':1,'CNname':'批量处理路径工具'}
    '''
    if cmds.window('PathbatToolwd',ex=True):
        cmds.deleteUI('PathbatToolwd',wnd=True)
    cmds.window('PathbatToolwd',t='Pathbat_Tool')
    cmds.columnLayout(adj=True,w=372)
    cmds.text(l='路径批处理工具V2.0', fn='fixedWidthFont',h=50,ann="" )
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
    cmds.textField('aistpath',tx=cmds.file(q=1,expandName=1),h=30)
    cmds.button(l='输出路径到txt',c='fb.com.pathToTxt_main()',h=50,ann="")
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.text(l="需要替换的路径关键字：",h=30,w=185)
    cmds.text(l="替换后的路径关键字：",h=30,w=185)
    cmds.setParent( '..' )  
    cmds.flowLayout( columnSpacing=0)
    cmds.textField('repalceA',tx="source",h=30,w=185)
    cmds.textField('repalceB',tx="target",h=30,w=185)
    cmds.setParent( '..' )  
    cmds.button(l='替换路径关键字',c='fb.com.pathreplace_main()',h=50,ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_pathbatTool()