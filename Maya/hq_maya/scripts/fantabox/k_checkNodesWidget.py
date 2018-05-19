# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/work/7_0616_CheckNode/bak/checkNodes/k_checkNodesWidget.ui'
#
# Created: Thu Jun 22 17:00:56 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *

class Ui_checkNodesWindow(object):
    def setupUi(self, checkNodesWindow):
        checkNodesWindow.setObjectName("checkNodesWindow")
        checkNodesWindow.resize(379, 817)
        self.centralwidget =  QWidget(checkNodesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout =  QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea =  QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents =  QWidget()
        self.scrollAreaWidgetContents.setGeometry( QRect(0, 0, 359, 743))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 =  QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.kframe_3 =  QFrame(self.centralwidget)
        self.kframe_3.setFrameShape( QFrame.Box)
        self.kframe_3.setFrameShadow( QFrame.Raised)
        self.kframe_3.setObjectName("kframe_3")
        self.verticalLayout.addWidget(self.kframe_3)
        self.horizontalLayout =  QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.doIt_Button =  QPushButton(self.centralwidget)
        self.doIt_Button.setMinimumSize( QSize(0, 30))
        font =  QFont()
        font.setFamily("AcadEref")
        font.setPointSize(10)
        self.doIt_Button.setFont(font)
        self.doIt_Button.setObjectName("doIt_Button")
        self.horizontalLayout.addWidget(self.doIt_Button)
        self.close_Button =  QPushButton(self.centralwidget)
        self.close_Button.setMinimumSize( QSize(0, 30))
        font =  QFont()
        font.setFamily("AcadEref")
        font.setPointSize(10)
        self.close_Button.setFont(font)
        self.close_Button.setObjectName("close_Button")
        self.horizontalLayout.addWidget(self.close_Button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        checkNodesWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(checkNodesWindow)
        QMetaObject.connectSlotsByName(checkNodesWindow)

    def retranslateUi(self, checkNodesWindow):
        try:
            checkNodesWindow.setWindowTitle( QApplication.translate("checkNodesWindow", "检查工具面板 ", None,  QApplication.UnicodeUTF8))
            self.doIt_Button.setText( QApplication.translate("checkNodesWindow", "执行", None,  QApplication.UnicodeUTF8))
            self.close_Button.setText( QApplication.translate("checkNodesWindow", "取消", None,  QApplication.UnicodeUTF8))
        except:
            checkNodesWindow.setWindowTitle( QApplication.translate("checkNodesWindow", "检查工具面板 ", None))
            self.doIt_Button.setText(QApplication.translate("checkNodesWindow", "执行", None))
            self.close_Button.setText(QApplication.translate("checkNodesWindow", "取消", None))


import k_checkNodesWidget_rc
