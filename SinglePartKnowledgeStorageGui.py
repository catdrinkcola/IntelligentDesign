# -*- coding: utf-8 -*-
# FreeCAD script for the commands of the FilletExpert workbench creation
# (c) 2021 Daohao Guo

# from PyQt5 import QtCore,QtGui
# from PySide2 import QtCore, QtGui
from PySide import QtCore, QtGui
import FreeCAD
import FreeCADGui
from PySide.QtCore import Slot
import Part
import os
import time
import sys

__knowledge_storage_dir__ = os.path.dirname(__file__)

# Task Panel creation: the task panel has to have:
#   1. a widget called self.form
#   2. reject and accept methods (if needed)
class SinglePartKnowledgeStoragePanel:
    def __init__(self):
        self.selection = FreeCADGui.Selection.getSelection()
        self.form = FreeCADGui.PySideUic.loadUi(__knowledge_storage_dir__ + "/UIs/KnowledgeStoragePanel.ui")
        self.mainLayout = QtGui.QGridLayout(self.form.scrollArea)
        self.additionLineEditCnt = 0
        self.scrollAreaRowCnt = 7

        # Item1
        self.keyLabel1 = QtGui.QLabel('模型名称')
        # self.keyLabel1.setMinimumWidth(20)
        # self.keyLabel1.setMinimumHeight(20)
        self.valueLineEdit1 = QtGui.QLineEdit()
        self.valueLineEdit1.setMinimumWidth(50)
        self.valueLineEdit1.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel1, 0, 0)
        self.mainLayout.addWidget(self.valueLineEdit1, 0, 1)

        # Item2
        self.keyLabel2 = QtGui.QLabel('最大长度')
        # self.keyLabel2.setMinimumWidth(20)
        # self.keyLabel2.setMinimumHeight(20)
        self.valueLineEdit2 = QtGui.QLineEdit()
        self.valueLineEdit2.setMinimumWidth(50)
        self.valueLineEdit2.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel2, 1, 0)
        self.mainLayout.addWidget(self.valueLineEdit2, 1, 1)

        # Item3
        self.keyLabel3 = QtGui.QLabel('最大宽度')
        # self.keyLabel3.setMinimumWidth(20)
        # self.keyLabel3.setMinimumHeight(20)
        self.valueLineEdit3 = QtGui.QLineEdit()
        self.valueLineEdit3.setMinimumWidth(50)
        self.valueLineEdit3.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel3, 2, 0)
        self.mainLayout.addWidget(self.valueLineEdit3, 2, 1)

        # Item4
        self.keyLabel4 = QtGui.QLabel('最大高度')
        # self.keyLabel4.setMinimumWidth(20)
        # self.keyLabel4.setMinimumHeight(20)
        self.valueLineEdit4 = QtGui.QLineEdit()
        self.valueLineEdit4.setMinimumWidth(50)
        self.valueLineEdit4.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel4, 3, 0)
        self.mainLayout.addWidget(self.valueLineEdit4, 3, 1)

        # Item5
        self.keyLabel5 = QtGui.QLabel('模型类型')
        # self.keyLabel5.setMinimumWidth(20)
        # self.keyLabel5.setMinimumHeight(20)
        self.valueLineEdit5 = QtGui.QLineEdit()
        self.valueLineEdit5.setMinimumWidth(50)
        self.valueLineEdit5.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel5, 4, 0)
        self.mainLayout.addWidget(self.valueLineEdit5, 4, 1)

        # Item6
        self.keyLabel6 = QtGui.QLabel('零件材料')
        # self.keyLabel6.setMinimumWidth(20)
        # self.keyLabel6.setMinimumHeight(20)
        self.valueLineEdit6 = QtGui.QLineEdit()
        self.valueLineEdit6.setMinimumWidth(50)
        self.valueLineEdit6.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel6, 5, 0)
        self.mainLayout.addWidget(self.valueLineEdit6, 5, 1)

        # Item7
        self.keyLabel7 = QtGui.QLabel('生产公司')
        # self.keyLabel7.setMinimumWidth(20)
        # self.keyLabel7.setMinimumHeight(20)
        self.valueLineEdit7 = QtGui.QLineEdit()
        self.valueLineEdit7.setMinimumWidth(50)
        self.valueLineEdit7.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel7, 6, 0)
        self.mainLayout.addWidget(self.valueLineEdit7, 6, 1)

        # Item8
        # self.keyLabel8 = QtGui.QLabel('制造工艺')
        # # self.keyLabel8.setMinimumWidth(20)
        # # self.keyLabel8.setMinimumHeight(20)
        # self.valueLineEdit8 = QtGui.QLineEdit()
        # self.valueLineEdit8.setMinimumWidth(50)
        # self.valueLineEdit8.setMinimumHeight(20)
        # self.mainLayout.addWidget(self.keyLabel8, 7, 0)
        # self.mainLayout.addWidget(self.valueLineEdit8, 7, 1)

        # addItemButton
        self.addItemButton = QtGui.QPushButton('+')
        self.addItemButton.setMinimumWidth(50)
        self.addItemButton.setMinimumHeight(20)
        self.mainLayout.addWidget(self.addItemButton, 7, 0, 2, 1)

        self.keyLineEdit9 = QtGui.QLineEdit()
        self.keyLineEdit9.setMaximumWidth(50)
        self.keyLineEdit9.setMinimumHeight(20)
        self.valueLineEdit9 = QtGui.QLineEdit()
        self.valueLineEdit9.setMinimumWidth(50)
        self.valueLineEdit9.setMinimumHeight(20)

        self.keyLineEdit10 = QtGui.QLineEdit()
        self.keyLineEdit10.setMaximumWidth(50)
        self.keyLineEdit10.setMinimumHeight(20)
        self.valueLineEdit10 = QtGui.QLineEdit()
        self.valueLineEdit10.setMinimumWidth(50)
        self.valueLineEdit10.setMinimumHeight(20)

        self.keyLineEdit11 = QtGui.QLineEdit()
        self.keyLineEdit11.setMaximumWidth(50)
        self.keyLineEdit11.setMinimumHeight(20)
        self.valueLineEdit11 = QtGui.QLineEdit()
        self.valueLineEdit11.setMinimumWidth(50)
        self.valueLineEdit11.setMinimumHeight(20)

        self.keyLineEdit12 = QtGui.QLineEdit()
        self.keyLineEdit12.setMaximumWidth(50)
        self.keyLineEdit12.setMinimumHeight(20)
        self.valueLineEdit12 = QtGui.QLineEdit()
        self.valueLineEdit12.setMinimumWidth(50)
        self.valueLineEdit12.setMinimumHeight(20)

        self.keyLineEdit13 = QtGui.QLineEdit()
        self.keyLineEdit13.setMaximumWidth(50)
        self.keyLineEdit13.setMinimumHeight(20)
        self.valueLineEdit13 = QtGui.QLineEdit()
        self.valueLineEdit13.setMinimumWidth(50)
        self.valueLineEdit13.setMinimumHeight(20)

        self.keyLineEdit14 = QtGui.QLineEdit()
        self.keyLineEdit14.setMaximumWidth(50)
        self.keyLineEdit14.setMinimumHeight(20)
        self.valueLineEdit14 = QtGui.QLineEdit()
        self.valueLineEdit14.setMinimumWidth(50)
        self.valueLineEdit14.setMinimumHeight(20)

        self.keyLineEdit15 = QtGui.QLineEdit()
        self.keyLineEdit15.setMaximumWidth(50)
        self.keyLineEdit15.setMinimumHeight(20)
        self.valueLineEdit15 = QtGui.QLineEdit()
        self.valueLineEdit15.setMinimumWidth(50)
        self.valueLineEdit15.setMinimumHeight(20)

        self.keyLineEdit16 = QtGui.QLineEdit()
        self.keyLineEdit16.setMaximumWidth(50)
        self.keyLineEdit16.setMinimumHeight(20)
        self.valueLineEdit16 = QtGui.QLineEdit()
        self.valueLineEdit16.setMinimumWidth(50)
        self.valueLineEdit16.setMinimumHeight(20)

        self.keyLineEdit17 = QtGui.QLineEdit()
        self.keyLineEdit17.setMaximumWidth(50)
        self.keyLineEdit17.setMinimumHeight(20)
        self.valueLineEdit17 = QtGui.QLineEdit()
        self.valueLineEdit17.setMinimumWidth(50)
        self.valueLineEdit17.setMinimumHeight(20)

        self.keyLineEdit18 = QtGui.QLineEdit()
        self.keyLineEdit18.setMaximumWidth(50)
        self.keyLineEdit18.setMinimumHeight(20)
        self.valueLineEdit18 = QtGui.QLineEdit()
        self.valueLineEdit18.setMinimumWidth(50)
        self.valueLineEdit18.setMinimumHeight(20)

        self.lineEditList = [(self.keyLineEdit9, self.valueLineEdit9), (self.keyLineEdit10, self.valueLineEdit10),
                             (self.keyLineEdit11, self.valueLineEdit11), (self.keyLineEdit12, self.valueLineEdit12),
                             (self.keyLineEdit13, self.valueLineEdit13), (self.keyLineEdit14, self.valueLineEdit14),
                             (self.keyLineEdit15, self.valueLineEdit15), (self.keyLineEdit16, self.valueLineEdit16),
                             (self.keyLineEdit17, self.valueLineEdit17), (self.keyLineEdit18, self.valueLineEdit18), ]

        self.addItemButton.clicked.connect(self.on_addItemButton_clicked)

    @Slot()
    def on_addItemButton_clicked(self):
        if self.additionLineEditCnt < 10:
            keyLineEdit, valueLineEdit = self.lineEditList[self.additionLineEditCnt]
            self.additionLineEditCnt += 1
            self.mainLayout.removeWidget(self.addItemButton)
            self.mainLayout.addWidget(keyLineEdit, self.scrollAreaRowCnt, 0)
            self.mainLayout.addWidget(valueLineEdit, self.scrollAreaRowCnt, 1)
            self.scrollAreaRowCnt += 1
            self.mainLayout.addWidget(self.addItemButton, self.scrollAreaRowCnt, 0, 2, 1)
        else:
            print("You can only add ten items at most !!!")

    def accept(self):
        doc = FreeCAD.ActiveDocument
        freecadFile = doc.FileName
        pos = freecadFile.index('FCStd')
        jsonFile = freecadFile[:pos] + 'json'

        modelName = self.valueLineEdit1.text()
        maxLength = self.valueLineEdit2.text()
        maxWidth = self.valueLineEdit3.text()
        maxHeight = self.valueLineEdit4.text()
        modelType = self.valueLineEdit5.text()
        material = self.valueLineEdit6.text()
        company = self.valueLineEdit7.text()
        # company = self.valueLineEdit8.text()

        with open(jsonFile, "w+", encoding="utf-8") as file:
            # toBeWritten = '{"模型名称":"' + modelName + '","最大长度":' + maxLength + ',"最大宽度":' + maxWidth + ',"最大高度":' + maxHeight + \
            #     ',"模型类型":"' + modelType + '","零件材料":"' + material + '","生产公司":"' + company + '"'
            toBeWritten = '{"模型名称":"' + modelName + '",'
            if maxLength != '':
                toBeWritten += '"最大长度":' + maxLength + ','
            if maxWidth != '':
                toBeWritten += '"最大宽度":' + maxWidth + ','
            if maxHeight != '':
                toBeWritten += '"最大高度":' + maxHeight + ','
            toBeWritten += '"模型类型":"' + modelType + '","零件材料":"' + material + '","生产公司":"' + company + '"'
            for i in range(self.additionLineEditCnt):
                keyLineEdit, valueLineEdit = self.lineEditList[i]
                if keyLineEdit.text() != '':
                    toBeWritten += ',"' + keyLineEdit.text() + '":"' + valueLineEdit.text() + '"'
            file.write(toBeWritten + '}')
            if len(self.selection):
                self.selection[0].Label2 = toBeWritten


        FreeCADGui.Control.closeDialog()


class SinglePartKnowledgeStorage:
    def Activated(self):
        panel = SinglePartKnowledgeStoragePanel()
        FreeCADGui.Control.showDialog(panel)

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'SinglePartKnowledgeStorage',
            'Single Part Knowledge Storage Dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'SinglePartKnowledgeStorage',
            'Store knowledge as a JSON file')
        return {
            'Pixmap': __knowledge_storage_dir__ + '/icons/KnowledgeStorage_cmd.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None


FreeCADGui.addCommand('SinglePartKnowledgeStorage', SinglePartKnowledgeStorage())
