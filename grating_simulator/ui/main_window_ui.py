# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_PySide6gYaVTh.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1220, 776)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_61 = QGridLayout(self.centralwidget)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.gratingGeneratorTab = QWidget()
        self.gratingGeneratorTab.setObjectName(u"gratingGeneratorTab")
        self.gridLayout_2 = QGridLayout(self.gratingGeneratorTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButton_5 = QPushButton(self.gratingGeneratorTab)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.pushButton_3 = QPushButton(self.gratingGeneratorTab)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.gratingGeneratorTab)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox_4 = QGroupBox(self.gratingGeneratorTab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_6 = QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.groupBox_4)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.headerLabel = QLabel(self.groupBox)
        self.headerLabel.setObjectName(u"headerLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.headerLabel)

        self.headerLineEdit = QLineEdit(self.groupBox)
        self.headerLineEdit.setObjectName(u"headerLineEdit")
        self.headerLineEdit.setClearButtonEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.headerLineEdit)

        self.samplingPixelSizeUmLabel = QLabel(self.groupBox)
        self.samplingPixelSizeUmLabel.setObjectName(u"samplingPixelSizeUmLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.samplingPixelSizeUmLabel)

        self.samplingPixelSizeUmDoubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.samplingPixelSizeUmDoubleSpinBox.setObjectName(u"samplingPixelSizeUmDoubleSpinBox")
        self.samplingPixelSizeUmDoubleSpinBox.setDecimals(5)
        self.samplingPixelSizeUmDoubleSpinBox.setSingleStep(0.010000000000000)
        self.samplingPixelSizeUmDoubleSpinBox.setValue(0.050000000000000)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.samplingPixelSizeUmDoubleSpinBox)

        self.invertReusltLabel = QLabel(self.groupBox)
        self.invertReusltLabel.setObjectName(u"invertReusltLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.invertReusltLabel)

        self.invertReusltCheckBox = QCheckBox(self.groupBox)
        self.invertReusltCheckBox.setObjectName(u"invertReusltCheckBox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.invertReusltCheckBox)

        self.saveReulstLabel = QLabel(self.groupBox)
        self.saveReulstLabel.setObjectName(u"saveReulstLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.saveReulstLabel)

        self.saveCheckBox = QCheckBox(self.groupBox)
        self.saveCheckBox.setObjectName(u"saveCheckBox")
        self.saveCheckBox.setChecked(True)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.saveCheckBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_save = QPushButton(self.groupBox)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout_2.addWidget(self.pushButton_save)

        self.pushButton_load = QPushButton(self.groupBox)
        self.pushButton_load.setObjectName(u"pushButton_load")

        self.horizontalLayout_2.addWidget(self.pushButton_load)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.groupBox_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.periodOfPatternUmLabel = QLabel(self.groupBox_2)
        self.periodOfPatternUmLabel.setObjectName(u"periodOfPatternUmLabel")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.periodOfPatternUmLabel)

        self.periodOfPatternUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.periodOfPatternUmDoubleSpinBox.setObjectName(u"periodOfPatternUmDoubleSpinBox")
        self.periodOfPatternUmDoubleSpinBox.setSingleStep(0.100000000000000)
        self.periodOfPatternUmDoubleSpinBox.setValue(20.800000000000001)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.periodOfPatternUmDoubleSpinBox)

        self.heightOfSawtoothUmLabel = QLabel(self.groupBox_2)
        self.heightOfSawtoothUmLabel.setObjectName(u"heightOfSawtoothUmLabel")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.heightOfSawtoothUmLabel)

        self.heightOfSawtoothUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.heightOfSawtoothUmDoubleSpinBox.setObjectName(u"heightOfSawtoothUmDoubleSpinBox")
        self.heightOfSawtoothUmDoubleSpinBox.setSingleStep(0.100000000000000)
        self.heightOfSawtoothUmDoubleSpinBox.setValue(5.200000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.heightOfSawtoothUmDoubleSpinBox)

        self.periodOfSawtoothUmLabel = QLabel(self.groupBox_2)
        self.periodOfSawtoothUmLabel.setObjectName(u"periodOfSawtoothUmLabel")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.periodOfSawtoothUmLabel)

        self.periodOfSawtoothUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.periodOfSawtoothUmDoubleSpinBox.setObjectName(u"periodOfSawtoothUmDoubleSpinBox")
        self.periodOfSawtoothUmDoubleSpinBox.setSingleStep(0.100000000000000)
        self.periodOfSawtoothUmDoubleSpinBox.setValue(1.980000000000000)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.periodOfSawtoothUmDoubleSpinBox)

        self.widthOfStemUmLabel = QLabel(self.groupBox_2)
        self.widthOfStemUmLabel.setObjectName(u"widthOfStemUmLabel")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.widthOfStemUmLabel)

        self.widthOfStemUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.widthOfStemUmDoubleSpinBox.setObjectName(u"widthOfStemUmDoubleSpinBox")
        self.widthOfStemUmDoubleSpinBox.setSingleStep(0.100000000000000)
        self.widthOfStemUmDoubleSpinBox.setValue(3.780000000000000)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.widthOfStemUmDoubleSpinBox)

        self.offsetBtwLinesLabel = QLabel(self.groupBox_2)
        self.offsetBtwLinesLabel.setObjectName(u"offsetBtwLinesLabel")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.offsetBtwLinesLabel)

        self.offsetBtwLinesDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.offsetBtwLinesDoubleSpinBox.setObjectName(u"offsetBtwLinesDoubleSpinBox")
        self.offsetBtwLinesDoubleSpinBox.setSingleStep(0.100000000000000)
        self.offsetBtwLinesDoubleSpinBox.setValue(6.620000000000000)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.offsetBtwLinesDoubleSpinBox)

        self.parameterConsistencyCheckLabel = QLabel(self.groupBox_2)
        self.parameterConsistencyCheckLabel.setObjectName(u"parameterConsistencyCheckLabel")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.parameterConsistencyCheckLabel)

        self.parameterConsistencyCheckLineEdit = QLineEdit(self.groupBox_2)
        self.parameterConsistencyCheckLineEdit.setObjectName(u"parameterConsistencyCheckLineEdit")
        self.parameterConsistencyCheckLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.parameterConsistencyCheckLineEdit)


        self.horizontalLayout_4.addLayout(self.formLayout_2)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.numOfLinesLabel = QLabel(self.groupBox_2)
        self.numOfLinesLabel.setObjectName(u"numOfLinesLabel")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.numOfLinesLabel)

        self.numOfLinesSpinBox = QSpinBox(self.groupBox_2)
        self.numOfLinesSpinBox.setObjectName(u"numOfLinesSpinBox")
        self.numOfLinesSpinBox.setMinimum(1)
        self.numOfLinesSpinBox.setMaximum(999)
        self.numOfLinesSpinBox.setValue(1)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.numOfLinesSpinBox)

        self.lengthOfLineUmLabel = QLabel(self.groupBox_2)
        self.lengthOfLineUmLabel.setObjectName(u"lengthOfLineUmLabel")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lengthOfLineUmLabel)

        self.lengthOfLineUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.lengthOfLineUmDoubleSpinBox.setObjectName(u"lengthOfLineUmDoubleSpinBox")
        self.lengthOfLineUmDoubleSpinBox.setMaximum(10000.000000000000000)
        self.lengthOfLineUmDoubleSpinBox.setSingleStep(10.000000000000000)
        self.lengthOfLineUmDoubleSpinBox.setValue(20.000000000000000)

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lengthOfLineUmDoubleSpinBox)


        self.horizontalLayout_4.addLayout(self.formLayout_4)


        self.gridLayout_3.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.groupBox_8 = QGroupBox(self.groupBox_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_12 = QGridLayout(self.groupBox_8)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.formLayout_11 = QFormLayout()
        self.formLayout_11.setObjectName(u"formLayout_11")
        self.imageHeightPxLabel = QLabel(self.groupBox_8)
        self.imageHeightPxLabel.setObjectName(u"imageHeightPxLabel")

        self.formLayout_11.setWidget(0, QFormLayout.ItemRole.LabelRole, self.imageHeightPxLabel)

        self.imageHeightPxLineEdit = QLineEdit(self.groupBox_8)
        self.imageHeightPxLineEdit.setObjectName(u"imageHeightPxLineEdit")
        self.imageHeightPxLineEdit.setReadOnly(True)

        self.formLayout_11.setWidget(0, QFormLayout.ItemRole.FieldRole, self.imageHeightPxLineEdit)

        self.imageWidthPxLabel = QLabel(self.groupBox_8)
        self.imageWidthPxLabel.setObjectName(u"imageWidthPxLabel")

        self.formLayout_11.setWidget(1, QFormLayout.ItemRole.LabelRole, self.imageWidthPxLabel)

        self.imageWidthPxLineEdit = QLineEdit(self.groupBox_8)
        self.imageWidthPxLineEdit.setObjectName(u"imageWidthPxLineEdit")
        self.imageWidthPxLineEdit.setReadOnly(True)

        self.formLayout_11.setWidget(1, QFormLayout.ItemRole.FieldRole, self.imageWidthPxLineEdit)

        self.imageHeightMmLabel = QLabel(self.groupBox_8)
        self.imageHeightMmLabel.setObjectName(u"imageHeightMmLabel")

        self.formLayout_11.setWidget(2, QFormLayout.ItemRole.LabelRole, self.imageHeightMmLabel)

        self.imageHeightMmLineEdit = QLineEdit(self.groupBox_8)
        self.imageHeightMmLineEdit.setObjectName(u"imageHeightMmLineEdit")
        self.imageHeightMmLineEdit.setReadOnly(True)

        self.formLayout_11.setWidget(2, QFormLayout.ItemRole.FieldRole, self.imageHeightMmLineEdit)

        self.imageWidthMmLabel = QLabel(self.groupBox_8)
        self.imageWidthMmLabel.setObjectName(u"imageWidthMmLabel")

        self.formLayout_11.setWidget(3, QFormLayout.ItemRole.LabelRole, self.imageWidthMmLabel)

        self.imageWidthMmLineEdit = QLineEdit(self.groupBox_8)
        self.imageWidthMmLineEdit.setObjectName(u"imageWidthMmLineEdit")
        self.imageWidthMmLineEdit.setReadOnly(True)

        self.formLayout_11.setWidget(3, QFormLayout.ItemRole.FieldRole, self.imageWidthMmLineEdit)


        self.gridLayout_12.addLayout(self.formLayout_11, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_8, 0, 1, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.groupBox_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.EdgeRounderGroupBox = QGroupBox(self.groupBox_3)
        self.EdgeRounderGroupBox.setObjectName(u"EdgeRounderGroupBox")
        self.EdgeRounderGroupBox.setCheckable(False)
        self.gridLayout_5 = QGridLayout(self.EdgeRounderGroupBox)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.methodLabel = QLabel(self.EdgeRounderGroupBox)
        self.methodLabel.setObjectName(u"methodLabel")

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.LabelRole, self.methodLabel)

        self.methodComboBox = QComboBox(self.EdgeRounderGroupBox)
        self.methodComboBox.addItem("")
        self.methodComboBox.addItem("")
        self.methodComboBox.addItem("")
        self.methodComboBox.setObjectName(u"methodComboBox")

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.FieldRole, self.methodComboBox)

        self.factorLabel = QLabel(self.EdgeRounderGroupBox)
        self.factorLabel.setObjectName(u"factorLabel")

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.LabelRole, self.factorLabel)

        self.factorSpinBox = QSpinBox(self.EdgeRounderGroupBox)
        self.factorSpinBox.setObjectName(u"factorSpinBox")
        self.factorSpinBox.setMinimum(1)

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.FieldRole, self.factorSpinBox)


        self.gridLayout_5.addLayout(self.formLayout_6, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.EdgeRounderGroupBox, 1, 0, 1, 1)

        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.diameterOfEdgeOfSawtoothUmLabel = QLabel(self.groupBox_3)
        self.diameterOfEdgeOfSawtoothUmLabel.setObjectName(u"diameterOfEdgeOfSawtoothUmLabel")

        self.formLayout_7.setWidget(0, QFormLayout.ItemRole.LabelRole, self.diameterOfEdgeOfSawtoothUmLabel)

        self.diameterOfEdgeOfSawtoothUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.diameterOfEdgeOfSawtoothUmDoubleSpinBox.setObjectName(u"diameterOfEdgeOfSawtoothUmDoubleSpinBox")
        self.diameterOfEdgeOfSawtoothUmDoubleSpinBox.setSingleStep(0.100000000000000)
        self.diameterOfEdgeOfSawtoothUmDoubleSpinBox.setValue(0.400000000000000)

        self.formLayout_7.setWidget(0, QFormLayout.ItemRole.FieldRole, self.diameterOfEdgeOfSawtoothUmDoubleSpinBox)


        self.gridLayout_4.addLayout(self.formLayout_7, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_3)


        self.gridLayout_6.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.horizontalLayout_5.addWidget(self.groupBox_4)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox_5 = QGroupBox(self.gratingGeneratorTab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_7 = QGridLayout(self.groupBox_5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")

        self.horizontalLayout_6.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.gratingGeneratorTab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_8 = QGridLayout(self.groupBox_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")

        self.horizontalLayout_6.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.gratingGeneratorTab)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_9 = QGridLayout(self.groupBox_7)
        self.gridLayout_9.setObjectName(u"gridLayout_9")

        self.horizontalLayout_6.addWidget(self.groupBox_7)


        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)

        self.tabWidget.addTab(self.gratingGeneratorTab, "")
        self.microscopeImageSimulatorTab = QWidget()
        self.microscopeImageSimulatorTab.setObjectName(u"microscopeImageSimulatorTab")
        self.gridLayout_16 = QGridLayout(self.microscopeImageSimulatorTab)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)

        self.OTFPushButton = QPushButton(self.microscopeImageSimulatorTab)
        self.OTFPushButton.setObjectName(u"OTFPushButton")

        self.horizontalLayout_13.addWidget(self.OTFPushButton)

        self.RunPushButton = QPushButton(self.microscopeImageSimulatorTab)
        self.RunPushButton.setObjectName(u"RunPushButton")

        self.horizontalLayout_13.addWidget(self.RunPushButton)


        self.gridLayout_16.addLayout(self.horizontalLayout_13, 3, 0, 1, 1)

        self.microscopeParamsGroupBox = QGroupBox(self.microscopeImageSimulatorTab)
        self.microscopeParamsGroupBox.setObjectName(u"microscopeParamsGroupBox")
        self.horizontalLayout_10 = QHBoxLayout(self.microscopeParamsGroupBox)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox_9 = QGroupBox(self.microscopeParamsGroupBox)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_13 = QGridLayout(self.groupBox_9)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.headerLabel_2 = QLabel(self.groupBox_9)
        self.headerLabel_2.setObjectName(u"headerLabel_2")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.headerLabel_2)

        self.nAOfOpticsLabel = QLabel(self.groupBox_9)
        self.nAOfOpticsLabel.setObjectName(u"nAOfOpticsLabel")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.nAOfOpticsLabel)

        self.nAOfOpticsDoubleSpinBox = QDoubleSpinBox(self.groupBox_9)
        self.nAOfOpticsDoubleSpinBox.setObjectName(u"nAOfOpticsDoubleSpinBox")
        self.nAOfOpticsDoubleSpinBox.setSingleStep(0.100000000000000)
        self.nAOfOpticsDoubleSpinBox.setValue(0.800000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.nAOfOpticsDoubleSpinBox)

        self.saveResultLabel = QLabel(self.groupBox_9)
        self.saveResultLabel.setObjectName(u"saveResultLabel")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.saveResultLabel)

        self.saveResultCheckBox = QCheckBox(self.groupBox_9)
        self.saveResultCheckBox.setObjectName(u"saveResultCheckBox")
        self.saveResultCheckBox.setChecked(True)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.saveResultCheckBox)

        self.headerLineEdit_2 = QLineEdit(self.groupBox_9)
        self.headerLineEdit_2.setObjectName(u"headerLineEdit_2")
        self.headerLineEdit_2.setClearButtonEnabled(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.headerLineEdit_2)

        self.simulationConditionLabel = QLabel(self.groupBox_9)
        self.simulationConditionLabel.setObjectName(u"simulationConditionLabel")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.simulationConditionLabel)

        self.simulationConditionLineEdit = QLineEdit(self.groupBox_9)
        self.simulationConditionLineEdit.setObjectName(u"simulationConditionLineEdit")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.simulationConditionLineEdit)


        self.horizontalLayout_9.addLayout(self.formLayout_3)


        self.gridLayout_13.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)

        self.customSpectrumGroupBox = QGroupBox(self.groupBox_9)
        self.customSpectrumGroupBox.setObjectName(u"customSpectrumGroupBox")
        self.customSpectrumGroupBox.setCheckable(True)
        self.customSpectrumGroupBox.setChecked(False)
        self.horizontalLayout_8 = QHBoxLayout(self.customSpectrumGroupBox)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.spectrumMinUmLabel = QLabel(self.customSpectrumGroupBox)
        self.spectrumMinUmLabel.setObjectName(u"spectrumMinUmLabel")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.spectrumMinUmLabel)

        self.spectrumMinUmDoubleSpinBox = QDoubleSpinBox(self.customSpectrumGroupBox)
        self.spectrumMinUmDoubleSpinBox.setObjectName(u"spectrumMinUmDoubleSpinBox")
        self.spectrumMinUmDoubleSpinBox.setDecimals(4)
        self.spectrumMinUmDoubleSpinBox.setValue(0.587600000000000)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spectrumMinUmDoubleSpinBox)

        self.spectrumMaxUmLabel = QLabel(self.customSpectrumGroupBox)
        self.spectrumMaxUmLabel.setObjectName(u"spectrumMaxUmLabel")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.LabelRole, self.spectrumMaxUmLabel)

        self.spectrumMaxUmDoubleSpinBox = QDoubleSpinBox(self.customSpectrumGroupBox)
        self.spectrumMaxUmDoubleSpinBox.setObjectName(u"spectrumMaxUmDoubleSpinBox")
        self.spectrumMaxUmDoubleSpinBox.setDecimals(4)
        self.spectrumMaxUmDoubleSpinBox.setValue(0.587600000000000)

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spectrumMaxUmDoubleSpinBox)

        self.spectrumStepLabel = QLabel(self.customSpectrumGroupBox)
        self.spectrumStepLabel.setObjectName(u"spectrumStepLabel")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.LabelRole, self.spectrumStepLabel)

        self.spectrumStepDoubleSpinBox = QDoubleSpinBox(self.customSpectrumGroupBox)
        self.spectrumStepDoubleSpinBox.setObjectName(u"spectrumStepDoubleSpinBox")
        self.spectrumStepDoubleSpinBox.setSingleStep(0.100000000000000)

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spectrumStepDoubleSpinBox)


        self.horizontalLayout_8.addLayout(self.formLayout_5)


        self.gridLayout_13.addWidget(self.customSpectrumGroupBox, 0, 1, 1, 1)


        self.horizontalLayout_7.addWidget(self.groupBox_9)

        self.groupBox_11 = QGroupBox(self.microscopeParamsGroupBox)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.horizontalLayout_15 = QHBoxLayout(self.groupBox_11)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.groupBox_12 = QGroupBox(self.groupBox_11)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setCheckable(True)
        self.groupBox_12.setChecked(False)
        self.gridLayout_15 = QGridLayout(self.groupBox_12)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.formLayout_8 = QFormLayout()
        self.formLayout_8.setObjectName(u"formLayout_8")
        self.samplingSizeUmLabel = QLabel(self.groupBox_12)
        self.samplingSizeUmLabel.setObjectName(u"samplingSizeUmLabel")

        self.formLayout_8.setWidget(0, QFormLayout.ItemRole.LabelRole, self.samplingSizeUmLabel)

        self.samplingSizeUmDoubleSpinBox = QDoubleSpinBox(self.groupBox_12)
        self.samplingSizeUmDoubleSpinBox.setObjectName(u"samplingSizeUmDoubleSpinBox")

        self.formLayout_8.setWidget(0, QFormLayout.ItemRole.FieldRole, self.samplingSizeUmDoubleSpinBox)


        self.gridLayout_15.addLayout(self.formLayout_8, 0, 0, 1, 1)


        self.horizontalLayout_15.addWidget(self.groupBox_12)

        self.groupBox_29 = QGroupBox(self.groupBox_11)
        self.groupBox_29.setObjectName(u"groupBox_29")
        self.gridLayout_11 = QGridLayout(self.groupBox_29)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.formLayout_10 = QFormLayout()
        self.formLayout_10.setObjectName(u"formLayout_10")
        self.heightPxLabel = QLabel(self.groupBox_29)
        self.heightPxLabel.setObjectName(u"heightPxLabel")

        self.formLayout_10.setWidget(0, QFormLayout.ItemRole.LabelRole, self.heightPxLabel)

        self.heightPxLineEdit = QLineEdit(self.groupBox_29)
        self.heightPxLineEdit.setObjectName(u"heightPxLineEdit")
        self.heightPxLineEdit.setReadOnly(True)

        self.formLayout_10.setWidget(0, QFormLayout.ItemRole.FieldRole, self.heightPxLineEdit)

        self.widthPxLabel = QLabel(self.groupBox_29)
        self.widthPxLabel.setObjectName(u"widthPxLabel")

        self.formLayout_10.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthPxLabel)

        self.widthPxLineEdit = QLineEdit(self.groupBox_29)
        self.widthPxLineEdit.setObjectName(u"widthPxLineEdit")
        self.widthPxLineEdit.setReadOnly(True)

        self.formLayout_10.setWidget(1, QFormLayout.ItemRole.FieldRole, self.widthPxLineEdit)


        self.gridLayout_11.addLayout(self.formLayout_10, 0, 0, 1, 1)

        self.formLayout_9 = QFormLayout()
        self.formLayout_9.setObjectName(u"formLayout_9")
        self.heightMmLabel = QLabel(self.groupBox_29)
        self.heightMmLabel.setObjectName(u"heightMmLabel")

        self.formLayout_9.setWidget(0, QFormLayout.ItemRole.LabelRole, self.heightMmLabel)

        self.heightMmLineEdit = QLineEdit(self.groupBox_29)
        self.heightMmLineEdit.setObjectName(u"heightMmLineEdit")
        self.heightMmLineEdit.setReadOnly(True)

        self.formLayout_9.setWidget(0, QFormLayout.ItemRole.FieldRole, self.heightMmLineEdit)

        self.widthMmLabel = QLabel(self.groupBox_29)
        self.widthMmLabel.setObjectName(u"widthMmLabel")

        self.formLayout_9.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthMmLabel)

        self.widthMmLineEdit = QLineEdit(self.groupBox_29)
        self.widthMmLineEdit.setObjectName(u"widthMmLineEdit")
        self.widthMmLineEdit.setReadOnly(True)

        self.formLayout_9.setWidget(1, QFormLayout.ItemRole.FieldRole, self.widthMmLineEdit)


        self.gridLayout_11.addLayout(self.formLayout_9, 0, 1, 1, 1)


        self.horizontalLayout_15.addWidget(self.groupBox_29)


        self.horizontalLayout_7.addWidget(self.groupBox_11)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_7)


        self.gridLayout_16.addWidget(self.microscopeParamsGroupBox, 2, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.loadedImageGroupBox = QGroupBox(self.microscopeImageSimulatorTab)
        self.loadedImageGroupBox.setObjectName(u"loadedImageGroupBox")
        self.gridLayout_18 = QGridLayout(self.loadedImageGroupBox)
        self.gridLayout_18.setObjectName(u"gridLayout_18")

        self.horizontalLayout_12.addWidget(self.loadedImageGroupBox)

        self.calcuratedOTFGroupBox = QGroupBox(self.microscopeImageSimulatorTab)
        self.calcuratedOTFGroupBox.setObjectName(u"calcuratedOTFGroupBox")
        self.gridLayout_20 = QGridLayout(self.calcuratedOTFGroupBox)
        self.gridLayout_20.setObjectName(u"gridLayout_20")

        self.horizontalLayout_12.addWidget(self.calcuratedOTFGroupBox)

        self.resultImageGroupBox = QGroupBox(self.microscopeImageSimulatorTab)
        self.resultImageGroupBox.setObjectName(u"resultImageGroupBox")
        self.gridLayout_21 = QGridLayout(self.resultImageGroupBox)
        self.gridLayout_21.setObjectName(u"gridLayout_21")

        self.horizontalLayout_12.addWidget(self.resultImageGroupBox)


        self.gridLayout_16.addLayout(self.horizontalLayout_12, 4, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.initializePushButton = QPushButton(self.microscopeImageSimulatorTab)
        self.initializePushButton.setObjectName(u"initializePushButton")

        self.horizontalLayout_14.addWidget(self.initializePushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_4)


        self.gridLayout_16.addLayout(self.horizontalLayout_14, 1, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.loadGratingPushButton = QPushButton(self.microscopeImageSimulatorTab)
        self.loadGratingPushButton.setObjectName(u"loadGratingPushButton")

        self.horizontalLayout_11.addWidget(self.loadGratingPushButton)

        self.loadGratingParamsPushButton = QPushButton(self.microscopeImageSimulatorTab)
        self.loadGratingParamsPushButton.setObjectName(u"loadGratingParamsPushButton")

        self.horizontalLayout_11.addWidget(self.loadGratingParamsPushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer)


        self.gridLayout_16.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)

        self.tabWidget.addTab(self.microscopeImageSimulatorTab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.prjLoadGratingPushButton = QPushButton(self.tab_2)
        self.prjLoadGratingPushButton.setObjectName(u"prjLoadGratingPushButton")

        self.horizontalLayout_32.addWidget(self.prjLoadGratingPushButton)

        self.prjLoadGratingParamsPushButton = QPushButton(self.tab_2)
        self.prjLoadGratingParamsPushButton.setObjectName(u"prjLoadGratingParamsPushButton")

        self.horizontalLayout_32.addWidget(self.prjLoadGratingParamsPushButton)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_11)


        self.verticalLayout_3.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.prjInitializePushButton = QPushButton(self.tab_2)
        self.prjInitializePushButton.setObjectName(u"prjInitializePushButton")

        self.horizontalLayout_31.addWidget(self.prjInitializePushButton)

        self.prjAutoInitializeCheckBox = QCheckBox(self.tab_2)
        self.prjAutoInitializeCheckBox.setObjectName(u"prjAutoInitializeCheckBox")
        self.prjAutoInitializeCheckBox.setChecked(True)

        self.horizontalLayout_31.addWidget(self.prjAutoInitializeCheckBox)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_10)


        self.verticalLayout_3.addLayout(self.horizontalLayout_31)

        self.microscopeParamsGroupBox_3 = QGroupBox(self.tab_2)
        self.microscopeParamsGroupBox_3.setObjectName(u"microscopeParamsGroupBox_3")
        self.horizontalLayout_33 = QHBoxLayout(self.microscopeParamsGroupBox_3)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.groupBox_26 = QGroupBox(self.microscopeParamsGroupBox_3)
        self.groupBox_26.setObjectName(u"groupBox_26")
        self.gridLayout_46 = QGridLayout(self.groupBox_26)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.formLayout_28 = QFormLayout()
        self.formLayout_28.setObjectName(u"formLayout_28")
        self.headerPrefixLabel = QLabel(self.groupBox_26)
        self.headerPrefixLabel.setObjectName(u"headerPrefixLabel")

        self.formLayout_28.setWidget(0, QFormLayout.ItemRole.LabelRole, self.headerPrefixLabel)

        self.prjHeaderPrefixLineEdit = QLineEdit(self.groupBox_26)
        self.prjHeaderPrefixLineEdit.setObjectName(u"prjHeaderPrefixLineEdit")
        self.prjHeaderPrefixLineEdit.setClearButtonEnabled(True)

        self.formLayout_28.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjHeaderPrefixLineEdit)

        self.saveResultLabel_4 = QLabel(self.groupBox_26)
        self.saveResultLabel_4.setObjectName(u"saveResultLabel_4")

        self.formLayout_28.setWidget(1, QFormLayout.ItemRole.LabelRole, self.saveResultLabel_4)

        self.prjSaveResultCheckBox = QCheckBox(self.groupBox_26)
        self.prjSaveResultCheckBox.setObjectName(u"prjSaveResultCheckBox")
        self.prjSaveResultCheckBox.setChecked(True)

        self.formLayout_28.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjSaveResultCheckBox)

        self.simulationConditionLabel_4 = QLabel(self.groupBox_26)
        self.simulationConditionLabel_4.setObjectName(u"simulationConditionLabel_4")

        self.formLayout_28.setWidget(2, QFormLayout.ItemRole.LabelRole, self.simulationConditionLabel_4)

        self.prjSimulationConditionLineEdit = QLineEdit(self.groupBox_26)
        self.prjSimulationConditionLineEdit.setObjectName(u"prjSimulationConditionLineEdit")
        self.prjSimulationConditionLineEdit.setReadOnly(True)

        self.formLayout_28.setWidget(2, QFormLayout.ItemRole.FieldRole, self.prjSimulationConditionLineEdit)


        self.gridLayout_46.addLayout(self.formLayout_28, 0, 0, 1, 1)

        self.prjCustomSpectrumGroupBox = QGroupBox(self.groupBox_26)
        self.prjCustomSpectrumGroupBox.setObjectName(u"prjCustomSpectrumGroupBox")
        self.prjCustomSpectrumGroupBox.setCheckable(True)
        self.prjCustomSpectrumGroupBox.setChecked(False)
        self.horizontalLayout_36 = QHBoxLayout(self.prjCustomSpectrumGroupBox)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.formLayout_24 = QFormLayout()
        self.formLayout_24.setObjectName(u"formLayout_24")
        self.spectrumMinUmLabel_3 = QLabel(self.prjCustomSpectrumGroupBox)
        self.spectrumMinUmLabel_3.setObjectName(u"spectrumMinUmLabel_3")

        self.formLayout_24.setWidget(0, QFormLayout.ItemRole.LabelRole, self.spectrumMinUmLabel_3)

        self.prjSpectrumMinUmDoubleSpinBox = QDoubleSpinBox(self.prjCustomSpectrumGroupBox)
        self.prjSpectrumMinUmDoubleSpinBox.setObjectName(u"prjSpectrumMinUmDoubleSpinBox")
        self.prjSpectrumMinUmDoubleSpinBox.setDecimals(4)
        self.prjSpectrumMinUmDoubleSpinBox.setValue(0.587600000000000)

        self.formLayout_24.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjSpectrumMinUmDoubleSpinBox)

        self.spectrumMaxUmLabel_3 = QLabel(self.prjCustomSpectrumGroupBox)
        self.spectrumMaxUmLabel_3.setObjectName(u"spectrumMaxUmLabel_3")

        self.formLayout_24.setWidget(1, QFormLayout.ItemRole.LabelRole, self.spectrumMaxUmLabel_3)

        self.prjSpectrumMaxUmDoubleSpinBox = QDoubleSpinBox(self.prjCustomSpectrumGroupBox)
        self.prjSpectrumMaxUmDoubleSpinBox.setObjectName(u"prjSpectrumMaxUmDoubleSpinBox")
        self.prjSpectrumMaxUmDoubleSpinBox.setDecimals(4)
        self.prjSpectrumMaxUmDoubleSpinBox.setValue(0.587600000000000)

        self.formLayout_24.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjSpectrumMaxUmDoubleSpinBox)

        self.spectrumStepLabel_3 = QLabel(self.prjCustomSpectrumGroupBox)
        self.spectrumStepLabel_3.setObjectName(u"spectrumStepLabel_3")

        self.formLayout_24.setWidget(2, QFormLayout.ItemRole.LabelRole, self.spectrumStepLabel_3)

        self.prjSpectrumStepDoubleSpinBox = QDoubleSpinBox(self.prjCustomSpectrumGroupBox)
        self.prjSpectrumStepDoubleSpinBox.setObjectName(u"prjSpectrumStepDoubleSpinBox")
        self.prjSpectrumStepDoubleSpinBox.setSingleStep(0.100000000000000)

        self.formLayout_24.setWidget(2, QFormLayout.ItemRole.FieldRole, self.prjSpectrumStepDoubleSpinBox)


        self.horizontalLayout_36.addLayout(self.formLayout_24)


        self.gridLayout_46.addWidget(self.prjCustomSpectrumGroupBox, 2, 0, 1, 1)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.prjPushButton_save = QPushButton(self.groupBox_26)
        self.prjPushButton_save.setObjectName(u"prjPushButton_save")

        self.horizontalLayout_35.addWidget(self.prjPushButton_save)

        self.prjPushButton_load = QPushButton(self.groupBox_26)
        self.prjPushButton_load.setObjectName(u"prjPushButton_load")

        self.horizontalLayout_35.addWidget(self.prjPushButton_load)


        self.gridLayout_46.addLayout(self.horizontalLayout_35, 1, 0, 1, 1)


        self.horizontalLayout_33.addWidget(self.groupBox_26)

        self.groupBox_27 = QGroupBox(self.microscopeParamsGroupBox_3)
        self.groupBox_27.setObjectName(u"groupBox_27")
        self.horizontalLayout_34 = QHBoxLayout(self.groupBox_27)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.formLayout_29 = QFormLayout()
        self.formLayout_29.setObjectName(u"formLayout_29")
        self.z0GratingToLensMmLabel = QLabel(self.groupBox_27)
        self.z0GratingToLensMmLabel.setObjectName(u"z0GratingToLensMmLabel")

        self.formLayout_29.setWidget(0, QFormLayout.ItemRole.LabelRole, self.z0GratingToLensMmLabel)

        self.prjZ0GratingToLensMmDoubleSpinBox = QDoubleSpinBox(self.groupBox_27)
        self.prjZ0GratingToLensMmDoubleSpinBox.setObjectName(u"prjZ0GratingToLensMmDoubleSpinBox")
        self.prjZ0GratingToLensMmDoubleSpinBox.setDecimals(3)
        self.prjZ0GratingToLensMmDoubleSpinBox.setValue(26.000000000000000)

        self.formLayout_29.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjZ0GratingToLensMmDoubleSpinBox)

        self.z1LensToProjectionPlaneMmLabel = QLabel(self.groupBox_27)
        self.z1LensToProjectionPlaneMmLabel.setObjectName(u"z1LensToProjectionPlaneMmLabel")

        self.formLayout_29.setWidget(1, QFormLayout.ItemRole.LabelRole, self.z1LensToProjectionPlaneMmLabel)

        self.prjZ1LensToProjectionPlaneMmDoubleSpinBox = QDoubleSpinBox(self.groupBox_27)
        self.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setObjectName(u"prjZ1LensToProjectionPlaneMmDoubleSpinBox")
        self.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setDecimals(3)
        self.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setMaximum(9999.000000000000000)
        self.prjZ1LensToProjectionPlaneMmDoubleSpinBox.setValue(510.000000000000000)

        self.formLayout_29.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjZ1LensToProjectionPlaneMmDoubleSpinBox)

        self.pupilDiameterMmLabel = QLabel(self.groupBox_27)
        self.pupilDiameterMmLabel.setObjectName(u"pupilDiameterMmLabel")

        self.formLayout_29.setWidget(2, QFormLayout.ItemRole.LabelRole, self.pupilDiameterMmLabel)

        self.prjPupilDiameterMmDoubleSpinBox = QDoubleSpinBox(self.groupBox_27)
        self.prjPupilDiameterMmDoubleSpinBox.setObjectName(u"prjPupilDiameterMmDoubleSpinBox")
        self.prjPupilDiameterMmDoubleSpinBox.setDecimals(3)
        self.prjPupilDiameterMmDoubleSpinBox.setValue(6.000000000000000)

        self.formLayout_29.setWidget(2, QFormLayout.ItemRole.FieldRole, self.prjPupilDiameterMmDoubleSpinBox)

        self.defocusMmLabel = QLabel(self.groupBox_27)
        self.defocusMmLabel.setObjectName(u"defocusMmLabel")

        self.formLayout_29.setWidget(3, QFormLayout.ItemRole.LabelRole, self.defocusMmLabel)

        self.prjDefocusMmDoubleSpinBox = QDoubleSpinBox(self.groupBox_27)
        self.prjDefocusMmDoubleSpinBox.setObjectName(u"prjDefocusMmDoubleSpinBox")
        self.prjDefocusMmDoubleSpinBox.setDecimals(3)
        self.prjDefocusMmDoubleSpinBox.setValue(10.000000000000000)

        self.formLayout_29.setWidget(3, QFormLayout.ItemRole.FieldRole, self.prjDefocusMmDoubleSpinBox)

        self.resizeFactorPixelBinningLabel = QLabel(self.groupBox_27)
        self.resizeFactorPixelBinningLabel.setObjectName(u"resizeFactorPixelBinningLabel")

        self.formLayout_29.setWidget(4, QFormLayout.ItemRole.LabelRole, self.resizeFactorPixelBinningLabel)

        self.prjResizeFactorPixelBinningDoubleSpinBox = QDoubleSpinBox(self.groupBox_27)
        self.prjResizeFactorPixelBinningDoubleSpinBox.setObjectName(u"prjResizeFactorPixelBinningDoubleSpinBox")
        self.prjResizeFactorPixelBinningDoubleSpinBox.setDecimals(4)
        self.prjResizeFactorPixelBinningDoubleSpinBox.setValue(1.000000000000000)

        self.formLayout_29.setWidget(4, QFormLayout.ItemRole.FieldRole, self.prjResizeFactorPixelBinningDoubleSpinBox)

        self.resizeFactorAlongHeightPixelBinningLabel = QLabel(self.groupBox_27)
        self.resizeFactorAlongHeightPixelBinningLabel.setObjectName(u"resizeFactorAlongHeightPixelBinningLabel")

        self.formLayout_29.setWidget(5, QFormLayout.ItemRole.LabelRole, self.resizeFactorAlongHeightPixelBinningLabel)

        self.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox = QDoubleSpinBox(self.groupBox_27)
        self.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.setObjectName(u"prjResizeFactorAlongWidthPixelBinningDoubleSpinBox")
        self.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.setDecimals(4)
        self.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox.setMinimum(1.000000000000000)

        self.formLayout_29.setWidget(5, QFormLayout.ItemRole.FieldRole, self.prjResizeFactorAlongWidthPixelBinningDoubleSpinBox)


        self.verticalLayout_8.addLayout(self.formLayout_29)

        self.prjEdgeRemoverGroupBox = QGroupBox(self.groupBox_27)
        self.prjEdgeRemoverGroupBox.setObjectName(u"prjEdgeRemoverGroupBox")
        self.prjEdgeRemoverGroupBox.setCheckable(True)
        self.prjEdgeRemoverGroupBox.setChecked(False)
        self.gridLayout_48 = QGridLayout(self.prjEdgeRemoverGroupBox)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.formLayout_23 = QFormLayout()
        self.formLayout_23.setObjectName(u"formLayout_23")
        self.edgeRemoverFactorLabel = QLabel(self.prjEdgeRemoverGroupBox)
        self.edgeRemoverFactorLabel.setObjectName(u"edgeRemoverFactorLabel")

        self.formLayout_23.setWidget(0, QFormLayout.ItemRole.LabelRole, self.edgeRemoverFactorLabel)

        self.prjEdgeRemoverFactorDoubleSpinBox = QDoubleSpinBox(self.prjEdgeRemoverGroupBox)
        self.prjEdgeRemoverFactorDoubleSpinBox.setObjectName(u"prjEdgeRemoverFactorDoubleSpinBox")
        self.prjEdgeRemoverFactorDoubleSpinBox.setValue(1.000000000000000)

        self.formLayout_23.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjEdgeRemoverFactorDoubleSpinBox)


        self.gridLayout_48.addLayout(self.formLayout_23, 0, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.prjEdgeRemoverGroupBox)


        self.horizontalLayout_34.addLayout(self.verticalLayout_8)

        self.groupBox_28 = QGroupBox(self.groupBox_27)
        self.groupBox_28.setObjectName(u"groupBox_28")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_28)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_30 = QFormLayout()
        self.formLayout_30.setObjectName(u"formLayout_30")
        self.objectSpaceFLabel = QLabel(self.groupBox_28)
        self.objectSpaceFLabel.setObjectName(u"objectSpaceFLabel")

        self.formLayout_30.setWidget(0, QFormLayout.ItemRole.LabelRole, self.objectSpaceFLabel)

        self.prjObjectSpaceFLineEdit = QLineEdit(self.groupBox_28)
        self.prjObjectSpaceFLineEdit.setObjectName(u"prjObjectSpaceFLineEdit")
        self.prjObjectSpaceFLineEdit.setReadOnly(True)

        self.formLayout_30.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjObjectSpaceFLineEdit)

        self.imageSpaceNALabel = QLabel(self.groupBox_28)
        self.imageSpaceNALabel.setObjectName(u"imageSpaceNALabel")

        self.formLayout_30.setWidget(1, QFormLayout.ItemRole.LabelRole, self.imageSpaceNALabel)

        self.prjImageSpaceNALineEdit = QLineEdit(self.groupBox_28)
        self.prjImageSpaceNALineEdit.setObjectName(u"prjImageSpaceNALineEdit")
        self.prjImageSpaceNALineEdit.setReadOnly(True)

        self.formLayout_30.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjImageSpaceNALineEdit)

        self.magnificationLabel = QLabel(self.groupBox_28)
        self.magnificationLabel.setObjectName(u"magnificationLabel")

        self.formLayout_30.setWidget(2, QFormLayout.ItemRole.LabelRole, self.magnificationLabel)

        self.prjMagnificationLineEdit = QLineEdit(self.groupBox_28)
        self.prjMagnificationLineEdit.setObjectName(u"prjMagnificationLineEdit")
        self.prjMagnificationLineEdit.setReadOnly(True)

        self.formLayout_30.setWidget(2, QFormLayout.ItemRole.FieldRole, self.prjMagnificationLineEdit)

        self.projectedImageHeightMmLabel = QLabel(self.groupBox_28)
        self.projectedImageHeightMmLabel.setObjectName(u"projectedImageHeightMmLabel")

        self.formLayout_30.setWidget(4, QFormLayout.ItemRole.LabelRole, self.projectedImageHeightMmLabel)

        self.prjProjectedImageHeightMmLineEdit = QLineEdit(self.groupBox_28)
        self.prjProjectedImageHeightMmLineEdit.setObjectName(u"prjProjectedImageHeightMmLineEdit")

        self.formLayout_30.setWidget(4, QFormLayout.ItemRole.FieldRole, self.prjProjectedImageHeightMmLineEdit)

        self.fullDepthOfFieldMmLabel = QLabel(self.groupBox_28)
        self.fullDepthOfFieldMmLabel.setObjectName(u"fullDepthOfFieldMmLabel")

        self.formLayout_30.setWidget(3, QFormLayout.ItemRole.LabelRole, self.fullDepthOfFieldMmLabel)

        self.prjFullDepthOfFieldMmLineEdit = QLineEdit(self.groupBox_28)
        self.prjFullDepthOfFieldMmLineEdit.setObjectName(u"prjFullDepthOfFieldMmLineEdit")

        self.formLayout_30.setWidget(3, QFormLayout.ItemRole.FieldRole, self.prjFullDepthOfFieldMmLineEdit)

        self.projectedImageWidthMmLabel = QLabel(self.groupBox_28)
        self.projectedImageWidthMmLabel.setObjectName(u"projectedImageWidthMmLabel")

        self.formLayout_30.setWidget(5, QFormLayout.ItemRole.LabelRole, self.projectedImageWidthMmLabel)

        self.prjProjectedImageWidthMmLineEdit = QLineEdit(self.groupBox_28)
        self.prjProjectedImageWidthMmLineEdit.setObjectName(u"prjProjectedImageWidthMmLineEdit")

        self.formLayout_30.setWidget(5, QFormLayout.ItemRole.FieldRole, self.prjProjectedImageWidthMmLineEdit)

        self.projectedImageSamplingSizeUmLabel = QLabel(self.groupBox_28)
        self.projectedImageSamplingSizeUmLabel.setObjectName(u"projectedImageSamplingSizeUmLabel")

        self.formLayout_30.setWidget(6, QFormLayout.ItemRole.LabelRole, self.projectedImageSamplingSizeUmLabel)

        self.prjProjectedImageSamplingSizeUmLineEdit = QLineEdit(self.groupBox_28)
        self.prjProjectedImageSamplingSizeUmLineEdit.setObjectName(u"prjProjectedImageSamplingSizeUmLineEdit")

        self.formLayout_30.setWidget(6, QFormLayout.ItemRole.FieldRole, self.prjProjectedImageSamplingSizeUmLineEdit)

        self.resizedImageHeightMmLabel = QLabel(self.groupBox_28)
        self.resizedImageHeightMmLabel.setObjectName(u"resizedImageHeightMmLabel")

        self.formLayout_30.setWidget(7, QFormLayout.ItemRole.LabelRole, self.resizedImageHeightMmLabel)

        self.prjResizedImageHeightMmLineEdit = QLineEdit(self.groupBox_28)
        self.prjResizedImageHeightMmLineEdit.setObjectName(u"prjResizedImageHeightMmLineEdit")

        self.formLayout_30.setWidget(7, QFormLayout.ItemRole.FieldRole, self.prjResizedImageHeightMmLineEdit)

        self.resizedImageWidthMmLabel = QLabel(self.groupBox_28)
        self.resizedImageWidthMmLabel.setObjectName(u"resizedImageWidthMmLabel")

        self.formLayout_30.setWidget(8, QFormLayout.ItemRole.LabelRole, self.resizedImageWidthMmLabel)

        self.prjResizedImageWidthMmLineEdit = QLineEdit(self.groupBox_28)
        self.prjResizedImageWidthMmLineEdit.setObjectName(u"prjResizedImageWidthMmLineEdit")

        self.formLayout_30.setWidget(8, QFormLayout.ItemRole.FieldRole, self.prjResizedImageWidthMmLineEdit)

        self.resizedImageSamplingSizeUmLabel = QLabel(self.groupBox_28)
        self.resizedImageSamplingSizeUmLabel.setObjectName(u"resizedImageSamplingSizeUmLabel")

        self.formLayout_30.setWidget(9, QFormLayout.ItemRole.LabelRole, self.resizedImageSamplingSizeUmLabel)

        self.prjResizedImageSamplingSizeUmLineEdit = QLineEdit(self.groupBox_28)
        self.prjResizedImageSamplingSizeUmLineEdit.setObjectName(u"prjResizedImageSamplingSizeUmLineEdit")

        self.formLayout_30.setWidget(9, QFormLayout.ItemRole.FieldRole, self.prjResizedImageSamplingSizeUmLineEdit)


        self.verticalLayout_4.addLayout(self.formLayout_30)


        self.horizontalLayout_34.addWidget(self.groupBox_28)


        self.horizontalLayout_33.addWidget(self.groupBox_27)

        self.groupBox_24 = QGroupBox(self.microscopeParamsGroupBox_3)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_24)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_30 = QGroupBox(self.groupBox_24)
        self.groupBox_30.setObjectName(u"groupBox_30")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_30)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.prjCustomImagePropertyGroupBox = QGroupBox(self.groupBox_30)
        self.prjCustomImagePropertyGroupBox.setObjectName(u"prjCustomImagePropertyGroupBox")
        self.prjCustomImagePropertyGroupBox.setCheckable(True)
        self.prjCustomImagePropertyGroupBox.setChecked(False)
        self.gridLayout_37 = QGridLayout(self.prjCustomImagePropertyGroupBox)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.formLayout_25 = QFormLayout()
        self.formLayout_25.setObjectName(u"formLayout_25")
        self.samplingSizeUmLabel_3 = QLabel(self.prjCustomImagePropertyGroupBox)
        self.samplingSizeUmLabel_3.setObjectName(u"samplingSizeUmLabel_3")

        self.formLayout_25.setWidget(0, QFormLayout.ItemRole.LabelRole, self.samplingSizeUmLabel_3)

        self.prjSamplingSizeUmDoubleSpinBox = QDoubleSpinBox(self.prjCustomImagePropertyGroupBox)
        self.prjSamplingSizeUmDoubleSpinBox.setObjectName(u"prjSamplingSizeUmDoubleSpinBox")
        self.prjSamplingSizeUmDoubleSpinBox.setDecimals(5)

        self.formLayout_25.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjSamplingSizeUmDoubleSpinBox)

        self.periodOfSawtoothUmLabel_3 = QLabel(self.prjCustomImagePropertyGroupBox)
        self.periodOfSawtoothUmLabel_3.setObjectName(u"periodOfSawtoothUmLabel_3")

        self.formLayout_25.setWidget(1, QFormLayout.ItemRole.LabelRole, self.periodOfSawtoothUmLabel_3)

        self.prjPeriodOfSawDoubleSpinBox = QDoubleSpinBox(self.prjCustomImagePropertyGroupBox)
        self.prjPeriodOfSawDoubleSpinBox.setObjectName(u"prjPeriodOfSawDoubleSpinBox")
        self.prjPeriodOfSawDoubleSpinBox.setDecimals(5)

        self.formLayout_25.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjPeriodOfSawDoubleSpinBox)


        self.gridLayout_37.addLayout(self.formLayout_25, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.prjCustomImagePropertyGroupBox)

        self.formLayout_27 = QFormLayout()
        self.formLayout_27.setObjectName(u"formLayout_27")
        self.heightMmLabel_3 = QLabel(self.groupBox_30)
        self.heightMmLabel_3.setObjectName(u"heightMmLabel_3")

        self.formLayout_27.setWidget(0, QFormLayout.ItemRole.LabelRole, self.heightMmLabel_3)

        self.prjHeightMmLineEdit = QLineEdit(self.groupBox_30)
        self.prjHeightMmLineEdit.setObjectName(u"prjHeightMmLineEdit")
        self.prjHeightMmLineEdit.setReadOnly(True)

        self.formLayout_27.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjHeightMmLineEdit)

        self.widthMmLabel_3 = QLabel(self.groupBox_30)
        self.widthMmLabel_3.setObjectName(u"widthMmLabel_3")

        self.formLayout_27.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthMmLabel_3)

        self.prjWidthMmLineEdit = QLineEdit(self.groupBox_30)
        self.prjWidthMmLineEdit.setObjectName(u"prjWidthMmLineEdit")
        self.prjWidthMmLineEdit.setReadOnly(True)

        self.formLayout_27.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjWidthMmLineEdit)


        self.verticalLayout_6.addLayout(self.formLayout_27)

        self.formLayout_26 = QFormLayout()
        self.formLayout_26.setObjectName(u"formLayout_26")
        self.heightPxLabel_3 = QLabel(self.groupBox_30)
        self.heightPxLabel_3.setObjectName(u"heightPxLabel_3")

        self.formLayout_26.setWidget(0, QFormLayout.ItemRole.LabelRole, self.heightPxLabel_3)

        self.prjHeightPxLineEdit = QLineEdit(self.groupBox_30)
        self.prjHeightPxLineEdit.setObjectName(u"prjHeightPxLineEdit")
        self.prjHeightPxLineEdit.setReadOnly(True)

        self.formLayout_26.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjHeightPxLineEdit)

        self.widthPxLabel_3 = QLabel(self.groupBox_30)
        self.widthPxLabel_3.setObjectName(u"widthPxLabel_3")

        self.formLayout_26.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthPxLabel_3)

        self.prjWidthPxLineEdit = QLineEdit(self.groupBox_30)
        self.prjWidthPxLineEdit.setObjectName(u"prjWidthPxLineEdit")
        self.prjWidthPxLineEdit.setReadOnly(True)

        self.formLayout_26.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjWidthPxLineEdit)


        self.verticalLayout_6.addLayout(self.formLayout_26)


        self.verticalLayout_5.addWidget(self.groupBox_30)


        self.horizontalLayout_33.addWidget(self.groupBox_24)


        self.verticalLayout_3.addWidget(self.microscopeParamsGroupBox_3)

        self.gridLayout_45 = QGridLayout()
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.prjOTFPushButton = QPushButton(self.tab_2)
        self.prjOTFPushButton.setObjectName(u"prjOTFPushButton")

        self.gridLayout_45.addWidget(self.prjOTFPushButton, 0, 1, 1, 1)

        self.prjPlotImageCrsPushButton = QPushButton(self.tab_2)
        self.prjPlotImageCrsPushButton.setObjectName(u"prjPlotImageCrsPushButton")

        self.gridLayout_45.addWidget(self.prjPlotImageCrsPushButton, 1, 2, 1, 1)

        self.prjRunPushButton = QPushButton(self.tab_2)
        self.prjRunPushButton.setObjectName(u"prjRunPushButton")

        self.gridLayout_45.addWidget(self.prjRunPushButton, 0, 2, 1, 1)

        self.prjPSFcrsPushButton = QPushButton(self.tab_2)
        self.prjPSFcrsPushButton.setObjectName(u"prjPSFcrsPushButton")

        self.gridLayout_45.addWidget(self.prjPSFcrsPushButton, 0, 4, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_45.addItem(self.horizontalSpacer_9, 0, 0, 1, 1)

        self.prjPlotPSFCrspushButton = QPushButton(self.tab_2)
        self.prjPlotPSFCrspushButton.setObjectName(u"prjPlotPSFCrspushButton")

        self.gridLayout_45.addWidget(self.prjPlotPSFCrspushButton, 1, 4, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_45)

        self.gridLayout_53 = QGridLayout()
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.prjLoadedImageGroupBox = QGroupBox(self.tab_2)
        self.prjLoadedImageGroupBox.setObjectName(u"prjLoadedImageGroupBox")
        self.gridLayout_35 = QGridLayout(self.prjLoadedImageGroupBox)
        self.gridLayout_35.setObjectName(u"gridLayout_35")

        self.gridLayout_53.addWidget(self.prjLoadedImageGroupBox, 0, 0, 1, 1)

        self.prjResultProjectedImageGroupBox = QGroupBox(self.tab_2)
        self.prjResultProjectedImageGroupBox.setObjectName(u"prjResultProjectedImageGroupBox")
        self.gridLayout_47 = QGridLayout(self.prjResultProjectedImageGroupBox)
        self.gridLayout_47.setObjectName(u"gridLayout_47")

        self.gridLayout_53.addWidget(self.prjResultProjectedImageGroupBox, 0, 2, 1, 1)

        self.prjPSFcrsGroupBox = QGroupBox(self.tab_2)
        self.prjPSFcrsGroupBox.setObjectName(u"prjPSFcrsGroupBox")
        self.gridLayout_36 = QGridLayout(self.prjPSFcrsGroupBox)
        self.gridLayout_36.setObjectName(u"gridLayout_36")

        self.gridLayout_53.addWidget(self.prjPSFcrsGroupBox, 0, 4, 1, 1)

        self.prjResultDefocusedImageGroupBox = QGroupBox(self.tab_2)
        self.prjResultDefocusedImageGroupBox.setObjectName(u"prjResultDefocusedImageGroupBox")
        self.gridLayout_51 = QGridLayout(self.prjResultDefocusedImageGroupBox)
        self.gridLayout_51.setObjectName(u"gridLayout_51")

        self.gridLayout_53.addWidget(self.prjResultDefocusedImageGroupBox, 0, 3, 1, 1)

        self.prjCalcuratedOTFGroupBox = QGroupBox(self.tab_2)
        self.prjCalcuratedOTFGroupBox.setObjectName(u"prjCalcuratedOTFGroupBox")
        self.gridLayout_44 = QGridLayout(self.prjCalcuratedOTFGroupBox)
        self.gridLayout_44.setObjectName(u"gridLayout_44")

        self.gridLayout_53.addWidget(self.prjCalcuratedOTFGroupBox, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_53)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_14 = QVBoxLayout(self.tab_3)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.aswLoadProjectedFlatImagePushButton = QPushButton(self.tab_3)
        self.aswLoadProjectedFlatImagePushButton.setObjectName(u"aswLoadProjectedFlatImagePushButton")

        self.horizontalLayout_37.addWidget(self.aswLoadProjectedFlatImagePushButton)

        self.aswLoadProjectorParamsPushButton = QPushButton(self.tab_3)
        self.aswLoadProjectorParamsPushButton.setObjectName(u"aswLoadProjectorParamsPushButton")

        self.horizontalLayout_37.addWidget(self.aswLoadProjectorParamsPushButton)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_12)


        self.verticalLayout_14.addLayout(self.horizontalLayout_37)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.aswInitializePushButton = QPushButton(self.tab_3)
        self.aswInitializePushButton.setObjectName(u"aswInitializePushButton")

        self.horizontalLayout_40.addWidget(self.aswInitializePushButton)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_40.addItem(self.horizontalSpacer_13)


        self.verticalLayout_14.addLayout(self.horizontalLayout_40)

        self.microscopeParamsGroupBox_4 = QGroupBox(self.tab_3)
        self.microscopeParamsGroupBox_4.setObjectName(u"microscopeParamsGroupBox_4")
        self.horizontalLayout_41 = QHBoxLayout(self.microscopeParamsGroupBox_4)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.groupBox_31 = QGroupBox(self.microscopeParamsGroupBox_4)
        self.groupBox_31.setObjectName(u"groupBox_31")
        self.gridLayout_49 = QGridLayout(self.groupBox_31)
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.prjPushButton_save_2 = QPushButton(self.groupBox_31)
        self.prjPushButton_save_2.setObjectName(u"prjPushButton_save_2")

        self.horizontalLayout_43.addWidget(self.prjPushButton_save_2)

        self.prjPushButton_load_2 = QPushButton(self.groupBox_31)
        self.prjPushButton_load_2.setObjectName(u"prjPushButton_load_2")

        self.horizontalLayout_43.addWidget(self.prjPushButton_load_2)


        self.gridLayout_49.addLayout(self.horizontalLayout_43, 1, 0, 1, 1)

        self.formLayout_31 = QFormLayout()
        self.formLayout_31.setObjectName(u"formLayout_31")
        self.headerPrefixLabel_2 = QLabel(self.groupBox_31)
        self.headerPrefixLabel_2.setObjectName(u"headerPrefixLabel_2")

        self.formLayout_31.setWidget(0, QFormLayout.ItemRole.LabelRole, self.headerPrefixLabel_2)

        self.prjHeaderPrefixLineEdit_2 = QLineEdit(self.groupBox_31)
        self.prjHeaderPrefixLineEdit_2.setObjectName(u"prjHeaderPrefixLineEdit_2")
        self.prjHeaderPrefixLineEdit_2.setClearButtonEnabled(True)

        self.formLayout_31.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjHeaderPrefixLineEdit_2)

        self.saveResultLabel_5 = QLabel(self.groupBox_31)
        self.saveResultLabel_5.setObjectName(u"saveResultLabel_5")

        self.formLayout_31.setWidget(1, QFormLayout.ItemRole.LabelRole, self.saveResultLabel_5)

        self.prjSaveResultCheckBox_2 = QCheckBox(self.groupBox_31)
        self.prjSaveResultCheckBox_2.setObjectName(u"prjSaveResultCheckBox_2")
        self.prjSaveResultCheckBox_2.setChecked(True)

        self.formLayout_31.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjSaveResultCheckBox_2)

        self.stretchImageToSquareLabel = QLabel(self.groupBox_31)
        self.stretchImageToSquareLabel.setObjectName(u"stretchImageToSquareLabel")

        self.formLayout_31.setWidget(2, QFormLayout.ItemRole.LabelRole, self.stretchImageToSquareLabel)

        self.stretchImageToSquareLineEdit = QLineEdit(self.groupBox_31)
        self.stretchImageToSquareLineEdit.setObjectName(u"stretchImageToSquareLineEdit")

        self.formLayout_31.setWidget(2, QFormLayout.ItemRole.FieldRole, self.stretchImageToSquareLineEdit)


        self.gridLayout_49.addLayout(self.formLayout_31, 0, 0, 1, 1)


        self.horizontalLayout_41.addWidget(self.groupBox_31)

        self.groupBox_32 = QGroupBox(self.microscopeParamsGroupBox_4)
        self.groupBox_32.setObjectName(u"groupBox_32")
        self.horizontalLayout_44 = QHBoxLayout(self.groupBox_32)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.formLayout_33 = QFormLayout()
        self.formLayout_33.setObjectName(u"formLayout_33")
        self.xProjectionAngleDegLabel = QLabel(self.groupBox_32)
        self.xProjectionAngleDegLabel.setObjectName(u"xProjectionAngleDegLabel")

        self.formLayout_33.setWidget(0, QFormLayout.ItemRole.LabelRole, self.xProjectionAngleDegLabel)

        self.xProjectionAngleDegDoubleSpinBox = QDoubleSpinBox(self.groupBox_32)
        self.xProjectionAngleDegDoubleSpinBox.setObjectName(u"xProjectionAngleDegDoubleSpinBox")

        self.formLayout_33.setWidget(0, QFormLayout.ItemRole.FieldRole, self.xProjectionAngleDegDoubleSpinBox)

        self.yProjectionAngleDegLabel = QLabel(self.groupBox_32)
        self.yProjectionAngleDegLabel.setObjectName(u"yProjectionAngleDegLabel")

        self.formLayout_33.setWidget(1, QFormLayout.ItemRole.LabelRole, self.yProjectionAngleDegLabel)

        self.yProjectionAngleDegDoubleSpinBox = QDoubleSpinBox(self.groupBox_32)
        self.yProjectionAngleDegDoubleSpinBox.setObjectName(u"yProjectionAngleDegDoubleSpinBox")

        self.formLayout_33.setWidget(1, QFormLayout.ItemRole.FieldRole, self.yProjectionAngleDegDoubleSpinBox)


        self.verticalLayout_10.addLayout(self.formLayout_33)

        self.prjEdgeRemoverGroupBox_2 = QGroupBox(self.groupBox_32)
        self.prjEdgeRemoverGroupBox_2.setObjectName(u"prjEdgeRemoverGroupBox_2")
        self.prjEdgeRemoverGroupBox_2.setCheckable(True)
        self.gridLayout_50 = QGridLayout(self.prjEdgeRemoverGroupBox_2)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.formLayout_34 = QFormLayout()
        self.formLayout_34.setObjectName(u"formLayout_34")
        self.edgeRemoverFactorLabel_2 = QLabel(self.prjEdgeRemoverGroupBox_2)
        self.edgeRemoverFactorLabel_2.setObjectName(u"edgeRemoverFactorLabel_2")

        self.formLayout_34.setWidget(0, QFormLayout.ItemRole.LabelRole, self.edgeRemoverFactorLabel_2)

        self.prjEdgeRemoverFactorDoubleSpinBox_2 = QDoubleSpinBox(self.prjEdgeRemoverGroupBox_2)
        self.prjEdgeRemoverFactorDoubleSpinBox_2.setObjectName(u"prjEdgeRemoverFactorDoubleSpinBox_2")
        self.prjEdgeRemoverFactorDoubleSpinBox_2.setValue(1.000000000000000)

        self.formLayout_34.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjEdgeRemoverFactorDoubleSpinBox_2)


        self.gridLayout_50.addLayout(self.formLayout_34, 0, 0, 1, 1)


        self.verticalLayout_10.addWidget(self.prjEdgeRemoverGroupBox_2)


        self.horizontalLayout_44.addLayout(self.verticalLayout_10)

        self.groupBox_33 = QGroupBox(self.groupBox_32)
        self.groupBox_33.setObjectName(u"groupBox_33")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_33)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.formLayout_35 = QFormLayout()
        self.formLayout_35.setObjectName(u"formLayout_35")
        self.z1WDefocusLensToPlaneMmLabel = QLabel(self.groupBox_33)
        self.z1WDefocusLensToPlaneMmLabel.setObjectName(u"z1WDefocusLensToPlaneMmLabel")

        self.formLayout_35.setWidget(0, QFormLayout.ItemRole.LabelRole, self.z1WDefocusLensToPlaneMmLabel)

        self.z1WDefocusLensToPlaneMmLineEdit = QLineEdit(self.groupBox_33)
        self.z1WDefocusLensToPlaneMmLineEdit.setObjectName(u"z1WDefocusLensToPlaneMmLineEdit")

        self.formLayout_35.setWidget(0, QFormLayout.ItemRole.FieldRole, self.z1WDefocusLensToPlaneMmLineEdit)

        self.xGratingTiltAngleDegLabel = QLabel(self.groupBox_33)
        self.xGratingTiltAngleDegLabel.setObjectName(u"xGratingTiltAngleDegLabel")

        self.formLayout_35.setWidget(1, QFormLayout.ItemRole.LabelRole, self.xGratingTiltAngleDegLabel)

        self.xGratingTiltAngleDegLineEdit = QLineEdit(self.groupBox_33)
        self.xGratingTiltAngleDegLineEdit.setObjectName(u"xGratingTiltAngleDegLineEdit")

        self.formLayout_35.setWidget(1, QFormLayout.ItemRole.FieldRole, self.xGratingTiltAngleDegLineEdit)

        self.yGratingTiltAngleDegLabel = QLabel(self.groupBox_33)
        self.yGratingTiltAngleDegLabel.setObjectName(u"yGratingTiltAngleDegLabel")

        self.formLayout_35.setWidget(2, QFormLayout.ItemRole.LabelRole, self.yGratingTiltAngleDegLabel)

        self.yGratingTiltAngleDegLineEdit = QLineEdit(self.groupBox_33)
        self.yGratingTiltAngleDegLineEdit.setObjectName(u"yGratingTiltAngleDegLineEdit")

        self.formLayout_35.setWidget(2, QFormLayout.ItemRole.FieldRole, self.yGratingTiltAngleDegLineEdit)


        self.verticalLayout_11.addLayout(self.formLayout_35)


        self.horizontalLayout_44.addWidget(self.groupBox_33)


        self.horizontalLayout_41.addWidget(self.groupBox_32)

        self.groupBox_25 = QGroupBox(self.microscopeParamsGroupBox_4)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_25)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.groupBox_34 = QGroupBox(self.groupBox_25)
        self.groupBox_34.setObjectName(u"groupBox_34")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_34)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.prjCustomImagePropertyGroupBox_2 = QGroupBox(self.groupBox_34)
        self.prjCustomImagePropertyGroupBox_2.setObjectName(u"prjCustomImagePropertyGroupBox_2")
        self.prjCustomImagePropertyGroupBox_2.setCheckable(True)
        self.prjCustomImagePropertyGroupBox_2.setChecked(False)
        self.gridLayout_52 = QGridLayout(self.prjCustomImagePropertyGroupBox_2)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.formLayout_36 = QFormLayout()
        self.formLayout_36.setObjectName(u"formLayout_36")
        self.samplingSizeUmLabel_4 = QLabel(self.prjCustomImagePropertyGroupBox_2)
        self.samplingSizeUmLabel_4.setObjectName(u"samplingSizeUmLabel_4")

        self.formLayout_36.setWidget(0, QFormLayout.ItemRole.LabelRole, self.samplingSizeUmLabel_4)

        self.prjSamplingSizeUmDoubleSpinBox_2 = QDoubleSpinBox(self.prjCustomImagePropertyGroupBox_2)
        self.prjSamplingSizeUmDoubleSpinBox_2.setObjectName(u"prjSamplingSizeUmDoubleSpinBox_2")

        self.formLayout_36.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjSamplingSizeUmDoubleSpinBox_2)


        self.gridLayout_52.addLayout(self.formLayout_36, 0, 0, 1, 1)


        self.verticalLayout_13.addWidget(self.prjCustomImagePropertyGroupBox_2)

        self.formLayout_37 = QFormLayout()
        self.formLayout_37.setObjectName(u"formLayout_37")
        self.heightMmLabel_4 = QLabel(self.groupBox_34)
        self.heightMmLabel_4.setObjectName(u"heightMmLabel_4")

        self.formLayout_37.setWidget(0, QFormLayout.ItemRole.LabelRole, self.heightMmLabel_4)

        self.prjHeightMmLineEdit_2 = QLineEdit(self.groupBox_34)
        self.prjHeightMmLineEdit_2.setObjectName(u"prjHeightMmLineEdit_2")
        self.prjHeightMmLineEdit_2.setReadOnly(True)

        self.formLayout_37.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjHeightMmLineEdit_2)

        self.widthMmLabel_4 = QLabel(self.groupBox_34)
        self.widthMmLabel_4.setObjectName(u"widthMmLabel_4")

        self.formLayout_37.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthMmLabel_4)

        self.prjWidthMmLineEdit_2 = QLineEdit(self.groupBox_34)
        self.prjWidthMmLineEdit_2.setObjectName(u"prjWidthMmLineEdit_2")
        self.prjWidthMmLineEdit_2.setReadOnly(True)

        self.formLayout_37.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjWidthMmLineEdit_2)


        self.verticalLayout_13.addLayout(self.formLayout_37)

        self.formLayout_38 = QFormLayout()
        self.formLayout_38.setObjectName(u"formLayout_38")
        self.heightPxLabel_4 = QLabel(self.groupBox_34)
        self.heightPxLabel_4.setObjectName(u"heightPxLabel_4")

        self.formLayout_38.setWidget(0, QFormLayout.ItemRole.LabelRole, self.heightPxLabel_4)

        self.prjHeightPxLineEdit_2 = QLineEdit(self.groupBox_34)
        self.prjHeightPxLineEdit_2.setObjectName(u"prjHeightPxLineEdit_2")
        self.prjHeightPxLineEdit_2.setReadOnly(True)

        self.formLayout_38.setWidget(0, QFormLayout.ItemRole.FieldRole, self.prjHeightPxLineEdit_2)

        self.widthPxLabel_4 = QLabel(self.groupBox_34)
        self.widthPxLabel_4.setObjectName(u"widthPxLabel_4")

        self.formLayout_38.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthPxLabel_4)

        self.prjWidthPxLineEdit_2 = QLineEdit(self.groupBox_34)
        self.prjWidthPxLineEdit_2.setObjectName(u"prjWidthPxLineEdit_2")
        self.prjWidthPxLineEdit_2.setReadOnly(True)

        self.formLayout_38.setWidget(1, QFormLayout.ItemRole.FieldRole, self.prjWidthPxLineEdit_2)


        self.verticalLayout_13.addLayout(self.formLayout_38)

        self.formLayout_32 = QFormLayout()
        self.formLayout_32.setObjectName(u"formLayout_32")
        self.z0GratingToLensMmLabel_2 = QLabel(self.groupBox_34)
        self.z0GratingToLensMmLabel_2.setObjectName(u"z0GratingToLensMmLabel_2")

        self.formLayout_32.setWidget(0, QFormLayout.ItemRole.LabelRole, self.z0GratingToLensMmLabel_2)

        self.z0GratingToLensMmLineEdit = QLineEdit(self.groupBox_34)
        self.z0GratingToLensMmLineEdit.setObjectName(u"z0GratingToLensMmLineEdit")

        self.formLayout_32.setWidget(0, QFormLayout.ItemRole.FieldRole, self.z0GratingToLensMmLineEdit)

        self.z1LensToProjectionPlaneMmLabel_2 = QLabel(self.groupBox_34)
        self.z1LensToProjectionPlaneMmLabel_2.setObjectName(u"z1LensToProjectionPlaneMmLabel_2")

        self.formLayout_32.setWidget(1, QFormLayout.ItemRole.LabelRole, self.z1LensToProjectionPlaneMmLabel_2)

        self.z1LensToProjectionPlaneMmLineEdit = QLineEdit(self.groupBox_34)
        self.z1LensToProjectionPlaneMmLineEdit.setObjectName(u"z1LensToProjectionPlaneMmLineEdit")

        self.formLayout_32.setWidget(1, QFormLayout.ItemRole.FieldRole, self.z1LensToProjectionPlaneMmLineEdit)

        self.defocusMmLabel_2 = QLabel(self.groupBox_34)
        self.defocusMmLabel_2.setObjectName(u"defocusMmLabel_2")

        self.formLayout_32.setWidget(2, QFormLayout.ItemRole.LabelRole, self.defocusMmLabel_2)

        self.defocusMmLineEdit_2 = QLineEdit(self.groupBox_34)
        self.defocusMmLineEdit_2.setObjectName(u"defocusMmLineEdit_2")

        self.formLayout_32.setWidget(2, QFormLayout.ItemRole.FieldRole, self.defocusMmLineEdit_2)


        self.verticalLayout_13.addLayout(self.formLayout_32)


        self.verticalLayout_12.addWidget(self.groupBox_34)


        self.horizontalLayout_41.addWidget(self.groupBox_25)


        self.verticalLayout_14.addWidget(self.microscopeParamsGroupBox_4)

        self.gridLayout_54 = QGridLayout()
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.prjOTFPushButton_2 = QPushButton(self.tab_3)
        self.prjOTFPushButton_2.setObjectName(u"prjOTFPushButton_2")

        self.gridLayout_54.addWidget(self.prjOTFPushButton_2, 0, 1, 1, 1)

        self.prjPlotImageCrsPushButton_2 = QPushButton(self.tab_3)
        self.prjPlotImageCrsPushButton_2.setObjectName(u"prjPlotImageCrsPushButton_2")

        self.gridLayout_54.addWidget(self.prjPlotImageCrsPushButton_2, 1, 2, 1, 1)

        self.prjRunPushButton_2 = QPushButton(self.tab_3)
        self.prjRunPushButton_2.setObjectName(u"prjRunPushButton_2")

        self.gridLayout_54.addWidget(self.prjRunPushButton_2, 0, 2, 1, 1)

        self.prjPSFcrsPushButton_2 = QPushButton(self.tab_3)
        self.prjPSFcrsPushButton_2.setObjectName(u"prjPSFcrsPushButton_2")

        self.gridLayout_54.addWidget(self.prjPSFcrsPushButton_2, 0, 4, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_54.addItem(self.horizontalSpacer_14, 0, 0, 1, 1)

        self.prjPlotPSFCrspushButton_2 = QPushButton(self.tab_3)
        self.prjPlotPSFCrspushButton_2.setObjectName(u"prjPlotPSFCrspushButton_2")

        self.gridLayout_54.addWidget(self.prjPlotPSFCrspushButton_2, 1, 4, 1, 1)


        self.verticalLayout_14.addLayout(self.gridLayout_54)

        self.gridLayout_55 = QGridLayout()
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.prjCalcuratedOTFGroupBox_2 = QGroupBox(self.tab_3)
        self.prjCalcuratedOTFGroupBox_2.setObjectName(u"prjCalcuratedOTFGroupBox_2")
        self.gridLayout_60 = QGridLayout(self.prjCalcuratedOTFGroupBox_2)
        self.gridLayout_60.setObjectName(u"gridLayout_60")

        self.gridLayout_55.addWidget(self.prjCalcuratedOTFGroupBox_2, 0, 1, 1, 1)

        self.prjPSFcrsGroupBox_2 = QGroupBox(self.tab_3)
        self.prjPSFcrsGroupBox_2.setObjectName(u"prjPSFcrsGroupBox_2")
        self.gridLayout_58 = QGridLayout(self.prjPSFcrsGroupBox_2)
        self.gridLayout_58.setObjectName(u"gridLayout_58")

        self.gridLayout_55.addWidget(self.prjPSFcrsGroupBox_2, 0, 4, 1, 1)

        self.prjResultProjectedImageGroupBox_2 = QGroupBox(self.tab_3)
        self.prjResultProjectedImageGroupBox_2.setObjectName(u"prjResultProjectedImageGroupBox_2")
        self.gridLayout_57 = QGridLayout(self.prjResultProjectedImageGroupBox_2)
        self.gridLayout_57.setObjectName(u"gridLayout_57")

        self.gridLayout_55.addWidget(self.prjResultProjectedImageGroupBox_2, 0, 2, 1, 1)

        self.prjResultDefocusedImageGroupBox_2 = QGroupBox(self.tab_3)
        self.prjResultDefocusedImageGroupBox_2.setObjectName(u"prjResultDefocusedImageGroupBox_2")
        self.gridLayout_59 = QGridLayout(self.prjResultDefocusedImageGroupBox_2)
        self.gridLayout_59.setObjectName(u"gridLayout_59")

        self.gridLayout_55.addWidget(self.prjResultDefocusedImageGroupBox_2, 0, 3, 1, 1)

        self.prjLoadedImageGroupBox_2 = QGroupBox(self.tab_3)
        self.prjLoadedImageGroupBox_2.setObjectName(u"prjLoadedImageGroupBox_2")
        self.gridLayout_56 = QGridLayout(self.prjLoadedImageGroupBox_2)
        self.gridLayout_56.setObjectName(u"gridLayout_56")

        self.gridLayout_55.addWidget(self.prjLoadedImageGroupBox_2, 0, 0, 1, 1)


        self.verticalLayout_14.addLayout(self.gridLayout_55)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout_61.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.terminalGroupBox = QGroupBox(self.centralwidget)
        self.terminalGroupBox.setObjectName(u"terminalGroupBox")
        self.gridLayout_10 = QGridLayout(self.terminalGroupBox)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.terminalTextEdit = QTextEdit(self.terminalGroupBox)
        self.terminalTextEdit.setObjectName(u"terminalTextEdit")

        self.gridLayout_10.addWidget(self.terminalTextEdit, 0, 0, 1, 1)


        self.gridLayout_61.addWidget(self.terminalGroupBox, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1220, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Grating Simulrator ver 1.0.0", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Review the parameter guide", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Initialize", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"General Parameters", None))
        self.headerLabel.setText(QCoreApplication.translate("MainWindow", u"Header (Prefix)", None))
        self.headerLineEdit.setText(QCoreApplication.translate("MainWindow", u"test_", None))
        self.samplingPixelSizeUmLabel.setText(QCoreApplication.translate("MainWindow", u"Sampling Pixel Size [um]", None))
        self.invertReusltLabel.setText(QCoreApplication.translate("MainWindow", u"Invert Reuslt", None))
        self.saveReulstLabel.setText(QCoreApplication.translate("MainWindow", u"Save Reulst", None))
        self.pushButton_save.setText(QCoreApplication.translate("MainWindow", u"Save As Json", None))
        self.pushButton_load.setText(QCoreApplication.translate("MainWindow", u"Load Json", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Grating Parameters", None))
        self.periodOfPatternUmLabel.setText(QCoreApplication.translate("MainWindow", u"Period of Pattern [um]", None))
        self.heightOfSawtoothUmLabel.setText(QCoreApplication.translate("MainWindow", u"Height of Sawtooth [um]", None))
        self.periodOfSawtoothUmLabel.setText(QCoreApplication.translate("MainWindow", u"Period of Sawtooth [um]", None))
        self.widthOfStemUmLabel.setText(QCoreApplication.translate("MainWindow", u"Width of Stem [um]", None))
        self.offsetBtwLinesLabel.setText(QCoreApplication.translate("MainWindow", u"Offset btw Lines", None))
        self.parameterConsistencyCheckLabel.setText(QCoreApplication.translate("MainWindow", u"Parameter Consistency Check", None))
        self.numOfLinesLabel.setText(QCoreApplication.translate("MainWindow", u"Num of Lines", None))
        self.lengthOfLineUmLabel.setText(QCoreApplication.translate("MainWindow", u"Length of Line [um]", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Review", None))
        self.imageHeightPxLabel.setText(QCoreApplication.translate("MainWindow", u"Image Height [px]", None))
        self.imageWidthPxLabel.setText(QCoreApplication.translate("MainWindow", u"Image Width [px]", None))
        self.imageHeightMmLabel.setText(QCoreApplication.translate("MainWindow", u"Image Height [mm]", None))
        self.imageWidthMmLabel.setText(QCoreApplication.translate("MainWindow", u"Image Width [mm]", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Advanced Parameters", None))
        self.EdgeRounderGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Edge Rounder", None))
        self.methodLabel.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.methodComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Auto", None))
        self.methodComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"None", None))
        self.methodComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"User", None))

        self.factorLabel.setText(QCoreApplication.translate("MainWindow", u"Factor", None))
        self.diameterOfEdgeOfSawtoothUmLabel.setText(QCoreApplication.translate("MainWindow", u"Diameter of Edge of Sawtooth [um]", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Grating Before Rounding", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Grating After Rounding", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Genetated Grating Mask", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gratingGeneratorTab), QCoreApplication.translate("MainWindow", u"Grating Generator", None))
        self.OTFPushButton.setText(QCoreApplication.translate("MainWindow", u"4. Calcurate OTF", None))
        self.RunPushButton.setText(QCoreApplication.translate("MainWindow", u"5. Generate Microscope Image", None))
        self.microscopeParamsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"General Parameters (based on EPI Incoherent Microscopy)", None))
        self.headerLabel_2.setText(QCoreApplication.translate("MainWindow", u"Header (Prefix)", None))
        self.nAOfOpticsLabel.setText(QCoreApplication.translate("MainWindow", u"NA of Optics", None))
        self.saveResultLabel.setText(QCoreApplication.translate("MainWindow", u"Save Result", None))
        self.headerLineEdit_2.setText(QCoreApplication.translate("MainWindow", u"test_", None))
        self.simulationConditionLabel.setText(QCoreApplication.translate("MainWindow", u"Simulation Condition", None))
        self.customSpectrumGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Custom Source Spectrum", None))
        self.spectrumMinUmLabel.setText(QCoreApplication.translate("MainWindow", u"Spectrum Min [um]", None))
        self.spectrumMaxUmLabel.setText(QCoreApplication.translate("MainWindow", u"Spectrum Max [um]", None))
        self.spectrumStepLabel.setText(QCoreApplication.translate("MainWindow", u"Spectrum Step", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Input Image Parameters", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.samplingSizeUmLabel.setText(QCoreApplication.translate("MainWindow", u"Sampling Size [um]", None))
        self.groupBox_29.setTitle(QCoreApplication.translate("MainWindow", u"Review", None))
        self.heightPxLabel.setText(QCoreApplication.translate("MainWindow", u"Height [px]", None))
        self.widthPxLabel.setText(QCoreApplication.translate("MainWindow", u"Width [px]", None))
        self.heightMmLabel.setText(QCoreApplication.translate("MainWindow", u"Height [mm]", None))
        self.widthMmLabel.setText(QCoreApplication.translate("MainWindow", u"Width [mm]", None))
        self.loadedImageGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Loaded Image", None))
        self.calcuratedOTFGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Calcurated OTF (depend on NA & Sampling Size)", None))
        self.resultImageGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Result Image", None))
        self.initializePushButton.setText(QCoreApplication.translate("MainWindow", u"3. Initialize", None))
        self.loadGratingPushButton.setText(QCoreApplication.translate("MainWindow", u"1. Load Grating image (*.bmp)", None))
        self.loadGratingParamsPushButton.setText(QCoreApplication.translate("MainWindow", u"2. Load Grating Parameter (*.json)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.microscopeImageSimulatorTab), QCoreApplication.translate("MainWindow", u"Microscope Image Simulator", None))
        self.prjLoadGratingPushButton.setText(QCoreApplication.translate("MainWindow", u"1. Load Grating image (*.bmp)", None))
        self.prjLoadGratingParamsPushButton.setText(QCoreApplication.translate("MainWindow", u"2. Load Grating Parameter (*.json)", None))
        self.prjInitializePushButton.setText(QCoreApplication.translate("MainWindow", u"3. Initialize", None))
        self.prjAutoInitializeCheckBox.setText(QCoreApplication.translate("MainWindow", u"Auto Initialize", None))
        self.microscopeParamsGroupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.groupBox_26.setTitle(QCoreApplication.translate("MainWindow", u"General Parameters", None))
        self.headerPrefixLabel.setText(QCoreApplication.translate("MainWindow", u"Header (Prefix)", None))
        self.prjHeaderPrefixLineEdit.setText(QCoreApplication.translate("MainWindow", u"test_", None))
        self.prjHeaderPrefixLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"test_", None))
        self.saveResultLabel_4.setText(QCoreApplication.translate("MainWindow", u"Save Result", None))
        self.simulationConditionLabel_4.setText(QCoreApplication.translate("MainWindow", u"Simulation Condition", None))
        self.prjCustomSpectrumGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Custom Source Spectrum", None))
        self.spectrumMinUmLabel_3.setText(QCoreApplication.translate("MainWindow", u"Spectrum Min [um]", None))
        self.spectrumMaxUmLabel_3.setText(QCoreApplication.translate("MainWindow", u"Spectrum Max [um]", None))
        self.spectrumStepLabel_3.setText(QCoreApplication.translate("MainWindow", u"Spectrum Step", None))
        self.prjPushButton_save.setText(QCoreApplication.translate("MainWindow", u"Save As Json", None))
        self.prjPushButton_load.setText(QCoreApplication.translate("MainWindow", u"Load Json", None))
        self.groupBox_27.setTitle(QCoreApplication.translate("MainWindow", u"Projection Parameters", None))
        self.z0GratingToLensMmLabel.setText(QCoreApplication.translate("MainWindow", u"z0 (grating to lens) [mm]", None))
        self.z1LensToProjectionPlaneMmLabel.setText(QCoreApplication.translate("MainWindow", u"z1 (lens to projection plane) [mm]", None))
        self.pupilDiameterMmLabel.setText(QCoreApplication.translate("MainWindow", u"Pupil Diameter [mm]", None))
        self.defocusMmLabel.setText(QCoreApplication.translate("MainWindow", u"Defocus [mm]", None))
        self.resizeFactorPixelBinningLabel.setText(QCoreApplication.translate("MainWindow", u"Resize Factor along height (pixel binning)", None))
        self.resizeFactorAlongHeightPixelBinningLabel.setText(QCoreApplication.translate("MainWindow", u"Resize Factor along width (pixel binning)", None))
        self.prjEdgeRemoverGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Edge Remover", None))
        self.edgeRemoverFactorLabel.setText(QCoreApplication.translate("MainWindow", u"Edge Remover Factor", None))
        self.groupBox_28.setTitle(QCoreApplication.translate("MainWindow", u"Review", None))
        self.objectSpaceFLabel.setText(QCoreApplication.translate("MainWindow", u"Object Space f/#", None))
        self.imageSpaceNALabel.setText(QCoreApplication.translate("MainWindow", u"Image Space NA", None))
        self.magnificationLabel.setText(QCoreApplication.translate("MainWindow", u"Magnification", None))
        self.projectedImageHeightMmLabel.setText(QCoreApplication.translate("MainWindow", u"Projected Image Height [mm]", None))
        self.fullDepthOfFieldMmLabel.setText(QCoreApplication.translate("MainWindow", u"Full Depth of Field [mm]", None))
        self.projectedImageWidthMmLabel.setText(QCoreApplication.translate("MainWindow", u"Projected Image Width  [mm]", None))
        self.projectedImageSamplingSizeUmLabel.setText(QCoreApplication.translate("MainWindow", u"Projected Image Sampling Size [um]", None))
        self.resizedImageHeightMmLabel.setText(QCoreApplication.translate("MainWindow", u"Resized Image Height [mm]", None))
        self.resizedImageWidthMmLabel.setText(QCoreApplication.translate("MainWindow", u"Resized Image Width [mm]", None))
        self.resizedImageSamplingSizeUmLabel.setText(QCoreApplication.translate("MainWindow", u"Resized Image Sampling Size [um]", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("MainWindow", u"Input Image Parameters", None))
        self.groupBox_30.setTitle(QCoreApplication.translate("MainWindow", u"Review", None))
        self.prjCustomImagePropertyGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.samplingSizeUmLabel_3.setText(QCoreApplication.translate("MainWindow", u"Sampling Size [um]", None))
        self.periodOfSawtoothUmLabel_3.setText(QCoreApplication.translate("MainWindow", u"Period of Sawtooth [um]", None))
        self.heightMmLabel_3.setText(QCoreApplication.translate("MainWindow", u"Height [mm]", None))
        self.widthMmLabel_3.setText(QCoreApplication.translate("MainWindow", u"Width [mm]", None))
        self.heightPxLabel_3.setText(QCoreApplication.translate("MainWindow", u"Height [px]", None))
        self.widthPxLabel_3.setText(QCoreApplication.translate("MainWindow", u"Width [px]", None))
        self.prjOTFPushButton.setText(QCoreApplication.translate("MainWindow", u"4. Calcurate OTF", None))
        self.prjPlotImageCrsPushButton.setText(QCoreApplication.translate("MainWindow", u"6. Plot Image CrossSection", None))
        self.prjRunPushButton.setText(QCoreApplication.translate("MainWindow", u"5. Generate Projected Image", None))
        self.prjPSFcrsPushButton.setText(QCoreApplication.translate("MainWindow", u"(optional) Create ZX PSF CrossSection", None))
        self.prjPlotPSFCrspushButton.setText(QCoreApplication.translate("MainWindow", u"Plot PSF Profile", None))
        self.prjLoadedImageGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Loaded Image", None))
        self.prjResultProjectedImageGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Projected Image", None))
        self.prjPSFcrsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"ZX PSF CrossSection", None))
        self.prjResultDefocusedImageGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Projected Image (defocused)", None))
        self.prjCalcuratedOTFGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Calcurated OTF (depend on NA & Sampling Size)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Grating Projection Simulator", None))
        self.aswLoadProjectedFlatImagePushButton.setText(QCoreApplication.translate("MainWindow", u"1. Load Projected Flat Image (*.bmp)", None))
        self.aswLoadProjectorParamsPushButton.setText(QCoreApplication.translate("MainWindow", u"2. Load Projector Parameter (*.json)", None))
        self.aswInitializePushButton.setText(QCoreApplication.translate("MainWindow", u"3. Initialize", None))
        self.microscopeParamsGroupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.groupBox_31.setTitle(QCoreApplication.translate("MainWindow", u"General Parameters", None))
        self.prjPushButton_save_2.setText(QCoreApplication.translate("MainWindow", u"Save As Json", None))
        self.prjPushButton_load_2.setText(QCoreApplication.translate("MainWindow", u"Load Json", None))
        self.headerPrefixLabel_2.setText(QCoreApplication.translate("MainWindow", u"Header (Prefix)", None))
        self.prjHeaderPrefixLineEdit_2.setText(QCoreApplication.translate("MainWindow", u"test_", None))
        self.prjHeaderPrefixLineEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"test_", None))
        self.saveResultLabel_5.setText(QCoreApplication.translate("MainWindow", u"Save Result", None))
        self.stretchImageToSquareLabel.setText(QCoreApplication.translate("MainWindow", u"Stretch Image to Square", None))
        self.groupBox_32.setTitle(QCoreApplication.translate("MainWindow", u"Scheimpflug Parameters", None))
        self.xProjectionAngleDegLabel.setText(QCoreApplication.translate("MainWindow", u"X Projection angle [deg]", None))
        self.yProjectionAngleDegLabel.setText(QCoreApplication.translate("MainWindow", u"Y Projection angle [deg]", None))
        self.prjEdgeRemoverGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Edge Remover", None))
        self.edgeRemoverFactorLabel_2.setText(QCoreApplication.translate("MainWindow", u"Edge Remover Factor", None))
        self.groupBox_33.setTitle(QCoreApplication.translate("MainWindow", u"Review", None))
        self.z1WDefocusLensToPlaneMmLabel.setText(QCoreApplication.translate("MainWindow", u"z1 w/ defocus (lens to plane) [mm]", None))
        self.xGratingTiltAngleDegLabel.setText(QCoreApplication.translate("MainWindow", u"X Grating tilt angle [deg]", None))
        self.yGratingTiltAngleDegLabel.setText(QCoreApplication.translate("MainWindow", u"Y Grating tilt angle [deg]", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("MainWindow", u"Input Image Parameters", None))
        self.groupBox_34.setTitle(QCoreApplication.translate("MainWindow", u"Review", None))
        self.prjCustomImagePropertyGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.samplingSizeUmLabel_4.setText(QCoreApplication.translate("MainWindow", u"Sampling Size [um]", None))
        self.heightMmLabel_4.setText(QCoreApplication.translate("MainWindow", u"Height [mm]", None))
        self.widthMmLabel_4.setText(QCoreApplication.translate("MainWindow", u"Width [mm]", None))
        self.heightPxLabel_4.setText(QCoreApplication.translate("MainWindow", u"Height [px]", None))
        self.widthPxLabel_4.setText(QCoreApplication.translate("MainWindow", u"Width [px]", None))
        self.z0GratingToLensMmLabel_2.setText(QCoreApplication.translate("MainWindow", u"z0 (grating to lens) [mm]", None))
        self.z1LensToProjectionPlaneMmLabel_2.setText(QCoreApplication.translate("MainWindow", u"z1 (lens to projection plane) [mm]", None))
        self.defocusMmLabel_2.setText(QCoreApplication.translate("MainWindow", u"Defocus [mm]", None))
        self.prjOTFPushButton_2.setText(QCoreApplication.translate("MainWindow", u"4. Calcurate OTF", None))
        self.prjPlotImageCrsPushButton_2.setText(QCoreApplication.translate("MainWindow", u"6. Plot Image CrossSection", None))
        self.prjRunPushButton_2.setText(QCoreApplication.translate("MainWindow", u"5. Generate Projected Image", None))
        self.prjPSFcrsPushButton_2.setText(QCoreApplication.translate("MainWindow", u"(optional) Create ZX PSF CrossSection", None))
        self.prjPlotPSFCrspushButton_2.setText(QCoreApplication.translate("MainWindow", u"Plot PSF Profile", None))
        self.prjCalcuratedOTFGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Calcurated OTF (depend on NA & Sampling Size)", None))
        self.prjPSFcrsGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"ZX PSF CrossSection", None))
        self.prjResultProjectedImageGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Projected Image", None))
        self.prjResultDefocusedImageGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Projected Image (defocused)", None))
        self.prjLoadedImageGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Loaded Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Apply Scheimpflug Wizard", None))
        self.terminalGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Terminal Output", None))
    # retranslateUi

