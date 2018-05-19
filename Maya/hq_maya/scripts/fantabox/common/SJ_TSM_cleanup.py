import maya.cmds as cmds
def TSM_menuCleanup():
    scriptnodes = cmds.ls(type="script")
    errorcol = []
    for scriptnode in scriptnodes:
        if scriptnode.find('TSM2FKIKSwitch')!=-1:
            try:
                cmds.delete(scriptnode)
            except:
                errorcol.append(scriptnode)
    return errorcol