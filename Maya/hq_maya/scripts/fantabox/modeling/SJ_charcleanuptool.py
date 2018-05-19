#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm  
import mtoa.aovs as aovs
def grp_proc(nodecols,charname,father=None,num=None):    
    if nodecols!=[]:
        typeName =  nodecols[0].getShape().type()
        if typeName == "transform":
            typeName =  nodecols[1].getShape().type()
        grpName =pm.group(nodecols)
        if father==None:
            lastname = "_G" 
            pm.parent(grpName,w=1)
        else:
            lastname = "_g" 
            pm.parent(grpName,father)
        if num ==None:
            pm.rename(grpName,charname+"_"+typeName+"_G")
        else:
            pm.rename(grpName,charname+"_"+typeName+"_G"+str(num+1))
        grpchild = pm.listRelatives(grpName,c=1) 
        for g in range(len(grpchild)): 
            if num ==None:  
                pm.rename(grpchild[g],charname+"_"+typeName+str(g+1))   
                pm.rename(grpchild[g].getShape(),charname+"_"+typeName+str(g+1)+"Shape")
            else:
                pm.rename(grpchild[g],charname+"_"+typeName+lastname+str(num+1)+"_fol"+str(g+1))   
                pm.rename(grpchild[g].getShape(),charname+"_"+typeName+lastname+str(num+1)+"_fol"+str(g+1)+"Shape")
        return grpName
def judgeName(name):
    if pm.objExists(name)==True:
        pm.rename(name,name+"_old")
def redobj(arg):
    nodetyp = ["aiStandard","aiSkin","layeredShader","aiHair","alHair","alLayer","alSurface"]
    notype = ["nurbsCurve","follicle","transform"]
    mtsel = cmds.ls(mat=1)
    objsel = cmds.ls(sl=True,typ="transform")
    shadernum = []
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel)
        flsel = cmds.ls(obj2shape,type=notype)
        obj2shapes =  list(set(obj2shape).difference(set(flsel)))
        for o in range(len(obj2shapes)):
            nhairshape = cmds.ls(obj2shapes[o],type="pfxHair")
            if nhairshape!=[]:
                for a in range(len(nhairshape)):
                    nhairsys =  cmds.listConnections(nhairshape[a]+".renderHairs")
                    if nhairsys!=None:
                        nhairsysshapes = cmds.listRelatives(nhairsys)
                        nhairshader = cmds.listConnections(nhairsysshapes[0]+".aiHairShader")
                        if nhairshader!=None:
                            myWT = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(myWT + '.shadeMode',2)
                            cmds.setAttr(myWT + '.color', 1, 0, 0, type="double3")
                            myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                            cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                            myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(myWT2 + '.shadeMode',2)
                            cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                            cmds.connectAttr( nhairshader[0] + '.outColor', myWC + '.beauty', f=True )
                            cmds.connectAttr(myWT2+".outColor",nhairsysshapes[0]+".aiHairShader",f=1)
                            shadernum.append(myWT2)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        myWT = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT + '.shadeMode',2)
                        cmds.setAttr(myWT + '.color', 1, 0, 0, type="double3")
                        myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                        myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT2 + '.shadeMode',2)
                        cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                        cmds.connectAttr( shaveshader[0] + '.outColor', myWC + '.beauty', f=True )
                        cmds.connectAttr(myWT2+".outColor",shaveshape[0]+".aiHairShader",f=1)
                        shadernum.append(myWT2)
                        
                else:
                    shapes2SG = cmds.listConnections(obj2shapes[o],s=0,type='shadingEngine')
                    if shapes2SG!=None:
                        if shapes2SG[0]!="initialShadingGroup":
                            SG2sel = cmds.listConnections(shapes2SG,d=0)
                            SG2Ai = [i for i in mtsel if i in SG2sel]
                            SG2AiRe = [i for i in list(set(SG2Ai)) if cmds.nodeType(i)!="displacementShader"]
                            for i in range(0,len(SG2AiRe)):    
                                myWT = cmds.shadingNode('aiUtility', asShader=True)
                                cmds.setAttr(myWT + '.shadeMode',2)
                                cmds.setAttr(myWT + '.color', 1, 0, 0, type="double3")
                                myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                                cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                                myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                                cmds.setAttr(myWT2 + '.shadeMode',2)
                                cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                                cmds.connectAttr( SG2AiRe[i] + ('.outColor'), myWC + '.beauty', f=True )
                                objselShape = cmds.listConnections( SG2AiRe[i], s=True,t='shadingEngine' )
                                cmds.connectAttr( myWT2 + '.outColor', objselShape[0] + '.surfaceShader', f=True )
                                shadernum.append(myWT2)
    shadersel = cmds.ls(sl=True,ext=nodetyp)
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            hairsadj=cmds.listConnections(shadersel[i]+".outColor",type="hairSystem" )  
            if hairsadj!=None:
                for h in range(len(hairsadj)):
                    myWTs = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWTs + '.shadeMode',2)
                    cmds.setAttr(myWTs + '.color', 1, 0, 0, type="double3")
                    myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                    myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWT2s + '.shadeMode',2)
                    cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                    cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                    cmds.connectAttr( myWT2s + '.outColor', hairsadj[h] + '.aiHairShader', f=True )
                    shadernum.append(myWT2s)
            else:
                shaveadj=cmds.listConnections(shadersel[i]+".outColor",type="shaveHair" )  
                if shaveadj!=None:
                    for s in range(len(shaveadj)):
                        myWTs = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWTs + '.shadeMode',2)
                        cmds.setAttr(myWTs + '.color', 1, 0, 0, type="double3")
                        myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                        myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT2s + '.shadeMode',2)
                        cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                        cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                        cmds.connectAttr( myWT2s + '.outColor', shaveadj[s] + '.aiHairShader', f=True )
                        shadernum.append(myWT2s)
                else:
                    myWTs = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWTs + '.shadeMode',2)
                    cmds.setAttr(myWTs + '.color', 1, 0, 0, type="double3")
                    myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                    myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWT2s + '.shadeMode',2)
                    cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                    cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                    shaderselShape = cmds.listConnections( shadersel[i], s=True,t='shadingEngine' )
                    cmds.connectAttr( myWT2s + '.outColor', shaderselShape[0] + '.surfaceShader', f=True )
                    shadernum.append(myWT2s)
    if shadersel ==[] and objsel==[]:
        cmds.warning("û��ѡ��ģ�ͻ����")
    if shadernum!=None:
        print "������"+str(len(shadernum))+"��ID \n",
def greenobj(arg):
    nodetyp = ["aiStandard","aiSkin","layeredShader","aiHair","alHair","alLayer","alSurface"]
    notype = ["nurbsCurve","follicle","transform"]
    mtsel = cmds.ls(mat=1)
    objsel = cmds.ls(sl=True,typ="transform")
    shadernum = []
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel)
        flsel = cmds.ls(obj2shape,type=notype)
        obj2shapes =  list(set(obj2shape).difference(set(flsel)))
        for o in range(len(obj2shapes)):
            nhairshape = cmds.ls(obj2shapes[o],type="pfxHair")
            if nhairshape!=[]:
                for a in range(len(nhairshape)):
                    nhairsys =  cmds.listConnections(nhairshape[a]+".renderHairs")
                    if nhairsys!=None:
                        nhairsysshapes = cmds.listRelatives(nhairsys)
                        nhairshader = cmds.listConnections(nhairsysshapes[0]+".aiHairShader")
                        if nhairshader!=None:
                            myWT = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(myWT + '.shadeMode',2)
                            cmds.setAttr(myWT + '.color', 0, 1, 0, type="double3")
                            myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                            cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                            myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(myWT2 + '.shadeMode',2)
                            cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                            cmds.connectAttr( nhairshader[0] + '.outColor', myWC + '.beauty', f=True )
                            cmds.connectAttr(myWT2+".outColor",nhairsysshapes[0]+".aiHairShader",f=1)
                            shadernum.append(myWT2)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        myWT = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT + '.shadeMode',2)
                        cmds.setAttr(myWT + '.color', 0, 1, 0, type="double3")
                        myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                        myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT2 + '.shadeMode',2)
                        cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                        cmds.connectAttr( shaveshader[0] + '.outColor', myWC + '.beauty', f=True )
                        cmds.connectAttr(myWT2+".outColor",shaveshape[0]+".aiHairShader",f=1)
                        shadernum.append(myWT2)
                        
                else:
                    shapes2SG = cmds.listConnections(obj2shapes[o],s=0,type='shadingEngine')
                    if shapes2SG!=None:
                        if shapes2SG[0]!="initialShadingGroup":
                            SG2sel = cmds.listConnections(shapes2SG,d=0)
                            SG2Ai = [i for i in mtsel if i in SG2sel]
                            SG2AiRe = [i for i in list(set(SG2Ai)) if cmds.nodeType(i)!="displacementShader"]
                            for i in range(0,len(SG2AiRe)):    
                                myWT = cmds.shadingNode('aiUtility', asShader=True)
                                cmds.setAttr(myWT + '.shadeMode',2)
                                cmds.setAttr(myWT + '.color', 0, 1, 0, type="double3")
                                myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                                cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                                myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                                cmds.setAttr(myWT2 + '.shadeMode',2)
                                cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                                cmds.connectAttr( SG2AiRe[i] + ('.outColor'), myWC + '.beauty', f=True )
                                objselShape = cmds.listConnections( SG2AiRe[i], s=True,t='shadingEngine' )
                                cmds.connectAttr( myWT2 + '.outColor', objselShape[0] + '.surfaceShader', f=True )
                                shadernum.append(myWT2)
    shadersel = cmds.ls(sl=True,ext=nodetyp)
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            hairsadj=cmds.listConnections(shadersel[i]+".outColor",type="hairSystem" )  
            if hairsadj!=None:
                for h in range(len(hairsadj)):
                    myWTs = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWTs + '.shadeMode',2)
                    cmds.setAttr(myWTs + '.color', 0, 1, 0, type="double3")
                    myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                    myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWT2s + '.shadeMode',2)
                    cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                    cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                    cmds.connectAttr( myWT2s + '.outColor', hairsadj[h] + '.aiHairShader', f=True )
                    shadernum.append(myWT2s)
            else:
                shaveadj=cmds.listConnections(shadersel[i]+".outColor",type="shaveHair" )  
                if shaveadj!=None:
                    for s in range(len(shaveadj)):
                        myWTs = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWTs + '.shadeMode',2)
                        cmds.setAttr(myWTs + '.color', 0, 1, 0, type="double3")
                        myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                        myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT2s + '.shadeMode',2)
                        cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                        cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                        cmds.connectAttr( myWT2s + '.outColor', shaveadj[s] + '.aiHairShader', f=True )
                        shadernum.append(myWT2s)
                else:
                    myWTs = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWTs + '.shadeMode',2)
                    cmds.setAttr(myWTs + '.color', 0, 1, 0, type="double3")
                    myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                    myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWT2s + '.shadeMode',2)
                    cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                    cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                    shaderselShape = cmds.listConnections( shadersel[i], s=True,t='shadingEngine' )
                    cmds.connectAttr( myWT2s + '.outColor', shaderselShape[0] + '.surfaceShader', f=True )
                    shadernum.append(myWT2s)
    if shadersel ==[] and objsel==[]:
        cmds.warning("û��ѡ��ģ�ͻ����")
    if shadernum!=None:
        print "������"+str(len(shadernum))+"��ID\n",
def blueobj(arg):
    nodetyp = ["aiStandard","aiSkin","layeredShader","aiHair","alHair","alLayer","alSurface"]
    notype = ["nurbsCurve","follicle","transform"]
    mtsel = cmds.ls(mat=1)
    objsel = cmds.ls(sl=True,typ="transform")
    shadernum = []
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel)
        flsel = cmds.ls(obj2shape,type=notype)
        obj2shapes =  list(set(obj2shape).difference(set(flsel)))
        for o in range(len(obj2shapes)):
            nhairshape = cmds.ls(obj2shapes[o],type="pfxHair")
            if nhairshape!=[]:
                for a in range(len(nhairshape)):
                    nhairsys =  cmds.listConnections(nhairshape[a]+".renderHairs")
                    if nhairsys!=None:
                        nhairsysshapes = cmds.listRelatives(nhairsys)
                        nhairshader = cmds.listConnections(nhairsysshapes[0]+".aiHairShader")
                        if nhairshader!=None:
                            myWT = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(myWT + '.shadeMode',2)
                            cmds.setAttr(myWT + '.color', 0, 0, 1, type="double3")
                            myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                            cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                            myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(myWT2 + '.shadeMode',2)
                            cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                            cmds.connectAttr( nhairshader[0] + '.outColor', myWC + '.beauty', f=True )
                            cmds.connectAttr(myWT2+".outColor",nhairsysshapes[0]+".aiHairShader",f=1)
                            shadernum.append(myWT2)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        myWT = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT + '.shadeMode',2)
                        cmds.setAttr(myWT + '.color', 0, 0, 1, type="double3")
                        myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                        myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT2 + '.shadeMode',2)
                        cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                        cmds.connectAttr( shaveshader[0] + '.outColor', myWC + '.beauty', f=True )
                        cmds.connectAttr(myWT2+".outColor",shaveshape[0]+".aiHairShader",f=1)
                        shadernum.append(myWT2)
                        
                else:
                    shapes2SG = cmds.listConnections(obj2shapes[o],s=0,type='shadingEngine')
                    if shapes2SG!=None:
                        if shapes2SG[0]!="initialShadingGroup":
                            SG2sel = cmds.listConnections(shapes2SG,d=0)
                            SG2Ai = [i for i in mtsel if i in SG2sel]
                            SG2AiRe = [i for i in list(set(SG2Ai)) if cmds.nodeType(i)!="displacementShader"]
                            for i in range(0,len(SG2AiRe)):    
                                myWT = cmds.shadingNode('aiUtility', asShader=True)
                                cmds.setAttr(myWT + '.shadeMode',2)
                                cmds.setAttr(myWT + '.color', 0, 0, 1, type="double3")
                                myWC = cmds.shadingNode('aiWriteColor', asShader=True)
                                cmds.connectAttr( myWT + '.outColor', myWC + '.input', f=True )
                                myWT2 = cmds.shadingNode('aiUtility', asShader=True)
                                cmds.setAttr(myWT2 + '.shadeMode',2)
                                cmds.connectAttr( myWC + '.outColor', myWT2 + '.color', f=True )
                                cmds.connectAttr( SG2AiRe[i] + ('.outColor'), myWC + '.beauty', f=True )
                                objselShape = cmds.listConnections( SG2AiRe[i], s=True,t='shadingEngine' )
                                cmds.connectAttr( myWT2 + '.outColor', objselShape[0] + '.surfaceShader', f=True )
                                shadernum.append(myWT2)
    shadersel = cmds.ls(sl=True,ext=nodetyp)
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            hairsadj=cmds.listConnections(shadersel[i]+".outColor",type="hairSystem" )  
            if hairsadj!=None:
                for h in range(len(hairsadj)):
                    myWTs = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWTs + '.shadeMode',2)
                    cmds.setAttr(myWTs + '.color', 0, 0, 1, type="double3")
                    myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                    myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWT2s + '.shadeMode',2)
                    cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                    cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                    cmds.connectAttr( myWT2s + '.outColor', hairsadj[h] + '.aiHairShader', f=True )
                    shadernum.append(myWT2s)
            else:
                shaveadj=cmds.listConnections(shadersel[i]+".outColor",type="shaveHair" )  
                if shaveadj!=None:
                    for s in range(len(shaveadj)):
                        myWTs = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWTs + '.shadeMode',2)
                        cmds.setAttr(myWTs + '.color', 0, 0, 1, type="double3")
                        myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                        myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(myWT2s + '.shadeMode',2)
                        cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                        cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                        cmds.connectAttr( myWT2s + '.outColor', shaveadj[s] + '.aiHairShader', f=True )
                        shadernum.append(myWT2s)
                else:
                    myWTs = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWTs + '.shadeMode',2)
                    cmds.setAttr(myWTs + '.color', 0, 0, 1, type="double3")
                    myWCs = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.connectAttr( myWTs + '.outColor', myWCs + '.input', f=True )
                    myWT2s = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(myWT2s + '.shadeMode',2)
                    cmds.connectAttr( myWCs + '.outColor', myWT2s + '.color', f=True )
                    cmds.connectAttr( shadersel[i] + ('.outColor'), myWCs + '.beauty', f=True )
                    shaderselShape = cmds.listConnections( shadersel[i], s=True,t='shadingEngine' )
                    cmds.connectAttr( myWT2s + '.outColor', shaderselShape[0] + '.surfaceShader', f=True )
                    shadernum.append(myWT2s)
    if shadersel ==[] and objsel==[]:
        cmds.warning("û��ѡ��ģ�ͻ����")
    if shadernum!=None:
        print "������"+str(len(shadernum))+"��ID\n",
def comidbyobj(arg):
    nodetyp = ["aiStandard","aiSkin","layeredShader","aiHair","alHair","alLayer","alSurface"]
    mtsel = cmds.ls(mat=1)
    objselID = cmds.ls(sl=True,typ="transform")
    if objselID !=[]: 
        obj2shapes = cmds.listRelatives(objselID)
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        SG2WT2 = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        WT22WC = cmds.listConnections(SG2WT2,d=0)
        WC2WT = cmds.listConnections(WT22WC,d=0,type='aiUtility')
        WC2WTRe = list(set(WC2WT))
        if len(WC2WTRe)>1:
            WC2WTReother = cmds.listConnections(WC2WTRe[1:len(WC2WTRe)],s=0,type='aiWriteColor')
            WC2WTRefirst = WC2WTRe[0]
            for i in range(0,len(WC2WTReother)):
                cmds.connectAttr(WC2WTRefirst + '.outColor',WC2WTReother[i] + '.input', f=True )
            cmds.delete(WC2WTRe[1:len(WC2WTRe)])
        else:
            print "ID�Ѿ��ϲ�",
    shaderselIDs = cmds.ls(sl=True,typ="aiUtility")
    if  shaderselIDs !=[]:
        Ai2WT = cmds.listConnections(shaderselIDs,d=0,type='aiWriteColor')
        SG2WT2 = cmds.listConnections(Ai2WT,d=0,type='aiUtility')
        SG2AiRe2 = list(set(SG2WT2))
        if len(SG2AiRe2)>1:
            WC2WTReother2 = cmds.listConnections(SG2AiRe2[1:len(SG2AiRe2)],s=0,type='aiWriteColor')
            WC2WTRefirst2 = SG2AiRe2[0]
            for i in range(0,len(WC2WTReother2)):
                cmds.connectAttr(WC2WTRefirst2 + '.outColor',WC2WTReother2[i] + '.input', f=True )
            cmds.delete(SG2AiRe2[1:len(SG2AiRe2)])
        else:
            print "ID�Ѿ��ϲ�",
    if objselID ==[] and shaderselIDs==[]:
        cmds.warning("û��ѡ��ģ�ͻ����")
def opset(arg):
    Aisel = cmds.ls(type="aiStandard")
    AOselset = []
    nmselset = []
    bygsel = []
    rgbRsel = []
    rgbGsel = []
    rgbBsel = []
    for i in range(len(Aisel)):
        AWOP = []
        AWUOP= []
        opfile = cmds.listConnections(Aisel[i]+".opacity",d=0)
        Aiop = cmds.getAttr(Aisel[i]+".opacity")
        if Aiop !=[(1.0,1.0,1.0)]:
            Awsel = cmds.listConnections(Aisel[i],s=0,type="aiWriteColor")
            if Awsel!=None:
                cmds.setAttr(Awsel[0] +'.blend',1)
                AWOP.append(Awsel)
            Awsels = cmds.listConnections(Awsel,s=0,type="aiWriteColor")
            if Awsels!=None:
                cmds.setAttr(Awsels[0] +'.blend',1)
                AWOP.append(Awsels)
            while Awsels!=None:
                Awsels = cmds.listConnections(Awsels,s=0,type="aiWriteColor")
                AWOP.append(Awsels)
                if Awsels!=None:
                    cmds.setAttr(Awsels[0] +'.blend',1)
            noneset =[None]
            AWOPs = [i for i in AWOP if i not in noneset]
            for p in range(0,len(AWOPs)):
                Ausel = cmds.listConnections(str(AWOPs[p][0])+".input",d=0,type="aiUtility")
                Aosel = cmds.listConnections(str(AWOPs[p][0])+".input",d=0,type="aiAmbientOcclusion")           
                if opfile!=None: 
                    cmds.setAttr(opfile[0]+'.alphaIsLuminance',1)
                    if Ausel !=None:
                        if cmds.isConnected(opfile[0]+".outAlpha",Ausel[0]+".opacity")==False:
                            cmds.connectAttr(opfile[0]+".outAlpha",Ausel[0]+".opacity",f=1)
                    if Aosel !=None:
                        if cmds.isConnected(opfile[0]+".outColor",Aosel[0]+".opacity")==False:
                            cmds.connectAttr(opfile[0]+".outColor",Aosel[0]+".opacity",f=1)
                Aufinal = cmds.listConnections(str(AWOP[p][0])+".outColor",s=0,type="aiUtility")
                if Aufinal!=None:
                    SGsel=cmds.listConnections(Aufinal[0],s=0,type="shadingEngine")
                    shapesel = cmds.listConnections(SGsel[0],d=0,type="mesh")
                    if shapesel!=None:
                        cmds.setAttr(shapesel[0] + ".aiOpaque",0)
        else:
            Awsel = cmds.listConnections(Aisel[i],s=0,type="aiWriteColor")
            AWUOP.append(Awsel)
            Awsels = cmds.listConnections(Awsel,s=0,type="aiWriteColor")
            if Awsels!=None:
                AWUOP.append(Awsels)
            while Awsels!=None:
                Awsels = cmds.listConnections(Awsels,s=0,type="aiWriteColor")
                AWUOP.append(Awsels)
            noneset =[None]
            AWUOPs = [i for i in AWUOP if i not in noneset]
            for p in range(0,len(AWUOPs)):
                Aosel = cmds.listConnections(str(AWUOPs[p][0])+".input",d=0,type="aiAmbientOcclusion")
                AOselset.append(Aosel)
                Ausel = cmds.listConnections(str(AWUOPs[p][0])+".input",d=0,type="aiUtility")
                if Ausel !=None:
                    OPramps = cmds.listConnections(str(Ausel[0])+".color",d=0,type="ramp")
                    if OPramps !=None:
                        bygsel.append(Ausel)
                    else:
                        OPcmode = cmds.getAttr(Ausel[0]+".colorMode")
                        if OPcmode == 3:
                            nmselset.append(Ausel)
                        else:
                            coloradj = cmds.getAttr(Ausel[0]+".color")
                            if coloradj[0] == (1,0,0):
                                rgbRsel.append(Ausel)
                            if coloradj[0]== (0,1,0):
                                rgbGsel.append(Ausel)
                            if coloradj[0]== (0,0,1):
                                rgbBsel.append(Ausel)
                                
    noneset =[None]
    AOselsets = [i for i in AOselset if i not in noneset]
    nmselsets = [i for i in nmselset if i not in noneset]
    bygsels = [i for i in bygsel if i not in noneset]
    rgbRsels = [i for i in rgbRsel if i not in noneset]
    rgbGsels = [i for i in rgbGsel if i not in noneset]
    rgbBsels = [i for i in rgbBsel if i not in noneset]
    
    if AOselsets !=None:
        for i in range(1,len(AOselsets)):
            Awsel = cmds.listConnections(AOselsets[i],s=0,type="aiWriteColor")
            Awseladj = cmds.isConnected(str(AOselsets[0][0])+".outColor",str(Awsel[0])+".input")
            if Awseladj!=True:
                cmds.connectAttr(str(AOselsets[0][0])+".outColor",str(Awsel[0])+".input",f=1)
    if nmselsets !=None:
        for i in range(1,len(nmselsets)):
            Awsel = cmds.listConnections(nmselsets[i],s=0,type="aiWriteColor")
            Awseladj = cmds.isConnected(str(nmselsets[0][0])+".outColor",str(Awsel[0])+".input")
            if Awseladj!=True:
                cmds.connectAttr(str(nmselsets[0][0])+".outColor",str(Awsel[0])+".input",f=1)
    if bygsels !=None:
        for i in range(1,len(bygsels)):
            Awsel = cmds.listConnections(bygsels[i],s=0,type="aiWriteColor")
            Awseladj = cmds.isConnected(str(bygsels[0][0])+".outColor",str(Awsel[0])+".input")
            if Awseladj!=True:
                cmds.connectAttr(str(bygsels[0][0])+".outColor",str(Awsel[0])+".input",f=1)
    if rgbRsels !=None:
        for i in range(1,len(rgbRsels)):
            Awsel = cmds.listConnections(rgbRsels[i],s=0,type="aiWriteColor")
            Awseladj = cmds.isConnected(str(rgbRsels[0][0])+".outColor",str(Awsel[0])+".input")
            if Awseladj!=True:
                cmds.connectAttr(str(rgbRsels[0][0])+".outColor",str(Awsel[0])+".input",f=1)
    if rgbGsels !=None:
        for i in range(1,len(rgbGsels)):
            Awsel = cmds.listConnections(rgbGsels[i],s=0,type="aiWriteColor")
            Awseladj = cmds.isConnected(str(rgbGsels[0][0])+".outColor",str(Awsel[0])+".input")
            if Awseladj!=True:
                cmds.connectAttr(str(rgbGsels[0][0])+".outColor",str(Awsel[0])+".input",f=1)
    if rgbBsels !=None:
        for i in range(1,len(rgbBsels)):
            Awsel = cmds.listConnections(rgbBsels[i],s=0,type="aiWriteColor")
            Awseladj = cmds.isConnected(str(rgbBsels[0][0])+".outColor",str(Awsel[0])+".input")
            if Awseladj!=True:
                cmds.connectAttr(str(rgbBsels[0][0])+".outColor",str(Awsel[0])+".input",f=1)        
##Ƥ��
    skAisel = cmds.ls(type="aiSkin")
    skskAoselset = []
    sknmselset = []
    skbygsel = []
    skrgbRsel = []
    skrgbGsel = []
    skrgbBsel = []
    if skAisel!=[]:
        for i in range(len(skAisel)):
            skAWOP = []
            skAWUOP= []
            skopfile = cmds.listConnections(skAisel[i]+".opacity",d=0)
            skAiop = cmds.getAttr(skAisel[i]+".opacity")
            skAiopc = cmds.getAttr(skAisel[i]+".opacityColor")
            if skAiop !=[(1.0,1.0,1.0)] and skAiopc !=[(1.0,1.0,1.0)]:
                print "yes"
            else:
                skAwsel = cmds.listConnections(skAisel[i],s=0,type="aiWriteColor")
                if skAwsel!=None:
                    skAWUOP.append(skAwsel)
                    skAwsels = cmds.listConnections(skAwsel,s=0,type="aiWriteColor")
                    if skAwsels!=None:
                        skAWUOP.append(skAwsels)
                    while skAwsels!=None:
                        skAwsels = cmds.listConnections(skAwsels,s=0,type="aiWriteColor")
                        skAWUOP.append(skAwsels)
                    sknoneset =[None]
                    skAWUOPs = [i for i in skAWUOP if i not in sknoneset]
                    for p in range(0,len(skAWUOPs)):
                        skAosel = cmds.listConnections(str(skAWUOPs[p][0])+".input",d=0,type="aiAmbientOcclusion")
                        skskAoselset.append(skAosel)
                        skAusel = cmds.listConnections(str(skAWUOPs[p][0])+".input",d=0,type="aiUtility")
                        if skAusel !=None:
                            skOPramps = cmds.listConnections(str(skAusel[0])+".color",d=0,type="ramp")
                            if skOPramps !=None:
                                skbygsel.append(skAusel)
                            else:
                                skOPcmode = cmds.getAttr(skAusel[0]+".colorMode")
                                if skOPcmode == 3:
                                    sknmselset.append(skAusel)
                                else:
                                    skcoloradj = cmds.getAttr(skAusel[0]+".color")
                                    if skcoloradj[0] == (1,0,0):
                                        skrgbRsel.append(skAusel)
                                    if skcoloradj[0]== (0,1,0):
                                        skrgbGsel.append(skAusel)
                                    if skcoloradj[0]== (0,0,1):
                                        skrgbBsel.append(skAusel)
                                    
    sknoneset =[None]
    skskAoselsets = [i for i in skskAoselset if i not in sknoneset]
    sknmselsets = [i for i in sknmselset if i not in sknoneset]
    skbygsels = [i for i in skbygsel if i not in sknoneset]
    skrgbRsels = [i for i in skrgbRsel if i not in sknoneset]
    skrgbGsels = [i for i in skrgbGsel if i not in sknoneset]
    skrgbBsels = [i for i in skrgbBsel if i not in sknoneset]
        
    if skskAoselsets !=None:
        for i in range(1,len(skskAoselsets)):
            skAwsel = cmds.listConnections(skskAoselsets[i],s=0,type="aiWriteColor")
            skAwseladj = cmds.isConnected(str(skskAoselsets[0][0])+".outColor",str(skAwsel[0])+".input")
            if skAwseladj!=True:
                cmds.connectAttr(str(skskAoselsets[0][0])+".outColor",str(skAwsel[0])+".input",f=1)
    if sknmselsets !=None:
        for i in range(1,len(sknmselsets)):
            skAwsel = cmds.listConnections(sknmselsets[i],s=0,type="aiWriteColor")
            skAwseladj = cmds.isConnected(str(sknmselsets[0][0])+".outColor",str(skAwsel[0])+".input")
            if skAwseladj!=True:
                cmds.connectAttr(str(sknmselsets[0][0])+".outColor",str(skAwsel[0])+".input",f=1)
    if skbygsels !=None:
        for i in range(1,len(skbygsels)):
            skAwsel = cmds.listConnections(skbygsels[i],s=0,type="aiWriteColor")
            skAwseladj = cmds.isConnected(str(skbygsels[0][0])+".outColor",str(skAwsel[0])+".input")
            if skAwseladj!=True:
                cmds.connectAttr(str(skbygsels[0][0])+".outColor",str(skAwsel[0])+".input",f=1)
    if skrgbRsels !=None:
        for i in range(1,len(skrgbRsels)):
            skAwsel = cmds.listConnections(skrgbRsels[i],s=0,type="aiWriteColor")
            skAwseladj = cmds.isConnected(str(skrgbRsels[0][0])+".outColor",str(skAwsel[0])+".input")
            if skAwseladj!=True:
                cmds.connectAttr(str(skrgbRsels[0][0])+".outColor",str(skAwsel[0])+".input",f=1)
    if skrgbGsels !=None:
        for i in range(1,len(skrgbGsels)):
            skAwsel = cmds.listConnections(skrgbGsels[i],s=0,type="aiWriteColor")
            skAwseladj = cmds.isConnected(str(skrgbGsels[0][0])+".outColor",str(skAwsel[0])+".input")
            if skAwseladj!=True:
                cmds.connectAttr(str(skrgbGsels[0][0])+".outColor",str(skAwsel[0])+".input",f=1)
    if skrgbBsels !=None:
        for i in range(1,len(skrgbBsels)):
            skAwsel = cmds.listConnections(skrgbBsels[i],s=0,type="aiWriteColor")
            skAwseladj = cmds.isConnected(str(skrgbBsels[0][0])+".outColor",str(skAwsel[0])+".input")
            if skAwseladj!=True:
                cmds.connectAttr(str(skrgbBsels[0][0])+".outColor",str(skAwsel[0])+".input",f=1)
    mm.eval('hyperShadePanelMenuCommand("hyperShadePanel", "deleteUnusedNodes");') 
    

##�޸�hair����״̬Ϊ��̬
    hairsel = cmds.ls(type="hairSystem")
    if hairsel!=[]:
        for i in range(len(hairsel)):
            cmds.setAttr(hairsel[i]+".simulationMethod",1)
            cmds.setAttr(hairsel[i]+".active",0)


##�޸��渳����
    meshape = pm.ls(type="mesh")
    multishape = []
    for m in range(len(meshape)):
        sg = pm.listConnections(meshape[m],d=0,type="shadingEngine")
        if  sg!=[]:
            if len(sg)==1:
                if pm.listConnections(sg[0]+".surfaceShader",d=0)!=[]:
                    shder =  pm.listConnections(sg[0]+".surfaceShader",d=0)[0]
                    pm.select(meshape[m])
                    pm.hyperShade(a = shder)
            else:
                multishape.append(meshape[m])
    mesh = pm.pickWalk(multishape,d="up")
    pm.select(mesh,r=1)

##����ռ�����
    try:
        allnmsp = [i for i in  pm.namespaceInfo(lon=1,r=1) if i not in ['UI','shared']]
        nmspnum=[]
        if allnmsp!=[]:
            for a in range(len(allnmsp)):
                pm.namespace(mv=[allnmsp[a],":"],f=1)
                pm.namespace(removeNamespace=allnmsp[a])
                nmspnum.append(allnmsp[a])
            print "������"+str(len(nmspnum))+"���ռ���������",
    except:
        print "�ռ���������",

def changeAovsname(arg):
    value=cmds.textField('cmmaov',q=True,tx=True)
    sel = cmds.ls(sl=1,type="aiWriteColor")
    if sel!=[]:
        for i in range(0,len(sel)):
            cmds.setAttr(sel[i]+'.aovName',value+"_ID",type="string")
    else:
        print "��ѡ��aiWriteColor�ڵ㣡��",
def clean(arg):
    mm.eval('checkNode')
def cleanzz(arg):
    mm.eval('source "O:/mocap/SJ_ToolBox/mel_source/zz01.mel" ')
def opmodel(arg):
    mocb=pm.checkBox("renallmo" ,q=True,v=True)
    shdercb=pm.checkBox("renallshader" ,q=True,v=True)
    aovcb=pm.checkBox("renallaov" ,q=True,v=True)
    ungroupcb=pm.checkBox("ungroup" ,q=True,v=True)

    unoptcb=pm.checkBox("unopt" ,q=True,v=True)
    unhaircb=pm.checkBox("haircl" ,q=True,v=True)
    unyeticb=pm.checkBox("yeticl" ,q=True,v=True)

    modelname=cmds.textField('cmmaov',q=True,tx=True)

##����������
    if shdercb!=1:
        vailshdrlist = open('//10.99.1.13/hq_tool/Maya/hq_maya/scripts/fantabox/modeling/vailshaderlist.txt')
        try:
            vailshdr = vailshdrlist.readlines( )[0].split(',')
        finally:
            vailshdrlist.close( )
        rname = [i for i in pm.ls(type=vailshdr) if i not in ["initialParticleSE","initialShadingGroup"]]
        for n in range(len(rname)):
            pm.rename(rname[n],modelname+"_AS")
##ģ��������
    if mocb!=1:
        sel =[i.getParent() for i in  pm.ls(typ="mesh") if pm.listConnections(i,s=0,type="shadingEngine")]
        puremesh =[]
        for i in range(len(sel)):
            if pm.listConnections(sel[i].getShape(),s=0,type="shaveHair")==[] and pm.listConnections(sel[i].getShape(),s=0,type="pgYetiMaya")==[] and pm.listConnections(sel[i].getShape(),s=0,type="follicle")==[]:
                if ungroupcb!=1:
                    pm.parent(sel[i],w=1)
                pm.setAttr(sel[i]+".tx",lock=0)
                pm.setAttr(sel[i]+".ty",lock=0)
                pm.setAttr(sel[i]+".tz",lock=0)
                pm.setAttr(sel[i]+".rx",lock=0)
                pm.setAttr(sel[i]+".ry",lock=0)
                pm.setAttr(sel[i]+".rz",lock=0)
                pm.setAttr(sel[i]+".sx",lock=0)
                pm.setAttr(sel[i]+".sy",lock=0)
                pm.setAttr(sel[i]+".sz",lock=0)
                pm.setAttr(sel[i]+".v",lock=0)
                if unoptcb!=1:
                    pm.makeIdentity(sel[i],apply=1,t=1,r=1,s=1,n=0,pn=1)
                    try:
                        pm.polyNormalPerVertex(sel[i],ufn=1)
                        pm.polySoftEdge(sel[i],a=180,ch=1)
                        pm.lattice(sel[i],dv=(2,5,2),oc =1,ldv=(2,2,2))
                    except:
                        print ""
                    pm.select(sel[i],r=1)
                    mm.eval("DeleteHistory")
                puremesh.append(sel[i])
        if ungroupcb!=1:
            if pm.objExists(modelname+"_geo")==True:
                pm.rename(modelname+"_geo",modelname+"_tmp")
            pm.group(puremesh,name=modelname+"_geo")
        for i in range(len(puremesh)):
            shape = puremesh[i].getShapes()
            puremesh[i].rename(modelname+"_tmp")
            newname = puremesh[i].rename(modelname+"_geo1")
            newnum  = newname.index("geo")
            shape[0].rename(str(modelname+"_geoShape"+newname[newnum+3:]))
##aov������
    if aovcb!=1:
        try:
            aovslist = pm.ls(type="aiAOV")
            pm.delete(aovslist)
            aovs.AOVInterface().addAOV(modelname+"_ID", aovType='rgba')
            aovsel=cmds.ls(typ='aiWriteColor')
            for a in range(0,len(aovsel)):
                cmds.setAttr(aovsel[a]+'.aovName',modelname+"_ID",type="string")
        except:
            print "��arnold��Ⱦ�ڵ�,AOV��Ⱦ������ʧ��!!", 
##yetië������
    if unyeticb!=1:
        yetitype  =[i for  i in pm.ls(type="pgYetiMaya") if pm.listConnections(i,d=0,type="mesh")]
        yetimesh = []
        yetigrm = []
        yetiref = []
        if yetitype!=[]:
            for y in range(len(yetitype)):
                yeticollections = [pm.PyNode(a) for a in  pm.hyperShade(listUpstreamNodes=yetitype[y])]
                pm.select(yeticollections,r= 1)
                mm.eval("DeleteHistory")
                yeticollections = [pm.PyNode(a) for a in  pm.hyperShade(listUpstreamNodes=yetitype[y])]
                meshcol = [m for m in yeticollections if pm.nodeType(m)=="mesh" if pm.listConnections(m+".referenceObject",d=0)!=[]]
                refmeshcol = [m for m in yeticollections if pm.nodeType(m)=="mesh" if pm.listConnections(m+".referenceObject",d=0)==[]]
                if meshcol==[]:
                    for m in range(len(refmeshcol)):
                        pm.select(refmeshcol[m],r=1)
                        mm.eval("CreateTextureReferenceObject")
                yeticollections = [pm.PyNode(a) for a in  pm.hyperShade(listUpstreamNodes=yetitype[y])]
                meshcol = [m for m in yeticollections if pm.nodeType(m)=="mesh" if pm.listConnections(m+".referenceObject",d=0)!=[]]
                yetimesh =yetimesh+meshcol
                refmeshcol = [m for m in yeticollections if pm.nodeType(m)=="mesh" if pm.listConnections(m+".referenceObject",d=0)==[]]
                yetiref = yetiref+refmeshcol
                groomcol = [g for g in yeticollections if pm.nodeType(g)=="pgYetiGroom"]
                yetigrm =yetigrm+groomcol
            if pm.objExists("yeti_show_G")==False:
                pm.group(yetitype,name = "yeti_show_G")
                pm.parent("yeti_show_G",w=1)
            else:
                pm.rename("yeti_show_G","yeti_show_G_old")
                pm.group(yetitype,name = "yeti_show_G")
                pm.parent("yeti_show_G",w=1)
            if yetimesh!= [] and pm.objExists("yeti_setup_G")==False:
                pm.group(yetimesh,name = "yeti_setup_G")
                pm.parent("yeti_setup_G",w=1)
            else:
                if yetimesh!= []:
                    pm.rename("yeti_setup_G","yeti_setup_G_old")
                    pm.group(yetimesh,name = "yeti_setup_G") 
                    pm.parent("yeti_setup_G",w=1)
            if yetigrm!= [] and pm.objExists("groom_G")==False:
                pm.group(yetigrm,name = "groom_G")
                pm.parent("groom_G",w=1)
            else:
                if yetigrm!=[]:
                    pm.rename("groom_G","groom_G_old")
                    pm.group(yetigrm,name = "groom_G")
                    pm.parent("groom_G",w=1)
            if yetiref!= [] and pm.objExists("reference_G")==False:
                pm.group(yetiref,name = "reference_G")
                pm.parent("reference_G",w=1)
            else:
                if yetiref!=[]:
                    pm.rename("reference_G","reference_G_old")
                    pm.group(yetiref,name = "reference_G")
                    pm.parent("reference_G",w=1)
            yetigrp = []
            if yetigrm!=[]:
                yetigrp.append("groom_G")
            if yetiref!=[]:
                yetigrp.append("reference_G")
            if yetimesh!=[]:
                yetigrp.append("yeti_setup_G")
            if pm.objExists("yeti_G")==False:
                pm.group(yetigrp,"yeti_show_G","reference_G",name = "yeti_G")
                pm.parent("yeti_G",w=1)
                pm.delete("yeti_G_old")
            else:
                pm.rename("yeti_G","yeti_G_old")
                pm.group(yetigrp,"yeti_show_G","reference_G",name = "yeti_G")
                pm.parent("yeti_G",w=1)
                pm.delete("yeti_G_old")
            pm.setAttr("yeti_setup_G.visibility",0)
            #pm.setAttr("groom_G.visibility",0)
            pm.setAttr("reference_G.visibility",0)
##hairë������
    if unhaircb!=1:
        hairsys  =[i.getParent() for  i in pm.ls(type="hairSystem") if pm.listConnections(i+".outputRenderHairs",s=0,type ="pfxHair")!=[]]
        judgeName(modelname+"_hairSystem_G")
        hairsysgrp = grp_proc(hairsys,modelname)

        judgeName(modelname+"_hair_setup_G")
        hairsetupgrp = pm.group(em=True,name = modelname+"_hair_setup_G")

        judgeName("hair_show_G")
        hairshowgrp = pm.group(em=True,name = "hair_show_G")

        judgeName(modelname+"_follicle_G")
        folliclegrp = pm.group(em=True,name = modelname+"_follicle_G")


        judgeName(modelname+"_pfxHair_G")
        pfxhairgrp = pm.group(em=True,name = modelname+"_pfxHair_G")
        pm.parent(pfxhairgrp,hairshowgrp)

        judgeName(modelname+"_OutputCVs_G")
        outputcvsgrp = pm.group(em=True,name = modelname+"_OutputCVs_G")

        fomeshcols =[]

        for h in range(len(hairsys)):
            hairsysShape =hairsys[h].getShape()
            pm.setAttr(hairsysShape+".simulationMethod",1)
            pm.setAttr(hairsysShape+".active",0)
            pfxhairs = pm.listConnections(hairsysShape,s=0,type="pfxHair")
            if pfxhairs!=[]:
                pm.parent(pfxhairs[0],pfxhairgrp)
                pm.rename(pfxhairs[0],modelname+"_pfxhairs"+str(h+1))
            follicles = pm.listConnections(hairsysShape,d=0,type="follicle")
            if follicles!=[]:
                follicleChildgrp = grp_proc(follicles,modelname,folliclegrp,h)
                for f in range(len(follicles)):
                    folcvs=[a for a in pm.listRelatives(follicles[f],c=1) if pm.nodeType(a)=="transform"]
                    if folcvs!=[] and len(folcvs)==1:
                        pm.rename(folcvs[0],modelname+"_folcvs"+"_G"+str(h+1)+"_cvs"+str(f+1))
                    folmesh =  pm.listConnections(follicles[f].getShape()+".inputWorldMatrix",d=0,type="mesh")
                    fomeshcols+=folmesh
                    outputcvs =  pm.listConnections(follicles[f].getShape(),s=0,type="nurbsCurve") 
                    outputcvsChildgrp = grp_proc(outputcvs,modelname+"_outputCvs",outputcvsgrp,h)
                    
        if fomeshcols!=[]:
            fomeshcols=list(set(fomeshcols))
        judgeName(modelname+"_hair_mesh_G")    
        hairmeshgrp = grp_proc(fomeshcols,modelname+"_hair")
        pm.parent(hairmeshgrp,hairsetupgrp)

        wholecols =[a for a in [folliclegrp,hairshowgrp,hairsysgrp,outputcvsgrp,hairsetupgrp] if pm.listRelatives(a,c=1)!=[]]
        for wholecol in wholecols:
            if wholecol.find("hair_show_G")==-1:
                pm.setAttr(wholecol+".visibility",0)      

        judgeName("hair_G")  
        pm.group([folliclegrp,hairshowgrp,hairsysgrp,outputcvsgrp,hairsetupgrp],name = "hair_G")
        delcols =list(set([folliclegrp,hairshowgrp,hairsysgrp,outputcvsgrp,hairsetupgrp])-set(wholecols))

        if delcols!=[]:
            pm.delete(delcols)

    disLayValid =["defaultLayer","ori_sim","NoRender","TX"]
    disLays =[d for d in cmds.ls(type="displayLayer") if d not in disLayValid]
    cmds.delete(disLays)
def SJ_charcleanuptoolwdUI():
    '''
    2.6����˵��������hairSystem�淶�������޸���hairSystem��shape�ڵ���������ȷ���µĽ�������;
    2.7����˵��������pfxHair�淶�������޸�groom��Ϊ�����أ�����ɾ��������ʾ�㹦��;
    2.8����˵�����������߹淶�����������ӽ�ɫ��ǰ׺;
    
    '''
    
    if cmds.window('aiWriteColor',ex=True):
        cmds.deleteUI('aiWriteColor',wnd=True)
    if cmds.window('IDmakerbyO',ex=True):
        cmds.deleteUI('IDmakerbyO',wnd=True)
    if cmds.window('addIDmakerbyO',ex=True):
        cmds.deleteUI('addIDmakerbyO',wnd=True)
    cmds.window('IDmakerbyO',t='CharCleanupToolV2.8')
    cmds.columnLayout(adj=True,w=300)
    cmds.text(l='��ɫ�ļ�������V2.8',fn='fixedWidthFont',h=50,ann=__doc__)
    cmds.textField('cmmaov',tx="charname",h=30,annotation="��������Ҫ��ɫ��")
    cmds.button(l='��ɫID����',bgc=[1,0.5,0.5],c=redobj,h=50,annotation="ѡ��ģ�ͻ��߲������ɺ�ɫID")
    cmds.button(l='��ɫID����',bgc=[0.5,0.5,1],c=blueobj,h=50,annotation="ѡ��ģ�ͻ��߲���������ɫID")
    cmds.button(l='��ɫID����',c=greenobj,bgc=[0.5,1,0.5],h=50,annotation="ѡ��ģ�ͻ��߲���������ɫID")
    cmds.button(l='�ֶ��ϲ���ͬ��ɫID',c=comidbyobj,h=50,bgc=[0.976,0.768,0.518],annotation="����ͬʱѡ��ģ�ͺͲ��ʻ�Ϻϲ�ID")
    cmds.button(l='һ���Ż�����',c=opset,bgc=[0.3,0.6,0.6],h=50,annotation="(1) ��͸����ͼ��Alpha Is��Luminanceѡ��� \n(2)��͸��ģ�͵�opaqueѡ��ȥ�� \n(3)��͸����ͼ���ӵ�ID�ڵ��opacity�� \n(4)��͸�������aiWriteColor��blendѡ��� \n(5)�ϲ���͸��������ͬ���ԵģɣĲ��ʣ����磺����ɫID�ϲ����������ļ���  \n(6)����ռ����� \n(7)���渳���޸� \n(8) hairsystem����״̬�޸�")
    cmds.button(l='�������������ύǰ���������һ�Σ�',c=clean,h=50,bgc=[0.3,0.63,0.83])
    cmds.flowLayout( columnSpacing=0)
    cmds.button(l='ZZ��װ���',c=cleanzz,h=50,bgc=[0.3,0.73,0.93],w=165)
    cmds.button(l='��ͼ����', c= "fb.mod.SJ_texToolswdUI()",h=50,ann="",w=165,bgc=[0.3,0.73,0.93])
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("renallmo" ,label='����ģ��',ann="",w=80,h=30)
    cmds.checkBox("ungroup" ,label='������',ann="",w=80,h=30)
    cmds.checkBox("unopt" ,label='��ִ��ģ���Ż�',ann="",w=120,h=30)
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("haircl" ,label='����hair',ann="",w=80,h=30)
    cmds.checkBox("yeticl" ,label='����yeti',ann="",w=80,h=30)
    cmds.checkBox("renallshader" ,label='���Բ���',ann="",w=80,h=30)
    cmds.checkBox("renallaov" ,label='����aovs��',ann="",w=80,h=30)

    cmds.setParent( '..' )
    cmds.button(l='һ�������ļ�',c=opmodel,h=50,bgc=[0.3,0.75,0.8],annotation="")
    cmds.button(l='�����޸�aiWriteColor��Aovs����',c=changeAovsname,bgc=[0.8,0.5,0.5],h=50,annotation="ѡ��aiWriteColor�ڵ㣨�ɶ�ѡ��")
    cmds.button(l='����ͼ�����л�����',c= "fb.mod.SJ_MultiTexwdUI()",h=50,bgc=[0.8,0.56,0.5])
    cmds.button(l='ģ����ʾ��ɫ��ɫ��',c= "fb.mod.SJ_hardwareColorchangerwdUI()",h=50,bgc=[0.8,0.66,0.5])
    cmds.button(l='����', c= "fb.mod.SJ_charToolwdUI()",h=50)
    cmds.showWindow()
if __name__ =="__main__":
    SJ_charcleanuptoolwdUI()