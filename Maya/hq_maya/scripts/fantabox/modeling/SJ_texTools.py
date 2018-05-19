#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-06-09
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
import fantabox
from  fantabox.common.SJ_clipBoard import *
class sjtextool ():
#获取所有贴图路径
    def getpath(self,filenode):
        nmfilepath  ={}
        mulfilepath  = {}
        if pm.nodeType(filenode)=="file":
            if pm.listConnections(filenode,d=0,type="choice")==[]:
                nmfilepath[filenode]=pm.getAttr(filenode+".fileTextureName").replace("\\","/")
            else:
                userattr =  pm.listAttr(filenode,ud=1)
                userattrpath = {}
                for u in range(len(userattr)):
                    if userattr[u][:3]=="Tex":
                        userattrpath[userattr[u]] = pm.getAttr(filenode +"."+userattr[u]).replace("\\","/")
                mulfilepath[filenode] = userattrpath
        else:
            try:
                nofiles = filenode.getShape()
            except:
                nofiles=filenode
            if nofiles!=[]:
                pgyetitexs = pm.pgYetiGraph(pm.PyNode(nofiles),listNodes=True,type="texture")                
                if pgyetitexs !=None:
                    yetipaths = {}
                    yetipathsudim ={}
                    for p in range(len(pgyetitexs)):
                        yetipath = pm.pgYetiGraph(nofiles,node=pgyetitexs[p],param="file_name",getParamValue=True)
                        if yetipath[-10:-4].upper() !="<UDIM>":
                            yetipaths[pgyetitexs[p]]=yetipath
                        else:
                            yetipathsudim[pgyetitexs[p]]=yetipath
                    if yetipaths!={}:
                        nmfilepath[nofiles] = yetipaths
                    if yetipathsudim!={}:
                        mulfilepath[nofiles] = yetipathsudim
        return nmfilepath,mulfilepath
        
    def checkexs(self,checknode,checkpath,checkex,checknoex):
        if os.path.exists(os.path.dirname(checkpath))==True:
            if os.path.splitext(os.path.basename(checkpath))[0][-6:].upper()!="<UDIM>":
                if os.path.exists(checkpath):
                    if checkex.has_key(os.path.dirname(checkpath))==False:
                        checkex[os.path.dirname(checkpath)] = {checknode:checkpath}
                    else:
                        checkex[os.path.dirname(checkpath)].update({checknode:checkpath})
                else:
                    if checknoex.has_key(os.path.dirname(checkpath))==False:
                        checknoex[os.path.dirname(checkpath)] = {checknode:checkpath}
                    else:
                        checknoex[os.path.dirname(checkpath)].update({checknode:checkpath})
            else:
                cklists = os.listdir(os.path.dirname(checkpath))
                for cklist in cklists:
                    if os.path.splitext(cklist)[0][:-4] ==os.path.splitext(os.path.basename(checkpath))[0][:-6]:
                        if os.path.exists( os.path.dirname(checkpath)+"/"+cklist): 
                            if checkex.has_key(os.path.dirname(checkpath))==False:
                                checkex[os.path.dirname(checkpath)] = {checknode:checkpath}
                            else:
                                checkex[os.path.dirname(checkpath)].update({checknode:checkpath})
                        else:
                            if checknoex.has_key(os.path.dirname(checkpath))==False:
                                checknoex[os.path.dirname(checkpath)] = {checknode:checkpath}
                            else:
                                checknoex[os.path.dirname(checkpath)].update({checknode:checkpath})
                    else:
                        pass
        else:
            if checknoex.has_key(os.path.dirname(checkpath))==False:
                checknoex[os.path.dirname(checkpath)] = {checknode:checkpath}
            else:
                checknoex[os.path.dirname(checkpath)].update({checknode:checkpath})
        return checkex,checknoex
                        
    def setcopy(self,filenode,yetitex,path,tarpaths,filetexname,setv,copyv,whole,absolute):
        #(节点名，yeti贴图节点，原始路径，目标路径，属性名，是否设置贴图，是否拷贝贴图，是否启动全局模式）
        if whole == 0:
            tarpath =tarpaths
        else:
            if path.find("sourceimages")!=-1:
                tarpath =os.path.dirname(tarpaths)+"/"+path[path.find("sourceimages"):]
            else:
                tarpath = tarpaths
        if pm.nodeType(filenode)=="file":
            if path !=tarpath:
                fileudimadj = os.path.splitext(os.path.basename(path))[0][-6:]
                orginalmode = filenode.getAttr("uvTilingMode")
                if fileudimadj.upper()!="<UDIM>":
                    if orginalmode==0:
                        if os.path.exists(os.path.dirname(path)):
                            if copyv ==1:                   
                                if os.path.exists(tarpath):
                                    os.remove(tarpath)
                                if os.path.exists(os.path.dirname(tarpath))!=True:
                                    os.makedirs(os.path.dirname(tarpath),mode =0777)
                                if os.path.exists(os.path.dirname(tarpath))!=True:
                                    os.makedirs(os.path.dirname(tarpath),mode =0777)
                                pm.sysFile(path,copy=tarpath)
                        else:
                            if setv ==1:
                                if absolute==0:
                                    pm.setAttr(filenode+"."+filetexname,tarpath,type="string")    
                                else:
                                    if path.find("sourceimages")!=-1:
                                        pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string") 
                                    else:
                                        "no sourceimages!!", 
                    else:
                        if os.path.exists(os.path.dirname(path))==True:
                            filelists = os.listdir(os.path.dirname(path))
                            for filelist in filelists:
                                if os.path.splitext(filelist)[0][:-4] ==os.path.splitext(os.path.basename(path))[0][:-4]:
                                    if os.path.exists(os.path.dirname(tarpath)+"/"+filelist):
                                        os.remove(os.path.dirname(tarpath)+"/"+filelist)
                                        if os.path.exists(os.path.dirname(tarpath))!=True:
                                            os.makedirs(os.path.dirname(tarpath),mode =0777)
                                        pm.sysFile(os.path.dirname(path)+"/"+filelist,copy=os.path.dirname(tarpath)+"/"+filelist)
                                    else:
                                        if os.path.exists(os.path.dirname(tarpath))!=True:
                                            os.makedirs(os.path.dirname(tarpath),mode =0777)
                                        pm.sysFile(os.path.dirname(path)+"/"+filelist,copy=os.path.dirname(tarpath)+"/"+filelist)
                                else:
                                    if setv ==1:
                                        filenode.setAttr("uvTilingMode",0)
                                        if absolute==0:
                                            pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                                        else:
                                            if path.find("sourceimages")!=-1:
                                                pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                            else:
                                                "no sourceimages!!", 
                                        filenode.setAttr("uvTilingMode",int(orginalmode))
                        else:
                            if setv ==1:
                                filenode.setAttr("uvTilingMode",0)
                                if absolute==0:
                                    pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                                else:
                                    if path.find("sourceimages")!=-1:
                                        pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                    else:
                                        "no sourceimages!!", 
                                filenode.setAttr("uvTilingMode",int(orginalmode))
                    if setv ==1:
                        if orginalmode==0:
                            if absolute==0:
                                pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                            else:
                                if path.find("sourceimages")!=-1:
                                    pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                else:
                                    "no sourceimages!!", 
                        else:
                            filenode.setAttr("uvTilingMode",0)
                            if absolute==0:
                                pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                            else:
                                if path.find("sourceimages")!=-1:
                                    pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                else:
                                    "no sourceimages!!", 
                            filenode.setAttr("uvTilingMode",int(orginalmode))
                else:
                    if os.path.exists(os.path.dirname(path)):
                        filelists = os.listdir(os.path.dirname(path))
                    elif os.path.exists(os.path.dirname(tarpaths)):
                        filelists = os.listdir(os.path.dirname(tarpaths))
                    else:
                        filelists = []
                    if filelists!=[]:
                        for filelist in filelists:
                            print filelist
                            if os.path.splitext(filelist)[0][:-4] ==os.path.splitext(os.path.basename(path))[0][:-6]:
                                if copyv ==1:
                                    if os.path.exists(os.path.dirname(tarpath)+"/"+filelist):
                                        os.remove(os.path.dirname(tarpath)+"/"+filelist)
                                    else:
                                        pass
                                    if os.path.exists(os.path.dirname(tarpath))!=True:
                                        os.makedirs(os.path.dirname(tarpath),mode =0777)
                                    else:
                                        pass
                                    pm.sysFile(os.path.dirname(path)+"/"+filelist,copy=os.path.dirname(tarpath)+"/"+filelist)
                                else:
                                    pass
                            else:
                                if setv ==1:
                                    filenode.setAttr("uvTilingMode",0)
                                    if absolute==0:
                                        pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                                    else:
                                        if path.find("sourceimages")!=-1:
                                            pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                        else:
                                            "no sourceimages!!", 
                                    filenode.setAttr("uvTilingMode",int(orginalmode))
                        if setv ==1:
                            if orginalmode==0:
                                if absolute==0:
                                    pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                                else:
                                    if path.find("sourceimages")!=-1:
                                        pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                    else:
                                        "no sourceimages!!", 
                            else:
                                filenode.setAttr("uvTilingMode",0)
                                if absolute==0:
                                    pm.setAttr(filenode+"."+filetexname,tarpath,type="string")
                                else:
                                    if path.find("sourceimages")!=-1:
                                        pm.setAttr(filenode+"."+filetexname,path[path.find("sourceimages"):],type="string")
                                    else:
                                        "no sourceimages!!",
                                filenode.setAttr("uvTilingMode",int(orginalmode))
        elif pm.nodeType(filenode)=="pgYetiMaya":
            if path !=tarpath:
                yetiudimadj = os.path.splitext(os.path.basename(path))[0][-6:]
                if yetiudimadj.upper()!="<UDIM>":
                    if os.path.exists(os.path.dirname(path)):
                        if copyv ==1:
                            if os.path.exists(tarpath):
                                os.remove(tarpath)
                            else:
                                pass
                            if os.path.exists(os.path.dirname(tarpath))!=True:
                                os.mkdir(os.path.dirname(tarpath))
                            else:
                                pass
                            pm.sysFile(path,copy=tarpath)
                        if setv ==1:
                            pm.pgYetiGraph(filenode,node=yetitex,param="file_name",setParamValueString=str(tarpath)) 
                    else:
                        if setv ==1:
                            pm.pgYetiGraph(filenode,node=yetitex,param="file_name",setParamValueString=str(tarpath)) 
                else:
                    if os.path.exists(path)==True:
                        filelists = os.listdir(os.path.dirname(path))
                    else:
                        filelists = os.listdir(os.path.dirname(tarpath))

                    for filelist in filelists:
                        if os.path.splitext(filelist)[0][:-4] ==os.path.splitext(os.path.basename(path))[0][:-6]:
                            if copyv ==1:
                                if os.path.exists(os.path.dirname(tarpath)+"/"+filelist):
                                    os.remove(os.path.dirname(tarpath)+"/"+filelist)
                                else:
                                    pass
                                if os.path.exists(os.path.dirname(tarpath))!=True:
                                    os.makedirs(os.path.dirname(tarpath),mode =0777)
                                else:
                                    pass
                                pm.sysFile(os.path.dirname(path)+"/"+filelist,copy=os.path.dirname(tarpath)+"/"+filelist)
                            else:
                                pass
                        else:
                            if setv ==1:
                                pm.pgYetiGraph(filenode,node=yetitex,param="file_name",setParamValueString=str(tarpath))  
                            
                    if setv ==1:
                        pm.pgYetiGraph(filenode,node=yetitex,param="file_name",setParamValueString=str(tarpath))                        
                    else:
                        pass
            else:
                pass
        return tarpath
def checktexpath(arg):
    newpath = cmds.textField('tartexpath',tx=1,q=1).replace("\\","/")
    settexvalue=pm.checkBox("settexpathcb" ,q=True,v=True)
    copytexvalue=pm.checkBox("copytexpathcb" ,q=True,v=True)
    wholevalue=pm.checkBox("wholecb" ,q=True,v=True)
    filewholes = pm.ls(type="file")+[u for u in pm.ls(type="pgYetiMaya") if pm.pgYetiGraph(u,listNodes=True,type="texture") !=[]]  
    global existspath
    global noexistpath
    existspath = {}
    noexistpath ={}
    for filewhole in filewholes:
        ##非多贴图
        if  sjtextool().getpath(filewhole)[0] !={}:
            texnode =  sjtextool().getpath(filewhole)[0]
            for texpath in texnode.values():
                if type(texpath)!=type({}):
                    filename =  os.path.basename(texpath)
                    dirname = os.path.dirname(texpath)
                    ##一般贴图
                    if texnode.keys()[0].getAttr("uvTilingMode")==0:
                        sjtextool().checkexs(texnode.keys()[0],texpath,existspath,noexistpath)
                    ##UDIM
                    elif texnode.keys()[0].getAttr("uvTilingMode")==3:
                        sjtextool().checkexs(texnode.keys()[0],texpath,existspath,noexistpath)
                    else:
                        print "not supported UVTiling Mode!!",
                else:
                    ##yeti的非udim
                    for y in range(len(texnode.keys())):
                        yetitex = texnode.values()[y]
                        for t in range(len(yetitex.keys())):
                            sjtextool().checkexs(texnode.keys()[y],yetitex.values()[t],existspath,noexistpath)
        ##多贴图
        if sjtextool().getpath(filewhole)[1] !={}:
            multinode =  sjtextool().getpath(filewhole)[1]
            for e in range(len(multinode.values())):
                texattr =  multinode.values()[e]
                if pm.nodeType(multinode.keys()[e])=="file":
                    for x in range(len(texattr.keys())):
                        sjtextool().checkexs(multinode.keys()[e],texattr.values()[x],existspath,noexistpath)
                else:
                    ##yeti的udim
                    texattr =  multinode.values()[e]
                    for r in range(len(texattr.keys())):
                        sjtextool().checkexs(multinode.keys()[e],texattr.values()[r],existspath,noexistpath)
    cmds.textScrollList("nomisslist",e=1,ra=1,a=existspath.keys())
    cmds.textScrollList("misslist",e=1,ra=1,a=noexistpath.keys())

def copytexfile(arg):
    newpath = cmds.textField('tartexpath',tx=1,q=1).replace("\\","/")
    settexvalue=pm.checkBox("settexpathcb" ,q=True,v=True)
    copytexvalue=pm.checkBox("copytexpathcb" ,q=True,v=True)
    wholevalue=pm.checkBox("wholecb" ,q=True,v=True)
    absolutevalue=pm.checkBox("absolutecb" ,q=True,v=True)
    
    selectednodes = pm.ls(sl=1)
    for selectednode in selectednodes:
        ##非多贴图
        if  sjtextool().getpath(selectednode)[0] !={}:
            texnode =  sjtextool().getpath(selectednode)[0]
            for texpath in texnode.values():
                if type(texpath)!=type({}):
                    filename =  os.path.basename(texpath)
                    dirname = os.path.dirname(texpath)
                    ##一般贴图
                    if texnode.keys()[0].getAttr("uvTilingMode")==0:
                        sjtextool().setcopy(texnode.keys()[0],None,texpath,newpath+"/"+filename,"fileTextureName",int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue))
                    ##UDIM
                    elif texnode.keys()[0].getAttr("uvTilingMode")==3:
                        sjtextool().setcopy(texnode.keys()[0],None,texpath,newpath+"/"+filename,"fileTextureName",int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue))
                    else:
                        print "not supported UVTiling Mode!!",
                else:
                    ##yeti的非udim
                    for y in range(len(texnode.keys())):
                        yetitex = texnode.values()[y]
                        for t in range(len(yetitex.keys())):
                            #print texnode.keys()[y],yetitex.keys()[t],yetitex.values()[t],newpath+"/"+os.path.basename(yetitex.values()[t]),None,int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue)
                            sjtextool().setcopy(texnode.keys()[y],yetitex.keys()[t],yetitex.values()[t],newpath+"/"+os.path.basename(yetitex.values()[t]),None,int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue))
        ##多贴图
        if sjtextool().getpath(selectednode)[1] !={}:
            multinode =  sjtextool().getpath(selectednode)[1]
            for e in range(len(multinode.values())):
                texattr =  multinode.values()[e]
                if pm.nodeType(multinode.keys()[e])=="file":
                    for x in range(len(texattr.keys())):
                        sjtextool().setcopy(multinode.keys()[e],None,texattr.values()[x],newpath+"/"+os.path.basename(texattr.values()[x]),texattr.keys()[x],int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue))
                else:
                    ##yeti的udim
                    texattr =  multinode.values()[e]
                    for r in range(len(texattr.keys())):
                        #print multinode.keys()[e],texattr.keys()[r],texattr.values()[r],newpath+"/"+os.path.basename(texattr.values()[r]),None,int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue)
                        sjtextool().setcopy(multinode.keys()[e],texattr.keys()[r],texattr.values()[r],newpath+"/"+os.path.basename(texattr.values()[r]),None,int(settexvalue),int(copytexvalue),int(wholevalue),int(absolutevalue))

def missselect():
    missselects = cmds.textScrollList("misslist",q=1,si=1)    
    missseled =[]
    if missselects!=[]:
        for missselecta in missselects:
            missseled =missseled+noexistpath[missselecta].keys()
    pm.select(missseled,r=1) 
    
def dismissselect():
    nomisssilist = cmds.textScrollList("nomisslist",q=1,si=1)
    nomissseled =[]
    if nomisssilist!=[]:
        for nomisssilista in nomisssilist:
            nomissseled =nomissseled+existspath[nomisssilista].keys()
    pm.select(nomissseled,r=1) 
def doubleClickNomiss():
    nomisssilist = cmds.textScrollList("nomisslist",q=1,si=1)
    if  nomisssilist!=[]:
        fantabox.common.setClipboard(nomisssilist[0])
def doubleClickmiss():
    misssilist = cmds.textScrollList("misslist",q=1,si=1)
    if  misssilist!=[]:
        fantabox.common.setClipboard(misssilist[0])
def SJ_texToolswdUI():
    '''
    2.5更新说明：增加双击复制文件夹路径功能
    2.6更新说明：修复贴图及yeti节点路径不存在时，无法获取节点路径到列表中的问题
    2.7更新说明:修复源路径没有贴图，进行设置贴图路径时报错问题
    2.8更新说明：修复源路径不存在，yeti的udim无法指认贴图路径问题
    '''
    if cmds.window('textoolwd',ex=True):
        cmds.deleteUI('textoolwd',wnd=True)
    cmds.window('textoolwd',t='TexToolV2.7')
    cmds.columnLayout(adj=True)
    cmds.text(l='贴图工具集V2.7',fn='fixedWidthFont',annotation="",w=250,h=50,ann="2.7更新说明:修复源路径没有贴图，进行设置贴图路径时报错问题")
    cmds.button(l='检查贴图',c=checktexpath,bgc=[0.4,0.7,0.5],w=180,h=50,ann="点击执行检查贴图，会将结果根据情况反馈到未丢失贴图的文件夹路径文本框及丢失贴图路径的file节点文本框内")
    cmds.text(l='目标贴图路径',fn='fixedWidthFont',annotation="",w=250,h=30)
    cmds.textField('tartexpath',tx="D:\\testfile\\tex",h=30,w=100,ann ="贴图路径")
    cmds.flowLayout( columnSpacing=0)
    cmds.text(l='未丢失贴图的文件夹路径',fn='fixedWidthFont',annotation="文本框内选择贴图文件夹路径选项，会自动选取文件内所有指定到该文件夹的file节点；多选再点击执行操作按钮会启动高级模式。",w=250,h=45)
    cmds.text(l='丢失贴图路径的file节点',fn='fixedWidthFont',annotation="文本框内选择丢失贴图节点选项，会自动选取该file节点",w=250,h=45)
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.textScrollList("nomisslist",allowMultiSelection=1,w=250,h=150,sc=dismissselect,dcc = doubleClickNomiss)
    cmds.textScrollList("misslist",allowMultiSelection=1,w=250,h=150,sc=missselect,dcc = doubleClickmiss)
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("wholecb" ,label='开启项目模式',v=0,ann="会在目标路径下建立角色子文件夹啊，注意：源贴图路径角色需要单独的贴图文件夹！！",h=50,w=125,bgc=[0.4,0.7,0.5])
    cmds.checkBox("absolutecb" ,label='切换为相对路径',v=0,ann="",h=50,w=125,bgc=[0.4,0.7,0.5])
    cmds.checkBox("copytexpathcb" ,label='启用拷贝功能',v=1,ann="勾选为执行对所选file节点的贴图进行拷贝操作，默认勾选",h=50,w=125,bgc=[0.4,0.7,0.5])
    cmds.checkBox("settexpathcb" ,label='启用指定功能',v=1,ann="勾选为执行对所选file节点的贴图进行指定操作",h=50,w=125,bgc=[0.4,0.7,0.5])
    cmds.setParent( '..' )
    cmds.button(l='执行操作',c=copytexfile,w=200,h=50,bgc=[0.4,0.7,0.5],ann="请输入目标贴图路径，并在以上文本框中选择需要执行操作的贴图文件夹路径，根据需要对以上选项进行勾选，再点击执行操作")
    cmds.button(l='贴图管理工具（原zz01）',c="mel.eval(r'zzFileTexturemanager')",w=200,h=50,bgc=[0.4,0.7,0.5],ann="")
    cmds.showWindow()
if __name__=="__main__":
    SJ_texToolswdUI() 