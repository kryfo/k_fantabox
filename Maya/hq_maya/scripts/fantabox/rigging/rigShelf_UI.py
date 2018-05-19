#!/usr/bin/env python
#coding=cp936
#coding=utf-8
#--author-- : yujing
#--date-- : 2017.7.19
#--update-- : 2018.1.12/2018.1.24
####### ---- "rigShelf_UI" ---- ############# 
import maya.cmds as cmds
import maya.mel as mel
import fantabox as fb
class AR_optionwindow (object):
    @classmethod
    def showUI(cls):
        win = cls()
        win.create()
        return win
    def __init__ (self):
        self.window = 'ar_optionwindow '
        self.title = '���ù��߼�'
        self.size = (546,350)
        self.supportsToolAction = False
    def creat(self):
        if cmds.window('optionWin',exists = 1):
            cmds.deleteUI('optionWin')
        self.window = cmds.window('optionWin',title = self.title,widthHeight = self.size, menuBar = True, resizeToFitChildren=True)
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        ################### ���ù����� ######################################
        child1 = cmds.frameLayout('frameLayout_1',label='���Թ��߼�_A', borderStyle='in',cll =1,bgc=(0.5,0.2,0))
        cmds.rowColumnLayout('rowColumnLayout_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='Ctrl Color',w=125,h=50,c='mel.eval("CtrlColorWindow")')
        cmds.button(label='��������������',w=125,h=50,c='mel.eval("PivotWindow")')
        cmds.button(label='������������������',w=125,h=50,c='mel.eval("poenclosewindow")')
        cmds.button(label='ȥ���ռ�����',w=125,h=50,c='mel.eval("removeNameSpace")')
        cmds.button(label='����������',w=125,h=50,c="fb.rigging.common.rename.rename_window()")
        cmds.button(label='�������������Թ���',w=125,h=50,c='mel.eval("Attr_Link")')
        cmds.button(label='�����й����в������',w=125,h=50,c='mel.eval("add_joint_tool")')
        cmds.button(label='Blend���㹤��',w=125,h=50,c='fb.rigging.common.correctiveShapeCmd.correctiveShapeCmd()')
        cmds.button(label='�����ؼ�֡���񹤾�',w=125,h=50,c="aa=fb.rigging.common.mirrorDrivenKey.MirrorDrivenKey()\naa.show()")
        cmds.setParent( tabs )
        ################### ���ô����� ######################################
        tab2=cmds.columnLayout(adj=True)
        child2 = cmds.frameLayout('frameLayout_2',label='���������߼�_A', borderStyle='in',cll =1,bgc=(0.2,0.2,0.6) )
        cmds.rowColumnLayout('rowColumnLayout_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='����������',w=125,h=50,c='mel.eval("Controller")')
        cmds.button(label='�����ܿش���',w=125,h=50,c="fb.rigging.create.Pro_Ctrl.wicket()")
        cmds.button(label='����Զ������ʽ',w=125,h=50,c='mel.eval("addExpression")')
        cmds.button(label='��ѡ����������',w=125,h=50,c="fb.rigging.create.softCreateCtrl.softSelCtrl()")
        cmds.button(label='��������IK�����죩����',w=125,h=50,c="fb.rigging.create.IkCurStretch.LsyIkCurStretchWin()")
        cmds.setParent( '..' )
        child2_1 = cmds.frameLayout('frameLayout_2_1',label='�����������߼�_B', borderStyle='in',cll =1,bgc=(0.2,0.2,0.6) )
        cmds.rowColumnLayout('rowColumnLayout_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='��ӵȾ����',w=125,h=50,c='mel.eval("wp_jointsOnCurves")')
        cmds.button(label='�������ƹ�����������',w=125,h=50,c='mel.eval("C_ctrlOnCurve")')
        cmds.button(label='����������������',w=125,h=50,c='mel.eval("C_jointOnCurve")')
        cmds.button(label='���ߴ�������',w=125,h=50,c='mel.eval("createOBJonCurve")')
        cmds.setParent( tabs )
        ################### �޸ı༭�� ######################################
        tab3=cmds.columnLayout(adj=True)
        child3 = cmds.frameLayout('frameLayout_3',label='Ȩ�ع��߼�_A', borderStyle='in',cll =1,bgc=(0.3,0.4,0) )
        cmds.rowColumnLayout('rowColumnLayout_3',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='����Ȩ�ع���',w=125,h=50,c='mel.eval("CopySkinWeightJoints")')
        cmds.button(label='ģ���滻Ȩ�ع���',w=125,h=50,c="bb = fb.rigging.edit.MatchingMesh.MatchingModel()\nbb.show()")
        cmds.button(label='ѡ����Ƥ����',w=125,h=50,c='mel.eval("selectSkinJoints")')
        cmds.button(label='���������Ź���',w=125,h=50,c='mel.eval("JointInverseScaleTool")')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child3_1 = cmds.frameLayout('frameLayout_3_1',label='�μ����߼�_B', borderStyle='in',cll =1,bgc=(0.3,0.4,0) )
        cmds.rowColumnLayout('rowColumnLayout_3_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='�μ�����',w=125,h=50,c='mel.eval("Jnt_sec_tool_CN_modify")')
        cmds.button(label='�ع���',w=125,h=50,c='mel.eval("clusterTool")')
        cmds.button(label='Poly�����ë��',w=125,h=50,c='mel.eval("YY_HUV")')
        cmds.button(label='ģ���ϼ�������ѡ�㣩',w=125,h=50,c="fb.rigging.edit.polyAttach.shuai_polyAttach()")
        cmds.button(label='í�����ߣ�ѡ�������ߣ�',w=125,h=50,c='mel.eval("YY_rivet")')
        cmds.button(label='���ι���',w=125,h=50,c="creat=fb.rigging.edit.dslSculptInbetweenEditor.SculptInbetweenEditor()\ncreat.ui()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( tabs )
        ################### ��ɫ����� ######################################
        tab4=cmds.columnLayout(adj=True)
        child4 = cmds.frameLayout('frameLayout_4',label='��ɫ���߼�_A', borderStyle='in',cll =1,bgc=(0.1,0.2,0.4))
        cmds.rowColumnLayout('rowColumnLayout_4',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='Smooth���������',w=125,h=50,c="fb.rigging.character.smooth_connectAttr.smooth_UI()")
        cmds.button(label='ë��������hair/yeti��',w=125,h=50,c="hairs=fb.rigging.character.allHairConnect.AllHairConnect()\nhairs.show()")
        cmds.button(label='adv������������������',w=125,h=50,c="fb.rigging.character.advFaceCtrlAdd.windows()")
        cmds.button(label='ȹ������Adv',w=125,h=50,c='mel.eval("dressRig_adv")')
        cmds.button(label = '��Ӹ�������',w = 125,h = 50,c="fb.rigging.character.AddOptionJointTool.optionUIClass()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child4_1 = cmds.frameLayout('frameLayout_4_1',label = 'ģ���๤�߼�_B', borderStyle='in',cll =1,bgc=(0.1,0.2,0.4))
        cmds.rowColumnLayout('rowColumnLayout_4_1',nc = 4,cat = [(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='ArnoldID�޸Ĺ���',w = 125,h = 50,c = "fb.mod.SJ_charcleanuptoolwdUI()")
        cmds.button(label='��ɫ������ͼ�л�����',w = 125,h = 50,c = "fb.rigging.character.texChangeTool.AnamorphosisLinkUI()")
        cmds.button(label='SJ���ù��߼�',w=125,h=50,c = "fb.rigging.character.SJ_RiggingTool.HDD()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( tabs )
        tab6 = cmds.columnLayout(adj=True)
        ################### ��������� ######################################
        child6 = cmds.frameLayout('frameLayout_6',label='������λ���߼�_A', borderStyle='in',cll =1,bgc=(0.1,0.2,0.2) )
        cmds.rowColumnLayout('rowColumnLayout_6',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='����forMB������λ',w=125,h=50,c='mel.eval("MocapCharacter_jnt_adv")')
        cmds.button(label='Ⱥ��Miarmy������λ',w=125,h=50,c='mel.eval("qunji_jnt_adv")')
        cmds.button(label='��ȡ�ؼ�֡��Χ',w=125,h=50,c='mel.eval("listFrameRange")')
        cmds.button(label='����ת�����ߣ�tsm��',w=125,h=50,c='mel.eval("motionCaptureConvertTool")')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child6_1 = cmds.frameLayout('frameLayout_6_1',label='���⹤�߼�_B', borderStyle='in',cll =1,bgc=(0.1,0.2,0.2) )
        cmds.rowColumnLayout('rowColumnLayout_6_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='OpenMayaMuscle2015',w=125,h=50,c='mel.eval("New_OpenMayaMuscle2015")')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child6_2 = cmds.frameLayout('frameLayout_6_2',label='���ϵͳ_C', borderStyle='in',cll =1,bgc=(0.1,0.2,0.2))
        cmds.rowColumnLayout('rowColumnLayout_6_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='Ⱥ��Miarmy������λ',w=125,h=50,c="fb.rigging.other.PlumeUI.run()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        ################### ADV5.42�汾 ######################################
        tab7= cmds.columnLayout('advLayout',adj=True)
        child7_1 = cmds.frameLayout('frameLayout_7_1',label='Face ���߼�', borderStyle='in',cll =1,bgc=(0.5,0,0.5))
        cmds.rowColumnLayout('rowColumnLayout_7_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='FacialRig����',w=125,h=50,c="fb.rigging.FacialRig.autoFacialRig.shuai_autoFacialRig()")
        cmds.button(label='�����ںϹ���',w=125,h=50,c="import edward.showUi;reload(edward.showUi)")
        cmds.button(label='���龵�񹤾�',w=125,h=50,c='mel.eval("abSymMesh")')
        cmds.button(label = '���㣨��������������',w = 125,h = 50,c = 'fb.rig.FacialRig.shuai_polyMeshCalculator()' )
        cmds.setParent('..')
        cmds.setParent('..')
        child7_2 = cmds.frameLayout('frameLayout_7_2',label='Adv/5.42�湤�߼�', borderStyle='in',cll =1,bgc=(0.5,0,0.5))
        cmds.rowColumnLayout('rowColumnLayout_7_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='ADV5.42�汾',w=125,h=50,c='mel.eval("source \\"//10.99.1.6/Digital/Library/rigging_Library/fantabox/Adv/Adv5.42/AdvancedSkeleton5.mel\\";AdvancedSkeleton5;")')
        cmds.button(label='���士�����Ż�����',w=125,h=50,c='mel.eval("zf_advxz")')
        cmds.setParent('..')
        cmds.setParent('..')
        ################### ADV5.00�汾 ######################################
        child7_3 = cmds.frameLayout('frameLayout_7_3',label='Adv/5.00�湤�߼�', borderStyle='in',cll =1,bgc=(0.5,0,0.5))
        cmds.rowColumnLayout('rowColumnLayout_7_3',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='ADV5.00�汾',w=125,h=50,c='mel.eval("source \\"//10.99.1.6/Digital/Library/rigging_Library/fantabox/Adv/Adv5.00/AdvancedSkeleton5/AdvancedSkeleton5.mel\\";AdvancedSkeleton5;")')
        cmds.button(label='�����Ż�',w=125,h=50,c='bo=fb.rig.FacialRig.bodyOptimize()\nbo.setupUI()')
        cmds.button(label='�����Ż�',w=125,h=50,c='fo=fb.rig.FacialRig.faceOptimize()\nfo.setupUI()')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        ################### �������� ######################################
        tab8= cmds.columnLayout('fixAnimShape',adj=True)
        child8 = cmds.frameLayout('frameLayout8',label='�������͹��߼�_A', borderStyle='in',cll =1,bgc=(0.5,0.4,0.9))
        cmds.rowColumnLayout('rowColumnLayout8',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='��������',w=125,h=50,c='bo=fb.rig.animFixShape.shuai_animFixShapeTool()')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child8_1 = cmds.frameLayout('frameLayout_8_1',label='���ü�鹤��_B', borderStyle='in',cll =1,bgc=(0.5,0.4,0.9) )
        cmds.rowColumnLayout('rowColumnLayout_8_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='���ü�鹤��',w=125,h=50,c='fb.rigging.check.stateRiggingCheck.stateRiggingCheck()')
        cmds.tabLayout( tabs, edit=True,tabLabel=((child1, '���ù�����'), (tab2, '���ô�����'),(tab3, '�޸ı༭��'),(tab4, '��ɫ�����'),(tab6, '���������'),(tab7,'FacialRig / Adv '),(tab8,'��������/��鹤��')))
        #cmds.rowColumnLayout('rowColumnLayout_8_1',nc=3,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])

        cmds.showWindow()

#def main():
if __name__=='__main__':
                 
    a = AR_optionwindow()
    a.creat()