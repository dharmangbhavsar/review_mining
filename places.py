try:
    from googleplaces import GooglePlaces, types, lang
except:
    print("Download and Install Google Places Library")
try:
    from pprint import pprint
    import json, sys, codecs, io
except: 
    print("Not able to load some basic libraries.")

#to get only ascii character in strings. 
#Yeah,    
def strip_non_ascii(string):
    #removing the non ascii characters from the string because Python has a lot of encoding problems
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)
#if sys.stdout.encoding != 'cp850':
 #   sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
#if sys.stderr.encoding != 'cp850':
 #   sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')
API_KEY = "AIzaSyC8gpRUz3DP0BozirgjWNom_h33QI_t7X4"
google_places = GooglePlaces(API_KEY)
#saving the names of places and reivews in .txt file
f = open("lol.txt", "w")
#latitude and longitude of a place
latlong = {"lat":38.8814, "lng":-77.0365}
#main Google places query. 
query_result = google_places.nearby_search(lat_lng = latlong, radius = 2000, rankby = "prominence", type = "library")
for place in query_result.places:
    # Returned places from a query are place summaries.
    pprint (place.name)
    #pprint (place.geo_location)
    #pprint (place.reference)

    # The following method has to make a further API call.
    place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    #pprint (place.details) # A dict matching the JSON response from Google.
    #for key in place.details:
     #   print(key)
    #lul = json.dumps(place.details)
    f.write("----------------------------------------------------------New Place-----------------------------------------------------------------\n")
    f.write(str(place.name))
    f.write("\n")
    data = place.details
    if 'reviews' in data.keys():
        for k in data['reviews']:
            x = strip_non_ascii(str(k))
            l = strip_non_ascii(str(k['text']))
            #f.write(x)
            f.write(l)
            f.write("\n")
    #for i in range (0, len(data)):
     #   for j in range (0,len(data["reviews"])):
      #      s = data["reviews"][j]
       #     print(unicode(s, "utf-8"))
    #print (place.local_phone_number)
    #print (place.international_phone_number)
    #print (place.website)
    #print (place.url)
    #print(place.details["reviews"])