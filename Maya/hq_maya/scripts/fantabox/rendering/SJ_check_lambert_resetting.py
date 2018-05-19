#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-06-23
import pymel.core as pm
class lambert_defaultSet():
    def __init__(self):
        self.noDefault={}
        self.displaymentCons = []
        self.specialAttr = ['outMatteOpacityR','outMatteOpacityG','outMatteOpacityB']
    def check_lambertAttr(self):
        lamallattrs=pm.listAttr("lambert1")
        for lamallattr in lamallattrs:
            try:
                ck_attrCons = pm.listConnections("lambert1."+lamallattr,d=0,plugs=1)
                if ck_attrCons ==[]:
                    localAttr =  pm.getAttr("lambert1."+lamallattr)
                    typejudge =type(localAttr)
                    defaultAttr = pm.attributeQuery(lamallattr,node ="lambert1",listDefault=1)
                    if str(typejudge).split("'")[1]=='tuple':
                        defaultAttrs = tuple(defaultAttr)
                    else:
                        defaultAttrs =  defaultAttr[0]
                    if localAttr!=defaultAttrs:
                        if lamallattr!='outMatteOpacity' and lamallattr not in self.specialAttr:
                            self.noDefault[lamallattr]=str(typejudge).split("'")[1]
                        elif lamallattr=='outMatteOpacity':
                            if localAttr!=(1.0, 1.0, 1.0):
                                self.noDefault[lamallattr]=str(typejudge).split("'")[1]
                        elif lamallattr in self.specialAttr:
                             if localAttr!=1.0:
                                 self.noDefault[lamallattr]=str(typejudge).split("'")[1]
                    else:
                        pass
                else:
                    self.noDefault[lamallattr]=None
            except:
                pass
        return self.noDefault
    def reset_lambertAttr(self):
        noDefaultattrs=lambert_defaultSet().check_lambertAttr()
        for noDefaultattr in noDefaultattrs:
            typejudge=  noDefaultattrs[noDefaultattr]
            attrCons = pm.listConnections("lambert1."+noDefaultattr,d=0,plugs=1)
            defaultAttr = pm.attributeQuery(noDefaultattr,node ="lambert1",listDefault=1)
            if attrCons!=[]:
                pm.disconnectAttr(attrCons[0],"lambert1."+noDefaultattr)
            if typejudge =='tuple':
                if noDefaultattr!="outMatteOpacity":
                    pm.setAttr("lambert1."+noDefaultattr,tuple(defaultAttr),type='double3')
                else:
                    pm.setAttr("lambert1.outMatteOpacity",(1.0, 1.0, 1.0),type='double3')
            else:
                if noDefaultattr not in self.specialAttr:
                    pm.setAttr("lambert1."+noDefaultattr,defaultAttr[0])
                else:
                    pm.setAttr("lambert1."+noDefaultattr,1.0)
            print "已重置了默认lambert的"+str(noDefaultattr)+"属性",

    def check_lambertDisplayment(self):
        SGdispAttrA = pm.listConnections('initialParticleSE.displacementShader',d=0,plugs=1)
        SGdispAttrB =pm.listConnections('initialShadingGroup.displacementShader',d=0,plugs=1)
        if SGdispAttrA:
            self.displaymentCons.append( [SGdispAttrA[0],'initialParticleSE.displacementShader'])
        if SGdispAttrB:
            self.displaymentCons.append([SGdispAttrB[0],'initialShadingGroup.displacementShader'])
        return self.displaymentCons
        
    def reset_lambertDisplayment(self):
        displaymentCons= lambert_defaultSet().check_lambertDisplayment()
        if displaymentCons!=[]:
            for displaymentCon in displaymentCons:
                pm.disconnectAttr(displaymentCon[0],displaymentCon[1])
                print "已断开了默认lambert的置换贴图",
def SJ_check_lambert_resetting():
    '''
    检查lambert属性
    '''
    lambert_defaultSet().check_lambertAttr()
    lambert_defaultSet().check_lambertDisplayment()
    return  lambert_defaultSet().check_lambertAttr().keys()
    
def SJ_doIt_lambert_resetting():
    '''
    重置lambert属性
    '''
    try:
        lambert_defaultSet().reset_lambertAttr()
        lambert_defaultSet().reset_lambertDisplayment()
        return "done!!"
    except:
        pm.warning('something Wrong in resetting!!')
if __name__ =="__main__":
    SJ_check_lambert_resetting()
    SJ_doIt_lambert_resetting()
    