#coding=cp936
#coding=utf-8

'''
������ʧ����ģ�ͣ�ck_missshader()
�������渳�����ģ�ͣ�ck_faceshader()
ck_meshcheck()

'''
import maya.cmds as cmds
#���ģ�顾������ʽ��[��ʧ����ģ��,...],[���渳��ģ��,...]��
def ck_meshcheck(checknum=None):
    if checknum ==None:
        meshsels = cmds.ls(type="mesh")
    else:
        geoGrp = cmds.ls("*:*_geo")+cmds.ls("*_geo")+cmds.ls("*:*other_G")+cmds.ls("*other_G")
        if geoGrp!=[]:
            meshsels = [a for a in cmds.listRelatives(geoGrp,f=1,ad=1,type="mesh") if a.find("Orig")==-1]
        else:
            meshsels = []
    faceshadermesh =[]
    missfacemesh = []
    for meshsel in meshsels:
        subshapejudge = cmds.ls(cmds.listConnections(meshsel,s=0),type=["curveFromMeshEdge","normalConstraint"])
        if subshapejudge==[]:
            sgs = cmds.listConnections(meshsel,type="shadingEngine")
            if not sgs:
                if meshsel not in missfacemesh:
                    missfacemesh.append(meshsel)
            else:
                for sg in sgs:
                    if cmds.listConnections(sg+".aiSurfaceShader",d=0)!=None or cmds.listConnections(sg+".surfaceShader",d=0)!=None:
                        if cmds.listConnections(sg+".surfaceShader",d=0)!=None:
                            shader = cmds.listConnections(sg+".surfaceShader",d=0)
                        else:
                            shader = cmds.listConnections(sg+".aiSurfaceShader",d=0)
                        if not cmds.ls(shader,mat=1):
                        	cmds.warning(shader+"���ǲ������ͣ�����")
    allSgNodes=cmds.ls(type='shadingEngine')
    for i in allSgNodes:
    	sgMembers =  cmds.sets(i,q=1)
        if sgMembers:
            for n in sgMembers:
                if n.find(".f[")!=-1 :
                    tfNode=n.split('.')[0]
                    faceshadermesh.append(tfNode)
	                
            '''if sgs!=None:
                sgs = list(set(cmds.listConnections(meshsel,type="shadingEngine")))
                for sg in sgs:
                    if cmds.listConnections(sg+".aiSurfaceShader",d=0)!=None or cmds.listConnections(sg+".surfaceShader",d=0)!=None:
                        if cmds.listConnections(sg+".surfaceShader",d=0)!=None:
                            shader = cmds.listConnections(sg+".surfaceShader",d=0)
                        else:
                            shader = cmds.listConnections(sg+".aiSurfaceShader",d=0)
                        if  cmds.ls(shader,mat=1) !=[]:
                            shader = shader[0] 
                            cmds.hyperShade(objects = shader)
                            meshseleds =  cmds.sets(sg,q=1)
                            for meshseled in meshseleds:
                                if meshseled.find(cmds.listRelatives(meshsel,p=1)[0])!=-1 and meshseled.find(".f[")!=-1 :
                                    faceshadermesh.append(meshsel)
                        else:
                            cmds.warning(shader+"���ǲ������ͣ�����")
            else:
                if meshsel not in missfacemesh:
                    missfacemesh.append(meshsel)'''
    missfacemesh =[a for a in list(set(missfacemesh)) if a.find("Orig")==-1]
    return missfacemesh,list(set(faceshadermesh))

#�޸����渳�����ģ��
def fixedfaceshader():
    meshape = cmds.ls(type="mesh")
    multishape = []
    faceshapesel =[]
    for m in range(len(meshape)):
        sg = cmds.listConnections(meshape[m],d=0,type="shadingEngine")
        if  sg!=[]:
            if len(sg)==1:
                if cmds.listConnections(sg[0]+".surfaceShader",d=0)!=[]:
                    shder =  cmds.listConnections(sg[0]+".surfaceShader",d=0)[0]
                    cmds.select(meshape[m])
                    cmds.hyperShade(a = shder)
                    faceshapesel.append(meshape[m])
            else:
                multishape.append(meshape[m])
    mesh = cmds.pickWalk(multishape,d="up")
    cmds.select(mesh,r=1)
    cmds.warning( u"���޸�"+str(len(faceshapesel))+u"�����渳�����ģ��!!")

#ѡ�ж�ʧ����ģ��
def fixedmisshader():
    missshadersels = ck_missshader()
    cmds.select(missshadersels,r=1)
    cmds.warning( u"��ѡ��"+str(len(missshadersels))+u"����ʧ����ģ��!!")

#������ʧ����ģ��
def ck_missshader(checknum=None):
    return ck_meshcheck(checknum)[0]
#�������渳�����ģ��
def ck_faceshader():
    return ck_meshcheck()[1]
    
if __name__=="__main__":
    ck_missshader()