#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
import re
def multinode(arg):
    num = pm.textField('multinum',q=True,tx=True)
    sels =pm.ls(sl=1,type="file")
    for sel in sels:
        choiceNodes =   pm.listConnections(sel,d=0,type="choice")
        udimNumsample=set(range(1001,1900))
        path  =pm.getAttr(sel+".fileTextureName")
        filepath = set([int(u) for u in re.findall("\d+",str(path))])
        udimjudge=list(filepath&udimNumsample)
        types = path.split(".")[-1]
        if udimjudge==[] and path.find("<UDIM>")==-1 :
            if choiceNodes==[]:
                choicesel = pm.shadingNode("choice",asUtility=1,name = sel[0])
                pm.connectAttr(choicesel+".output",sel+".fileTextureName",f=1)
                for n in range(int(num)):
                    pm.addAttr(sel,ln="Tex"+str(n),dt="string")
                    pm.connectAttr(sel+".Tex"+str(n),choicesel.input[n],f=1)
                    if n==0:
                        pm.setAttr(sel+".Tex"+str(n),path,type="string")
                    else:
                        pm.setAttr(sel+".Tex"+str(n),path[:-4]+"_"+str(n+1)+"."+types,type="string")
            else:
                Texlists = [a for a in pm.listAttr(sel) if a.find('Tex')!=-1 and len(a)<=5]
                texnum = len(Texlists)
                for n in range(int(num)):
                    pm.addAttr(sel,ln="Tex"+str(n+texnum),dt="string")
                    pm.connectAttr(sel+".Tex"+str(n+texnum),choiceNodes[0]+".input["+str(n+texnum)+"]",f=1)
                    pm.setAttr(sel+".Tex"+str(n+texnum),path[:-4]+"_"+str(n+1+texnum)+"."+types,type="string")
        else:
            if udimjudge!=[]:
                udimpath= path[:-4].replace(str(udimjudge[-1]),"<UDIM>")
            else:
                udimpath =  path[:-4]
            if choiceNodes==[]:
                choicesel = pm.shadingNode("choice",asUtility=1,name = sel[0])
                pm.connectAttr(choicesel+".output",sel+".fileTextureName",f=1)
                for n in range(int(num)):
                    pm.addAttr(sel,ln="Tex"+str(n),dt="string")
                    pm.connectAttr(sel+".Tex"+str(n),choicesel.input[n],f=1)
                    if n==0:
                        pm.setAttr(sel+".Tex"+str(n),udimpath+"."+types,type="string")
                    else:
                        pm.setAttr(sel+".Tex"+str(n),udimpath[:-7]+"_"+str(n+1)+udimpath[-7:]+"."+types,type="string")
            else:
                Texlists = [a for a in pm.listAttr(sel) if a.find('Tex')!=-1 and len(a)<=5]
                texnum = len(Texlists)
                for n in range(int(num)):
                    pm.addAttr(sel,ln="Tex"+str(n+texnum),dt="string")
                    pm.connectAttr(sel+".Tex"+str(n+texnum),choiceNodes[0]+".input["+str(n+texnum)+"]",f=1)
                    pm.setAttr(sel+".Tex"+str(n+texnum),udimpath[:-7]+"_"+str(n+1+texnum)+udimpath[-7:]+"."+types,type="string")
def chconnect(arg):
    sel =pm.ls(sl=1)
    for i in range(1,len(sel)):
        pm.connectAttr(sel[0]+".selector",sel[i]+".selector",f=1)
def displaychoice(arg):
    sel =pm.ls(sl=1)
    hsv = pm.shadingNode("remapHsv",asUtility=1,name =sel[0] )
    pm.removeMultiInstance(hsv+".hue[1]",b=1)
    pm.setAttr(hsv+".color",1,0,0,type= "double3")
    pm.setAttr(hsv+".hue[0].hue_FloatValue",0.1)
    pm.connectAttr(hsv+".outColor",sel[0]+".hardwareColor",f=1)
def SJ_MultiTexwdUI():
    if pm.window('multitex',ex=True):
        pm.deleteUI('multitex',wnd=True)
    pm.window('multitex',t='MultiTexToolV1.1')
    '''
    1.1更新说明增加对udim贴图的支持
    '''
    pm.columnLayout(adj=True)
    pm.text(l='',fn='fixedWidthFont',h=30,annotation="")
    pm.text(l='贴图路径数量',fn='fixedWidthFont',h=30,annotation="")
    pm.textField('multinum',tx="",h=30,ann="输入文件夹路径",w=50)
    pm.button(l='生成多贴图链接',c=multinode,h=50,ann = "选择需要生产多贴图链接的file节点，输入贴图路径的数量，点击确定生成")
    pm.button(l='链接节点关联',c=chconnect,h=50,ann="先选择主体choice节点，再选择被关联节点")
    pm.button(l='创建区分显示颜色节点',c=displaychoice,h=50,ann="选择主体choice节点的材质节点")
    pm.showWindow()