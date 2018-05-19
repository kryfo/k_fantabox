import pymel.core as pm       
class IDtool():
    def byg(self):
        ramNd = pm.shadingNode('ramp', asTexture=True)
        samInfo = pm.shadingNode('samplerInfo', asUtility=True)
        newAU =[ pm.shadingNode('aiUtility', asShader=True)]
        pm.setAttr(newAU[0] + '.shadeMode',2)
        pm.setAttr(ramNd+".colorEntryList[0].color",1, 0, 0, type="double3")
        pm.setAttr(ramNd+".colorEntryList[1].color",0, 0, 1, type="double3")
        pm.setAttr(ramNd+".colorEntryList[1].position",0.635)
        pm.connectAttr(samInfo+".facingRatio",ramNd+".vCoord")
        pm.connectAttr(ramNd+".outColor",newAU[0]+".color")
        return newAU
    def xray(self):
        ramNd = pm.shadingNode('ramp', asTexture=True)
        samInfo = pm.shadingNode('samplerInfo', asUtility=True)
        newAU = [pm.shadingNode('aiUtility', asShader=True)]
        pm.setAttr(newAU[0] + '.shadeMode',0)
        pm.setAttr(ramNd + '.invert',1)
        pm.setAttr(ramNd+".colorEntryList[0].color",0, 0, 0, type="double3")
        pm.setAttr(ramNd+".colorEntryList[1].color",1, 1, 1, type="double3")
        pm.setAttr(ramNd+".colorEntryList[1].position",0.828)
        pm.connectAttr(samInfo+".facingRatio",ramNd+".vCoord")
        pm.connectAttr(samInfo+".facingRatio",ramNd+".uCoord")
        pm.connectAttr(ramNd+".outColor",newAU[0]+".color")
        pm.connectAttr(ramNd+".outAlpha",newAU[0]+".opacity")
        return newAU
    def occ(self):
        newAU = [pm.shadingNode('aiAmbientOcclusion', asShader=True)]
        pm.setAttr(newAU[0] + '.samples',5)
        return newAU
    def nm(self):
        newAU = [pm.shadingNode('aiUtility', asShader=True)]
        pm.setAttr(newAU[0] + '.shadeMode',2)
        pm.setAttr(newAU[0]+ '.colorMode',3)
        return newAU
    def doit(self,shaderattr):
        occsel =pm.ls(type="aiAmbientOcclusion")
        if occsel==[]:
            occsel =IDtool().occ()
        nmsel  = [a for  a in  pm.ls(type="aiUtility") if pm.getAttr(a+'.colorMode')==3]
        if nmsel==[]:
            nmsel = IDtool().nm()
        bygsel =[a for  a in pm.ls(type="aiUtility") if pm.listConnections(a+".color",d=0,type="ramp")!=[] and pm.listConnections(a+".color",d=0,type="ramp")[0].getAttr("colorEntryList[0].color")==(1,0,0)]
        if bygsel==[]:
            bygsel = IDtool().byg()
        xraysel =[a for  a in pm.ls(type="aiUtility") if pm.listConnections(a+".color",d=0,type="ramp")!=[] and pm.listConnections(a+".color",d=0,type="ramp")[0].getAttr("colorEntryList[0].color")==(0,0,0)]
        if xraysel==[]:
            xraysel = IDtool().xray() 
        if shaderattr ==[]:
            shaderattr =pm.listConnections(SGs+".surfaceShader",c=1,plugs=1)
        shader =  shaderattr[0][1].split(".")[0]
        xrayAW = pm.shadingNode('aiWriteColor', asShader=True,name = shader)
        pm.setAttr(xrayAW+'.aovName',"xray",type="string")
        nmAW = pm.shadingNode('aiWriteColor', asShader=True,name = shader)
        pm.setAttr(nmAW+'.aovName',"normal",type="string")
        occAW = pm.shadingNode('aiWriteColor', asShader=True,name = shader)
        pm.setAttr(occAW+'.aovName',"OCC",type="string")
        bygAW = pm.shadingNode('aiWriteColor', asShader=True,name = shader)
        pm.setAttr(bygAW+'.aovName',"BYG",type="string")
        finalAU =pm.shadingNode('aiUtility', asShader=True,name=shader)
        pm.setAttr(finalAU + '.shadeMode',2)
        pm.connectAttr( finalAU + '.outColor', shaderattr[0][0], f=True )
        pm.connectAttr( nmAW + '.outColor', finalAU + '.color', f=True )
        pm.connectAttr( xrayAW + '.outColor', nmAW + '.beauty', f=True )
        pm.connectAttr( occAW + '.outColor', xrayAW + '.beauty', f=True )
        pm.connectAttr( bygAW + '.outColor', occAW + '.beauty', f=True )
        pm.connectAttr( shaderattr[0][1], bygAW + '.beauty', f=True )
        pm.connectAttr( xraysel[0] + '.outColor', xrayAW + '.input', f=True )
        pm.connectAttr( bygsel[0] + '.outColor', bygAW + '.input', f=True )
        pm.connectAttr( occsel[0] + '.outColor', occAW + '.input', f=True )
        pm.connectAttr( nmsel[0] + '.outColor', nmAW + '.input', f=True )
def main():
    sels =pm.ls(sl=1)
    for sel in sels:
        if sel.getShape().nodeType()=="mesh" or sel.getShape().nodeType()=="pgYetiMaya":
            SGs=pm.listConnections(sel.getShape(),s=0,type="shadingEngine")[0]
            shaderattr =pm.listConnections(SGs+".aiSurfaceShader",c=1,plugs=1)
            if shaderattr ==[]:
                shaderattr =pm.listConnections(SGs+".surfaceShader",c=1,plugs=1)
            IDtool().doit(shaderattr)
        elif sel.getShape().nodeType()=="pfxHair":
            hairsys =  pm.listConnections(sel.getShape()+".renderHairs",d=0,type="hairSystem")[0]
            shaderattr = pm.listConnections(hairsys+".aiHairShader",c=1,plugs=1)
            IDtool().doit(shaderattr)