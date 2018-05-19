#!/usr/bin/python
#coding=utf-8
#--author--:dengtao
#--date--:2017-10-17
import maya.cmds as cmds
def k_mayaMax_camTransfer():
    u'''
    {'load':'maya_tool','defaultOption':1,'CNname':'Maya立体相机转Max'}
    '''
    cames=[a for  a in cmds.ls( sl=True ) if cmds.ls(cmds.listRelatives(a,c=1),type="camera")!=[]]
    if cames!=[]:
        cmds.cycleCheck (e=0)
        stm=cmds.playbackOptions( q=True,minTime=True) 
        etm=cmds.playbackOptions( q=True,maxTime=True)
        timRgs=etm-stm+1
        timRg=int(timRgs)
        
        cmds.polyCube(name='locS_') 
        cmds.delete('locS_*')
    
        localS=[]
    
        for i in cames:
            loco1=cmds.spaceLocator(name=i)
            loco1New=cmds.rename('locS_'+loco1[0])
            cmds.addAttr( longName='FlimOffset', attributeType='double3' )
            cmds.addAttr( longName='XX', attributeType='double', parent='FlimOffset' )
            cmds.addAttr( longName='YY', attributeType='double', parent='FlimOffset' )
            cmds.addAttr( longName='focalLen', attributeType='double', parent='FlimOffset' )
            localS.append(loco1New)
    
        for i2 in range(0,timRg+1,1):
            cons=0
            for i3 in cames:
                cmds.select(i3)
                caT=cmds.xform(q=1,ws=1,t=1)
                caR=cmds.xform(q=1,ws=1,ro=1)
                hfa=cmds.camera(i3, q=True,  hfa=True)
                vfa=cmds.camera(i3, q=True,  vfa=True)
                hfo=cmds.camera(i3, q=True,  hfo=True)
                vfo=cmds.camera(i3, q=True,  vfo=True)
                horHo=hfo/hfa 
                vorHo=vfo/hfa
                cFL = cmds.camera(cames[cons], q=True, hfv=True)
                cmds.setAttr(localS[cons]+'.XX', (horHo*-1) )
                cmds.setAttr(localS[cons]+'.YY', (vorHo*-1) )
                cmds.setAttr(localS[cons]+'.focalLen',cFL)
                cmds.setKeyframe(localS[cons], at='XX')
                cmds.setKeyframe(localS[cons], at='YY' )
                cmds.setKeyframe(localS[cons], at='focalLen' ) 

                cmds.setAttr(localS[cons]+'.tx',caT[0])
                cmds.setAttr(localS[cons]+'.ty',caT[1])
                cmds.setAttr(localS[cons]+'.tz',caT[2])
                cmds.setAttr(localS[cons]+'.rx',caR[0])
                cmds.setAttr(localS[cons]+'.ry',caR[1])
                cmds.setAttr(localS[cons]+'.rz',caR[2])
                cmds.setKeyframe(localS[cons], at='tx' )
                cmds.setKeyframe(localS[cons], at='ty' )
                cmds.setKeyframe(localS[cons], at='tz' )
                cmds.setKeyframe(localS[cons], at='rx' )
                cmds.setKeyframe(localS[cons], at='ry' )
                cmds.setKeyframe(localS[cons], at='rz' )
                cons=cons+1
            cmds.currentTime(stm+i2)
        cmds.currentTime(stm)
        print  "MayaCamLocater is created!!",
    else:
        cmds.warning("please select Target camera and do it again!!")
if __name__ =="__main__":
    k_mayaMax_camTransfer()