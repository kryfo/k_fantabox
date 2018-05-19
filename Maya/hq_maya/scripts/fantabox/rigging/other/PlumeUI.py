#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import sys
import os 
import logging 
from Qt import QtGui ,QtCore ,QtWidgets
from Qt.QtCompat import wrapInstance
import maya.OpenMayaUI as OpenMayaUI 
import avesPlumeJoint 
def getMayaWindow():
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr :
		return wrapInstance(long(ptr))
		


def run():
	global Buid_win
	try:
		if Buid_win.isVisible():
			Buid_win.close()
	except:
		pass
	Buid_win = plumeUi(parent = getMayaWindow())
	Buid_win.show


class plumeUi(QtWidgets.QDialog):
	
	plumeCs = avesPlumeJoint.AvesPlumePitchJiont()
	
	def __init__(self , parent = None):
		super(plumeUi ,self).__init__(parent)
		
		self.verticalLayout_q = QtWidgets.QVBoxLayout()
		self.verticalLayout_q.setContentsMargins(5,5,5,5)
		
		self.verticalLayout_1 = QtWidgets.QVBoxLayout()
		self.verticalLayout_1.setContentsMargins(5,5,5,5)
		
		
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()
		self.verticalLayout_2.setContentsMargins(5,5,5,5)
		
		self.jointLable = QtWidgets.QLabel('Please Create Joint :')
		self.jointLable.setToolTip(unicode('请创建并读入骨骼','gbk'))
		self.jointLable.setWhatsThis(unicode('1 创建骨骼：你可以点"Create Joint" 或自己创建骨骼再读入骨骼 ','gbk'))
		self.jointLine = QtWidgets.QLineEdit()
		self.pushButton_1 = QtWidgets.QPushButton('Create Joint')
		self.pushButton_1.setToolTip(unicode('创建骨骼','gbk'))
		self.pushButton_5 = QtWidgets.QPushButton('Readin Joint')
		self.pushButton_5.setToolTip(unicode('读入骨骼','gbk'))
		
		self.verticalLayout_2.addWidget(self.jointLable)
		self.verticalLayout_2.addWidget(self.jointLine)
		self.verticalLayout_2.addWidget(self.pushButton_1)
		self.verticalLayout_2.addWidget(self.pushButton_5)
		
		self.verticalLayout_3 = QtWidgets.QVBoxLayout()
		self.verticalLayout_3.setContentsMargins(5,5,5,5)
		
		self.jointLable_1 = QtWidgets.QLabel('Create Middle Joint :')
		self.jointLable_1.setToolTip(unicode('创建中间羽毛骨骼','gbk'))
		self.jointLable_1.setWhatsThis(unicode('2 创建中间骨骼：羽毛中间骨骼的多少 ','gbk'))
		self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_1.setContentsMargins(5,5,5,5)
		
		self.jointLable_num = QtWidgets.QLabel('Joint Number :')
		self.lcdNum = QtWidgets.QLCDNumber()
		self.slider = QtWidgets.QSlider()
		self.slider.setMinimum(1)
		self.slider.setMaximum(20)
		self.slider.setOrientation(QtCore.Qt.Horizontal)
		
		self.horizontalLayout_1.addWidget(self.jointLable_num)
		self.horizontalLayout_1.addWidget(self.lcdNum)
		self.horizontalLayout_1.addWidget(self.slider)
		
		self.verticalLayout_3.addWidget(self.jointLable_1)
		self.verticalLayout_3.addLayout(self.horizontalLayout_1)
		
		self.verticalLayout_4 = QtWidgets.QVBoxLayout()
		self.verticalLayout_4.setContentsMargins(5,0,5,5)
		
		self.pushButton_2 = QtWidgets.QPushButton('Create Bird Plumage')
		self.pushButton_2.setToolTip(unicode('创建鸟类羽毛','gbk'))
		
		self.verticalLayout_4.addWidget(self.pushButton_2 )
		
		self.verticalLayout_5 = QtWidgets.QVBoxLayout()
		self.verticalLayout_5.setContentsMargins(5,0,5,5)
		
		self.jointLable_2 = QtWidgets.QLabel('Multilayer Joint :')
		self.jointLable_2.setToolTip(unicode('创建多层骨骼','gbk'))
		self.jointLable_2.setWhatsThis(unicode('3 创建多层骨骼：','gbk'))
		self.pushButton_3 = QtWidgets.QPushButton('Add Joint')
		self.pushButton_3.setToolTip(unicode('添加骨骼','gbk'))
		self.pushButton_4 = QtWidgets.QPushButton('Create')
		self.pushButton_4.setToolTip(unicode('创建','gbk'))
		
		self.verticalLayout_5.addWidget(self.jointLable_2 )
		self.verticalLayout_5.addWidget(self.pushButton_3 )
		self.verticalLayout_5.addWidget(self.pushButton_4 )
		
		
		self.verticalLayout_1.addLayout(self.verticalLayout_2)
		self.verticalLayout_1.addLayout(self.verticalLayout_3)
		self.verticalLayout_1.addLayout(self.verticalLayout_4)
		self.verticalLayout_1.addLayout(self.verticalLayout_5)
		
		
		
		self.groupBox = QtWidgets.QGroupBox()
		
		self.groupBox.setMinimumSize(QtCore.QSize(300, 325))
		self.groupBox.setMaximumSize(QtCore.QSize(300, 325))
		
		self.groupBox.setLayout(self.verticalLayout_1)
		
		self.verticalLayout_q.addWidget(self.groupBox)

		
		self.setLayout(self.verticalLayout_q)
		
		self.makeConnections()
		self.setWindowTitle("BIRD PLUMAGE UI")
		
		self.resize(310, 335)
		self.setMinimumSize(QtCore.QSize(310, 335))
		self.setObjectName('BIRD UI')
		self.initUiState()
		self.show()
		
	def makeConnections(self):
		self.pushButton_1.clicked.connect(self.createJoint)
		self.pushButton_2.clicked.connect(self.biud)
		self.pushButton_3.clicked.connect(self.addCreateJoint)
		self.pushButton_4.clicked.connect(self.addBiud)
		self.pushButton_5.clicked.connect(self.readin)

		self.slider.valueChanged.connect(self.lcdNum.display)
		
	def initUiState(self):
		
		self.jointLine.setEnabled(False)
		self.jointLine.setPlaceholderText('Joint Name')
		self.slider.setValue(6)
		self.lcdNum.display(6)
		
	def createJoint(self):
		plumeUi.plumeCs._biudPitchJoint()
		name = [a.name() for a in plumeUi.plumeCs.leftList]
		txt = ' , '.join(name)
		self.jointLine.setText('name: %s'%(txt))
	
	
	def biud(self):
		num_n = self.slider.value()
		txt1 = self.jointLine.text()
		if txt1 == 'Joint Name' or not txt1:
			logger.error('not obj')
			return 
		
		plumeUi.plumeCs.biud(num_n)
	
	
	def addCreateJoint(self):
		plumeUi.plumeCs._addBiudPitchJoint()
		
	
	def addBiud(self):
		plumeUi.plumeCs.addBuid()
		
	def readin(self):
		plumeUi.plumeCs.readinJoint()
		name = [a.name() for a in plumeUi.plumeCs.leftList]
		txt = ' , '.join(name)
		self.jointLine.setText('name: %s'%(txt))
		
		
		

def PlumeUI():
#if __name__=='__main__':

    run()



