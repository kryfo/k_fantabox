#coding=cp936
#coding=utf-8
import maya.cmds as cmds
import pymel.core as pm
import os

def anisymb(arg):
    errornum =[]
    sel =cmds.ls(sl=1)
    #print cmds.listAttr(r=1,channelBox=1)
    if sel!=[]:
        selall = cmds.listRelatives(sel[0],allDescendents=1)
        lsel =[]
        rsel=[]
        msel=[]
        allsel =[]
        pairblendnum =[]
        unvail =["Global"]
        spadj=["FKChest_M.rotateZ","FKNeck_M.rotateZ","","FKNeck_M.rotateY","FKChest_M.rotateY","FKRoot_M.rotateZ","FKRoot_M.rotateY","FKHead_M.rotateZ","FKHead_M.rotateY","FKSpine2_M.rotateZ","FKSpine2_M.rotateY","RootX_M.translateX","RootX_M.rotateZ","RootX_M.rotateY","lowerLid2_R.rotateZ","lowerLid2_L.rotateZ","lowerLid2_R.rotateY","lowerLid2_L.rotateY","lowerLid2_R.translateX","lowerLid2_L.translateX","lowerLid1_R.rotateZ","lowerLid1_L.rotateZ","lowerLid1_R.rotateY","lowerLid1_L.rotateY","lowerLid1_R.translateX","lowerLid1_L.translateX","lowerLid3_R.rotateZ","lowerLid3_L.rotateZ","lowerLid3_R.rotateY","lowerLid3_L.rotateY","lowerLid3_R.translateX","lowerLid3_L.translateX","LidCorner2_R.rotateZ","LidCorner2_L.rotateZ","LidCorner2_R.rotateY","LidCorner2_L.rotateY","LidCorner2_R.translateX","LidCorner2_L.translateX","upperLid3_R.rotateZ","upperLid3_L.rotateZ","upperLid3_R.rotateY","upperLid3_L.rotateY","upperLid3_R.translateX","upperLid3_L.translateX","upperLid1_R.rotateZ","upperLid1_L.rotateZ","upperLid1_R.rotateY","upperLid1_L.rotateY","upperLid1_R.translateX","upperLid1_L.translateX","upperLid2_R.rotateZ","upperLid2_L.rotateZ","upperLid2_R.rotateY","upperLid2_L.rotateY","upperLid2_R.translateX","upperLid2_L.translateX","LidCorner1_R.rotateZ","LidCorner1_L.rotateZ","LidCorner1_R.rotateY","LidCorner1_L.rotateY","LidCorner1_R.translateX","LidCorner1_L.translateX","browOuter_R.rotateZ","browOuter_L.rotateZ","browOuter_R.rotateY","browOuter_L.rotateY","browOuter_R.translateX","browOuter_L.translateX","browHalf_R.rotateZ","browHalf_L.rotateZ","browHalf_R.rotateY","browHalf_L.rotateY","browHalf_R.translateX","browHalf_L.translateX","browInner_R.rotateZ","browInner_L.rotateZ","browInner_R.rotateY","browInner_L.rotateY","browInner_R.translateX","browInner_L.translateX","noseCorner_R.rotateZ","noseCorner_L.rotateZ","noseCorner_R.rotateY","noseCorner_L.rotateY","noseCorner_R.translateX","noseCorner_L.translateX","lowerLip3_R.rotateZ","lowerLip3_L.rotateZ","lowerLip3_R.rotateY","lowerLip3_L.rotateY","lowerLip3_R.translateX","lowerLip3_L.translateX","upperLip3_R.R_rotateZ","upperLip3_R.L_rotateZ","upperLip3_R.R_rotateY","upperLip3_R.L_rotateY","upperLip3_R.R_translateX","upperLip3_R.L_translateX","Lip6_R.rotateZ","Lip6_L.rotateZ","Lip6_R.rotateY","Lip6_L.rotateY","Lip6_R.translateX","Lip6_L.translateX","cheek_R.rotateZ","cheek_L.rotateZ","cheek_R.rotateY","cheek_L.rotateY","cheek_R.translateX","cheek_L.translateX","FKScapula_R.translateY","FKScapula_L.translateY","FKScapula_R.translateX","FKScapula_L.translateX","FKScapula_R.translateZ","FKScapula_L.translateZ","IKArm_L.rotateY","IKArm_L.rotateZ","IKArm_R.rotateY","IKArm_R.rotateZ","IKLeg_L.rotateY","IKLeg_L.rotateZ","IKLeg_R.rotateY","IKLeg_R.rotateZ","IKArm_L.translateX","IKArm_R.translateX","IKLeg_L.translateX","IKLeg_R.translateX","IKLeg_L.swivel_foo","IKLeg_R.swivel_foot","PoleLeg_L.translateX","PoleLeg_R.translateX","PoleArm_R.translateX","PoleArm_L.translateX","Eyectrl_R.rotateY","Eyectrl_L.rotateY","RollToes_R.rotateY","RollToes_L.rotateY","RollToes_R.rotateZ","RollToes_L.rotateZ","RollToesEnd_L.rotateY","RollToesEnd_R.rotateY","RollToesEnd_L.rotateZ","RollToesEnd_R.rotateZ","RollHeel_R.rotateY","RollHeel_L.rotateY","RollHeel_R.rotateZ","RollHeel_L.rotateZ"]
        selsplit = sel[0].split(":")
        spacename =  sel[0][0:(len(sel[0])-len(selsplit[-1]))]
        for i in range(len(selall)):
            cvshape = cmds.ls( selall[i],type="nurbsCurve")
            if cvshape!=[]:
                cvs = cmds.pickWalk(cvshape[0],d="up")
    #            print cvs[0][len(spacename):-1]
                adj =  cvs[0].split("_")[-1]
                if adj=="L":
                    lsel.append(cvs[0]) 
                    allsel.append(cvs[0]) 
                elif adj=="R":
                    rsel.append(cvs[0])
                    allsel.append(cvs[0])  
                elif adj =="M":
                    msel.append(cvs[0])
                    allsel.append(cvs[0]) 
    for a in range(len(allsel)):
        allattrlist =  cmds.listAttr(allsel[a],keyable=1,u=1)
        for t in range(len(allattrlist)):
            pbadj = cmds.listConnections( allsel[a]+"."+allattrlist[t],d=0,type="pairBlend")
            if pbadj!=None:
                pairblendnum.append(pbadj[0])
    if len(pairblendnum)==0:
        
        if len(lsel) == len(rsel):
            for l in range(len(lsel)):
                attrlist =  cmds.listAttr(lsel[l],keyable=1,u=1)
                ctrlname = lsel[l][0:(len(lsel[l])-1)]
                for a in range(len(attrlist)):
                    if attrlist[a] not in unvail:
                        lsrattradj = cmds.getAttr(ctrlname+"L"+"."+attrlist[a],lock=1)
                        lattr = ctrlname+"L"+"."+attrlist[a]
                        rsrattradj = cmds.getAttr(ctrlname+"R"+"."+attrlist[a],lock=1)
                        rattr = ctrlname+"R"+"."+attrlist[a]
                        if lsrattradj==False:                      
        #                        print lattr[len(spacename):]
                            lattrAC = cmds.listConnections(lattr,d=0,type="animCurve")
                            rattrAC = cmds.listConnections(rattr,d=0,type="animCurve")
                            if lattrAC!=None:
                                if rattrAC!=None:
                                    for c in range(len(lattrAC)):
                                        lattrACsin= cmds.listConnections(lattrAC[c],s=0,plugs=1)[0][len(spacename):]
                                        rattrACsin= cmds.listConnections(rattrAC[c],s=0,plugs=1)[0][len(spacename):]
                                        if cmds.isConnected(lattrAC[c]+".output",rattr)==False:
                                            cmds.connectAttr(lattrAC[c]+".output",rattr,f=1)
                                        if cmds.isConnected(rattrAC[c]+".output",lattr)==False:
                                            cmds.connectAttr(rattrAC[c]+".output",lattr,f=1) 
                                        if lattrACsin in spadj:
                                            indexnum =  cmds.keyframe( lattrAC[c], query=True, keyframeCount=True )
                                            for i in range(indexnum):
                                                indexvalue =  cmds.keyframe( lattrAC[0], query=True,index=(i,i),eval=1)
                                                newindexvalue = -float(indexvalue[0])
                                                cmds.keyframe(lattrAC[0],index=(i,i),absolute=1,valueChange=float(newindexvalue)) 
                                        if rattrACsin in spadj:
                                            rindexnum =  cmds.keyframe( rattrAC[c], query=True, keyframeCount=True )
                                            for r in range(rindexnum):
                                                rindexvalue =  cmds.keyframe( rattrAC[0], query=True,index=(r,r),eval=1)
                                                rnewindexvalue = -float(rindexvalue[0])
                                                cmds.keyframe(rattrAC[0],index=(r,r),absolute=1,valueChange=float(rnewindexvalue))   
                                else:
                                    errornum.append(rattrAC)
                                    cmds.setKeyframe(rattr)
                            else:
                                errornum.append(lattrAC)
                                cmds.setKeyframe(lattr)
    
        for m in range(len(msel)):
            attrlist =  cmds.listAttr(msel[m],keyable=1,u=1)
            for a in range(len(attrlist)):
                if attrlist[a] not in unvail:
                    mattradj = cmds.getAttr(msel[m]+"."+attrlist[a],lock=1)
                    mattr = msel[m]+"."+attrlist[a]
                    mattrAC = cmds.listConnections(mattr,d=0,type="animCurve")
                    if mattrAC!=None: 
                        for c in range(len(mattrAC)):
                            mattrACsin= cmds.listConnections(mattrAC[c],s=0,plugs=1)[0][len(spacename):]
                            if cmds.isConnected(mattrAC[c]+".output",mattr)==False:
                                cmds.connectAttr(mattrAC[c]+".output",mattr,f=1)
                            if mattrACsin in spadj:
                                mindexnum =  cmds.keyframe( mattrAC[c], query=True, keyframeCount=True )
                                for i in range(mindexnum):
                                    mindexvalue =  cmds.keyframe( mattrAC[0], query=True,index=(i,i),eval=1)
                                    mnewmindexvalue = -float(mindexvalue[0])
                                    cmds.keyframe(mattrAC[0],index=(i,i),absolute=1,valueChange=float(mnewmindexvalue)) 
        print "对称动画完成！",
    else:
        print "有约束属性，请烘焙该控制器的动画后解除约束，再进行操作！！",
def SJ_animateSybwdUI():
	if cmds.window('Anisymb',ex=True):
	    cmds.deleteUI('Anisymb',wnd=True)
	cmds.window('Anisymb',t='动画对称工具V1.0')
	cmds.columnLayout(adj=True)
	cmds.text(l='选择角色总控',fn='fixedWidthFont',h=50,ann="若有约束关系，在对称动画前 ，先烘焙动画及解除约束")
	cmds.button(l='对称动画',bgc=[1,0.5,0.5],c=anisymb,h=50,annotation="")
	cmds.showWindow()