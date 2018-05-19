import pymel.core as pm
import random
def SJ_randomChoice():
    sels =pm.ls(sl=1)
    for sel in sels:
        try:
            selshape = sel.getShape()
        except:
            selshape =None
        if selshape!=None:
            sg = pm.listConnections(selshape,s=0,type="shadingEngine")[0]
            choicesels= pm.listHistory(sg,ac=1,type="choice")
            if choicesels!=[]:
                for  choicesel in choicesels:
                    filesel = pm.listConnections(choicesel,s=0,type="file")
                    if filesel!=[]:
                        num = len(filesel[0].listAttr(ud=1))-1
                        value= random.randint(0,num)
                        conjudges = pm.listConnections(choicesel+".selector",c=1)
                        if conjudges ==[]:
                            pm.setAttr(choicesel+".selector",value)
                            print str(sel)+">>>>>"+str(value),
                        else:
                            pm.disconnectAttr(conjudges[0])
                            pm.setAttr(choicesel+".selector",value)
                            print str(sel)+">>>>>"+str(value),
                    else:
                        pm.warning("no choiceFileNode!!")
            else:
                pm.warning("no choiceNode!!")