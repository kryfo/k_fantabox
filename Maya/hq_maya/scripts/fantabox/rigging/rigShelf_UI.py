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
        self.title = '设置工具架'
        self.size = (546,350)
        self.supportsToolAction = False
    def creat(self):
        if cmds.window('optionWin',exists = 1):
            cmds.deleteUI('optionWin')
        self.window = cmds.window('optionWin',title = self.title,widthHeight = self.size, menuBar = True, resizeToFitChildren=True)
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        ################### 常用工具栏 ######################################
        child1 = cmds.frameLayout('frameLayout_1',label='属性工具架_A', borderStyle='in',cll =1,bgc=(0.5,0.2,0))
        cmds.rowColumnLayout('rowColumnLayout_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='Ctrl Color',w=125,h=50,c='mel.eval("CtrlColorWindow")')
        cmds.button(label='中心轴锁定隐藏',w=125,h=50,c='mel.eval("PivotWindow")')
        cmds.button(label='锁定并隐藏所有属性',w=125,h=50,c='mel.eval("poenclosewindow")')
        cmds.button(label='去除空间命名',w=125,h=50,c='mel.eval("removeNameSpace")')
        cmds.button(label='重命名工具',w=125,h=50,c="fb.rigging.common.rename.rename_window()")
        cmds.button(label='多物体属性属性关联',w=125,h=50,c='mel.eval("Attr_Link")')
        cmds.button(label='在已有骨骼中插入骨骼',w=125,h=50,c='mel.eval("add_joint_tool")')
        cmds.button(label='Blend反算工具',w=125,h=50,c='fb.rigging.common.correctiveShapeCmd.correctiveShapeCmd()')
        cmds.button(label='驱动关键帧镜像工具',w=125,h=50,c="aa=fb.rigging.common.mirrorDrivenKey.MirrorDrivenKey()\naa.show()")
        cmds.setParent( tabs )
        ################### 设置创建栏 ######################################
        tab2=cmds.columnLayout(adj=True)
        child2 = cmds.frameLayout('frameLayout_2',label='控制器工具架_A', borderStyle='in',cll =1,bgc=(0.2,0.2,0.6) )
        cmds.rowColumnLayout('rowColumnLayout_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='创建控制器',w=125,h=50,c='mel.eval("Controller")')
        cmds.button(label='道具总控创建',w=125,h=50,c="fb.rigging.create.Pro_Ctrl.wicket()")
        cmds.button(label='添加自动化表达式',w=125,h=50,c='mel.eval("addExpression")')
        cmds.button(label='软选创建控制器',w=125,h=50,c="fb.rigging.create.softCreateCtrl.softSelCtrl()")
        cmds.button(label='创建线性IK（拉伸）工具',w=125,h=50,c="fb.rigging.create.IkCurStretch.LsyIkCurStretchWin()")
        cmds.setParent( '..' )
        child2_1 = cmds.frameLayout('frameLayout_2_1',label='骨骼创建工具架_B', borderStyle='in',cll =1,bgc=(0.2,0.2,0.6) )
        cmds.rowColumnLayout('rowColumnLayout_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='添加等距骨骼',w=125,h=50,c='mel.eval("wp_jointsOnCurves")')
        cmds.button(label='创建控制骨骼跟随曲线',w=125,h=50,c='mel.eval("C_ctrlOnCurve")')
        cmds.button(label='创建骨骼跟随曲线',w=125,h=50,c='mel.eval("C_jointOnCurve")')
        cmds.button(label='曲线创建物体',w=125,h=50,c='mel.eval("createOBJonCurve")')
        cmds.setParent( tabs )
        ################### 修改编辑栏 ######################################
        tab3=cmds.columnLayout(adj=True)
        child3 = cmds.frameLayout('frameLayout_3',label='权重工具架_A', borderStyle='in',cll =1,bgc=(0.3,0.4,0) )
        cmds.rowColumnLayout('rowColumnLayout_3',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='拷贝权重工具',w=125,h=50,c='mel.eval("CopySkinWeightJoints")')
        cmds.button(label='模型替换权重工具',w=125,h=50,c="bb = fb.rigging.edit.MatchingMesh.MatchingModel()\nbb.show()")
        cmds.button(label='选择蒙皮骨骼',w=125,h=50,c='mel.eval("selectSkinJoints")')
        cmds.button(label='骨骼链缩放关联',w=125,h=50,c='mel.eval("JointInverseScaleTool")')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child3_1 = cmds.frameLayout('frameLayout_3_1',label='次级工具架_B', borderStyle='in',cll =1,bgc=(0.3,0.4,0) )
        cmds.rowColumnLayout('rowColumnLayout_3_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='次级控制',w=125,h=50,c='mel.eval("Jnt_sec_tool_CN_modify")')
        cmds.button(label='簇工具',w=125,h=50,c='mel.eval("clusterTool")')
        cmds.button(label='Poly点添加毛囊',w=125,h=50,c='mel.eval("YY_HUV")')
        cmds.button(label='模型上加柳钉（选点）',w=125,h=50,c="fb.rigging.edit.polyAttach.shuai_polyAttach()")
        cmds.button(label='铆钉工具（选择两根线）',w=125,h=50,c='mel.eval("YY_rivet")')
        cmds.button(label='修形工具',w=125,h=50,c="creat=fb.rigging.edit.dslSculptInbetweenEditor.SculptInbetweenEditor()\ncreat.ui()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( tabs )
        ################### 角色相关栏 ######################################
        tab4=cmds.columnLayout(adj=True)
        child4 = cmds.frameLayout('frameLayout_4',label='角色工具架_A', borderStyle='in',cll =1,bgc=(0.1,0.2,0.4))
        cmds.rowColumnLayout('rowColumnLayout_4',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='Smooth控制器添加',w=125,h=50,c="fb.rigging.character.smooth_connectAttr.smooth_UI()")
        cmds.button(label='毛发关联（hair/yeti）',w=125,h=50,c="hairs=fb.rigging.character.allHairConnect.AllHairConnect()\nhairs.show()")
        cmds.button(label='adv表情设置新增控制器',w=125,h=50,c="fb.rigging.character.advFaceCtrlAdd.windows()")
        cmds.button(label='裙子设置Adv',w=125,h=50,c='mel.eval("dressRig_adv")')
        cmds.button(label = '添加辅助骨骼',w = 125,h = 50,c="fb.rigging.character.AddOptionJointTool.optionUIClass()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child4_1 = cmds.frameLayout('frameLayout_4_1',label = '模型类工具架_B', borderStyle='in',cll =1,bgc=(0.1,0.2,0.4))
        cmds.rowColumnLayout('rowColumnLayout_4_1',nc = 4,cat = [(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='ArnoldID修改工具',w = 125,h = 50,c = "fb.mod.SJ_charcleanuptoolwdUI()")
        cmds.button(label='角色变体贴图切换工具',w = 125,h = 50,c = "fb.rigging.character.texChangeTool.AnamorphosisLinkUI()")
        cmds.button(label='SJ设置工具集',w=125,h=50,c = "fb.rigging.character.SJ_RiggingTool.HDD()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( tabs )
        tab6 = cmds.columnLayout(adj=True)
        ################### 其他相关栏 ######################################
        child6 = cmds.frameLayout('frameLayout_6',label='骨骼对位工具架_A', borderStyle='in',cll =1,bgc=(0.1,0.2,0.2) )
        cmds.rowColumnLayout('rowColumnLayout_6',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='动捕forMB骨骼对位',w=125,h=50,c='mel.eval("MocapCharacter_jnt_adv")')
        cmds.button(label='群集Miarmy骨骼对位',w=125,h=50,c='mel.eval("qunji_jnt_adv")')
        cmds.button(label='获取关键帧范围',w=125,h=50,c='mel.eval("listFrameRange")')
        cmds.button(label='动捕转换工具（tsm）',w=125,h=50,c='mel.eval("motionCaptureConvertTool")')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child6_1 = cmds.frameLayout('frameLayout_6_1',label='肌肉工具架_B', borderStyle='in',cll =1,bgc=(0.1,0.2,0.2) )
        cmds.rowColumnLayout('rowColumnLayout_6_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='OpenMayaMuscle2015',w=125,h=50,c='mel.eval("New_OpenMayaMuscle2015")')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child6_2 = cmds.frameLayout('frameLayout_6_2',label='翅膀系统_C', borderStyle='in',cll =1,bgc=(0.1,0.2,0.2))
        cmds.rowColumnLayout('rowColumnLayout_6_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='群集Miarmy骨骼对位',w=125,h=50,c="fb.rigging.other.PlumeUI.run()")
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        ################### ADV5.42版本 ######################################
        tab7= cmds.columnLayout('advLayout',adj=True)
        child7_1 = cmds.frameLayout('frameLayout_7_1',label='Face 工具架', borderStyle='in',cll =1,bgc=(0.5,0,0.5))
        cmds.rowColumnLayout('rowColumnLayout_7_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='FacialRig工具',w=125,h=50,c="fb.rigging.FacialRig.autoFacialRig.shuai_autoFacialRig()")
        cmds.button(label='表情融合工具',w=125,h=50,c="import edward.showUi;reload(edward.showUi)")
        cmds.button(label='表情镜像工具',w=125,h=50,c='mel.eval("abSymMesh")')
        cmds.button(label = '反算（脸部减法）工具',w = 125,h = 50,c = 'fb.rig.FacialRig.shuai_polyMeshCalculator()' )
        cmds.setParent('..')
        cmds.setParent('..')
        child7_2 = cmds.frameLayout('frameLayout_7_2',label='Adv/5.42版工具架', borderStyle='in',cll =1,bgc=(0.5,0,0.5))
        cmds.rowColumnLayout('rowColumnLayout_7_2',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='ADV5.42版本',w=125,h=50,c='mel.eval("source \\"//10.99.1.6/Digital/Library/rigging_Library/fantabox/Adv/Adv5.42/AdvancedSkeleton5.mel\\";AdvancedSkeleton5;")')
        cmds.button(label='身体＋表情优化工具',w=125,h=50,c='mel.eval("zf_advxz")')
        cmds.setParent('..')
        cmds.setParent('..')
        ################### ADV5.00版本 ######################################
        child7_3 = cmds.frameLayout('frameLayout_7_3',label='Adv/5.00版工具架', borderStyle='in',cll =1,bgc=(0.5,0,0.5))
        cmds.rowColumnLayout('rowColumnLayout_7_3',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='ADV5.00版本',w=125,h=50,c='mel.eval("source \\"//10.99.1.6/Digital/Library/rigging_Library/fantabox/Adv/Adv5.00/AdvancedSkeleton5/AdvancedSkeleton5.mel\\";AdvancedSkeleton5;")')
        cmds.button(label='身体优化',w=125,h=50,c='bo=fb.rig.FacialRig.bodyOptimize()\nbo.setupUI()')
        cmds.button(label='表情优化',w=125,h=50,c='fo=fb.rig.FacialRig.faceOptimize()\nfo.setupUI()')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        ################### 动画修型 ######################################
        tab8= cmds.columnLayout('fixAnimShape',adj=True)
        child8 = cmds.frameLayout('frameLayout8',label='动画修型工具架_A', borderStyle='in',cll =1,bgc=(0.5,0.4,0.9))
        cmds.rowColumnLayout('rowColumnLayout8',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='动画修型',w=125,h=50,c='bo=fb.rig.animFixShape.shuai_animFixShapeTool()')
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        child8_1 = cmds.frameLayout('frameLayout_8_1',label='设置检查工具_B', borderStyle='in',cll =1,bgc=(0.5,0.4,0.9) )
        cmds.rowColumnLayout('rowColumnLayout_8_1',nc=4,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])
        cmds.button(label='设置检查工具',w=125,h=50,c='fb.rigging.check.stateRiggingCheck.stateRiggingCheck()')
        cmds.tabLayout( tabs, edit=True,tabLabel=((child1, '常用工具栏'), (tab2, '设置创建栏'),(tab3, '修改编辑栏'),(tab4, '角色相关栏'),(tab6, '其他相关栏'),(tab7,'FacialRig / Adv '),(tab8,'动画修型/检查工具')))
        #cmds.rowColumnLayout('rowColumnLayout_8_1',nc=3,cat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)],rat=[(1,'both',10),(2,'both',10),(3,'both',10),(4,'both',10)])

        cmds.showWindow()

#def main():
if __name__=='__main__':
                 
    a = AR_optionwindow()
    a.creat()