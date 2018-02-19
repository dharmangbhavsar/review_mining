
try:
	import twitter
	from textblob import TextBlob
	import csv
	import sys
	import io
	import re
except:
	print("ERROR MESSAGE:")
	print("You should have twitter-pyton api installed.")
	print("You should have textblob api installed.")
	print("You should have csv api installed.")
	print("You should have io api installed.")
	print("You should have re api installed.")

def strip_non_ascii(string):
	#removing the non ascii characters from the string because Python has a lot of encoding problems
	''' Returns the string without non ASCII characters'''
	stripped = (c for c in string if 0 < ord(c) < 127)
	return ''.join(stripped)

def clean_tweet(string):
	# Turns out that Text blob handles emoticons for sentiment analysis as well.
	# So there is no need to replace emoticons.
	#cleaning tweets for some well known abbreviations and removing special characters.
	string = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', string)
	string = re.sub(r'\bthats\b', 'that is', string)
	string = re.sub(r'\bive\b', 'i have', string)
	string = re.sub(r'\bim\b', 'i am', string)
	string = re.sub(r'\bya\b', 'yeah', string)
	string = re.sub(r'\bcant\b', 'can not', string)
	string = re.sub(r'\bwont\b', 'will not', string)
	string = re.sub(r'\bid\b', 'i would', string)
	string = re.sub(r'wtf', 'what the fuck', string)
	string = re.sub(r'\bwth\b', 'what the hell', string)
	string = re.sub(r'\br\b', 'are', string)
	string = re.sub(r'\bu\b', 'you', string)
	string = re.sub(r'\bk\b', 'OK', string)
	string = re.sub(r'\bsux\b', 'sucks', string)
	string = re.sub(r'\bno+\b', 'no', string)
	string = re.sub(r'\bcoo+\b', 'cool', string)
	return string

consumer_key = 'DGh9KwPCvFwmOGHoBajHaCEIP'
consumer_secret = 'h5nGxUW36rKDYyXJF2bJRHafLOmPwOO6hPqWAraDNMh3j0DUWc'
access_token = '963536281165803520-NQzBRAIa13bjmIYd2cEmgDKqgvFY3JP'
access_secret = 'lp2Hu3FOdJ5Z563Isb7VCUtTk2UwH03LLummrYskunnd3'

#40.7127° N, 74.0134° W One World Trade Center
outfile = "tweets.csv"
latitude = 34.0430
longitude = -118.2673
km_range = 1000
num_results = 100

#auth = OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_secret)

#twitter = Twitter(
#	auth = OAuth(access_token, access_secret, consumer_key, consumer_secret)) 
try:
	api = twitter.Api(consumer_key, consumer_secret, access_token, access_secret)
except:
	print("ERROR MESSAGE: ")
	print("Authentication Failed. Do something!!!!")


try:
	indexer = ["User", "Tweet", "Latitude", "Longitude", "Sentiment"]
	csvfile = open(outfile,"w+")
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(indexer)
except:
	print("ERROR MESSAGE: ")
	print("cannot open the csv file to save the tweets.")


#api = tweepy.API(auth)
#for status in tweepy.Cursor(api.home_timeline).items(100):
 #   with io.open("lol.txt", "w+", encoding = 'utf-8') as f:
  #  	f.write(status.text)
#f.close()
try:
	result_count= 0
	query = api.GetSearch(geocode = (latitude, longitude, "100mi"), until = "2018-02-25", since = "2010-01-01", count=512)
	print(len(query))
except: 
	print("ERROR MESSAGE: ")
	print("Not able to query the twitter API. ")
	print("Check Connection.")

count = 1
for result in query:
	print(result)
	only_ascii = strip_non_ascii(result.text)
	ans = clean_tweet(only_ascii)
	print(ans)
	print(str(count) + ". " + str(ans))
	count += 1
	user = result.user.screen_name
	text = ans  
	sentiments = TextBlob(ans)
	setup = sentiments.sentiment.polarity
	polarity = "positive"
	if setup >= 0.1:
		polarity = 'positive'
	elif setup <= -0.1:
		polarity = 'negative'
	else:
		polarity = 'neutral'
	print(polarity)
	row = [user, ans, latitude, longitude, polarity]
	csvwriter.writerow(row)
	#print(result.full_text)
	#if(result["geo"]):
	#	user = result["user"]["screen_name"]
	#	text = result["text"]
	#	t=text
	#	text = str(t)
	#	latituded = result["geo"]["coordinates"][0]
	#	longituded = result["geo"]["coordinates"][1
	#	#-----------------------------------------------------------------------
	#	# now write this row to our CSV file
		#-----------------------------------------------------------------------
	#	row = [ user, text, latituded, longituded[] ]
	#	csvwriter.writerow(row)
	#	result_count += 1
	#	last_id = result["id"]
csvfile.close()
