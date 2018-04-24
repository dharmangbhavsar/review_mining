# Twitter Review Mining

**Demo Link** - https://drive.google.com/file/d/1S6mTuQvzM94p-mdHp7tp2vOFgWFVEsst/view?usp=sharing  
**Live Link** (No longer active) - http://167.99.15.101:8000/review_mining/home

**Reviews**, might it be from peers or from the internet, is the first thing that a person looks for while making a choice between a plethora of places. Reviews are also helpful when you consider the organizational facade of businesses, because these reviews gives the management team a chance to look back, evaluate themselves and improve their services according to the valuable feedback from such reviews. There are too many websites where a person can look for reviews of places. But, it is equally important nowadays to get the feel of how a place is perceived on social media. This report is about our effort to do exactly the same by finding reviews about a particular location from Twitter and as an extended effort, we also recommend places surrounding the searched place having the most positive reviews on Google.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


The project is based on Python 3. Project uses some concepts which are avaialble after Python 3.2 so any version of Python after 3.2 can be used.
Setup pip before trying the installation given below.

Django
Installation - 

```pip install Django```  

After Django is installed, go to the root folder (containing manage.py file) and run cmd command - 

```python manage.py runserver```

The application will now be running at localhost:8000/review_mining/    

Google Places Python API
Installation - 

```pip install python-google-places```

After installation is finished, you will have to follow the steps given here - 
[https://developers.google.com/places/web-service/get-api-key](https://developers.google.com/places/web-service/get-api-key) to get the keys required for Google Places API.  

Twitter Python API
Installation - 

```pip install twitter```

After installation is finished, you will have to create a new application here and get access keys from Twitter to be able to query Twitter for tweets.   
  
TextBlob
Installation - 

```pip install textblob```

TextBlob is used for sentiment analysis.

Microsoft Azure TextAnaltyics API
Though this API is not used in the final iteration of the project, here is the description if this needs to be used. 
You should follow some instructions from here :- 
[https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/)

Spacy (NLP Library)
This is not used in the final iteration of the project, here is the link from where you can download Spacy :- 
[https://spacy.io/](https://spacy.io/)


## Tech-Stack
### Languages
**BackEnd** - Python, JavaScript  
**FrontEnd** - JavaScript, HTML, CSS  
**NLP** - Python

### APIs
Microsoft Azure TextAnalytics API, Google Places API, Google Maps API, Twitter API

### Libraries
Python Standard Libraries, TextBlob, python-google-places, python-twitter, Spacy

### Frameworks
**BackEnd/FrontEnd** - Django  
**FrontEnd** - BootStrapJS, JQuery, RateYoJS  
**BackEnd** - Python, Django

## Sentiment Analysis Testing
Microsoft API tested on only 2000 rows because it has a monthly limit of 5000 requests and a limit of 1000 rows at a time.
Google API had the same limit, I like Microsoft, chose Microsoft. 
We are choosing the TextBlob library for sentiment analytics because of the cap limit of Microsoft and Google Analytics libraries. Also, tweets needed to be changed to a specific JSON structure for Microsoft TextAnalytics API to analyse sentiments which cost an unnecessary overhead.  
Also, results of TextBlob and Microsoft Azure TextAnalytics is "almost" similar. Thus, these above details made us tilt towards using TextBlob.

## TextBlob Sentiment Analysis Results
    [6918 rows]
    Accuracy 0.867236195432
    Precision 0.894869638352
## Microsoft TextAnalytics API
    [2000 rows]
    Accuracy 0.89863014257
    Precision 0.907563210781

## NLP Algorithm and Testing
The project was tested on 3 different NLP algorithms and in the end the simplest one was used. The three different algorithms used were:  
1) Named Entity Recognition (N.E.R)  
2) Fuzzy word matching  
3) Regex Matching   
For named entity recognition, a new model was trained using the tweet obtained by querying the Twitter API. The reason N.E.R was not used was because it was still missing many tweets because of the lack of structure in tweets and it was incredibly slow.  
As for regex matching, it was giving performance but it was including tweets which did not involve the exact keyword we were looking for thus including extra tweets.  
So finally, Fuzzy word matching was used. Its performance was not as great as regex matching, but better than N.E.R and unlike regex matching, this algorithm did not include more tweets than needed. 

