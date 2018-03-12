import time, csv, sys, io, re
import twitter
from textblob import TextBlob
try:
	pass
except:
	print("ERROR MESSAGE:")
	print("You should have twitter-pyton api installed.")
	print("You should have textblob api installed.")
	print("You should have csv api installed.")
	print("You should have io api installed.")
	print("You should have re api installed.")
	print("You should have time api installed.")

def clean_tweet(string):
	# Turns out that Text blob handles emoticons for sentiment analysis as well.
	# So there is no need to replace emoticons.
	#cleaning tweets for some well known abbreviations and removing special characters.
	#removing hyperlinks as well as Twitter is attaching the Tweet link after the Tweet text.
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
	#no need to remove emoticons
	#string = re.sub(r'\b:\)\b', 'good', string)
	#string = re.sub(r'\b:D\b', 'good', string)
	#string = re.sub(r'\b:\(\b', 'sad', string)
	#string = re.sub(r'\b:-\)\b', 'good', string)
	#string = re.sub(r'\b=\)\b', 'good', string)
	#string = re.sub(r'\b\(:\b', 'good', string)
	#string = re.sub(r'\b:\\\b', 'annoyed', string)
	return string

#Python has some serious problems with non ascii characters.
def strip_non_ascii(string):
	#removing the non ascii characters from the string because Python has a lot of encoding problems
	''' Returns the string without non ASCII characters'''
	stripped = (c for c in string if 0 < ord(c) < 127)
	return ''.join(stripped)

#TO get the runtime of the program, can be ignored.
start_time = time.time()
#Access keys for the Twitter API
consumer_key = 'DGh9KwPCvFwmOGHoBajHaCEIP'
consumer_secret = 'h5nGxUW36rKDYyXJF2bJRHafLOmPwOO6hPqWAraDNMh3j0DUWc'
access_token = '963536281165803520-NQzBRAIa13bjmIYd2cEmgDKqgvFY3JP'
access_secret = 'lp2Hu3FOdJ5Z563Isb7VCUtTk2UwH03LLummrYskunnd3'

#40.7127° N, -74.0134° W One World Trade Center
#37.8199° N, -122.4783° W Golden Gate Bridge
#Getting the Latitude and Longitude from Google Places API
outfile = "tweets.csv"
latitude = 37.8199
longitude = -122.4783
km_range = 1000
num_results = 100

#auth = OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_secret)

#twitter = Twitter(
#	auth = OAuth(access_token, access_secret, consumer_key, consumer_secret)) 
#Authentication for the Twitter API
try:
	api = twitter.Api(consumer_key, consumer_secret, access_token, access_secret)
except:
	print("ERROR MESSAGE: ")
	print("Authentication Failed. Do something!!!!")

#INdexing and opening the CSV file to store the tweets in
#Stream API can also work.
try:
	indexer = ["User", "Tweet", "Latitude", "Longitude", "Sentiment", "ID"]
	csvfile = open(outfile,"w")
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(indexer)
except:
	print("ERROR MESSAGE: ")
	print("cannot open the csv file to save the tweets.")

#Main Program starts here,
#api = tweepy.API(auth)
#for status in tweepy.Cursor(api.home_timeline).items(100):
 #   with io.open("lol.txt", "w+", encoding = 'utf-8') as f:
  #  	f.write(status.text)
#f.close()
try:
	global last_id
	result_count= 0
	last_id = None
	query = api.GetSearch(geocode = (latitude, longitude, "100mi"), count=512, max_id = last_id)
	print(len(query))
except: 
	print("ERROR MESSAGE: ")
	print("Not able to query the twitter API. ")
	print("Check Connection.")
#total count is the number of tweets we have
#needed_tweets is the number of tweets we need
#we call the api until we get the amount of tweets that we need.
total_count = 1
needed_tweets = 1000
while(total_count<needed_tweets):
	query = api.GetSearch(geocode = (latitude, longitude, "100mi"), count=512, max_id = last_id)
	for result in query:
		#print(result)
		only_ascii = strip_non_ascii(result.text)
		ans = clean_tweet(only_ascii)
		#print(ans)
		#print(str(total_count) + ". " + str(ans))
		total_count += 1
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
		#print(polarity)
		#last_id gets the last ID of the tweet that was found in the last iteration
		if(not(last_id)):
			last_id = result.id
		else:
			last_id = min(result.id, last_id)
		#we use last ID so that we do not get past tweets again and again
		ID = result.id
		#print(str(last_id) +"	 + str(ID))
		row = [user, ans, latitude, longitude, polarity, ID]
		csvwriter.writerow(row)
		#Still getting same tweets again and again.
		#Twitter API is not giving access to old tweets I suppose. Maybe the result of a Standard Licence API?
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
		#print("%d tweets received as of now"%(count))
	#total_count+=count
	#print("%d is the total amount of tweets received."%(total_count))
csvfile.close()
print("--- %s seconds ---" % (time.time() - start_time))



#[6918 rows x 3 columns]
#Accuracy 0.837236195432
#Precision 0.894869638352