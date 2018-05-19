# -*- coding:gbk -*-
import maya.cmds as cmds
import maya.mel as mel
import mtoa
import json
import os
from functools import partial

class FantaBoxMenu():
    def __init__(self):
        
        self.projectPath = r"O:/hq_tool/Maya/hq_maya/scripts/fantabox"
        self.rigpath = "O:/hq_tool/Maya/hq_maya/scripts/fantabox/rigging"
        
        ##ͨ��
        self.commenus = (
        {"arnold����ת������":'fb.com.SJ_convertArnoldShaders()'},
        {"��������":'mel.eval("playblastTool")' },
        {"ƴ������":'fb.com.camViewJointScriptUI()' },
        {"�ο�����":'mel.eval("editRefPathBat")'},
        {"������":'mel.eval("proxyTool")'},
        {},
        {"�����������Ϣ": 'fb.com.k_check_unPlugin()'},
        {"�����������": 'fb.com.SJ_repeatNameToolUI()'},
        {"�������ýڵ㹤��": 'fb.com.SJ_cleanUpTool()'},
        {"�������ò㹤��": 'fb.com.SJ_cleanLayerTool()'},
        {"�޸�ģ�Ͳ��ʹ���": 'fb.com.SJ_fixedShadermodToolUI()'},
        {},
        {"Maya�������תMax": 'fb.com.k_mayaMax_camTransfer()'},
        {},
        {"ɫ�������ɹ���": 'fb.com.k_tintplate()'},
        {},
        {"ȥ�ռ���������": 'mel.eval("removeNameSpace")'},
        {"�ڵ�������������":'mel.eval("unlockNodeTool")'},
        {"���ѡȡ���幤��":'mel.eval("ramdonsel")' },
        {"�����޸Ĳ�������":'fb.com.SJ_attrEditedToolwdUI()'},
        {"·����������ģ�͹���":'mel.eval("dulpathgeoTool")'  },
        {"ģ�Ͷ��㹤��":'fb.com.shuai_polyAttach()'},
        {"������Ӱ��ƽ�湤��":'mel.eval("loadcameraplanelTool")'},
        {"����·��ת���·��":'mel.eval("absolutepathbat")' },
        {},
        {"��������·������":'fb.com.SJ_pathbatTool()'},
        {"��������Ⱦ����":'mel.eval("batrenderTool")' },
        {},
        {"MayaSublime�����л�":'fb.com.MayaSublime_UI()'},
        {"MayaSP�����л�":'fb.com.MayaSP_UI()'},
        )
        # ģ��
        self.modmenus = (
        {"SJ��ɫ���߼�":'fb.mod.SJ_charToolwdUI()'},
        {},
        {"��ɫģ�Ϳ�":'fb.mod.Char_ModelLibWin()'},
        {"����ģ�Ϳ�":'fb.mod.YY_ModelLibWin()'},
        {},
        {"uv����":'fb.mod.UVToolwdUI()'},
        {"��ͼ����":'fb.mod.SJ_texToolswdUI()'},
        {"���ʹ���":'fb.mod.comshderwdUI()'},
        {"�ƹ�ͨ��������":'mel.eval("lightechbox")'},
        {},
        {"�ڷ����嵽�湤��":'mel.eval("putonface")' },
        {"���������������":'mel.eval("snaponface")'},
        {},
        {"�����������":'mel.eval("measuredistance")'},
        {"ѡ���������幤��":'mel.eval("selhidden")'},
        {"Ŀ��Ⱥ��Լ������":'mel.eval("objconstrain")' },
        {},
        {"���������ˢ����":'mel.eval("crobjbrush")'},
        {"ʯͷ���ɹ���":'mel.eval("stonemaker")'},
        {"������и��":'mel.eval("tjh_cut_tool")'}
        )
        
        # ����
        self.animenus = (
        {"IKFK�޷��л���Adv��":'mel.eval("shuaiAdvIkFkSwitch")'},
        {"�߿�ģʽ�л������ԣ�":'fb.ani.SJ_animateDisplaywdUI()'},
        {"��ʾ��ɫ����":'fb.ani.SJ_hardwareDisplaySwitcherwdUI()'},
        {},
        {"�������ù������":'mel.eval("AnimateusefulTool")'},
        {"�����ۺϹ���":'mel.eval("AnimateeCom")'},
        {},
        {"Arnold��occ���ʸ��蹤��":'mel.eval("Arnoldocc")' },
        {"�������綪ʧ�޸�����":'mel.eval("fixmissingshader")'},
        {"ѡ����������ʵ�ģ��":'mel.eval("faceToShader")'},
        {},
        {"�����Գƹ���(adv)":'fb.ani.SJ_animateSybwdUI()'},
        {"��֡FKIK��ת(adv)":'mel.eval("IKFKAnimSwitchWin")'},
        {"���Ŷ������߹���":'fb.ani.SJ_scaleAnimationwdUI()'},
        {"�ɱ༭�����켣":'mel.eval("editableMotionTrail")'},
        {"�Ż��������߹���":'mel.eval("opAnimateCurve")'},
        {},
        {"ѡ���ӹ�������":'mel.eval("seljoint")'},
        {"��׽��ӿ���������":'mel.eval("mopctrlTool")' },
        {},
        {"����·����鹤��":'mel.eval("cacheFileCheckWindow")'},
        {"yeti������ë���������������":'fb.ani.SJ_yetiCachewdUI()'},
        {"�Ͽ�����ڵ�":'fb.ren.SJ_choicebreak()'},
        {"abc��ë������֡�����湤�߼�":'fb.ani.SJ_abcFurCache_ToolwdUI()'},
		{"rjAnchorTransform��������":'fb.ani.rjAnchorTransform.ui.show()'}
        )
        
        # ��Ч
        
        self.fxmenus = (
        {"vfx_maya":'w00_window_QSTools(ICONDIRS)' },
        {"��Ч����������":'mel.eval("fxrenametool")' },
        {"��Чabcģ�͹淶���":'fb.fx.fx_prefixNameUI()' },
        {"������̹���":'fb.fx.camerapipwdUI()'},
        {"����ģ�����й���":r'mel.eval("geoAnimateseq")' },
        {"ת�������������":'mel.eval("nParticlesTranslater")' },
        {"��������決����":'fb.fx.bakeInstancer.ui.show()' },
        {"��Ч��Ⱦ���ù���":'mel.eval("TX_RenderSettingUI")' }
        )
        # ��װ
        self.renmenus = (
        {"����Ĭ��lambert����":'fb.ren.lambert_defaultSet().reset_lambertAttr();fb.ren.lambert_defaultSet().reset_lambertDisplayment()'},
        {"Arnold��Yeti��Ⱦ����Ż�":'fb.ren.SJ_resetAiYetiRender()'},
        {"����������":'mel.eval("GYF_winUI")'},
        {"Arnoldǰ̨��Ⱦ":"import mtoa.cmds.arnoldRender;mtoa.cmds.arnoldRender.arnoldBatchRender('')"},
        {},
        {"�Զ����ù���Ŀ¼":'mel.eval("autosetproj")'},
        {},
        {"��������л�":'fb.ren.SJ_randomChoice()'},
        {"ë����Ӱ����":'fb.ren.SJ_furDisplaySwitchwdUI()'}
        )

        # ���
        self.cammenus = (
        {"�����":'fb.cam.simpleCam().windowOfCamCreat()'},
        {"�������":'fb.cam.simpleStereoCam().windowOfCamCreat()'},
        {"��Ļ���":'fb.cam.radianScreenStereoCam().windowOfCamCreat()'},
        {"��Ļ���":'fb.cam.sphereScreenStereoCam().windowOfCamCreat()'},
        {"�����(��)":'fb.cam.simpleCamMeter().windowOfCamCreat()'},
        {"�������(��)":'fb.cam.simpleStereoCamMeter().windowOfCamCreat()'},
        {"��Ļ���(��)":'fb.cam.radianScreenStereoCamMeter().windowOfCamCreat()'},
        {"��Ļ���(��)":'fb.cam.sphereScreenStereoCamMeter().windowOfCamCreat()'},
        )

    #���ýű�Ŀ¼�Զ���
    def automenu(self, famenu, autopath, menunamedict, maindict, subdict):
        rigdirs = maindict[autopath]
        for r in range(len(rigdirs)):
            if rigdirs[r] != None:
                paths = autopath + "/" + rigdirs[r]
                try:
                    cmds.menuItem(str(rigdirs[r]), label=str(r + 1) + "." + menunamedict[rigdirs[r]], p=famenu, to=1,
                                  sm=1)
                except:
                    cmds.menuItem(str(rigdirs[r]), label=str(r + 1) + "." + rigdirs[r], p=famenu, to=1, sm=1)
                cmds.setParent("..", menu=True)
                submenufile = subdict[paths]
                for u in range(len(submenufile)):
                    scriptpath = paths + "/" + submenufile[u]
                    submenuname = os.path.splitext(submenufile[u])[0]
                    if os.path.splitext(scriptpath)[-1] == ".mel":
                        melname = r'''mel.eval('source "%s"')''' % (scriptpath)
                        try:
                            cmds.menuItem(label=str(u + 1) + "." + menunamedict[submenuname], p=str(rigdirs[r]), to=1,
                                          c=melname)
                        except:
                            cmds.menuItem(label=str(u + 1) + "." + str(submenuname), p=str(rigdirs[r]), to=1, c=melname)
                    else:
                        pyname = r'execfile("%s")' % (scriptpath)
                        try:
                            cmds.menuItem(label=str(u + 1) + "." + menunamedict[submenuname], p=str(rigdirs[r]), to=1,
                                          c=pyname)
                        except:
                            cmds.menuItem(label=str(u + 1) + "." + str(submenuname), p=str(rigdirs[r]), to=1, c=pyname)
    #�Ӳ˵�Ŀ¼��
    def menubuild(self,menuchild,menufather):
        modmenuChild = self.modmenus
        mc=0
        for m in range(len(menuchild)):
            if menuchild[m]!={}:
                if menuchild[m].values()[0]!=None:
                    cmds.menuItem(l=str(m+1-mc)+"."+menuchild[m].keys()[0], to=1, p=menufather, c=menuchild[m].values()[0])
                else:
                    mc = mc+1
                    
            else:
                mc = mc+1
                cmds.menuItem(d=1, p=menufather)
    #���˵�Ŀ¼
    def main(self, *args):
        #global gMainWindow
        #gMainWindow = mel.eval('global string $gMainWindow;global string $tempMelVar;$tempMelVar=$gMainWindow')
        gMainWindow = mel.eval('$tempMelVar=$gMainWindow')
        if cmds.menu("fantaboxwd", q=1, ex=1):
            cmds.deleteUI("fantaboxwd")
        cmds.menu("fantaboxwd", p=gMainWindow, to=1, label=r"FantaBox")
        commonmn = cmds.menuItem(label='ͨ��', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        modelmn = cmds.menuItem(label='ģ��', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        rigmn = cmds.menuItem(label='����',c = "fb.rig.AR_optionwindow().creat()")
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        animatmn = cmds.menuItem(label='����', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        fxmn = cmds.menuItem(label='��Ч', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        rendermn = cmds.menuItem(label='��װ', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        cammn = cmds.menuItem(label='���', to=1, sm=1)
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        checkmn = cmds.menuItem(label='�ύ�淶��鹤��',c='fb.loadcheckNode()' )
        cmds.setParent("..", menu=True)
        cmds.menuItem(d=1)
        #refreshmn = cmds.menuItem(label='ˢ��',c='import FantaBoxMenu;reload(fb.FantaBoxMenu);fb.FantaBoxMenu.FantaBoxMenu().main()' )

        cmds.setParent("..", menu=True)

        ##ͨ�������:
        self.menubuild(self.commenus,commonmn)
           
        ##ģ������壺
        self.menubuild(self.modmenus,modelmn)
        '''
        ##��������壺
        rigFile = open(u'%s/rigpath.json'%(self.rigpath), 'r').read()
        rigData = json.loads(rigFile)
        self.automenu(rigmn, self.rigpath, rigData["name"], rigData["path"][0], rigData["path"][1])
        '''
        ##��������壺
        self.menubuild(self.animenus,animatmn)
            
        ##��Ч����壺
        self.menubuild(self.fxmenus,fxmn)

        ##��װ����壺
        self.menubuild(self.renmenus,rendermn)

        ##�������壺
        self.menubuild(self.cammenus,cammn)