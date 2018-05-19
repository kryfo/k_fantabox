#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
def comshder(arg):
    SGsel =pm.ls(type="shadingEngine")
    shader = [pm.listConnections(i+".surfaceShader",d=0)[0] for i in  SGsel if pm.listConnections(i+".surfaceShader",d=0)!=[]]
    shaderdict ={}
    mushder = []
    for s in range(len(shader)):
        if len(shader[s].split(":"))!=1:
            choicefile = [h for h in pm.hyperShade(listUpstreamNodes = shader[s]) if pm.nodeType(h)=="file" and pm.listConnections(h+".fileTextureName",d=0,type="choice")!=[]]
            if choicefile==[]:
                shdernickname =  shader[s][-len(shader[s].split(":")[-1]):]
                if shdernickname not in shaderdict.keys():
                    shaderdict[shdernickname]=shader[s]     
                else:
                    sg =  pm.listConnections(shader[s],s=0,type="shadingEngine")
                    for g in range(len(sg)):
                        if pm.listConnections(sg[g],d=0,type="mesh")!=[] or pm.listConnections(sg[g],s=0,type="mesh")==[]:
                            pm.hyperShade(objects = shader[s])
                            pm.hyperShade(assign = shaderdict[shdernickname])
                            print u"%s �������滻Ϊ%s���ʣ���"%(shader[s],shaderdict[shdernickname]),
            else:
                mushder.append(shader[s])
    multistnickname =[]
    multistpath =[]
    multistshder = []
    multistifile =[]
    mushaderdict ={}
    for m in range(len(mushder)):
        multichoicefile = [h for h in pm.hyperShade(listUpstreamNodes = mushder[m]) if pm.nodeType(h)=="file" and pm.listConnections(h+".fileTextureName",d=0,type="choice")!=[]]
        mutlichfilepath  = pm.getAttr(multichoicefile[0]+".fileTextureName")
        shdernicknames =  mushder[m][-len(mushder[m].split(":")[-1]):]
        if multichoicefile not in multistifile:
            if  shdernicknames not in multistnickname and mutlichfilepath not in multistpath:
                multistnickname.append(shdernicknames)
                multistpath.append(mutlichfilepath)
                multistshder.append(mushder[m])
                multistifile.append(multichoicefile)
        else:
            if  shdernicknames not in multistnickname:
                multistnickname.append(shdernicknames)
                multistpath.append(mutlichfilepath)
                multistshder.append(mushder[m])
    mushders=[u for u in mushder if u not in multistshder]
    for ms in range(len(mushders)):
        multichoicefiles = [h for h in pm.hyperShade(listUpstreamNodes = mushders[ms]) if pm.nodeType(h)=="file" and pm.listConnections(h+".fileTextureName",d=0,type="choice")!=[]]
        mutlichfilepaths  = pm.getAttr(multichoicefiles[0]+".fileTextureName")
        shdernicknames =  mushders[ms][-len(mushders[ms].split(":")[-1]):]
        if shdernicknames in multistnickname :
            num = multistnickname.index(shdernicknames)
            if shdernicknames==multistnickname[num] and mutlichfilepaths ==multistpath[num]:
                sg =  pm.listConnections(mushders[ms],s=0,type="shadingEngine")
                for g in range(len(sg)):
                    if pm.listConnections(sg[g],d=0,type="mesh")!=[] and pm.listConnections(sg[g],s=0,type="mesh")==[]:
                        pm.hyperShade(objects = mushders[ms])
                        pm.hyperShade(assign = multistshder[num])
                        print u"%s �������滻Ϊ%s���ʣ���"%(mushders[ms], multistshder[num]),
    print "���������ͬ���ͽ�ɫ�Ĳ����滻����",

scriptPath = r"O:\hq_tool\Maya\hq_maya\scripts\fantabox\modeling".replace("\\","/")

def comshderwdUI():
	if pm.window('shaderToolwd',ex=True):
	    pm.deleteUI('shaderToolwd',wnd=True)
	pm.window('shaderToolwd',t='shaderToolV1.0')
	pm.columnLayout(adj=True)
	pm.text(l='���ʹ��߼�V1.0',fn='fixedWidthFont',annotation="",w=250,h=50,ann="")
	pm.button(l='Arnold���ʹ���',w=180,h=50,ann="",c=r'fb.mod.SJ_arnoldIDToolwdUI()')
	pm.button(l='���ʴ���',w=180,h=50,ann="",c=r'fb.mod.SJ_shaderTranswdUI()') 
	pm.button(l='����ת��',w=180,h=50,ann="",c=r'fb.mod.SJ_transferShaderwdUI()') 
	pm.button(l='������Ϣ���뵼������',w=180,h=50,ann="",c=r'mel.eval("shadingInfoIO")')
	pm.button(l='�ϲ���������ͬ����',w=180,h=50,ann="",c=comshder) 
	pm.button(l='SP����������',w=180,h=50,ann="",c=r'fb.mod.SJ_SpShaderMakerwdUI()') 
	pm.showWindow()     