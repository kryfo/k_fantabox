import os
import sys
__author__ = 'xusj'
def pySource(filePath):
    myFile = os.path.basename(filePath)
    dir = os.path.dirname(filePath)
    fileName = os.path.splitext(myFile)[0]
    if( os.path.exists( dir ) ):
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
            if not pathfound:
                sys.path.append( dir )
        exec('import ' +fileName) in globals()
        exec( 'reload( ' + fileName + ' )' ) in globals()
    return fileName