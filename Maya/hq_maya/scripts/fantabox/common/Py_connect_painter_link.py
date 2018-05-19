#coding=utf-8
import maya.mel as mel
import pymel.core as pm
import os  
def Py_connect_painter_link_main():
    SJ_SP_texpath = mel.eval("$temp=$SJ_SP_texpath")
    SJ_SP_filetyp = mel.eval("$temp=$SJ_SP_filet =$SJ_SP_filetyp")
    SJ_SP_tx = mel.eval("$temp=$SJ_SP_tx")
    SJ_SP_mats = mel.eval("$temp=$SJ_SP_mats")
    SJ_SP_rndr = mel.eval("$temp=$SJ_SP_rndr")
    SJ_SP_matlists=SJ_SP_mats.split("|")
    texpath = os.path.dirname(SJ_SP_texpath)
    SJ_meshName = os.path.splitext(os.path.basename(SJ_SP_texpath))[0]
    print texpath,SJ_meshName,SJ_SP_filetyp,SJ_SP_tx,SJ_SP_mats,SJ_SP_rndr
    arnoldspshmaker(texpath,SJ_meshName,SJ_SP_matlists,SJ_SP_filetyp,SJ_SP_tx,SJ_SP_rndr)
def arnoldspshmaker(path,meshName,texSets,fileType,autocbvalue,mattype):
    pm.arnoldFlushCache( textures=True )
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    udimlists = list(set(texSets)&set(udimvial))
    if udimlists==[]:
        for texSet in texSets:
            if pm.objExists(texSet)==True:
                shader =pm.listConnections(texSet+".aiSurfaceShader",d=0)
                if shader == []:
                    shader =pm.listConnections(texSet+".surfaceShader",d=0)
                pm.hyperShade(o=shader[0])
                mesh = pm.ls(sl=1,r=1)
                if mattype.find("ARNOLD4(aistandard)")!=-1:
                    Aishaderfunc(path,meshName,texSet,"."+fileType,autocbvalue,mesh)
                elif mattype.find("Arnold4(AlSurface)")!=-1:
                    Alshaderfunc(path,meshName,texSet,"."+fileType,autocbvalue,mesh)
            else:
                mesh=[]
                if mattype.find("ARNOLD4(aistandard)")!=-1:
                    Aishaderfunc(path,meshName,texSet,"."+fileType,autocbvalue,mesh)
                elif mattype.find("Arnold4(AlSurface)")!=-1:
                    Alshaderfunc(path,meshName,texSet,"."+fileType,autocbvalue,mesh)
    else:
        sel =pm.ls(sl=1,type="transform")
        if sel!=[]:
            mesh = [a for a in sel if pm.nodeType(a.getShape())=="mesh"]
            if mesh!=[]:
                if mattype.find("ARNOLD4(aistandard)")!=-1:
                    Aishaderfunc(path,meshName,texSets[0],"."+fileType,autocbvalue,mesh)
                elif mattype.find("Arnold4(AlSurface)")!=-1:
                    Alshaderfunc(path,meshName,texSets[0],"."+fileType,autocbvalue,mesh)
            else:
                pm.warning("请选择模型！！")
def maketx(dirname,name,texudim,type):
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    if texudim in udimvial:
        dirlists = [a for a in os.listdir(dirname) if a.find(name)!=-1]
        for dirlist in dirlists:
            os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(dirname+"/"+dirlist,dirname+"/"+os.path.splitext(dirlist)[0]+".tx")) 
    else:
        os.system("maketx -v -u --oiio --checknan --filter lanczos3 %s -o %s" %(dirname+"/"+name+type,dirname+"/"+name+".tx")) 

def filenodebuild(ptnode,filenode):
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
def setconnect(name,texsetname,texpaths,newshaderAttr,mode="common",texpaths2=""):
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    filenode =pm.shadingNode("file",asTexture=1,name=name)
    ptnode = pm.shadingNode("place2dTexture",asUtility=1,name=name)
    filenodebuild(ptnode,filenode)
    pm.setAttr(filenode+".colorProfile",3)
    pm.setAttr(filenode+".fileTextureName",texpaths,type="string")
    if texsetname in udimvial:
        pm.setAttr(filenode+".uvTilingMode",3)
    if mode=="common":
        pm.connectAttr(filenode+".outColor",newshaderAttr)
    elif mode == "gamma":
        gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
        pm.setAttr(gammanode+".gammaX",2.2)
        pm.setAttr(gammanode+".gammaY",2.2)
        pm.setAttr(gammanode+".gammaZ",2.2)
        pm.setAttr(filenode+".alphaIsLuminance",1)
        #pm.connectAttr(filenode+".outColor",gammanode+".value")
        pm.connectAttr(filenode+".outAlpha",gammanode+".valueX")
        pm.connectAttr(gammanode+".outValueX",newshaderAttr)
    elif mode =="normal":
        nmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
        pm.setAttr(nmnode+".bumpInterp",1)
        pm.setAttr(nmnode+".aiFlipR",0)
        pm.setAttr(nmnode+".aiFlipG",0)
        pm.connectAttr(filenode+".outAlpha",nmnode+".bumpValue")
        pm.connectAttr(nmnode+".outNormal",newshaderAttr)
    elif mode =="bump":
        bmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
        pm.setAttr(bmnode+".bumpDepth",0.010)
        pm.connectAttr(filenode+".outAlpha",bmnode+".bumpValue")
        pm.connectAttr(bmnode+".outNormal",newshaderAttr)
    elif mode =="bumpNormal":
        filenode2 =pm.shadingNode("file",asTexture=1,name=name)
        ptnode2 = pm.shadingNode("place2dTexture",asUtility=1,name=name)
        filenodebuild(ptnode2,filenode2)
        pm.setAttr(filenode2+".colorProfile",3)
        pm.setAttr(filenode2+".fileTextureName",texpaths2,type="string")

        nmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
        pm.setAttr(nmnode+".bumpInterp",1)
        pm.setAttr(nmnode+".aiFlipR",0)
        pm.setAttr(nmnode+".aiFlipG",0)

        bmnode =pm.shadingNode("bump2d",asUtility=1,name=name)
        pm.setAttr(bmnode+".bumpDepth",0.010)
       
        pm.connectAttr(filenode+".outAlpha",nmnode+".bumpValue")
        pm.connectAttr(filenode2+".outAlpha",bmnode+".bumpValue")
        pm.connectAttr(bmnode+".outNormal",nmnode+".normalCamera")
        pm.connectAttr(nmnode+".outNormal",newshaderAttr)
    elif mode=="metal":
        gammanode =pm.shadingNode("gammaCorrect",asUtility=1,name=name)
        pm.setAttr(gammanode+".gammaX",2.2)
        pm.setAttr(gammanode+".gammaY",2.2)
        pm.setAttr(gammanode+".gammaZ",2.2)
        pm.setAttr(filenode+".alphaIsLuminance",1)
        #pm.connectAttr(filenode+".outColor",gammanode+".value")
        setRangenode =pm.shadingNode("setRange",asUtility=1,name=name)
        pm.setAttr(setRangenode+".minX",1.5)
        pm.setAttr(setRangenode+".maxX",20)
        pm.setAttr(setRangenode+".oldMaxX",1)

        pm.connectAttr(filenode+".outColorR",setRangenode+".valueX")
        pm.connectAttr(setRangenode+".outValueX",gammanode+".valueX")
        pm.connectAttr(gammanode+".outValueX",newshaderAttr)

def Aishaderfunc(dirname,meshname,texsetname,type,autocbvalue,mesh):
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    if texsetname not in udimvial:
        basename = meshname+"_"+texsetname
        diftex =  dirname+"/"+ basename+"_Diffuse"+type
        f0tex =  dirname+"/"+ basename+"_f0"+type
        nortex =  dirname+"/"+ basename+"_Normal"+type
        heitex =  dirname+"/"+ basename+"_Height"+type
        routex =  dirname+"/"+ basename+"_Roughness"+type
        spetex =  dirname+"/"+ basename+"_Specular"+type
        name = texsetname.replace("matSG","part")+"_AS"
    else:
        basename = meshname
        diftex =  dirname+"/"+ basename+"_Diffuse"+"_"+texsetname+type
        f0tex =  dirname+"/"+ basename+"_f0"+"_"+texsetname+type
        nortex =  dirname+"/"+ basename+"_Normal"+"_"+texsetname+type
        heitex =  dirname+"/"+ basename+"_Height"+"_"+texsetname+type
        routex =  dirname+"/"+ basename+"_Roughness"+"_"+texsetname+type
        spetex =  dirname+"/"+ basename+"_Specular"+"_"+texsetname+type
        name = meshname+"_AS"
    if pm.objExists(name)!=True:
        newaishader = pm.shadingNode("aiStandard",asShader=1,name=name)
        pm.setAttr(newaishader+".Ks",1)
        pm.setAttr(newaishader+".Kd",1)
        pm.setAttr(newaishader+".specularDistribution",1)
        pm.setAttr(newaishader+".specularFresnel",1)
        if mesh!=[]:
            pm.select(mesh,r=1)
            pm.hyperShade(assign=newaishader)
        if os.path.exists(diftex)==True:
            if autocbvalue=="1":
                maketx(dirname,basename+"_Diffuse",texsetname,type)
            setconnect(name,texsetname,diftex,newaishader+".color","common")
        if os.path.exists(spetex)==True:
            if autocbvalue=="1":
                maketx(dirname,basename+"_Specular",texsetname,type)
            setconnect(name,texsetname,spetex,newaishader+".KsColor","common")
        if os.path.exists(routex)==True:
            setconnect(name,texsetname,routex,newaishader+".specularRoughness","gamma")
        if os.path.exists(f0tex)==True:
            setconnect(name,texsetname,f0tex,newaishader+".Ksn","gamma")
        if os.path.exists(nortex)==True and os.path.exists(heitex)==True:
            setconnect(name,texsetname,nortex,newaishader+".normalCamera","bumpNormal",heitex)
        elif os.path.exists(heitex)==False:
            setconnect(name,texsetname,nortex,newaishader+".normalCamera","normal")
        else:
            setconnect(name,texsetname,heitex,newaishader+".normalCamera","bump")
    else:
        print "updateMat",
        pm.arnoldFlushCache( textures=True )
        maketx(dirname,basename+"_Diffuse",texsetname,type)
        maketx(dirname,basename+"_Specular",texsetname,type)


def Alshaderfunc(dirname,meshname,texsetname,type,autocbvalue,mesh):
    udimvial =["1001","1002","1003","1004","1005","1006","1007","1008","1009","1011","1012","1013","1014","1015","1016","1017","1018","1019"]
    if texsetname not in udimvial:
        basename = meshname+"_"+texsetname
        diftex =  dirname+"/"+ basename+"_Diffuse"+type
        metaltex =  dirname+"/"+ basename+"_metal"+type
        nortex =  dirname+"/"+ basename+"_Normal"+type
        heitex =  dirname+"/"+ basename+"_Height"+type
        routex =  dirname+"/"+ basename+"_Roughness"+type
        spetex =  dirname+"/"+ basename+"_Specular"+type
        name = texsetname.replace("matSG","part")+"_AS"
    else:
        basename = meshname
        diftex =  dirname+"/"+ basename+"_Diffuse"+"_"+texsetname+type
        metaltex =  dirname+"/"+ basename+"_metal"+"_"+texsetname+type
        nortex =  dirname+"/"+ basename+"_Normal"+"_"+texsetname+type
        heitex =  dirname+"/"+ basename+"_Height"+"_"+texsetname+type
        routex =  dirname+"/"+ basename+"_Roughness"+"_"+texsetname+type
        spetex =  dirname+"/"+ basename+"_Specular"+"_"+texsetname+type
        name = meshname+"_AS"
    #print diftex,metaltex,os.path.exists(diftex)
    #name = basename+"_AS"
    if pm.objExists(name)!=True:
        newaishader = pm.shadingNode("alSurface",asShader=1,name=name)
        pm.setAttr(newaishader+".specular1Distribution",1)
        if mesh!=[]:
            pm.select(mesh,r=1)
            pm.hyperShade(assign=newaishader)
        if os.path.exists(diftex)==True:
            if autocbvalue=="1":
                maketx(dirname,basename+"_Diffuse",texsetname,type)
            setconnect(name,texsetname,diftex,newaishader+".diffuseColor","common")
        if os.path.exists(spetex)==True:
            if autocbvalue=="1":
                maketx(dirname,basename+"_Specular",texsetname,type)
            setconnect(name,texsetname,spetex,newaishader+".specular1Color","common")
        if os.path.exists(routex)==True:
            setconnect(name,texsetname,routex,newaishader+".specular1Roughness","gamma")
        if os.path.exists(metaltex)==True:
            setconnect(name,texsetname,metaltex,newaishader+".specular1Ior","metal")
        if os.path.exists(nortex)==True and os.path.exists(heitex)==True:
            setconnect(name,texsetname,nortex,newaishader+".normalCamera","bumpNormal",heitex)
        elif os.path.exists(heitex)==False:
            setconnect(name,texsetname,nortex,newaishader+".normalCamera","normal")
        else:
            setconnect(name,texsetname,heitex,newaishader+".normalCamera","bump")
    else:
        print "updateMat",
        pm.arnoldFlushCache( textures=True )
        maketx(dirname,basename+"_Diffuse",texsetname,type)
        maketx(dirname,basename+"_Specular",texsetname,type)
