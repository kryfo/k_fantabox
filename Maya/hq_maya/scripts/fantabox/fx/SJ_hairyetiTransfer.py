#coding=utf-8
import pymel.core as pm
import maya.mel as mel
import os
import maya.cmds as cmds
def yeticonnectAttr(typename,yetishapesr,yetishapetr):
    yetinodes=[]
    if yetishapesr!=[] and yetishapetr!=[]:
        yeticonnects = yetishapesr.listConnections(c=1,type=typename,plugs=1)
        if yeticonnects!=[]:
            for yeticonnect in yeticonnects:
                yeticonnectsr = yeticonnect[0]
                yeticonnecttr = yeticonnect[1]
                yetinode = yeticonnect[1].split(".")[0]
                pm.connectAttr( yeticonnectsr.replace(str(yetishapesr),str(yetishapetr)),yeticonnecttr,f=1)
                if pm.nodeType(yetinode)=="pgYetiMaya":
                    yetiimps = pm.pgYetiGraph(yetinode,listNodes=True,type="import") 
                    if yetiimps!=[]:
                        for yetiimp in yetiimps:
                            if pm.pgYetiGraph(yetinode,node=yetiimp,param="type",getParamValue=1)==0:
                                pm.pgYetiGraph(yetinode,node=yetiimp,param="geometry",setParamValueString=yetishapetr.split("|")[-1].split(":")[-1])
                yetinodes.append(yetinode)
    return yetinodes

def grmrebuild(grmsels,trmesh):
    if grmsels!=[]:
        for grmsel in grmsels:
            adj = pm.objExists(grmsel+"Shape_strand_set")
            if adj:
                pm.delete(grmsel+"Shape_strand_set")
            pm.pgYetiCommand(pm.listRelatives(grmsel,c=1),convertToCurves=1)
            grmset = cmds.ls(grmsel+"Shape_strand_set")
            grmcvs = cmds.listConnections(grmset[0],d=1)
            delcvgrps = pm.group(grmcvs)
            newset = cmds.sets(grmcvs,n=grmsel+"_set")
            newgrm = pm.createNode("pgYetiGroom")
            pm.rename(newgrm.getParent(),trmesh.getParent().replace(":","_")+"_grm")
            pm.rename(newgrm,trmesh.getParent().replace(":","_")+"_grmShape")
            pm.connectAttr(trmesh+".worldMesh[0]",newgrm+".inputGeometry",f=1)
            yetitarattrs = grmsel.getShape().listConnections(s=0,type="pgYetiMaya",plugs=1)
            for yetitarattr  in yetitarattrs:
                pm.connectAttr(newgrm+ ".outputData" ,yetitarattr,f=1)
            pm.connectAttr("time1.outTime",newgrm+".currentTime",f=1)
            pm.pgYetiCommand(newgrm,convertFromCurves=newset,inputGeometry=trmesh,stepSize=0.001)
            yetinodesrs = trmesh.listConnections(s=0,type="pgYetiMaya")
            for yetinodesr in yetinodesrs:
                yetiimps = pm.pgYetiGraph(yetinodesr,listNodes=True,type="import")
                if yetiimps!=[]:
                    for yetiimp in yetiimps:
                        if pm.pgYetiGraph(yetinodesr,node=yetiimp,param="type",getParamValue=1)==1:
                            pm.pgYetiGraph(yetinodesr,node=yetiimp,param="geometry",setParamValueString=newgrm.split(":")[-1])
            pm.delete(delcvgrps)
            return newgrm

def yetitransfer(yetimeshsrs,yetimeshtrs):
    try:
        yetishapesrs = yetimeshsrs.getShape()
        yetishapetrs = yetimeshtrs.getShape()
    except:
        yetishapesrs=[]
        yetishapetrs=[]
        cmds.warning(str(yetishapesrs)+"'s shapeNode is not exists!!")
    #sruvset = pm.polyUVSet(yetishapesrs,q=1,currentUVSet=1)[0]
    #truvset = pm.polyUVSet(yetishapetrs,q=1,currentUVSet=1)[0]
    pm.transferAttributes(yetishapetrs,yetishapesrs,transferPositions=1,transferNormals=1,transferUVs=0,transferColors=0,sampleSpace=3,sourceUvSpace='map1',targetUvSpace='map1',searchMethod=3,flipUVs=0,colorBorders=1)
    yetinodecol = yeticonnectAttr("pgYetiMaya",yetishapesrs,yetishapetrs)
    grmsels= yetishapesrs.listConnections(s=0,type="pgYetiGroom")
    grmcols = grmrebuild(grmsels,yetishapetrs)
    pm.select(yetimeshtrs,r=1)
    if pm.objExists(yetimeshtrs+"_reference")==True:
        pm.delete(yetimeshtrs+"_reference")
    try:
        mel.eval("CreateTextureReferenceObject")
    except:
        pass
    refmesh = cmds.listConnections(yetishapetrs+".referenceObject",d=0,type="mesh")
    pm.group(yetinodecol,grmcols,refmesh,name=str(yetimeshtrs.split(":")[-1])+"_yeti_G")

def hairtransfer(hairsrmesh,hairtrmesh):
    hairsyssels=[]
    filename =os.path.basename( cmds.file(expandName=1,q=1)).split(".")[0]
    hairwhole = pm.group(em=1,name=filename+"_hair_G")
    folwhole = pm.group(em=1,name=filename+"_fols_G")
    cvswhole = pm.group(em=1,name=filename+"_outputCvs_G")
    pfxwhole = pm.group(em=1,name=filename+"_pfxHairs_G")
    try:
        hairShapesr =  hairsrmesh.getShape()
        hairShapetr =  hairtrmesh.getShape()
    except:
        hairShapesr=[]
        hairShapetr=[]
        pm.warning(selsrs[i]+"'s shapeNode is not exists!!")
    follicles =  pm.listConnections(hairShapesr,s=0,type="follicle")
    if follicles!=None:
        for follicle in follicles:
            follicleshape =  follicle.getShape()
            hairsyssel = pm.listConnections( follicleshape+".outHair",s=0,type="hairSystem")[0]
            if hairsyssel not in hairsyssels:
                hairsyssels.append(hairsyssel)
                pfxhairsel = pm.listConnections( hairsyssel+".outputRenderHairs",s=0,type="pfxHair")[0]
                pm.parent(pfxhairsel,pfxwhole)
                folliclesels = pm.listConnections( hairsyssel+".inputHair",d=0)
                cvs = [pm.listConnections(a+".outCurve",s=0)[0] for a in folliclesels]
                for cv in cvs:
                    cvsconnects= pm.listConnections(cv.getShape(),c=1,plugs=1)[0]
                    pm.disconnectAttr(cvsconnects[1],cvsconnects[0])
                cvsgrp =pm.group(cvs,name=str(hairsyssel)+"_cvs_g")
                pm.select(hairtrmesh,r=1)
                pm.select(cvsgrp,tgl=1)
                mel.eval('makeCurvesDynamic 2 { "1", "1", "1", "1", "1"};')
                newfollicles = [b.getParent() for b in cvs if b.getParent().getShape()!=None]
                newcvs = [pm.listConnections(a+".outCurve",s=0)[0] for a in newfollicles ]
                oldhairsys =[pm.listConnections(a.getShape()+".outHair",s=0,type="hairSystem")[0] for a in newfollicles]
                oldhairsys = list(set(oldhairsys))
                nucleussels =[pm.listConnections(a.getShape(),s=0,type="nucleus")[0] for a in oldhairsys]
                nucleussels = list(set(nucleussels))
                pm.delete(oldhairsys,nucleussels)
                pm.select(newfollicles,r=1)
                mel.eval('assignHairSystem %s'%(hairsyssel))
                try:
                    pm.parent(hairsyssel+"Follicles",folwhole)
                    
                    pm.parent(hairsyssel+"OutputCurves",cvswhole)
                    pm.setAttr(hairsyssel+"OutputCurves.visibility",0)
                except:
                    pm.warning('cant not parent Follicles and OutputCurves group!!')
    hairsystrsgrp = pm.group(hairsyssels,name = filename+"_hairSystems_G")      
    pm.parent(pfxwhole,hairwhole)       
    pm.parent(hairsystrsgrp,hairwhole)
    pm.setAttr(hairsystrsgrp+".visibility",0)
    pm.parent(folwhole,hairwhole)
    pm.setAttr(folwhole+".visibility",0)
    pm.parent(cvswhole,hairwhole)
    pm.setAttr(cvswhole+".visibility",0)

def hairyetitransfer_main():
    '''
    {'load':'maya_fur','defaultOption':1,'CNname':'一键传递hair或yeti毛发'}
    '''
    sels=pm.ls(sl=1)
    selsrs = sels[:len(sels)/2]
    seltrs = sels[len(sels)/2:]
    for i in range(len(selsrs)):
        try:
            hairShapesr =  selsrs[i].getShape()
            hairShapetr =  seltrs[i].getShape()
        except:
            hairShapesr=[]
            hairShapetr=[]
            pm.warning(selsrs[i]+"'s shapeNode is not exists!!")
        if hairShapesr!=[] and hairShapetr!=[]:
            hairadj =  pm.listConnections(hairShapesr,s=0,type="follicle")
            yetiadj= pm.listConnections(hairShapesr,s=0,type="pgYetiMaya")
            if hairadj!=[]:
                hairtransfer(selsrs[i],seltrs[i])
            elif yetiadj!=[]:
                yetitransfer(selsrs[i],seltrs[i])