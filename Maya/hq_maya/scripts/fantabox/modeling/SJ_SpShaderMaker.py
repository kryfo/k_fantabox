#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
import maya.mel as mel
import os
import time
class filenodebuild ():
    def builder(self,ptnode,filenode):
        pm.connectAttr(ptnode+".coverage",filenode+".coverage",f=1)
        pm.connectAttr(ptnode+".translateFrame",filenode+".translateFrame",f=1)
        pm.connectAttr(ptnode+".rotateFrame",filenode+".rotateFrame",f=1)
        pm.connectAttr(ptnode+".mirrorU",filenode+".mirrorU",f=1)
        pm.connectAttr(ptnode+".mirrorV",filenode+".mirrorV",f=1)
        pm.connectAttr(ptnode+".stagger",filenode+".stagger",f=1)
        pm.connectAttr(ptnode+".wrapU",filenode+".wrapU",f=1)
        pm.connectAttr(ptnode+".wrapV",filenode+".wrapV",f=1)
        pm.connectAttr(ptnode+".repeatUV",filenode+".repeatUV",f=1)
        pm.connectAttr(ptnode+".offset",filenode+".offset",f=1)
        pm.connectAttr(ptnode+".rotateUV",filenode+".rotateUV",f=1)
        pm.connectAttr(ptnode+".noiseUV",filenode+".noiseUV",f=1)
        pm.connectAttr(ptnode+".vertexUvOne",filenode+".vertexUvOne",f=1)
        pm.connectAttr(ptnode+".vertexUvTwo",filenode+".vertexUvTwo",f=1)
        pm.connectAttr(ptnode+".vertexUvThree",filenode+".vertexUvThree",f=1)
        pm.connectAttr(ptnode+".vertexCameraOne",filenode+".vertexCameraOne",f=1)
        pm.connectAttr(ptnode+".outUV",filenode+".uv",f=1)
        pm.connectAttr(ptnode+".outUvFilterSize",filenode+".uvFilterSize",f=1)  

def vrayspshmaker(arg):
    selit = pm.textScrollList("piclist",q=1,si=1)
    #selit = ["jia_al_1102l_Diffuse.1001.png"]
    path =pm.textField('sptexpath',tx=1,q=1).replace("\\","/")
    #path ="D:\\udim".replace("\\","/")
    paths =path+"/"+selit[0]
    textype =  os.path.splitext(os.path.basename(paths))[0].split("_")[-1]
    type = os.path.splitext(os.path.basename(paths))[-1]
    udimadj=  os.path.splitext(os.path.basename(paths))[0].split(".")[-1]
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    basename =  os.path.splitext(os.path.basename(paths))[0][0:len(os.path.splitext(os.path.basename(paths))[0])-len(textype)-1]
    dirname = os.path.dirname(paths)
    texlist =pm.getFileList(fld = dirname)
    textlists =[i for i in texlist if i[0:len(i)-len(i.split("_")[-1])-1]==basename]
    textlistspath =[dirname+"/"+i for i in textlists]
    if udimadj not in udimvial:
        textypeadj =[i.split(".")[0] for i in textlists ]
        diftex =  dirname+"/"+ basename+"_Diffuse"+type
        iortex =  dirname+"/"+ basename+"_ior"+type
        nortex =  dirname+"/"+ basename+"_Normal"+type
        heitex =  dirname+"/"+ basename+"_Height"+type
        Glosstex =  dirname+"/"+ basename+"_Glossiness"+type
        Reftex =  dirname+"/"+ basename+"_Reflection"+type
    
    else :
        textypeadj =[i.split(".")[0] for i in textlists ]
        diftex =  dirname+"/"+ basename+"_Diffuse."+str(udimadj)+type
        iortex =  dirname+"/"+ basename+"_ior."+str(udimadj)+type
        nortex =  dirname+"/"+ basename+"_Normal."+str(udimadj)+type
        heitex =  dirname+"/"+ basename+"_Height."+str(udimadj)+type
        Glosstex =  dirname+"/"+ basename+"_Glossiness."+str(udimadj)+type
        Reftex =  dirname+"/"+ basename+"_Reflection."+str(udimadj)+type
     
    sel =pm.ls(sl=1,type="transform")
    if sel!=[]:
        selshape =  sel[0].getShape()
        typeadj = pm.nodeType(selshape)
        if typeadj=="mesh":
            name = sel[0]+"_VS"
            newaishader = pm.shadingNode("VRayMtl",asShader=1,name=name)
            pm.setAttr(newaishader+".brdfType",3)
            pm.setAttr(newaishader+".lockFresnelIORToRefractionIOR",0)
            selshape =  sel[0].getShape()
            pm.select(sel,r=1)
            pm.hyperShade(assign=newaishader)
            if diftex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
                pm.setAttr(gammanode+".gammaX",0.454)
                pm.setAttr(gammanode+".gammaY",0.454)
                pm.setAttr(gammanode+".gammaZ",0.454)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",diftex,type="string")
                pm.connectAttr(filenode+".outColor",gammanode+".value")
                pm.connectAttr(gammanode+".outValue",newaishader+".diffuseColor")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)
            if Reftex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
                pm.setAttr(gammanode+".gammaX",0.454)
                pm.setAttr(gammanode+".gammaY",0.454)
                pm.setAttr(gammanode+".gammaZ",0.454)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",Reftex,type="string")
                pm.connectAttr(filenode+".outColor",gammanode+".value")
                pm.connectAttr(gammanode+".outValue",newaishader+".reflectionColor")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)
            if iortex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",iortex,type="string")
                pm.connectAttr(filenode+".outAlpha",newaishader+".fresnelIOR")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)   
            if Glosstex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",Glosstex,type="string")
                pm.connectAttr(filenode+".outAlpha",newaishader+".reflectionGlossiness")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)     
            if nortex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",nortex,type="string")
                pm.connectAttr(filenode+".outColor",newaishader+".bumpMap")
                pm.setAttr(newaishader+".bumpMapType",1)
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3) 
            if heitex in textlistspath:
                vraybump = pm.shadingNode("VRayBumpMtl",asShader=1,name=name)
                vraysg = pm.listConnections(newaishader,s=0,type="shadingEngine")
                pm.connectAttr(newaishader+".outColor",vraybump+".base_material",f=1)
                pm.connectAttr(vraybump+".outColor",vraysg[0]+".surfaceShader",f=1)
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",heitex,type="string")
                pm.connectAttr(filenode+".outColor",vraybump+".bumpMap",f=1)
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3) 
        else:
            print "请选择模型！！"


def arnoldspshmaker(arg):
    autocbvalue=pm.checkBox("autocb" ,q=True,v=True)
    selit = pm.textScrollList("piclist",q=1,si=1)
    #selit = ["jia_al_1102l_Diffuse.1001.png"]
    path =pm.textField('sptexpath',tx=1,q=1).replace("\\","/")
    #path ="D:\\udim".replace("\\","/")
    paths =path+"/"+selit[0]
    textype =  os.path.splitext(os.path.basename(paths))[0].split("_")[-1]
    type = os.path.splitext(os.path.basename(paths))[-1]
    udimadj=  os.path.splitext(os.path.basename(paths))[0].split(".")[-1]
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    basename =  os.path.splitext(os.path.basename(paths))[0][0:len(os.path.splitext(os.path.basename(paths))[0])-len(textype)-1]
    dirname = os.path.dirname(paths)
    texlist =pm.getFileList(fld = dirname)
    textlists =[i for i in texlist if i[0:len(i)-len(i.split("_")[-1])-1]==basename]
    textlistspath =[dirname+"/"+i for i in textlists]
    if udimadj not in udimvial:
        textypeadj =[i.split(".")[0] for i in textlists ]
        diftex =  dirname+"/"+ basename+"_Diffuse"+type
        f0tex =  dirname+"/"+ basename+"_f0"+type
        nortex =  dirname+"/"+ basename+"_Normal"+type
        heitex =  dirname+"/"+ basename+"_Height"+type
        routex =  dirname+"/"+ basename+"_Roughness"+type
        spetex =  dirname+"/"+ basename+"_Specular"+type
    else :
        textypeadj =[i.split(".")[0] for i in textlists ]
        diftex =  dirname+"/"+ basename+"_Diffuse."+str(udimadj)+type
        f0tex =  dirname+"/"+ basename+"_f0."+str(udimadj)+type
        nortex =  dirname+"/"+ basename+"_Normal."+str(udimadj)+type
        heitex =  dirname+"/"+ basename+"_Height."+str(udimadj)+type
        routex =  dirname+"/"+ basename+"_Roughness."+str(udimadj)+type
        spetex =  dirname+"/"+ basename+"_Specular."+str(udimadj)+type
    sel =pm.ls(sl=1,type="transform")

    if sel!=[]:
        selshape =  sel[0].getShape()
        typeadj = pm.nodeType(selshape)
        if typeadj=="mesh":
            name = sel[0]+"_AS"
            newaishader = pm.shadingNode("aiStandard",asShader=1,name=name)
            pm.setAttr(newaishader+".Ks",1)
            pm.setAttr(newaishader+".Kd",1)
            pm.setAttr(newaishader+".specularDistribution",1)
            pm.setAttr(newaishader+".specularFresnel",1)
            selshape =  sel[0].getShape()
            pm.select(sel,r=1)
            pm.hyperShade(assign=newaishader)
            if diftex in textlistspath:
                if autocbvalue==1:
                    os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(diftex,diftex[:-len(diftex.split(".")[-1])]+"tx")) 
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",diftex,type="string")
                pm.connectAttr(filenode+".outColor",newaishader+".color")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)
            if spetex in textlistspath:
                if autocbvalue==1:
                    os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(spetex,spetex[:-len(spetex.split(".")[-1])]+"tx")) 
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",spetex,type="string")
                pm.connectAttr(filenode+".outColor",newaishader+".KsColor")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)   
            if f0tex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
                pm.setAttr(gammanode+".gammaX",2.2)
                pm.setAttr(gammanode+".gammaY",2.2)
                pm.setAttr(gammanode+".gammaZ",2.2)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",f0tex,type="string")
                pm.connectAttr(filenode+".outColor",gammanode+".value")
                pm.connectAttr(gammanode+".outValueX",newaishader+".Ksn")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)
            if routex in textlistspath:
                filenode =pm.shadingNode("file",asTexture=1,name=name)
                ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
                gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
                pm.setAttr(gammanode+".gammaX",2.2)
                pm.setAttr(gammanode+".gammaY",2.2)
                pm.setAttr(gammanode+".gammaZ",2.2)
                filenodebuild().builder(ptnode,filenode)
                pm.setAttr(filenode+".colorProfile",3)
                pm.setAttr(filenode+".fileTextureName",routex,type="string")
                pm.connectAttr(filenode+".outColor",gammanode+".value")
                pm.connectAttr(gammanode+".outValueX",newaishader+".specularRoughness")
                if udimadj in udimvial:
                    pm.setAttr(filenode+".uvTilingMode",3)
            if nortex in textlistspath and heitex in textlistspath:
                if autocbvalue==1:
                    os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(nortex,nortex[:-len(nortex.split(".")[-1])]+"tx")) 
                nmfilenode =pm.shadingNode("file",asTexture=1,name=name)
                bmfilenode =pm.shadingNode("file",asUtility=1,name=name)
                nmptnode = pm.shadingNode("place2dTexture",asTexture=1,name=name)
                bmptnode = pm.shadingNode("place2dTexture",asTexture=1,name=name)
                nmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
                bmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
                pm.setAttr(nmnode+".bumpInterp",1)
                pm.setAttr(nmnode+".aiFlipR",0)
                pm.setAttr(nmnode+".aiFlipG",0)
                filenodebuild().builder(nmptnode,nmfilenode)
                filenodebuild().builder(bmptnode,bmfilenode)
                pm.setAttr(nmfilenode+".colorProfile",3)
                pm.setAttr(bmfilenode+".colorProfile",3)
                pm.setAttr(bmnode+".bumpDepth",0.002)
                pm.setAttr(nmfilenode+".fileTextureName",nortex,type="string")
                pm.setAttr(bmfilenode+".fileTextureName",heitex,type="string")
                pm.connectAttr(nmfilenode+".outAlpha",nmnode+".bumpValue")
                pm.connectAttr(bmfilenode+".outAlpha",bmnode+".bumpValue")
                pm.connectAttr(bmnode+".outNormal",nmnode+".normalCamera")
                pm.connectAttr(nmnode+".outNormal",newaishader+".normalCamera")
                if udimadj in udimvial:
                    pm.setAttr(nmfilenode+".uvTilingMode",3)
                    pm.setAttr(bmfilenode+".uvTilingMode",3)
            elif nortex in textlistspath:
                if autocbvalue==1:
                    os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(nortex,nortex[:-len(nortex.split(".")[-1])]+"tx")) 
                nmfilenode =pm.shadingNode("file",asTexture=1,name=name)
                nmptnode = pm.shadingNode("place2dTexture",asTexture=1,name=name)
                nmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
                pm.setAttr(nmnode+".bumpInterp",1)
                pm.setAttr(nmnode+".aiFlipR",0)
                pm.setAttr(nmnode+".aiFlipG",0)
                filenodebuild().builder(nmptnode,nmfilenode)
                pm.setAttr(nmfilenode+".colorProfile",3)
                pm.setAttr(nmfilenode+".fileTextureName",nortex,type="string")
                pm.connectAttr(nmfilenode+".outAlpha",nmnode+".bumpValue")
                pm.connectAttr(nmnode+".outNormal",newaishader+".normalCamera")
                if udimadj in udimvial:
                    pm.setAttr(nmfilenode+".uvTilingMode",3)
            elif heitex in textlistspath:
                bmfilenode =pm.shadingNode("file",asUtility=1,name=name)
                bmptnode = pm.shadingNode("place2dTexture",asTexture=1,name=name)
                bmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
                filenodebuild().builder(bmptnode,bmfilenode)
                pm.setAttr(bmfilenode+".colorProfile",3)
                pm.setAttr(bmnode+".bumpDepth",0.002)
                pm.setAttr(bmfilenode+".fileTextureName",heitex,type="string")
                pm.connectAttr(bmfilenode+".outAlpha",bmnode+".bumpValue")
                pm.connectAttr(bmnode+".outNormal",newaishader+".normalCamera")
                if udimadj in udimvial:
                    pm.setAttr(bmfilenode+".uvTilingMode",3)   
        else:
            print "请选择模型！！"

def spaddfile(arg):
    vail = ["png","tga","tif","jpg"]
    path = pm.textField('sptexpath',tx=1,q=1).replace("\\","/")
    if os.path.exists(path)==True:
        filelist = [i for i in pm.getFileList(fld=path) if i.split(".")[-1] in vail]
        pm.textScrollList("piclist",e=1,ra=1,a=filelist)
    else:
        print "路径错误！！",
def fleshtx(arg):
    listseledcb=pm.checkBox("seledcb" ,q=True,v=True)
    vail = ["png","tga","tif","jpg"]
    nowtime = time.localtime(time.time())
    nowtimeymd = str(nowtime[0])+str(nowtime[1])+str(nowtime[2])+str(nowtime[3])
    path =pm.textField('sptexpath',tx=1,q=1).replace("\\","/")
    invalidtx = ['roughness','Height','Normal','f0']
    if listseledcb==True:
        print"路径模式！！",
        if os.path.exists(path)==True: 
            filelist = pm.textScrollList("piclist",q=1,si=1)
            if filelist!=[]:
                for f in range(len(filelist)):
                    type = filelist[f].split(".")[-1]
                    basename = filelist[f][:-len(type)]
                    os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(path+"/"+filelist[f],path+"/"+basename+"tx"))
#                        print path+"/"+filelist[f],path+"/"+basename+"tx"
            else:
                print "列表为空，获取路径下最新修改贴图并转换为tx！！",
                filelist= pm.getFileList(fld=path)
                for f in range(len(filelist)):
                    filetime =  time.localtime(os.path.getmtime(path+"/"+filelist[f]))
                    fileymd = str(filetime[0])+str(filetime[1])+str(filetime[2])+str(filetime[3])
                    type = filelist[f].split(".")[-1]
                    basename = filelist[f][:-len(type)]
                    if fileymd ==nowtimeymd:
                        if nowtime[4]-filetime[4]<=3:
                            invalidjudge =[t for t in invalidtx if filelist[f].find(t)!=-1]
                            if invalidjudge==[]:
                                os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(path+"/"+filelist[f],path+"/"+basename+"tx"))
        else:
            print "路径不存在！！",
    else:
        print "场景模式！！",
        filelist=[]
        filesel = pm.ls(type="file")
        for a in range(len(filesel)):
            filepath  = pm.getAttr(filesel[a]+".fileTextureName")
            filemode = pm.getAttr(filesel[a]+".uvTilingMode")
            if filemode==0:
                filelist.append(filepath)
            elif filemode==3:
                filelist=[]
                orgname = os.path.basename(filepath)[:-len(os.path.basename(filepath).split(".")[-1])-6]
                dirname = os.path.dirname(filepath)
                filell =[g for g in  pm.getFileList(fld=dirname) if g.split(".")[-1] in vail]
                for e in range(len(filell)):
                    traname = os.path.basename(filell[e])[:-len(os.path.basename(filell[e]).split(".")[-1])-6]
                    if traname ==orgname:
                        filelist.append(dirname+"/"+filell[e])
                        filetime =  time.localtime(os.path.getmtime(dirname+"/"+filell[e]))
                        fileymd = str(filetime[0])+str(filetime[1])+str(filetime[2])+str(filetime[3])
                        type = os.path.basename(filell[e]).split(".")[-1]
                        basename = filell[e][:-len(type)]
                        if fileymd ==nowtimeymd:
                            if nowtime[4]-filetime[4]<=3:
                                invalidjudge =[t for t in invalidtx if filell[e].find(t)!=-1]
                                if invalidjudge==[]:
                                    os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(dirname+"/"+filell[e],dirname+"/"+basename+"tx")) 
def pathtx(arg):
    path =pm.textField('sptexpath',tx=1,q=1).replace("\\","/")
    if os.path.exists(path):
        filelist= pm.getFileList(fld=path)
        invalidtx = ['Roughness','Height','Normal','f0']
        for f in range(len(filelist)):
            type = filelist[f].split(".")[-1]
            basename = filelist[f][:-len(type)]
            invalidjudge =[t for t in invalidtx if filelist[f].find(t)!=-1]
            if invalidjudge==[]:
                os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(path+"/"+filelist[f],path+"/"+basename+"tx"))
def udimexnode(arg):
    filesel =pm.ls(sl=1,type="file")
    if filesel!=[]:
        for i in range(len(filesel)):
            filemode = pm.getAttr(filesel[i]+".uvTilingMode")
            if filemode ==3:
                pm.setAttr(filesel[i]+".uvTilingMode",0)
                baseptnode = pm.listConnections(filesel[i],d=0,type="place2dTexture")[0]
                pm.setAttr(baseptnode+".wrapU",0)
                pm.setAttr(baseptnode+".wrapV",0)
                filepath  =pm.getAttr(filesel[i]+".fileTextureName").replace("\\","/")
                type =filepath.split(".")[-1]
                adjname =os.path.basename(filepath)[:-len(type)-6]
                dirname = os.path.dirname(filepath)
                filelist = pm.getFileList(fld = dirname)
                fileseled = []
                for f in range(len(filelist)):
                    listype = filelist[f].split(".")[-1]
                    listadj = os.path.basename(filelist[f])[:-len(listype)-6]
                    if listadj == adjname:
                        fileseled.append(dirname+"/"+filelist[f])
                filenodeas = []
                for l in range(1,len(fileseled)):
                    types =fileseled[l].split(".")[-1]
                    vvalue =int(fileseled[l][:-len(types)-1][-2])
                    uvalue = int(fileseled[l][:-len(types)-1][-1])-1
                    if types!="tx":
    #                    print fileseled[l],vvalue,uvalue
                        filenode =pm.shadingNode("file",asTexture=1,name=filesel[i])
                        pm.setAttr(filenode+".fileTextureName",fileseled[l],type="string")
                        ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=filesel[i])
                        pm.setAttr(ptnode+".translateFrameU",int(uvalue))
                        pm.setAttr(ptnode+".translateFrameV",int(vvalue))
                        pm.setAttr(ptnode+".wrapU",0)
                        pm.setAttr(ptnode+".wrapV",0)
                        filenodebuild().builder(ptnode,filenode)
                        filenodeas.append(filenode)
                        fnum = len(filenodeas)
                        if fnum==1:
                            pm.connectAttr(filenodeas[fnum-1]+".outColor",filesel[i]+".defaultColor",f=1)
                        else:
                            pm.connectAttr(filenodeas[fnum-1]+".outColor",filenodeas[fnum-2]+".defaultColor",f=1)
            else:
                if pm.listConnections(filesel[i]+".defaultColor",d=0)!=[]:
                    
                    filein  = pm.listConnections(filesel[i]+".defaultColor",d=0,plugs=1)
                    pm.disconnectAttr(filein[0],filesel[i]+".defaultColor")
                    ptfile = pm.listConnections(filesel[i],d=0,type="place2dTexture")
                    pm.setAttr(ptfile[0]+".wrapU",1)
                    pm.setAttr(ptfile[0]+".wrapV",1)
                    pm.setAttr(ptfile[0]+".translateFrameU",0)
                    pm.setAttr(ptfile[0]+".translateFrameV",0)
                    pm.setAttr(filesel[i]+".uvTilingMode",3)
                    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel", "deleteUnusedNodes");') 
    else:
        print "请选择需要转换的file节点！！",
        
        
def SJ_SpShaderMakerwdUI():
    '''
    2.2更新说明：修复刷新tx的bug，修复udim与串联转换的bug，增加生成arnold材质自动生成tx的选择
    2.3更新说明：增加目标路径排除'roughness','Height','Normal','f0'贴图批量生成tx功能
    '''
    if pm.window('spshader',ex=True):
        pm.deleteUI('spshader',wnd=True)
    pm.window('spshader',t='SPshaderForMayaMakerV2.3')
    pm.columnLayout(adj=True,w=600)
    pm.text(l='一键生成spForMaya材质',fn='fixedWidthFont',h=50,annotation="2.3更新说明：增加目标路径排除'roughness','Height','Normal','f0'贴图批量生成tx功能")
    pm.textScrollList("piclist",allowMultiSelection=1)
    pm.text(l='',fn='fixedWidthFont',h=30,annotation="")
    pm.textField('sptexpath',tx="D:/test",h=30,annotation="")
    pm.button(l='获取路径下的贴图列表',c=spaddfile,bgc=[0.5,1,0.8],h=50,annotation="输入贴图路径，获取路径下的贴图，并选中贴图")
    pm.text(l='~~~~~~~~~~~~~~~~~~',fn='fixedWidthFont',h=20,annotation="")
    pm.flowLayout( columnSpacing=0)
    pm.checkBox("autocb" ,label='生成arnold材质并自动转tx',h=50,w=300,ann="不转换height，f0，specularRoughness贴图为tx")
    pm.checkBox("seledcb" ,label='切换为刷新路径\\列表模式',ann="当列表为空时，刷新路径文件夹里最新修改的贴图；当列表内已获取贴图信息时，刷新列表中选中的贴图为tx！！",h=50,w=150,ed=1)
    pm.setParent( '..' )
    pm.flowLayout( columnSpacing=0)
    pm.button(l='生成arnold材质',c=arnoldspshmaker,bgc=[1,0.5,0.5],h=50,annotation="选择列表中的贴图名字，点击确定生成arnold材质球",w=300)
    pm.button(l='刷新贴图为tx',c=fleshtx,bgc=[1,0.5,0.5],h=50,annotation=" 默认刷新三分钟内修改的贴图tx",w=300)
    pm.setParent( '..' )
    pm.button(l='刷新目标路径的tx',c=pathtx,bgc=[1,0.5,0.5],h=50,annotation=" 默认不对Roughness，f0，Normal，Height这四种贴图进行tx转换",w=300)
    pm.button(l='选择列表中的贴图名字，生成vray材质',c=vrayspshmaker,bgc=[1,1,0.5],h=50,annotation="点击确定生成vray材质球")
    pm.text(l='~~~~~~~~~~~~~~~~~~',fn='fixedWidthFont',h=20,annotation="")
    pm.button(l='多uv材质udim模式与串联式节点互转',c=udimexnode,bgc=[0.8,0.6,0.8],h=50,annotation=" 选择需要转换的file节点，点击确定；当file节点为udim模式时则转换为节点串联模式，反之亦然")
    pm.showWindow()

