# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/k/k_pyside/weimeng/checkNodeForMayaReplyWin.ui'
#
# Created: Thu Jun 15 12:01:38 2017
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
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(391, 672)
        self.k_centralwidget = QWidget(MainWindow)
        self.k_centralwidget.setObjectName("k_centralwidget")
        self.verticalLayout = QVBoxLayout(self.k_centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBox = QToolBox(self.k_centralwidget)
        self.toolBox.setObjectName("toolBox")
        self.k_page = QWidget()
        self.k_page.setGeometry(QRect(0, 0, 373, 628))
        self.k_page.setObjectName("k_page")
        self.verticalLayout_2 = QVBoxLayout(self.k_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox.addItem(self.k_page, "")
        self.verticalLayout.addWidget(self.toolBox)
        MainWindow.setCentralWidget(self.k_centralwidget)
        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        try:
            MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None,QApplication.UnicodeUTF8))
            self.toolBox.setItemText(self.toolBox.indexOf(self.k_page), QApplication.translate("MainWindow", "无发现不符合规定节点", None,QApplication.UnicodeUTF8))
        except:
            MainWindow.setWindowTitle(QApplication.translate("MainWindow", "MainWindow", None))
            self.toolBox.setItemText(self.toolBox.indexOf(self.k_page), QApplication.translate("MainWindow", "无发现不符合规定节点", None))
