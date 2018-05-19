#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-09-21

import maya.cmds as cmds
import math
import os
from pymel import versions

def SJ_convertSelection():
    """
    Loops through the selection and attempts to create arnold shaders on whatever it finds
    """
    if versions.current()>=201700:
        targetShs = ['aiStandard', 'aiHair', 'alSurface', 'alHair']
    else:
        targetShs = ["aiSkin"]
    sel = cmds.ls(sl=True,exactType=targetShs)
    if sel:
        for s in sel:
            ret = SJ_doMapping(s)

def SJ_convertAlltypeShaders():
    """
    Converts each Target Type (in-use) material in the scene
    """
    # better to loop over the types instead of calling
    # ls -type targetShader
    # if a shader in the list is not registered (i.e. VrayMtl)
    # everything would fail
    targetShaders = ['aiStandard', 'aiHair', 'alSurface', 'alHair',"aiSkin"]
    sels =[cmds.nodeType(a) for  a in cmds.ls(sl=1)]
    newTargetShaders =  list(set(sels)&set(targetShaders))
    for shdType in newTargetShaders:
        shaderColl = cmds.ls(exactType=shdType)
        if shaderColl:
            for x in shaderColl:
                print x
                # query the objects assigned to the shader
                # only convert things with members
                #shdGroup = cmds.listConnections(x, type="shadingEngine")
                #setMem = cmds.sets( shdGroup, query=True )
                #if setMem:
                SJ_doMapping(x)
                
               
                

def SJ_doMapping(inShd):
    """
    Figures out which attribute mapping to use, and does the thing.
    
    @param inShd: Shader name
    @type inShd: String
    """
    ret = None
    
    shaderType = cmds.objectType(inShd)
    #print shaderType
    if 'aiStandard' in shaderType :
        ret = SJ_convertAiStandard(inShd)
    elif 'aiHair' in shaderType :
        ret = SJ_convertAiHair(inShd)
    elif 'alHair' in shaderType:
        ret = SJ_convertAlHair(inShd)
    elif 'alSurface' in shaderType:
        ret = SJ_convertAlSurface(inShd)
    elif 'aiSkin' in shaderType:
        ret = SJ_convertAiStandardsss(inShd)
    if ret:
        # assign objects to the new shader
        SJ_assignToNewShader(inShd, ret)

def SJ_assignToNewShader(oldShd, newShd):

    replaceShaders = True

    if ':' in oldShd:
        aiName = oldShd.rsplit(':')[-1] + '_old'
    else:
        aiName = oldShd + '_old'
    
    cmds.rename(oldShd, aiName)
    cmds.rename(newShd, oldShd)

    newShd = oldShd
    oldShd = aiName

    """
    Creates a shading group for the new shader, and assigns members of the old shader to it
    
    @param oldShd: Old shader to upgrade
    @type oldShd: String
    @param newShd: New shader
    @type newShd: String
    """
    
    retVal = False
    
    shdGroups = cmds.listConnections(oldShd + '.outColor', plugs=True)
    
    #print 'shdGroup:', shdGroup
    if shdGroups != None:    
        for shdGroup in  shdGroups:
            cmds.connectAttr(newShd + '.outColor', shdGroup, force=True)
            retVal =True

    if replaceShaders:
        cmds.delete(oldShd)        
    return retVal


def SJ_setupConnections(inShd, fromAttr, outShd, toAttr,mode=None):
    conns = cmds.listConnections( inShd + '.' + fromAttr, d=False, s=True, plugs=True )
    if conns:
        #print 'has connections'
        if mode =="aiStandardsss":
            print inShd, fromAttr, outShd, toAttr
            if conns[0].find("outColor")!=-1:
                cmds.connectAttr(conns[0], outShd + '.' + toAttr, force=True)
                filebase = conns[0].split(".")[0]
                if cmds.nodeType(filebase)=="file":
                    a,b,c = cmds.getAttr(filebase+".colorGain")[0]
                    a1,b1,c1 = 0.216,0.447,0.538
                    cmds.setAttr(filebase+".colorGain",a-a1,b-b1,c-c1,type="double3")
                    while  cmds.listConnections(filebase+".defaultColor",d=0)!=None:
                        filebase = cmds.listConnections(filebase+".defaultColor",d=0)[0]
                        cmds.setAttr(filebase+".colorGain",a-a1,b-b1,c-c1,type="double3")
            else:
                cmds.connectAttr(conns[0], outShd + '.' + toAttr, force=True)
        elif mode =="alSurface":
            if conns[0].find("outColor")!=-1:
                remapNode = cmds.shadingNode('alRemapColor', name=outShd+"_remapColor", asUtility=True)
                cmds.setAttr(remapNode+".gamma",0.5)
                cmds.connectAttr(conns[0], remapNode + '.input', force=True)
                cmds.connectAttr(remapNode + '.outColor', outShd + '.' + toAttr, force=True)
            else:
                cmds.connectAttr(conns[0], outShd + '.' + toAttr, force=True)
        else:
            cmds.connectAttr(conns[0], outShd + '.' + toAttr, force=True)
        return True
    else:
        return False



def SJ_convertAiStandard(inShd):
    if ':' in inShd:
        aiName = inShd.rsplit(':')[-1] + '_new'
    else:
        aiName = inShd + '_new'
    
    
    #print 'creating '+ aiName
    outNode = cmds.shadingNode('aiStandardSurface', name=aiName, asShader=True)
    

    SJ_convertAttr(inShd, 'Kd', outNode, 'base')
    SJ_convertAttr(inShd, 'color', outNode, 'baseColor')
    SJ_convertAttr(inShd, 'diffuseRoughness', outNode, 'diffuseRoughness')

    SJ_convertAttr(inShd, 'Ks', outNode, 'specular')
    SJ_convertAttr(inShd, 'KsColor', outNode, 'specularColor')
    SJ_convertAttr(inShd, 'specularRoughness', outNode, 'specularRoughness')

    fresnel = cmds.getAttr(inShd + '.Fresnel')
    fresnel_use_ior = cmds.getAttr(inShd + '.Fresnel_use_IOR')
    specular_Fresnel = cmds.getAttr(inShd + '.specular_Fresnel')

    if int(fresnel) > 0:
        if int(fresnel_use_ior) > 0:
            SJ_convertAttr(inShd, 'IOR', outNode, 'specular_IOR')
        else:
            SJ_convertAttr(inShd, 'Krn', outNode, 'specular_IOR', krnToIorRemap)

    if int(specular_Fresnel) > 0:
        if int(fresnel_use_ior) > 0:
            SJ_convertAttr(inShd, 'IOR', outNode, 'coat_IOR')
        else:
            SJ_convertAttr(inShd, 'Ksn', outNode, 'coat_IOR', krnToIorRemap)

    SJ_convertAttr(inShd, 'specularAnisotropy', outNode, 'specularAnisotropy', anisotropyRemap)

    SJ_convertAttr(inShd, 'specularRotation', outNode, 'specularRotation', rotationRemap)
    SJ_convertAttr(inShd, 'Kt', outNode, 'transmission')

    SJ_convertAttr(inShd, 'KtColor', outNode, 'transmissionColor') # not multiplying by transmittance

    # transmission_depth => (transmittance == AI_RGB_WHITE) ? 0.0 : 1.0
    SJ_convertAttr(inShd, 'dispersionAbbe', outNode, 'transmissionDispersion') # not multiplying by transmittance    

    # transmission_extra_roughness => refraction_roughness - specular_roughness    

    SJ_convertAttr(inShd, 'Ksss', outNode, 'subsurface')
    SJ_convertAttr(inShd, 'KsssColor', outNode, 'subsurfaceColor')
    SJ_convertAttr(inShd, 'sssRadius', outNode, 'subsurfaceRadius')

    SJ_convertAttr(inShd, 'Kr', outNode, 'coat')
    SJ_convertAttr(inShd, 'KrColor', outNode, 'coatColor')
    cmds.setAttr(outNode + '.coat_roughness', 0)


    SJ_convertAttr(inShd, 'emission', outNode, 'emission')
    SJ_convertAttr(inShd, 'emissionColor', outNode, 'emissionColor')
    SJ_convertAttr(inShd, 'opacity', outNode, 'opacity')

    # caustics => enable_glossy_caustics || enable_reflective_caustics || enable_refractive_caustics
    SJ_convertAttr(inShd, 'enable_internal_reflections', outNode, 'internal_reflections')
    SJ_convertAttr(inShd, 'indirect_diffuse', outNode, 'indirect_diffuse')
    SJ_convertAttr(inShd, 'indirect_specular', outNode, 'indirect_specular')
    # exit_to_background => reflection_exit_use_environment || refraction_exit_use_environment

    SJ_convertAttr(inShd, 'normalCamera', outNode, 'normalCamera') # not multiplying by transmittance
    print "Converted %s to aiStandardSurface" % inShd
    return outNode


def SJ_convertAiHair(inShd):
    if ':' in inShd:
        aiName = inShd.rsplit(':')[-1] + '_new'
    else:
        aiName = inShd + '_new'    
    
    outNode = cmds.shadingNode('aiStandardHair', name=aiName, asShader=True)
    SJ_convertAttr(inShd, 'tipcolor', outNode, 'base_color') #not converting root_color here
    SJ_convertAttr(inShd, 'KdInd', outNode, 'indirect_diffuse')
    #SJ_convertAttr(inShd, 'spec', outNode, 'specular')
    SJ_convertAttr(inShd, 'specColor', outNode, 'specular_tint')
    #SJ_convertAttr(inShd, 'spec2', outNode, 'specular2')
    SJ_convertAttr(inShd, 'spec2Color', outNode, 'specular2_tint')
    SJ_convertAttr(inShd, 'specGloss', outNode, 'roughness', glossRemap)
    SJ_convertAttr(inShd, 'specShift', outNode, 'shift', shiftRemap)
    SJ_convertAttr(inShd, 'transmission_color', outNode, 'transmission_tint')
    SJ_convertAttr(inShd, 'opacity', outNode, 'opacity')

    cmds.setAttr(outNode + '.melanin', 0)

    print "Converted %s to aiStandardHair" % inShd
    return outNode

def SJ_convertAlSurface(inShd):
    if ':' in inShd:
        aiName = inShd.rsplit(':')[-1] + '_new'
    else:
        aiName = inShd + '_new'

    #print 'creating '+ aiName
    outNode = cmds.shadingNode('aiStandardSurface', name=aiName, asShader=True)
    
    SJ_convertAttr(inShd, 'diffuseStrength', outNode, 'base',None,"alSurface")
    SJ_convertAttr(inShd, 'diffuseColor', outNode, 'baseColor',None,"alSurface")
    
    SJ_convertAttr(inShd, 'diffuseRoughness', outNode, 'diffuseRoughness',None,"alSurface")
    
    SJ_convertAttr(inShd, 'sssMix', outNode, 'subsurface',None,"alSurface")
    sssmixcon =cmds.listConnections(inShd+".sssMix",d=0,plugs=1)
    if sssmixcon!=None:
        SJ_convertAttr(inShd, 'diffuseColor', outNode, 'subsurfaceColor',None,"alSurface")
    else:
        if cmds.getAttr(inShd+".sssMix")>0:
            SJ_convertAttr(inShd, 'diffuseColor', outNode, 'subsurfaceColor',None,"alSurface")
    SJ_convertAttr(inShd, 'sssDensityScale', outNode, 'subsurfaceScale',SJ_shiftSssScale)
    SJ_convertAttr(inShd, 'sssRadiusColor2', outNode, 'subsurfaceRadius')
    SJ_convertAttr(inShd, 'specular1Strength', outNode, 'specular')
    SJ_convertAttr(inShd, 'specular1Color', outNode, 'specularColor',None,"alSurface")
    SJ_convertAttr(inShd, 'specular1Roughness', outNode, 'specularRoughness')
    SJ_convertAttr(inShd, 'specular1Anisotropy', outNode, 'specularAnisotropy')
    SJ_convertAttr(inShd, 'specular1Rotation', outNode, 'specularRotation')
    SJ_convertAttr(inShd, 'specular1Ior', outNode, 'specularIOR')
    SJ_convertAttr(inShd, 'specular2Strength', outNode, 'coat')
    SJ_convertAttr(inShd, 'specular2Color', outNode, 'coatColor',None,"alSurface")
    SJ_convertAttr(inShd, 'specular2Roughness', outNode, 'coatRoughness')
    SJ_convertAttr(inShd, 'specular2Ior', outNode, 'coatIOR')
    SJ_convertAttr(inShd, 'specular2Normal', outNode, 'coatNormal')
    SJ_convertAttr(inShd, 'transmissionStrength', outNode, 'transmission')
    SJ_convertAttr(inShd, 'transmissionColor', outNode, 'transmissionColor',None,"alSurface")
    SJ_convertAttr(inShd, 'transmissionRoughness', outNode, 'transmissionExtraRoughness')
    SJ_convertAttr(inShd, 'ssAttenuationColor', outNode, 'transmissionScatter')
    SJ_convertAttr(inShd, 'ssInScatteringStrength', outNode, 'transmissionDepth')
    SJ_convertAttr(inShd, 'ssDirection', outNode, 'transmissionScatterAnisotropy')
    SJ_convertAttr(inShd, 'emissionStrength', outNode, 'emission')
    SJ_convertAttr(inShd, 'emissionColor', outNode, 'emissionColor',None,"alSurface")
    SJ_convertAttr(inShd, 'opacity', outNode, 'opacity')
    SJ_convertAttr(inShd, 'normalCamera', outNode, 'normalCamera')

    print "Converted %s to aiStandardSurface" % inShd
    return outNode


def SJ_convertAlHair(inShd):
    if ':' in inShd:
        aiName = inShd.rsplit(':')[-1] + '_new'
    else:
        aiName = inShd + '_new'    
    
    outNode = cmds.shadingNode('aiStandardHair', name=aiName, asShader=True)

    SJ_convertAttr(inShd, 'dyeColor', outNode, 'baseColor')
    SJ_convertAttr(inShd, 'melanin', outNode, 'melanin')
    SJ_convertAttr(inShd, 'opacity', outNode, 'opacity')
    SJ_convertAttr(inShd, 'randomMelanin', outNode, 'melaninRandomize')
    SJ_convertAttr(inShd, 'diffuseStrength', outNode, 'diffuse')
    SJ_convertAttr(inShd, 'diffuseColor', outNode, 'diffuseColor')
    
    print "Converted %s to aiStandardHair" % inShd
    return outNode

        
def SJ_anisotropyRemap(val):
    return 2 * abs(val -0.5)

def SJ_rotationRemap(val):
    return 0.5 * val

def SJ_krnToIorRemap(val):
    
    if val > 0.99999:
        ior = 0.9999
    elif val < 0.0:
        ior = 0.0
    else:
        ior = val

    val_A = math.sqrt(ior)
    return (val_A + 1.0) / (1.0 - val_A)

def SJ_glossRemap(val):
    val =math.pow(float(val), float(-0.355))
    val *=  0.9928 
    
    if (val > 1):
        return 1

    return val

def SJ_shiftRemap(val):
    return 0.5 - (val/180.0)
    
def SJ_shiftSssScale(val):
    return 0.005

def SJ_convertAttr(inNode, inAttr, outNode, outAttr, functionPtr = None,mode=None):

    if cmds.objExists(inNode + '.' + inAttr):
        #print '\t', inAttr, ' -> ', outAttr
        
        if not SJ_setupConnections(inNode, inAttr, outNode, outAttr,mode):
            # copy the values
            val = cmds.getAttr(inNode + '.' + inAttr)
            if functionPtr:
                val = functionPtr(val)
                
            SJ_setValue(outNode + '.' + outAttr, val)

            attrType = cmds.getAttr(inNode + '.' + inAttr, type=True)
            if attrType in ['float3']:
                subAttr = inAttr + '.' + inAttr + 'R'
                if cmds.objExists(inNode + '.' + subAttr):
                    SJ_setupConnections(inNode, subAttr, outNode, outAttr + '.' + outAttr + 'R',mode)

                subAttr = inAttr + '.' + inAttr + 'G'
                if cmds.objExists(inNode + '.' + subAttr):
                    SJ_setupConnections(inNode, subAttr, outNode, outAttr + '.' + outAttr + 'G',mode)

                subAttr = inAttr + '.' + inAttr + 'B'
                if cmds.objExists(inNode + '.' + subAttr):
                    SJ_setupConnections(inNode, subAttr, outNode, outAttr + '.' + outAttr + 'B',mode)

                subAttr = inAttr + 'X'
                if cmds.objExists(inNode + '.' + subAttr):
                    SJ_setupConnections(inNode, subAttr, outNode, outAttr + 'X',mode)

                subAttr = inAttr + 'Y'
                if cmds.objExists(inNode + '.' + subAttr):
                    SJ_setupConnections(inNode, subAttr, outNode, outAttr + 'Y',mode)

                subAttr = inAttr + 'Z'
                if cmds.objExists(inNode + '.' + subAttr):
                    SJ_setupConnections(inNode, subAttr, outNode, outAttr + 'Z',mode)



def SJ_setValue(attr, value):
    """Simplified set attribute function.

    @param attr: Attribute to set. Type will be queried dynamically
    @param value: Value to set to. Should be compatible with the attr type.
    """

    aType = None
    
    if cmds.objExists(attr):
        attrType = cmds.getAttr(attr, type=True)
        # temporarily unlock the attribute
        isLocked = cmds.getAttr(attr, lock=True)
        if isLocked:
            cmds.setAttr(attr, lock=False)

        # one last check to see if we can write to it
        if cmds.getAttr(attr, settable=True):
            attrType = cmds.getAttr(attr, type=True)
            
            #print value, type(value)
            
            if attrType in ['string']:
                aType = 'string'
                cmds.setAttr(attr, value, type=aType)
                
            elif attrType in ['long', 'short', 'float', 'byte', 'double', 'doubleAngle', 'doubleLinear', 'bool']:
                aType = None
                cmds.setAttr(attr, value)
                
            elif attrType in ['long2', 'short2', 'float2',  'double2', 'long3', 'short3', 'float3',  'double3']:
                if isinstance(value, float):
                    if attrType in ['long2', 'short2', 'float2',  'double2']:
                        value = [(value,value)]
                    elif attrType in ['long3', 'short3', 'float3',  'double3']:
                        value = [(value, value, value)]
                        
                cmds.setAttr(attr, *value[0], type=attrType)

        if isLocked:
            # restore the lock on the attr
            cmds.setAttr(attr, lock=True)

    
def SJ_convertAiStandardsss(inShd):
    if ':' in inShd:
        aiName = inShd.rsplit(':')[-1] + '_new'
    else:
        aiName = inShd + '_new'
    #print 'creating '+ aiName
    outNode = cmds.shadingNode('aiStandard', name=aiName, asShader=True)
    SJ_convertAttr(inShd, 'deepScatterColor', outNode, 'KsssColor',None,"aiStandardsss")
    SJ_convertAttr(inShd, 'shallowScatterColor', outNode, 'color',None,"aiStandardsss")
    SJ_convertAttr(inShd, 'specularWeight', outNode, 'Ks',None,"aiStandardsss")
    SJ_convertAttr(inShd, 'normalCamera', outNode, 'normalCamera')
    cmds.setAttr(outNode+".Kd",0.5)
    cmds.setAttr(outNode+".specularRoughness",0.580)
    cmds.setAttr(outNode+".specularDistribution",1)
    cmds.setAttr(outNode+".specularFresnel",1)
    cmds.setAttr(outNode+".Ksn",0.25)
    cmds.setAttr(outNode+".specularFresnel",1)
    cmds.setAttr(outNode+".Ksss",1)
    cmds.setAttr(outNode+".sssRadius",0.197,0,0,type="double3")
    cmds.setAttr(outNode+".sssProfile",0)
    conouts = cmds.listConnections(inShd+".outColor",s=0,plugs=1)[0]
    cmds.connectAttr(outNode+".outColor",conouts,f=1)
    print "Converted %s to aiStandardSSS" % inShd
    return outNode   

def fixedID():
    AUsels = [{cmds.listConnections(a+".surfaceShader",d=0,type="aiUtility")[0]:a} for a in cmds.ls(type="shadingEngine") if cmds.listConnections(a+".surfaceShader",d=0,type="aiUtility")!=None]
    for AUsel in AUsels:
        if cmds.listConnections(AUsel.keys()[0]+".color",plugs=1,d=0)!=None:
            AWsel =  cmds.listConnections(AUsel.keys()[0]+".color",plugs=1,d=0)[0]
            if cmds.isConnected(AWsel,AUsel.values()[0]+".aiSurfaceShader")==False:
                cmds.connectAttr(AWsel,AUsel.values()[0]+".aiSurfaceShader",f=1)
            
    hairAUsels = [{cmds.listConnections(a+".aiHairShader",d=0,type="aiUtility")[0]:a} for a in cmds.ls(type="hairSystem") if cmds.listConnections(a+".aiHairShader",d=0,type="aiUtility")!=None]
    for hairAUsel in hairAUsels:
        if cmds.listConnections(hairAUsel.keys()[0]+".color",plugs=1,d=0)!=None:
            hairAWsel =  cmds.listConnections(hairAUsel.keys()[0]+".color",plugs=1,d=0)[0]
            if cmds.isConnected(hairAWsel,hairAUsel.values()[0]+".aiHairShader")==False:
                cmds.connectAttr(hairAWsel,hairAUsel.values()[0]+".aiHairShader",f=1)

def filecolorfix():
    filesels =cmds.ls(type="file")
    aists = cmds.ls(type="aiStandard")
    adjfiles =[]
    for aist in aists:
        if cmds.getAttr(aist+".Kr")>0 and cmds.getAttr(aist+".Fresnel"):
            adjfiles+= cmds.ls(cmds.hyperShade(lun=aist),type="file")
    adjfiles=list(set(adjfiles))
    for filesel in filesels:
        if cmds.listConnections(filesel,s=0,type="bump2d")!=None:
            if cmds.listConnections(filesel+".outColor",s=0)==None:
                cmds.setAttr(filesel+".colorSpace","Raw",type="string")
            else:
                cmds.setAttr(filesel+".colorSpace","sRGB",type="string")
        elif cmds.listConnections(filesel,s=0,type="displacementShader")!=None:
            cmds.setAttr(filesel+".colorSpace","Raw",type="string")
        else:
            if os.path.splitext(cmds.getAttr(filesel+".fileTextureName"))[-1]!=".hdr":
                cmds.setAttr(filesel+".colorSpace","sRGB",type="string")
                if cmds.listConnections(filesel+".outColor",s=0,type="alRemapColor")==None:
                    trattrs = cmds.listConnections(filesel+".outColor",s=0,plugs=1)
                    if trattrs!=None:
                        for trattr in trattrs:
                            if cmds.nodeType(trattr) not in ["file"] and filesel in adjfiles:
                                remapNode = cmds.shadingNode('alRemapColor', name=filesel+"_remapColor", asUtility=True)
                                cmds.setAttr(remapNode+".gamma",0.5)
                                cmds.connectAttr(filesel+".outColor", remapNode + '.input', force=True)
                                cmds.connectAttr(remapNode + '.outColor', trattr, force=True)
                          
            else:
                cmds.setAttr(filesel+".colorSpace","Raw",type="string")


def subColorvalue():
    aists = cmds.ls(type=["aiHair","aiStandard"]) 
    aistClists = {"aiStandard":["KrColor","KsColor","KsssColor","KtColor","color","emissionColor"],
                    "aiHair":["rootcolor","specColor","spec2Color","tipcolor","transmissionColor"]}
    for aist in aists:
        for aistClist in aistClists[cmds.nodeType(aist)]:
            if cmds.listConnections(aist+"."+aistClist,d=0)==None:
                subvalue =[0.6,0.6,0.6]
                newattr = list(cmds.getAttr(aist+"."+aistClist)[0])
                value=list(map(lambda x: x[0]-x[0]*x[1],zip(newattr,subvalue)))
                cmds.setAttr(aist+"."+aistClist,value[0],value[1],value[2],type="double3")
            else:
                conns = cmds.listConnections(aist+"."+aistClist, d=False, s=True, plugs=True )
                if cmds.nodeType(conns[0].split(".")[0])=="ramp":
                    remapNode = cmds.shadingNode('alRemapColor', name=aist+"_remapColor", asUtility=True)
                    cmds.setAttr(remapNode+".gamma",0.5)
                    cmds.connectAttr(conns[0], remapNode + '.input', force=True)
                    cmds.connectAttr(remapNode + '.outColor', aist+"."+aistClist, force=True) 

def convertAlShaders():
    shaderColl = cmds.ls(type="alSurface")
    if shaderColl:
        for x in shaderColl:
            SJ_doMapping(x)   
    
def al2aiSwitcher():            
    alswitchs = cmds.ls(type="alSwitchColor") 
    for alswitch in alswitchs:
        aiswitch = cmds.shadingNode("aiSwitch",name=alswitch+"_aiSwitch" ,asShader=True)
        alswitchouts =  cmds.listConnections(alswitch+".outColor",s=0,plugs=1)
        for alswitchout in alswitchouts:
            cmds.connectAttr(aiswitch+".outColor",alswitchout,f=1)
            
        alswitchins = [a for a in  cmds.listConnections(alswitch,d=0,plugs=1) if cmds.ls(a.split(".")[0],mat=1)!=None]
        for a in range(len(alswitchins)):
            cmds.connectAttr(alswitchins[a],aiswitch+".input"+str(a),f=1)
            
        alswitchmix = cmds.listConnections(alswitch+".mix",d=0,plugs=1)
        if alswitchmix!=None:
            cmds.connectAttr(alswitchmix[0],aiswitch+".index",f=1)
        else:
            mixvalue= cmds.getAttr(alswitch+".mix")
            cmds.setAttr(aiswitch+".index",mixvalue)
            
def fixmaya2017():
    fixIDcbs = cmds.checkBox("fixIDcb",q=1,v=1)
    alSurfTranscbs = cmds.checkBox("alSurfTranscb",q=1,v=1)
    filecolorcbs = cmds.checkBox("filecolorcb",q=1,v=1)
    aiStHaircbs = cmds.checkBox("aiStHaircb",q=1,v=1)
    layToMixcbs = cmds.checkBox("layToMixcb",q=1,v=1)
    alswToaiSWcbs = cmds.checkBox("alswToaiSWcb",q=1,v=1)
    AuNodefixedcbs = cmds.checkBox("AuNodefixedcb",q=1,v=1)
    if fixIDcbs==1:
        fixedID()
    if alSurfTranscbs==1:
        convertAlShaders()
    if filecolorcbs==1:
        filecolorfix()
    if aiStHaircbs==1:
        subColorvalue()
    if layToMixcbs==1:
        layer2Fixed()
    if alswToaiSWcbs==1:
        al2aiSwitcher()
    if AuNodefixedcbs==1:
        deletebadAu()
        
    
def SJ_convertAllShaders():
    targetShaders = []
    aiStandardcb = cmds.checkBox("aiStandardcb",q=1,v=1)
    alSurfacecbs = cmds.checkBox("alSurfacecb",q=1,v=1)
    aiHaircbs = cmds.checkBox("aiHaircb",q=1,v=1)
    alHaircbs = cmds.checkBox("alHaircb",q=1,v=1)
    if aiStandardcb==1:
        targetShaders.append("aiStandard")
    if alSurfacecbs==1:
        targetShaders.append("alSurface")
    if aiHaircbs==1:
        targetShaders.append("aiHair")
    if alHaircbs==1:
        targetShaders.append("alHair")
    if targetShaders!=[]:
        for shdType in targetShaders:
            shaderColl = cmds.ls(exactType=shdType)
            if shaderColl:
                for x in shaderColl:
                    print x
                    SJ_doMapping(x)   
                     
def SJ_convertAiskinAllShaders():
    shaderColl = cmds.ls(exactType="aiSkin")
    if shaderColl:
        for x in shaderColl:
            print x
            SJ_doMapping(x) 

def deletebadAu():
    Ausels = cmds.ls(type="aiUtility")
    for Ausel in Ausels:
        if cmds.listConnections(Ausel+".outColor",plugs=1,s=0)!=None:
            AuselOuts =[a for a in cmds.listConnections(Ausel+".outColor",plugs=1,s=0) if a.split(".")[-1]=="beauty" ]
            AuselIns = cmds.listConnections(Ausel+".color",plugs=1,d=0)
            for AuselOut in AuselOuts:
                cmds.connectAttr( AuselIns[0],AuselOut,f=1)
                cmds.delete(Ausel)   
            
def layer2Fixed():
    allayers = cmds.ls(type=["layeredTexture","alLayerColor"])
    for allayer in allayers:
        allayerouts=cmds.listConnections(allayer+".outColor",s=0,plugs=1)
        allayerIns = cmds.listConnections(allayer,d=0,plugs=1)
        if allayerIns!=None and allayerouts!=None:
            allayercolors = [a for  a in allayerIns if a.split(".")[-1]=="outColor"]
            base = allayercolors[0].split(".")[0]
            for l in range(len(allayercolors)):
                if l!=0:
                    basemix= cmds.shadingNode("aiMixShader",name= allayer+str(l),asShader=True)
                    cmds.connectAttr(base+".outColor",basemix+".shader1",f=1)
                    cmds.connectAttr(allayercolors[l],basemix+".shader2",f=1)
                    base = basemix
                    if cmds.nodeType(allayer)=="layeredTexture":
                        layCAttrs =[a for a in  cmds.listConnections(allayercolors[l],s=0,plugs=1,type="layeredTexture") if a.find(allayer)!=-1]
                        if cmds.getAttr(layCAttrs[0][:-len(layCAttrs[0].split(".")[-1])]+"blendMode") in [4]:
                            cmds.setAttr(basemix+".mode",1)
                        layerAlpha = cmds.listConnections(layCAttrs[0][:-len(layCAttrs[0].split(".")[-1])]+"alpha",d=0,plugs=1)
                        if layerAlpha==None:
                            allayerA =  cmds.getAttr(layCAttrs[0][:-len(layCAttrs[0].split(".")[-1])]+"alpha")
                            cmds.setAttr(basemix+".mix",allayerA/2)
                        else:
                            cmds.connectAttr(layerAlpha[0],basemix+".mix",f=1)
                    else:
                        if cmds.getAttr(allayer+".layer"+str(l+1)+"blend") in [5,1,10,11,12]:
                            cmds.setAttr(basemix+".mode",1)
                        layerAlpha = cmds.listConnections(allayer+".layer"+str(l+1)+"a",d=0,plugs=1)
                        if layerAlpha==None:
                            allayerA =  cmds.getAttr(allayer+".layer"+str(l+1)+"a")
                            cmds.setAttr(basemix+".mix",allayerA/2)
                        else:
                            cmds.connectAttr(layerAlpha[0],basemix+".mix",f=1)
            for allayerout in allayerouts:
                cmds.connectAttr( base+".outColor",allayerout,f=1)

def SJ_aiTranser2017UI():
    u'''
    {'load':'maya_common','defaultOption':1,'CNname':'Maya2017材质转化工具'}
    '''
    nodetypelist=['aiStandard', 'aiHair', 'alSurface', 'alHair']
    if cmds.window('aiTransfer2017wd',ex=True):
        cmds.deleteUI('aiTransfer2017wd',wnd=True)
    cmds.window('aiTransfer2017wd',t="Maya2015转2017-Maya2017材质转换工具")
    cmds.columnLayout(adj=True,w=440)
    
    '''
    cmds.text(l=u"材质转换", fn='fixedWidthFont',h=50,ann=u'将%s\n类型材质节点分别转换为\naiStandardSurface或alstandardHair'%(nodetypelist) )
    cmds.setParent("..")
    cmds.flowLayout()
    cbvalue=False
    cmds.checkBox("aiStandardcb" ,label=u'aiStandard',v=cbvalue,ann="",w=95,h=50)
    cmds.checkBox("alSurfacecb" ,label=u'alSurface',v=cbvalue,ann="",w=95,h=50)
    cmds.checkBox("aiHaircb" ,label=u'aiHair',v=cbvalue,ann="",w=95,h=50)
    cmds.checkBox("alHaircb" ,label=u'alHair',v=cbvalue,ann="",w=95,h=50)
    cmds.setParent( '..' )
    cmds.button(l=u'转换此类型的\n所有材质',c=u'SJ_convertAllShaders()',h=50,w=150,ann="")
    cmds.setParent( '..' )
    cmds.flowLayout( columnSpacing=0)
    cmds.button(l=u'转换所选节点类型\n所有材质',c=u'SJ_convertAlltypeShaders()',h=50,w=220,ann="")
    cmds.button(l=u'转换所选节点',c=u'SJ_convertSelection()',h=50,w=220,ann="")
    cmds.setParent("..")
    '''
    cmds.text(l=u'maya2015转Maya2017文件修复', fn='fixedWidthFont',h=50,ann="" )
    cmds.setParent("..")
    cmds.flowLayout()
    cmds.checkBox("fixIDcb" ,label=u'修复ID节点',v=1,ann="",w=150,h=50)
    cmds.checkBox("alSurfTranscb" ,label=u'alsurface转化为\naiStandardSurface',v=1,ann="",w=150,h=50)
    cmds.checkBox("filecolorcb" ,label=u'贴图节点色彩空间修复',v=1,ann="",w=150,h=50)
    cmds.setParent("..")
    cmds.flowLayout()
    cmds.checkBox("aiStHaircb" ,label=u'aiStandard和aihair\n材质属性更新',v=1,ann="",w=150,h=50)
    cmds.checkBox("layToMixcb" ,label=u'无效层纹理\n转化为aiMixshader',v=1,ann="layeredTexture或alLayerColor转换为aiMixShader，层的叠加目前支持add和normal",w=150,h=50)
    cmds.checkBox("alswToaiSWcb" ,label=u'alSwitchColor\n转换为aiSwitch',v=1,ann="",w=150,h=50)
    cmds.setParent("..")
    cmds.flowLayout()
    cmds.checkBox("AuNodefixedcb" ,label=u'修复无效aiUtility',v=1,ann="",w=150,h=50)
    cmds.setParent("..")
    cmds.button(l=u'一键修复',c=u'fixmaya2017()',h=50,w=150,ann="")
    cmds.showWindow()
    
def SJ_aiTranser2015UI():
    u'''
    {'load':'maya_common','defaultOption':1,'CNname':'Maya2015材质转化工具'}
    '''
    if cmds.window('aiTransfer2015wd',ex=True):
        cmds.deleteUI('aiTransfer2015wd',wnd=True)
    cmds.window('aiTransfer2015wd',t="Maya2015转2017-Maya2015材质转换工具")
    cmds.columnLayout(adj=True,w=440)
    cmds.text(l=u"材质转换", fn='fixedWidthFont',h=50,ann="" )
    cmds.button(l=u'转换此aiSkin类型的\n所有材质为aiStandardSSS',c=u'SJ_convertAiskinAllShaders()',h=50,w=150,ann="")
    cmds.button(l=u'转换所选aiSkin节点',c=u'SJ_convertSelection()',h=50,w=220,ann="")
    cmds.showWindow()
def SJ_convertArnoldShaders():
    if not cmds.pluginInfo( 'mtoa', query=True, loaded=True ):
        cmds.loadPlugin('mtoa')
    if versions.current()>=201700:
        SJ_aiTranser2017UI()
    else:
        SJ_aiTranser2015UI()
    
if __name__=="__main__":
    SJ_convertArnoldShaders()
