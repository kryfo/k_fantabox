from shuai_FaceOptimizeOption import faceOptimizeWin
import maya.cmds as mc
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtCompat import wrapInstance
from Qt.QtWidgets import *
from maya import OpenMayaUI as omui
#from shiboken import wrapInstance
class faceOptimize():
	def __init__(self):
		if(mc.window('shuaiAdvOptimizeWin',ex=1)):
		    mc.deleteUI('shuaiAdvOptimizeWin')
		    
		self.mayaMainWindowPtr = omui.MQtUtil.mainWindow()
		self.QMayaWindow= wrapInstance(long(self.mayaMainWindowPtr))
	def setupUI(self):		
		self.QFaceOptimizeWin=QMainWindow(self.QMayaWindow)
		self.faceOptimize_ui=faceOptimizeWin()
		self.faceOptimize_ui.setupUI(self.QFaceOptimizeWin)
		self.QFaceOptimizeWin.show()