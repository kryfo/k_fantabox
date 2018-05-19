import os
def initbuilder_buildinit(subdirs,invaliddir=[]):
    invaliddirs =invaliddir+["bak","AnimLib","animLib"]
    subtexts = []
    subfiles =[b for b in  os.listdir(subdirs) if b.split(".")[-1]=="py" or len(b.split('.'))==1]
    for subfile in subfiles:
        subpath = subdirs+"/"+ subfile
        if len(subfile.split('.'))==2:
            filenames = subfile.split('.')[0]
            if filenames !="__init__" and filenames not in invaliddirs:
                subtexts.append("from "+filenames+" import *")
        else:
            if subfile not in invaliddirs:
                subtexts.append("import "+subfile)
    return subtexts
def initbuilder_writeinit(path,texts):
    fl=open(path+'/__init__.py', 'w')
    for subtext in texts:
        fl.write(subtext)
        fl.write("\n")
    fl.close()
def initbuilder_updateInitFile(path):
    subpaths=[]
    maindirs = [a for a in os.listdir(path) if len(a.split("."))==1]
    mainpys = [a for a in os.listdir(path) if a.split(".")[-1]=="py"] 
    for maindir in maindirs:
        subdirs = path+"/"+maindir
        subtexts = initbuilder_buildinit(subdirs)
        initbuilder_writeinit(subdirs,subtexts)
    if mainpys!=[]:
        subtexts = initbuilder_buildinit(path)
        initbuilder_writeinit(path,subtexts)
    return "done!"