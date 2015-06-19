from selectsentence import chooseSentence
from twitterapi import TwitterAPI
import datetime
 
if __name__ == "__main__":
    twitter = TwitterAPI()
    sentence = chooseSentence()
    twitter.tweet(sentence)
    print "Tweeted:", sentence, "at", datetime.datetime.now()
