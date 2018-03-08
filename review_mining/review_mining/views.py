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

import sys, csv, datetime

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
		pass
	
	def post(self,request):
		consumer_key = "DGh9KwPCvFwmOGHoBajHaCEIP"
		consumer_secret = "h5nGxUW36rKDYyXJF2bJRHafLOmPwOO6hPqWAraDNMh3j0DUWc"
		access_key = "963536281165803520-NQzBRAIa13bjmIYd2cEmgDKqgvFY3JP"
		access_secret = "lp2Hu3FOdJ5Z563Isb7VCUtTk2UwH03LLummrYskunnd3"

		post = request.POST
		
		search_name = post.get('name')
		latitude = float(post.get('lat'))
		longitude = float(post.get('lng'))
		max_range = 1 			# search range in kilometres
		num_results = 5			# minimum results to obtain
		
		twitter = Twitter(
		        auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

		result_count = 0
		last_id = None
		all_tweets = []

		while result_count <  num_results:
			query = twitter.search.tweets(q = "", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)

			for result in query["statuses"]:
				if result["geo"]:
					user = result["user"]["screen_name"]
					text = result["text"]
					latitude = result["geo"]["coordinates"][0]
					longitude = result["geo"]["coordinates"][1]

					if self.is_related(text, search_name):
						all_tweets.append({"user": user, "text": text, "lat": latitude, "lng": longitude })
						result_count += 1
				last_id = result["id"]

			
		return render(request, self.template_name, {'all_tweets':all_tweets, 'search_name': search_name})

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