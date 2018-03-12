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
import sys, csv, datetime
import six 
from googleplaces import GooglePlaces, types, lang

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
		consumer_key = "DGh9KwPCvFwmOGHoBajHaCEIP"
		consumer_secret = "h5nGxUW36rKDYyXJF2bJRHafLOmPwOO6hPqWAraDNMh3j0DUWc"
		access_key = "963536281165803520-NQzBRAIa13bjmIYd2cEmgDKqgvFY3JP"
		access_secret = "lp2Hu3FOdJ5Z563Isb7VCUtTk2UwH03LLummrYskunnd3"

		get = request.GET
		
		search_name = get.get('name')
		latitude = float(get.get('lat'))
		longitude = float(get.get('lng'))
		max_range = 1 			# search range in kilometres
		num_results = 0		# minimum results to obtain
		
		twitter = Twitter(
		        auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

		result_count = 0
		loop_cnt = 1000
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
					display_name = result["user"]["name"]
					user_name = result["user"]["screen_name"]
					profile_img = result["user"]["profile_image_url_https"]

					if self.is_related(tweet, search_name):
						all_tweets.append({"tweet": tweet, "display_name": display_name, "user_name": user_name, "profile_img": profile_img })
						result_count += 1
				last_id = result["id"]
				loop_cnt -= 1
			
		return render(request, self.template_name, {'all_tweets':all_tweets, 'search_name': search_name, 'lat': latitude, 'lng': longitude})
	
	def post(self,request):
		pass

	def is_related(self, tweet, search):
		lemmatizer = WordNetLemmatizer()
		s = re.sub('[^0-9a-zA-Z ]+', '', search).lower()
		words = set()
		for w in nltk.word_tokenize(s):
			words.add(lemmatizer.lemmatize(w))
		
		flag = False
		t = re.sub('[^0-9a-zA-Z ]+', '', tweet).lower()

		for w in nltk.word_tokenize(t):
			if w in words:
				flag = True
				break

		return flag


		#---------------------------------------------------------------------------------------------------------------------
		#Now Starts Google Places Reviews.
		#---------------------------------------------------------------------------------------------------------------------
		API_KEY = 'AIzaSyBdx5s56pNhrwTfCoqxqlUk2YjABXJub9U'

		user_input = search_name
		place = GooglePlaces(API_KEY)
		result = place.text_search(query= user_input)	#calling text search on a particular keyword
		for loc in result.places:	#getting details about the place
			#print (loc.name)
			#print (loc.geo_location)
			loc.get_details()
			#print (loc.rating) 
			#place.text_search
			#rating has the reviews, author_name and ratings in a dictionary style.
			rating = []
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
					rating.append({"rating": k['rating'], "user_name": k['author_name'], "text": l})
					#print("\n")
			#print(rating)
