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

__fillet_expert_dir__ = os.path.dirname(__file__)


class FilletHelper:
    def __init__(self):
        self.selection = FreeCADGui.Selection.getSelection()
        self.doc = FreeCAD.ActiveDocument
        self.selection_len = len(self.selection)

    def getSelections(self):
        selections: {str: list} = {}
        edges_to_fillet: {str: list} = {}
        for i in self.selection:
            if type(i) != Part.Feature:
                edges = []
                edges.clear()
                edges_to_fillet[i.Name] = []
                for j in range(len(i.Shape.Edges)):
                    if i.Name == "Cylinder" and not i.Shape.Edges[j].Closed:
                        continue
                    else:
                        edges.append(j + 1)
                selections[i.Name] = edges

        return selections, edges_to_fillet

    def doFillet(self, edges_to_fillet):
        if len(edges_to_fillet) == 0:
            return

        for item in edges_to_fillet.items():
            get_parent_obj = self.doc.getObject(item[0])
            __filetEdgeslist__: {list} = item[1]

            # print("key: " + item[0])
            # print("value: " + str(item[1]))
            # 创建的倒角对象的名称
            # fillet_name = "Fillet" + time.strftime("%H%M%S", time.localtime()) + "_" + str(i)
            fillet_name = "Fillet" + "_" + item[0]
            while True:
                __filetEdgestuple__ = []
                __filetEdgestuple__.clear()
                for li in __filetEdgeslist__:
                    __filetEdgestuple__.append(tuple(li))

                # 添加并返回倒角对象，与 temp_fillet_obj =  Doc.getObject(fillet_name) 具有同样的作用
                temp_fillet_obj = self.doc.addObject("Part::Fillet", fillet_name)

                # print("Name: " + get_parent_obj.Name)
                # print("Label: " + get_parent_obj.Label)
                # 将被选对象的基础位置参数等赋值给倒角对象的 Base 属性
                temp_fillet_obj.Base = get_parent_obj

                # 将包含要倒角的边的列表赋值给倒角对象的 Edges 属性即可完成倒角
                # temp_fillet_obj.Edges = item[1]
                temp_fillet_obj.Edges = __filetEdgestuple__
                # 刷新文档对象
                self.doc.recompute()
                # 如果刚刚创建的倒角对象无效，则移除此倒角对象，并将倒角对象的半径减 0.1mm，然后再次尝试倒角
                if "Invalid" in temp_fillet_obj.State:
                    self.doc.removeObject(temp_fillet_obj.Name)
                    print("Fillet object removed!!")
                    # __filetEdgeslistcopy__ = __filetEdgeslist__.copy()
                    for edge in __filetEdgeslist__:
                        if edge[1]-0.1 <= 0 or edge[2]-0.1 <= 0:
                            __filetEdgeslist__.remove(edge)
                            continue
                        edge[1] -= 0.1
                        edge[2] -= 0.1
                    # fillet_radius -= 0.100
                else:
                    # 如果刚刚创建的倒角对象有效，则将被倒角对象隐藏，并退出循环
                    get_parent_obj.Visibility = False
                    print("Fillet radius is:" + str(__filetEdgeslist__[0][1]) + "mm")
                    break


class FilletRadiusDelegate(QtGui.QItemDelegate):
    def __init__(self, parent):
        super(FilletRadiusDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        # dsb = filletExpertTaskPanel().form.radiusValue
        editor = QtGui.QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0.0)
        editor.setMaximum(2147483647.0)
        editor.setSingleStep(0.1)
        editor.setSuffix(' mm')
        return editor

    def setEditorData(self, editor, index):
        valuestr = index.model().data(index, QtCore.Qt.EditRole)
        if type(valuestr) == str:
            value = valuestr[0:valuestr.index(" mm")]
            editor.setValue(float(value))
        else:
            editor.setValue(valuestr)

    def setModelData(self, editor, model, index):
        editor.interpretText()
        value = editor.value()
        model.setData(index, str(value) + " mm", QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


# Task Panel creation: the task panel has to have:
#   1. a widget called self.form
#   2. reject and accept methods (if needed)
class filletExpertTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi(__fillet_expert_dir__ + "/UIs/FilletExpertPanel.ui")
        model = QtGui.QStandardItemModel(self.form.treeView)
        model.setHorizontalHeaderLabels(["Edges to fillet", "Radius"])
        self.selections, self.edges_to_fillet = FilletHelper().getSelections()

        for item in self.selections.items():
            for i in item[1]:
                edgeItem = QtGui.QStandardItem(item[0] + "-" + "Edge" + str(i))
                model.appendRow(edgeItem)
                edgeItem.setCheckable(True)
                model.setItem(edgeItem.index().row(), 1, QtGui.QStandardItem('1 mm'))

        self.form.treeView.setModel(model)
        delegate = FilletRadiusDelegate(self.form.treeView)
        self.form.treeView.setItemDelegate(delegate)
        self.treeViewModel = self.form.treeView.model()
        # 改变最下方的 QDoubleSpinBox 的值则改变所有的 QDoubleSpinBox 的值
        self.form.radiusValue.valueChanged.connect(self.on_filletStartRadius_valueChanged)
        self.form.radiusValue.valueChanged.emit(self.form.radiusValue.value())

        # 点击 All 这个按钮可以选中所有的边
        self.form.selectAllButton.clicked.connect(self.on_selectAllButton_clicked)
        # self.form.selectAllButton.clicked.emit()

        # 点击 None 这个按钮可以清除所有选中的边
        self.form.selectNoneButton.clicked.connect(self.on_selectNoneButton_clicked)

    @Slot(float)
    def on_filletStartRadius_valueChanged(self, radius):
        # model = self.form.treeView.model()
        for i in range(self.treeViewModel.rowCount()):
            value = self.treeViewModel.index(i, 0).data(QtCore.Qt.CheckStateRole)

            if value & QtCore.Qt.Checked:
                self.treeViewModel.setData(self.treeViewModel.index(i, 1), str(round(radius, 1)) + " mm")

    @Slot()
    def on_selectAllButton_clicked(self):
        # model = self.form.treeView.model()
        for i in range(self.treeViewModel.rowCount()):
            self.treeViewModel.setData(self.treeViewModel.index(i, 0), QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)

    @Slot()
    def on_selectNoneButton_clicked(self):
        # model = self.form.treeView.model()
        for i in range(self.treeViewModel.rowCount()):
            self.treeViewModel.setData(self.treeViewModel.index(i, 0), QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)

    def accept(self):
        for i in range(self.treeViewModel.rowCount()):
            value = self.treeViewModel.index(i, 0).data(QtCore.Qt.CheckStateRole)

            if value & QtCore.Qt.Checked:
                valuestr = self.treeViewModel.index(i, 0).data(QtCore.Qt.EditRole)
                radius_value_str = self.treeViewModel.index(i, 1).data(QtCore.Qt.EditRole)
                radius_value = float(radius_value_str[0:radius_value_str.index(" mm")])
                fillet_object_name = valuestr[0:valuestr.index('-')]
                fillet_object_value = int(valuestr[valuestr.index("Edge") + 4:])
                self.edges_to_fillet[fillet_object_name] \
                    .append([fillet_object_value, radius_value, radius_value])

        FilletHelper().doFillet(self.edges_to_fillet)
        FreeCADGui.Control.closeDialog()


class FilletExpert:
    """Command to fillet edges with a dialog where you can set the fillets
    """

    def Activated(self):
        # what is done when the command is clicked
        # creates a panel with a dialog

        # baseWidget = QtGui.QWidget()
        # baseWidget.setMinimumSize(380, 150)
        # baseWidget.setMaximumSize(380, 150)
        # panel = filletExpertTaskPanel(baseWidget)
        panel = filletExpertTaskPanel()
        # having a panel with a widget in self.form and the accept and
        # reject functions (if needed), we can open it:
        FreeCADGui.Control.showDialog(panel)

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'FilletExpert',
            'FilletExpert Dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'FilletExpert',
            'Use expert knowledge to fillet all selected edges')
        return {
            'Pixmap': __fillet_expert_dir__ + '/icons/FilletExpert_cmd.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None


FreeCADGui.addCommand('FilletExpert', FilletExpert())

