#coding=cp936
#coding=utf-8
import maya.cmds as cmds
import pymel.core as pm


def yetiwritecache(arg):
    path =cmds.textField('pathnum',tx=1,q=1).replace("\\","/")
    rangea =cmds.textField('rangenuma',tx=1,q=1)
    rangeb =cmds.textField('rangenumb',tx=1,q=1)
    rangesam =cmds.textField('rangesamnum',tx=1,q=1)
    yetitype =pm.ls(type="pgYetiMaya")
    yetisel =[i.split(":")[-1] for i in pm.selected() if i.getShape() in yetitype]
    yetisels =[i for i in pm.selected() if i.getShape() in yetitype]
    for i in range(len(yetisel)):
        furname =  yetisels[i].replace(":","__")
        pm.select(cl=1)
        pm.select(yetisels[i],r=1)
        pm.pgYetiCommand(writeCache=path+"/"+furname+".%04d.fur",range=(int(rangea),int(rangeb)),samples=int(rangesam))
    print "�����"+str(len(yetisel))+"��ë���ڵ�!!",
def changecache(arg):
    switchcb= pm.checkBox("switch" ,q=True,v=True)
    singlecb= pm.checkBox("single" ,q=True,v=True)
    path =cmds.textField('pathnum',tx=1,q=1).replace("\\","/")
    yetitype =pm.ls(type="pgYetiMaya")
    yetisel =[i.split(":")[-1] for i in pm.selected() if i.getShape() in yetitype]
    yetifurname = [i for i in pm.selected() if i.getShape() in yetitype]
    yetisels =[i for i in pm.selected() if i.getShape() in yetitype]
    for i in range(len(yetisel)):
        if singlecb ==1:
            timevalue = int(pm.currentTime( query=True ))
            pm.setAttr(yetisels[i]+".cacheFileName",str(path+"/"+yetifurname[i].replace(":","__")+"."+timevalue+".fur"))
        else: 
            pm.setAttr(yetisels[i]+".cacheFileName",str(path+"/"+yetifurname[i].replace(":","__")+".%04d.fur")) 
        if  switchcb==0:
            try:
                pm.setAttr(yetisels[i]+".fileMode",1) 
            except:
                print "ë��ģʽ�л����󣡣�",
        else:
            try:
                pm.setAttr(yetisels[i]+".fileMode",2) 
            except:
                print "ë��ģʽ�л����󣡣�",
        print path+"/"+yetifurname[i].replace(":","__")+".%04d.fur"
    print "�����"+str(len(yetisel))+"��ë���ڵ�!!",  

def SJ_yetiCachewdUI():
	if pm.window('yeticache',ex=True):
	    pm.deleteUI('yeticache',wnd=True)
	pm.window('yeticache',t='yeticacheV3.1')
	pm.columnLayout(adj=True,w=240)
	pm.text(l='֡�����䣨��ʼ֡������֡��Sample',fn='fixedWidthFont',h=50,ann="����˵��V3.1���޸�����ë��·���У������ë������·�����ֲ�ƥ������")
	pm.flowLayout( columnSpacing=0)
	pm.textField('rangenuma',tx="0",h=30,w=80)
	pm.textField('rangenumb',tx="1",h=30,w=80)
	pm.textField('rangesamnum',tx="1",h=30,w=80)
	pm.setParent( '..' )
	pm.text(l='ë����������·��', fn='fixedWidthFont',h=50,ann="" )
	pm.flowLayout( columnSpacing=0)
	pm.checkBox("switch" ,label='�л�yeti1.3.19',ann="",h=50,w=120)
	pm.checkBox("single" ,label="��֡����ָ��",ann="",h=50,w=120)
	pm.setParent( '..' )
	pm.textField('pathnum',tx="D:/textest/fur",h=30)
	pm.button(l=r'�������ë������',c=yetiwritecache,h=50)
	pm.button(l=r'�����滻ë������·��',c=changecache,h=50)
	
	pm.showWindow()