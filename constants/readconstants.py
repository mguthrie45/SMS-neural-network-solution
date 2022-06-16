import os
from typing import Generator
from tensorflow.python.framework.ops import EagerTensor

BASEPATH = "C:\spring22\data\labeled"
FILENAMES = ["a", "b", "c", "d", "e"]
TESTFILENAME = 'tst'
COLTYPES = [str, int]
UNMODCOLTYPES = [str]
DATACOLS = ["MSG", "LABEL"]
UNMODDATACOLS = ["MSG"]
NUMCOLS = len(DATACOLS)
NUMUNMODCOLS = len(UNMODDATACOLS)
DELIMITER = "~"

PARSEERR1 = f"parseLine Error: columns parsed less than number of unmodified columns."
PARSEERR2 = f"parseLine Error: columns parsed more than number of unmodified columns."
PARSEERR3 = f"parseLine Error: columns parsed less than number of modified columns."
PARSEERR4 = f"parseLine Error: columns parsed more than number of modified columns."
COLTYPEERR = f"Column Type Error: column does not satisfy type requirement"