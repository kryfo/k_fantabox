import sys
import getpass
from pymel.core import versions
hostname =getpass.getuser()
arnoldpath = []
modulespath= "C:/Users/"+hostname+"/Documents/maya/modules"
modulefile = open(modulespath+ r"\foma_plugins.mod", 'r')
modulelines = modulefile.readlines()
modulefile.close()
for moduleline in modulelines:
    if moduleline.find("+ MAYAVERSION:"+str(versions.current())[:4]+" mtoa")!=-1:
        try:
            Arnoldname = moduleline[moduleline.find("Arnold_"):][:-10]
        except:
            Arnoldname=[]
        if Arnoldname!=[]:
            arnoldpath.append(r"O:/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
if arnoldpath[0] not in sys.path:
    sys.path.append(arnoldpath[0])
sys.path.append(r"\\10.99.1.13\hq_tool\Maya\hq_maya\scripts")
import fantabox as fb
import maya.standalone
maya.standalone.initialize(name="python")
from pymel.core import pluginInfo,loadPlugin
import maya.cmds as cmds
if pluginInfo("pgYetiMaya",q=1,loaded=1,name=1)==0:
    try:
        loadPlugin("pgYetiMaya")
    except:
        print "failed to load pgYetiMaya",
if pluginInfo("mtoa",q=1,loaded=1,name=1)==0:
    try:
        loadPlugin("mtoa")
    except:
        print "failed to load mtoa",
#excefile("//10.99.1.13/hq_tool/Maya/hq_maya/scripts/initialmaya.py")
#cmds.file(r"D:/testZone/0906/maya2015/scenes/test.mb",f=1,ignoreVersion=1,o=1)
