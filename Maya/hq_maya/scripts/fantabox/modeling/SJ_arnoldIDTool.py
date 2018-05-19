#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
import maya.mel as mel
import os
import mtoa.aovs as aovs
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
        cmds.warning("没有选择模型或材质")
    if shadernum!=None:
        print "已生成"+str(len(shadernum))+"个ID \n",
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
        cmds.warning("没有选择模型或材质")
    if shadernum!=None:
        print "已生成"+str(len(shadernum))+"个ID\n",
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
        cmds.warning("没有选择模型或材质")
    if shadernum!=None:
        print "已生成"+str(len(shadernum))+"个ID\n", 
def byg(arg):
    objsel =cmds.ls(sl=True,typ="transform")
    addnum =[]
    if objsel !=[]: 
        obj2shapes = cmds.listRelatives(objsel,c=1)   
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        sels = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        if sels!=None:
            sel = list(set(sels))
            for i in range(0,len(sel)):
                AWsel = cmds.listConnections(sel[i],d=0,type="aiWriteColor")
                if AWsel != None:
                    newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.setAttr(newAW+'.aovName',"BYG",type="string")
                    ramNd = cmds.shadingNode('ramp', asTexture=True)
                    samInfo = cmds.shadingNode('samplerInfo', asUtility=True)
                    newAU = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(newAU + '.shadeMode',2)
                    cmds.setAttr(ramNd+".colorEntryList[0].color",1, 0, 0, type="double3")
                    cmds.setAttr(ramNd+".colorEntryList[1].color",0, 0, 1, type="double3")
                    cmds.setAttr(ramNd+".colorEntryList[1].position",0.635)
                    cmds.connectAttr(samInfo+".facingRatio",ramNd+".vCoord")
                    cmds.connectAttr(ramNd+".outColor",newAU+".color")
                    cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                    cmds.connectAttr( newAW + '.outColor', sel[i] + '.color', f=True )
                    cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                    addnum.append(newAU)
    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            AWshadersel = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshadersel != None:
                newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                cmds.setAttr(newAW+'.aovName',"BYG",type="string")
                ramNd = cmds.shadingNode('ramp', asTexture=True)
                samInfo = cmds.shadingNode('samplerInfo', asUtility=True)
                newAU = cmds.shadingNode('aiUtility', asShader=True)
                cmds.setAttr(newAU + '.shadeMode',2)
                cmds.setAttr(ramNd+".colorEntryList[0].color",1, 0, 0, type="double3")
                cmds.setAttr(ramNd+".colorEntryList[1].color",0, 0, 1, type="double3")
                cmds.setAttr(ramNd+".colorEntryList[1].position",0.635)
                cmds.connectAttr(samInfo+".facingRatio",ramNd+".vCoord")
                cmds.connectAttr(ramNd+".outColor",newAU+".color")
                cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                cmds.connectAttr( newAW + '.outColor', shadersel[i] + '.color', f=True )
                cmds.connectAttr( AWshadersel[0] + '.outColor', newAW + '.beauty', f=True )
                addnum.append(newAU)
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
    if addnum!=None:
        print "已增加了"+str(len(addnum))+"个BYG节点！！\n",    
def occ(arg):
    notype = ["nurbsCurve","follicle","transform"]
    addnum = []
    objsel =cmds.ls(sl=True,typ="transform")
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel,c=1) 
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
                            AWsel = cmds.listConnections(nhairshader[0],d=0,type="aiWriteColor")
                            newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                            cmds.setAttr(newAW+'.aovName',"OCC",type="string")
                            newAU = cmds.shadingNode('aiAmbientOcclusion', asShader=True)
                            cmds.setAttr(newAU + '.samples',5)
                            cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                            cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                            cmds.connectAttr( newAW + '.outColor', nhairshader[0] + '.color', f=True )
                            addnum.append(newAU)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        AWsel = cmds.listConnections(shaveshader[0],d=0,type="aiWriteColor")
                        newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                        cmds.setAttr(newAW+'.aovName',"OCC",type="string")
                        newAU = cmds.shadingNode('aiAmbientOcclusion', asShader=True)
                        cmds.setAttr(newAU + '.samples',5)
                        cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                        cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                        cmds.connectAttr( newAW + '.outColor', shaveshader[0] + '.color', f=True )
                        addnum.append(newAU) 
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        sels = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        if sels!=None:
            sel = list(set(sels))   
            for i in range(0,len(sel)):
                AWsel = cmds.listConnections(sel[i],d=0,type="aiWriteColor")
                if AWsel != None:
                    newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.setAttr(newAW+'.aovName',"OCC",type="string")
                    newAU = cmds.shadingNode('aiAmbientOcclusion', asShader=True)
                    cmds.setAttr(newAU + '.samples',5)
                    cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                    cmds.connectAttr( newAW + '.outColor', sel[i] + '.color', f=True )
                    cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                    addnum.append(newAU)
    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            AWshadersel = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshadersel != None:
                newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                cmds.setAttr(newAW+'.aovName',"OCC",type="string")
                newAU = cmds.shadingNode('aiAmbientOcclusion', asShader=True)
                cmds.setAttr(newAU + '.samples',5)
                cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                cmds.connectAttr( newAW + '.outColor', shadersel[i] + '.color', f=True )
                cmds.connectAttr( AWshadersel[0] + '.outColor', newAW + '.beauty', f=True )
                addnum.append(newAU)
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
    if addnum!=None:
        print "已增加了"+str(len(addnum))+"个OCC节点！！\n",    
def norm(arg):
    objsel =cmds.ls(sl=True,typ="transform")
    addnum = []
    if objsel !=[]: 
        obj2shapes = cmds.listRelatives(objsel,c=1)   
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        sels = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        if sels!=None:
            sel = list(set(sels))
            for i in range(0,len(sel)):
                AWsel = cmds.listConnections(sel[i],d=0,type="aiWriteColor")
                if AWsel != None:
                    newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                    cmds.setAttr(newAW+'.aovName',"normal",type="string")
                    newAU = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(newAU + '.shadeMode',2)
                    cmds.setAttr(newAU + '.colorMode',3)
                    cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                    cmds.connectAttr( newAW + '.outColor', sel[i] + '.color', f=True )
                    cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                    addnum.append(newAU)

    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            AWshadersel = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshadersel != None:
                newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                cmds.setAttr(newAW+'.aovName',"normal",type="string")
                newAU = cmds.shadingNode('aiUtility', asShader=True)
                cmds.setAttr(newAU + '.shadeMode',2)
                cmds.setAttr(newAU + '.colorMode',3)
                cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                cmds.connectAttr( newAW + '.outColor', shadersel[i] + '.color', f=True )
                cmds.connectAttr( AWshadersel[0] + '.outColor', newAW + '.beauty', f=True )
                addnum.append(newAU)
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
    if addnum!=None:
        print "已增加了"+str(len(addnum))+"个Normal节点！！\n",    
def redadd(arg):
    notype = ["nurbsCurve","follicle","transform"]
    addnum = []
    objsel =cmds.ls(sl=True,typ="transform")
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel,c=1) 
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
                            AWsel = cmds.listConnections(nhairshader[0],d=0,type="aiWriteColor")
                            newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                            newAU = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(newAU + '.shadeMode',2)
                            cmds.setAttr(newAU + '.color', 1, 0, 0, type="double3")
                            cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                            cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                            cmds.connectAttr( newAW + '.outColor', nhairshader[0] + '.color', f=True )
                            addnum.append(newAU)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        AWsel = cmds.listConnections(shaveshader[0],d=0,type="aiWriteColor")
                        newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                        newAU = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(newAU + '.shadeMode',2)
                        cmds.setAttr(newAU + '.color', 1, 0, 0, type="double3")
                        cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                        cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                        cmds.connectAttr( newAW + '.outColor', shaveshader[0] + '.color', f=True )
                        addnum.append(newAU) 
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        sels = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        if sels!=None:
            sel = list(set(sels))   
            for i in range(0,len(sel)):
                AWsel = cmds.listConnections(sel[i],d=0,type="aiWriteColor")
                if AWsel != None:
                    newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                    newAU = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(newAU + '.shadeMode',2)
                    cmds.setAttr(newAU + '.color', 1, 0, 0, type="double3")
                    cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                    cmds.connectAttr( newAW + '.outColor', sel[i] + '.color', f=True )
                    cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                    addnum.append(newAU)
    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            AWshadersel = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshadersel != None:
                newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                newAU = cmds.shadingNode('aiUtility', asShader=True)
                cmds.setAttr(newAU + '.shadeMode',2)
                cmds.setAttr(newAU + '.color', 1, 0, 0, type="double3")
                cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                cmds.connectAttr( newAW + '.outColor', shadersel[i] + '.color', f=True )
                cmds.connectAttr( AWshadersel[0] + '.outColor', newAW + '.beauty', f=True )
                addnum.append(newAU)
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
    if addnum!=None:
        print "已增加了"+str(len(addnum))+"个ＩＤ节点！！\n",    
def greenadd(arg):
    notype = ["nurbsCurve","follicle","transform"]
    addnum = []
    objsel =cmds.ls(sl=True,typ="transform")
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel,c=1) 
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
                            AWsel = cmds.listConnections(nhairshader[0],d=0,type="aiWriteColor")
                            newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                            newAU = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(newAU + '.shadeMode',2)
                            cmds.setAttr(newAU + '.color', 0, 1, 0, type="double3")
                            cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                            cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                            cmds.connectAttr( newAW + '.outColor', nhairshader[0] + '.color', f=True )
                            addnum.append(newAU)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        AWsel = cmds.listConnections(shaveshader[0],d=0,type="aiWriteColor")
                        newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                        newAU = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(newAU + '.shadeMode',2)
                        cmds.setAttr(newAU + '.color', 0, 1, 0, type="double3")
                        cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                        cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                        cmds.connectAttr( newAW + '.outColor', shaveshader[0] + '.color', f=True )
                        addnum.append(newAU) 
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        sels = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        if sels!=None:
            sel = list(set(sels))   
            for i in range(0,len(sel)):
                AWsel = cmds.listConnections(sel[i],d=0,type="aiWriteColor")
                if AWsel != None:
                    newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                    newAU = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(newAU + '.shadeMode',2)
                    cmds.setAttr(newAU + '.color', 0, 1, 0, type="double3")
                    cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                    cmds.connectAttr( newAW + '.outColor', sel[i] + '.color', f=True )
                    cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                    addnum.append(newAU)
    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            AWshadersel = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshadersel != None:
                newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                newAU = cmds.shadingNode('aiUtility', asShader=True)
                cmds.setAttr(newAU + '.shadeMode',2)
                cmds.setAttr(newAU + '.color', 0, 1, 0, type="double3")
                cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                cmds.connectAttr( newAW + '.outColor', shadersel[i] + '.color', f=True )
                cmds.connectAttr( AWshadersel[0] + '.outColor', newAW + '.beauty', f=True )
                addnum.append(newAU)
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
    if addnum!=None:
        print "已增加了"+str(len(addnum))+"个ＩＤ节点！！\n",      
def blueadd(arg):
    notype = ["nurbsCurve","follicle","transform"]
    addnum = []
    objsel =cmds.ls(sl=True,typ="transform")
    if objsel !=[]: 
        obj2shape = cmds.listRelatives(objsel,c=1) 
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
                            AWsel = cmds.listConnections(nhairshader[0],d=0,type="aiWriteColor")
                            newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                            newAU = cmds.shadingNode('aiUtility', asShader=True)
                            cmds.setAttr(newAU + '.shadeMode',2)
                            cmds.setAttr(newAU + '.color', 0, 0, 1, type="double3")
                            cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                            cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                            cmds.connectAttr( newAW + '.outColor', nhairshader[0] + '.color', f=True )
                            addnum.append(newAU)
            else:
                shaveshape = cmds.ls(obj2shapes[o],type="shaveHair")
                if shaveshape!=[]:
                    shaveshader = cmds.listConnections(shaveshape[0]+".aiHairShader")
                    if shaveshader!=None:
                        AWsel = cmds.listConnections(shaveshader[0],d=0,type="aiWriteColor")
                        newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                        newAU = cmds.shadingNode('aiUtility', asShader=True)
                        cmds.setAttr(newAU + '.shadeMode',2)
                        cmds.setAttr(newAU + '.color', 0, 0, 1, type="double3")
                        cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                        cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                        cmds.connectAttr( newAW + '.outColor', shaveshader[0] + '.color', f=True )
                        addnum.append(newAU) 
        shapes2SG = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        sels = cmds.listConnections(shapes2SG,d=0,type='aiUtility')
        if sels!=None:
            sel = list(set(sels))   
            for i in range(0,len(sel)):
                AWsel = cmds.listConnections(sel[i],d=0,type="aiWriteColor")
                if AWsel != None:
                    newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                    newAU = cmds.shadingNode('aiUtility', asShader=True)
                    cmds.setAttr(newAU + '.shadeMode',2)
                    cmds.setAttr(newAU + '.color', 0, 0, 1, type="double3")
                    cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                    cmds.connectAttr( newAW + '.outColor', sel[i] + '.color', f=True )
                    cmds.connectAttr( AWsel[0] + '.outColor', newAW + '.beauty', f=True )
                    addnum.append(newAU)
    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        for i in range(0,len(shadersel)):
            AWshadersel = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshadersel != None:
                newAW = cmds.shadingNode('aiWriteColor', asShader=True)
                newAU = cmds.shadingNode('aiUtility', asShader=True)
                cmds.setAttr(newAU + '.shadeMode',2)
                cmds.setAttr(newAU + '.color', 0, 0, 1, type="double3")
                cmds.connectAttr( newAU + '.outColor', newAW + '.input',f=True )
                cmds.connectAttr( newAW + '.outColor', shadersel[i] + '.color', f=True )
                cmds.connectAttr( AWshadersel[0] + '.outColor', newAW + '.beauty', f=True )
                addnum.append(newAU)
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
    if addnum!=None:
        print "已增加了"+str(len(addnum))+"个ＩＤ节点！！\n",      

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
            
##毛发
    ytAisel = cmds.ls(type="aiHair")
    ytytAoselset = []
    ytnmselset = []
    ytbygsel = []
    ytrgbRsel = []
    ytrgbGsel = []
    ytrgbBsel = []
    for i in range(len(ytAisel)):
        ytAWOP = []
        ytAWUOP= []
        ytopfile = cmds.listConnections(ytAisel[i]+".opacity",d=0)
        ytAiop = cmds.getAttr(ytAisel[i]+".opacity")
        if ytAiop !=[(1.0,1.0,1.0)]:
            ytAwsel = cmds.listConnections(ytAisel[i],s=0,type="aiWriteColor")
            cmds.setAttr(ytAwsel[0] +'.blend',1)
            ytAWOP.append(ytAwsel)
            ytAwsels = cmds.listConnections(ytAwsel,s=0,type="aiWriteColor")
            if ytAwsels!=None:
                cmds.setAttr(ytAwsels[0] +'.blend',1)
                ytAWOP.append(ytAwsels)
            while ytAwsels!=None:
                ytAwsels = cmds.listConnections(ytAwsels,s=0,type="aiWriteColor")
                ytAWOP.append(ytAwsels)
                if ytAwsels!=None:
                     cmds.setAttr(ytAwsels[0] +'.blend',1)
            ytnoneset =[None]
            ytAWOPs = [i for i in ytAWOP if i not in ytnoneset]
            for p in range(0,len(ytAWOPs)):
                ytAusel = cmds.listConnections(str(ytAWOPs[p][0])+".input",d=0,type="aiUtility")
                ytAosel = cmds.listConnections(str(ytAWOPs[p][0])+".input",d=0,type="aiAmbientOcclusion")  
                if ytAusel!=None:
                    ytAuseladj = cmds.isConnected(ytAisel[0]+'.opacity.opacityR',ytAusel[0]+'.opacity') 
                    if ytAuseladj==False:
                        cmds.connectAttr(ytAisel[0]+".opacity.opacityR",ytAusel[0]+".opacity",f=1)
                if  ytAosel!=None:
                    ytAoseladj = cmds.isConnected(ytAisel[0]+'.opacity',ytAosel[0]+'.opacity') 
                    if ytAoseladj==False:
                        cmds.connectAttr(ytAisel[0]+'.opacity',ytAosel[0]+'.opacity',f=1)
                if ytopfile!=None: 
                    cmds.setAttr(ytopfile[0]+'.alphaIsLuminance',1)
                    if ytAusel !=None:
                        if cmds.isConnected(ytopfile[0]+".outAlpha",ytAusel[0]+".opacity")==False:
                            cmds.connectAttr(ytopfile[0]+".outAlpha",ytAusel[0]+".opacity",f=1)
                    if ytAosel !=None:
                        if cmds.isConnected(ytopfile[0]+".outColor",ytAosel[0]+".opacity")==False:
                            cmds.connectAttr(ytopfile[0]+".outColor",ytAosel[0]+".opacity",f=1)
                ytAufinal = cmds.listConnections(str(ytAWOP[p][0])+".outColor",s=0,type="aiUtility")
                if ytAufinal!=None:
                    ytAufinal=cmds.listConnections(ytAufinal[0],s=0,type="shadingEngine")
                    ytshapesel = cmds.listConnections(ytAufinal[0],d=0,type="pgYetiMaya")
                    if ytshapesel !=None:
                        cmds.setAttr(ytshapesel[0] + ".aiOpaque",0)
        else:
            ytAwsel = cmds.listConnections(ytAisel[i],s=0,type="aiWriteColor")
            ytAWUOP.append(ytAwsel)
            ytAwsels = cmds.listConnections(ytAwsel,s=0,type="aiWriteColor")
            if ytAwsels!=None:
                ytAWUOP.append(ytAwsels)
            while ytAwsels!=None:
                ytAwsels = cmds.listConnections(ytAwsels,s=0,type="aiWriteColor")
                ytAWUOP.append(ytAwsels)
            ytnoneset =[None]
            ytAWUOPs = [i for i in ytAWUOP if i not in ytnoneset]
            for p in range(0,len(ytAWUOPs)):
                ytAosel = cmds.listConnections(str(ytAWUOPs[p][0])+".input",d=0,type="aiAmbientOcclusion")
                ytytAoselset.append(ytAosel)
                ytAusel = cmds.listConnections(str(ytAWUOPs[p][0])+".input",d=0,type="aiUtility")
                if ytAusel !=None:
                    ytOPramps = cmds.listConnections(str(ytAusel[0])+".color",d=0,type="ramp")
                    if ytOPramps !=None:
                        ytbygsel.append(ytAusel)
                    else:
                        ytOPcmode = cmds.getAttr(ytAusel[0]+".colorMode")
                        if ytOPcmode == 3:
                            ytnmselset.append(ytAusel)
                        else:
                            ytcoloradj = cmds.getAttr(ytAusel[0]+".color")
                            if ytcoloradj[0] == (1,0,0):
                                ytrgbRsel.append(ytAusel)
                            if ytcoloradj[0]== (0,1,0):
                                ytrgbGsel.append(ytAusel)
                            if ytcoloradj[0]== (0,0,1):
                                ytrgbBsel.append(ytAusel)
                                
    ytnoneset =[None]
    ytytAoselsets = [i for i in ytytAoselset if i not in ytnoneset]
    ytnmselsets = [i for i in ytnmselset if i not in ytnoneset]
    ytbygsels = [i for i in ytbygsel if i not in ytnoneset]
    ytrgbRsels = [i for i in ytrgbRsel if i not in ytnoneset]
    ytrgbGsels = [i for i in ytrgbGsel if i not in ytnoneset]
    ytrgbBsels = [i for i in ytrgbBsel if i not in ytnoneset]
    
    if ytytAoselsets !=None:
        for i in range(1,len(ytytAoselsets)):
            ytAwsel = cmds.listConnections(ytytAoselsets[i],s=0,type="aiWriteColor")
            ytAwseladj = cmds.isConnected(str(ytytAoselsets[0][0])+".outColor",str(ytAwsel[0])+".input")
            if ytAwseladj!=True:
                cmds.connectAttr(str(ytytAoselsets[0][0])+".outColor",str(ytAwsel[0])+".input",f=1)
    if ytnmselsets !=None:
        for i in range(1,len(ytnmselsets)):
            ytAwsel = cmds.listConnections(ytnmselsets[i],s=0,type="aiWriteColor")
            ytAwseladj = cmds.isConnected(str(ytnmselsets[0][0])+".outColor",str(ytAwsel[0])+".input")
            if ytAwseladj!=True:
                cmds.connectAttr(str(ytnmselsets[0][0])+".outColor",str(ytAwsel[0])+".input",f=1)
    if ytbygsels !=None:
        for i in range(1,len(ytbygsels)):
            ytAwsel = cmds.listConnections(ytbygsels[i],s=0,type="aiWriteColor")
            ytAwseladj = cmds.isConnected(str(ytbygsels[0][0])+".outColor",str(ytAwsel[0])+".input")
            if ytAwseladj!=True:
                cmds.connectAttr(str(ytbygsels[0][0])+".outColor",str(ytAwsel[0])+".input",f=1)
    if ytrgbRsels !=None:
        for i in range(1,len(ytrgbRsels)):
            ytAwsel = cmds.listConnections(ytrgbRsels[i],s=0,type="aiWriteColor")
            ytAwseladj = cmds.isConnected(str(ytrgbRsels[0][0])+".outColor",str(ytAwsel[0])+".input")
            if ytAwseladj!=True:
                cmds.connectAttr(str(ytrgbRsels[0][0])+".outColor",str(ytAwsel[0])+".input",f=1)
    if ytrgbGsels !=None:
        for i in range(1,len(ytrgbGsels)):
            ytAwsel = cmds.listConnections(ytrgbGsels[i],s=0,type="aiWriteColor")
            ytAwseladj = cmds.isConnected(str(ytrgbGsels[0][0])+".outColor",str(ytAwsel[0])+".input")
            if ytAwseladj!=True:
                cmds.connectAttr(str(ytrgbGsels[0][0])+".outColor",str(ytAwsel[0])+".input",f=1)
    if ytrgbBsels !=None:
        for i in range(1,len(ytrgbBsels)):
            ytAwsel = cmds.listConnections(ytrgbBsels[i],s=0,type="aiWriteColor")
            ytAwseladj = cmds.isConnected(str(ytrgbBsels[0][0])+".outColor",str(ytAwsel[0])+".input")
            if ytAwseladj!=True:
                cmds.connectAttr(str(ytrgbBsels[0][0])+".outColor",str(ytAwsel[0])+".input",f=1)           
##皮肤
    skAisel = cmds.ls(type="aiSkin")
    skskAoselset = []
    sknmselset = []
    skbygsel = []
    skrgbRsel = []
    skrgbGsel = []
    skrgbBsel = []
    for i in range(len(skAisel)):
        skAWOP = []
        skAWUOP= []
        skopfile = cmds.listConnections(skAisel[i]+".opacity",d=0)
        skAiop = cmds.getAttr(skAisel[i]+".opacity")
        skAiopc = cmds.getAttr(skAisel[i]+".opacityColor")
        if skAiop !=[(1.0,1.0,1.0)] and skAiopc !=[(1.0,1.0,1.0)]:
            print "yse"
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
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel", "deleteUnusedNodes");') 
def AWselect(arg):        
    nodetyp = ["aiStandard","aiSkin","layeredShader","aiHair","alHair","alLayer","alSurface"]
    mtsel = cmds.ls(mat=1)
    objsel = cmds.ls(sl=True,typ="transform")
    onlyread = ["initialShadingGroup","lambert1","particleCloud1","initialParticleSE"]
    if objsel !=[]:
        AWsel = [] 
        obj2shapes = cmds.listRelatives(objsel)
        shapes2SGs = cmds.listConnections(obj2shapes,s=0,type='shadingEngine')
        shapes2SG = [i for i in shapes2SGs if i not in onlyread]
        SG2sel = cmds.listConnections(shapes2SG,d=0)
        SG2Ai = [i for i in mtsel if i in SG2sel]
        SG2AiRe = list(set(SG2Ai))
        for i in range(0,len(SG2AiRe)):
            AWselo = cmds.listConnections(SG2AiRe[i],d=0,type="aiWriteColor")
            AWsel.append(AWselo)
            if AWselo!=None:
                AWselos = cmds.listConnections(AWselo[0],d=0,type="aiWriteColor")
                if AWselos!=None:
                    AWsel.append(AWselos)
                while AWselos!=None:
                    AWselos = cmds.listConnections(AWselos[0],d=0,type="aiWriteColor")
                    AWsel.append(AWselos)
        noneset =[None]
        AWsels = [i for i in AWsel if i not in noneset]
        cmds.select(cl=1)
        for i in range(len(AWsels)):
            cmds.select(AWsels[i][0],add=1)
    shadersel = cmds.ls(sl=1,type = "aiUtility")
    if shadersel!=[]:
        AWshadersel = [] 
        for i in range(0,len(shadersel)):
            AWshaderselo = cmds.listConnections(shadersel[i],d=0,type="aiWriteColor")
            if AWshaderselo != None:
                AWshadersel.append(AWshaderselo)
                AWshaderselos = cmds.listConnections(AWshaderselo[0],d=0,type="aiWriteColor")
                if AWshaderselos!=None:
                    AWshadersel.append(AWshaderselos)
                while AWshaderselos!=None:
                    AWshaderselos = cmds.listConnections(AWshaderselos[0],d=0,type="aiWriteColor")
                    AWshadersel.append(AWshaderselos)
        noneset =[None]
        AWshadersels = [i for i in AWshadersel if i not in noneset]
        cmds.select(cl=1)
        for i in range(len(AWshadersels)):
            cmds.select(AWshadersels[i][0],add=1)
                    
    if shadersel ==[] and objsel==[]:
        cmds.warning("没有选择模型或“aiUtility”节点")
def changeAovsname(arg):
    value=cmds.textField('cmmaov',q=True,tx=True)
    sel = cmds.ls(sl= 1)
    for i in range(0,len(sel)):
        cmds.setAttr(sel[i]+'.aovName',value,type="string")
def reNmae(arg):
    value=cmds.textField('cmmaov',q=True,tx=True)
    rname=cmds.ls(typ=("layeredTexture","remapColor","reverse","remapHsv","aiAmbientOcclusion","aiImage","alSurface","layeredShader","alHair","alLayer",'aiUtility','aiStandard','aiWriteColor','file','place2dTexture','displacementShader','bump2d','shadingEngine','ramp','blendColors','condition','gammaCorrect','luminance','samplerInfo','surfaceLuminance','aiSkin','aiHair'))
    ron=["initialParticleSE","initialShadingGroup"]
    ret = [i for i in rname if i not in ron]
    for n in range(0,len(ret)):
            cmds.rename(ret[n],value)  
def filepathbtn(arg):
    filepath = cmds.file(q=1,exn=1)
    myFile = os.path.basename(filepath)
    filename = os.path.splitext(myFile)[0]
    path = cmds.textField('pathfilecmm',q=True,tx=True)
    newpath = path+"/"+filename+".txt"
    p=open(newpath,"w+")
    com = []
    filesel = cmds.ls(type="file")
    for i in range(len(filesel)):
        oldpath = cmds.getAttr(filesel[i]+".fileTextureName")
        olddirpath = os.path.dirname(oldpath)
        com.append(olddirpath)
        print com
    if com!=None:
        coms =list(set(com))
        for a in range(len(coms)):
            p.write(coms[a]+"; \n")
        p.close()
def aovrebuild(arg):
	aiAov = cmds.ls(type="aiAOV")
	for i in range(len(aiAov)):
	    aovadj = cmds.listConnections(aiAov[i]+".message",s=0,type="aiOptions")
	    if aovadj ==None:
	        cmds.delete(aiAov[i])
	AWsel = cmds.ls(type="aiWriteColor")
	if AWsel !=[]:
		aovname=list(set([cmds.getAttr(i+".aovName") for i in AWsel if len(cmds.getAttr(i+".aovName").split("("))==1]))
		aovnode = ["aiAOV_"+i for i in aovname]
		for a in range(len(aovname)):
			if cmds.objExists(aovnode[a])==False:
				aovs.AOVInterface().addAOV(aovname[a], aovType='rgba')
			else:
				aovadj = cmds.listConnections(aovnode[a]+".message",s=0,type="aiOptions")
				if aovadj==[]:
					aovs.AOVInterface().addAOV(aovname[a], aovType='rgba')

def reaov(arg):
    value=cmds.textField('cmmaov',q=True,tx=True)
    rname=cmds.ls(typ=('aiUtility','aiStandard','aiWriteColor','file','place2dTexture','displacementShader','bump2d','shadingEngine','ramp','blendColors','condition','gammaCorrect','luminance','samplerInfo','surfaceLuminance','aiSkin','aiHair'))
    ron=["initialParticleSE","initialShadingGroup"]
    ret = [i for i in rname if i not in ron]
    aovs.AOVInterface().addAOV(value, aovType='rgba')
    aovsel=cmds.ls(typ='aiWriteColor')
    for a in range(0,len(aovsel)):
        cmds.setAttr(aovsel[a]+'.aovName',value,type="string")    
        
def SJ_arnoldIDToolwdUI()   :   
	if cmds.window('arnoldIDtool',ex=True):
	    cmds.deleteUI('arnoldIDtool',wnd=True)
	cmds.window('arnoldIDtool',t='ArnoldIDtoolV1.0')
	cmds.columnLayout(adj=True)
	cmds.text(l='Arnold材质工具V1.0',fn='fixedWidthFont',h=50,annotation="V1.0更新说明：整合ID生成和ID修改工具。")
	cmds.text(l='ID生成',fn='fixedWidthFont',h=30,annotation="")
	cmds.flowLayout( columnSpacing=0)
	cmds.button(l='红色ID生成',c=redobj,bgc=[1,0.5,0.5],h=50,w=120,annotation="选择模型或者材质增加红色ID")
	cmds.button(l='蓝色ID生成',c=blueobj,bgc=[0.5,0.5,1],h=50,w=120,annotation="选择模型或者材质增加蓝色ID")
	cmds.button(l='绿色ID生成',c=greenobj,bgc=[0.5,1,0.5],h=50,w=120,annotation="选择模型或者材质增加绿色ID")
	cmds.setParent( '..' )
	cmds.text(l='ID添加',fn='fixedWidthFont',h=30,annotation="")
	cmds.flowLayout( columnSpacing=0)
	cmds.button(l='添加红色ID',c=redadd,bgc=[1,0.5,0.5],h=50,w=120,annotation="选择模型或者材质增加红色ID")
	cmds.button(l='添加蓝色ID',c=blueadd,bgc=[0.5,0.5,1],h=50,w=120,annotation="选择模型或者材质增加蓝色ID")
	cmds.button(l='添加绿色ID',c=greenadd,bgc=[0.5,1,0.5],h=50,w=120,annotation="选择模型或者材质增加绿色ID")
	cmds.setParent( '..' )
	cmds.flowLayout( columnSpacing=0)
	cmds.button(l='添加OCCID',c=occ,bgc=[0.8,0.8,0.8],h=50,w=120,annotation="选择模型或者材质增加occID")
	cmds.button(l='添加normalID',c=norm,bgc=[0.8,0.6,1],h=50,w=120,annotation="选择模型或者材质增加normalID")
	cmds.button(l='添加BYGID',c=byg,bgc=[0,0.3,0.9],h=50,w=120,annotation="选择模型或者材质增加BYGID")
	cmds.setParent( '..' )
	cmds.button(l='一键处理所有透明物体属性 \n 并合并不透明物体的相同属性ID球',c=opset,bgc=[0.3,0.6,0.6],h=50,annotation="(1) 将透明贴图的Alpha Is　Luminance选项勾上 \n(2)将透明模型的opaque选项去除 \n(3)将透明贴图连接到ID节点的opacity上 \n(4)将透明物体的aiWriteColor的blend选项勾上 \n(5)合并不透明物体相同属性的ＩＤ材质（例如：将红色ID合并），减少文件量")
	cmds.button(l='智能选择aiWriteColor节点',h=50,c=AWselect,bgc=[0.88,0.7,0.6],ann="通过模型或材质选择相关联的aiWriteColor节点")
	cmds.button(l=' 一键恢复Aovs渲染层',h=50,c=aovrebuild,bgc=[0.9,0.74,0.4],ann="修复导abc丢失aov渲染层问题")
	cmds.textField('cmmaov',tx="AOVsIDname",h=30,annotation="请输入需要修改的名字")
	cmds.button(l='创建Aovs渲染层， \n 指定ID渲染层',c=reaov,h=50,bgc=[1,1,0.7])
	cmds.button(l='批量修改aiWriteColor的Aovs名字',c=changeAovsname,bgc=[1,1,0.5],h=50,annotation="选择aiWriteColor节点")
	cmds.button(l='重命名所有材质节点',h=50,c=reNmae,bgc=[0.521,0.764,0.980],ann="重命名节点类型:'layeredTexture','remapColor','reverse','remapHsv','aiAmbientOcclusion','aiImage','alSurface','layeredShader','alHair','alLayer','aiUtility','aiStandard','aiWriteColor',\n'file','place2dTexture','displacementShader','bump2d','shadingEngine','ramp','blendColors','condition','gammaCorrect','luminance','samplerInfo','surfaceLuminance','aiSkin','aiHair'")
	cmds.textField('pathfilecmm',tx="D:\\filepath",h=30,ann="输入txt文件输出路径")
	cmds.button(l='输出file节点贴图路径到txt',c =filepathbtn,h=50,bgc=[1,0.7,0.5])
	cmds.showWindow()