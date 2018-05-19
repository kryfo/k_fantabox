#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import maya.cmds as cmds
import json
def shdtr(arg):
    tartyp = ["mesh"]
    objls = cmds.ls(type="transform")
    selbase = cmds.ls(sl=1)
    seladd = []
    if len(selbase)==2:
        sel1 = selbase[0]
        sel2 = selbase[1]
        cmds.select(cl=1)
        cmds.select(sel1,hi=1,vis=1)
        selsourceall = cmds.ls(sl=1,ext=tartyp)
        cmds.select(cl=1)
        cmds.select(sel2,hi=1,vis=1)
        seltargetall = cmds.ls(sl=1,ext=tartyp,v=1)
        cmds.select(cl=1)
        for i in range(len(selsourceall)):
            sourcepv = cmds.polyEvaluate(selsourceall[i],v=True)
            sourcepuv = cmds.polyEvaluate(selsourceall[i],uv=True)
            sourcee = cmds.polyEvaluate(selsourceall[i],e=True)
            u=0
            while u<len(seltargetall):
                tarpv = cmds.polyEvaluate(seltargetall[u],v=True)
                tarpuv = cmds.polyEvaluate(seltargetall[u],uv=True)
                tare= cmds.polyEvaluate(seltargetall[u],e=True)
                if sourcepv ==tarpv and sourcepuv ==tarpuv and sourcee == tare:
                    sourceSGs = cmds.listConnections(selsourceall[i],s=0,type="shadingEngine")
                    sourceSG=json.dumps(sourceSGs)
                    SG2Source = cmds.listConnections(sourceSGs[0],d=0)
                    sourceSGsp = sourceSG.split('"')
                    SG2mat = [m for m in SG2Source if m not in objls]
                    cmds.select(seltargetall[u])
                    cmds.sets(e=1,forceElement = sourceSGsp[1])
                    cmds.select(cl=1)
                    seladd.append(seltargetall[u])
                u=u+1
        selnos =[i for i in seltargetall if i not in seladd]
        for i in range(len(selnos)):
            selno = json.dumps(selnos[i])
            selnosp = selno.split('"')
            cmds.warning(selnosp[1]+"��ƥ��ģ��")
        selnosobj = cmds.pickWalk(selnos,d="up")
        cmds.select(selnosobj)
        cmds.delete(sel1)
    else:
        cmds.warning("��ѡ��Դ����Ŀ����")
def reNmae(arg):
    value=cmds.textField('cmm',q=True,tx=True)
    rname=cmds.ls(typ=("aiImage","alSurface","layeredShader","alHair","alLayer",'aiUtility','aiStandard','aiWriteColor','file','place2dTexture','displacementShader','bump2d','shadingEngine','ramp','blendColors','condition','gammaCorrect','luminance','samplerInfo','surfaceLuminance','aiSkin','aiHair'))
    ron=["initialParticleSE","initialShadingGroup"]
    ret = [i for i in rname if i not in ron]
    for n in range(0,len(ret)):
            cmds.rename(ret[n],value)
    mm.eval('hyperShadePanelMenuCommand("hyperShadePanel", "deleteUnusedNodes");') 

def SJ_shaderTranswdUI():
	if cmds.window('shadertr',ex=True):
	    cmds.deleteUI('shadertr',wnd=True)
	cmds.window('shadertr',t='shaderTransTool_V2.0')
	cmds.columnLayout(adj=True)
	cmds.text(l='����ƥ��ģ��,�������ݲ���',fn='fixedWidthFont',h=50,ann="1.��������ʵ�ģ���ļ� \n 2.��ѡ�����ģ���飬��ѡ����Ҫ���ݲ��ʵ�ģ����  \n 3.ȷ�����ɴ��ݣ�ȷ�������뱻���ݵ�ģ������һ�£�uvһ�£� \n 4.��ƥ��Ŀ��ģ�ͻᱻѡ��")
	cmds.button(l='ȷ��', c=shdtr,h=50)
	cmds.text(l='���������в��ʽڵ� \n �������������ò��ʽڵ�', fn='fixedWidthFont',h=50,ann="֧�����ͣ�\n aiImage,alSurface,layeredShader,alHair,alLayer \n aiUtility,aiStandard,aiWriteColor,File,place2dTexture \n displacementShader,bump2d,shadingEngine,ramp,blendCol \n ors,Condition,gammaCorrect,luminance,samplerInfo,surf \n aceLuminance ,aiSkin,aiHair \n ����Ҫ����µĽڵ����ͣ�����ϵ��˼��" )
	cmds.textField('cmm',tx="newName",h=30)
	cmds.button(l='ȷ��',h=50,c=reNmae)
	
	cmds.showWindow()