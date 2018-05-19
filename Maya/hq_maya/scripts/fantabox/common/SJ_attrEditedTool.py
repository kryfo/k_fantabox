#coding=cp936
#coding=utf-8
__author__ = 'xusj'
import pymel.core as pm
def attrfun(arg):
    sels = pm.ls(sl=1)
    attrname =pm.textField('attnamefield',q=True,tx=True)
    attrvalue = pm.textField('attvaluefield',q=True,tx=True)
    for sel in sels:
        newattrname = sel+"."+attrname
        attrealname = [a for a in sel.listAttr() if a.upper() ==newattrname.upper()]
        if attrealname!=[]:
            attrtype = pm.attributeQuery(attrealname[0].split(".")[-1],node = pm.general.PyNode(attrealname[0].split(".")[0]),at=1)
            try:
                if attrtype =="float":
                    if len(attrvalue.split(","))==1:
                        pm.setAttr(attrealname[0],float(attrvalue))
                    else:
                        pm.setAttr(attrealname[0],float(attrvalue.split(",")[0]))
                elif attrtype =="float3":
                    if len(attrvalue.split(","))==3:
                        colorR,colorG,colorB =  attrvalue.split(",")
                        pm.setAttr(attrealname[0],float(colorR),float(colorG),float(colorB))
                elif attrtype =="typed":
                    if len(attrvalue.split(","))==1:
                        pm.setAttr(attrealname[0],str(attrvalue),type="string")
                    else:
                        pass
            except:
                pass
def SJ_attrEditedToolwdUI():          
	if pm.window('attrbatwd',ex=True):
	    pm.deleteUI('attrbatwd',wnd=True)
	pm.window('attrbatwd',t='attrEditedToolV1.0')
	pm.columnLayout(adj=True)
	pm.text(l='�����޸Ĳ�������V1.0',fn='fixedWidthFont',h=50,annotation="��ѡ��Ҫ�����޸ĵ�ģ�ͻ���ʵȽڵ㣬���������������Բ��������ȷ���޸�")
	pm.text(l='������',fn='fixedWidthFont',h=30,annotation="")
	pm.textField('attnamefield',tx="ambientcolor",h=30,ann="�ɲ����ִ�Сд")
	pm.text(l='���Բ���',fn='fixedWidthFont',h=30,annotation="")
	pm.textField('attvaluefield',tx="1",h=30,ann="������ʽ��0.5��1��0.5,0.5,0.3��D:\\filepath")
	pm.button(l='ȷ���޸�',c =attrfun,h=50)
	pm.showWindow()