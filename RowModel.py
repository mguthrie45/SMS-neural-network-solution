from constants.readconstants import *

class RowModel:
    def __init__(self, msg: list, label: int = None, encoding: EagerTensor = None):
        self.msg = msg
        self.encoding = encoding
        self.label = label