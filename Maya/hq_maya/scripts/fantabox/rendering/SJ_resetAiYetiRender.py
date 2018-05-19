import maya.cmds as cmds
def typecol(types):
    typcols=[]
    try:
        for type in types:
            if type!="renderLayer":
                typcol =cmds.ls(type=type)
                typcols+=typcol
            else:
                typcol =[a for a in cmds.ls(type=type) if a.find("defaultRenderLayer")!=-1]
    except:
        cmds.warning(type+" cant been deleted!!")
    print typcols
    return typcols
def resetYetiRender():
    renderpremel = cmds.getAttr ('defaultRenderGlobals.preMel')
    if cmds.getAttr("defaultRenderGlobals.preMel",l=1)==True:
        cmds.setAttr("defaultRenderGlobals.preMel",l=0)
    if renderpremel!="pgYetiPreRender":
        cmds.setAttr('defaultRenderGlobals.preMel',"pgYetiPreRender",type="string")
    cmds.setAttr("defaultRenderGlobals.preMel",l=1)
    return "done!!",
    
def SJ_resetAiYetiRender():
    cams = cmds.ls(type="camera")
    for cam in cams:
        cmds.setAttr(cam+".renderable",1)

    aovdrs= cmds.ls(type="aiAOVDriver")
    if aovdrs!=[]:
        for aovdr in aovdrs:
            if aovdr.find("defaultArnoldDisplayDriver")==-1:
                cmds.setAttr(aovdr+".aiTranslator","exr",type="string")
            else:
                cmds.setAttr(aovdr+".aiTranslator","maya",type="string")
    if cmds.objExists("defaultArnoldRenderOptions") and cmds.objExists("defaultArnoldDriver"):
        cmds.setAttr("defaultArnoldRenderOptions.force_scene_update_before_IPR_refresh",1)
        cmds.setAttr("defaultArnoldRenderOptions.force_texture_cache_flush_after_render",1)
        cmds.setAttr("defaultArnoldRenderOptions.use_existing_tiled_textures",1)
        cmds.setAttr("defaultArnoldRenderOptions.textureMaxMemoryMB",1024000000)
        cmds.setAttr("defaultArnoldRenderOptions.abortOnError",1)
        cmds.setAttr("defaultArnoldDriver.halfPrecision",1)
        cmds.setAttr("defaultArnoldDriver.autocrop",1)
        
    if cmds.ls(type="pgYetiMaya")!=[]:
        resetYetiRender()
    renderjudge = cmds.getAttr ('defaultRenderGlobals.currentRenderer')
    if renderjudge=="arnold":
        norType = ["renderLayer","unknown"]
        delType = ["VRayGeomList","VRayMesh","VRaySettingsNode"]
        miType = [u'mentalrayItemsList', u'mentalrayFramebuffer', u'mentalrayGlobals', u'mentalrayOptions']
        WholeType = norType+delType+miType
        delcols=[a for a in  typecol(WholeType) if a not in cmds.ls(ro=1)]
        for delcol in delcols:
            try:
                print delcol,
                cmds.delete(delcol)
            except:
                pass


