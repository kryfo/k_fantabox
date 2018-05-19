#!/usr/bin/python
#-*- coding: iso-8859-15 -*-
# -*- coding: cp936 -*-
# -*- coding: utf-8 -*-
###================ Model library =======================
import maya.cmds as cmds
import os
import re
###======================================================
def YY_Desk():
    return '//10.99.1.6/Digital/Library'
###======================================================
def YY_SoDir(path = '',copyPath = '',texs = []):
    pa = os.listdir(path)
    for p in pa:
        fullPath = os.path.join(path,p)
        if os.path.isdir(fullPath):
            YY_SoDir(fullPath,copyPath,texs)
        else:
            if p.lower() in texs:
                shutil.copyfile(fullPath,'%s/%s'%(copyPath,p))
###======================================================
def propList():
    pFloders = [g for g in os.listdir('%s/propLibrary'%YY_Desk()) if  os.path.isdir('%s/propLibrary/%s/scenes'%(YY_Desk(),g)) and os.path.isfile('%s/propLibrary/%s/fileInfo.txt'%(YY_Desk(),g))]
    infos = []
    for p in pFloders:
        pi = '%s/propLibrary/%s'%(YY_Desk(),p)
        if os.path.isfile('%s/fileInfo.txt'%pi):
            mFiles = [f for f in os.listdir('%s/scenes'%pi) if os.path.isfile('%s/scenes/%s'%(pi,f)) and re.match('[A-Za-z]\w*\.m(a|b)',f)]
            
            baseNames = [m.split('.')[0] for m in mFiles]
            
            try:
                f = file('%s/fileInfo.txt'%pi,'r')
                reads = [p + '/' +i.replace('\r\n','')+'\r\n' for i in f.readlines() if len(i.split()) and re.match('[A-Za-z]\w*',i.split()[0]) and i.split()[0] in baseNames]
                print reads
                infos+=reads           
            except:
                return
            finally:
                f.close() 
    try:
        infos.sort()
        fi = file('%s/propLibrary/propList.txt'%YY_Desk(),'w')
        fi.writelines(infos)
    except:
        return
    finally:
        fi.close()
    cmds.confirmDialog(t = 'ÕûºÏµÀŸßÐÅÏ¢',m = 'µÀŸßÐÅÏ¢ÕûºÏÍê±Ï',b = 'OK')
    YY_ModelLibWin()
###======================================================
def pathList(path,shortName = '',lst = []):
    list = [f for f in os.listdir(path) if os.path.isdir('%s/%s'%(path,f))]
    if list:
        for li in list:
            if li == 'scenes':
                lst.append([shortName,path])
            else:
                pathList('%s/%s'%(path,li),'%s/%s'%(shortName,li),lst)
    return lst
###*****************************************************
def YY_PropList():
    fileName = '%s/propLibrary/propList.txt'%YY_Desk()
    listType = []#°ŽÀàÐÍ·ÖÀàÁÐ±í
    listProp = []#°ŽÏîÄ¿·ÖÀàÁÐ±í
    if os.path.isfile(fileName):
        f = file(fileName,'r')
        proInfos = f.readlines()
        f.close()
        for proInfo in proInfos:#¶ÁÈ¡Ã¿ÐÐÄÚÈÝ
            pros = proInfo.split()#·ÖžîÃ¿ÐÐÄÚÈÝ
            if len(pros) == 6:
                types = [t[0] for t in listType]#¶ÁÈ¡ÒÑŽæÔÚµÄÀàÐÍÁÐ±í
                props = [p[0] for p in listProp]#¶ÁÈ¡ÒÑŽæÔÚµÄÏîÄ¿ÁÐ±í
                if not pros[2] in types:
                    listType.append([pros[2],[pros[1],pros[0]]])#Èç¹ûÃ»ÓÐÖØžŽŒÓÈëÐÂµÄÀàÐÍ
                else:
                    index = types.index(pros[2])#»ñÈ¡ÖØžŽµÄ·ÖÀàÔÚÀàÐÍÁÐ±íÖÐµÄÎ»ÖÃ
                    indexStr = listType[index]#»ñÈ¡žÃÎ»ÖÃµÄÔ­ÀàÐÍÊýŸÝ
                    nameList = [n[0] for n in indexStr[1:]]#»ñÈ¡ÖØžŽ·ÖÀàµÄÃû³ÆÁÐ±í
                    if not pros[1] in nameList:
                        listType.pop(index)
                        indexStr.append([pros[1],pros[0]])
                        listType.insert(index,indexStr)
                if not pros[3] in props: 
                    listProp.append([pros[3],[pros[1],pros[0]]])#Èç¹ûÃ»ÓÐÖØžŽŒÓÈëÐÂµÄÏîÄ¿
                else:
                    indexP = props.index(pros[3])#»ñÈ¡ÖØžŽµÄÏîÄ¿ÔÚÏîÄ¿ÁÐ±íÖÐµÄÎ»ÖÃ
                    indexStrP = listProp[indexP]#»ñÈ¡žÃÎ»ÖÃµÄÔ­ÀàÐÍÊýŸÝ
                    nameListP = [p[0] for p in indexStrP[1:]]#»ñÈ¡ÖØžŽ·ÖÀàµÄÃû³ÆÁÐ±í
                    if not pros[1] in nameListP:
                        listProp.pop(indexP)
                        indexStrP.append([pros[1],pros[0]])
                        listProp.insert(indexP,indexStrP)
    return [listType,listProp]
def YY_TreeList(typ = 1):
    cmds.treeLister('YY_TreeList',e = True,add = [('ÀàÐÍ/%s'%t[0],'','fb.mod.propLibrary.YY_PicList(%s)'%t[1:]) for t in YY_PropList()[0]])#'YY_PicList(\'%s/propLibrary/%s/images\')'%(YY_Desk(),os.path.dirname(p)))
    cmds.treeLister('YY_TreeList',e = True,add = [('ÏîÄ¿/%s'%p[0],'','fb.mod.propLibrary.YY_PicList(%s)'%p[1:]) for p in YY_PropList()[1]])
    #cmds.treeLister('YY_TreeList',e = True,add = [(n,'','YY_PicList(\'%s/images\')'%a) for a,n,t in list])
###===================== Open Pics ======================================
def YY_OpenPicture(picPath = ''):
    if os.path.isfile(picPath):
        if re.match('^.+\.(jpg|jpeg|bmp|png|iff|tif)$',os.path.basename(picPath)):
            picWin = 'YY_PictureWinName'
            if cmds.window(picWin,q = True,ex = True):
                cmds.deleteUI(picWin)
            cmds.window(picWin,wh = [1024,768],t = 'ÍŒÆ¬Ô€ÀÀ',s = True)
            cmds.scrollLayout('scrollLyPic',cr = True,hst = 1000,vst = 1000,mcw = 1000)
            cmds.picture('opImage',image=picPath )
            cmds.showWindow(picWin)
###===================== Show Pics ====================================== 
def YY_PicList(picPaths = []):
    isSel = cmds.menuItem('addSelmen',q = True,cb = True)
    picList = cmds.gridLayout('YY_GridLY',q= True,ca = True)
    if picList and not isSel:
        cmds.deleteUI(cmds.gridLayout('YY_GridLY',q= True,ca = True))
    for name,picPath in picPaths:
        imageFloder = '%s/propLibrary/%s/images'%(YY_Desk(),os.path.dirname(picPath))
        sceneFloder = '%s/propLibrary/%s/scenes'%(YY_Desk(),os.path.dirname(picPath))
        filePath = '%s/propLibrary/%s/scenes/%s.mb'%(YY_Desk(),os.path.dirname(picPath),os.path.basename(picPath))
        if cmds.columnLayout('col%s'%os.path.basename(picPath),q = True,ex = True):
            cmds.deleteUI('col%s'%os.path.basename(picPath))
        if os.path.isdir(imageFloder):
            pics = [c for c in os.listdir(imageFloder) if re.match('^.+\.(jpg|jpeg|bmp|png|iff|tif)$',c) and c.split('.')[0] == os.path.basename(picPath)]
            if pics:
                p = pics[0]
                cmds.columnLayout('col%s'%os.path.basename(picPath),p = 'YY_GridLY',adj = True)
                if os.path.isfile('%s/%s'%(imageFloder,re.sub('\.','_Big.',p))):
                    bigp = re.sub('\.','_Big.',p)
                    cmds.iconTextButton(os.path.basename(picPath),i='%s/%s'%(imageFloder,p),w = 100,h = 80,c = 'fb.mod.propLibrary.YY_OpenPicture(picPath = \'%s/%s\')'%(imageFloder,bigp))
                else:
                    cmds.iconTextButton(os.path.basename(picPath),i='%s/%s'%(imageFloder,p),w = 100,h = 80,c = 'fb.mod.propLibrary.YY_OpenPicture(picPath = \'%s/%s\')'%(imageFloder,p))
                cmds.popupMenu()
                if os.path.isfile(filePath):
                    cmds.menuItem(l = 'µŒÈëµœ³¡Ÿ°',c = 'fb.mod.propLibrary.YY_ImportProp(filePath = \'%s\')'%filePath)
                else:
                    cmds.menuItem(l = 'µŒÈëµœ³¡Ÿ°',en = False)
                cmds.menuItem(l = 'Žò¿ª³¡Ÿ°ÎÄŒþŒÐ',c = 'import os;os.startfile(\'%s\')'%sceneFloder.replace("/","\\\\"))
                cmds.menuItem(l = 'Žò¿ªÍŒÆ¬ÎÄŒþŒÐ',c = 'import os;os.startfile(\'%s\')'%imageFloder.replace("/","\\\\"))
                #cmds.menuItem(l = 'ÁÐ³öÉÏÒ»²ãŒ°ËùÓÐÍŒÆ¬',c = 'os.startfile(\'%s\')'%imageFloder)
                cmds.text(h = 20,l = name,bgc = [1,1,1])
                cmds.setParent('..')
            '''else:
                cmds.popupMenu(p = 'YY_GridLY')
                if os.path.isfile(filePath):
                    cmds.menuItem(l = 'µŒÈëµœ³¡Ÿ°',c = 'fb.mod.propLibrary.YY_ImportProp(filePath = \'%s\')'%filePath)
                    cmds.menuItem('YY_ImportFile',e = True,c = 'fb.mod.propLibrary.YY_ImportProp(filePath = \'%s\')'%filePath)
                else:
                    cmds.menuItem(l = 'µŒÈëµœ³¡Ÿ°',en = False)
                    cmds.menuItem('YY_ImportFile',e = True,en = False)
                cmds.menuItem(l = 'Žò¿ª³¡Ÿ°ÎÄŒþŒÐ',c = 'os.startfile(\'%s\')'%sceneFloder)
                cmds.menuItem(l = 'Žò¿ªÍŒÆ¬ÎÄŒþŒÐ',c = 'os.startfile(\'%s\')'%imageFloder)
                cmds.menuItem('YY_OpenScenesFolder',e = True,en = True,c = 'os.startfile(\'%s\')'%sceneFloder)
                cmds.menuItem('YY_OpenImageFolder',e = True,en = True,c = 'os.startfile(\'%s\')'%imageFloder)'''
        elif os.path.isdir(sceneFloder):
            cmds.popupMenu(p = 'YY_GridLY')
            if os.path.isfile(filePath):
                cmds.menuItem(l = 'µŒÈëµœ³¡Ÿ°',c = 'fb.mod.propLibrary.YY_ImportProp(filePath = \'%s\')'%filePath)
                cmds.menuItem('YY_ImportFile',e = True,c = 'fb.mod.propLibrary.YY_ImportProp(filePath = \'%s\')'%filePath)
            else:
                cmds.menuItem(l = 'µŒÈëµœ³¡Ÿ°',en = False)
                cmds.menuItem('YY_ImportFile',e = True,en = False)
            cmds.menuItem(l = 'Žò¿ª³¡Ÿ°ÎÄŒþŒÐ',c = 'os.startfile(\'%s\')'%sceneFloder.replace("/","\\\\"))
            cmds.menuItem('YY_OpenScenesFolder',e = True,en = True,c = 'os.startfile(\'%s\')'%sceneFloder)
            cmds.menuItem('YY_OpenImageFolder',e = True,en = False)
        else:
            pass
###==================== Open Folder ================================
def YY_OpenFolder(folderPath = ''):
    os.startfile(folderPath)
###==================== Import =====================================
def YY_ImportProp(filePath = ''):
    bName = os.path.basename(filePath).split('.')[0]
    fileFolder = os.path.dirname(os.path.dirname(filePath))
    cmds.file(filePath,i = True,type = 'mayaBinary',ra = True,mnc = False,rdn = True,gr = True,gn = '%s_#'%bName,rpr = '%s_#'%bName)
    project = cmds.workspace(q = True,rd = True) + 'sourceimages'
    propImageFolder = fileFolder + '/sourceimages'
    if not os.path.isdir('%s/%s'%(project,bName)):
        os.makedirs('%s/%s'%(project,bName))
    for i in cmds.ls(type = 'file'):
        if re.match('(.+:)+.+',i):
            cmds.rename(i,'%s_%s'%(bName,i.split(':')[-1]))
    textureFiles = cmds.ls('%s*'%bName,type = 'file')# + [i for i in cmds.ls(type = 'file') if re.match('(.+:)+.+',i)]
    texturePics = []
    for t in textureFiles:
        fileTexturePath = cmds.getAttr('%s.fileTextureName'%t)
        textureBaseName = os.path.basename(fileTexturePath)
        texturePics.append(textureBaseName)
        cmds.setAttr('%s.fileTextureName'%t,'sourceimages/%s/%s'%(bName,textureBaseName),type = 'string')
    YY_SoDir(path = propImageFolder,copyPath = '%s/%s'%(project,bName),texs = [low.lower() for low in texturePics])
###==================== Add PropInfo ============================================
def YY_AddProp():
    propScenes = cmds.textScrollList('addPropTextSc',q = True,si = True)
    fileN = '%s/propLibrary/propList.txt'%YY_Desk()
    if os.path.isfile(fileN):
        fy = file(fileN,'r')
        proi = fy.readlines()
        fy.close()
    newProp = []
    for r in proi:
        if not r.split()[0].split('/')[0] in propScenes:
            newProp.append(r)
    for pro in propScenes:
        fileId = '%s/propLibrary/%s/fileInfo.txt'%(YY_Desk(),pro)
        fis = file(fileId ,'r')
        fs = fis.readlines()
        fis.close()
        newProp += ['%s/%s'%(str(pro),(g.replace('\r\n','')+'\r\n')) for g in fs]
    #print newProp
    newProp.sort()
    fyi = file(fileN,'w')
    fyi.writelines(newProp)
    fyi.close()
    YY_ModelLibWin()
###==================== Add PropInfo Window =====================================
def YY_AddPropWin():
    addWinName = 'addPropWin'
    if cmds.window(addWinName,q = True,ex = True):
        cmds.deleteUI(addWinName)
    cmds.window(addWinName,wh = (200,500))
    cmds.frameLayout('addPropScrolLY',l = 'ÎÄŒþÁÐ±í',bs = 'etchedOut')
    cmds.textScrollList('addPropTextSc',ams = True)
    cmds.button(l = 'ÌíŒÓÐÂµÀŸß',c = 'fb.mod.propLibrary.YY_AddProp()')
    cmds.showWindow(addWinName)
    cmds.window(addWinName,e = True,wh = (200,500))
    props = [r for r in os.listdir('%s/propLibrary'%YY_Desk()) if os.path.isdir('%s/propLibrary/%s/scenes'%(YY_Desk(),r)) and os.path.isfile('%s/propLibrary/%s/fileInfo.txt'%(YY_Desk(),r))]
    if props:
        cmds.textScrollList('addPropTextSc',e = True,a = props,sii = 1)
        
    #cmds.confirmDialog(t = 'ÌíŒÓµÀŸßÐÅÏ¢',m = 'µÀŸßÐÅÏ¢ÌíŒÓÍê±Ï',b = 'OK')
###==================== reFresh =====================================
def YY_Rcmd():
    fw = cmds.frameLayout('PicFrameLay',q = True,w = True)
    griNum = fw/100
    if griNum <1:
        griNum = 1
    cmds.gridLayout('YY_GridLY',e = True,nc = griNum,nr = 5000)
    #cmds.treeLister('YY_TreeList',q= True,po = True)
###==================== ModelLib Windown =====================================
def YY_ModelLibWin():
    winWH = [500,420]
    winName = 'ModelLibraryWin'
    if cmds.window(winName,q = True,ex = True):
        cmds.deleteUI(winName)
    cmds.window(winName,wh = winWH,t = 'ModelLibrary',mb = True)
    cmds.menu(l = 'ÎÄŒþ')
    cmds.menuItem(l = 'ÕûÀíÎÄŒþÐÅÏ¢',c = 'fb.mod.propLibrary.propList()')
    cmds.menuItem(l = 'ÌíŒÓµÀŸß',c = 'fb.mod.propLibrary.YY_AddPropWin()')
    cmds.menuItem('addSelmen',l = 'µþŒÓÑ¡Ôñ',cb = False)
    cmds.menu(l = 'Ë¢ÐÂ')
    cmds.menuItem(l = 'Ë¢ÐÂŽ°¿Ú',c = 'fb.mod.propLibrary.YY_ModelLibWin()')
    cmds.formLayout('YY_MLformLayout',nd=100)
    coLayoutTop = cmds.columnLayout(adj = True,cat = ['both',0],rs = 10)
    cmds.text(l = 'Ä£ÐÍµÀŸß¿â')
    cmds.separator()
    cmds.setParent('..')
    treeList = cmds.treeLister('YY_TreeList')
    #cmds.popupMenu()
    #cmds.menuItem('YY_OpenScenesFolder',l = 'Žò¿ª³¡Ÿ°ÎÄŒþŒÐ')
    #cmds.menuItem('YY_OpenImageFolder',l = 'Žò¿ªÍŒÆ¬ÎÄŒþŒÐ')
    scLy = cmds.frameLayout('PicFrameLay',l = 'ÍŒÆ¬',bs = 'etchedOut')
    cmds.scrollLayout('picScrolLY',cr = True,hst = 1000,vst = 1000,mcw = 1000,rc = 'fb.mod.propLibrary.YY_Rcmd()')
    cmds.gridLayout('YY_GridLY',cwh =(100,100))
    cmds.setParent('..')
    cmds.showWindow(winName)
    cmds.formLayout('YY_MLformLayout',e = True,
    af = [(coLayoutTop,'top',5),(coLayoutTop,'left',5),(coLayoutTop,'right',5),(treeList,'left',5),(treeList,'bottom',5),(scLy,'right',5),(scLy,'bottom',0)],
    ac = [(treeList,'top',0,coLayoutTop),(scLy,'top',0,coLayoutTop),(scLy,'left',0,treeList)],
    ap = [(treeList,'right',5,40)])
    if cmds.window('addPropWin',q = True,ex = True):
        cmds.deleteUI('addPropWin')
    YY_TreeList()
###==================== textures =================================================
def YY_AllTextures(texpath = '',jpgs = []):
    ts = os.listdir(texpath)
    for t in ts:
        txFullPath = os.path.join(texpath,t)
        if os.path.isdir(txFullPath):
            YY_AllTextures(txFullPath)
        else:
            if re.match('^.+\.(jpg|jpeg|bmp|png|iff|tif)$',t.lower()):
                jpgs.append(t)
    return jpgs
###==================== ClearUp FileTextures =====================================
def YY_CleraUpTextures():
    textures = cmds.ls(type = 'file')
    noFindPics = []
    for te in textures:
        fileTePath = cmds.getAttr('%s.fileTextureName'%te)
        if not re.match('^sourceimages.+\.(jpg|jpeg|bmp|png|iff|tif)$',fileTePath.lower()):
            teBName = os.path.basename(fileTePath)
            noFindPics.append(te)
    return noFindPics


