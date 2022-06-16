MODELDIR = "./Model"
MODELPATH = "./Model/model"
MODELNAME = "model"

RESULTSPATH  ="./Model/results.p"

EPOCHS = 7

OPTFPR = 0.04

'''
Given the false positive rates (iterable) and thresholds (iterable),
this function finds the best threshold that satisfied the OPTFPR (false positive rate)
'''
def findBestThreshold(fprs, thresholds):
    thresh = None
    diff = float('inf')
    for i, t in enumerate(thresholds):
        fpr = fprs[i]
        d = abs(fpr - OPTFPR)
        if d < diff:
            diff = d
            thresh = t
        if d == diff and t < thresh:
            thresh = t

    return thresh