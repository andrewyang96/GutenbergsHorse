from twitterconfig import *
import tweepy

class TwitterAPI:
    def __init__(self):
        consumer_key = CONSUMERKEY
        consumer_secret = CONSUMERSECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = ACCESSTOKEN
        access_token_secret = ACCESSTOKENSECRET
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
 
    def tweet(self, message):
        self.api.update_status(status=message)
