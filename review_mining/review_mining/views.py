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
from textblob import TextBlob

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
		num_results = 5		# minimum results to obtain
		
		twitter = Twitter(
		        auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

		result_count = 0
		loop_cnt = 2
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
					setup = TextBlob(tweet)
					sentiment_score = setup.sentiment.polarity
					if sentiment_score > 0.2:
						s_class = "success"
					elif sentiment_score > -0.2:
						s_class = "warning"
					else:
						s_class = "danger"

					sentiment_score = float("{0:.2f}".format(((sentiment_score+1)/2)*100))

					if self.is_related(tweet, search_name):
						all_tweets.append({"tweet": tweet, "display_name": display_name, "user_name": user_name, "profile_img": profile_img, "sentiment_score": sentiment_score, "s_class": s_class })
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
