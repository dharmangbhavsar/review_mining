try:
	import requests
	import json
except:
	print("requests library not found or loaded.")
	print("json library not found or loaded.")
try:
	from pprint import pprint
except:
	print("pprint library not found")


#=====================================================================================
#Testing data
documents = { 'documents': [
    { 'id': '1', 'text': 'This is a document written in English.' },
    { 'id': '2', 'text': 'Este es un document escrito en Espanol.' },
    { 'id': '3', 'text': 'Hello' },
    { 'id': '4', 'text': 'The empire state building is awesome.'}
]}
lul = documents
#=====================================================================================

#Subscription Key for Microsoft Text Analytics.
#subscription key
subscription_key="f05b33b3e4f24a908b7dbe2d17d23466"
assert subscription_key
#link for the text analytics API
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
#this is the link for sentiment 
sentiment_api_url = text_analytics_base_url + "sentiment"
language_api_url = text_analytics_base_url + "languages"
#This is to get the language of the document
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
#Querying the API with a json call with documents.
response  = requests.post(language_api_url, headers=headers, json=documents)
languages = response.json()
#Output
pprint(languages)

#TESTING
#TESTING
#KILL ME! FUCK JSON CONVERSION IN PYTHON

print("-------------------Langauges-------------------\n")
for i in range(0,4):
	for keys in languages:
		print(keys)
		if(keys=='documents'):
			#print(languages[keys][i]['iso6391Name'])
			print("lol")
			print(len(languages['documents']))
			print(type(len(languages['documents'])))
print("-------------------Languages-------------------\n")
#languagedata = json.loads(languages)
#pprint(languages['documents'][0]['detectedLanguages'][0]['iso6391Name'])  ------------- prints- 'en'

#Setting the language detected by Microsoft API to the lul documents
for i in range(len(languages['documents'])):
	#for key in keyy['detectedLanguages']:
	#	lul['documents'][0]['language'] = key['iso6391Name']
	lul['documents'][i]['language'] = languages['documents'][i]['detectedLanguages'][0]['iso6391Name']
pprint(languages['documents'])
#for key in documents['documents']:
	#print(key)
#for key in documents:
	#key['documents'][0]['']

#Recalling the API
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(sentiment_api_url, headers=headers, json=documents)
sentiments = response.json()

#Ahhh... Such are the FUCKIN SENTIMENTS
#Printing Sentiments
print("---------------------------------Sentiments-----------------------------------")
pprint(documents)
pprint(sentiments)
print("---------------------------------Sentiments-----------------------------------")
j = 0
#Trying to save the Languages obtained by API calls into the json structure
#This is fucking weird
#Why DOES PYTHON GO INTO SO MANY CODEC ERRORS
#C++ is Better! 100%

for keyy in sentiments['documents'][0]:
	for key in keyy:
		for i in range(len(languages['documents'])):
			if(str(key) == 'score' and i==j):
				lul['documents'][i]['score'] = keyy[key]
	j+=1
#Checking
for key in lul['documents'][0]:
	print(key)
pprint(lul)
