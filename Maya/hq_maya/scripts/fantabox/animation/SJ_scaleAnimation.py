#coding=cp936
#coding=utf-8
import pymel.core as pm
def getattr(arg):
	sel = pm.ls(sl=1)
	aniattrcom =[]
	if sel !=[]:
		for i in range(len(sel)):
			selAC = pm.listConnections(sel[i],d=0,type="animCurve")
			if selAC !=[]:
				selattr = pm.listConnections(sel[i],d=0,plugs=1,type="animCurve")
				for a in range(len(selattr)):
					aniattr =  pm.listConnections(selattr[a],s=0,plugs=1)[0]
					aniattrcom.append(aniattr)
					pm.textScrollList("keyattr",e=1,ra=1,a=aniattrcom)
def scaleani(arg):
	selACs = pm.textScrollList("keyattr",q=1,si=1) 
	start = pm.textField('startnum',q=True,tx=True)
	end =pm.textField('endnum',q=True,tx=True)
	sel = pm.ls(sl=1)
	if sel !=[]:
		for i in range(len(sel)):
			selAC = pm.listConnections(sel[i],d=0,type="animCurve")
			if selAC !=[]:
				selattr = pm.listConnections(sel[i],d=0,plugs=1,type="animCurve")
				for a in range(len(selattr)):
					aniattr =  pm.listConnections(selattr[a],s=0,plugs=1)
					if aniattr!=[]:
						if aniattr[0] in selACs:
							attrname =  str(aniattr[0])[(len(aniattr[0].split(".")[0])+1):]
							pm.scaleKey(iub=False,newStartTime=start,newEndTime=end,attribute=attrname)
						
def anisplits(arg):
	sel = pm.ls(sl=1)
	for i in range(len(sel)):
		selAC = pm.listConnections(sel[i],d=0,type="animCurve")
		if selAC!=[]:
			for a in range(len(selAC)):
				indexnum =  pm.keyframe( selAC[a], query=True, keyframeCount=True )
				for n in range(indexnum):
					frame =  pm.keyframe( selAC[a], query=True,index=(n,n),timeChange=1)[0]
					if int(str(frame).split(".")[-1]) !=0:
						intframe = "%d" %frame
						pm.setKeyframe(selAC[a],t=intframe)
						pm.cutKey(selAC[a],t=frame)

def SJ_scaleAnimationwdUI():
	if pm.window('scaleani',ex=True):
	    pm.deleteUI('scaleani',wnd=True)
	pm.window('scaleani',t='ScaleAnimationToolV1.0')
	pm.columnLayout(adj=True)
	pm.text(l='缩放动画工具V1.0 ',fn='fixedWidthFont',h=50,w=10)
	pm.flowLayout( columnSpacing=0)
	pm.text(l='起始帧 ',fn='fixedWidthFont',h=30,w=130)
	pm.text(l='结束帧 ',fn='fixedWidthFont',h=30,w=130)
	pm.setParent( '..' )
	pm.flowLayout( columnSpacing=0)
	pm.textField('startnum',tx=u"1",w=130,h=30,ann="")
	pm.textField('endnum',tx=u"100",w=130,h=30,ann="")
	pm.setParent( '..' )
	pm.button(l='获取key帧属性',c=getattr,bgc=[0.4,0.6,0.5],w=160,h=50)
	pm.textScrollList("keyattr",allowMultiSelection=1)
	pm.button(l='缩放动画',c=scaleani,bgc=[0.4,0.6,0.5],w=160,h=50)
	pm.button(l='去除小数点帧数',c=anisplits,bgc=[0.4,0.6,0.5],w=160,h=50)
	pm.showWindow()