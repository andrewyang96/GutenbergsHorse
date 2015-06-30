from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from mostpopular import MOSTPOPULAR
import sys
import traceback
import os
import re
import json
import cPickle

BASEPATH = os.path.dirname(os.path.realpath(__file__))
ABBREVS = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])

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
    if len(letters) == 0:
        # return None if no letters can be found
        return None
    else:
        return sentence.find(letters[0])

def ensureFirstLetterUpper(sentence):
    flIdx = findFirstLettersIdx(sentence)
    if flIdx is None:
        # return None if no letters can be found
        return None
    else:
        s = list(sentence)
        s[flIdx] = s[flIdx].upper()
        return ''.join(s)

def cleanupSentence(sentence):
    # Clean up sentence by doing the following:
    # 1. Resolve dangling quotation marks at either the front or end of the sentence.
    if sentence[0] == '"' and sentence[1:].count('"') % 2 == 0:
        sentence += '"'
    elif sentence[-1] == '"' and sentence[:-1].count('"') % 2 == 0:
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
    if sentence is None or len(sentence) > 140:
        # None is returned if sentence has no letters or it exceeds 140 characters
        return None
    else:
        # 5. If a dangling abbreviation still occurs, then just return None.
        if sentence.strip().split(" ")[-1][:-1].lower() in ABBREVS:
            print "Sentence still has dangling abbreviation:", sentence
            return None
        else:
            return sentence

def getSplitter():
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = ABBREVS
    return PunktSentenceTokenizer(punkt_param)

def tokenizeText(splitter, text):
    initList = [unicode(sentence).strip() for sentence in splitter.tokenize(text)]
    # filter out sentences that are less than two words long
    # filter out sentences that exceed 140 characters
    cleanedUpSentences = [cleanupSentence(sentence) for sentence in filter(filterSentenceFunc, initList)]
    return [sentence for sentence in cleanedUpSentences if sentence is not None]

def downloadMain(textIDs=MOSTPOPULAR):
    splitter = getSplitter()
    manifest = {}
    if not os.path.exists(os.path.join(BASEPATH, "data")):
        print "Making data directory"
        os.mkdir(os.path.join(BASEPATH, "data"))
    for textID in textIDs:
        try:
            text = downloadText(textID)
            sents = tokenizeText(splitter, text)
            manifest[textID] = len(sents)
            with open(os.path.join(BASEPATH, "data", str(textID) + ".bin"), "w") as f:
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
    with open(os.path.join(BASEPATH, "manifest.json"), "w") as f:
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
        '"Well," said Andrea, "admitting your love, why do you want me to breakfast with you?"',
        '"Oh, Mrs. Churchill; every body knows Mrs. Churchill," replied Isabella: "and I am sure I never think of that poor young man without the greatest compassion.',
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
