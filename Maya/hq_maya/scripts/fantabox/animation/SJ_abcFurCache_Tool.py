#coding=cp936
#coding=utf-8
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import os
import fantabox
import mtoa
import shutil
class abctool ():
    def __init__(self):
        self.geodict = {}
        self.matcol  =pm.ls(mat =1)
        self.srmesh =[]
    def splitRealname(self,selected):
        if selected!=[]:
            if len(selected.split(":"))!=1:
                return selected.split(":")[-1]
            else:
                return []
        else:
            return []
    def adjExistDict(self,dictlist,dict_mesh,dict_shader,callback):
        if dict_mesh not in dictlist.keys():
            dictlist[dict_mesh]=dict_shader
            return callback
            #return dictlist
        else:
            pass
        
    def builddict(self,selit):
        if selit!=[]:
            srgeoalls =[a for a in pm.listRelatives(selit,ad=1) if pm.nodeType(a)=="transform"]
            for srgeoall in srgeoalls:
                if srgeoall.getShape()!= None:
                    sgs=list(set([gs for gs in  pm.listConnections(srgeoall.getShape(),s=0,type="shadingEngine") if gs!=[]]))
                    for sg in sgs:
                        if pm.listConnections(sg+".aiSurfaceShader",d=0)!=[]:
                            srshader  = pm.listConnections(sg+".aiSurfaceShader",d=0)[0]
                        else:    
                            srshader  = pm.listConnections(sg+".surfaceShader",d=0)[0]
                        if srshader in self.matcol:
                            pm.hyperShade(o=srshader) 
                            sel_lists =[os for os in cmds.ls(sl=1, allPaths=1) if str(srgeoall.getShape()) in str(os) or str(srgeoall) in str(os)]
                            for sel_list in sel_lists:
                                if '.f[' in sel_list:
                                    abctool().adjExistDict(self.geodict,sel_list,srshader,'f mode')
                                else:
                                    abctool().adjExistDict(self.geodict,sel_list,srshader,'g mode')      
                        else:
                            SGorginalcons = list(pm.listConnections(srshader,c=1,type="shadingEngine",plugs=1))
                            for SGorginalcon in SGorginalcons:
                                tmpshader = pm.shadingNode('lambert',asShader =1)
                                pm.connectAttr(str(tmpshader)+".outColor",SGorginalcon[1],f=1)
                                pm.hyperShade(o=tmpshader)
                                sel_lists =[os for os in cmds.ls(sl=1, allPaths=1) if str(srgeoall.getShape()) in str(os) or str(srgeoall) in str(os)]
                                pm.connectAttr(str(SGorginalcon[0]),SGorginalcon[1],f=1)
                                pm.delete(tmpshader)
                                for sel_list in sel_lists:
                                    if '.f[' in sel_list:
                                        abctool().adjExistDict(self.geodict,sel_list,srshader,'f mode')
                                    else:
                                        abctool().adjExistDict(self.geodict,sel_list,srshader,'g mode') 

                else:
                    #group
                    pass
            return self.geodict
class spacename():
    def splitRealname(self,selected):
        if selected!=[]:
            return selected.split(":")[-1]
        return []
        
def getFileNames():
    filepath = cmds.file(expandName=1,q=1)
    filedir = os.path.dirname(filepath)
    return filedir
    
def rmparentCons(firstname,name,trlists):
    if pm.objExists(firstname+"_"+name)==True:
        pm.rename(firstname+"_"+name,firstname+"_"+name+"_tmp")
        for trlist in trlists:
            parentCons =  cmds.listRelatives(trlist,c=1,type=("parentConstraint","scaleConstraint"))
            cmds.delete(parentCons)
        pm.group(trlists,name=firstname+"_"+name)
    else:
        for trlist in trlists:
            parentCons =  cmds.listRelatives(trlist,c=1,type=("parentConstraint","scaleConstraint"))
            cmds.delete(parentCons)
        pm.group(trlists,name=firstname+"_"+name)
        
def abcoutput(arg):
    filename = os.path.basename(os.path.splitext(cmds.file(expandName=1,q=1))[0])
    path =cmds.textField('pathnum',tx=1,q=1).replace("\\","/")
    rangea =cmds.textField('rangenuma',tx=1,q=1)
    rangeb =cmds.textField('rangenumb',tx=1,q=1)
    rangesam =cmds.textField('rangesamnum',tx=1,q=1)
    geocb=cmds.checkBox("geonlycb" ,q=True,v=True)
    furcb = cmds.checkBox("furonlycb" ,q=True,v=True)
    if cmds.pluginInfo("AbcExport",q=1,loaded=1,name=1)==0:
        try:
            cmds.loadPlugin("AbcExport")
        except:
            pass
    if os.path.exists(path):
        sels = cmds.ls(sl=1)
        yeticols =[]
        yetiAss =[]
        locatercols = []  
        geoout = []  
        if sels!=[]:
            for sel in sels:
                locsels = [ y for y in cmds.listRelatives(sel,c=1) if y.find("arnold_loc")!=-1 and cmds.getAttr(y+".visibility")==1]
                yetiselgrps = [ y for y in cmds.listRelatives(sel,c=1) if y.find("yeti_G")!=-1]
                if geocb==1:
                    geodels = []
                    Miajudge = sel.find('Miarmy_Contents')
                    if Miajudge ==-1:
                        geogrps = [ y for y in cmds.listRelatives(sel,c=1) if y.find("_geo")!=-1]
                    else:
                        Agent =[a for a in cmds.listRelatives(sel,c=1) if a.find('Agent')!=-1]
                        if Agent!=[]:
                            geogrps = [b for b in  cmds.listRelatives(Agent[0],c=1) if b.find('Geometry')!=-1]
                        else:
                            geogrps = []
                    if geogrps!=[]:
                        for geogrp in geogrps:
                            if cmds.getAttr(geogrp+".visibility")==0:
                                try:
                                    cmds.setAttr(geogrp+".visibility",1)
                                except:
                                    cmds.warning(geogrp+".visibility cant be set!!")
                            #mainCtrl
                            if cmds.listConnections(geogrp,d=0,type="transform")!=None:
                                mainctrl =[m for m in cmds.listConnections(geogrp,d=0,type="transform") if m.find("Main")!=-1]
                                if mainctrl!=[]:
                                    mainFurAttrs =[f for f in cmds.listAttr(mainctrl[0],k=1) if f in['hair','yeti','hairYeti']]
                                    if mainFurAttrs!=[]:
                                        for  mainFurAttr in mainFurAttrs:
                                            if cmds.getAttr(mainctrl[0]+'.'+mainFurAttr)!=1:
                                                cmds.setAttr(mainctrl[0]+'.'+mainFurAttr,1)
                            #geoall
                            geoalls =[a for a in cmds.listRelatives(geogrp,ad=1) if cmds.nodeType(a)=="transform"]
                            for geoall in geoalls:
                                if cmds.listConnections(geoall+".visibility",type="animCurve")==None:
                                    if cmds.getAttr(geoall+".visibility")==False:
                                        geodels.append(geoall)
                            geoout.append(geogrp)
                        if  geodels !=[]:
                            if cmds.objExists(str(geogrps[0]+"_del"))==True:
                                cmds.rename(str(geogrps[0]+"_del"),str(geogrp[0]+"_tmp"))
                                cmds.parent(geodels,w=1)
                                cmds.group(geodels,name=str(geogrps[0]+"_del"))
                            else:
                                cmds.parent(geodels,w=1)
                                cmds.group(geodels,name=str(geogrps[0]+"_del") ) 

                    #bake blender
                    try:
                        blctrl = sel[:len(sel.split(":")[-1])]+":key_Ani"
                    except:
                        blctrl = []
                    if blctrl!=[]:
                        if cmds.objExists(blctrl):
                            blnode = [ bln for bln in  cmds.hyperShade(listDownstreamNodes =blctrl) if cmds.nodeType(bln)=="blendColors"]
                            cmds.bakeResults(blnode,simulation=1,t=rangea+":"+rangeb,sampleBy = int(rangesam))
                        
                if furcb==1:
                    locatercols += locsels
                    if yetiselgrps!=[]:
                        yetishowgrps = [yt for yt in  cmds.listRelatives(yetiselgrps,c=1) if yt.find("yeti_show_G")!=-1]
                        yetinodes =cmds.listRelatives(yetishowgrps,c=1)
                        if yetinodes!=None:
                            for yetinode in yetinodes:
                                if cmds.getAttr(yetinode+".visibility")==True:
                                    if cmds.getAttr(cmds.listRelatives(yetinode,p=1)[0]+".visibility")==True:
                                        yeticols.append(yetinode)
        if geocb==False:
            geoout=[]
        if furcb==False:
            yeticols=[]
            locatercols=[]

        #output abc
        cmds.select(geoout,r=1)
        abcname ="-frameRange {0} {1} -uvWrite -worldSpace -writeVisibility -dataFormat hdf".format(rangea,rangeb)
        for ou in range(len(geoout)):
            abcname = abcname+" -root "+geoout[ou]
        if abcname!="-frameRange {0} {1} -uvWrite -worldSpace -writeVisibility -dataFormat hdf".format(rangea,rangeb):
            abcoutputfurpath = path+"/"+filename+".abc"
            nn=1
            while os.path.exists(abcoutputfurpath)==True:
                abcoutputfurpath = path+"/"+filename+"_"+str(nn)+".abc"
                nn =nn+1 
            cmds.AbcExport(j = abcname+" -file {0}".format(abcoutputfurpath)) 
  
        #output yeticache    
        if yeticols!=[]:
            yeticachename = yeticols[0].replace(":","__")
            cmds.select(yeticols,r=1)
            cmds.pgYetiCommand(flushGeometryCache=1)
            cmds.pgYetiCommand(flushTextureCache=1)
            cmds.pgYetiCommand(flushDisplayCache=1)
            if os.path.exists(path+"/yetiAss")==False:
                os.mkdir(path+"/yetiAss")
            cmds.select(yeticols,r=1)
            cmds.arnoldExportAss(f=path+"/yetiAss/"+yeticachename+".ass",s=1,expandProcedurals=1,startFrame=int(rangea),endFrame=int(rangeb),frameStep=int(rangesam),lightLinks=0,compressed=1,boundingBox=1,shadowLinks=0,mask=24,cam='perspShape')
            mtoa.core.createStandIn(path+"/yetiAss/"+yeticachename+r".####.ass.gz")
            assShape = cmds.ls(sl=1,type="aiStandIn") 
            cmds.expression(s =assShape[0]+ ".frameNumber=frame")
            yetiAss = cmds.listRelatives(assShape[0],p=1)
            print "已输出"+str(len(yeticols))+"个毛发节点!!",

        #bak hairAss locater    
        if locatercols!=[]:
            for locatercol in locatercols:
                locaterAttrs =  cmds.listAttr(locatercol,v=1,k=1)
                for locaterAttr in locaterAttrs:
                    lockjudge = cmds.getAttr(locatercol+"."+locaterAttr,l=1)
                    if lockjudge==1:
                        cmds.setAttr(locatercol+"."+locaterAttr,l=0)

            pm.bakeResults(locatercols,simulation=1,t=rangea+":"+rangeb,sampleBy = int(rangesam))
            for locatercol in locatercols:
                parentCons =  cmds.listRelatives(locatercol,c=1,type=("parentConstraint","scaleConstraint"))
                cmds.delete(parentCons)
                lacattrv =   cmds.listConnections(locatercol+".visibility",d=0,plugs=1)
                if lacattrv!=[]:
                    cmds.disconnectAttr(lacattrv[0],locatercol+".visibility")
            cmds.parent(locatercols,w=1)  
        if yetiAss!=[] and locatercols!=[]:
            rmparentCons(filename,"Ass_G",locatercols)
            furcachegrp = cmds.group(yetiAss,filename+"_Ass_G",name=filename+"_furCache_G")
            cmds.select(furcachegrp,r=1,hi=1)
            cmds.rename(yetiAss[0],filename+"_yetiAss_Aist")
            outputfurpath = path+"/"+filename+"_fur.mb"
            nn=1
            while os.path.exists(outputfurpath)==True:
                outputfurpath = path+"/"+filename+"_fur_"+str(nn)+".mb"
                nn =nn+1
            cmds.file(outputfurpath,force = 1,options ='v=0;' ,typ = 'mayaBinary',pr=1,es=1 )

        elif locatercols!=[]:
            rmparentCons(filename,"Ass_G",locatercols)
            furcachegrp = cmds.group(filename+"_Ass_G",name=filename+"_furCache_G")
            cmds.select(furcachegrp,r=1,hi=1)
            outputfurpath = path+"/"+filename+"_fur.mb"
            nn=1
            while os.path.exists(outputfurpath)==True:
                outputfurpath = path+"/"+filename+"_fur_"+str(nn)+".mb"
                nn =nn+1 
            cmds.file(outputfurpath,force = 1,options ='v=0;' ,typ = 'mayaBinary',pr=1,es=1 )
    else:
        cmds.warning('目标路径不存在！！！')


def changecache(arg):
    path =cmds.textField('pathnum',tx=1,q=1).replace("\\","/")
    sel = [u for u in pm.ls(sl=1) if u.nodeType()=="transform" ]
    yeticol =[]
    locatercol = []     
    if sel!=[]:
        for s in range(len(sel)):
            yetigrpsel = [e for e in  sel[s].getChildren() if e.split("_")[-2]=="yeti"]
            if yetigrpsel!=[]:
                yetisel =[a for a in  yetigrpsel[0].getChildren()]
                for y in range(len(yetisel)):
                    yeticachename = [e.replace(":","__") for e in  yetisel if yetisel !=[]]
                    pm.pgYetiCommand(flushGeometryCache=1)
                    pm.pgYetiCommand(flushTextureCache=1)
                    pm.pgYetiCommand(flushDisplayCache=1)
                    pm.setAttr(yetisel[y].getShape()+".cacheFileName",str(path+"/"+yeticachename[y]+".%04d.fur"))
                print "设置了"+str(len(yetisel))+"个毛发节点的缓存路径!!",
    abcsel =pm.ls(type = "AlembicNode")
    if abcsel!=[]:
        for b in range(len(abcsel)):
            abcoldpath = abcsel[b].getAttr("abc_File").replace("\\","/")
            abcnewpath = path+"/"+os.path.basename(abcoldpath)
            pm.setAttr(str(abcsel[b]+".abc_File"),str(abcnewpath),type="string")


def offsetanim(arg):
    offsetnums =cmds.textField('offsetnum',tx=1,q=1)
    try:
        mel.eval('source "C:/Program Files/Autodesk/Maya2015/scripts/AETemplates/AEnewNonNumericMulti.mel"')
    except:
        cmds.warning( "maya不是安装在C盘!")
    sel =pm.ls(sl=1)
    if sel!=[]:
        for s in range(len(sel)):
            yetigrpsel = [e for e in  sel[s].getChildren() if e.split("_")[-2]=="yeti"]
            if yetigrpsel!=[]:
                yetisel =[a for a in  yetigrpsel[0].getChildren()]
                for y in range(len(yetisel)):
                    time =pm.listConnections(yetisel[y].getShape()+".currentTime",d=0,plugs=1)[0]
                    timeadj = pm.listConnections(yetisel[y].getShape()+".currentTime",d=0,type="time")
                    if timeadj!=[]:
                        newsub=pm.shadingNode("plusMinusAverage",asUtility=1)
                        pm.setAttr(newsub+".operation",2)
                        add2did= 'AEnewNonNumericMultiAddNewItem("%s","input2D");'%(newsub)
                        mel.eval(add2did)
                        pm.connectAttr(time,newsub+".input2D[0].input2Dx",f=1)
                        pm.setAttr(newsub+".input2D[1].input2Dx",float(offsetnums))
                        pm.connectAttr(newsub+".output2D.output2Dx",yetisel[y].getShape()+".currentTime",f=1)
                    else:
                        unit = pm.listConnections(yetisel[y].getShape()+".currentTime",d=0)[0]
                        subnode = pm.listConnections(unit,d=0)[0]
                        pm.setAttr(subnode+".input2D[1].input2Dx",float(offsetnums))
            locatgrp = [e for e in  sel[s].getChildren() if e.split("_")[-2]=="Ass"]
            if locatgrp!=[]:
                locatsel =[l for l in  locatgrp[0].getChildren()] 
                for o in range (len(locatsel)):
                    ancv = pm.listConnections(locatsel[o],d=0,type="animCurve")
                    for c in range(len(ancv)):
                        pm.keyframe(ancv[c],e=1,iub=False,an="objects",t=":",r=1,o="over",tc=float(offsetnums))
            yetiassgrps = [y for y in  sel[s].getChildren() if y.split("_")[-2]=="yetiAss"]
            if yetiassgrps!=[]:
                for yetiassgrp in yetiassgrps:
                    pm.setAttr(yetiassgrp.getShape()+'.frameOffset',float(offsetnums))
        pm.select(sel,hi=1)
        abcgrp =[sh for sh in pm.ls(sl=1) if sh.nodeType() =="mesh" and pm.listConnections(sh+".inMesh",d=0,type = "AlembicNode")]
        
        if abcgrp!=[]:
            for ax in range(len(abcgrp)):
                abcnode =  pm.listConnections(abcgrp[ax]+".inMesh",d=0,type = "AlembicNode")
                for ab in range(len(abcnode)):
                    pm.setAttr(abcnode[ab]+".offset",int(offsetnums))  


def recovershader(arg):
    transferAttrs = ['aiOpaque',
             'aiSubdivType',
             'aiSubdivIterations',
             'aiSubdivAdaptiveMetric',
             'aiSubdivPixelError',
             'aiSubdivAdaptiveSpace',
             'aiSubdivUvSmoothing',
             'aiSubdivSmoothDerivs',
             'aiDispHeight',
             'aiDispPadding',
             'aiDispZeroValue',
             'aiDispAutobump']
    filename = os.path.basename(os.path.splitext(cmds.file(expandName=1,q=1))[0])
    path =cmds.textField('pathnum',tx=1,q=1).replace("\\","/")
    recoverNombCB=pm.checkBox("recoverNoMb" ,q=True,v=True)
    sels =cmds.ls(sl=1,type="transform",l=1) 
    geotrgrp = [d for d in sels if d.find('Geometry')!=-1 or d.split('_')[-1]=="geo"]
    for sel in sels:
        if sel!=[]:
            geodel = [d for d in sel if d.find('_del')!=-1]
            geosrgrp = []
            attrShape = []
            Miajudge = sel.find('Miarmy_Contents')
            if Miajudge==-1:
                if sel.find("_all")!=-1:
                    geoallsrs = [sel+"|"+a for a in cmds.listRelatives(sel,c=1) if a.find('_geo')!=-1]
                    geosrgrp += geoallsrs
            else:
                Agent =[a for a in cmds.listRelatives(sel,c=1) if a.find('Agent')!=-1]
                if Agent!=[]:
                    Mageogrps = [b for b in  cmds.listRelatives(Agent[0],c=1) if b.find('Geometry')!=-1]
                    Mageogrp = [c for c in cmds.ls(Mageogrps,l=1) if len(c.split("|"))!=2]
                    geosrgrp +=Mageogrp   
            for x in range(len(geosrgrp)):
                geotrgrps = [t for t in geotrgrp if t.split("|")[-1] == geosrgrp[x].split("|")[-1]]
                geotr =pm.listRelatives(geotrgrps,ad=1)
                if geotr!=[]:
                    geosrs = abctool().builddict(geosrgrp[x])
                    for o in range(len(geosrs.keys())):
                        targetgeo = [ z for z in geotr if z.split("|")[-1] ==geosrs.keys()[o].split("|")[-1]]
                        if targetgeo==[]:
                            targetgeo = [ z+"."+geosrs.keys()[o].split("|")[-1].split(".")[-1] for z in geotr if z.split("|")[-1] ==geosrs.keys()[o].split("|")[-1].split(".")[0]]
                        if len(targetgeo)==1:
                            if pm.objExists(pm.general.PyNode(targetgeo[0]))==True:
                                #属性传递
                                if geosrs.keys()[o].find('.f[')==-1:
                                    if geosrs.keys()[o] not in attrShape:
                                        for transferAttr in transferAttrs:
                                            try:
                                                pm.general.PyNode(targetgeo[0]).setAttr(transferAttr,pm.general.PyNode(geosrs.keys()[o]).getAttr(transferAttr))
                                                attrShape.append(geosrs.keys()[o])
                                            except:
                                                pm.warning( transferAttr+"属性传递失败！！",)
                                else:
                                    faceshape = pm.general.PyNode(geosrs.keys()[o][:-len(geosrs.keys()[o].split('.')[-1])-1]).getShapes()
                                    trfaceshape = pm.general.PyNode(targetgeo[0][:-len(targetgeo[0].split('.')[-1])-1]).getShapes()
                                    if faceshape not in attrShape:
                                        for transferAttr in transferAttrs:
                                            try:
                                                if faceshape[0].getAttr(transferAttr)!=trfaceshape[0].getAttr(transferAttr):
                                                    trfaceshape[0].setAttr(transferAttr,faceshape[0].getAttr(transferAttr)) 
                                                attrShape.append(faceshape)
                                            except:
                                                pm.warning( transferAttr+"属性传递失败！！",)
                                #材质传递      
                                shader = pm.ls(geosrs.values()[o],mat=1)
                                if shader!=[]:              
                                    pm.select(targetgeo[0],r=1)
                                    pm.hyperShade(assign=shader[0])
                                else:
                                    shader = pm.ls(geosrs.values()[o])
                                    attrConnects=pm.listConnections(shader[0],c=1,type="shadingEngine",plugs=1)
                                    if attrConnects!=[]:
                                        for attrConnect in attrConnects:
                                            tmplam = pm.shadingNode('lambert',asShader=1)
                                            attrs= list(attrConnect)
                                            pm.connectAttr(tmplam+'.outColor',attrs[1],f=1)
                                            pm.select(targetgeo[0],r=1)
                                            pm.hyperShade(assign=tmplam)
                                            pm.connectAttr(attrs[0],attrs[1],f=1)
                                            pm.delete(tmplam)
                                    else:
                                        pm.warning( "――――――――材质找不到对应的SG节点――――――――")
                                        
                            else:
                                pm.warning( geosrs.keys()[o]+"找不到对应的材质恢复模型")
    if recoverNombCB==0:
        pm.select(geotrgrp,hi=1,r=1)
        pm.delete(geosrgrp)
        abcgeooutputfurpath = path+"/"+filename+"_geoabc.mb"
        nn=1
        while os.path.exists(abcgeooutputfurpath)==True:
            abcgeooutputfurpath = path+"/"+filename+"_"+str(nn)+"_geoabc.mb"
            nn =nn+1 
        cmds.file(abcgeooutputfurpath,force = 1,options ='v=0;' ,typ = 'mayaBinary',pr=1,es=1,ch=1 )

        
def comshder(arg):
    SGsel =pm.ls(type="shadingEngine")
    shader = [pm.listConnections(i+".surfaceShader",d=0)[0] for i in  SGsel if pm.listConnections(i+".surfaceShader",d=0)!=[]]
    shaderdict ={}
    mushder = []
    for s in range(len(shader)):
        if len(shader[s].split(":"))!=1:
            choicefile = [h for h in pm.hyperShade(listUpstreamNodes = shader[s]) if pm.nodeType(h)=="file" and pm.listConnections(h+".fileTextureName",d=0,type="choice")!=[]]
            if choicefile==[]:
                shdernickname =  shader[s][-len(shader[s].split(":")[-1]):]
                if shdernickname not in shaderdict.keys():
                    shaderdict[shdernickname]=shader[s]     
                else:
                    sg =  pm.listConnections(shader[s],s=0,type="shadingEngine")
                    for g in range(len(sg)):
                        if pm.listConnections(sg[g],d=0,type="mesh")!=[] or pm.listConnections(sg[g],s=0,type="mesh")==[]:
                            pm.hyperShade(objects = shader[s])
                            pm.hyperShade(assign = shaderdict[shdernickname])
                            print u"%s 材质已替换为%s材质！！"%(shader[s],shaderdict[shdernickname]),
            else:
                mushder.append(shader[s])
    multistnickname =[]
    multistpath =[]
    multistshder = []
    multistifile =[]
    mushaderdict ={}
    for m in range(len(mushder)):
        multichoicefile = [h for h in pm.hyperShade(listUpstreamNodes = mushder[m]) if pm.nodeType(h)=="file" and pm.listConnections(h+".fileTextureName",d=0,type="choice")!=[]]
        mutlichfilepath  = pm.getAttr(multichoicefile[0]+".fileTextureName")
        shdernicknames =  mushder[m][-len(mushder[m].split(":")[-1]):]
        if multichoicefile not in multistifile:
            if  shdernicknames not in multistnickname and mutlichfilepath not in multistpath:
                multistnickname.append(shdernicknames)
                multistpath.append(mutlichfilepath)
                multistshder.append(mushder[m])
                multistifile.append(multichoicefile)
        else:
            if  shdernicknames not in multistnickname:
                multistnickname.append(shdernicknames)
                multistpath.append(mutlichfilepath)
                multistshder.append(mushder[m])
    mushders=[u for u in mushder if u not in multistshder]
    for ms in range(len(mushders)):
        multichoicefiles = [h for h in pm.hyperShade(listUpstreamNodes = mushders[ms]) if pm.nodeType(h)=="file" and pm.listConnections(h+".fileTextureName",d=0,type="choice")!=[]]
        mutlichfilepaths  = pm.getAttr(multichoicefiles[0]+".fileTextureName")
        shdernicknames =  mushders[ms][-len(mushders[ms].split(":")[-1]):]
        if shdernicknames in multistnickname :
            num = multistnickname.index(shdernicknames)
            if shdernicknames==multistnickname[num] and mutlichfilepaths ==multistpath[num]:
                sg =  pm.listConnections(mushders[ms],s=0,type="shadingEngine")
                for g in range(len(sg)):
                    if pm.listConnections(sg[g],d=0,type="mesh")!=[] and pm.listConnections(sg[g],s=0,type="mesh")==[]:
                        pm.hyperShade(objects = mushders[ms])
                        pm.hyperShade(assign = multistshder[num])
                        print u"%s 材质已替换为%s材质！！"%(mushders[ms], multistshder[num]),
    print "已完成所有同类型角色的材质替换！！",
    
def AiSTsetCopypath(arg):
    path =cmds.textField('pathnum',tx=1,q=1).replace("\\","/")
    aiStInsel=pm.checkBox("aiStInselcb" ,q=True,v=True)
    aiStIncopy=pm.checkBox("aiStIncopycb" ,q=True,v=True)
    if aiStInsel==0:
        sels =pm.ls(type = "aiStandIn")
    else:
        sels =[s.getShape() for s in  pm.ls(sl=1) if pm.ls(s.getShape(),type="aiStandIn")!=[]]
    repathcol = []
    for sel in sels:
        getpath = cmds.getAttr(sel+'.dso' )
        getdir = os.path.dirname(getpath)
        newpath = getpath.replace(getdir,path)
        if getpath=="":
            continue
        if aiStIncopy==0:
            if os.path.exists(getpath):
                if newpath!=getpath:
                    cmds.setAttr( sel+'.dso',newpath, type='string' )
                    shutil.copyfile(getpath,newpath)
                    
            else:
                repathcol.append(sel)
                cmds.warning(sel+"'s path no exists!!")
        else:
            if os.path.exists(newpath):
                cmds.setAttr( sel+'.dso',newpath, type='string' )
            else:
                repathcol.append(sel)
                cmds.warning(sel+"'s newpath no exists!!")
    if repathcol!=[]:
        repathcol ==len(list(set(repathcol)))
    return repathcol
def AbcAioffsetConnected(arg):
    try:
        mel.eval('source "C:/Program Files/Autodesk/Maya2015/scripts/AETemplates/AEnewNonNumericMulti.mel"')
    except:
        pm.warning( "maya不是安装在C盘!")
    sels=cmds.ls(sl=1)
    abcnode=pm.ls(type="AlembicNode")
    AiStnodes = pm.ls(type='aiStandIn')
    gtime = pm.ls(type='time',ud=1)
    if len(abcnode)==1:
        try:
            for AiStnode in AiStnodes:
                newsub = pm.shadingNode('plusMinusAverage',asUtility=1,name="abc_plus")
                pm.setAttr(newsub+".operation",2)
                add2did= 'AEnewNonNumericMultiAddNewItem("%s","input2D");'%(newsub)
                mel.eval(add2did)
                pm.connectAttr(gtime[0]+".outTime",newsub+".input2D[0].input2Dx",f=1)
                pm.connectAttr(abcnode[0]+".offset",newsub+".input2D[1].input2Dx",f=1)
                pm.connectAttr(newsub+".output2Dx",AiStnode+'.frameNumber',f=1)
            print 'abc成功链接了'+len(AiStnodes)+'个Arnold缓存的帧偏移',
        except:
            pm.warning('abc与Arnold缓存链接不成功！！')
    else:
        if sels!=[]:
            abcnode = sels[0]
            AiStnodes = sels[1:]
            gtime = pm.ls(type='time',ud=1)
            try:
                for AiStnode in AiStnodes:
                    newsub = pm.shadingNode('plusMinusAverage',asUtility=1,name="abc_plus")
                    pm.setAttr(newsub+".operation",2)
                    add2did= 'AEnewNonNumericMultiAddNewItem("%s","input2D");'%(newsub)
                    mel.eval(add2did)
                    pm.connectAttr(gtime[0]+".outTime",newsub+".input2D[0].input2Dx",f=1)
                    pm.connectAttr(abcnode+".offset",newsub+".input2D[1].input2Dx",f=1)
                    pm.connectAttr(newsub+".output2Dx",AiStnode+'.frameNumber',f=1)
                print 'abc成功链接了'+str(len(AiStnodes))+'个Arnold缓存的帧偏移',
            except:
                pm.warning('abc与Arnold缓存链接不成功！！')
        else:
            pm.warning('文件中存在多个abc缓存节点，请选择一个abc缓存节点再多选Arnold缓存节点进行操作关联！！')
        
def yeticonnectAttr(typename,yetishapesr,yetishapetr):
    yetinodes=[]
    if yetishapesr!=[] and yetishapetr!=[]:
        yeticonnects = yetishapesr.listConnections(c=1,type=typename,plugs=1)
        if yeticonnects!=[]:
            for yeticonnect in yeticonnects:
                yeticonnectsr = yeticonnect[0]
                yeticonnecttr = yeticonnect[1]
                yetinode = yeticonnect[1].split(".")[0]
                pm.connectAttr( yeticonnectsr.replace(str(yetishapesr),str(yetishapetr)),yeticonnecttr,f=1)
                if pm.nodeType(yetinode)=="pgYetiMaya":
                    yetiimps = pm.pgYetiGraph(yetinode,listNodes=True,type="import") 
                    if yetiimps!=[]:
                        for yetiimp in yetiimps:
                            if pm.pgYetiGraph(yetinode,node=yetiimp,param="type",getParamValue=1)==0:
                                pm.pgYetiGraph(yetinode,node=yetiimp,param="geometry",setParamValueString=yetishapetr.split("|")[-1].split(":")[-1])
                yetinodes.append(yetinode)
    return yetinodes

def grmrebuild(grmsels,trmesh):
    if grmsels!=[]:
        for grmsel in grmsels:
            adj = pm.objExists(grmsel+"Shape_strand_set")
            if adj:
                pm.delete(grmsel+"Shape_strand_set")
            pm.pgYetiCommand(pm.listRelatives(grmsel,c=1),convertToCurves=1)
            grmset = cmds.ls(grmsel+"Shape_strand_set")
            grmcvs = cmds.listConnections(grmset[0],d=1)
            delcvgrps = pm.group(grmcvs)
            newset = cmds.sets(grmcvs,n=grmsel+"_set")
            newgrm = pm.createNode("pgYetiGroom")
            pm.rename(newgrm.getParent(),trmesh.getParent().replace(":","_")+"_grm")
            pm.rename(newgrm,trmesh.getParent().replace(":","_")+"_grmShape")
            pm.connectAttr(trmesh+".worldMesh[0]",newgrm+".inputGeometry",f=1)
            yetitarattrs = grmsel.getShape().listConnections(s=0,type="pgYetiMaya",plugs=1)
            for yetitarattr  in yetitarattrs:
                pm.connectAttr(newgrm+ ".outputData" ,yetitarattr,f=1)
            pm.connectAttr("time1.outTime",newgrm+".currentTime",f=1)
            pm.pgYetiCommand(newgrm,convertFromCurves=newset,inputGeometry=trmesh,stepSize=0.001)
            yetinodesrs = trmesh.listConnections(s=0,type="pgYetiMaya")
            for yetinodesr in yetinodesrs:
                yetiimps = pm.pgYetiGraph(yetinodesr,listNodes=True,type="import")
                if yetiimps!=[]:
                    for yetiimp in yetiimps:
                        if pm.pgYetiGraph(yetinodesr,node=yetiimp,param="type",getParamValue=1)==1:
                            pm.pgYetiGraph(yetinodesr,node=yetiimp,param="geometry",setParamValueString=newgrm.split(":")[-1])
            pm.delete(delcvgrps)
            return newgrm

def yetitransfer(yetimeshsrs,yetimeshtrs):
    try:
        yetishapesrs = yetimeshsrs.getShape()
        yetishapetrs = yetimeshtrs.getShape()
    except:
        yetishapesrs=[]
        yetishapetrs=[]
        cmds.warning(str(yetishapesrs)+"'s shapeNode is not exists!!")
    #sruvset = pm.polyUVSet(yetishapesrs,q=1,currentUVSet=1)[0]
    #truvset = pm.polyUVSet(yetishapetrs,q=1,currentUVSet=1)[0]
    pm.transferAttributes(yetishapetrs,yetishapesrs,transferPositions=1,transferNormals=1,transferUVs=0,transferColors=0,sampleSpace=3,sourceUvSpace='map1',targetUvSpace='map1',searchMethod=3,flipUVs=0,colorBorders=1)
    yetinodecol = yeticonnectAttr("pgYetiMaya",yetishapesrs,yetishapetrs)
    grmsels= yetishapesrs.listConnections(s=0,type="pgYetiGroom")
    grmcols = grmrebuild(grmsels,yetishapetrs)
    pm.select(yetimeshtrs,r=1)
    if pm.objExists(yetimeshtrs+"_reference")==True:
        pm.delete(yetimeshtrs+"_reference")
    try:
        mel.eval("CreateTextureReferenceObject")
    except:
        pass
    refmesh = cmds.listConnections(yetishapetrs+".referenceObject",d=0,type="mesh")
    pm.group(yetinodecol,grmcols,refmesh,name=str(yetimeshtrs.split(":")[-1])+"_yeti_G")

def hairtransfer(hairsrmesh,hairtrmesh):
    hairsyssels=[]
    filename =os.path.basename( cmds.file(expandName=1,q=1)).split(".")[0]
    hairwhole = pm.group(em=1,name=filename+"_hair_G")
    folwhole = pm.group(em=1,name=filename+"_fols_G")
    cvswhole = pm.group(em=1,name=filename+"_outputCvs_G")
    pfxwhole = pm.group(em=1,name=filename+"_pfxHairs_G")
    try:
        hairShapesr =  hairsrmesh.getShape()
        hairShapetr =  hairtrmesh.getShape()
    except:
        hairShapesr=[]
        hairShapetr=[]
        pm.warning(selsrs[i]+"'s shapeNode is not exists!!")
    follicles =  pm.listConnections(hairShapesr,s=0,type="follicle")
    if follicles!=None:
        for follicle in follicles:
            follicleshape =  follicle.getShape()
            hairsyssel = pm.listConnections( follicleshape+".outHair",s=0,type="hairSystem")[0]
            if hairsyssel not in hairsyssels:
                hairsyssels.append(hairsyssel)
                pfxhairsel = pm.listConnections( hairsyssel+".outputRenderHairs",s=0,type="pfxHair")[0]
                pm.parent(pfxhairsel,pfxwhole)
                folliclesels = pm.listConnections( hairsyssel+".inputHair",d=0)
                cvs = [pm.listConnections(a+".outCurve",s=0)[0] for a in folliclesels]
                for cv in cvs:
                    cvsconnects= pm.listConnections(cv.getShape(),c=1,plugs=1)[0]
                    pm.disconnectAttr(cvsconnects[1],cvsconnects[0])
                cvsgrp =pm.group(cvs,name=str(hairsyssel)+"_cvs_g")
                pm.select(hairtrmesh,r=1)
                pm.select(cvsgrp,tgl=1)
                mel.eval('makeCurvesDynamic 2 { "1", "1", "1", "1", "1"};')
                newfollicles = [b.getParent() for b in cvs if b.getParent().getShape()!=None]
                newcvs = [pm.listConnections(a+".outCurve",s=0)[0] for a in newfollicles ]
                oldhairsys =[pm.listConnections(a.getShape()+".outHair",s=0,type="hairSystem")[0] for a in newfollicles]
                oldhairsys = list(set(oldhairsys))
                nucleussels =[pm.listConnections(a.getShape(),s=0,type="nucleus")[0] for a in oldhairsys]
                nucleussels = list(set(nucleussels))
                pm.delete(oldhairsys,nucleussels)
                pm.select(newfollicles,r=1)
                mel.eval('assignHairSystem %s'%(hairsyssel))
                try:
                    pm.parent(hairsyssel+"Follicles",folwhole)
                    
                    pm.parent(hairsyssel+"OutputCurves",cvswhole)
                    pm.setAttr(hairsyssel+"OutputCurves.visibility",0)
                except:
                    pm.warning('cant not parent Follicles and OutputCurves group!!')
    hairsystrsgrp = pm.group(hairsyssels,name = filename+"_hairSystems_G")      
    pm.parent(pfxwhole,hairwhole)       
    pm.parent(hairsystrsgrp,hairwhole)
    pm.setAttr(hairsystrsgrp+".visibility",0)
    pm.parent(folwhole,hairwhole)
    pm.setAttr(folwhole+".visibility",0)
    pm.parent(cvswhole,hairwhole)
    pm.setAttr(cvswhole+".visibility",0)

def hairyetitransfer_main(arg):
    '''
    {'load':'maya_fur','defaultOption':1,'CNname':'一键传递hair或yeti毛发'}
    '''
    sels=pm.ls(sl=1)
    selsrs = sels[:len(sels)/2]
    seltrs = sels[len(sels)/2:]
    for i in range(len(selsrs)):
        try:
            hairShapesr =  selsrs[i].getShape()
            hairShapetr =  seltrs[i].getShape()
        except:
            hairShapesr=[]
            hairShapetr=[]
            pm.warning(selsrs[i]+"'s shapeNode is not exists!!")
        if hairShapesr!=[] and hairShapetr!=[]:
            hairadj =  pm.listConnections(hairShapesr,s=0,type="follicle")
            yetiadj= pm.listConnections(hairShapesr,s=0,type="pgYetiMaya")
            if hairadj!=[]:
                hairtransfer(selsrs[i],seltrs[i])
            elif yetiadj!=[]:
                yetitransfer(selsrs[i],seltrs[i])
    
def  SJ_abcFurCache_ToolwdUI():
    '''
    1.5更新说明：修复按面赋予材质无法复原abc材质的问题,增加智能筛选大组功能，已能自动识别大组后带数字的情况，如char_all2,char_geo6..等情况；修复仅模型输出功能失效问题
    1.6更新说明：增加魔礼兽表情blender节点烘焙帧功能
    1.7更新说明：优化复原abc材质功能，增加复原后不输出mb文件选项。
    1.8更新说明：增加Arnold缓存批量指定及拷贝功能。
    1.9更新说明：目标路径自动获取本文件所在文件夹；优化abc及毛发输出;增加自动加载abc插件功能；整合miamy的abc输出及材质复原流程
    1.9.1更新说明：修复跑多个mb文件，及yeti节点为空时报错问题
    2.0更新说明：增加yeti跑Ass缓存功能
    2.1更新说明：增加abc与Arnold帧偏移关联功能
    2.2更新说明：增加hair及yeti传递毛发到abc模型的功能
    '''
    if cmds.window('abctoolwd',ex=True):
        cmds.deleteUI('abctoolwd',wnd=True)
    updatetxt =fantabox.ani.SJ_abcFurCache_ToolwdUI.__doc__
    cmds.window('abctoolwd',t='abcToolV2.2')
    cmds.columnLayout(adj=True,w=240)
    cmds.text(l='abc工具V2.2', fn='fixedWidthFont',h=50,ann=updatetxt )
    cmds.text(l='帧数区间（开始帧，结束帧,Sample）',fn='fixedWidthFont',h=50,ann="")
    cmds.flowLayout( columnSpacing=0)
    cmds.textField('rangenuma',tx="0",h=30,w=100)
    cmds.textField('rangenumb',tx="1",h=30,w=100)
    cmds.textField('rangesamnum',tx="1",h=30,w=100)
    cmds.setParent( '..' )
    cmds.text(l='目标路径', fn='fixedWidthFont',h=50,ann="" )
    cmds.textField('pathnum',tx=getFileNames(),h=30)
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("geonlycb" ,label='输出模型',v=1,ann="",w=210,h=30)
    cmds.checkBox("furonlycb" ,label='输出毛发',v=1,ann="",w=80,h=30)
    cmds.setParent( '..' )
    cmds.button(l='输出abc及毛发缓存',c=abcoutput,h=50,ann="选择角色大组（可多选），输入输出路径，设置起始帧，点击执行命令。")
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("aiStInselcb" ,label='仅对选择对象进行操作',v=0,ann="默认情况对场景所有Arnold缓存进行操作",w=150,h=30)
    cmds.checkBox("aiStIncopycb" ,label='仅指定Arnold缓存路径，不拷贝',v=0,ann="默认情况下进行缓存的拷贝并指定到目标路径",w=180,h=30)
    cmds.setParent( '..' )
    cmds.button(l='Arnold缓存批量指认拷贝',c=AiSTsetCopypath,h=50,ann="")
    cmds.button(l='选中毛发组yeti缓存路径指定\ \n 全场景abc缓存路径指定',c=changecache,h=50,ann="选择输出的毛发缓存大组，输入需要指定的毛发缓存路径，点击执行命令。\ \n 场景内所有abc缓存路径替换为指定路径") 
    cmds.text(l='~~~~~~导入abc文件~~~~~~~', fn='fixedWidthFont',h=50,ann="" )
    cmds.flowLayout( columnSpacing=0)
    cmds.checkBox("recoverNoMb" ,label='复原后不输出mb文件',v=0,ann="",w=210,h=30)
    cmds.setParent( '..' ) 
    cmds.button(l='复原abc材质并输出abc文件', c= recovershader,h=50,ann="选择原角色大组及导入的abc角色大组，点击自动还原")
    cmds.button(l='合并角色材质', c= comshder,h=50,ann="合并场景内所有相同角色材质")
    cmds.button(l='传递毛发', c= hairyetitransfer_main,h=50,ann="先选原毛发生长模型，再选择目标模型，点击传递（可多对多）")
    cmds.button(l='选中毛发组yeti缓存路径指定\ \n 全场景abc缓存路径指定',c=changecache,h=50,ann="选择输出的毛发缓存大组，输入需要指定的毛发缓存路径，点击执行命令。\ \n 场景内所有abc缓存路径替换为指定路径")
    cmds.textField('offsetnum',tx="10",h=30)
    cmds.button(l='偏移缓存动画',c=offsetanim,h=50,ann="选择输出的毛发缓存大组或abc角色大组，输入偏移帧数，点击执行命令")
    cmds.button(l='abc与AiStandIn关联帧偏移',c=AbcAioffsetConnected,h=50,ann="若场景中只有一个abc缓存节点，请直接执行；若场景中有多个abc缓存节点，请先选一个abc缓存节点，再多选arnold缓存节点，再执行操作")
    cmds.showWindow()