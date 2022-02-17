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

__draft_expert_dir__ = os.path.dirname(__file__)


class DraftHelper:
    def __init__(self):
        self.selection = FreeCADGui.Selection.getSelection()
        self.doc = FreeCAD.ActiveDocument
        self.selection_len = len(self.selection)
        self.body_obj = self.doc.getObject("Body")

    def doDraft(self):
        # if type(self.selection[0]) == Part.Feature:
        self.selection[0].Visibility = False
        self.body_obj.Visibility = True
        FreeCADGui.Selection.clearSelection()
        vector_of_face = self.body_obj.Shape.Faces[0].CenterOfMass
        FreeCADGui.Selection.addSelection(self.doc.Name, "Body", self.body_obj.Tip.Name + '.Face1',
                                          vector_of_face[0], vector_of_face[1], vector_of_face[2])
        FreeCADGui.runCommand('PartDesign_Draft', 0)
        # if self.body_obj.Tip.Name.__contains__("Draft"):
        # self.body_obj.Visibility = False
        # self.selection[0].Visibility = True
        # else:
            # tmp_features = []
            # for i in self.body_obj.Group:
            #     if i.Name.__contains__("Fillet"):
            #         tmp_features.append((i.Name, i))
            #         self.body_obj.removeObject(i)
            #         print("removed")
            #         self.doc.recompute()
            # # Doc.removeObject(i.Name)
            # for i in tmp_features:
            #     self.body_obj.addObject(i[1])
            # self.doc.recompute()
            # if self.body_obj.Tip.Name.__contains__("Draft"):
            # self.body_obj.Visibility = False
            # self.selection[0].Visibility = True

class DraftExpert:
    """Command to fillet edges with a dialog where you can set the fillets
    """

    def Activated(self):
        draft_helper = DraftHelper()
        draft_helper.doDraft()

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'DraftExpert',
            'DraftExpert Dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'DraftExpert',
            'Use smart method to draft a body')
        return {
            'Pixmap': __draft_expert_dir__ + '/icons/DraftExpert_cmd.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None


FreeCADGui.addCommand('DraftExpert', DraftExpert())
