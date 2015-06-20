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

def filterSentenceFunc(sentence):
    # Return True only if these conditions are satisfied:
    # 1. Sentence has at least two words.
    # 2. Sentence has at most 140 characters.
    return countWords(sentence) >= 2 and len(sentence) <= 140

def cleanupSentence(sentence):
    # Clean up sentence by doing the following:
    # 1. Resolve dangling quotation marks at either the front or end of the sentence.
    # 2. Resolve dangling parenthesis at either the front or end of the sentence.
    # 3. Resolve dangling brackets at either the front or end of the sentence.
    # 4. Capitalize the first letter of the sentence (may not be at index 0).
    return sentence # TODO: change
    # Test cases:
    # "She is well, but sad.
    # "I'm not a bit changed--not really.
    # GREEK CUT OPEN-WORK PATTERN (fig.
    # WHEEL BEGUN IN HOLE GROUND.]
    # while he storms, 't is well \nThat thou descend."
    # my nice \nwaistcoat!"
    # Shouldn't change:
    # But have I now seen Death?
    # "I am called," said Andrea.
    # "Well," said Andrea, "admitting your love, why do you want me to breakfast with you?"

def tokenizeText(splitter, text):
    initList = [unicode(sentence).strip() for sentence in splitter.tokenize(text)]
    # filter out sentences that are less than two words long
    # filter out sentences that exceed 140 characters
    return [cleanupSentence(sentence) for sentence in filter(filterSentenceFunc, initList)]

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
