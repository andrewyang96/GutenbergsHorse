import random
import cPickle
import json
import os

def weightedChoice(choices):
    total = sum(val for key, val in choices.items())
    r = random.uniform(0, total)
    upto = 0
    for choice, val in choices.items():
        if upto + val > r:
            return choice
        upto += val
    assert False, "Shouldn't get here"

def loadSentence(textID):
    FILEPATH = os.path.join(os.getcwd(), "data", textID + ".bin")
    with open(FILEPATH, 'r') as f:
        return cPickle.load(f)

def chooseSentence():
    with open(os.path.join(os.getcwd(), "manifest.json"), "r") as f:
        manifest = json.load(f)
    textID = weightedChoice(manifest)
    sents = loadSentence(textID)
    return (textID, random.choice(sents))
