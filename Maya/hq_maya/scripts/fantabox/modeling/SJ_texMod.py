#coding=cp936
#coding=utf-8
'''
��ͼ����ģ�飨����file�ڵ㣬yetië���ڵ㣬����ڵ����ͼ����
��ͼ����ࣨtexCheckClass����
    ������ͼ�ļ���·���б�������ʽ��[��ͼ�ļ���·��,......]����ck_texdirlists()
    ������ͼ�ڵ㼰��ͼ·���б�������ʽ��[{��ʧ��ͼ�ڵ㣺��ͼ·��},......]����ck_texpathlists()
    ������ʧ��ͼ�ļ���·���б�������ʽ��[��ͼ�ļ���·��,......]����ck_miss_texdirlists()
    ������ʧ��ͼ�ڵ㡾������ʽ��[��ʧ��ͼ�ڵ�,......]����ck_miss_texpathlists()
    ������ͼ����O����ͼ�ڵ㡾������ʽ��[��ͼ�ڵ�,......]��:texonODisk()    
'''
import pymel.core as pm
import os
import maya.cmds as cmds

class texCheckClass ():
    def __init__(self):
        self.yetinum =1
    if pm.pluginInfo("pgYetiMaya",q=1,loaded=1,name=1)==0:

        pm.warning("û�а�װyeti�������") 
        #��ȡ������ͼ·��
    def getPath(self,filenode):
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
                if self.yetinum==1:
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
                else:
                    pass

        return nmfilepath,mulfilepath
    #�����ͼ�Ƿ����    
    def checkExs(self,checknode,checkpath,checkex,checknoex):
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
            try:
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
            except:
                pass
        return checkex,checknoex

    def k_dx11file(self):
        k_dxtexfile=[]
        k_container = cmds.ls(type='container')
        k_dxs = [a for a in k_container if 'dx11Shader_ast' in a]
        for k_dx in k_dxs:
            k_dxfiles=cmds.container(k_dx,q=1,nodeList=1)
            for k_dxfile in k_dxfiles:
                k_dxtex=cmds.nodeType(k_dxfile)
                if k_dxtex=='file':
                    k_dxtexfile.append(k_dxfile)

        return k_dxtexfile


    #������нڵ㼰��ͼ·��    
    def checkTexPath(self):
        if self.yetinum==1:
            filewholes = pm.ls(type="file")+[u for u in pm.ls(type="pgYetiMaya") if pm.pgYetiGraph(u,listNodes=True,type="texture") !=[]]  
        else:
            filewholes = pm.ls(type="file")
        global existspath
        global noexistpath
        existspath = {}
        noexistpath ={}
        for filewhole in filewholes:
            ##�Ƕ���ͼ
            if  texCheckClass().getPath(filewhole)[0] !={}:
                texnode =  texCheckClass().getPath(filewhole)[0]
                for texpath in texnode.values():
                    if type(texpath)!=type({}):
                        filename =  os.path.basename(texpath)
                        dirname = os.path.dirname(texpath)
                        ##һ����ͼ
                        if texnode.keys()[0].getAttr("uvTilingMode")==0:
                            texCheckClass().checkExs(texnode.keys()[0],texpath,existspath,noexistpath)
                        ##UDIM
                        elif texnode.keys()[0].getAttr("uvTilingMode")==3:
                            texCheckClass().checkExs(texnode.keys()[0],texpath,existspath,noexistpath)
                        else:
                            print "not be supported UVTiling Mode!!",
                    else:
                        if self.yetinum==1:
                            ##yeti�ķ�udim
                            for y in range(len(texnode.keys())):
                                yetitex = texnode.values()[y]
                                for t in range(len(yetitex.keys())):
                                    texCheckClass().checkExs(texnode.keys()[y],yetitex.values()[t],existspath,noexistpath)
                        else:
                            pass
            ##����ͼ
            if texCheckClass().getPath(filewhole)[1] !={}:
                multinode =  texCheckClass().getPath(filewhole)[1]
                for e in range(len(multinode.values())):
                    texattr =  multinode.values()[e]
                    if pm.nodeType(multinode.keys()[e])=="file":
                        for x in range(len(texattr.keys())):
                            texCheckClass().checkExs(multinode.keys()[e],texattr.values()[x],existspath,noexistpath)
                    else:
                        if self.yetinum==1:
                            ##yeti��udim
                            texattr =  multinode.values()[e]
                            for r in range(len(texattr.keys())):
                                texCheckClass().checkExs(multinode.keys()[e],texattr.values()[r],existspath,noexistpath)
                        else:
                            pass
        return existspath,noexistpath


#������ͼ�ļ���·���б�
def ck_texdirlists():
    return texCheckClass().checkTexPath()[0].keys()
    
#������ͼ�ڵ㼰��ͼ·���б�
def ck_texpathlists():
    return texCheckClass().checkTexPath()[0].values()
    
#������ʧ��ͼ�ļ���·���б�
def ck_miss_texdirlists():
    return texCheckClass().checkTexPath()[1].keys()
    
#������ʧ��ͼ�ڵ�
def SJ_miss_texpathlists():
    misstexdict =  texCheckClass().checkTexPath()[1].values()
    if misstexdict!=[]:
        misstexlist = pm.ls([a.keys() for a in misstexdict][0])
        misstexlist = [ str(k) for k in misstexlist ]
        k_dxfile=texCheckClass().k_dx11file()
        misstexlist=list(set(misstexlist).difference(set(k_dxfile)))

    else:
        misstexlist=[]
    return misstexlist
    
#��������o����ͼ�ڵ��б�
def SJ_texNo2ODisk():
    texex =  []
    if texCheckClass().checkTexPath()[0]!=[]:
        fullpaths =  texCheckClass().checkTexPath()[0].keys()
        for f in range(len(fullpaths)):
            if fullpaths[f].split(":")[0].upper()!="O":
                texex= cmds.ls(texex+texCheckClass().checkTexPath()[0].values()[f].keys())
            else:
                pass
    return texex