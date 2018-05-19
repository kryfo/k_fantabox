#!/usr/bin/env python
#coding=cp936
#coding=utf-8
import maya.cmds as mc
import maya.mel as mm
from maya import OpenMayaUI as omui
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *
import faceOptimizeCommands
from faceOptimize_ui import Ui_shuaiFaceOptimizeWin
class faceOptimizeWin(Ui_shuaiFaceOptimizeWin):
    def __init__(self):
        self.allCBoxes=["shuaiChangeCtrls_checkBox","addTougueCtrls_checkBox","shuaiEyeBallCtrls_checkBox","shuaiAddScaleConstraint_checkBox","shuaiLockAndHideVisibility_checkBox"]
    def setupUI(self,shuaiFaceOptimizeWin):
        Ui_shuaiFaceOptimizeWin.setupUi(self,shuaiFaceOptimizeWin)
        self.optimizeButton.clicked.connect(self.optimize_ButtonCmd)
        self.selectAll_checkBox.stateChanged.connect(self.selectAll_checkBoxCmd)
        self.shuaiChangeCtrls_checkBox.stateChanged.connect(self.shuaiChangeCtrls_checkBoxCmd)
        self.addTougueCtrls_checkBox.stateChanged.connect(self.addTougueCtrls_checkBoxCmd)
        self.shuaiEyeBallCtrls_checkBox.stateChanged.connect(self.shuaiEyeBallCtrls_checkBoxCmd)
        self.shuaiAddScaleConstraint_checkBox.stateChanged.connect(self.shuaiAddScaleConstraint_checkBoxCmd)
        self.shuaiLockAndHideVisibility_checkBox.stateChanged.connect(self.shuaiLockAndHideVisibility_checkBoxCmd)
    
    def selectAll_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            for i in self.allCBoxes:
                if not eval('self.%s.isChecked()'%i):
                    eval('self.%s.setChecked(True)'%i)
    def shuaiChangeCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiChangeCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def addTougueCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.addTougueCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiEyeBallCtrls_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiEyeBallCtrls_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiAddScaleConstraint_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiAddScaleConstraint_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def shuaiLockAndHideVisibility_checkBoxCmd(self):
        CheckState=self.selectAll_checkBox.isChecked()
        if CheckState:
            if not self.shuaiLockAndHideVisibility_checkBox.isChecked():
                self.selectAll_checkBox.setChecked(False)
    def optimize_ButtonCmd(self):
        self.textList=['�����������ת��������','�����ͷ������','������������','�������Լ��','��������visbility����']
        self.optimizeCmds=['faceOptimizeCommands.ChangeToCurve()','faceOptimizeCommands.adv_tongueCtrl()','faceOptimizeCommands.adv_EyeCtrl()','faceOptimizeCommands.face_Scale()','faceOptimizeCommands.adv_hideVisiblity()']
        ErrorNum=0
        print "\n==========================================��ʼ�Ż�==========================================\n"
        for i in range(len(self.optimizeCmds)):
            if eval('self.%s.isChecked()'%self.allCBoxes[i]):
                errorString=self.optimize(i)
                if not errorString==None:
                    ErrorNum+=1
                    print ('����'+str(ErrorNum)+':')
                    print '-------------------------------------------------------------------------------------------'
                    print ('****** \" %s \" ʱ��������ϸ�鿴����Ĵ�����ʾ����******'%self.textList[i])
                    print errorString
                    print '-------------------------------------------------------------------------------------------\n'
        print "==========================================�Ż�����==========================================\n"
        if ErrorNum==0:
            mc.warning('<<--��ϲ��ȫ���Ż��ɹ�����-->>')
        else:
            mc.warning('<<--�����У�%d�����Ż�ʧ�ܣ���򿪽ű��༭����Script Editor���鿴��ϸʧ��ԭ��-->>'%ErrorNum)
    def optimize(self,CBoxIndex):
        try:
            eval('%s'%self.optimizeCmds[CBoxIndex])
        except StandardError as ErrorString:
            return ErrorString

