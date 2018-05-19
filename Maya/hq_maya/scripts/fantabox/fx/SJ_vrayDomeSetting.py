#coding:utf-8
import pymel.core as  pm
import maya.mel as mel
def vrayDomeSetting(vrfol):
    defaultcam =[u'frontShape', u'perspShape', u'sideShape', u'topShape']
    camshapes =[c for c in pm.ls(type="camera") if c not in defaultcam]
    for camshape in camshapes:
        camshape.setAttr("focalLength",l = False)
        camname = None
        camshapenode =camshape
        while pm.general.PyNode(camshapenode).getParent()!=None:
            
            if camname==None:
                camname = str(camshapenode.getParent())+"|"+str(camshapenode)
            else:
                camname =camshapenode.getParent()+"|"+ camname
            camshapenode = camshapenode.getParent()
        try:
            camshape.getAttr("vrayCameraDomeOn")
            mel.eval('vray addAttributesFromGroup |%s vray_cameraDome %s;'%(str(camname),0))
            mel.eval('vray addAttributesFromGroup |%s vray_cameraDome %s;'%(str(camname),1))
            camshape.setAttr("vrayCameraDomeOn",1)
            camshape.setAttr("vrayCameraDomeFov",vrfol)
            print "球幕相机已更新设置，fov设置值为"+str(vrfol),
        except:
            print "非Vray球幕相机！！",