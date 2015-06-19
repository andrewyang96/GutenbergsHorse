from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.tokenize.punkt import PunktSentenceTokenizer
from mostpopular import MOSTPOPULAR
import os
import re
import cPickle

def downloadTexts(textIDs):
    d = []
    for i in textIDs:
        print "Downloading", i
        text = strip_headers(load_etext(i)).strip()
        d.append(text)
    return d

def countWords(sentence):
    return len(re.findall(r'\w+', sentence))

def tokenizeText(splitter, text):
    initList = [unicode(sentence).strip() for sentence in splitter.tokenize(text)]
    # filter out sentences that are less than two words long
    # filter out sentences that exceed 140 characters
    return [sentence for sentence in initList if countWords(sentence) >= 2 and len(sentence) <= 140]

def tokenizeTexts(texts):
    splitter = PunktSentenceTokenizer()
    ret = []
    for text in texts:
        sentences = tokenizeText(splitter, text)
        ret.append(sentences)
    return ret

def retrieveSentences():
    texts = downloadTexts(MOSTPOPULAR)
    return tokenizeTexts(texts)

if __name__ == "__main__":
    sents = retrieveSentences()
    with open(os.path.join(os.getcwd(), "gutenbergpickle.bin"), 'w') as f:
        print "Dumping to file"
        cPickle.dump(sents, f)
