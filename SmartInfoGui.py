# -*- coding: utf-8 -*-
# FreeCAD script for the commands of the SmartInfo workbench creation
# (c) 2021 Daohao Guo

# from PyQt5 import QtCore,QtGui
# from PySide2 import QtCore, QtGui
from PySide import QtCore, QtGui
import FreeCAD
import FreeCADGui
from PySide.QtCore import Slot
import Part
import os
import pymysql

__smart_features_dir__ = os.path.dirname(__file__)


class SmartInfoHelper:
    def __init__(self):
        self.selection = FreeCADGui.Selection.getSelection()
        self.doc = FreeCAD.ActiveDocument

    def insertInfoIntoDb(self):
        currentPart = self.selection[0]
        part_name = currentPart.Name
        material = currentPart.Material
        color = currentPart.Color
        width = currentPart.Width
        length = currentPart.Length
        height = currentPart.Height
        radius = currentPart.Radius

        # 打开数据库连接
        conn = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Haoge88.',
                                     database='freecaddb',
                                     cursorclass=pymysql.cursors.DictCursor)
        # 使用cursor()方法创建一个游标对象
        cursor = conn.cursor()

        sql = """INSERT INTO part_info(part_name,
                 material, color, width, length, height, radius)
                 VALUES (%s, %s, %s, %d, %d, %d, %d)"""

        # 使用execute()方法执行SQL查询
        # cursor.execute(sql, ('cube','grey', 'iron', 5, 5, 5, 0))
        cursor.execute(sql, (part_name, material, color, width, length, height, radius))
        conn.commit()

        conn.close()


class SmartInfo:
    def Activated(self):
        smart_info_helper = SmartInfoHelper()
        smart_info_helper.insertInfoIntoDb()

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'SmartInfo',
            'SmartInfo Dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'SmartInfo',
            'Save part information to the database')
        return {
            'Pixmap': __smart_features_dir__ + '/icons/SmartInfo_cmd.svg',
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not FreeCAD.ActiveDocument is None


FreeCADGui.addCommand('SmartInfo', SmartInfo())
