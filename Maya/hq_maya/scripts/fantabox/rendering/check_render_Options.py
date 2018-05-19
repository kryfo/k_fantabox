#!/usr/bin/python
# -*- coding: utf-8 -*-
#--author--:huwenbin,xusijian
#--date--:2017-08-24
import maya.cmds as cmds
from fantabox.rendering.check_render_Options import *
def check_render_Options():
    u'''
    {'load':'maya_Check','defaultOption':1,'CNname':检查Arnold与yeti渲染设置是否正确'}
    '''
    render_Options=[u"defaultRenderGlobals.preMel",u"defaultRenderGlobals.poam",u"defaultRenderGlobals.prlm",u"defaultRenderGlobals.polm",u"defaultRenderGlobals.preRenderMel",u"defaultRenderGlobals.pom"]    
    other_render_Options=[]
    for i in range(len(render_Options)):
        render_Options_name=cmds.getAttr(render_Options[i])
        if render_Options_name!=None:
            other_render_Options.append(render_Options[i])
    other_render_Options+=check_render_Options_judges(u"defaultArnoldRenderOptions",u"force_scene_update_before_IPR_refresh",1)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldRenderOptions",u"force_texture_cache_flush_after_render",1)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldRenderOptions",u"use_existing_tiled_textures",1)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldRenderOptions",u"textureMaxMemoryMB",4096)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldRenderOptions",u"abortOnError",1)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldDriver",u"halfPrecision",1)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldDriver",u"autocrop",1)
    other_render_Options+=check_render_Options_judges(u"defaultArnoldDisplayDriver",u"aiTranslator","maya")   
    other_render_Options+=check_render_Options_judges(u"defaultArnoldDriver",u"aiTranslator","exr")
    return list(set(other_render_Options))
def check_render_Options_judges(nodes,attrs,values):
    namedicts= {u"defaultArnoldRenderOptions.force_scene_update_before_IPR_refresh":u"为加载渲染IPR前清理缓存功能！！",
                u"defaultArnoldRenderOptions.force_texture_cache_flush_after_render":u"为加载渲染前清理缓存功能！！",
                u"defaultArnoldRenderOptions.use_existing_tiled_textures":u"未加载使用tx格式功能！！",
                u"defaultArnoldRenderOptions.abortOnError":"请务打开忽略渲染错误选项",
                u"defaultArnoldRenderOptions.textureMaxMemoryMB":u"最大缓存空间设置过小！！",
                u"defaultArnoldDriver.halfPrecision":u"halfPrecision属性未加载！！",
                u"defaultArnoldDriver.autocrop":u"autocrop属性未加载！！",
                u"defaultArnoldDisplayDriver.aiTranslator":u"前台渲染格式设置错误！！",
                u"defaultArnoldDriver.aiTranslator":u"未将渲染输出格式设置为exr！！",
                u"defaultRenderGlobals.preMel":u"渲染预处理脚本设置不正确！！",
                }
    if cmds.objExists(nodes):
        if attrs!="textureMaxMemoryMB":
            if cmds.getAttr(nodes+"."+attrs)!=values:
                if namedicts.get(nodes+"."+attrs)!=None:
                    return [namedicts.get(nodes+"."+attrs)]
                else:
                    return [nodes+"."+attrs]
            else:
                return []
        else:
            if cmds.getAttr(nodes+"."+attrs)<=values:
                if namedicts.get(nodes+"."+attrs)!=None:
                    return [namedicts.get(nodes+"."+attrs)]
                else:
                    return [nodes+"."+attrs]
            else:
                return []
    else:
        return [nodes+u"节点不存在！！"]
if __name__=="__main__":
    print check_render_Options()