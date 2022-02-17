# -*- coding: utf-8 -*-
# FreeCAD init script of the FilletExpert module,
# simple workbench, 1 command

class IntelligentDesignWorkbench (Workbench):
    """IntelligentDesign workbench object"""
    # this is the icon in XPM format 16x16 pixels
    Icon = """
    /* XPM */
    static char * IntelligentDesign_xpm[] = {
    "16 16 3 1",
    " 	c None",
    ".	c #F2F2F2",
    "+  c #084B8A",
    "                ",
    "   ++++++++++   ",
    "  ++++++++++++  ",
    " ++++++++++++++ ",
    "+++..++..++..+++",
    "++...+....+...++",
    "++..+......+..++",
    "++..+......+..++",
    "++..+......+..++",
    "++..+......+..++",
    "++...+....+...++",
    "+++...+..+...+++",
    " +++...++...+++ ",
    "  +++......+++  ",
    "   ++......++   ",
    "     ......     "};
    """
    MenuText = "IntelligentDesign"
    ToolTip = "IntelligentDesign workbench"

    def Initialize(self) :
        """This function is executed when FreeCAD starts"""
        from PySide import QtCore, QtGui
        # python file where the commands are:
        import FilletExpertGui
        import DraftExpertGui
        import SmartPartsGui
        import SmartFeaturesGui
        import SmartInfoGui
        import SinglePartKnowledgeStorageGui
        import MulPartsKnowledgeStorageGui
        import ProcessKnowledgeStorageGui
        # list of commands, 1 (they are in the imported FilletExpertGui):
        cmdlist = ["FilletExpert", "DraftExpert", "SmartFeatures", "SmartParts", "SmartInfo",
                   "SinglePartKnowledgeStorage", "MulPartsKnowledgeStorage", "ProcessKnowledgeStorage"]
        self.appendToolbar(
            str(QtCore.QT_TRANSLATE_NOOP("IntelligentDesign", "IntelligentDesign")), cmdlist)
        self.appendMenu(
            str(QtCore.QT_TRANSLATE_NOOP("IntelligentDesign", "IntelligentDesign")), cmdlist)

        Log ('Loading IntelligentDesign module... done\n')

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# The workbench is added
Gui.addWorkbench(IntelligentDesignWorkbench())

