import maya.cmds as cc
import math
import maya.mel as mel
import json

def k_tintplate():

    #k_cpath='//10.99.1.13/hq_tool3/Maya/hq_maya/icons/color_card.psd'
    k_cpath = cc.getModulePath(moduleName='hq_maya')+'/icons/color_card.psd'

    k_mesh=cc.ls(type=['mesh','nurbsSurface'])

    k_hair=cc.ls(type=['pfxHair','pgYetiGroom','pgYetiMaya'])

    k_shave=[]
    if cc.pluginInfo('shaveNode',q=1,loaded=1,name=1):
        k_shave=cc.ls(type=['shaveHair'])

    k_hide=k_mesh+k_hair+k_shave

    if cc.objExists('k_bak_disL'):
        cc.editDisplayLayerMembers('k_bak_disL',k_hide)
        cc.setAttr('k_bak_disL.visibility',0)
    else:
        cc.createDisplayLayer(name='k_bak_disL',e=1)
        cc.editDisplayLayerMembers('k_bak_disL',k_hide)
        cc.setAttr('k_bak_disL.visibility',0)


    mel.eval("postModelEditorSelectCamera modelPanel4 modelPanel4 0")
    k_cam=cc.ls(sl=1)



    if cc.nodeType(k_cam)!='camera':
        try:
            cc.listRelatives(k_cam,f=1,type='camera')[0]
        except:
            cc.confirmDialog( title='k_problem', message='select one camera')
            cc.error('didnot select one camera')
    elif cc.nodeType(k_cam)=='camera':
        k_cam[0]=cc.listRelatives(k_cam,f=1,parent=1)[0]



    if cc.objExists('k_colorball'):
        cc.delete('k_colorball')
        k_colorball=cc.group(em=True,name='k_colorball')
    else:k_colorball=cc.group(em=True,name='k_colorball')



    k_mbc_tx=cc.getAttr(k_cam[0]+'.tx')
    k_mbc_ty=cc.getAttr(k_cam[0]+'.ty')
    k_mbc_tz=cc.getAttr(k_cam[0]+'.tz')
    k_mbc_rx=cc.getAttr(k_cam[0]+'.rx')%360
    k_mbc_ry=cc.getAttr(k_cam[0]+'.ry')%360
    k_mbc_rz=cc.getAttr(k_cam[0]+'.rz')%360


    #k_max=max([abs(k_mbc_tx),abs(k_mbc_ty),abs(k_mbc_tz)])



    if cc.objExists('k_colorball_1'):
        cc.delete('k_colorball_1')
        cc.polySphere(ch=1,n='k_colorball_1')
        cc.move(-.6,0,0)
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_1','k_colorball')
        cc.setAttr('k_colorball_1Shape.castsShadows',0)
        cc.setAttr('k_colorball_1Shape.receiveShadows',0)
    else:
        cc.polySphere(ch=1,n='k_colorball_1')
        cc.move(-.6,0,0)
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_1','k_colorball')
        cc.setAttr('k_colorball_1Shape.castsShadows',0)
        cc.setAttr('k_colorball_1Shape.receiveShadows',0)



    if cc.objExists('k_colorball_2'):
        cc.delete('k_colorball_2')
        cc.polySphere(ch=1,n='k_colorball_2')
        cc.move(-.3,0,0)
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_2','k_colorball')
        cc.setAttr('k_colorball_2Shape.castsShadows',0)
        cc.setAttr('k_colorball_2Shape.receiveShadows',0)
    else:
        cc.polySphere(ch=1,n='k_colorball_2')
        cc.move(-.3,0,0)
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_2','k_colorball')
        cc.setAttr('k_colorball_2Shape.castsShadows',0)
        cc.setAttr('k_colorball_2Shape.receiveShadows',0)

    if cc.objExists('k_colorball_3'):
        cc.delete('k_colorball_3')
        cc.polySphere(ch=1,n='k_colorball_3')
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_3','k_colorball')
        cc.setAttr('k_colorball_3Shape.castsShadows',0)
        cc.setAttr('k_colorball_3Shape.receiveShadows',0)    
    else:
        cc.polySphere(ch=1,n='k_colorball_3')
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_3','k_colorball')
        cc.setAttr('k_colorball_3Shape.castsShadows',0)
        cc.setAttr('k_colorball_3Shape.receiveShadows',0)    

    if cc.objExists('k_colorball_4'):
        cc.delete('k_colorball_4')
        cc.polySphere(ch=1,n='k_colorball_4')
        cc.move(.3,0,0)
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_4','k_colorball')
        cc.setAttr('k_colorball_3Shape.castsShadows',0)
        cc.setAttr('k_colorball_3Shape.receiveShadows',0)    
    else:
        cc.polySphere(ch=1,n='k_colorball_4')
        cc.move(.3,0,0)
        cc.scale(.1,.1,.1)
        cc.parent('k_colorball_4','k_colorball')
        cc.setAttr('k_colorball_4Shape.castsShadows',0)
        cc.setAttr('k_colorball_4Shape.receiveShadows',0)    


    if cc.objExists('k_colorbox'):
        cc.delete('k_colorbox')
        cc.polyCube(ch=1,n='k_colorbox')
        cc.move(.8,0,0)
        cc.scale(.3,.2,.2)
        cc.rotate(0,10,0)
        cc.parent('k_colorbox','k_colorball')
        cc.setAttr('k_colorboxShape.castsShadows',0)
        cc.setAttr('k_colorboxShape.receiveShadows',0)    
    else:
        cc.polyCube(ch=1,n='k_colorbox')
        cc.move(.8,0,0)
        cc.scale(.3,.2,.2)
        cc.rotate(0,10,0)
        cc.parent('k_colorbox','k_colorball')
        cc.setAttr('k_colorboxShape.castsShadows',0)
        cc.setAttr('k_colorboxShape.receiveShadows',0)   

    cc.select(cl=1)

    try:
        cc.parentConstraint(k_cam[0],'k_colorball',n='k_colorball_parentC')
        cc.delete('k_colorball_parentC')
    except:
        cc.error('didnot select one camera')

    if cc.objExists('k_mbg'):
        cc.delete('k_mbg')
        k_colorball=cc.group(em=True,name='k_mbg')
    else:k_colorball=cc.group(em=True,name='k_mbg')

    cc.parent('k_mbg','k_colorball')


    if 85<(k_mbc_ry%180)<95:
        k_y=abs(k_mbc_tx)
    else:

        k_x=k_mbc_tz/math.cos(math.radians(k_mbc_ry%360))

        #if abs(k_mbc_rx)>40:k_mbc_rx=40
        k_y=k_x/math.cos(math.radians(abs(k_mbc_rx%360)))



    #print k_y
    
    cc.setAttr("k_mbg.translateX",0);
    cc.setAttr("k_mbg.translateY",0);
    cc.setAttr("k_mbg.translateZ",-abs(k_y));
    cc.setAttr("k_mbg.rotateX",0);
    cc.setAttr("k_mbg.rotateY",0);
    cc.setAttr("k_mbg.rotateZ",0);
    cc.parent('k_mbg',w=1)

    try:
        cc.parentConstraint('k_mbg','k_colorball',n='k_tmp_parentC')
        cc.delete('k_tmp_parentC')
    except:
        cc.error('something error')

    k_scale=.2*abs(k_y)

    cc.setAttr("k_colorball.scaleX",k_scale);
    cc.setAttr("k_colorball.scaleY",k_scale);
    cc.setAttr("k_colorball.scaleZ",k_scale);


    if not cc.objExists('k_wb1_SG'):
        cc.sets(empty=1,renderable=1,nss=1,n='k_wb1_SG')

    if not cc.objExists('k_wb1_shader'):
        cc.shadingNode('aiStandard',asShader=1,name='k_wb1_shader')
        cc.setAttr('k_wb1_shader.Kd',1)
        cc.setAttr('k_wb1_shader.color',.8,.8,.8,type='double3')
    else:
        cc.setAttr('k_wb1_shader.Kd',1)
        cc.setAttr('k_wb1_shader.color',.8,.8,.8,type='double3')

    if not cc.isConnected('k_wb1_shader.outColor','k_wb1_SG.surfaceShader'):
        cc.connectAttr ('k_wb1_shader.outColor','k_wb1_SG.surfaceShader',f=1)

    cc.sets('k_colorball_1Shape',e=1,fe='k_wb1_SG')


    if not cc.objExists('k_fb2_SG'):
        cc.sets(empty=1,renderable=1,nss=1,n='k_fb2_SG')

    if not cc.objExists('k_fb2_shader'):
        cc.shadingNode('aiStandard',asShader=1,name='k_fb2_shader')
        cc.setAttr('k_fb2_shader.Kd',0);
        cc.setAttr('k_fb2_shader.Ks',1);
        cc.setAttr('k_fb2_shader.specularRoughness',0)
    else:
        cc.setAttr('k_fb2_shader.Kd',0);
        cc.setAttr('k_fb2_shader.Ks',1);
        cc.setAttr('k_fb2_shader.specularRoughness',0)

    if not cc.isConnected('k_fb2_shader.outColor','k_fb2_SG.surfaceShader'):
        cc.connectAttr ('k_fb2_shader.outColor','k_fb2_SG.surfaceShader',f=1)

    cc.sets('k_colorball_2Shape',e=1,fe='k_fb2_SG')


    if not cc.objExists('k_hb3_SG'):
        cc.sets(empty=1,renderable=1,nss=1,n='k_hb3_SG')

    if not cc.objExists('k_hb3_shader'):
        cc.shadingNode('aiStandard',asShader=1,name='k_hb3_shader')
        cc.setAttr('k_hb3_shader.Kd',1)
        cc.setAttr('k_hb3_shader.color',.5,.5,.5,type='double3')
    else:
        cc.setAttr('k_hb3_shader.Kd',1)
        cc.setAttr('k_hb3_shader.color',.5,.5,.5,type='double3')

    if not cc.isConnected('k_hb3_shader.outColor','k_hb3_SG.surfaceShader'):
        cc.connectAttr ('k_hb3_shader.outColor','k_hb3_SG.surfaceShader',f=1)

    cc.sets('k_colorball_3Shape',e=1,fe='k_hb3_SG')





    if not cc.objExists('k_bb4_SG'):
        cc.sets(empty=1,renderable=1,nss=1,n='k_bb4_SG')

    if not cc.objExists('k_bb4_shader'):
        cc.shadingNode('aiStandard',asShader=1,name='k_bb4_shader')
        cc.setAttr('k_bb4_shader.Kd',0)
        cc.setAttr('k_bb4_shader.Ks',0.5)
        cc.setAttr('k_bb4_shader.specularRoughness',0.3)
        cc.setAttr('k_bb4_shader.KsColor',.5,.5,.5,type='double3')
    else:
        cc.setAttr('k_bb4_shader.Kd',0)
        cc.setAttr('k_bb4_shader.Ks',0.5)
        cc.setAttr('k_bb4_shader.specularRoughness',0.3)
        cc.setAttr('k_bb4_shader.KsColor',.5,.5,.5,type='double3')

    if not cc.isConnected('k_bb4_shader.outColor','k_bb4_SG.surfaceShader'):
        cc.connectAttr ('k_bb4_shader.outColor','k_bb4_SG.surfaceShader',f=1)

    cc.sets('k_colorball_4Shape',e=1,fe='k_bb4_SG')






    if not cc.objExists('k_card_SG'):
        cc.sets(empty=1,renderable=1,nss=1,n='k_card_SG')

    if not cc.objExists('k_card_file'):
        cc.shadingNode('file',asTexture=1,name='k_card_file')
        cc.setAttr('k_card_file.fileTextureName',k_cpath,type='string')

    else:cc.setAttr('k_card_file.fileTextureName',k_cpath,type='string')


    if not cc.objExists('k_card_shader'):
        cc.shadingNode('aiStandard',asShader=1,name='k_card_shader')
        cc.setAttr('k_card_shader.Kd',1)

    if not cc.isConnected('k_card_shader.outColor','k_card_SG.surfaceShader'):
        cc.connectAttr ('k_card_shader.outColor','k_card_SG.surfaceShader',f=1)

    if not cc.isConnected('k_card_file.outColor','k_card_shader.color'):
        cc.connectAttr ('k_card_file.outColor','k_card_shader.color',f=1)



    cc.sets('k_colorboxShape',e=1,fe='k_card_SG')


    cc.delete('k_mbg')



    if cc.objExists('k_colorball_disL'):
        cc.editDisplayLayerMembers('k_colorball_disL','k_colorball')
    else:
        cc.createDisplayLayer(name='k_colorball_disL',e=1)
        cc.editDisplayLayerMembers('k_colorball_disL','k_colorball')


    cc.select(cl=1)


if __name__=='__main__':
    k_tintplate()

