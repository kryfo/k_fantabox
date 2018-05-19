#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
import maya.mel as mel
def uvsettool(arg):
	#拷贝uvset到默认uvset
	sel =pm.ls(sl=1)
	for i in range(len(sel)):
		cruv =  pm.getAttr(sel[i].getShapes()[0]+".currentUVSet")
		if cruv!="map1":
			alluvset=pm.polyUVSet(sel[i],q=1,allUVSets=1)
			pm.polyUVSet(sel[i],copy=True,uvSet=cruv,nuv="map1")
		else:
			alluvset=pm.polyUVSet(sel[i],q=1,allUVSets=1)
			if len(alluvset)>=1:
				uvrightset = [u for u in alluvset if u=="UVChannel_1"]
				if uvrightset!=[]:
					pm.setAttr(sel[i].getShapes()[0]+".currentUVSet",uvrightset[0],type="string")
					cruv =  pm.getAttr(sel[i].getShapes()[0]+".currentUVSet")
					pm.polyUVSet(sel[i],copy=True,uvSet=cruv,nuv="map1")
	for i in range(len(sel)):
		pm.select(sel[i],r=1)
		alluvset=pm.polyUVSet(sel[i],q=1,allUVSets=1)
		print sel[i],alluvset
		for n in range(len(alluvset)):
			if len( alluvset)!=1:
				if alluvset[n]!="map1":
					pm.setAttr(sel[i].getShapes()[0]+".currentUVSet",alluvset[n],type="string")
					try:
						pm.polyUVSet(delete=True)
					except:
						pass
def SJ_uvsetToolwdUI():					
	if pm.window('uvsetreset',ex=True):
	    pm.deleteUI('uvsetreset',wnd=True)
	pm.window('uvsetreset',t='uvset重置工具V1.0')
	pm.columnLayout(adj=True)
	pm.text(l="uvset重置工具V1.0",h=50,ann="选择需要转uvset的模型，输入正确uvset名字，点击确定")
	pm.textField('uvsetcmm',tx="UVChannel_1",h=30)
	pm.button(l='确定转换',c=uvsettool,h=50,w=10)
	pm.showWindow()
