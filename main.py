from selectsentence import chooseSentence
from twitterapi import TwitterAPI
import datetime
 
if __name__ == "__main__":
    twitter = TwitterAPI()
    textID, sentence = chooseSentence()
    twitter.tweet(sentence)
    print "Using tweet from", textID
    print "Sentence:"
    print sentence
    print "Timestamp:"
    print datetime.datetime.now()
    print "-"*60
