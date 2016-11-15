#!/usr/bin/env python3
#
# This is the main GUI function for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import os
import time
import sys
try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from PyQt5.QtCore import QTimer, Qt, QCoreApplication, QObject, pyqtSignal
    from PyQt5.QtGui import QColor, QPalette
    from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMessageBox, QVBoxLayout, QHBoxLayout
    from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QGroupBox, QPushButton, QRadioButton, QLineEdit, QFileDialog
except ImportError:
    from tkinter import messagebox
    messagebox.showinfo(message='Please close this dialog and install dependencies typing the following in terminal:\n'
                                'python3\n'
                                'from Coliform import InitialSetup\n'
                                'InitialSetup.addShortcuts()\n'
                                'InitialSetup.installDependencies()\n')
from Coliform import OneWire, MultiPlot, RPiGPIO, RPiCamera, RGBSensor
import threading

# from datetime import datetime
'''
import as:
from Coliform import GUI
use as:
GUI.startGUI()
'''


class GUICenterWidget(QWidget):
    def __init__(self):
        super(GUICenterWidget, self).__init__()
        self.initUI()
        self.start_time = time.time()

    def initUI(self):
        self.tf = 'PlotTextFile.txt'

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.topLeftGroupBox)
        topLayout.addWidget(self.topRightGroupBox)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.bottomLeftGroupBox)
        bottomLayout.addWidget(self.bottomRightGroupBox)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

        self.show()

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Temperature Sensor")

        tempLabel = QLabel('Temperature: ')
        self.tempValLabel = QLabel('NULL')

        plotButton = QPushButton("Show Plot")
        plotButton.clicked.connect(self.tempPlot)
        saveDataButton = QPushButton('Save Data File')
        saveDataButton.clicked.connect(self.savefile)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(tempLabel)
        vbox1.addWidget(self.tempValLabel)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(plotButton)
        vbox2.addWidget(saveDataButton)

        layout = QHBoxLayout()
        layout.addLayout(vbox1)
        layout.addLayout(vbox2)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox('Heater')

        heatLabel = QLabel('Target Temperature(C):')
        heatEntry = QLineEdit()
        heatEntry.textChanged[str].connect(self.tempOnChanged)
        heatEntry.setText('41')

        self.heatButton = QPushButton('Heater ON')
        self.heatButton.clicked.connect(self.heaterPower)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(heatLabel)
        hbox1.addWidget(heatEntry)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.heatButton)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox('Pump')

        self.pumpPowerButton = QPushButton('Power ON')
        self.pumpPowerButton.clicked.connect(self.pumpPower)

        pumpEntry = QLineEdit()
        pumpEntry.textChanged[str].connect(self.pumpOnChanged)
        pumpValChangeButton = QPushButton('Submit')
        pumpValChangeButton.clicked.connect(self.pumppowerchange)


        layout = QVBoxLayout()
        layout.addWidget(self.pumpPowerButton)
        layout.addWidget(pumpEntry)
        layout.addWidget(pumpValChangeButton)
        layout.addStretch(1)
        self.bottomLeftGroupBox.setLayout(layout)

    def tempOnChanged(self, text):
        if text != '':
            self.tempTarget = int(float(text))

    def pumpOnChanged(self, text):
        if text:
           self.pumppwmvalue = int(float(text))

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox('Status')

        self.tempSensorLbl = QLabel('Temp. Sensor OFF')
        self.pumpLbl = QLabel('Pump OFF')
        self.heatLbl = QLabel('Heater OFF')

        layout = QVBoxLayout()
        layout.addWidget(self.tempSensorLbl)
        layout.addWidget(self.pumpLbl)
        layout.addWidget(self.heatLbl)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

    def statusOnChanged(self, text):
        if 'Temp. Sensor' in text:
            self.tempSensorStatus = text
            self.tempSensorLbl.adjustSize()
        elif 'Pump' in text:
            self.pumpStatus = text
            self.pumpLbl.adjustSize()
        elif 'Heater' in text:
            self.heatStatus = text
            self.heatLbl.adjustSize()

    def onewireOn(self):
        try:
            self.ids = OneWire.getOneWireID()
            TemperatureDegrees, self.TemperatureNumber = OneWire.getTempList()
            self.tempValLabel.setText(TemperatureDegrees)
            MultiPlot.GeneratePlotDataFile(self.tf, self.TemperatureNumber, self.start_time)
            if not self.ids:
                self.tempSensorLbl.setText('Temp. Sensor OFF')
                self.tempValLabel.setText('NULL')
                self.tempValLabel.adjustSize()
            else:
                self.tempSensorLbl.setText('Temp. Sensor ON')
                self.tempValLabel.adjustSize()
        except IndexError:
            pass

    def tempPlot(self):
        try:
            MultiPlot.Plot(self.tf, len(self.ids))
        except KeyError:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Information)
            mb.setWindowTitle('Error')
            mb.setText('No temperature sensor connected.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.show()

    def pumpPower(self):
        if 'OFF' in self.pumpLbl.text():
            self.PUMPPWM = RPiGPIO.Controller(11, 100)
            self.PUMPPWM.startup()
            self.pumpLbl.setText('Pump ON')
            self.pumpPowerButton.setText('Power OFF')
        elif 'ON' in self.pumpLbl.text():
            self.PUMPPWM.shutdown()
            self.pumpLbl.setText('Pump OFF')
            self.pumpPowerButton.setText('Power ON')

    def savefile(self):
        tempfilename = 'TemperatureData.csv'
        filepath = QFileDialog.getExistingDirectory(self, 'Choose Directory', os.sep.join((os.path.expanduser('~'), 'Desktop')))
        MultiPlot.SaveToCsv(self.tf, tempfilename, filepath, len(self.ids))
        mb = QMessageBox()
        mb.setIcon(QMessageBox.Information)
        mb.setWindowTitle('Information')
        mb.setText('File saved to directory.')
        mb.setStandardButtons(QMessageBox.Ok)
        mb.show()

    def heaterPower(self):
        if 'OFF' in self.heatLbl.text():
            self.heatLbl.setText('Heater ON')
            self.heatButton.setText('Power OFF')
            self.HEATPWM = RPiGPIO.Controller(12, 100)
            self.HEATPWM.startup()
        elif 'ON' in self.heatLbl.text():
            self.HEATPWM.shutdown()
            self.heatLbl.setText('Heater OFF')
            self.heatButton.setText('Power ON')

    def heaterinput(self):
        if self.heatLbl.text() != 'Heater OFF':
            value = float(self.tempTarget)
            sensor = float(self.TemperatureNumber[1])
            self.HEATPWM.HeaterPID(value, sensor)

    def pumppowerchange(self):
        try:
            if self.pumppwmvalue > 100:
                raise ValueError
            else:
                self.PUMPPWM.setIntensity(self.pumppwmvalue)
        except ValueError:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Information)
            mb.setWindowTitle('Error')
            mb.setText('Please type in a value between 0-100.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.show()


class GUIMainWindow(QMainWindow):
    def __init__(self):
        super(GUIMainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # QToolTip.setFont(QFont('SansSerif', 9))

        self.cwidget = GUICenterWidget()
        self.setCentralWidget(self.cwidget)

        # self.setToolTip('This is a <b>QWidget</b> widget')

        self.statusBar().showMessage('Ready')

        self.center()
        self.setWindowTitle('Coliform Control GUI')

        self.onewiretimer = QTimer(self)
        self.onewiretimer.timeout.connect(self.cwidget.onewireOn)
        self.onewiretimer.start(1000)

        # self.p = QPalette(self.palette())
        # self.p.setColor(QPalette.Window, QColor(53, 53, 53))
        # self.p.setColor(QPalette.WindowText, Qt.white)
        # self.p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # self.p.setColor(QPalette.ToolTipBase, Qt.white)
        # self.p.setColor(QPalette.ToolTipText, Qt.white)
        # self.p.setColor(QPalette.Button, QColor(53, 53, 53))
        # self.p.setColor(QPalette.ButtonText, Qt.white)
        # self.p.setColor(QPalette.BrightText, Qt.red)
        # self.p.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        # self.p.setColor(QPalette.HighlightedText, Qt.black)
        # self.setPalette(self.p)

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def quitApp(self):
        QCoreApplication.instance().quit()


class CameraCenterWidget(QWidget):
    def __init__(self):
        super(CameraCenterWidget, self).__init__()
        self.initUI()
        # self.start_time = time.time()

    def initUI(self):
        self.tf = 'PlotTextFile.txt'

        self.statusbar = 'Ready'
        self.createTopGroupBox()
        self.createMidTopGroupBox()
        self.createMidBottomGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()

        topLayout = QVBoxLayout()
        topLayout.addWidget(self.topGroupBox)
        topLayout.addWidget(self.midTopGroupBox)
        topLayout.addWidget(self.midBottomGroupBox)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.bottomLeftGroupBox)
        bottomLayout.addWidget(self.bottomRightGroupBox)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

        self.show()

    def createTopGroupBox(self):
        self.topGroupBox = QGroupBox("Camera Capture Parameters")

        delayLbl = QLabel('Delay:')
        self.delayEntry = QLineEdit()
        self.delayEntry.setText('5')

        brightLbl = QLabel('Brightness:')
        self.brightEntry = QLineEdit()
        self.brightEntry.setText('50')

        contrastLbl = QLabel('Contrast:')
        self.contrastEntry = QLineEdit()
        self.contrastEntry.setText('0')

        shutterLbl = QLabel('Shutter Speed(μs)')
        self.shutterEntry = QLineEdit()
        self.shutterEntry.setText('0')
        # Line 2
        isoLbl = QLabel('ISO:')
        self.isoEntry = QLineEdit()
        self.isoEntry.setText('0')

        prevTimeLbl = QLabel('Preview Timeout:')
        self.prevTimeEntry = QLineEdit()
        self.prevTimeEntry.setText('10')

        resLbl = QLabel('Resolution:')
        self.resEntry = QLineEdit()
        self.resEntry.setText('2592x1944')

        zoomLbl = QLabel('Zoom:')
        self.zoomEntry = QLineEdit()
        self.zoomEntry.setText('0.0, 0.0, 1.0, 1.0')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(delayLbl)
        hbox1.addWidget(self.delayEntry)
        hbox1.addWidget(brightLbl)
        hbox1.addWidget(self.brightEntry)
        hbox1.addWidget(contrastLbl)
        hbox1.addWidget(self.contrastEntry)
        hbox1.addWidget(shutterLbl)
        hbox1.addWidget(self.shutterEntry)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(isoLbl)
        hbox2.addWidget(self.isoEntry)
        hbox2.addWidget(prevTimeLbl)
        hbox2.addWidget(self.prevTimeEntry)
        hbox2.addWidget(resLbl)
        hbox2.addWidget(self.resEntry)
        hbox2.addWidget(zoomLbl)
        hbox2.addWidget(self.zoomEntry)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addStretch(1)
        self.topGroupBox.setLayout(layout)

    def createMidTopGroupBox(self):
        self.midTopGroupBox = QGroupBox('Auto White Balance Modes')

        self.autoAwb = QRadioButton()
        self.autoAwb.setText('auto')
        self.autoAwb.toggled.connect(lambda: self.abtnstate(self.autoAwb))

        self.fluorAwb = QRadioButton()
        self.fluorAwb.setText('fluorescent')
        self.fluorAwb.toggled.connect(lambda: self.abtnstate(self.fluorAwb))

        self.incanAwb = QRadioButton()
        self.incanAwb.setText('incandescent')
        self.incanAwb.toggled.connect(lambda: self.abtnstate(self.incanAwb))

        self.offAwb = QRadioButton()
        self.offAwb.setText('off')
        self.offAwb.toggled.connect(lambda: self.abtnstate(self.offAwb))

        self.defaultAwb = QRadioButton()
        self.defaultAwb.setText('default')
        self.defaultAwb.toggled.connect(lambda: self.abtnstate(self.defaultAwb))

        self.sunAwb = QRadioButton()
        self.sunAwb.setText('sun')
        self.sunAwb.toggled.connect(lambda: self.abtnstate(self.sunAwb))

        self.cloudAwb = QRadioButton()
        self.cloudAwb.setText('cloud')
        self.cloudAwb.toggled.connect(lambda: self.abtnstate(self.cloudAwb))

        self.shadeAwb = QRadioButton()
        self.shadeAwb.setText('shade')
        self.shadeAwb.toggled.connect(lambda: self.abtnstate(self.shadeAwb))

        self.tungsAwb = QRadioButton()
        self.tungsAwb.setText('tungsten')
        self.tungsAwb.toggled.connect(lambda: self.abtnstate(self.tungsAwb))

        self.flashAwb = QRadioButton()
        self.flashAwb.setText('flash')
        self.flashAwb.toggled.connect(lambda: self.abtnstate(self.flashAwb))

        self.horizonAwb = QRadioButton()
        self.horizonAwb.setText('horizon')
        self.horizonAwb.toggled.connect(lambda: self.abtnstate(self.horizonAwb))

        self.defaultAwb.setChecked(True)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.autoAwb)
        hbox1.addWidget(self.fluorAwb)
        hbox1.addWidget(self.incanAwb)
        hbox1.addWidget(self.offAwb)
        hbox1.addWidget(self.defaultAwb)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.sunAwb)
        hbox2.addWidget(self.cloudAwb)
        hbox2.addWidget(self.shadeAwb)
        hbox2.addWidget(self.tungsAwb)
        hbox2.addWidget(self.flashAwb)
        hbox2.addWidget(self.horizonAwb)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addStretch(1)
        self.midTopGroupBox.setLayout(layout)

    def createMidBottomGroupBox(self):
        self.midBottomGroupBox = QGroupBox('Exposure Modes')

        self.autoExp = QRadioButton()
        self.autoExp.setText('auto')
        self.autoExp.toggled.connect(lambda: self.btnstate(self.autoExp))

        self.nightExp = QRadioButton()
        self.nightExp.setText('night')
        self.nightExp.toggled.connect(lambda: self.btnstate(self.nightExp))

        self.offExp = QRadioButton()
        self.offExp.setText('off')
        self.offExp.toggled.connect(lambda: self.btnstate(self.offExp))

        self.defaultExp = QRadioButton()
        self.defaultExp.setText('default')
        self.defaultExp.toggled.connect(lambda: self.btnstate(self.defaultExp))

        self.sportsExp = QRadioButton()
        self.sportsExp.setText('sports')
        self.sportsExp.toggled.connect(lambda: self.btnstate(self.sportsExp))

        self.longExp = QRadioButton()
        self.longExp.setText('verylong')
        self.longExp.toggled.connect(lambda: self.btnstate(self.longExp))

        self.spotExp = QRadioButton()
        self.spotExp.setText('spotlight')
        self.spotExp.toggled.connect(lambda: self.btnstate(self.spotExp))

        self.backExp = QRadioButton()
        self.backExp.setText('backlight')
        self.backExp.toggled.connect(lambda: self.btnstate(self.backExp))

        self.fireExp = QRadioButton()
        self.fireExp.setText('fireworks')
        self.fireExp.toggled.connect(lambda: self.btnstate(self.fireExp))

        self.antiExp = QRadioButton()
        self.antiExp.setText('antishake')
        self.antiExp.toggled.connect(lambda: self.btnstate(self.antiExp))

        self.fixedExp = QRadioButton()
        self.fixedExp.setText('fixedfps')
        self.fixedExp.toggled.connect(lambda: self.btnstate(self.fixedExp))

        self.beachExp = QRadioButton()
        self.beachExp.setText('beach')
        self.beachExp.toggled.connect(lambda: self.btnstate(self.beachExp))

        self.snowExp = QRadioButton()
        self.snowExp.setText('snow')
        self.snowExp.toggled.connect(lambda: self.btnstate(self.snowExp))

        self.nightpExp = QRadioButton()
        self.nightpExp.setText('nightpreview')
        self.nightpExp.toggled.connect(lambda: self.btnstate(self.nightpExp))

        self.defaultExp.setChecked(True)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.autoExp)
        hbox1.addWidget(self.longExp)
        hbox1.addWidget(self.nightExp)
        hbox1.addWidget(self.defaultExp)
        hbox1.addWidget(self.spotExp)
        hbox1.addWidget(self.sportsExp)
        hbox1.addWidget(self.offExp)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.backExp)
        hbox2.addWidget(self.fireExp)
        hbox2.addWidget(self.antiExp)
        hbox2.addWidget(self.fixedExp)
        hbox2.addWidget(self.beachExp)
        hbox2.addWidget(self.snowExp)
        hbox2.addWidget(self.nightpExp)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addStretch(1)
        self.midBottomGroupBox.setLayout(layout)

    def abtnstate(self, state):
        if state.text() == 'auto':
            if state.isChecked():
                self.awbvar = 'auto'
        elif state.text() == 'fluorescent':
            if state.isChecked():
                self.awbvar = 'fluorescent'
        elif state.text() == 'incandescent':
            if state.isChecked():
                self.awbvar = 'incandescent'
        elif state.text() == 'off':
            if state.isChecked():
                self.awbvar = 'off'
        elif state.text() == 'default':
            if state.isChecked():
                self.awbvar = ''
        elif state.text() == 'sun':
            if state.isChecked():
                self.awbvar = 'sun'
        elif state.text() == 'cloud':
            if state.isChecked():
                self.awbvar = 'cloud'
        elif state.text() == 'shade':
            if state.isChecked():
                self.awbvar = 'shade'
        elif state.text() == 'tungsten':
            if state.isChecked():
                self.awbvar = 'tungsten'
        elif state.text() == 'flash':
            if state.isChecked():
                self.awbvar = 'flash'
        elif state.text() == 'horizon':
            if state.isChecked():
                self.awbvar = 'horizon'

    def btnstate(self, state):
        if state.text() == 'auto':
            if state.isChecked():
                self.expvar = 'auto'
        elif state.text() == 'night':
            if state.isChecked():
                self.expvar = 'night'
        elif state.text() == 'verylong':
            if state.isChecked():
                self.expvar = 'verylong'
        elif state.text() == 'off':
            if state.isChecked():
                self.expvar = 'off'
        elif state.text() == 'default':
            if state.isChecked():
                self.expvar = ''
        elif state.text() == 'sports':
            if state.isChecked():
                self.expvar = 'sports'
        elif state.text() == 'spotlight':
            if state.isChecked():
                self.expvar = 'spotlight'
        elif state.text() == 'backlight':
            if state.isChecked():
                self.expvar = 'backlight'
        elif state.text() == 'fireworks':
            if state.isChecked():
                self.expvar = 'fireworks'
        elif state.text() == 'antishake':
            if state.isChecked():
                self.expvar = 'antishake'
        elif state.text() == 'fikedfps':
            if state.isChecked():
                self.expvar = 'fixedfps'
        if state.text() == 'beach':
            if state.isChecked():
                self.expvar = 'beach'
        elif state.text() == 'snow':
            if state.isChecked():
                self.expvar = 'snow'
        elif state.text() == 'nightpreview':
            if state.isChecked():
                self.expvar = 'nightpreview'

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox('Camera Options')

        captureBtn = QPushButton('Take Picture')
        captureBtn.clicked.connect(self.takePictureThread)

        setNormOptionsBtn = QPushButton('Set Normal Options')
        setNormOptionsBtn.clicked.connect(self.normalSettings)

        setDarkOptionsBtn = QPushButton('Set Low Light Options')
        setDarkOptionsBtn.clicked.connect(self.darkSettings)

        previewBtn = QPushButton('Camera Preview')
        previewBtn.clicked.connect(self.cameraPreviewThread)

        showPlotsBtn = QPushButton('Show Plots')
        showPlotsBtn.clicked.connect(self.showPlots)

        showImageBtn = QPushButton('Show Image')
        showImageBtn.clicked.connect(lambda: self.showImage(showImageBtn.text()))

        importImageBtn = QPushButton('Import Image')
        importImageBtn.clicked.connect(self.importImageThread)

        saveImageBtn = QPushButton('Save Image')
        saveImageBtn.clicked.connect(self.saveImage)

        showRedImageBtn = QPushButton('Show Red')
        showRedImageBtn.clicked.connect(lambda: self.showImage(showRedImageBtn.text()))

        showBlueImageBtn = QPushButton('Show Blue')
        showBlueImageBtn.clicked.connect(lambda: self.showImage(showBlueImageBtn.text()))

        showGreenImageBtn = QPushButton('Show Green')
        showGreenImageBtn.clicked.connect(lambda: self.showImage(showGreenImageBtn.text()))

        saveAllBtn = QPushButton('Save All')
        saveAllBtn.clicked.connect(self.saveAllThread)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(captureBtn)
        vbox1.addWidget(setNormOptionsBtn)
        vbox1.addWidget(setDarkOptionsBtn)
        vbox1.addWidget(previewBtn)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(showImageBtn)
        vbox2.addWidget(showPlotsBtn)
        vbox2.addWidget(importImageBtn)
        vbox2.addWidget(saveImageBtn)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(showRedImageBtn)
        vbox3.addWidget(showGreenImageBtn)
        vbox3.addWidget(showBlueImageBtn)
        vbox3.addWidget(saveAllBtn)

        layout = QHBoxLayout()
        layout.addLayout(vbox1)
        layout.addLayout(vbox2)
        layout.addLayout(vbox3)
        layout.addStretch(1)
        self.bottomLeftGroupBox.setLayout(layout)

    def takePictureThread(self):
        self.statusbar = 'Taking Picture...'

        captureThread = threading.Thread(target=self.takePicture)
        captureThread.start()

    def importImageThread(self):
        self.statusbar = 'Importing Image...'
        self.image = QFileDialog.getOpenFileName(self, 'Choose Image', os.sep.join((os.path.expanduser('~'), 'Desktop')),
                                                 'Image Files (*.png *.jpg *.jpeg)')
        importThread = threading.Thread(target=self.importImage)
        importThread.start()

    def cameraPreviewThread(self):
        self.statusbar = 'Loading Preview...'
        previewThread = threading.Thread(target=self.cameraPreview)
        previewThread.start()

    def saveAllThread(self):
        self.statusbar = 'Saving Files..'
        self.directory = QFileDialog.getExistingDirectory(self, 'Choose Directory', os.path.expanduser('~'))
        saveThread = threading.Thread(target=self.saveAll)
        saveThread.start()

    def takePicture(self):
        iso = int(float(self.isoEntry.text()))
        resolution_string = self.resEntry.text().split('x')
        resolution = (int(float(resolution_string[0])), int(float(resolution_string[1])))
        delay = int(float(self.delayEntry.text()))
        brightness = int(float(self.brightEntry.text()))
        contrast = int(float(self.contrastEntry.text()))
        shutterspeed = int(float(self.shutterEntry.text()))
        zoom = tuple(map(float, self.zoomEntry.text().split(',')))
        exposuremode = self.expvar
        awbmode = self.awbvar

        self.rgb_array = RPiCamera.takePicture(iso=iso, timeout=delay, resolution=resolution, exposure=exposuremode,
                                               brightness=brightness, contrast=contrast, shutterspeed=shutterspeed,
                                               zoom=zoom, awb_mode=awbmode)
        red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(self.rgb_array)
        intensity_array = '\n'.join(['R:' + '{:.3f}'.format(red_intensity),
                                     'G:' + '{:.3f}'.format(green_intensity),
                                     'B:' + '{:.3f}'.format(blue_intensity),
                                     'I:' + '{:.3f}'.format(intensity)])
        self.intensityLbl.setText(intensity_array)
        self.intensityLbl.adjustSize()
        self.statusbar = 'Ready'

    def normalSettings(self):
        self.delayEntry.setText('5')
        self.prevTimeEntry.setText('10')
        self.shutterEntry.setText('0')

    def darkSettings(self):
        self.delayEntry.setText('50')
        self.prevTimeEntry.setText('50')
        self.shutterEntry.setText('6000000')

    def cameraPreview(self):
        iso = int(float(self.isoEntry.text()))
        resolution_string = self.resEntry.text().split('x')
        resolution = (int(float(resolution_string[0])), int(float(resolution_string[1])))
        delay = int(float(self.prevTimeEntry.text()))
        brightness = int(float(self.brightEntry.text()))
        contrast = int(float(self.contrastEntry.text()))
        shutterspeed = int(float(self.shutterEntry.text()))
        zoom = tuple(map(float, self.zoomEntry.text().split(',')))
        exposuremode = self.expvar
        awbmode = self.awbvar

        RPiCamera.startPreview(iso=iso, timeout=delay, resolution=resolution, exposure=exposuremode,
                               brightness=brightness, contrast=contrast, shutterspeed=shutterspeed,
                               zoom=zoom, awb_mode=awbmode)
        self.statusbar = 'Ready'

    def showPlots(self):
        try:
            RPiCamera.showPlot(self.rgb_array)
            self.statusbar = 'Ready'
        except ValueError:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Information)
            mb.setWindowTitle('Error')
            mb.setText('Array not loaded, make sure you take picture or import an image first.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.show()

    def showImage(self, text):
        try:
            if text == 'Show Red':
                RPiCamera.showImage(self.rgb_array, 'r')
            elif text == 'Show Green':
                RPiCamera.showImage(self.rgb_array, 'g')
            elif text == 'Show Blue':
                RPiCamera.showImage(self.rgb_array, 'b')
            else:
                RPiCamera.showImage(self.rgb_array)
        except ValueError:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Information)
            mb.setWindowTitle('Error')
            mb.setText('Array not loaded, make sure you take picture or import an image first.')
            mb.setStandardButtons(QMessageBox.Ok)
            mb.show()

    def saveImage(self):
        filename = QFileDialog.getSaveFileName(self, 'Save Image As', os.sep.join((os.path.expanduser('~'), 'Desktop')), 'Image Files (*.png *.jpg *.jpeg)')
        RPiCamera.saveImage(self.rgb_array, filename[0])

    def saveAll(self):
        foldername = 'ISO={}-Delay={}-Resolution={}-Brightness={}-Contrast={}-ShutterSpeed={}' \
                     '-Exposure={}-AutoWhiteBalance={}-' \
                     'Zoom={}'.format(self.isoEntry.text(), self.delayEntry.text(), self.resEntry.text(),
                                      self.brightEntry.text(), self.contrastEntry.text(),
                                      self.shutterEntry.text(), self.expvar, self.awbvar, self.zoomEntry.text())
        RPiCamera.saveAllImages(self.rgb_array, self.directory, foldername)
        self.statusbar = 'Ready'

    def importImage(self):
        self.rgb_array = RPiCamera.importImage(self.image[0])

        red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(self.rgb_array)
        intensity_array = '\n'.join(['R:' + '{:.3f}'.format(red_intensity),
                                     'G:' + '{:.3f}'.format(green_intensity),
                                     'B:' + '{:.3f}'.format(blue_intensity),
                                     'I:' + '{:.3f}'.format(intensity)])
        self.intensityLbl.setText(intensity_array)
        self.intensityLbl.adjustSize()
        self.statusbar = 'Ready'

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox('Image Intensity Data')

        self.intensityLbl = QLabel('Not Taken')

        layout = QHBoxLayout()
        layout.addWidget(self.intensityLbl)
        layout.addStretch(1)

        self.bottomRightGroupBox.setLayout(layout)


class CameraMainWindow(QMainWindow):
    def __init__(self):
        super(CameraMainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # QToolTip.setFont(QFont('SansSerif', 9))

        self.cwidget = CameraCenterWidget()
        self.setCentralWidget(self.cwidget)

        # self.setToolTip('This is a <b>QWidget</b> widget')

        self.center()
        self.setWindowTitle('Camera Control GUI')

        self.statusBarTimer = QTimer(self)
        self.statusBarTimer.timeout.connect(self.statusUpdate)
        self.statusBarTimer.start(100)

        # self.p = QPalette(self.palette())
        # self.p.setColor(QPalette.Window, QColor(53, 53, 53))
        # self.p.setColor(QPalette.WindowText, Qt.white)
        # self.p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # self.p.setColor(QPalette.ToolTipBase, Qt.white)
        # self.p.setColor(QPalette.ToolTipText, Qt.white)
        # self.p.setColor(QPalette.Button, QColor(53, 53, 53))
        # self.p.setColor(QPalette.ButtonText, Qt.white)
        # self.p.setColor(QPalette.BrightText, Qt.red)
        # self.p.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        # self.p.setColor(QPalette.HighlightedText, Qt.black)
        # self.setPalette(self.p)

        self.show()

    def statusUpdate(self):
        self.statusBar().showMessage(self.cwidget.statusbar)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # def quitApp(self):
    #     QCoreApplication.instance().quit()


class RGBCenterWidget(QWidget):
    def __init__(self):
        super(RGBCenterWidget, self).__init__()
        self.initUI()
        # self.start_time = time.time()

    def initUI(self):
        self.tf = 'PlotTextFile.txt'

        self.statusbar = 'Ready'
        self.createTopGroupBox()
        self.createMidGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()

        topLayout = QVBoxLayout()
        topLayout.addWidget(self.topGroupBox)
        topLayout.addWidget(self.midGroupBox)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.bottomLeftGroupBox)
        bottomLayout.addWidget(self.bottomRightGroupBox)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

        self.show()

    def createTopGroupBox(self):
        self.topGroupBox = QGroupBox('Integration Time')

        self.it2_4ms = QRadioButton()
        self.it2_4ms.setText('2.4ms')
        self.it2_4ms.toggled.connect(lambda: self.itstate(self.it2_4ms))

        self.it24ms = QRadioButton()
        self.it24ms.setText('24ms')
        self.it24ms.toggled.connect(lambda: self.itstate(self.it24ms))

        self.it50ms = QRadioButton()
        self.it50ms.setText('50ms')
        self.it50ms.toggled.connect(lambda: self.itstate(self.it50ms))

        self.it101ms = QRadioButton()
        self.it101ms.setText('101ms')
        self.it101ms.toggled.connect(lambda: self.itstate(self.it101ms))

        self.it154ms = QRadioButton()
        self.it154ms.setText('154ms')
        self.it154ms.toggled.connect(lambda: self.itstate(self.it154ms))

        self.it700ms = QRadioButton()
        self.it700ms.setText('700ms')
        self.it700ms.toggled.connect(lambda: self.itstate(self.it700ms))

        self.it2_4ms.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.it2_4ms)
        layout.addWidget(self.it24ms)
        layout.addWidget(self.it50ms)
        layout.addWidget(self.it101ms)
        layout.addWidget(self.it154ms)
        layout.addWidget(self.it700ms)
        layout.addStretch(1)

        self.topGroupBox.setLayout(layout)

    def createMidGroupBox(self):
        self.midGroupBox = QGroupBox('Gain')

        self.gain1 = QRadioButton()
        self.gain1.setText('1X')
        self.gain1.toggled.connect(lambda: self.gnstate(self.gain1))

        self.gain4 = QRadioButton()
        self.gain4.setText('4X')
        self.gain4.toggled.connect(lambda: self.gnstate(self.gain4))

        self.gain16 = QRadioButton()
        self.gain16.setText('16X')
        self.gain16.toggled.connect(lambda: self.gnstate(self.gain16))

        self.gain60 = QRadioButton()
        self.gain60.setText('60X')
        self.gain60.toggled.connect(lambda: self.gnstate(self.gain60))

        self.gain1.setChecked(True)

        layout = QHBoxLayout()
        layout.addWidget(self.gain1)
        layout.addWidget(self.gain4)
        layout.addWidget(self.gain16)
        layout.addWidget(self.gain60)
        layout.addStretch(1)
        self.midGroupBox.setLayout(layout)

    def itstate(self, state):
        if state.text() == '2.4ms':
            if state.isChecked():
                self.itvar = '2.4'
        elif state.text() == '24ms':
            if state.isChecked():
                self.itvar = '24'
        elif state.text() == '50ms':
            if state.isChecked():
                self.itvar = '50'
        elif state.text() == '101ms':
            if state.isChecked():
                self.itvar = '101'
        elif state.text() == '154ms':
            if state.isChecked():
                self.itvar = '154'
        elif state.text() == '700ms':
            if state.isChecked():
                self.itvar = '700'

    def gnstate(self, state):
        if state.text() == '1X':
            if state.isChecked():
                self.gainvar = '1'
        elif state.text() == '4X':
            if state.isChecked():
                self.gainvar = '4'
        elif state.text() == '16X':
            if state.isChecked():
                self.gainvar = '16'
        elif state.text() == '60X':
            if state.isChecked():
                self.gainvar = '60'

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox('Sensor Options')

        captureBtn = QPushButton('Capture Data')
        captureBtn.clicked.connect(self.captureDataThread)

        setNormOptionsBtn = QPushButton('Set Normal Options')
        setNormOptionsBtn.clicked.connect(self.normalSettings)

        setDarkOptionsBtn = QPushButton('Set Low Light Options')
        setDarkOptionsBtn.clicked.connect(self.darkSettings)

        saveBtn = QPushButton('Save Data')
        saveBtn.clicked.connect(self.saveData)

        layout = QVBoxLayout()
        layout.addWidget(captureBtn)
        layout.addWidget(setNormOptionsBtn)
        layout.addWidget(setDarkOptionsBtn)
        layout.addWidget(saveBtn)
        layout.addStretch(1)
        self.bottomLeftGroupBox.setLayout(layout)

    def captureDataThread(self):
        self.statusbar = 'Capturing Data...'

        captureThread = threading.Thread(target=self.captureData)
        captureThread.start()

    def captureData(self):
        self.red_intensity, self.green_intensity, self.blue_intensity, self.clear_unfiltered, self.lux,\
        self.color_temperature = RGBSensor.Capture(integrationtime=float(self.itvar), gain=int(self.gainvar))
        intensity_array = '\n'.join(['R:' + '{}'.format(self.red_intensity),
                                     'G:' + '{}'.format(self.green_intensity),
                                     'B:' + '{}'.format(self.blue_intensity),
                                     'Clear:' + '{}'.format(self.clear_unfiltered),
                                     'Luminosity:{} lux'.format(self.lux),
                                     'Color Temperature:{} K'.format(self.color_temperature)])
        self.intensityLbl.setText(intensity_array)
        self.intensityLbl.adjustSize()
        self.statusbar = 'Ready'

    def normalSettings(self):
        self.gain1.setChecked(True)
        self.it2_4ms.setChecked(True)

    def darkSettings(self):
        self.gain60.setChecked(True)
        self.it700ms.setChecked(True)

    def saveData(self):
        RGBSensor.saveData(self.red_intensity, self.green_intensity, self.blue_intensity, self.clear_unfiltered,
                           self.lux, self.color_temperature)
        self.statusbar = 'Ready'

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox('Sensor Data')

        self.intensityLbl = QLabel('Not Taken')

        layout = QHBoxLayout()
        layout.addWidget(self.intensityLbl)
        layout.addStretch(1)

        self.bottomRightGroupBox.setLayout(layout)


class RGBMainWindow(QMainWindow):
    def __init__(self):
        super(RGBMainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # QToolTip.setFont(QFont('SansSerif', 9))

        self.cwidget = RGBCenterWidget()
        self.setCentralWidget(self.cwidget)

        # self.setToolTip('This is a <b>QWidget</b> widget')

        self.center()
        self.setWindowTitle('RGB Sensor GUI')

        self.statusBarTimer = QTimer(self)
        self.statusBarTimer.timeout.connect(self.statusUpdate)
        self.statusBarTimer.start(100)

        # self.p = QPalette(self.palette())
        # self.p.setColor(QPalette.Window, QColor(53, 53, 53))
        # self.p.setColor(QPalette.WindowText, Qt.white)
        # self.p.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # self.p.setColor(QPalette.ToolTipBase, Qt.white)
        # self.p.setColor(QPalette.ToolTipText, Qt.white)
        # self.p.setColor(QPalette.Button, QColor(53, 53, 53))
        # self.p.setColor(QPalette.ButtonText, Qt.white)
        # self.p.setColor(QPalette.BrightText, Qt.red)
        # self.p.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        # self.p.setColor(QPalette.HighlightedText, Qt.black)
        # self.setPalette(self.p)

        self.show()

    def statusUpdate(self):
        self.statusBar().showMessage(self.cwidget.statusbar)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # def quitApp(self):
    #     QCoreApplication.instance().quit()


def startGUI():
    app = QApplication(sys.argv)
    mw = GUIMainWindow()
    # cw = GUICenterWidget()
    rc = app.exec_()
    del app
    sys.exit(rc)


def startCameraGUI():
    app = QApplication(sys.argv)
    mw = CameraMainWindow()
    # cw = CameraCenterWidget()
    rc = app.exec_()
    del app
    sys.exit(rc)


def startRGBSensorGUI():
    app = QApplication(sys.argv)
    mw = RGBMainWindow()
    # cw = RGBCenterWidget()
    rc = app.exec_()
    del app
    sys.exit(rc)
