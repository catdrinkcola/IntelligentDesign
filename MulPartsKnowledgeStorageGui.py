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

__mul_knowledge_storage_dir__ = os.path.dirname(__file__)


# Task Panel creation: the task panel has to have:
#   1. a widget called self.form
#   2. reject and accept methods (if needed)
class MulPartsKnowledgeStoragePanel:
    def __init__(self):
        self.selection = FreeCADGui.Selection.getSelection()
        self.form = FreeCADGui.PySideUic.loadUi(__mul_knowledge_storage_dir__ + "/UIs/KnowledgeStoragePanel.ui")
        self.mainLayout = QtGui.QGridLayout(self.form.scrollArea)
        self.additionLineEditCnt = 0
        self.scrollAreaRowCnt = 5
        self.firstModelName = self.selection[0].Name
        self.secondModelName = self.selection[1].Name

        # Item1
        self.keyLabel1 = QtGui.QLabel(self.firstModelName + '详细信息')
        self.valueLineEdit1 = QtGui.QLineEdit(self.selection[0].Label2 if self.selection[0].Label2 != '' else '{}')
        self.valueLineEdit1.setMinimumWidth(50)
        self.valueLineEdit1.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel1, 0, 0)
        self.mainLayout.addWidget(self.valueLineEdit1, 0, 1)

        # Item2
        self.keyLabel2 = QtGui.QLabel(self.secondModelName + '详细信息')

        self.valueLineEdit2 = QtGui.QLineEdit(self.selection[1].Label2 if self.selection[0].Label2 != '' else '{}')
        self.valueLineEdit2.setMinimumWidth(50)
        self.valueLineEdit2.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel2, 1, 0)
        self.mainLayout.addWidget(self.valueLineEdit2, 1, 1)

        # Item3
        self.keyLabel3 = QtGui.QLabel('装配尺寸')
        self.valueLineEdit3 = QtGui.QLineEdit(self.firstModelName + '直径10cm,' + self.secondModelName + '直径10cm')
        self.valueLineEdit3.setMinimumWidth(50)
        self.valueLineEdit3.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel3, 2, 0)
        self.mainLayout.addWidget(self.valueLineEdit3, 2, 1)

        # Item4
        self.keyLabel4 = QtGui.QLabel(self.firstModelName + '&' + self.secondModelName + '配合关系')
        self.valueLineEdit4 = QtGui.QLineEdit('过渡配合')
        self.valueLineEdit4.setMinimumWidth(50)
        self.valueLineEdit4.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel4, 3, 0)
        self.mainLayout.addWidget(self.valueLineEdit4, 3, 1)

        # Item5
        self.keyLabel5 = QtGui.QLabel(self.firstModelName + '&' + self.secondModelName + '装配关系')
        self.valueLineEdit5 = QtGui.QLineEdit(self.firstModelName + '套入' + self.secondModelName)
        self.valueLineEdit5.setMinimumWidth(50)
        self.valueLineEdit5.setMinimumHeight(20)
        self.mainLayout.addWidget(self.keyLabel5, 4, 0)
        self.mainLayout.addWidget(self.valueLineEdit5, 4, 1)

        # addItemButton
        self.addItemButton = QtGui.QPushButton('+')
        self.addItemButton.setMinimumWidth(50)
        self.addItemButton.setMinimumHeight(20)
        self.mainLayout.addWidget(self.addItemButton, 5, 0, 2, 1)

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

        label1 = self.keyLabel1.text()
        label2 = self.keyLabel2.text()
        label3 = self.keyLabel3.text()
        label4 = self.keyLabel4.text()
        label5 = self.keyLabel5.text()

        model1Info = self.valueLineEdit1.text()
        model2Info = self.valueLineEdit2.text()
        assemblyDimensions = self.valueLineEdit3.text()
        agreement = self.valueLineEdit4.text()
        assemblyRelationship = self.valueLineEdit5.text()
        if not os.path.exists(jsonFile):
            tmpfile = open(jsonFile, "w+", encoding="utf-8")
            tmpfile.close()

        with open(jsonFile, "r", encoding="utf-8") as f:
            content = f.read()

        with open(jsonFile, "w+", encoding="utf-8") as file:
            if content:
                file.write(content[:-1])
                toBeWritten = ''
                if content.find(label1) == -1:
                    toBeWritten += ',"' + label1 + '":' + model1Info

                if content.find(label2) == -1:
                    toBeWritten += ',"' + label2 + '":' + model2Info + ',"' + label3 + '":"' + assemblyDimensions + '"' + \
                                   ',"' + label4 + '":"' + agreement + '"' + ',"' + label5 + '":"' + assemblyRelationship + '"'

                # if content.find(label3) == -1:
                #     toBeWritten += ',"' + label3 + '":"' + assemblyDimensions + '"'

                # if content.find(label4) == -1:
                #     toBeWritten += ',"' + label4 + '":"' + agreement + '"'

                # if content.find(label5) == -1:
                #     toBeWritten += ',"' + label5 + '":"' + assemblyRelationship + '"'

                for i in range(self.additionLineEditCnt):
                    keyLineEdit, valueLineEdit = self.lineEditList[i]
                    if keyLineEdit.text() != '':
                        toBeWritten += ',"' + keyLineEdit.text() + '":"' + valueLineEdit.text() + '"'
            else:
                toBeWritten = '{"' + label1 + '":' + model1Info + ',"' + label2 + '":' + model2Info + ',"' \
                              + label3 + '":"' + assemblyDimensions + '","' \
                              + label4 + '":"' + agreement + '","' + label5 + '":"' + assemblyRelationship + '"'

                for i in range(self.additionLineEditCnt):
                    keyLineEdit, valueLineEdit = self.lineEditList[i]
                    if keyLineEdit.text() != '':
                        toBeWritten += ',"' + keyLineEdit.text() + '":"' + valueLineEdit.text() + '"'
            file.write(toBeWritten + '}')

        FreeCADGui.Control.closeDialog()


class MulPartsKnowledgeStorage:
    def Activated(self):
        panel = MulPartsKnowledgeStoragePanel()
        FreeCADGui.Control.showDialog(panel)

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'MulPartsKnowledgeStorage',
            'Mul Parts Assembly Knowledge Storage Dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'MulPartsKnowledgeStorage',
            'Store multiple Parts Assembly knowledge as a JSON file')
        return {
            'Pixmap': __mul_knowledge_storage_dir__ + '/icons/MulKnowledgeStorage_cmd.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None


FreeCADGui.addCommand('MulPartsKnowledgeStorage', MulPartsKnowledgeStorage())
