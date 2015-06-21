from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.tokenize.punkt import PunktSentenceTokenizer
from mostpopular import MOSTPOPULAR
import sys
import traceback
import os
import re
import json
import cPickle

def downloadText(textID):
    print "Downloading", textID
    text = strip_headers(load_etext(textID)).strip()
    return text

def countWords(sentence):
    return len(re.findall(r'\w+', sentence))

def filterSentenceFunc(sentence):
    # Return True only if these conditions are satisfied:
    # 1. Sentence has at least two words.
    # 2. Sentence has at most 140 characters.
    return countWords(sentence) >= 2 and len(sentence) <= 140

def findFirstLettersIdx(sentence):
    letters = re.findall(r'[a-zA-Z]', sentence)
    return sentence.find(letters[0])

def ensureFirstLetterUpper(sentence):
    flIdx = findFirstLettersIdx(sentence)
    s = list(sentence)
    s[flIdx] = s[flIdx].upper()
    return ''.join(s)

def cleanupSentence(sentence):
    # Clean up sentence by doing the following:
    # 1. Resolve dangling quotation marks at either the front or end of the sentence.
    if sentence[0] == '"' and '"' not in sentence[1:]:
        sentence += '"'
    elif sentence[-1] == '"' and '"' not in sentence[:-1]:
        sentence = '"' + sentence
    # 2. Resolve dangling parenthesis at either the front or end of the sentence.
    if "(" in sentence and ")" not in sentence:
        sentence += ")"
    elif ")" in sentence and "(" not in sentence:
        sentence = '(' + sentence
    # 3. Resolve dangling brackets at either the front or end of the sentence.
    if "[" in sentence and "]" not in sentence:
        sentence += "]"
    elif "]" in sentence and "[" not in sentence:
        sentence = "[" + sentence
    # 4. Capitalize the first letter of the sentence (may not be at index 0).
    sentence = ensureFirstLetterUpper(sentence)
    return sentence

def tokenizeText(splitter, text):
    initList = [unicode(sentence).strip() for sentence in splitter.tokenize(text)]
    # filter out sentences that are less than two words long
    # filter out sentences that exceed 140 characters
    return [cleanupSentence(sentence) for sentence in filter(filterSentenceFunc, initList)]

def downloadMain(textIDs=MOSTPOPULAR):
    splitter = PunktSentenceTokenizer()
    manifest = {}
    if not os.path.exists(os.path.join(os.getcwd(), "data")):
        print "Making data directory"
        os.mkdir(os.path.join(os.getcwd(), "data"))
    for textID in textIDs:
        try:
            text = downloadText(textID)
            sents = tokenizeText(splitter, text)
            manifest[textID] = len(sents)
            with open(os.path.join(os.getcwd(), "data", str(textID) + ".bin"), "w") as f:
                print "Dumping", textID
                cPickle.dump(sents, f)
        except Exception, e:
            print "Error:"
            traceback.print_exc(file=sys.stdout)
            try: # rollback changes to manifest
                del manifest[textID]
            except KeyError:
                pass
    print "Here's the manifest:"
    print manifest
    with open(os.path.join(os.getcwd(), "manifest.json"), "w") as f:
        json.dump(manifest, f)

def runTestcases():
    cases = [
        '"She is well, but sad.',
        '"I\'m not a bit changed--not really.',
        "GREEK CUT OPEN-WORK PATTERN (fig.",
        "WHEEL BEGUN IN HOLE GROUND.]",
        'while he storms, \'t is well \nThat thou descend."',
        'my nice \nwaistcoat!"',
        "Shouldn't change:",
        "But have I now seen Death?",
        '"I am called," said Andrea.',
        '"Well," said Andrea, "admitting your love, why do you want me to breakfast with you?"'
    ]
    for case in cases:
        print "Original"
        print case
        print "cleanupSentence"
        print cleanupSentence(case)
        print

if __name__ == "__main__":
    print "Running test cases for cleanupSentence. downloadMain() runs the download utility."
    runTestcases()
