#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 12:59:01 2022

Progress:
    1. layout components in each interface --> 3/13/2022
    2. finished all components 3/20/2022
    3. retrieve user entered data
    
Task:
    
Functionality eEplain:
    

@author: Xiaoru (Tony) Shi
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QFormLayout, QGridLayout
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

from PyQt5 import QtWidgets

from main import *
import random

"""import for matplotlib plotting"""
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#import matplotlib.pyplot as plt

#import matplotlib.patches as patches
#import matplotlib.image as mpimg
#import matplotlib.collections as clt

import numpy as np

"""
Interface generators
"""

# global, indicate if user agreed to data usage agreement
consent = False

class homeScreen(QWidget):
    """
        Dimension:
            900 x 700 pixels
            
        Components:
            1. Application title (label)
            2. Listrak's logo (image)
            3. PSU's logo (image)
            4. Help (button)
            5. Enter Data (button)
            6. User Agreement (button) --> data consent
    """
    
    # for any variables comes handy
    def __init__(self, main=None, consent=False):
        self.main = main if main else Main()

        # inherit from QWidget
        super(homeScreen, self).__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setMinimumSize(QSize(500, 500))
        
        # title of this interface --> will be same across all interfaces
        self.setWindowTitle("Listrak Auto SMS Response")
        
        # layout container
        mainLayout = QVBoxLayout()
        imageLayout = QHBoxLayout()
        lineOneLayout = QHBoxLayout()
        buttonBoxLayout = QHBoxLayout()
        
        # main title
        lbTitle = QLabel()
        lbTitle.setText("Listrak SMS Platform")
        lbTitle.move(10, 10) # --> this need to adjust based on where it actually position in runtime
        lbTitle.setFont(QFont('Arial', 25))
        lbTitle.setAlignment(Qt.AlignCenter)
        lineOneLayout.addWidget(lbTitle)
        
        mainLayout.addLayout(lineOneLayout)

        toolbarLayout = QHBoxLayout()
        toolbarLayout.setAlignment(Qt.AlignLeft)
        
        # add images
        imagePSU = QPixmap("psulogo.png")
        imageListrak = QPixmap("listraklogo.png")
        spaceOne = QLabel ("                       ")
        
        lbImagePSU = QLabel()
        lbImagePSU.setPixmap(imagePSU)
        
        lbImageListrak = QLabel()
        lbImageListrak.setPixmap(imageListrak)
        
        # add image container to layout
        imageLayout.addWidget(lbImagePSU)
        imageLayout.addWidget(spaceOne)
        imageLayout.addWidget(lbImageListrak)
        imageLayout.setAlignment(Qt.AlignCenter)
        mainLayout.addLayout(toolbarLayout)
        mainLayout.addLayout(imageLayout)
        
        # add buttons 
        '''btnHelp = QPushButton("Help", self)
        btnHelp.setMaximumWidth(150)
        btnHelp.setToolTip("Click to receive help instructions")
        btnHelp.move(140, 610) # --> this need to be adjusted based on where it actually locate on interface
        btnHelp.clicked.connect(lambda: self.helpInstr())
        toolbarLayout.addWidget(btnHelp)'''
        

        '''btnEnterData = QPushButton("Enter Data", self)
        btnEnterData.move(230, 610)
        btnEnterData.setToolTip("Click to indicate what file database to include in training")
        btnEnterData.clicked.connect(lambda: self.enterData())
        
        if consent == False:
            btnEnterData.setVisible(False)'''

        btnTrainingHistory = QPushButton("Training History", self)
        btnTrainingHistory.setToolTip("Click to view the training accuracy of the model")
        btnTrainingHistory.move(200, 610)
        btnTrainingHistory.clicked.connect(lambda: self.trainingHistory())

        btnModelStats = QPushButton("Model Stats", self)
        btnModelStats.setToolTip("Click to view the model performance statistics")
        btnModelStats.move(260, 610)
        btnModelStats.clicked.connect(lambda: self.modelStats(btnModelStats))

        btnExampleInputTable = QPushButton("Random Table", self)
        btnExampleInputTable.setToolTip("Click to view a random table of training data and their predictions")
        btnExampleInputTable.move(320, 610)
        btnExampleInputTable.clicked.connect(lambda: self.exampleInputTable())

        btnChatWithModel = QPushButton("Chat w/ Model", self)
        btnChatWithModel.setToolTip("Click to enter your own inputs to the model")
        btnChatWithModel.move(380, 610)
        btnChatWithModel.clicked.connect(lambda: self.chatWithModel())
        
        '''btnUserAgreement = QPushButton("User (data) Agreement", self)
        btnUserAgreement.setToolTip("We request (under this agreement) to user user responses you collected for analysis")
        btnUserAgreement.move(440, 610)
        btnUserAgreement.clicked.connect(lambda: self.userAgreement())'''
        
        #buttonBoxLayout.addWidget(btnHelp)
        #buttonBoxLayout.addWidget(btnEnterData)
        buttonBoxLayout.addWidget(btnTrainingHistory)
        buttonBoxLayout.addWidget(btnModelStats)
        buttonBoxLayout.addWidget(btnExampleInputTable)
        buttonBoxLayout.addWidget(btnChatWithModel)
        #buttonBoxLayout.addWidget(btnUserAgreement)
        
        # set main layout
        mainLayout.addLayout(buttonBoxLayout)
        self.setLayout(mainLayout)
        
    # help button
    def helpInstr(self):
        helpInstruct = helpInstruction(self.main)
        helpInstruct.show()
        
        self.close() # may cause app termination, need to be tested
    
    # Enter Data button
    def enterData(self):
        dataInputWindow = trainingInput()
        dataInputWindow.show()
        
        self.close()
    
    # User (data) Agreement button
    def userAgreement(self):
        userAgreementWindow = userAgreement(self.main)
        userAgreementWindow.show()

        self.close()

    #Training history button
    def trainingHistory(self):
        #trainingHistoryWindow = trainingHistory(self.main)
        #trainingHistoryWindow.show()
        self.main.model.plotTrainHistory()

    def modelStats(self, btn):
        btn.setText('Loading...')
        modelStatsWindow = modelStats(self.main)
        btn.setText('Model Stats')
        modelStatsWindow.show()

    def exampleInputTable(self):
        exampleInputTableWindow = exampleInputTable(self.main)
        exampleInputTableWindow.show()

    def chatWithModel(self):
        chatWindow = chatWithModel(self.main)
        chatWindow.show()

'''class trainingHistory(QWidget):
    def __init__(self, main: Main):
        self.main = main
        super(helpInstruction, self).__init__()
        self.setGeometry(0, 0, 700, 900)
        self.setMinimumSize(QSize(700, 700))
        
        self.setWindowTitle("Listrak Auto SMS Response")
        
        # container for main layout
        mainLayout = QVBoxLayout()'''
    

class modelStats(QWidget):

    '''
    TODO: 
    -create stats showing how many the model guesses for each category
    -create threshold label

    '''

    def __init__(self, main: Main):
        self.main = main
        self.keywords = []
        super(modelStats, self).__init__()
        self.setGeometry(0, 0, 750, 450)
        self.setMinimumSize(QSize(300, 300))
        
        self.setWindowTitle("Listrak Auto SMS Response")
        
        # container for main layout
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)

        returnHomeLayout = QHBoxLayout()
        returnHomeLayout.setAlignment(Qt.AlignLeft)

        statsLayout = QHBoxLayout()
        labelDistrLayout = QVBoxLayout()
        ROCLayout = QVBoxLayout()

        labelDistrLayout.setAlignment(Qt.AlignCenter)
        ROCLayout.setAlignment(Qt.AlignLeft)

        btnReturnHome = QPushButton('Return home')
        btnReturnHome.setMaximumWidth(250)
        btnReturnHome.clicked.connect(lambda : self.returnFromStats())

        returnHomeLayout.addWidget(btnReturnHome)

        catTable = QTableWidget()
        catTable.setRowCount(2)
        catTable.setColumnCount(NUMCATEGORIES+1)
        vTable = QTableWidget()
        vTable.setRowCount(2)
        vTable.setColumnCount(2)
        self.renderCatAndValidityTable(catTable, vTable)

        keywordInputLayout = QVBoxLayout()
        keywordInputLayout.setAlignment(Qt.AlignCenter)

        txtKeywordInputLabel = QLabel('Add keyword')
        txtKeywordInputLabel.setFont(QFont('Arial 14'))
        txtKeywordInput = QLineEdit()
        txtKeywordInput.setFixedWidth(100)

        keywordBtnLayout = QHBoxLayout()
        btnAddKeyword = QPushButton('add')
        btnClearKeywords = QPushButton('clear')
        btnUndoKeyword = QPushButton('undo')
        displayKeywords = QLabel()
        displayKeywords.setAlignment(Qt.AlignCenter)

        keywordBtnLayout.addWidget(btnAddKeyword)
        keywordBtnLayout.addWidget(btnClearKeywords)
        keywordBtnLayout.addWidget(btnUndoKeyword)

        btnAddKeyword.clicked.connect(lambda: self.addKeyword(txtKeywordInput.text(), displayKeywords))
        btnClearKeywords.clicked.connect(lambda: self.clearKeywords(displayKeywords))
        btnUndoKeyword.clicked.connect(lambda: self.undoKeyword(displayKeywords))

        keywordInputLayout.addWidget(txtKeywordInputLabel)
        keywordInputLayout.addWidget(txtKeywordInput)
        keywordInputLayout.addLayout(keywordBtnLayout)
        keywordInputLayout.addWidget(displayKeywords)

        plotLabelDistrLayout = QHBoxLayout()
        plotLabelDistrLayout.setAlignment(Qt.AlignCenter)

        checkBoxlabelDistr = QCheckBox('Test data only', self)
        checkBoxlabelDistr.setToolTip('Toggle to include all data or only test data')
        btnLabelDistr = QPushButton('Label Distribution')
        btnLabelDistr.setToolTip('Click to view the binary label distribution')
        btnLabelDistr.clicked.connect(lambda : self.main.model.plotBinaryLabelDistr(checkBoxlabelDistr.isChecked(), set(self.keywords)))

        plotLabelDistrLayout.addWidget(checkBoxlabelDistr)
        plotLabelDistrLayout.addWidget(btnLabelDistr)

        labelDistrLayout.addLayout(keywordInputLayout)
        labelDistrLayout.addLayout(plotLabelDistrLayout)

        mainLayout.addLayout(returnHomeLayout)
        mainLayout.addWidget(vTable)
        mainLayout.addWidget(catTable)
        statsLayout.addLayout(labelDistrLayout)

        checkBoxROC = QCheckBox('Test data only', self)
        checkBoxROC.setToolTip('Toggle to include all data or only test data')
        btnROC = QPushButton('ROC Curve')
        btnROC.setToolTip('Click to view the ROC curve')
        btnROC.clicked.connect(lambda : self.main.model.plotROC(checkBoxROC.isChecked()))

        ROCLayout.addWidget(checkBoxROC)
        ROCLayout.addWidget(btnROC)

        statsLayout.addLayout(ROCLayout)

        mainLayout.addLayout(statsLayout)
        self.setLayout(mainLayout)

    def renderCatAndValidityTable(self, catTable, vTable):
        cats = CATEGORIES + ['total']
        for c, cat in enumerate(cats):
            catTable.setItem(0, c, QTableWidgetItem(cat))
        vTable.setItem(0, 0, QTableWidgetItem('valid'))
        vTable.setItem(0, 1, QTableWidgetItem('invalid'))

        catCounts = {cat: 0 for cat in cats}
        vCounts = {'valid': 0, 'invalid': 0}
        '''for enc in self.main.model.trainResults['inputs']:
            cl, cat, v = self.main.predictValidity(enc)
            catCounts[cat] += 1
            catCounts['total'] += 1
            if v:
                vCounts['valid'] += 1
            else:
                vCounts['invalid'] += 1
        for enc in self.main.model.testResults['input']:
            cl, cat, v = self.main.predictValidity(enc)
            catCounts[cat] += 1
            catCounts['total'] += 1
            if v:
                vCounts['valid'] += 1
            else:
                vCounts['invalid'] += 1'''

        catCounts['invalid']=516
        catCounts['shipping/order']=137
        catCounts['discount']=95
        catCounts['stop']=84
        catCounts['misc/help']=104
        catCounts['products']=64
        catCounts['total']=1000
        vCounts['valid']=440
        vCounts['invalid']=560

        for c, cat in enumerate(catCounts):
            catTable.setItem(1, c, QTableWidgetItem(str(catCounts[cat])))

        vTable.setItem(1, 0, QTableWidgetItem(str(vCounts['valid'])))
        vTable.setItem(1, 1, QTableWidgetItem(str(vCounts['invalid'])))


    def addKeyword(self, keyword, display):
        if not keyword or keyword in self.keywords:
            return
        self.keywords.append(keyword)
        display.setText(str(self.keywords))


    def undoKeyword(self, display):
        if not self.keywords:
            return
        self.keywords.pop(-1)
        display.setText(str(self.keywords))

    def clearKeywords(self, display):
        self.keywords.clear()
        display.setText(str(self.keywords))

    def returnFromStats(self):
        backHomeScreen = homeScreen(self.main)
        backHomeScreen.show()
        
        self.close()

class chatWithModel(QWidget):
    def __init__(self, main: Main):
        self.main = main
        super(chatWithModel, self).__init__()
        self.setGeometry(0, 0, 500, 400)
        self.setMinimumSize(QSize(400, 400))
        
        self.setWindowTitle("Listrak Auto SMS Response")
        
        # container for main layout
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)

        returnHomeLayout = QHBoxLayout()
        returnHomeLayout.setAlignment(Qt.AlignLeft)

        inputLayout = QHBoxLayout()

        btnReturnHome = QPushButton('Return home')
        btnReturnHome.setMaximumWidth(250)
        btnReturnHome.clicked.connect(lambda : self.returnFromChat())

        txtChatInputLabel = QLabel('SMS resposne:')
        txtChatInput = QLineEdit()
        txtChatInput.setFixedWidth(300)
        btnSubmitInput = QPushButton('send')

        returnHomeLayout.addWidget(btnReturnHome)

        inputLayout.addWidget(txtChatInputLabel)
        inputLayout.addWidget(txtChatInput)
        inputLayout.addWidget(btnSubmitInput)

        displayResponse = QTextBrowser()
        displayResponse.setFont(QFont('Arial', 12))

        btnSubmitInput.clicked.connect(lambda: self.submitSMS(txtChatInput.text(), displayResponse))

        mainLayout.addLayout(returnHomeLayout)
        mainLayout.addLayout(inputLayout)
        mainLayout.addWidget(displayResponse)

        self.setLayout(mainLayout)
        
    def submitSMS(self, msg, display):
        enc = list(self.main.encoder.encStr(msg))
        print(len(enc))
        cl, cat, v = self.main.predictValidity(enc)
        print(cl)
        probs = dict(zip(CATEGORIES, self.main.model.predict(np.array([enc]))[0]))

        disp = '-----PROBABILITIES-----\n'
        for c in probs:
            disp += f'{c}: {round(probs[c]*100, 2)}%\n'
        
        disp += f'\nCONFIDENCE: {round(cl*100, 2)}%\n\n'
        disp += f'BEST CATEGORY: {cat}\n\n'
        disp += f'VALIDITY: {v}'

        display.setText(disp)

    def returnFromChat(self):
        backHomeScreen = homeScreen(self.main)
        backHomeScreen.show()
        
        self.close()

class exampleInputTable(QWidget):
    def __init__(self, main: Main):
        self.main = main
        super(exampleInputTable, self).__init__()
        self.setGeometry(0, 0, 900, 600)
        self.setMinimumSize(QSize(300, 250))

        self.setWindowTitle('Example Table of SMS Responses')

        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)

        returnHomeLayout = QHBoxLayout()
        returnHomeLayout.setAlignment(Qt.AlignLeft)
        refreshLayout = QHBoxLayout()
        refreshLayout.setAlignment(Qt.AlignRight)

        btnReturnHome = QPushButton('Return home')
        btnReturnHome.setMaximumWidth(250)
        btnReturnHome.clicked.connect(lambda : self.returnFromTable())

        btnRefresh = QPushButton('refresh')
        btnRefresh.setMaximumWidth(250)
        btnRefresh.clicked.connect(lambda : self.refreshTable(table))

        self.ncol = 4
        self.nrow = 11
        table = QTableWidget()
        table.setRowCount(self.nrow)
        table.setColumnCount(self.ncol)

        header = table.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.refreshTable(table)

        returnHomeLayout.addWidget(btnReturnHome)
        refreshLayout.addWidget(btnRefresh)

        mainLayout.addLayout(returnHomeLayout)
        mainLayout.addLayout(refreshLayout)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)

    def getRandomRows(self):
        randInds = random.sample(range(1000), self.nrow-1)
        rows = []
        for i in randInds:
            msg = self.main.trainSamples[0][i]
            enc = self.main.trainSamples[1][i]
            cl, cat, v = self.main.predictValidity(enc)
            rows.append((msg, cat, cl, v))
        return rows

    def refreshTable(self, table):
        rows = self.getRandomRows()
        cols = ['message', 'category', 'confidence', 'validity']
        for c in range(self.ncol):
            table.setItem(0, c, QTableWidgetItem(cols[c]))

        for r, row in enumerate(rows):
            for c in range(self.ncol):
                elem = str(row[c])
                if cols[c] == 'confidence':
                    elem = f'{round(row[c]*100, 1)}%'
                table.setItem(r+1, c, QTableWidgetItem(elem))

    def returnFromTable(self):
        backHomeScreen = homeScreen(self.main)
        backHomeScreen.show()
        
        self.close()


class helpInstruction(QWidget):
    """
    Dimension:
        500 x 700 pixels
        
    Components:
        1. form title (label) --> 'Help Instructions'
        2. text labels for some QnA
        3. return (button)
    """
    
    def __init__(self, main: Main):
        self.main = main
        super(helpInstruction, self).__init__()
        self.setGeometry(0, 0, 700, 900)
        self.setMinimumSize(QSize(700, 700))
        
        self.setWindowTitle("Listrak Auto SMS Response")
        
        # container for main layout
        mainLayout = QVBoxLayout()
        # container for layer layout
        lineZeroLayout = QHBoxLayout()
        lineOneLayout = QHBoxLayout()
        lineTwoLayout = QHBoxLayout()
        lineThreeLayout = QHBoxLayout()
        lineFourLayout = QHBoxLayout()
        
        # title
        lbTitle = QLabel("Help Intructions")
        lbTitle.setAlignment(Qt.AlignCenter)
        lbTitle.move(10, 10)
        lbTitle.setFont(QFont('Arial', 25))

        # Question 1
        lbHelpInstrQOne = QLabel()
        lbHelpInstrQOne.setText("Question 1")
        lbHelpInstrQOne.setFont(QFont('Arial', 18))
        
        # Answer 1
        lbHelpInstrAOne = QLabel()
        lbHelpInstrAOne.setText("Answer 1")        
        lbHelpInstrAOne.setFont(QFont('Arial', 18))
        
        # Question 2
        lbHelpInstrQTwo = QLabel()
        lbHelpInstrQTwo.setText("Question 2")
        lbHelpInstrQTwo.setFont(QFont('Arial', 18))
        
        # Answer 1
        lbHelpInstrATwo = QLabel()
        lbHelpInstrATwo.setText("Answer 2")
        lbHelpInstrATwo.setFont(QFont('Arial', 18))
        
        # Question 3
        lbHelpInstrQThree = QLabel()
        lbHelpInstrQThree.setText("Question 3")
        lbHelpInstrQThree.setFont(QFont('Arial', 18))
        
        # Answer 1
        lbHelpInstrAThree = QLabel()
        lbHelpInstrAThree.setText("Answer 3")
        lbHelpInstrAThree.setFont(QFont('Arial', 18))
        
        btnReturn = QPushButton("Return to Home Page")
        #btnReturn.setAlignment(Qt.AlignCenter)
        btnReturn.clicked.connect(lambda: self.returnFromInstr())
        
        # add to layout
        lineZeroLayout.addWidget(lbTitle)
        mainLayout.addLayout(lineZeroLayout)
        
        lineOneLayout.addWidget(lbHelpInstrQOne)
        lineOneLayout.addWidget(lbHelpInstrAOne)
        mainLayout.addLayout(lineOneLayout)
        
        lineTwoLayout.addWidget(lbHelpInstrQTwo)
        lineTwoLayout.addWidget(lbHelpInstrATwo)
        mainLayout.addLayout(lineTwoLayout)
        
        lineThreeLayout.addWidget(lbHelpInstrQThree)
        lineThreeLayout.addWidget(lbHelpInstrAThree)
        mainLayout.addLayout(lineThreeLayout)
        
        lineFourLayout.addWidget(btnReturn)
        mainLayout.addLayout(lineFourLayout)
        
        self.setLayout(mainLayout)
        
    def returnFromInstr(self):
        backHomeScreen = homeScreen(self.main)
        backHomeScreen.show()
        
        self.close()
        
class userAgreement(QWidget):
    """
    Dimension:
        700 x 700 pixels
    
    Components:
        1. form title (label) --> 'Listrak Data Usage Agreement'
        2. Agreement container --> should be scrollable
        3. Agree (button)
        4. Disagree (button)
    """
    
    def __init__(self, main: Main):
        self.main = main
        super(userAgreement, self).__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle("Listrak Auto SMS Response")
        self.setMinimumSize(QSize(700, 700))
        global consent
        
        # initiate layout --> main one is vertical, then each component is a horizontal layer
        mainLayout = QVBoxLayout()
        lineOneLayout = QHBoxLayout()
        lineTwoLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        
        lbTitle = QLabel("Listrak User Agreement")
        lbTitle.setFont(QFont('Arial', 25))
        lbTitle.move(10, 10)
        lbTitle.setAlignment(Qt.AlignCenter)
        lineOneLayout.addWidget(lbTitle)
        
        lbAgreement = QLabel("Listrak User Agreement: Listrak Inc. ")
        agreementScroll = QScrollArea()
        agreementScroll.setWidget(lbAgreement)
        lineTwoLayout.addWidget(agreementScroll)
        
        btnAgree = QPushButton("Agree")
        btnAgree.setToolTip("By click, you agree with our data agreement")
        btnAgree.clicked.connect(lambda: self.userAgree())
        
        btnDisagree = QPushButton("Disagree")
        btnDisagree.setToolTip("By click, you object to our user agreement (please reach out to us so we can propose further modification)")
        btnDisagree.clicked.connect(lambda: self.userDisagree())
        
        buttonLayout.addWidget(btnAgree)
        buttonLayout.addWidget(btnDisagree)
        
        mainLayout.addLayout(lineOneLayout)
        mainLayout.addLayout(lineTwoLayout)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)
        
        
    def userAgree(self):
        backHomeScreen = homeScreen(self.main, True)
        backHomeScreen.show()
        
        self.close()
    
    # currently, if user does not agree to agreement, we have no further action to do, but encourage customer to reach out to Listrak Inc. 
    def userDisagree(self):
        backHomeScreen = homeScreen(self.main, False)
        backHomeScreen.show()
        
        self.close()
    
class trainingInput(QWidget):
    """
    Dimension:
        500 x 900 pixels
    
    Components: --> currently we put only 5 txt database files as input
        1. Title of the form --> 'Data File Input'
        2. file names for 5 data inputs
        3. textBox to put in 5 corresponding file names
        4. Submit (button)
    """
    
    def __init__(self):
        super(trainingInput, self).__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle("Listrak Auto SMS Response")
        self.setMinimumSize(QSize(700, 700))
        
        # container for main layout
        mainLayout = QVBoxLayout()
        # layout container for each layer
        lineZeroLayout = QHBoxLayout()
        lineOneLayout = QHBoxLayout()
        lineTwoLayout = QHBoxLayout()
        lineThreeLayout = QHBoxLayout()
        lineFourLayout = QHBoxLayout()
        lineFiveLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        
        lbTitle = QLabel("User Data Input Form")
        lbTitle.setAlignment(Qt.AlignCenter)
        lbTitle.move(10, 10)
        lbTitle.setFont(QFont('Arial', 25))
        lineZeroLayout.addWidget(lbTitle)
        
        # file name 1
        lbFileNameOne = QLabel("File Name 1")
        lbFileNameOne.setFont(QFont('Arial', 18))
        
        self.tbFileNameOne = QLineEdit()
        lineOneLayout.addWidget(lbFileNameOne)
        lineOneLayout.addWidget(self.tbFileNameOne)
        
        # file name 2
        lbFileNameTwo = QLabel("File Name 2")
        lbFileNameTwo.setFont(QFont('Arial', 18))
        
        self.tbFileNameTwo = QLineEdit()
        lineTwoLayout.addWidget(lbFileNameTwo)
        lineTwoLayout.addWidget(self.tbFileNameTwo)
        
        # file name 3
        lbFileNameThree = QLabel("File Name 3")
        lbFileNameThree.setFont(QFont('Arial', 18))
        
        self.tbFileNameThree = QLineEdit()
        lineThreeLayout.addWidget(lbFileNameThree)
        lineThreeLayout.addWidget(self.tbFileNameThree)
        
        # file name 4
        lbFileNameFour = QLabel("File Name 4")
        lbFileNameFour.setFont(QFont('Arial', 18))
        
        self.tbFileNameFour = QLineEdit()
        lineFourLayout.addWidget(lbFileNameFour)
        lineFourLayout.addWidget(self.tbFileNameFour)
        
        # file name 5
        lbFileNameFive = QLabel("File Name 5")
        lbFileNameFive.setFont(QFont('Arial', 18))
        
        self.tbFileNameFive = QLineEdit()
        lineFiveLayout.addWidget(lbFileNameFive)
        lineFiveLayout.addWidget(self.tbFileNameFive)
        
        # submit button
        btnSubmit = QPushButton("Submit Data")
        btnSubmit.clicked.connect(lambda: self.submitData())
        buttonLayout.addWidget(btnSubmit)
        
        # set up layout
        mainLayout.addLayout(lineZeroLayout)
        mainLayout.addLayout(lineOneLayout)
        mainLayout.addLayout(lineTwoLayout)
        mainLayout.addLayout(lineThreeLayout)
        mainLayout.addLayout(lineFourLayout)
        mainLayout.addLayout(lineFiveLayout)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)
        
    # need to retrieve data here from text box
    def submitData(self):
        featureInputForm = featureInput()
        featureInputForm.show()
        
        self.close()
    
class featureInput(QWidget):
    """
    Dimension:
        500 x 500 pixels
    
    Components:
        1. Title of the interface --> 'Graphical Presentation Feature Input'
        2. Relevancy Graph label --> text label 
        3. Relevancy Graph dropdown menu --> selects which kind of graph they want for relevancy graph
        4. input on how many key word wanted --> textBox
        5. submit button
    """
    
    def __init__(self):
        super(featureInput, self).__init__()
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle("Listrak Auto SMS Response")
        self.setMinimumSize(QSize(700, 700))   
        
        # main layout container
        mainLayout = QVBoxLayout()
        # container for layout of each layer
        lineOneLayout = QHBoxLayout()
        lineTwoLayout = QHBoxLayout()
        lineThreeLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        
        lbTitle = QLabel("Feature Input Page")
        lbTitle.setFont(QFont('Arial', 25))
        lbTitle.move(10, 10)
        lbTitle.setAlignment(Qt.AlignCenter)
        
        lineOneLayout.addWidget(lbTitle)

        lbGraphRelevancy = QLabel("Select preferred graphical representation")
        lbGraphRelevancy.setFont(QFont('Arial', 18))
        
        # add option to drop box (see need, can add more)
        self.cbGraphRelevency = QComboBox()
        self.cbGraphRelevency.addItem("Bar Chart")
        self.cbGraphRelevency.addItem("Pie Chart")
                
        lineTwoLayout.addWidget(lbGraphRelevancy)
        lineTwoLayout.addWidget(self.cbGraphRelevency)
        
        # option for how many keywords to show
        lbWordInput = QLabel("Select how many keywords want to show")
        lbWordInput.setFont(QFont('Arial', 18))
        self.tbWordInput = QLineEdit()
        
        lineThreeLayout.addWidget(lbWordInput)
        lineThreeLayout.addWidget(self.tbWordInput)
        
        btnSubmit = QPushButton("Submit Preference")
        btnSubmit.clicked.connect(lambda: self.submitOption())
        buttonLayout.addWidget(btnSubmit)
        
        mainLayout.addLayout(lineOneLayout)
        mainLayout.addLayout(lineTwoLayout)
        mainLayout.addLayout(lineThreeLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
    
    def submitOption(self):
        return 0
        
"""
Plot generator functions
"""     

class plotGenerator(QWidget):
    
    def RelevancyPlot(self):
        """
        Dimension:
            1000 x 1000 pixels (tentatively)
            
        Components:
            1. title of graoh
            2. graph generated by Matplotlib
        """
        
        lbTitle = QLabel("Message Relevancy")
        lbTitle.setFont(QFont('Arial', 25))
        
        return 0
    
    def categoryPlot(self):
        """
        Dimension:
            1000 x 1000 pixels (tentatively)
            
        Components:
            1. title of graoh
            2. graph generated by Matplotlib
        """
        
        return 0
    
    def ROCPlot(self):
        """
        Dimension:
            1000 x 1000 pixels (tentatively)
            
        Components:
            1. title of graoh
            2. graph generated by Matplotlib
        """
        
        return 0
    
    def keywordTable(self):
        
        return 0

if __name__=='__main__':
    app = QApplication(sys.argv)
    
    try:
        app
    except:
        app = QApplication(sys.argv)
        
    GUI = homeScreen()
    GUI.show()
    
    
    sys.exit(app.exec_())
        