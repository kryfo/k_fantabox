#!/usr/bin/python
#coding=utf-8
#--author--:dengtao
#--date--:2017-08-29
from maya.cmds import unknownPlugin
def k_check_unPlugin():
    k_unknownPlugins=unknownPlugin(q=1,l=1)
    if k_unknownPlugins!=None:
        for k_unknownPlugin in k_unknownPlugins:
            unknownPlugin(k_unknownPlugin,r=1)
    return k_unknownPlugins