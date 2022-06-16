from constants.readconstants import *
from RowModel import *

'''
##########IMPORTANT##########
The isMod parameter is used in every method. This variables
tells the DataReader whether or not the training labels have been added yet (modified).
If isMod = False, then the DataReader will only expect to read "NUMUNMODCOLS" columns.
If isMod = True, then the DataReader will expect to read "NUMCOLS" columns.
'''

'''
The DataReader class is responsible for parsing and reading the raw text data using
the constants defined in readconstants.py.
'''
class DataReader:
    '''
    basePath: the directory of the data, which can be found in readconstants.py
    filenames: the list of the data files, which can be found in readconstants.py
    ext: the extension of the data files (default is 'txt')
    '''
    def __init__(self, basePath: str, filenames: list, ext: str = 'txt'):
        self.base = basePath
        self.filnames = filenames
        self.nfiles = len(filenames)
        self.ext = ext

    '''
    responsible for:
    1) removing whitespace, the \n character, and any "" quotes that may cause bugs
    2) ommitting blank lines
    3) using verifyParsed method to raise any formatting related exceptions
    4) turning the parsed data into a RowModel object
    '''
    @staticmethod
    def parseLine(line: str, isMod: bool) -> RowModel:
        line = line.strip()
        if "\n" in line:
            line = line[:-1]
        parsed = line.split(DELIMITER)
        if parsed == ['']:
            return None

        DataReader.verifyParsed(parsed, line, isMod)

        if isMod:
            parsed[1] = int(parsed[1].strip())
        parsed[0] = parsed[0].replace('"', '')
        return RowModel(*parsed)

    '''
    this method raises any format or type related exceptions (check readconstants.py for the exceptions)
    responsible for:
    1) Making sure the number of parsed columns match the columns expected (based on the isMod parameter)
    2) Making sure each element in the parsed list is of the correct type
    '''
    @staticmethod
    def verifyParsed(parsed: list, line: str, isMod: bool) -> None:
        if isMod:
            if len(parsed) < NUMCOLS:
                raise Exception(f"{PARSEERR1} \n Tried to parse: {line}")
            elif len(parsed) > NUMCOLS:
                raise Exception(f"{PARSEERR2} \n Tried to parse: {line}")
        else:
            if len(parsed) < NUMUNMODCOLS:
                raise Exception(f"{PARSEERR3} \n Tried to parse: {line}")
            elif len(parsed) > NUMUNMODCOLS:
                raise Exception(f"{PARSEERR4} \n Tried to parse: {line}")

        '''types = COLTYPES if isMod else UNMODCOLTYPES
        for i, ty in enumerate(types):
            if not isinstance(parsed[i], ty):
                raise Exception(f"{COLTYPEERR} \n column {i} does not match type {ty}")'''

    '''
    this method reads one file and returns a list of all the RowModels it contains
    '''
    def read(self, fname: str, isMod: bool) -> list:
        path = os.path.join(self.base, f'{fname}.{self.ext}')
        rows = []
        with open(path, "r", encoding='utf-8') as f:
            while True:
                s = f.readline()
                if not s or s.strip() == '\n':
                    break
                row = self.parseLine(s, isMod)
                if row:
                    rows.append(row)
        return rows

    '''
    this method iteratively calls read() method on all the data files.
    returns a list, each of which contain a list of RowModels corresponding to each file.
    '''
    def readAllFiles(self, isMod: bool) -> list:
        rowLists = []
        for file in self.filnames:
            gen = self.read(file, isMod)
            rowLists.append(gen)
        return rowLists