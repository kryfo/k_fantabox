import ctypes.wintypes
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, buf)
def myDocPathwdUI():
    hostname = buf.value
    arnoldpath = []
    modulespath= hostname+"\maya\modules"
    modulefile = open(modulespath+ r"\foma_plugins.mod", 'r')
    modulelines = modulefile.readlines()
    modulefile.close()
    for moduleline in modulelines:
        if moduleline.find("+ MAYAVERSION:2015 mtoa")!=-1:
            try:
                Arnoldname = moduleline[moduleline.find("Arnold_"):][:-10]
            except:
                Arnoldname=[]
            if Arnoldname!=[]:
                if Arnoldname.find("O:/hq_tool/Maya/Arnold/")!=-1:
                    arnoldpath.append(r"O:/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
                else:
                    if Arnoldname.find("C:/hq_tool/Maya/Arnold/")!=-1:
                        arnoldpath.append(r"C:/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")
                    else:
                        arnoldpath.append(r"//10.99.1.2/digital/film_project/hq_tool/Maya/Arnold/"+Arnoldname+r"Maya2015/scripts")   
    return arnoldpath[0][:arnoldpath[0].find('hq_tool')]

