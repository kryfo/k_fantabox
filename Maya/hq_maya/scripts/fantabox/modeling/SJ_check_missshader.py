from fantabox.modeling.SJ_faceShaderMod import *
def SJ_check_missshader(checknum):
    u'''
    {'load':'maya_Check','defaultOption':1,'CNname':'检查丢失材质模型'}
    '''
    if checknum in range(5,8):
        return ck_missshader(checknum)
    else:
        return ck_missshader()
