'''
This file contains the main control interface for the system.
It has access to:
1) DataReader
2) DataCacher
3) Model
4) ChatTool
'''

#TODO: change predictConfLev to handle multiclassification
#TODO: create chat() method

from DataCacher import *
from SentenceEncoder import *
from Model import *
from Validator import *

class Main:
    TH = 0.5
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.dataCacher = DataCacher(DBPATH, BASEPATH, debug=self.debug)
        self.encoder = SentenceEncoder()
        self.model = Model(NUMCATEGORIES)
        print(self.model.threshold)
        self.validator = Validator(self.model.threshold)

        self.trainSamples = self.getTrainingData()

    def plotTrainDataDistr(self):
        labels = self.trainSamples[2]
        labels = [e.index(1) for e in labels]
        plt.hist(labels, bins=NUMCATEGORIES)
        plt.title('Training Data Histogram')
        plt.xlabel('Label')
        plt.ylabel('Frequency')
        plt.show()

    def cacheData(self) -> None:
        if self.debug:
            self.dataCacher.cacheFile(TESTFILENAME, True)
        else:
            self.dataCacher.cacheAllFiles(True)

    def getTrainingData(self) -> tuple:
        if self.debug:
            return self.dataCacher.getTrainingDataByTable('tst')
        else:
            return self.dataCacher.getTrainingDataMerged()

    def train(self) -> None:
        self.model.train(self.trainSamples)
        self.validator.threshold = self.model.threshold

    def test(self, all=False) -> None:
        self.model.test(self.trainSamples, testOnly=False)

    def predictConfLev(self, enc: list) -> tuple:
        pred = self.model.predict(np.array([enc]))[0]
        cl = 1 - pred[INVIDX]
        cat = CATEGORIES[np.argmax(pred)]

        return cl, cat

    def predictValidity(self, enc: list) -> tuple:
        cl, cat = self.predictConfLev(enc)
        return cl, cat, self.validator.validate(cl)

    def chat(self) -> None:
        while True:
            display = f'type "/quit" to exit \n message: '
            userIn = str(input(display))

            if userIn.strip().lower() == '/quit':
                print('Exiting...')
                break
            else:
                enc = list(self.encoder.encStr(userIn))
                cl, cat, v = self.predictValidity(enc)
                print(f"{'valid' if v else 'invalid'}( {cl} ) -> {cat}")


if __name__ == "__main__":
    main = Main()
   # main.train()
    #main.model.saveModel()