#!/usr/bin/python
#coding=utf-8
#--author--:liushengyao
#--date--:2017-08-30
from maya.cmds import lsUI,deleteUI
def deleteNoneUI():
    u'''
    {'load':'maya_clean','defaultOption':1,'CNname':'关闭所有窗口'}
    '''
    allUI = lsUI(wnd = 1)
    for w in allUI:
        if w=="MayaWindow" or w=="nexFloatWindow":
            continue
        deleteUI(w)
if __name__=="__main__":
    deleteNoneUI()