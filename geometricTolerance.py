#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2016 Juan Vanyo Cerda <juavacer@inf.upv.es>             *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

from GDT import *
import  DraftTools

gdt = GDTWidget()
Label = ['Straightness', 'Flatness', 'Circularity', 'Cylindricity', 'Profile of a line', 'Profile of a surface', 'Perpendicularity', 'Angularity', 'Parallelism', 'Symmetry', 'Position', 'Concentricity','Circular run-out', 'Total run-out']
Icon = [':/dd/icons/Characteristic/straightness.svg', ':/dd/icons/Characteristic/flatness.svg', ':/dd/icons/Characteristic/circularity.svg', ':/dd/icons/Characteristic/cylindricity.svg', ':/dd/icons/Characteristic/profileOfALine.svg', ':/dd/icons/Characteristic/profileOfASurface.svg', ':/dd/icons/Characteristic/perpendicularity.svg', ':/dd/icons/Characteristic/angularity.svg', ':/dd/icons/Characteristic/parallelism.svg', ':/dd/icons/Characteristic/symmetry.svg', ':/dd/icons/Characteristic/position.svg', ':/dd/icons/Characteristic/concentricity.svg',':/dd/icons/Characteristic/circularRunOut.svg', ':/dd/icons/Characteristic/totalRunOut.svg']
gdt.dialogWidgets.append( comboLabelWidget(Text='Characteristic:', List=Label, Icons=Icon) )
gdt.dialogWidgets.append( fieldLabeCombolWidget(Text='Tolerance value:', Circumference = [], List=[], Icons=[], ToolTip=[]) )
gdt.dialogWidgets.append( comboLabelWidget(Text='Datum system:', List=[]) )
gdt.dialogWidgets.append( comboLabelWidget(Text='Active annotation plane:', List=[]) )

class GeometricToleranceCommand:
    def __init__(self):
        self.iconPath = ':/dd/icons/geometricTolerance.svg'
        self.toolTip = 'Add Geometric Tolerance'
        self.Dictionary = []
        for i in range(1,100):
            self.Dictionary.append('GT'+str(i))
        self.idGDT = 3
        self.FeatureControlFrame = makeFeatureControlFrame()

    def Activated(self):
        ContainerOfData = makeContainerOfData()
        if getAnnotationObj(ContainerOfData):
            annotation = getAnnotationObj(ContainerOfData)
            self.toolTip = 'Add Geometric Tolerance to ' + annotation.Label
            gdt.dialogWidgets[3] = None
            if annotation.GT == []:
                gdt.dialogWidgets[1] = fieldLabeCombolWidget(Text='Tolerance value:', Circumference = ['',':/dd/icons/diameter.svg'], Diameter = ContainerOfData.diameter, List=self.FeatureControlFrame.Label, Icons=self.FeatureControlFrame.Icon, ToolTip=self.FeatureControlFrame.toolTip)
            else:
                if annotation.toleranceSelectBool:
                    gdt.dialogWidgets[1] = fieldLabeCombolWidget(Text='Tolerance value:', Circumference = ['',':/dd/icons/diameter.svg'], Diameter = annotation.diameter, tolerance = annotation.toleranceDiameter, List=self.FeatureControlFrame.Label, Icons=self.FeatureControlFrame.Icon, ToolTip=self.FeatureControlFrame.toolTip)
                else:
                    gdt.dialogWidgets[1] = fieldLabeCombolWidget(Text='Tolerance value:', Circumference = ['',':/dd/icons/diameter.svg'], Diameter = annotation.diameter, toleranceSelect=False, lowLimit = annotation.lowLimit, highLimit = annotation.highLimit, List=self.FeatureControlFrame.Label, Icons=self.FeatureControlFrame.Icon, ToolTip=self.FeatureControlFrame.toolTip)
        else:
            self.toolTip = 'Add Geometric Tolerance'
            showGrid()
            gdt.dialogWidgets[3] = comboLabelWidget(Text='Active annotation plane:', List=getAllAnnotationPlaneObjects())
            gdt.dialogWidgets[1] = fieldLabeCombolWidget(Text='Tolerance value:', Circumference = ['',':/dd/icons/diameter.svg'], Diameter = ContainerOfData.diameter, List=self.FeatureControlFrame.Label, Icons=self.FeatureControlFrame.Icon, ToolTip=self.FeatureControlFrame.toolTip)
        gdt.dialogWidgets[2] = comboLabelWidget(Text='Datum system:', List=[None]+getAllDatumSystemObjects())
        gdt.activate(idGDT = self.idGDT, dialogTitle=self.toolTip, dialogIconPath=self.iconPath, endFunction=self.Activated, Dictionary=self.Dictionary)

    def GetResources(self):
        return {
            'Pixmap' : self.iconPath,
            'MenuText': self.toolTip,
            'ToolTip':  self.toolTip
            }

    def IsActive(self):
        if len(getObjectsOfType('AnnotationPlane')) == 0:
            return False
        if getSelection():
            for i in range(len(getSelectionEx())):
                if len(getSelectionEx()[i].SubObjects) == 0:
                    return False
                for j in range(len(getSelectionEx()[i].SubObjects)):
                    if getSelectionEx()[i].SubObjects[j].ShapeType == 'Face':
                        pass
                    else:
                        return False
        else:
            return False
        return True

FreeCADGui.addCommand('dd_geometricTolerance', GeometricToleranceCommand())
