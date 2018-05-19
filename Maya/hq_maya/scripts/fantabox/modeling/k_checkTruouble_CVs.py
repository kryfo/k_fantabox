# coding:utf-8
def k_checkTrouble_CVs():
    u'''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查模型CV点位移信息是否清零'}
    '''
    import maya.cmds as cc
    import re
    
    k_troubleCVmesh=[]
    k_lsmeshs=[]
    
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
                    
   
    else:
        k_lsmeshs=cc.ls(type='mesh',long=1)
        
       
    
    for k_lsmesh in k_lsmeshs:
        if cc.getAttr(k_lsmesh+'.intermediateObject')==0:
            k_polyCVs=[]
            try:
                k_polyCVs=cc.getAttr(k_lsmesh+'.pnts[*]')
            except:
                pass
            for k_polyCV in k_polyCVs:
                if not -0.00001<k_polyCV[0]<0.00001 or not -0.00001<k_polyCV[1]<0.00001 or not -0.00001<k_polyCV[2]<0.00001:
                    k_troubleCVmesh.append(k_lsmesh)
                    break
    
    
    
    k_troubleCVmeshs=set(k_troubleCVmesh)
    
    k_troubleCVmeshss=list(k_troubleCVmeshs)

               
    return k_troubleCVmeshss