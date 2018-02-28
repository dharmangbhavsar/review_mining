import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler
import json
consumer_key = "fDyXXSIZ2TIdmPUf6TmWZtxIB"
consumer_secret = "YD1Olf7sgYXdjOS8wbRz7WzBiR96SHy55B8F6ZiZMOv6HOvnlA"
access_token = "340750238-PMrhm6sDjQ7RpD6iW00VrTDFMN98dOUoCdbfkb8g"
access_secret = "jJjXCNKfXJJT1VUO1f6blNzeXwCPs89yzBauep5oyaK47"
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#Error handling
if (not api):
    print ("Problem connecting to API")
    
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('tweet_data.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
    
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(locations=[-73.987013,40.747092,-73.984315,40.749789])
#Getting Geo ID for USA
#places = api.geo_search(query="USA", granularity="country")

#Copy USA id
#place_id = places[0].id
#print('USA id is: ',place_id)