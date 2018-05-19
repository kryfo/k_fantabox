#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-06-08
from maya.cmds import commandPort
from maya.cmds import warning,ls,shadingNode,setAttr,hyperShade,select,promptDialog,listRelatives,listConnections,rename,commandPort,file,loadPlugin,pluginInfo
from maya.mel import eval as meleval
import  getpass
import subprocess
import os
import shutil
import time
import random
import json

def copyfile(sr,tr):
    if os.path.exists(os.path.dirname(tr))==False:
        os.mkdir(os.path.dirname(tr))
    shutil.copy(sr,tr)
def MayaSP_open():
    try:
        commandPort(name=':8080', sourceType='mel')
        
        print "port has successfully connected ",
    except:
        warning('port has already connected')
def MayaSP_close():
    try:
        commandPort(name=':8080', close=True)
        print "port:8080 has successfully disconnected ",
    except:
        warning('Could not close port 8080 (maybe it is not opened yet)')
def SJ_spPlugins():
    username =  getpass.getuser()
    spPath = "C:/Users/"+username+"/Documents/Allegorithmic/Substance Painter/plugins/hedgehog-connect"
    if os.path.exists("//10.99.1.13/hq_tool/Maya/substacePainter/hedgehog-connect")==True:
        srPath ="//10.99.1.13/hq_tool/Maya/substacePainter/hedgehog-connect"
    else:
        srPath ="O:/hq_tool/Maya/substacePainter/hedgehog-connect"
    if os.path.exists(spPath)==False:
        os.mkdir(spPath)
    srfilelist ={a.split(srPath)[-1]:a for a in walkDir_cmd(srPath,"file") if a!=""}
    trfilelist = {a.split(spPath)[-1]:a for a in walkDir_cmd(spPath,"file") if a!=""}
    #add
    addfilelists=  list(set(srfilelist)-set(trfilelist))
    for addfilelist in addfilelists:
        print "add::"+srfilelist[addfilelist],srfilelist[addfilelist].replace(srPath,spPath)
        copyfile(srfilelist[addfilelist],srfilelist[addfilelist].replace(srPath,spPath))
    #update
    compfilelists = list(set(srfilelist)&set(trfilelist))
    for comp in compfilelists:
        if getTime(os.stat(srfilelist[comp]))!=getTime(os.stat(trfilelist[comp])):
            print "update::"+srfilelist[comp],trfilelist[comp]
            copyfile(srfilelist[comp],trfilelist[comp])
    #del
    delfilelists = list(set(trfilelist)-set(srfilelist))
    for delfile in delfilelists:
        print "del::"+trfilelist[delfile]
        os.remove(trfilelist[delfile])
def getTime(state):
    return time.strftime('%y-%m-%d-%H:%M:%S',time.localtime(state.st_mtime))

def walkDir_cmd(dir,mod="file"):
    assert os.path.isdir(dir)
    if mod =="dir":
        cmd ='dir /s /b /ad "%s"'%(dir.replace("/","\\"))
    else:
        cmd ='dir /s /b /a-d "%s"'%(dir.replace("/","\\"))
    cmdout =subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (stdout,stderr)=cmdout.communicate()
    walkdirlist = stdout.replace("\r\n",",,").replace("\\","/").split(",,")
    return walkdirlist
def setID():
    sels = ls(sl=1)
    if sels!=[]:
        newshader = shadingNode("lambert",asShader=1)
        setAttr(newshader+".color",random.random(),random.random(),random.random(),type="double3")
        select(sels,r=1)
        hyperShade(a=newshader)
        meleval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    else:
        warning("please select A mesh!!")
def pathinput(chname,titlename):
    result = promptDialog(
            title=titlename,
            message=chname,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
    if result == 'OK':
        path = promptDialog(query=True, text=True)
        return  path
    else:
        return None
    
def meshinput(chname,titlename):
    
    result = promptDialog(
            title=titlename,
            message=chname,
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
    if result == 'OK':
        meshname = promptDialog(query=True, text=True)
        pathname = pathinput(u"输出路径：",titlename)
        return  meshname,pathname
    else:
        return None,None
    
def outputmesh():
    if pluginInfo("objExport",q=1,loaded=1,name=1)==0:
        try:
            loadPlugin("objExport")
        except:
            warning(u"obj插件加载不成功！！")
    meshname,pathname =  meshinput(u"模型名字：","Obj_Output")
    sels = [a for a in ls(sl=1) if listRelatives(a,c=1,type="mesh")!=None]
    if sels!=[]:
        if meshname!=None:
            if pathname!=None:
                for sel in sels:
                    meshshapes = listRelatives(sel,c=1,type="mesh")
                    if len(meshshapes)==1:
                        SG = listConnections(meshshapes[0],s=0,type="shadingEngine")
                        if SG!=None and len(SG)==1:
                            shader =  listConnections(SG[0]+".surfaceShader",d=0)
                            rename(shader[0],meshname+"_mat")
                            rename(SG[0],meshname+"_matSG")
                    else:
                        warning(u"有多个shape节点，请删除历史试试看？！")

                file(pathname.replace("\\","/")+"/"+meshname+".obj",force=1,options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1",typ="OBJexport",pr=1,es=1)
            else:
                warning(u"请输入输出模型路径！！")
        else:
            warning(u"请输入模型名字！！")
    else:
        warning(u"请选择输出模型！！")
def MayaSP_UI():
    ver = "2.0"

    path = "//10.99.1.13/hq_tool/Maya/substacePainter/hedgehog-connect/plugin.json"
    if os.path.exists(path)==False:
        path = "O:/hq_tool/Maya/substacePainter/hedgehog-connect/plugin.json"
    datas = json.loads(open(path).read(),encoding='gbk')
    if ver!=datas.get("version"):
        name = 'MayaSP'+ver+u"(最新版本为："+str(datas.get("version"))+")"
    else:
        name = 'MayaSP'+ver
    from maya.cmds import window
    from maya.cmds import deleteUI
    from maya.cmds import columnLayout
    from maya.cmds import button
    from maya.cmds import showWindow
    if window('MayaSP_UIwd',ex=True):
        deleteUI('MayaSP_UIwd',wnd=True)
    window('MayaSP_UIwd',t=name)
    columnLayout(adj=True,w=240)
    button(l='connect MayaSP', c= 'fb.com.MayaSP_open()',h=50,ann="")
    button(l='break MayaSP',c='fb.com.MayaSP_close()',h=50,ann="")
    button(l=u'设置随机材质ID',c='fb.com.setID()',h=50,ann="")
    button(l=u'输出obj到SP',c='fb.com.outputmesh()',h=50,ann="")
    button(l=u'配置同步SP插件',c='fb.com.SJ_spPlugins()',h=50,ann=datas.get("updateInfo"))
    showWindow()
if __name__=="__main__":
    MayaSP_UI()