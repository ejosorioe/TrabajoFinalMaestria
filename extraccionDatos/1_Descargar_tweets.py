# -*- coding: utf-8 -*-
import json
from datetime import date, datetime
from pymongo import MongoClient
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey 	= '' 	# CONSUMER_KEY
csecret = '' 	# CONSUMER_SECRET
atoken 	= '' 	# APP_TOKEN
asecret = '' 	# APP_SECRET

valle_aburra = [-75.8206665, 5.9339047, -75.1776110, 6.5794602] # Cuadro qe contiene el valle de aburra

client = MongoClient('localhost', 27017)
db = client.twitter 			# twitter es la BD
tweets = db.tweets_valle_aburra # tweets_valle_aburra es la coleccion

file =  open('tweets.txt', 'a')

class listener(StreamListener):

    def on_data(self, data):
        # Se retorna los datos en formato JSON format - se necesitar hacer un decode
        try:
            decoded = json.loads(data)
            decoded["fecha_guardado"] = datetime.now()
            tweet_id = tweets.insert_one(decoded).inserted_id
            print tweet_id
            
        except Exception as e:
            print e # Para no detener el listener
            return True
   
        try:
            if decoded.get('geo') is not None:
                location = decoded.get('geo').get('coordinates')
            else:
                location = '[,]'
            text = decoded['text'].replace('\n',' ')
            user = '@' + decoded.get('user').get('screen_name')
            created = decoded.get('created_at')
            
            tweet = '%s|%s|%s|%s\n' % (user.encode('utf-8'),location,created.encode('utf-8'),text.encode('utf-8'))

            file.write(tweet)
            print tweet
            return True
        except Exception as ex:
            print ex # Para no detener el listener
            return True

    def on_error(self, status_code):
        if status_code == 420:
            print status_code
            # Retorna falso si se desconecta el stream
            return False
            
if __name__ == '__main__':
    print 'Starting'
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=valle_aburra)