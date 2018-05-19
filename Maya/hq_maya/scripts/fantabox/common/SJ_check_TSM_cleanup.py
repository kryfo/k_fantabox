import maya.cmds as cmds
def SJ_check_TSM_cleanup():
    '''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查TSM残留script节点'}
    '''
    scriptnodes = cmds.ls(type="script")
    tsmScriptNode = []
    for scriptnode in scriptnodes:
        if scriptnode.find('TSM2FKIKSwitch')!=-1:
            tsmScriptNode.append(scriptnode)
    return tsmScriptNode

def TSM_menuCleanup(nodecols):
    for nodecol in nodecols:
        try:
            cmds.delete(nodecol)
        except:
            pass