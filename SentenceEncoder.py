#pip install tensorflow-hub
import tensorflow_hub as tfhub
from tensorflow.python.framework.ops import EagerTensor

''' expect this to take a bit of time to initialize '''
class SentenceEncoder:
    URL = "https://tfhub.dev/google/universal-sentence-encoder/4"
    def __init__(self):
        self.encModel = self.loadModel()
        self.encLen = self.findEncLen()

    ''' This method loads the encoder model from tensorflow dev hub '''
    def loadModel(self):
        return tfhub.load(self.URL)

    ''' This method finds the length of an encoding (size of NN input layer) '''
    def findEncLen(self) -> int:
        lst = ['']
        enc = self.encModel(lst)
        return len(enc)

    ''' This method calculates and returns the encoding of one string as an EagerTensor object (similar to a list)'''
    def encStr(self, s: str) -> EagerTensor:
        sentences = [s]
        return self.encModel(sentences)[0]

    ''' This method calls encStr() method iteratively and returns the encodings of multiple strings '''
    def encStrs(self, lst: list) -> list:
        return self.encModel(lst)


#Driver code for testing/debugging purposes
if __name__ == '__main__':
    senc = SentenceEncoder()
    slst = [
        'What is the location of your store?',
        'What is your most popular product?',
        'Would I be able to get an order delivered?',
        'PLEASE STOP MESSAGING ME',
        'How should I go about implementing warp drive?',
        'You wanna go on a date?',
        '2+2=4 right?',
        'a;lsdkhaiuoa;sebg'
    ]

    enc = senc.encStrs(slst)
    for i, e in enumerate(enc):
        disp = f'{slst[i]} \n {e} \n'
        print(disp)