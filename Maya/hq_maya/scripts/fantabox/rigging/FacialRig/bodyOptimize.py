from shuai_OptimizeOption import optimizeWin
import maya.cmds as mc
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtCompat import wrapInstance
from Qt.QtWidgets import *
from maya import OpenMayaUI as omui
#from shiboken import wrapInstance
class bodyOptimize():
	def __init__(self):
		if(mc.window('shuaiAdvOptimizeWin',ex=1)):
		    mc.deleteUI('shuaiAdvOptimizeWin')
		    
		self.mayaMainWindowPtr = omui.MQtUtil.mainWindow()
		self.QMayaWindow= wrapInstance(long(self.mayaMainWindowPtr))
	def setupUI(self):		
		self.QOptimizeWin=QMainWindow(self.QMayaWindow)
		self.optimize_ui=optimizeWin()
		self.optimize_ui.setupUI(self.QOptimizeWin)
		self.QOptimizeWin.show()