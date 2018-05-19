#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-08-02
import maya.cmds as cmds 
def SJ_choicebreak():
    choicesels = cmds.ls(type="choice")
    for choicesel in choicesels:
        srattrs = cmds.listConnections(choicesel,s=0,type="file",plugs=1)
        if srattrs!=None:
            for srattr in srattrs:
                if srattr.split(".")[-1]=="fileTextureName":
                    srattrcons = cmds.listConnections(srattr,c=1,plugs=1)
                    try:
                        cmds.disconnectAttr(srattrcons[1],srattrcons[0])
                    except:
                        cmds.warning(srattrcons+"Connected error!!")
        else:
            tarsels = [a for a in cmds.listConnections(choicesel,s=0) if a!="defaultRenderUtilityList1"]
            if tarsels!=[]:
                for tarsel in tarsels:
                    tarattrcs= cmds.listConnections(tarsel,c=1,plugs=1,type="choice")
                    try:
                        cmds.disconnectAttr(tarattrcs[1],tarattrcs[0])
                    except:
                    	pass
        trattrs = cmds.listConnections(choicesel,d=0,type="file",plugs=1)
        if trattrs!=None:
            for trattr in trattrs:
                if trattr.find("Tex")!=-1:
                    trattrcons = cmds.listConnections(trattr,c=1,plugs=1)
                    try:
                        print trattrcons[0]+"xxxxxx"+trattrcons[1],
                        cmds.disconnectAttr(trattrcons[0],trattrcons[1])
                    except:
                       cmds.warning(trattrcons+"Connected error!!")
    alswsels =cmds.ls(type="alSwitchColor")
    Ennum = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]
    for alswsel in alswsels:
        awattr= cmds.listConnections(alswsel,c=1,type="aiWriteColor",plugs=1)
        mixnum =  int(cmds.getAttr(alswsel+".mix"))
        attrsr = cmds.listConnections(alswsel+".input"+str(Ennum[mixnum]),c=1,plugs=1)
        if awattr!=None and attrsr!=None:
            try:
                print attrsr[1]+"xxxxxx"+awattr[1],
                cmds.connectAttr(attrsr[1],awattr[1],f=1)
            except:
                cmds.warning(attrsr[1]+"connecting failed!!")
        else:
            pass
       
if __name__=='__main__':
    SJ_choicebreak()