from SQLiteConnection import *
from DataReader import *
from SentenceEncoder import *
import numpy as np

#TODO: Change convToNNFormat to handle the categories and make an one hot encoded list like [0,...,0,1,0,...,0]

'''
The DataCacher class uses the SQLiteConnection, DataReader, and SentenceEncoder as internal objects.
This class is responsible for:
1) reading the data and caching it in one method.
2) executing additional preprocessing for the neural network
3) retrieving the training data in its fully processed form
'''
class DataCacher:
    def __init__(self, dbpath: str, datapath: str, debug: bool = False):
        self.dbpath = dbpath
        self.datapath = datapath
        self.debug = debug
        self.sqcon = SQLiteConnection(dbpath)
        self.dataReader = DataReader(datapath, [TESTFILENAME] if self.debug else FILENAMES)
        self.encoder = SentenceEncoder()

    '''
    This method converts an index to a one-hot encoded vector. For example, if 5 categories exist,
    oneHotEncode(2) will return [0, 0, 1, 0, 0]
    '''
    @staticmethod
    def oneHotEncode(idx: int):
        lst = [1 if i == idx else 0 for i in range(NUMCATEGORIES)]
        return lst

    '''
    This method converts a list of RowModels into a format understandable by tf neural network.
    this method is reponsible for:
    1) converting encodings from EagerTensors to Numpy arrays
    2) organizing the encodings and training labels into a tuple
    '''
    @staticmethod
    def convToNNFormat(rows: list) -> tuple:
        strs, enc, labels = [], [], []
        for row in rows:
            strs.append(row.msg)
            npEnc = row.encoding
            enc.append(npEnc)
            label = DataCacher.oneHotEncode(row.label)
            labels.append(label)
        return strs, enc, labels

    '''
    this method uses the DataReader to read a given file, calculate the encodings,
    and add the RowModels to the database.
    '''
    def cacheFile(self, fname: str, isMod: bool) -> None:
        rows = self.dataReader.read(fname, isMod)
        numRows = len(rows)
        rows = self.applyEncodings(rows)
        self.sqcon.deleteContentByTable(fname)
        numRowsAdded = self.sqcon.addRows(fname, rows)

        if numRowsAdded != numRows:
            raise Exception(ROWMISMATCHERROR(numRows, numRowsAdded))

    '''
    This method uses cacheFile() method iteratively to cache a list of file data.
    '''
    def cacheFiles(self, fnames: list, isMod: bool) -> None:
        for file in fnames:
            self.cacheFile(file, isMod)

    '''
    This method caches all files according to FILENAMES defined in readconstants.py
    '''
    def cacheAllFiles(self, isMod: bool) -> None:
        self.cacheFiles(FILENAMES, isMod)

    '''
    This method calculates the encoding for a msg string, then converts it to a list,
    and then converts the list to a string literal. The purpose of this is to store it in the
    database. SQLite databases are unable to store lists directly.
    '''
    def getEncAsStr(self, msg: str) -> str:
        enc = self.encoder.encStr(msg)
        enc = str(list(np.array(enc)))
        return enc

    '''
    This method calculates and stores the encodings for all the RowModels in a list given.
    This is so done just before the rows are added to the database.
    '''
    def applyEncodings(self, rows: list) -> list:
        rowsLst = []
        for row in rows:
            row.encoding = self.getEncAsStr(row.msg)
            rowsLst.append(row)
        return rowsLst

    '''
    This method retrieves all the rows from the database and converts them
    to the format acceptable by the Neural Network.
    '''
    def getTrainingDataMerged(self) -> tuple:
        rows = self.sqcon.getAllRows()
        strs, enc, labels = self.convToNNFormat(rows)
        return strs, enc, labels

    '''
    This method retrieves the training data like in getTrainingDataMerged() but
    only for one table.
    '''
    def getTrainingDataByTable(self, table: str) -> tuple:
        rows = self.sqcon.getAllRowsByTable(table)
        strs, enc, labels = self.convToNNFormat(rows)
        return strs, enc, labels