#coding:utf-8
def k001_check_hairlinkarnold():
    from maya.cmds import pluginInfo,ls,connectionInfo,listConnections
    k_return=[]
    k_lsshaveHair=[]
    k_lshairSystem=[]
    k_lsshaveHair=[a for a in ls(type='hairSystem') if a.find("rig_")==-1 and listConnections(a,type='pfxHair')]
    if pluginInfo('shaveNode',q=1,loaded=1):
        k_lsshaveHair+= ls(type='shaveHair')
    else:
        pass
    for k_shave in k_lsshaveHair:
        k_attrn=[]
        try:
            k_attrn= connectionInfo((k_shave+".aiHairShader"),id=1)       
        except:
            pass
        if k_attrn:
            k_listai= listConnections(k_shave+".aiHairShader",d=1)
            if k_listai :pass
            else :k_return.append(k_shave)
        else:k_return.append(k_shave)
        
    return k_return
def noAishaderhair():
    from maya.cmds import select,warning
    noAishaderhairsels = k001_check_hairlinkarnold()
    select(noAishaderhairsels,r=1)
    warning(u"已选中"+str(len(noAishaderhairsels))+u"个没有链接Arnold材质的毛发节点！！")

        
if __name__=='__main__':
    k001_check_hairlinkarnold()