from typing import Generator
from constants.modelconstants import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from constants.cacheconstants import *
import os
import matplotlib.pyplot as plt
import pickle

class Model:
    def __init__(self, numCat):
        self.neuralModel = None
        self.numCat = numCat
        self.trainResults = {
            'strings': None,
            'input': None,
            'true': None,
            'history': None
        }
        self.testResults = {
            'strings': None,
            'input': None,
            'pred': None,
            'true': None
        }
        self.threshold = None
        self.loadedPrevModel = False
        self.initModel()

    '''
    Checks if an existing model has already been saved:
        if one exists, then it is loaded
        if one doesn't exist, a new model is created and compiled
    '''
    def initModel(self) -> None:
        files = os.listdir(MODELDIR)
        if MODELNAME not in files:
            self.createModel()
        else:
            self.loadModel()

    '''
    Loads the model files along with the training results, testing results, and threshold
    '''
    def loadModel(self) -> None:
        with open(RESULTSPATH, 'rb') as f:
            self.trainResults, self.testResults, self.threshold = pickle.load(f)
        self.neuralModel = keras.models.load_model(MODELPATH)
        self.loadedPrevModel = True 
        
    '''
    Saves the model files along with the training results, test results, and threshold
    '''
    def saveModel(self) -> None:
        self.neuralModel.save(MODELPATH)
        results = (self.trainResults, self.testResults, self.threshold)
        with open(RESULTSPATH, 'wb') as f:
            pickle.dump(results, f)

    '''
    Configures a sequential model (ANN) and compiles it
    '''
    def createModel(self) -> None:
        self.neuralModel = keras.Sequential([
            keras.layers.Dense(512, input_shape=(512,), activation='relu'),
            keras.layers.Dropout(rate=0.25, input_shape=(256,)),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(self.numCat, activation='softmax'),
        ])
        self.neuralModel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    '''
    Gets the confidence scores from the test results using filterScoresByWords()
    includesWords = None gets everything and doesn't filter by a certain words
    '''
    def getScoresFromOutputs(self, testOnly: bool, includesWords: set) -> list:
        try:
            return self.filterScoresByWords(testOnly, includesWords)
        except:
            raise Exception("Data Error: Test outputs are either unfilled or not an iterable.")

    '''
    Gets the binary labels from the test results using filterLabelsByWords()
    '''
    def getBinaryLabelsFromInputs(self, testOnly: bool, includesWords: set) -> list:
        try:
            return self.filterLabelsByWords(testOnly, includesWords)
        except:
            raise Exception("Data Error: Training labels are either unfilled or not an iterable.")

    '''
    Converts all training labels (which are an array of length numCategories) to a valid-invalid labels
    Can filter by a set of words
    '''
    def filterLabelsByWords(self, testOnly: bool, includesWords: set):
        labels = []
        outputs = self.testResults['true'] if testOnly else np.concatenate((self.trainResults['true'], self.testResults['true']))
        filtered = self.filterByWords(testOnly, includesWords)
        for i in filtered:
            label = 0 if outputs[i][INVIDX] else 1
            labels.append(label)
        return labels

    '''
    Converts all training predictions to confidence scores for valid-invalid
    Can filter by a set of words
    '''
    def filterScoresByWords(self, testOnly: bool, includesWords: set):
        scores = []
        outputs = self.testResults['pred'] if testOnly else np.concatenate((self.trainResults['pred'], self.testResults['pred']))
        filtered = self.filterByWords(testOnly, includesWords)
        for i in filtered:
            score = 1 - outputs[i][INVIDX]
            scores.append(score)
        return scores

    '''
    Goes through the test data and filters them by the set includesWords.
    If the test message contains one of the words in includesWords, it will be added to the returned list.
    '''
    def filterByWords(self, testOnly: bool, includesWords: set) -> list:
        strs = self.testResults['strings'] if testOnly else np.concatenate((self.trainResults['strings'], self.testResults['strings']))
        if not includesWords:
            if testOnly:
                return range(len(strs))
            else:
                return range(len(strs))
        indices = []
        for i, s in enumerate(strs):
            words = set(s.strip().split())
            if len(words.intersection(includesWords)) > 0:
                indices.append(i)
        return indices

    '''
    Returns a 6-length tuple of the training data in the following order:
    train msgs, train encs, tests messages, test encs, train labels, test labels
    '''
    def splitTrainTest(self, trainSamples: tuple) -> tuple:
        strs, encs, labels = trainSamples
        data = train_test_split(list(zip(strs, encs)), labels, test_size=0.2, random_state=42)
        trX, teX, trY, teY = data
        trStrs, trEncs = zip(*trX)
        teStrs, teEncs = zip(*teX)
        data = trStrs, trEncs, teStrs, teEncs, trY, teY
        return tuple([np.array(d) for d in data])

    '''
    Plots the train history
    graphs the train accuracy and validation accuracy against the number of epochs
    '''
    def plotTrainHistory(self) -> None:
        plt.plot(self.trainResults['history']['accuracy'])
        plt.plot(self.trainResults['history']['val_accuracy'])
        plt.legend(['train', 'test'], loc='lower right')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.title('Training/Test Accuracy')
        plt.show()

    '''
    Plots the ROC curve
    '''
    def plotROC(self, testOnly) -> None:
        scores = self.getScoresFromOutputs(testOnly, None)
        ytrue = self.getBinaryLabelsFromInputs(testOnly, None)
        fpr, tpr, thresholds = roc_curve(ytrue, scores)
        optThresh = findBestThreshold(fpr, thresholds)
        self.threshold = optThresh
        plt.plot(fpr, tpr)
        plt.plot(np.linspace(0, 1, 30), np.linspace(0, 1, 30), ':')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.show()

    '''
    Plots the distribution of test data. Frequency on the y axis and confidence score on the x axis.
    Data points are differentiated by their true labels.
    '''
    def plotBinaryLabelDistr(self, testOnly: bool, includesWords: set = None) -> None:
        scores = self.getScoresFromOutputs(testOnly, includesWords)
        ytrue = self.getBinaryLabelsFromInputs(testOnly, includesWords)
        zeros = [sc for i, sc in enumerate(scores) if ytrue[i] == 0]
        ones = [sc for i, sc in enumerate(scores) if ytrue[i] == 1]
        plt.hist(zeros, bins=25)
        plt.hist(ones, bins=25)
        plt.xlabel('CL Prediction')
        plt.ylabel('Frequency')
        plt.legend(['0', '1'], loc='upper right')
        plt.show()

    '''
    Given testSamples, it tests the model and prints the accuracy. It also plots the binary label distribution and the ROC curve.
    '''
    def test(self, testSamples: tuple, testOnly=True):
        testStrs, testX, testY = testSamples
        testHistory = self.neuralModel.evaluate(testX, testY)
        outputs = self.predict(testX)
        if testOnly:
            self.testResults['strings'] = testStrs
            self.testResults['input'] = testX
            self.testResults['pred'] = outputs
            self.testResults['true'] = testY
        self.plotBinaryLabelDistr(testOnly)
        self.plotROC(testOnly)

    '''
    Trains the model using trainSamples. It plots the train history then immediately tests the model.
    '''
    def train(self, trainSamples: tuple) -> None:
        trStrs, trX, teStrs, teX, trY, teY = self.splitTrainTest(trainSamples)
        trainHistory = self.neuralModel.fit(trX, trY, validation_split=0.1, batch_size=64, epochs=EPOCHS)
        self.trainResults['strings'] = trStrs
        self.trainResults['input'] = trX
        self.trainResults['true'] = trY
        self.trainResults['history'] = trainHistory.history
        self.trainResults['pred'] = self.predict(trX)
        self.plotTrainHistory()
        self.test((teStrs, teX, teY))

    '''
    Returns the last layers given a list of encodings
    '''
    def predict(self, encs: list) -> list:
        outputs = self.neuralModel.predict(encs)
        return outputs