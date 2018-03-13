from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from twitter import *
import nltk, pickle, re, nltk.tag, nltk.data
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown, wordnet, stopwords
from pprint import pprint
import sys, csv, datetime, json, urllib.request, codecs, io
import six, difflib
from googleplaces import GooglePlaces, types, lang
from textblob import TextBlob

#So that Python doesnt get into Codec Errors.
def strip_non_ascii(string):
    #removing the non ascii characters from the string because Python has a lot of encoding problems
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

#Migrated from FBVs to CBVs as CBVs handle get and post logic cleanly
#----DASHBOARD----
class index(View):
	template_name = 'review_mining/index.html'	
	
	def get(self, request):
		return render(request, self.template_name)
	
	def post(self,request):
		pass

class get_reviews(View):
	template_name = "review_mining/get_reviews.html"

	def get(self, request):
		consumer_key = "ghkzJ4mR0ywmIHIk9exDqfYBJ"
		consumer_secret = "EDaAlc9msQtoEY8TBQzIRKBFOMo50hp3FsWVtsGpXG05Mppk05"
		access_key = "1600221949-p6YbkDsmCEYq1MSpNWsL7gfsSrztnEtZtkXWksG"
		access_secret = "MahHvrzl1I5sQDEGYBVMQ6HuwIGagow2zs3DcXVFztEYc"
		# consumer_key = "DGh9KwPCvFwmOGHoBajHaCEIP"
		# consumer_secret = "h5nGxUW36rKDYyXJF2bJRHafLOmPwOO6hPqWAraDNMh3j0DUWc"
		# access_key = "963536281165803520-NQzBRAIa13bjmIYd2cEmgDKqgvFY3JP"
		# access_secret = "lp2Hu3FOdJ5Z563Isb7VCUtTk2UwH03LLummrYskunnd3"
		# consumer_key = "fDyXXSIZ2TIdmPUf6TmWZtxIB"
		# consumer_secret = "YD1Olf7sgYXdjOS8wbRz7WzBiR96SHy55B8F6ZiZMOv6HOvnlA"
		# access_key = "340750238-PMrhm6sDjQ7RpD6iW00VrTDFMN98dOUoCdbfkb8g"
		# access_secret = "jJjXCNKfXJJT1VUO1f6blNzeXwCPs89yzBauep5oyaK47"

		get = request.GET
		
		search_name = get.get('name')
		latitude = float(get.get('lat'))
		longitude = float(get.get('lng'))
		location_type = get.get('type')

		max_range = 1			# search range in kilometres
		num_results = 5			# minimum results to obtain
		
		twitter = Twitter(
		        auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

		result_count = 0
		t_plus, g_plus, t_minus, g_minus =0,0,0,0
		loop_cnt = 100
		last_id = None
		all_tweets = []

		# words_f = open("tweets.data","rb")
		# all_tweets = pickle.load(words_f)
		# words_f.close()
		# return render(request, self.template_name, {'all_tweets':all_tweets, 'search_name': search_name, 'lat': latitude, 'lng': longitude})
		
		while result_count <  num_results and loop_cnt > 0:
			query = twitter.search.tweets(q = "", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)

			for result in query["statuses"]:
				if result["geo"]:
					tweet = result["text"]
					
					if result['lang'] == "en":
						display_name = result["user"]["name"]
						user_name = result["user"]["screen_name"]
						profile_img = result["user"]["profile_image_url_https"]
						setup = TextBlob(tweet)
						rating = setup.sentiment.polarity
						rating = float("{0:.1f}".format(((rating+1)/2)*5))

						if self.is_related(tweet, search_name):
							if rating > 2:
								t_plus +=1
							else:
								t_minus+=1
							all_tweets.append({"tweet": tweet, "display_name": display_name, "user_name": user_name, "profile_img": profile_img, "rating": rating })
							result_count += 1


				last_id = result["id"]
				loop_cnt -= 1
		
		if t_plus + t_minus != 0:		
			t_plus = int(t_plus*100/(t_plus + t_minus))
			t_minus = 100 - t_plus

		API_KEY = 'AIzaSyCkBJ4fQJUupdRiE1sgfRArEbGhCiZIVr0'

		rating = []
		user_input = search_name
		place = GooglePlaces(API_KEY)
		result = place.text_search(query= user_input)	#calling text search on a particular keyword
		for loc in result.places:	#getting details about the place
			#print (loc.name)
			#print (loc.geo_location)
			loc.get_details()
			result_count = 0
			#print (loc.rating) 
			#place.text_search
			#rating has the reviews, author_name and ratings in a dictionary style.
			#Getting details
			data = loc.details
			if 'reviews' in data.keys():
				for k in data['reviews']:
					#Cleaning tweets.
					x = strip_non_ascii(str(k))
					l = strip_non_ascii(str(k['text']))
					#print(k['rating'],": ",l)
					#f.write(x)
					#print(l)
					#Appending ratings.
					
					rating.append({"text": l, "rating": k['rating'], "user_name": k['author_name'], "img": k['profile_photo_url'], 'a_url': k['author_url']})

					if k['rating'] > 2:
						g_plus +=1
					else:
						g_minus+=1
					result_count += 1

		if g_plus + g_minus > 0:
			g_plus = int(g_plus*100/(g_plus + g_minus))
			g_minus = 100 - g_plus
						
		latlong = {"lat":latitude, "lng":longitude}
		#main Google places query. 
		query_result = place.nearby_search(lat_lng = latlong, radius = 2000, rankby = "prominence", type = location_type)
		all_nearby_places = []
		limit = 9
		for place in query_result.places:
		    # Returned places from a query are place summaries.
		    if limit <= 0: 
		    	break
		    else:
		    	limit -= 1
		    if place.name != search_name:
			    #pprint (place.geo_location)
			    #pprint (place.reference)
			    # Referencing any of the attributes below, prior to making a call to
			    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
			    # print("----------------------------")
			    place.get_details()
			    #pprint(vars(place))
			    # print(place.formatted_address)
			    # print(place.rating)
			    # print(place.geo_location)
			    #place.rating or place._rating
			    #place.photos[0].photo_reference
			    # The following method has to make a further API call.

			    if len(place.photos) > 0:
			    	all_nearby_places.append({'image': place.photos[0].photo_reference, 'name': place.name, 'rating': place.rating, 'location': place.geo_location, 'address': place.formatted_address, 'type': place.types[0] })
			    else:
			    	all_nearby_places.append({'name': place.name, 'rating': place.rating, 'location': place.geo_location, 'address': place.formatted_address, 'type': place.types[0] })

			    if not place.rating:
			    	all_nearby_places[len(all_nearby_places) - 1]['rating'] = 0

		all_nearby_places = sorted(all_nearby_places, key=lambda k: k['rating'], reverse = True)
		return render(request, self.template_name, {'all_tweets':all_tweets, 'search_name': search_name, 'lat': latitude, 'lng': longitude, 'google_ratings':rating, 't_plus': t_plus, 't_minus': t_minus, 'g_plus': g_plus, 'g_minus': g_minus, 'key': "AIzaSyCkBJ4fQJUupdRiE1sgfRArEbGhCiZIVr0", "all_nearby_places": all_nearby_places})
	
	def post(self,request):
		pass

	def is_related(self, text, search):
		words = text.split()
		word = search.split()
		tweet_words = len(words)
		query_words = len(word)
		#all_words contains the set of words equal to the search term
		all_words = []
		for i in range(0,tweet_words):
			t = ""
			for j in range(0,query_words):
				if((i+j)<tweet_words):
					t += words[i+j]
					t+=" "
			all_words.append(t)
		#printing all works
		#print(all_words)
		ans = difflib.get_close_matches(search, all_words, cutoff=0.7)
		#Prints Yes if the search term is present
		if(len(ans) > 0):
			return True
		else: 
			return False
		# lemmatizer = WordNetLemmatizer()
		# s = re.sub('[^0-9a-zA-Z ]+', '', search).lower()
		# words = set()
		# for w in nltk.word_tokenize(s):
		# 	words.add(lemmatizer.lemmatize(w))
		
		# flag = False
		# t = re.sub('[^0-9a-zA-Z ]+', '', tweet).lower()

		# for w in nltk.word_tokenize(t):
		# 	if w in words:
		# 		flag = True
		# 		break

		# return flag


	#---------------------------------------------------------------------------------------------------------------------
	#Now Starts Google Places Reviews.
	#---------------------------------------------------------------------------------------------------------------------
