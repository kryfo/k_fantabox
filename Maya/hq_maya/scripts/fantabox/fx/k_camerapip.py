#coding:utf-8
import maya.cmds as cmds
import sys,shutil,math
def camerapipwdUI():
	if  cmds.window('k_dengtao',exists=True):
	    cmds.deleteUI('k_dengtao',window=True)
	cmds.window('k_dengtao',title="拍摄相机流程辅助面板_k")
	
	cmds.columnLayout(adjustableColumn=1)
	cmds.text(label='')
	cmds.button(label='为人物修改颜色',h=40,command='fb.fx.matren()')
	cmds.button(label='为道具修改颜色',h=40,command='fb.fx.matdj()')
	cmds.button(label='为群众修改颜色',h=40,command='fb.fx.matqz()')
	cmds.text(label='')
	
	cmds.floatFieldGrp('k_gaodu',label='离地高度:',pre=5,extraLabel='',enable=True)
	
	cmds.button(label='选择相机_first',h=50,command='fb.fx.k_selcam()')
	
	cmds.button(label='选择测量物体_first',h=50,command='fb.fx.k_selwuti()')
	
	
	
	cmds.button(label='转移至坐标原点_first',h=50,command='fb.fx.k_move()')
	cmds.text(label='')
	cmds.button(label='选择相机_end',h=50,command='fb.fx.k_selcam2()')
	
	cmds.button(label='选择测量物体_end',h=50,command='fb.fx.k_selwuti2()')
	
	cmds.button(label='转移至坐标原点_end',h=50,command='fb.fx.k_move2()')
	
	cmds.text(label='')
	cmds.button(label='创建Locator的坐标',h=50,command='fb.fx.k_ann()')
	cmds.text(label='')
	cmds.button(label='创建相机显示窗口',h=50,command='fb.fx.k_camwin()')
	cmds.showWindow('k_dengtao')

def k_selcam():
    global kd_cam
    global k_ffs
    k_cam=cmds.ls(sl=1)
    k_cams=cmds.listRelatives(k_cam[0],f=1)
    k_type=cmds.nodeType(k_cams)
    
    if not cmds.objExists('first_frame_scenes'):
        k_ffs=cmds.createNode('transform',n="first_frame_scenes")
    
    if k_type=="camera" and len(k_cam)==1:
        kd_cam=cmds.duplicate(k_cam,rc=1,rr=1,n=("k_"+k_cam[0]))
        cmds.setAttr (kd_cam[0]+".tx",l=0)
        cmds.setAttr (kd_cam[0]+".ty",l=0) 
        cmds.setAttr (kd_cam[0]+".tz",l=0) 
        cmds.setAttr (kd_cam[0]+".rx",l=0) 
        cmds.setAttr (kd_cam[0]+".ry",l=0) 
        cmds.setAttr (kd_cam[0]+".rz",l=0) 
        cmds.setAttr (kd_cam[0]+".sx",l=0)
        cmds.setAttr (kd_cam[0]+".sy",l=0)
        cmds.setAttr (kd_cam[0]+".sz",l=0) 
        for kd_camd in kd_cam:
            cmds.parent(kd_camd,'first_frame_scenes')
            
def k_selcam2():
    global kd_cam2
    global k_ffs2
    k_cam=cmds.ls(sl=1)
    k_cams=cmds.listRelatives(k_cam[0],f=1)
    k_type=cmds.nodeType(k_cams)
    
    if not cmds.objExists('end_frame_scenes'):
        k_ffs2=cmds.createNode('transform',n="end_frame_scenes")
    
    if k_type=="camera" and len(k_cam)==1:
        kd_cam2=cmds.duplicate(k_cam,rc=1,rr=1,n=("k_"+k_cam[0]))
        cmds.setAttr (kd_cam2[0]+".tx",l=0)
        cmds.setAttr (kd_cam2[0]+".ty",l=0) 
        cmds.setAttr (kd_cam2[0]+".tz",l=0) 
        cmds.setAttr (kd_cam2[0]+".rx",l=0) 
        cmds.setAttr (kd_cam2[0]+".ry",l=0) 
        cmds.setAttr (kd_cam2[0]+".rz",l=0) 
        cmds.setAttr (kd_cam2[0]+".sx",l=0)
        cmds.setAttr (kd_cam2[0]+".sy",l=0)
        cmds.setAttr (kd_cam2[0]+".sz",l=0) 
        for kd_camd in kd_cam2:
            cmds.parent(kd_camd,'end_frame_scenes')
            
    
def k_selwuti():
    global k_dds
    global k_ffs
    k_meshs=cmds.ls(sl=1)
    
    if not cmds.objExists('first_frame_scenes'):
        k_ffs=cmds.createNode('transform',n="first_frame_scenes")
    
    for k_mesh in k_meshs:
        k_dds=cmds.duplicate(k_mesh,rc=1,rr=1,n=("k_"+k_mesh))
        for k_dd in k_dds:
            cmds.parent(k_dd,'first_frame_scenes')

def k_selwuti2():
    global k_dds2
    global k_ffs2
    k_meshs=cmds.ls(sl=1)
    
    if not cmds.objExists('end_frame_scenes'):
        k_ffs2=cmds.createNode('transform',n="end_frame_scenes")
    
    for k_mesh in k_meshs:
        k_dds2=cmds.duplicate(k_mesh,rc=1,rr=1,n=("k_"+k_mesh))
        for k_dd in k_dds2:
            cmds.parent(k_dd,'end_frame_scenes')
            

def k_move():
    global k_css
    global k_ffs
    if cmds.objExists('cam_scenes_first'):
        cmds.delete('cam_scenes_first')
        k_css=cmds.createNode('transform',n="cam_scenes_first")
    else :
        k_css=cmds.createNode('transform',n="cam_scenes_first")
    
    k_pointCon=cmds.pointConstraint(kd_cam[0],k_css)
    cmds.delete(k_pointCon)   
    
    cmds.parent(k_ffs,k_css)
    
    if cmds.objExists('cam_sceness_first'):
        cmds.delete('cam_sceness_first')
        k_csc=cmds.createNode('transform',n="cam_sceness_first")
    else :
        k_csc=cmds.createNode('transform',n="cam_sceness_first")
         
    cmds.parent(k_css,k_csc)
    
    k_pointCo=cmds.pointConstraint(k_csc,k_css)
    cmds.delete(k_pointCo)
    cmds.parent("cam_scenes_first",w=1)
    cmds.delete(k_csc)
    
    k_lidigaodu=cmds.floatFieldGrp('k_gaodu',value1=True,q=True)
    
    k_rc=cmds.getAttr(kd_cam[0]+".ry")
    cmds.setAttr(k_css+".ry",-k_rc)
    
    cmds.setAttr(k_css+".ty",k_lidigaodu)
    

def k_move2():
    global k_css2
    global k_ffs2
    if cmds.objExists('cam_scenes_end'):
        cmds.delete('cam_scenes_end')
        k_css2=cmds.createNode('transform',n="cam_scenes_end")
    else :
        k_css2=cmds.createNode('transform',n="cam_scenes_end")
    
    k_pointCon=cmds.pointConstraint(kd_cam2[0],k_css2)
    cmds.delete(k_pointCon)   
    
    cmds.parent(k_ffs2,k_css2)
    print k_css2
    
    if cmds.objExists('cam_sceness_end'):
        cmds.delete('cam_sceness_end')
        k_csc=cmds.createNode('transform',n="cam_sceness_end")
    else :
        k_csc=cmds.createNode('transform',n="cam_sceness_end")
    
    print k_css2     
    cmds.parent(k_css2,k_csc)
    k_pointCo=cmds.pointConstraint(k_csc,k_css2)
    cmds.delete(k_pointCo)
    cmds.parent("cam_scenes_end",w=1)
    cmds.delete(k_csc)
    
    k_lidigaodu=cmds.floatFieldGrp('k_gaodu',value1=True,q=True)
    
    k_rc=cmds.getAttr(kd_cam2[0]+".ry")
    cmds.setAttr(k_css2+".ry",-k_rc)
    
    cmds.setAttr(k_css2+".ty",k_lidigaodu)
   
    
    


def k_ann():
    k_locas=cmds.ls(sl=1)
    
    for k_loca in k_locas:
        k_locass=cmds.listRelatives(k_loca)
        if cmds.nodeType(k_locass)=="locator":
            kl_tx=cmds.getAttr(k_loca+".tx")
            kl_ty=cmds.getAttr(k_loca+".ty")
            kl_tz=cmds.getAttr(k_loca+".tz")        
            kl_tya=abs(kl_ty)
            kl_tza=abs(kl_tz)
            kl_txt=str(kl_tx)
            kl_tyt=str(kl_tya)
            kl_tzt=str(kl_tza)
            
            kt_zuobiao=cmds.annotate (k_loca,tx='('+kl_txt[0:5]+','+kl_tzt[0:4]+','+kl_tyt[0:4]+')')
            kr_zuobiao=cmds.listRelatives(kt_zuobiao,p=1)
            kpc_zuobaio=cmds.pointConstraint(k_loca,kr_zuobiao)
            cmds.delete(kpc_zuobaio)
        
        
        
def matren():
    k_sels=cmds.ls(sl=1) 
    if not cmds.objExists('kMskSG_r'):
        cmds.sets(n='kMskSG_r',empty=1,renderable=1,noSurfaceShader=1)
        
    if not cmds.objExists('kMskShader_r'):
        cmds.shadingNode('surfaceShader',asShader=1,n='kMskShader_r')
        cmds.setAttr('kMskShader_r.outColor',1,0,0,type='double3')
        
    if not cmds.isConnected('kMskShader_r.outColor','kMskSG_r.surfaceShader'):
        cmds.connectAttr('kMskShader_r.outColor','kMskSG_r.surfaceShader',f=1) 
        
    
    cmds.sets(k_sels,e=1,fe='kMskSG_r')


def matdj():
    k_sels=cmds.ls(sl=1) 
    if not cmds.objExists('kMskSG_b'):
        cmds.sets(n='kMskSG_b',empty=1,renderable=1,noSurfaceShader=1)
        
    if not cmds.objExists('kMskShader_b'):
        cmds.shadingNode('surfaceShader',asShader=1,n='kMskShader_b')
        cmds.setAttr('kMskShader_b.outColor',0,0,1,type='double3')
        
    if not cmds.isConnected('kMskShader_b.outColor','kMskSG_b.surfaceShader'):
        cmds.connectAttr('kMskShader_b.outColor','kMskSG_b.surfaceShader',f=1) 
        
    
    cmds.sets(k_sels,e=1,fe='kMskSG_b')

def matqz():
    k_sels=cmds.ls(sl=1) 
    if not cmds.objExists('kMskSG_p'):
        cmds.sets(n='kMskSG_p',empty=1,renderable=1,noSurfaceShader=1)
        
    if not cmds.objExists('kMskShader_p'):
        cmds.shadingNode('surfaceShader',asShader=1,n='kMskShader_p')
        cmds.setAttr('kMskShader_p.outColor',.2,0,.3,type='double3')
        
    if not cmds.isConnected('kMskShader_p.outColor','kMskSG_p.surfaceShader'):
        cmds.connectAttr('kMskShader_p.outColor','kMskSG_p.surfaceShader',f=1) 
        
    
    cmds.sets(k_sels,e=1,fe='kMskSG_p')
    
    
def k_camwin():
    k_camt=cmds.ls(sl=1,l=1)
    
    k_camtss=cmds.ls(sl=1)
    
    k_camst=cmds.listRelatives(k_camt[0],f=1)
    k_typec=cmds.nodeType(k_camst)
    
    
    if k_typec=="camera" and len(k_camt)==1:
        k_camn=k_camt[0].replace('|','_')
        if  cmds.window(k_camn,exists=True):
            cmds.deleteUI(k_camn,window=True)
        cmds.window(k_camn,title="dengtao的测试窗口")   
        cmds.paneLayout()
        cmds.modelPanel(cam=k_camt[0])
        print "ha"
        cmds.window(k_camn,e=1,wh=(960,640))
        cmds.showWindow(k_camn)
    
      
    
    
    
    
    
    
    