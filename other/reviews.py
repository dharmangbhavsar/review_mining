import time
import csv , sys
import six 
from googleplaces import GooglePlaces, types, lang

API_KEY = 'AIzaSyBdx5s56pNhrwTfCoqxqlUk2YjABXJub9U'

user_input = input("Enter a restaurant")
place = GooglePlaces(API_KEY)
result = place.text_search(query= user_input)	#calling text search on a particular keyword

if result.has_attributions:
	print (result.html_attributions)

for loc in result.places:	#getting details about the place
	print (loc.name)
	print (loc.geo_location)
	loc.get_details()
	print (loc.rating) 

	place.text_search
	
