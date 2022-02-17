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

__smart_features_dir__ = os.path.dirname(__file__)


class SmartFeaturesHelper:
    def __init__(self):
        self.selection = FreeCADGui.Selection.getSelection()
        self.doc = FreeCAD.ActiveDocument

    def insertFeatures(self):
        cutObj = self.doc.addObject("Part::Cut",self.selection[0].Name+'_SmartPart')
        cutObj.Base = self.selection[1]
        cutObj.Tool = self.selection[0]
        self.selection[0].Visibility = True
        self.doc.recompute()


class SmartFeatures:
    def Activated(self):
        smart_features_helper = SmartFeaturesHelper()
        smart_features_helper.insertFeatures()

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'SmartFeatures',
            'SmartFeatures Dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'SmartFeatures',
            'Insert smart features to a part')
        return {
            'Pixmap': __smart_features_dir__ + '/icons/SmartFeatures_cmd.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None


FreeCADGui.addCommand('SmartFeatures', SmartFeatures())
