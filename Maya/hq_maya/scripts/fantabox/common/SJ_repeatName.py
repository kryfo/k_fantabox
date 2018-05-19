#coding=cp936
#coding=utf-8
#重命名的名字：repeatName().keys()
#重命名名字的节点列表：repeatName().values()
import maya.cmds as cmds
def rpname():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'重命名名字的节点列表'}
    '''
    allnodedicts = dict([[a,a.split("|")[-1]] for a in cmds.ls(dag=True)])
    repeatname ={}
    if len(allnodedicts.values())!=len(list(set(allnodedicts.values()))):
        for  k in range(len(allnodedicts.keys())):
            if allnodedicts.values().count(allnodedicts.values()[k])>1:
                if allnodedicts.values()[k] not in set(repeatname.keys()):
                    repeatname[allnodedicts.values()[k]] =[allnodedicts.keys()[k]]
                else:
                    repeatname[allnodedicts.values()[k]].append(allnodedicts.keys()[k])
    return repeatname

def SJ_repeatName(checknum):
    validlists = range(2,11)+[-1]
    if checknum in validlists:
        return rpname().values()
    else:
        return []
