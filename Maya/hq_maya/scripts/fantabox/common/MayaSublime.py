#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:xusijian
#--date--:2017-06-08
from maya.cmds import commandPort
from maya.cmds import warning
def MayaSublime_open():
    try:
        commandPort(name=':7001', sourceType='mel')
        commandPort(name=':7002', sourceType='python')
        print "port has successfully connected ",
    except:
        warning('port has already connected')
def MayaSublime_close():
    try:
        commandPort(name=':7001', close=True)
        print "port:7001 has successfully disconnected ",
    except:
        warning('Could not close port 7001 (maybe it is not opened yet)')
    try:
        commandPort(name=':7002', close=True)
        print "port:7002 has successfully disconnected ",
    except:
        warning('Could not close port 7002 (maybe it is not opened yet)')
    
def MayaSublime_UI():
    from maya.cmds import window
    from maya.cmds import deleteUI
    from maya.cmds import columnLayout
    from maya.cmds import button
    from maya.cmds import showWindow
    if window('MayaSublime_UIwd',ex=True):
        deleteUI('MayaSublime_UIwd',wnd=True)
    window('MayaSublime_UIwd',t='MayaSublime')
    columnLayout(adj=True,w=240)
    button(l='connect MayaSublime', c= 'fb.com.MayaSublime_open()',h=50,ann="")
    button(l='break MayaSublime',c='fb.com.MayaSublime_close()',h=50,ann="")
    showWindow()