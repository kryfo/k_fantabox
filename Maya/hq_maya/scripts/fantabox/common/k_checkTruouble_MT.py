# coding:utf-8

def k_checkTrouble_MT():
    u'''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查模型以及组属性是否冻结'}
    '''
    import maya.cmds as cc
    import re
    k_lsmeshs=[]
    k_lstranforms=[]
    
    k_lsalltfs=cc.ls(type='transform',long=1)
    
    k_matchgeo=[]
    
    for k_lsalltf in k_lsalltfs:
        try:
            k_match=re.search('_all.*\|.*_geo$',k_lsalltf)
            k_havematch=k_match.group()
            k_matchgeo.append(k_lsalltf)
        except:
            pass
    
    if k_matchgeo: 
            
        for k_matchgeo in k_matchgeo:
            k_listallchilds=cc.listRelatives(k_matchgeo,fullPath=1,ad=1)
            if k_listallchilds:
                for k_listallchild in k_listallchilds:
                    if cc.nodeType(k_listallchild)=='mesh':
                        k_lsmeshs.append(k_listallchild)
                    if cc.nodeType(k_listallchild)=='transform':
                        k_lstranforms.append(k_listallchild)
    
    
    else:                 
        k_lsmeshs=cc.ls(long=1,type='mesh')
        k_lstranforms=cc.ls(long=1,type='transform')
    
    k_meshs=[]
    
    for k_lsmesh in k_lsmeshs:
        k_mesh=cc.listRelatives(k_lsmesh,fullPath=1,allParents=1)
        k_meshs=k_meshs+k_mesh

    k_tranforms=[]
    
    for k_lstranform in k_lstranforms:
        if cc.nodeType(k_lstranform)=='transform':
            k_tranform=cc.listRelatives(k_lstranform,fullPath=1,s=1)
            if k_tranform:
                pass
            else:
                k_tranforms.append(k_lstranform)
        
    k_check_MTs=k_meshs+k_tranforms
    
    k_trouble_MTs=[]
    
    for k_check_MT in k_check_MTs:
        k_MTtx=cc.getAttr(k_check_MT+'.tx')
        k_MTty=cc.getAttr(k_check_MT+'.ty')
        k_MTtz=cc.getAttr(k_check_MT+'.tz')
        k_MTrx=cc.getAttr(k_check_MT+'.rx')
        k_MTry=cc.getAttr(k_check_MT+'.ry')
        k_MTrz=cc.getAttr(k_check_MT+'.rz')
        k_MTsx=cc.getAttr(k_check_MT+'.sx')
        k_MTsy=cc.getAttr(k_check_MT+'.sy')
        k_MTsz=cc.getAttr(k_check_MT+'.sz')
                
        if k_MTtx==0. and k_MTty==0. and k_MTtz==0. and k_MTrx==0. and k_MTry==0. and k_MTrz==0. and k_MTsx==1. and k_MTsy==1. and k_MTsz==1.: 
            pass
        else :
            k_trouble_MTs.append(k_check_MT)
            
    k_trouble_MTs=set(k_trouble_MTs)
    
    k_trouble_MTss=list(k_trouble_MTs)

    return k_trouble_MTss
