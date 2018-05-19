import maya.cmds as cc
def k015_check_displink():
	
	k_return=[]

	k_dxdis=[]
	k_container = cc.ls(type='container')
	k_dxs = [a for a in k_container if 'dx11Shader_ast' in a]
	for k_dx in k_dxs:
		k_dxfiles=cc.container(k_dx,q=1,nodeList=1)
		for k_dxfile in k_dxfiles:
			k_dxtex=cc.nodeType(k_dxfile)
			if k_dxtex=='displacementShader':
				k_dxdis.append(k_dxfile)


	k_lsdisa=cc.ls(type='displacementShader')

	k_lsdiss=list(set(k_lsdisa).difference(set(k_dxdis)))

	for k_lsdis in k_lsdiss:
		k_listdis=cc.listConnections(k_lsdis,type='shadingEngine',d=1)
		if k_listdis :pass
		else:k_return.append(k_lsdis)

	return k_return
