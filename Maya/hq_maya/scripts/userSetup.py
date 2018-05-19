#coding=utf-8
import time
start =time.time()
from maya.utils import executeDeferred
from maya.cmds import pluginInfo,loadPlugin,warning,evalDeferred,unloadPlugin
import fantabox as fb
from fantabox.FantaBoxMenu import *
import  maya.mel as mel
from subprocess import Popen, PIPE


def documentsLocation():    
    handle = Popen('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"  /v personal', shell=True, stdout=PIPE)
    hostid = handle.communicate()[0]
    handle.kill
    return hostid.split( 'REG_SZ')[1].strip()

from maya.OpenMaya import MGlobal  as _MGlobal
mayaver = str(_MGlobal.apiVersion())[0:4]

def pluginload():
    if pluginInfo("mtoa",q=1,loaded=1,name=1)==0:
        try:
            loadPlugin("mtoa")
        except:
            warning("no arnold����")
    if pluginInfo("pgYetiMaya",q=1,loaded=1,name=1)==0:
        try:
            loadPlugin("pgYetiMaya")
        except:
            warning("no pgYetiMaya")

    if pluginInfo('MelDecryptor',q=1,loaded=1,name=1)==0:
        try:
            loadPlugin("MelDecryptor")
            mel.eval("simpleCam()")
            mel.eval("simpleStereoCam()")
            mel.eval("sphereScreenStereoCam()")
            mel.eval("radianScreenStereoCam()")
        except:
            warning("no MelDecryptor")





def mtoasetting():
    hostname = documentsLocation()
    arnoldpath = []
    modulespath= hostname+"\maya\modules"
    modulefile = open(modulespath+ r"\foma_plugins.mod", 'r')
    modulelines = modulefile.readlines()
    modulefile.close()
    for moduleline in modulelines:
        if moduleline.find("+ MAYAVERSION:2015 mtoa")!=-1:
            try:
                Arnoldname = moduleline[moduleline.find("Arnold_"):][:-10]
                if Arnoldname.find("O:/hq_tool/Maya/Arnold/")!=-1:
                    arnoldpath.append("O:/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
                elif Arnoldname.find("C:/hq_tool/Maya/Arnold/")!=-1:
                    arnoldpath.append("C:/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
                elif Arnoldname.find("//10.99.1.13/digital/film_project/hq_tool/Maya/Arnold/")!=-1:
                    arnoldpath.append("//10.99.1.13/digital/film_project/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
                elif Arnoldname.find("//XMFTDYPROJECT/digital/film_project/hq_tool/Maya/Arnold/")!=-1:
                    arnoldpath.append("//XMFTDYPROJECT/digital/film_project/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
            except:
                warning("arnold��Ⱦ��������ʧ�ܣ���")

executeDeferred(pluginload)
executeDeferred(mtoasetting)

executeDeferred( FantaBoxMenu().main )




##��������
if mayaver !="2017":
    try:
        evalDeferred('''mel.eval('source "//10.99.1.13/hq_tool/Maya/hq_maya/scripts/fantabox/toolBox.mel";')''' )
        #evalDeferred('''mel.eval('source "//10.99.1.12/�����Ӱ/�����ļ�/08����/������������/������������_����ɾ��/All_mel/UN/UN_Menu.mel";')''' )
        #evalDeferred('''mel.eval('source "//10.99.1.12/�����Ӱ/�����ļ�/08����/������������/������������_����ɾ��/All_mel/address.mel";' )''' )
    except:
        evalDeferred('''mel.eval('source "//XMFTDYPROJECT/digital/film_project/hq_tool/Maya/hq_maya/scripts/fantabox/toolBox.mel";')''' )
        pass

##��managerTool�����Զ�����
try:
    cmd = 'tasklist ' 
    cmdout = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    ToolManagersw=[]
    for line in cmdout.stdout.readlines():
        if line.find('ToolManager')!=-1:
            ToolManagersw.append(line) 
    if ToolManagersw==[]:
        try:
            cmdstart = 'start O:\\hq_tool\\programs\\ToolManager\\ToolManager.exe'
            toolmg = Popen(cmdstart,shell=True,stdout=PIPE,stderr=PIPE)
        except:
            print "ToolManager.exe cant be started!! "
except:
    print "subprocess not work!! "
starttime =time.time()-start
print "����ʱ��Ϊ��"+str(starttime)

pyhostname = documentsLocation().split("\\")[-2]
autopath = "C:/Users/"+pyhostname+"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/famo_configure_autorun.exe"
if os.path.exists(autopath)==True:
    try:
        delfilecmd = 'del /s "%s" '%(autopath.replace("/","\\"))
        Popen(delfilecmd,shell=True)
    except:
        warning("�����Զ����ػ�ľ����ʧ�ܣ��������û�Ȩ��")




#�������Ĳ����Ϣ
#������ര��
'''
try:
    evalDeferred('from fantabox.common import k_check_unPlugin;k_check_unPlugin()')
    evalDeferred("from fantabox.common import deleteNoneUI;deleteNoneUI()")
except:
    pass
'''