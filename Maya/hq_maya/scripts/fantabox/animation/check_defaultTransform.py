#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:libin,xusijian
#--date--:2017-09-28
def check_defaultTransform():
    from maya.cmds import ls,listRelatives,getAttr,listConnections
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查位移旋转缩放是否初始化'}
    '''
    lights = listRelatives(ls(lt=1),p=1)
    fols =  listRelatives(ls(type="follicle"),p=1)
    folcvs = [listRelatives(a,p=1)[0] for a in ls(type="nurbsCurve") if listConnections(a,s=0,type="follicle")!=None]
    sels = set(ls(type="transform"))-set(listRelatives(ls(ca=1),p=1))
    if lights!=None:
        sels= sels-set(lights)
    if fols!=None:
        sels= sels-set(fols)
    if folcvs !=None:
        sels= sels-set(folcvs)
    sels = list(sels)
    vails = ["tx","ty","tz","rx","ry","rz"]
    novails = ["sx","sy","sz"]
    attNoright = []
    for sel in sels:
        for vail in vails:
            attr = getAttr(sel+"."+vail)
            if attr!=0:
                attNoright.append(sel+"."+vail)
        for novail in novails:
            attr =getAttr(sel+"."+novail)
            if attr!=1:
                attNoright.append(sel+"."+novail)
    attNoright= list(set([a.split(".")[0] for a in attNoright]))
    return attNoright

if __name__=='__main__':
    adj = check_defaultTransform()
    if adj!=[]:
        print  "位移旋转缩放未初始化"
    else:
        print  "位移旋转缩放已初始化"
