import random
import cPickle
import os

def loadSentences():
    FILEPATH = os.path.join(os.getcwd(), "gutenbergpickle.bin")
    with open(FILEPATH, 'r') as f:
        return cPickle.load(f)

def chooseSentence():
    sents = [sent for sentlist in loadSentences() for sent in sentlist]
    return random.choice(sents)
