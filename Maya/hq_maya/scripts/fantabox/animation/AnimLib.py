#!/usr/bin/env python
# -*- coding: cp936 -*-
#coding = utf-8

import maya.cmds as cmds
from functools import partial
import os
import getpass
import glob
import re
#import AniLibPath
import codecs
import maya.mel as mel
import sys
import AniEditWin
import makeAnimCurCycle
import C_save_Anifile
import C_mirrorCharacterAnimUI
reload(sys)
sys.setdefaultencoding('gb18030')
##cmds.window('AnimateLibWin',q=1,wh=1)

mel.eval('global string $allpath;global string $allpathfile;source "O:/hq_tool/Maya/hq_maya/scripts/fantabox/animation/animLib/inputAnim01.mel"')

class AniLibWin():
    #�����ڣ�
    def __init__(self):
#��ȡ�ƶ�·���ļ�
        f=open('O:/hq_tool/Maya/hq_maya/scripts/fantabox/animation/animLib/AniLibPath.py','r')
        ap=f.readlines()
        f.close()
        for line in ap:
            self.pathA1=line.encode('gbk')#ת���ȡ��ȷ·��
        pathA=self.pathA1[0:]
    #���ض���api
        aniLoaded = cmds.pluginInfo('animImportExport',query=True, l=True)
        if aniLoaded!=True:
            cmds.loadPlugin('animImportExport')
            aniLoaded = cmds.pluginInfo('animImportExport',query=True, l=True)
        self.user=getpass.getuser()
        if cmds.window("AnimateLibWin",ex=1):
            cmds.deleteUI("AnimateLibWin",window=1)
        #if cmds.control('AniWin',ex=1):
        #    cmds.deleteUI('AniWin',control=True)
        self.AnilibWindow=cmds.window('AnimateLibWin',t="���������ϵͳ",menuBar=1 ,wh=(705, 585),s=1)
        cmds.menu(label=u'�ļ�',tearOff=True)
        cmds.menuItem(label=u"�������Ա",c=self.ENTRYwin)
        cmds.menuItem(label=u"�˳�����Ա",c=self.SecedeUser)
        cmds.menu(label=u"����",helpMenu=True)
        cmds.menuItem(label="About",c=self.helpWin)
        cmds.rowColumnLayout( numberOfColumns=2, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 705) )
        cmds.text( label='')
        cmds.separator(bgc=(.5,.5,.6))
        cmds.setParent('..')
        rowlay=cmds.rowLayout(nc=8)
        cmds.text('usertext',l=u'�û�:',w=30)
        cmds.text('userlist',l=self.user,w=50)  
        cmds.button('Addanims',l=u'��Ӷ�����',bgc=(.7,.7,1),vis=1,c=self.doanilib)
        cmds.button('mirrorani',l=u'��������',bgc=(.7,.7,1),vis=1,c=self.mirrorani)
        cmds.button(l=u'ɾ�����',bgc=(.7,.7,1),vis=0)
        self.editwins=cmds.checkBox('cBWinS',label="WinSizeable",onc=self.ON,ofc=self.OFF)
        cmds.button(l=u'ˢ��',bgc=(.5,.9,.5),c='AnimLibWin.AniLibWin()')
        cmds.setParent('..')
        rowlayPath=cmds.rowLayout(nc=3)
        cmds.text('Pathtext',l=u'��·��:',w=40)
        self.allpat=cmds.textField('Path',tx=pathA,w=600,en=False,ec=self.EDITPATH_01)
        self.textFieldenable=cmds.checkBox('Path001EN',label="enable",onc=self.ONTEXTfon,ofc=self.ONTEXTfoff)
        cmds.setParent('..')
        findlayPath=cmds.rowLayout(nc=3)
        cmds.text('findobj',l=u'����:',w=40)
        self.FindObj=cmds.textField('Name',tx='',w=150,en=True,ec=self.FINDOBJ)
        self.PicS=cmds.intSlider('picSize',min=0,max=200,value=100,w=200,step=1,cc=self.EDITSbSIZE)
        cmds.setParent('..')     
        self.column = cmds.columnLayout('column')
        self.theForm=cmds.formLayout('theForm')
        self.t1 = cmds.treeView('ok',w=50,h=500)
        self.column1 =cmds.rowLayout('column1',nc=2)
        cmds.text(l=u'��������:')
        self.AniName=cmds.textField('aniName',tx='',w=220,editable=False)
        cmds.setParent('..')
        self.tuplistlayout=cmds.tabLayout('tuplistlayout',h=520,w=100)
        cmds.setParent('..')        
        self.column2 =cmds.rowLayout('column2',nc=2)
        cmds.text(l=u'����:')
        cmds.textField('aa',tx=u'����Ԩ��SevinChen��', w=220,editable=False)
        cmds.setParent('..')
        self.column3 = cmds.rowLayout('column3',nc=2)
        cmds.text(l=u'����:')
        cmds.textField (tx='2014/10',w=220,editable=False)
        cmds.setParent('..')
        self.column4 = cmds.rowLayout('column4',nc=2)
        cmds.text(l=u'·��:')
        self.dzlj=cmds.textField('dzlj',tx='',w=220,editable=False)
        cmds.setParent('..')
        self.column5 = cmds.rowLayout('column5',nc=1)
        b1 = cmds.button(l=u'��ӱ�ע',en=1,bgc=(.5 ,1 ,.5 ),c=self.addbeizhu)
        cmds.setParent('..')
        self.column6 = cmds.rowLayout('column6',nc=1)
        t6 = cmds.scrollField('t6',wordWrap=True,text=u'��')
        cmds.setParent('..')
        self.column7 =cmds.rowLayout('column7',nc=1)
        self.img=cmds.image('Pic',image ='O:/hq_tool/Maya/hq_maya/scripts/fantabox/animation/animLib/С��.jpg')
        cmds.setParent('..')
        self.column8 = cmds.gridLayout('column8',numberOfColumns=3,cw=85)
        cmds.button(l=u'�ۿ���Ƶ',bgc=(.5, .8, 1),c=self.OPENVIDEO)
        cmds.button(l=u'ʹ�ö���',bgc=(.5, .8, 1),c=self.IMPPORTwin)
        cmds.popupMenu()
        cmds.menuItem(l=u'�߼�����',c=self.gaojiani)
        cmds.button(l=u'���ļ�',bgc=(.5 ,.8, 1),c=self.OPENMB)
        cmds.popupMenu('ButtonPM')
        cmds.menuItem(l=u'���ļ���',c=self.OPENFILE)
        cmds.formLayout('theForm',e=True,
        attachForm=[('ok', 'top', 0),('ok', 'left' ,0),('ok', 'bottom', 0),('ok', 'right', 550),
            ('column1','top',5),('column1','right',0),('column2','top',30),('column2','right',0),
            ('column3','top',55),('column3','right',0),('column4','top',75),('column4','right',0),
            ('column5','top',95),('column5','right',0),('column6','top',115),('column6','right',0),
            ('column7','top',335),('column7','right',0),('column8','top',500),('column8','right',0),('tuplistlayout', "top", 0),('tuplistlayout', "right", 300)],
        attachPosition=[('column1','left',0, 60),('column2','left',0, 63),('column3','left',0, 63),('column4','left',0, 63),
            ('column5','left',0, 63),('column6','left',0, 63),('column7','left',0, 63),('column8','left',0, 63),('tuplistlayout',"left" , 0, 25)],
        attachControl=[('column1','bottom',0,'ok'),('column2','bottom',0,'ok'),('column3','bottom',0,'ok'),('column4','bottom',0,'ok'), 
            ('column5','bottom',0,'ok'),('column6','bottom',0,'ok'),('column7','bottom',0,'ok'),('column8','bottom',0,'ok'),('tuplistlayout', "bottom", 0 ,'ok')] )   
        cmds.showWindow('AnimateLibWin')
        cmds.window('AnimateLibWin',e=True,wh=(405, 670),s=1)
        #allowedAreas = ['right', 'left']
        #cmds.dockControl('AniWin',l='AniWin',area='left', content='AnimateLibWin', allowedArea=allowedAreas )

        #�����������Ŀ
        getpath=cmds.textField('Path',q=True,tx=True)
        delto=getpath.replace('\\','/')#�޸�·��
        path=delto+'/'    
        WJno=cmds.getFileList(folder=path)
        for i in WJno:
            cmds.treeView('ok',edit=True,addItem=(i,''))
            WJno1=cmds.getFileList(folder=path+i+'/')
            if WJno1!=[]:
                for j in WJno1:
                    pt=path+i+'/'+j+'/'
                    cmds.treeView('ok',edit=True,addItem=(j,i),scc=self.REN)
###############################
#############################
#����·��__���붯��
    def eidtpath(self,ppath,*args):
        pathA=self.pathA1[0:]
        getpath=cmds.textField('Path',q=True,tx=True)
        delto=getpath.replace('\\','/')
        path=delto+'/'    
        trvsel=cmds.treeView('ok',q=True,si=True)
        trvselP=cmds.treeView('ok',q=True,ip=trvsel[0])
        object=cmds.tabLayout('tuplistlayout',q=True,st=True)
        Path1=path+trvselP+'/'+trvsel[0]+'/'+object[0:]+'/'
        cmds.textField('dzlj',e=True,tx=ppath)
        tFpath=cmds.textField('dzlj',q=True,tx=True)
        amin=[w for w in os.listdir(tFpath) if w.endswith('.anim')]
        picc=[h for h in os.listdir(tFpath) if h.endswith('.jpg')]
        txt=[j for j in os.listdir(tFpath) if j.endswith('.txt')]
        cmds.textField('aniName',e=True,tx=amin[0])
        cmds.image('Pic',e=True,image=tFpath+picc[0])    
        if len(txt)==0:
            cmds.scrollField('t6',e=True,text='û��txt�ļ���')
        else:            
            fileId=open((tFpath+txt[0]),'r') 
            filereadline=fileId.readline()
            if len(filereadline)==0:
                cmds.scrollField('t6',e=True,text='û��ע')
            else: 
                fileId1=open((tFpath+txt[0]),'r')          
                for obj in fileId1:
                    cmds.scrollField('t6',e=True,text=obj)
                fileId.close()
            fileId.close()
    
    ##############������
        sels=cmds.ls(sl=True)  
        if len(sels)==0:
            print "��ѡ������������"
        else:
            if ':' in list(sels[0]):  
                selupobjectcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'Spine_joint7'),c=True)
                lshoulder=selupobjectcns.index(str(sels[0].split(':')[0])+':'+'LeftArm_scalingCompensate')
                rshoulder=selupobjectcns.index(str(sels[0].split(':')[0])+':'+'RightArm_scalingCompensate')
                seldnobjectcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'Spine_joint1'),c=True)
                lleg=seldnobjectcns.index(str(sels[0].split(':')[0])+':'+'LeftLeg_scalingCompensate')
                rleg=seldnobjectcns.index(str(sels[0].split(':')[0])+':'+'RightLeg_scalingCompensate')
                selobjectIKcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'IK'),c=True)
                larmik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'LeftArm_IK')
                rarmik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'RightArm_IK')
                lfootik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'LeftLeg_IK')
                rfootik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'RightLeg_IK')
                if lshoulder>rshoulder:
                    cmds.confirmDialog(title='Confirm', message='LR���ǿ������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR���ǿ������㼶����')
                if rleg>lleg:
                    cmds.confirmDialog(title='Confirm', message='LR��֫�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫�������㼶����')
                if larmik>rarmik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                if rfootik>lfootik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                else:
                    mel.eval("inputAnim01")
            else:
                selupobjectcns=cmds.listRelatives('Spine_joint7',c=True)
                lshoulder=selupobjectcns.index('LeftArm_scalingCompensate')
                rshoulder=selupobjectcns.index('RightArm_scalingCompensate')
                seldnobjectcns=cmds.listRelatives('Spine_joint1',c=True)
                lleg=seldnobjectcns.index('LeftLeg_scalingCompensate')
                rleg=seldnobjectcns.index('RightLeg_scalingCompensate')
                selobjectIKcns=cmds.listRelatives('IK',c=True)
                larmik=selobjectIKcns.index('LeftArm_IK')
                rarmik=selobjectIKcns.index('RightArm_IK')
                lfootik=selobjectIKcns.index('LeftLeg_IK')
                rfootik=selobjectIKcns.index('RightLeg_IK')
                if lshoulder>rshoulder:
                    cmds.confirmDialog(title='Confirm', message='LR���ǿ������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR���ǿ������㼶����')
                if rleg>lleg:
                    cmds.confirmDialog(title='Confirm', message='LR��֫�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫�������㼶����')
                if larmik>rarmik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                if rfootik>lfootik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                else:
                    mel.eval("inputAnim01")

##############################################
##############################################
###############################
#############################
#����·��__���붯��
    def showFileInfo(self,ppath,*args):
        pathA=self.pathA1[0:]
        getpath=cmds.textField('Path',q=True,tx=True)
        delto=getpath.replace('\\','/')
        path=delto+'/'    
        trvsel=cmds.treeView('ok',q=True,si=True)
        trvselP=cmds.treeView('ok',q=True,ip=trvsel[0])
        object=cmds.tabLayout('tuplistlayout',q=True,st=True)
        Path1=path+trvselP+'/'+trvsel[0]+'/'+object[0:]+'/'
        cmds.textField('dzlj',e=True,tx=ppath)
        tFpath=cmds.textField('dzlj',q=True,tx=True)
        amin=[w for w in os.listdir(tFpath) if w.endswith('.anim')]
        picc=[h for h in os.listdir(tFpath) if h.endswith('.jpg')]
        txt=[j for j in os.listdir(tFpath) if j.endswith('.txt')]
        cmds.textField('aniName',e=True,tx=amin[0])
        cmds.image('Pic',e=True,image=tFpath+picc[0])    
        if len(txt)==0:
            cmds.scrollField('t6',e=True,text='û��txt�ļ���')
        else:            
            fileId=open((tFpath+txt[0]),'r') 
            filereadline=fileId.readline()
            if len(filereadline)==0:
                cmds.scrollField('t6',e=True,text='û��ע')
            else: 
                fileId1=open((tFpath+txt[0]),'r')          
                for obj in fileId1:
                    cmds.scrollField('t6',e=True,text=obj)
                fileId.close()
            fileId.close()
            
    #�޸�WinSizeable
    def on(self):
           cmds.window(self.AnilibWindow,e=True,wh=(405, 670),s=1)
    def off(self):
           cmds.window(self.AnilibWindow,e=True,wh=(405, 670),s=0)
    def ontextFOFF(self):
            cmds.textField('Path',e=True,en=False)
    def ontextFON(self):
            cmds.textField('Path',e=True,en=True)

    #�г�������
    def ren(self):
        pathA=self.pathA1[0:]
        getpath=cmds.textField('Path',q=True,tx=True)
        delto=getpath.replace('\\','/')
        path=delto+'/'    
        tabLayoutlist=cmds.tabLayout('tuplistlayout',q=True,tabLabel=True)
        if tabLayoutlist==None:
            print 'no!'
        else:
            for tabLayoutlistobj in tabLayoutlist:
                cmds.deleteUI(tabLayoutlistobj,control=True)
        trvsel=cmds.treeView('ok',q=True,si=True)
        trvselP=cmds.treeView('ok',q=True,ip=trvsel[0])
        Path=path+trvselP+'/'+trvsel[0]+'/'
        id=cmds.getFileList(folder=Path) 
        for k in id:
            cmds.scrollLayout(k,p='tuplistlayout',nch=2)#����
            cmds.tabLayout('tuplistlayout',edit=True,tabLabel=(k, k ),sc=self.P)
            
        self.P()
    
    def p(self):  
        pathA=self.pathA1[0:]
        getpath=cmds.textField('Path',q=True,tx=True)
        delto=getpath.replace('\\','/')
        path=delto+'/'    
        trvsel=cmds.treeView('ok',q=True,si=True)
        trvselP=cmds.treeView('ok',q=True,ip=trvsel[0])
        object=cmds.tabLayout('tuplistlayout',q=True,st=True)
        Path1=path+trvselP+'/'+trvsel[0]+'/'+object[0:]+'/'
        id1=cmds.getFileList(folder=Path1)
        slLc=cmds.scrollLayout(object[0:],q=True,ca=True)
        #cmds.rowColumnLayout('RowL',numberOfColumns=1,p=object[0:])
        if slLc!=None:
            for slLcobj in slLc:
                cmds.deleteUI(slLcobj,control=True)
        else:
            print 'û��'
        if cmds.formLayout('RowL',ex=True):
             cmds.deleteUI('RowL')
        #cmds.rowColumnLayout('RowL',numberOfColumns=1,p=object[0:])  
        cmds.formLayout('RowL',p=object[0:]) 
        ksymbolButtonk=[] 
        ktextk=[]
        k_tW=100
        k_tH=100 
        k_tH=20     
            
        for i in range(len(id1)):
            pic=[w for w in os.listdir(Path1+id1[i]+'/') if w.endswith('.jpg')]
            pp=Path1+id1[i]+'/'
            #cmds.symbolButton(image=(Path1+id1[i]+'/'+pic[0]),ann='oo',p='RowL',w=100,h=100,c=partial(self.showFileInfo,(Path1+id1[i]+'/'))) #����ͼƬ��ť 
            ksymbolButtonk.append(cmds.symbolButton(image=(Path1+id1[i]+'/'+pic[0]),p='RowL',w=k_tW,h=k_tH,c=partial(self.showFileInfo,(Path1+id1[i]+'/'))))#����ͼƬ��ť                    
            cmds.popupMenu()
            cmds.menuItem(l=u'���붯������',c = partial(self.eidtpath,(Path1+id1[i]+'/')))
            cmds.menuItem(l=u'�ۿ���Ƶ��',c=self.OPENVIDEO)
            cmds.menuItem(l=u'���ļ��У�',c=self.OPENFILE)
            cmds.menuItem(l=u'���ļ���',c=self.OPENMB)
            cmds.menuItem(l=u'��Ϣ�鿴�붯����ȡ',c=self.editaniwin)
            #cmds.text(l=id1[i],p='RowL')
            ktextk.append(cmds.iconTextButton (style=('textOnly'),enable=0,l=id1[i],w=k_tW,h=k_tH,p='RowL'))
            self.editSBsize()
            
        for o in range(len(id1)):
            if o==0:
                cmds.formLayout('RowL',e=True,attachPosition=((ksymbolButtonk[o],'top',0,0),(ksymbolButtonk[o],'left',0,0)))
            elif o==1:
                cmds.formLayout('RowL',e=True,attachPosition=(ksymbolButtonk[o],'top',0,0),attachControl=(ksymbolButtonk[o],'left',0,ksymbolButtonk[o-1]))
            elif o%2==1:  
                cmds.formLayout('RowL',e=True,attachControl=((ksymbolButtonk[o],'top',0,ktextk[o-2]),(ksymbolButtonk[o],'left',0,ksymbolButtonk[o-1])))
            else:
                cmds.formLayout('RowL',e=True,attachControl=(ksymbolButtonk[o],'top',k_tH,ksymbolButtonk[o-2]),attachPosition=(ksymbolButtonk[o],'left',0,0))

        for u in range(len(id1)):
            if u%2==1:
                cmds.formLayout('RowL',e=True,attachControl=((ktextk[u],'top',0,ksymbolButtonk[u]),(ktextk[u],'left',0,ktextk[u-1])))
            else:
                cmds.formLayout('RowL',e=True,attachControl=(ktextk[u],'top',0,ksymbolButtonk[u]),attachPosition=(ktextk[u],'left',0,0))            
    
    #�ı�shelfButton��С
    def editSBsize(self):
        whsize=cmds.intSlider('picSize',q=True,value=True)
        #contrlsName=cmds.rowColumnLayout('RowL',q=True,ca=True)
        contrlsName=cmds.formLayout('RowL',q=True,ca=True)    
        for i in range(len(contrlsName)):
            j=i+1
            if j%2==0:
                #cmds.text(contrlsName[i],e=True,w=whsize)
                cmds.iconTextButton(contrlsName[i],e=True,w=whsize)
            else:  
                cmds.symbolButton(contrlsName[i],e=True,w=whsize,h=whsize)
    #��mb�ļ�
    def openmb(self):
        VideoPath=cmds.textField('dzlj',q=True,tx=True)
        allPath=VideoPath+[w for w in os.listdir(VideoPath) if w.endswith('.mb')][0]
        os.startfile(allPath.replace('/','\\'))
    #�򿪶�ӦĿ¼�µ��ļ���
    def openfile(self):        
        filePath=cmds.textField('dzlj',q=True,tx=True) 
        os.startfile(filePath.replace('/','\\'))

#os.startfile('\\10.99.1.2\�����Ӱ\��ʱ����\02��������\02G��ɫ\Ա���ļ�\c_����Ԩ/')
    #�򿪶�Ӧ�Ĳο���Ƶ    
    def openVideo(self):
        VideoPath=cmds.textField('dzlj',q=True,tx=True)
        Video=[w for w in os.listdir(VideoPath) if w.endswith('.avi')]
        Path=VideoPath+Video[0]
        os.system(Path)
    
    #����ָ������
    def findobj(self):
        path=cmds.textField('Path',q=True,tx=True)     
        name=cmds.textField('Name',q=True,tx=True)
        if len(name)!=0:
            roesize=cmds.rowColumnLayout('RowL',q=1,ca=1)
            if roesize!=None:
                for obj in roesize:
                    cmds.deleteUI(obj,control=True)
            else:
                print "None"
            trvsel=cmds.treeView('ok',q=True,si=True)
            trvselP=cmds.treeView('ok',q=True,ip=trvsel[0])
            object=cmds.tabLayout('tuplistlayout',q=True,st=True)
            Path2=path+trvselP+'/'+trvsel[0]+'/'+object[0:]+'/'+name
            picc1=[w for w in os.listdir(Path2) if w.endswith('.jpg')]
            cmds.symbolButton(image=(Path2+'/'+picc1[0]),ann='oo',p='RowL',w=100,h=100,c=self.tjEDITtxOPENDG)         
            cmds.popupMenu()
            cmds.menuItem(l=u'�ۿ���Ƶ��',c=self.OPENVIDEO)
            cmds.menuItem(l=u'���ļ��У�',c=self.OPENFILE)
            cmds.menuItem(l=u'���ļ���',c=self.OPENMB)
            cmds.menuItem(l=u'��Ϣ�鿴�붯����ȡ',c=self.editaniwin)
            cmds.text(l=name,p='RowL')
    def TJeditTXopendg(self):
        path=cmds.textField('Path',q=True,tx=True)
        name=cmds.textField('Name',q=True,tx=True)
        trvsel=cmds.treeView('ok',q=True,si=True)
        trvselP=cmds.treeView('ok',q=True,ip=trvsel[0])
        object=cmds.tabLayout('tuplistlayout',q=True,st=True)
        Path3=path+trvselP+'/'+trvsel[0]+'/'+object[0:]+'/'+name+'/'
        cmds.textField('dzlj',e=True,tx=Path3)
        tFpath=cmds.textField('dzlj',q=True,tx=True)
        amin=[w for w in os.listdir(tFpath) if w.endswith('.anim')]
        picc=[w for w in os.listdir(tFpath) if w.endswith('.jpg')]
        txt1=[w for w in os.listdir(tFpath) if w.endswith('.txt')]
        cmds.textField('aniName',e=True,tx=amin[0])
        cmds.image('Pic',e=True,image=tFpath+picc[0])    
        if len(txt1)==0:
            cmds.scrollField('t6',e=True,text='û��txt�ļ���')
        else:            
            fileId=open((Path3+txt1[0]),'r')        
            for obj in fileId:
                cmds.scrollField('t6',e=True,text=obj)
            fileId.close()
######��鵼����
        self.findobjC() 
    #���붯��
    def impportWin(self):
        filePath=cmds.textField('dzlj',q=True,tx=True)
        if cmds.window('inputAnim',ex=True):
            cmds.deleteUI('inputAnim',window=True)
        cmds.window('inputAnim',t=u'InputAnim')
        cmds.columnLayout(adj=True)
        cmds.optionMenuGrp('aniname', label=u'�������ͣ�',columnWidth=(2, 30))
        allfiles=[w for w in os.listdir(filePath) if w.endswith('.anim')]
        for allfilesobj in allfiles:
            cmds.menuItem( label=allfilesobj )    
        cmds.button(l=u'���붯��',c=self.INPUTTANIM02)
        cmds.showWindow('inputAnim')
        cmds.window('inputAnim',e=True,wh=(405, 54))
        #cmds.deleteUI("inputAnim",window=True)
    def inputanim02(self):
        sels=cmds.ls(sl=True)  
        if len(sels)==0:
            print "��ѡ������������"
        else:
            if ':' in list(sels[0]):  
                selupobjectcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'Spine_joint7'),c=True)
                lshoulder=selupobjectcns.index(str(sels[0].split(':')[0])+':'+'LeftArm_scalingCompensate')
                rshoulder=selupobjectcns.index(str(sels[0].split(':')[0])+':'+'RightArm_scalingCompensate')
                seldnobjectcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'Spine_joint1'),c=True)
                lleg=seldnobjectcns.index(str(sels[0].split(':')[0])+':'+'LeftLeg_scalingCompensate')
                rleg=seldnobjectcns.index(str(sels[0].split(':')[0])+':'+'RightLeg_scalingCompensate')
                selobjectIKcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'IK'),c=True)
                larmik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'LeftArm_IK')
                rarmik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'RightArm_IK')
                lfootik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'LeftLeg_IK')
                rfootik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'RightLeg_IK')
                if lshoulder>rshoulder:
                    cmds.confirmDialog(title='Confirm', message='LR���ǿ������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR���ǿ������㼶����')
                if rleg>lleg:
                    cmds.confirmDialog(title='Confirm', message='LR��֫�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫�������㼶����')
                if larmik>rarmik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                if rfootik>lfootik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                else:
                    mel.eval("inputAnim02")
            else:
                selupobjectcns=cmds.listRelatives('Spine_joint7',c=True)
                lshoulder=selupobjectcns.index('LeftArm_scalingCompensate')
                rshoulder=selupobjectcns.index('RightArm_scalingCompensate')
                seldnobjectcns=cmds.listRelatives('Spine_joint1',c=True)
                lleg=seldnobjectcns.index('LeftLeg_scalingCompensate')
                rleg=seldnobjectcns.index('RightLeg_scalingCompensate')
                selobjectIKcns=cmds.listRelatives('IK',c=True)
                larmik=selobjectIKcns.index('LeftArm_IK')
                rarmik=selobjectIKcns.index('RightArm_IK')
                lfootik=selobjectIKcns.index('LeftLeg_IK')
                rfootik=selobjectIKcns.index('RightLeg_IK')
                if lshoulder>rshoulder:
                    cmds.confirmDialog(title='Confirm', message='LR���ǿ������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR���ǿ������㼶����')
                if rleg>lleg:
                    cmds.confirmDialog(title='Confirm', message='LR��֫�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫�������㼶����')
                if larmik>rarmik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                if rfootik>lfootik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                else:
                    mel.eval("inputAnim02")

#�޸�·��
    def editpath_01(self):
        path=cmds.textField('Path',q=True,tx=True)
        delto=path.replace('\\','/')
        path_01=delto+'/'
        path=cmds.textField('Path',e=True,tx=path_01)
        
#####��ӱ�ע
    def AddBeizhu(self):
        Listbeizhu=cmds.scrollField('t6',q=True,text=True)
        ListLJ=cmds.textField('dzlj',q=True,tx=True)
        txt1=[w for w in os.listdir(ListLJ) if w.endswith('.txt')]
        if len(txt1)==0:
            f=open((ListLJ+'aniInfo.txt'),'w')
            f.write(Listbeizhu)
            f.close() 
        else:            
            f=open((ListLJ+txt1[0]),'w+')
            f.write(Listbeizhu)
            f.close()
    ##�û�����
    def entryWin(self):
        if cmds.window('UserWin',ex=True):
                cmds.deleteUI('UserWin',window=True)
        cmds.window('UserWin',t=u'�û�����!')
        cmds.rowColumnLayout('laout02',nc=5)
        cmds.text(l=u'�û���:')
        cmds.textField('yonghuming',tx='')
        cmds.text(l=u'����:')
        cmds.textField('mima',tx='')
        cmds.button(l=u'���룡' ,c=self.EntryUser)
        cmds.showWindow('UserWin') 
        cmds.window('UserWin',e=1,wh=(339, 25))  
####################################
##############�����û�/////�˳��û�
    def entryuser(self):
        passworld=['Uys2817','Uys2828','Uys2839']
        users=['1700','1701','1702']
        userspassworld={'1700':'Uys2817','1701':'Uys2828','1702':'Uys2839'}
        User=cmds.textField('yonghuming',q=True,tx=True)
        Passworld=cmds.textField('mima',q=True,tx=True)
        if User in users:   
            if Passworld==userspassworld[User]:
                cmds.text('userlist',e=True,l=User)
                cmds.button('Addanims',e=True,vis=1)
                cmds.button('mirrorani',e=True,vis=1)
                cmds.deleteUI('UserWin')       
            else:
                cmds.confirmDialog( title='Confirm', message='Password Wrong', button='Yes', defaultButton='Yes', dismissString='No' )
        else:
            cmds.confirmDialog( title='Confirm', message='User Wrong', button='Yes', defaultButton='Yes', dismissString='No' )
###############################################
    def secedeuser(self):
        cmds.text('userlist',e=True,l=self.user)
        cmds.button('Addanims',e=True,vis=0) 
        cmds.button('mirrorani',e=True,vis=0)
        if cmds.objExists('Ani_camera'):                    
            cmds.delete('Ani_camera')
        if cmds.window('AnimCreateWin',ex=True):
            cmds.deleteUI('AnimCreateWin',window=True)
                       
    #����Ŀ�������
    def findobjC(self):
        sels=cmds.ls(sl=True)  
        if len(sels)==0:
            print "��ѡ������������"
        else:
            if ':' in list(sels[0]):  
                selupobjectcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'Spine_joint7'),c=True)
                lshoulder=selupobjectcns.index(str(sels[0].split(':')[0])+':'+'LeftArm_scalingCompensate')
                rshoulder=selupobjectcns.index(str(sels[0].split(':')[0])+':'+'RightArm_scalingCompensate')
                seldnobjectcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'Spine_joint1'),c=True)
                lleg=seldnobjectcns.index(str(sels[0].split(':')[0])+':'+'LeftLeg_scalingCompensate')
                rleg=seldnobjectcns.index(str(sels[0].split(':')[0])+':'+'RightLeg_scalingCompensate')
                selobjectIKcns=cmds.listRelatives((str(sels[0].split(':')[0])+':'+'IK'),c=True)
                larmik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'LeftArm_IK')
                rarmik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'RightArm_IK')
                lfootik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'LeftLeg_IK')
                rfootik=selobjectIKcns.index(str(sels[0].split(':')[0])+':'+'RightLeg_IK')
                if lshoulder>rshoulder:
                    cmds.confirmDialog(title='Confirm', message='LR���ǿ������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR���ǿ������㼶����')
                if rleg>lleg:
                    cmds.confirmDialog(title='Confirm', message='LR��֫�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫�������㼶����')
                if larmik>rarmik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                if rfootik>lfootik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                else:
                    mel.eval("inputAnim01")
            else:
                selupobjectcns=cmds.listRelatives('Spine_joint7',c=True)
                lshoulder=selupobjectcns.index('LeftArm_scalingCompensate')
                rshoulder=selupobjectcns.index('RightArm_scalingCompensate')
                seldnobjectcns=cmds.listRelatives('Spine_joint1',c=True)
                lleg=seldnobjectcns.index('LeftLeg_scalingCompensate')
                rleg=seldnobjectcns.index('RightLeg_scalingCompensate')
                selobjectIKcns=cmds.listRelatives('IK',c=True)
                larmik=selobjectIKcns.index('LeftArm_IK')
                rarmik=selobjectIKcns.index('RightArm_IK')
                lfootik=selobjectIKcns.index('LeftLeg_IK')
                rfootik=selobjectIKcns.index('RightLeg_IK')
                if lshoulder>rshoulder:
                    cmds.confirmDialog(title='Confirm', message='LR���ǿ������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR���ǿ������㼶����')
                if rleg>lleg:
                    cmds.confirmDialog(title='Confirm', message='LR��֫�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫�������㼶����')
                if larmik>rarmik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                if rfootik>lfootik:
                    cmds.confirmDialog(title='Confirm', message='LR��֫IK�������㼶����', button=['Yes'], defaultButton='Yes' )
                    cmds.error('LR��֫IK�������㼶����')
                else:
                    mel.eval("inputAnim01")
            
######
    #��ȡ����
    def EditAniWin(self):
        if cmds.window('Win',ex=True):
            cmds.deleteUI('Win',window=True)
        cmds.window('Win',t='��������')
        cmds.columnLayout('column',adj=True)
        cmds.rowColumnLayout('row01',numberOfColumns=2)
        cmds.showWindow('Win')
        Path_new=cmds.textField('dzlj',q=True,tx=True)
        AniName=cmds.textField('aniName',q=True,tx=True)
        anipath=Path_new+AniName
        f=open(anipath,'r')
        self.flist=f.readlines()[:9]
        self.flist_start_end=self.flist[5:7]
        f.close()    
        for flistobj in self.flist:
            flistobj_del=flistobj.split(' ')
            flistobj_del1=flistobj_del[1].split(';')
            cmds.text(str((flistobj_del[0])+'name'),l=(flistobj_del[0]+':'),p='row01')  
            cmds.textField((str(flistobj_del[0])+str(flistobj_del1[0])),en=False,tx=(str(flistobj_del1[0])),p='row01')
        cmds.button(l='�޸Ĳ���',p='column',c=self.ENtx)
        cmds.button(l='���붯��',p='column',c=self.NEWani)
    def en1Tx(self):
        Path_new=cmds.textField('dzlj',q=True,tx=True)
        AniName=cmds.textField('aniName',q=True,tx=True)
        anipath=Path_new+AniName
        f=open(anipath,'r')
        self.flist=f.readlines()[:9]
        self.flist_start_end=self.flist[5:7]
        f.close()    
        for flist_start_endobj in self.flist_start_end:
            flist_start_endobj_del=flist_start_endobj.split(' ')
            flist_start_endobj_del1=flist_start_endobj_del[1].split(';')
            QtxF=cmds.textField((str(flist_start_endobj_del[0])+str(flist_start_endobj_del1[0])),q=True,en=True)
            if QtxF==True:
                cmds.textField((str(flist_start_endobj_del[0])+str(flist_start_endobj_del1[0])),e=True,en=False)
            else:
                cmds.textField((str(flist_start_endobj_del[0])+str(flist_start_endobj_del1[0])),e=True,en=True)
    def newAni(self):
        selboss=cmds.ls(sl=1)
        if len(selboss)==0:
            cmds.confirmDialog(title='Confirm', message='��ѡ��boss��������', button=['Yes'], defaultButton='Yes' )
        else:
            self.findobjC()
            #mel.eval("inputAnim01")
            flist_start_del=self.flist_start_end[0].split(' ')
            flist_start_del1=flist_start_del[1].split(';') 
            Qtxfirstno=int(cmds.textField((str(flist_start_del[0])+str(flist_start_del1[0])),q=True,tx=True))
            flist_end_del=self.flist_start_end[1].split(' ')
            flist_end_del1=flist_end_del[1].split(';')  
            Qtxendno=int(cmds.textField((str(flist_end_del[0])+str(flist_end_del1[0])),q=True,tx=True))
            cmds.select(selboss)
            cmds.select(cmds.ls(selboss,sl=True,dag=True,typ='nurbsCurve'))
            sell=cmds.ls(sl=1)
            cmds.pickWalk(d='up')
            sel=cmds.ls(sl=1)
            #cmds.setKeyframe(sel,t=(Qtxendno+1))
            #���ñ���֡ ǰһ֡�Ĺؼ�֡
            cmds.currentTime((Qtxfirstno-1))
            cmds.setKeyframe(sel,breakdown=0,hierarchy='none',controlPoints=0,shape=0)
            cmds.currentTime((Qtxfirstno))
            cmds.setKeyframe(sel,breakdown=0,hierarchy='none',controlPoints=0,shape=0)
            #ɾ���������ǰ�ιؼ�֡
            cmds.selectKey(sel,k=True,t=(int(flist_start_del1[0]),(Qtxfirstno-1)))
            cmds.keyTangent(lock=0)
            cmds.cutKey(animation='keys',clear=True)  
            #���ñ���֡ ��һ֡�Ĺؼ�֡  
            cmds.currentTime((Qtxendno+1))
            cmds.setKeyframe(sel,breakdown=0,hierarchy='none',controlPoints=0,shape=0)
            cmds.currentTime(Qtxendno)
            cmds.setKeyframe(sel,breakdown=0,hierarchy='none',controlPoints=0,shape=0)        
            #ɾ���������ǰ�ιؼ�֡
            cmds.selectKey(sel,k=True,t=(int(flist_end_del1[0]),(Qtxendno+1)))
            cmds.keyTangent(lock=0)
            cmds.cutKey(animation='keys',clear=True)  
###########################
#helpwin_pic
    def HelpWin(self):
        os.startfile('O:/hq_tool/Maya/hq_maya/scripts/fantabox/animation/animLib/anilibhelp.chm')
#############################
#######�޸Ķ�����·��~~~���޸���
###�߼�����
    def GaoJiAni(self):
        AniEditWin.inputAniWin() 
###����������
    def DoAnilib(self):   
        C_save_Anifile.main() 
###��������
    def MirrorAni(self):
        C_mirrorCharacterAnimUI.main()                         
#############################################
    def ON(self,*args):
        self.on()
    def OFF(self,*args):
        self.off()
    def REN(self,*args):        
        self.ren()
    def P(self,*args):        
        self.p()
    def EDITSbSIZE(self,*args):         
        self.editSBsize()
    def OPENMB(self,*args):         
        self.openmb()        
    def OPENFILE(self,*args):         
        self.openfile()        
    def OPENVIDEO(self,*args):         
        self.openVideo()        
    def FINDOBJc(self,*args):         
        self.findobjC()               
    def FINDOBJ(self,*args):         
        self.findobj()     
    def tjEDITtxOPENDG(self,*args):         
        self.TJeditTXopendg()     
    def IMPPORTwin(self,*args):         
        self.impportWin()
    def INPUTTANIM02(self,*args):         
        self.inputanim02()    
    def ENTRYwin(self,*args):         
        self.entryWin()               
    def ONTEXTfoff(self,*args):       
        self.ontextFOFF()
    def ONTEXTfon(self,*args):       
        self.ontextFON()
    def EDITPATH_01(self,*args):       
        self.editpath_01()        
    def editaniwin(self,*args):         
        self.EditAniWin()       
    def ENtx(self,*args):          
        self.en1Tx()        
    def NEWani(self,*args):          
        self.newAni()
    def helpWin(self,*args):          
        self.HelpWin()
    def addbeizhu(self,*args):          
        self.AddBeizhu()        
    def EntryUser(self,*args):          
        self.entryuser() 
    def SecedeUser(self,*args):          
        self.secedeuser() 
    def gaojiani(self,*args):          
        self.GaoJiAni()
    def doanilib(self,*args):          
        self.DoAnilib()        
    def mirrorani(self,*args):          
        self.MirrorAni() 

        

