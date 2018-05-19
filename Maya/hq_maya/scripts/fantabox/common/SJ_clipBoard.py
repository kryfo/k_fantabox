#coding=utf-8
import ctypes
from maya.cmds import warning
def getClipboard(): 
    u'''从剪切板中获得字符串'''
    user32=ctypes.WinDLL('user32.dll')
    user32.OpenClipboard(0) 
    getdata=user32.GetClipboardData(13) 
    dataout=ctypes.c_wchar_p(getdata) 
    user32.CloseClipboard()
    return dataout.value
    
    
def setClipboard(mystr):
    u'''把字符串放到剪切板中,成功返回1，失败返回0'''
    user32=ctypes.WinDLL('user32.dll')
    kernel32=ctypes.WinDLL('kernel32.dll')
    Enmystr=mystr.encode('utf-16')
    Enmystr=Enmystr[2:]+b'\0\0'
    Enmystrs=ctypes.c_char_p(Enmystr)
    user32.OpenClipboard(0)
    user32.EmptyClipboard()
    kernel32.GlobalAlloc.argtypes=[ctypes.c_uint32,ctypes.c_uint32]
    try:
        globalAll=kernel32.GlobalAlloc(0,len(Enmystr))
        globalAll=ctypes.c_void_p(globalAll)
        ctypes.memmove(globalAll,Enmystrs,len(Enmystr))
        feedback=user32.SetClipboardData(13,globalAll) # 13->unicode
    except:
        warning(u"无法写入剪切板！！")
        feedback=0
    finally:
        user32.CloseClipboard()
    if feedback==0:
        return 0
    else:
        return 1
if __name__=="__main__":
    setClipboard("test")