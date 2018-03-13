# Twitter Review Mining
**Reviews**, might it be from peers or from the internet, is the first thing that a person looks for while making a choice between a plethora of places. Reviews are also helpful when you consider the organizational facade of businesses, because these reviews gives the management team a chance to look back, evaluate themselves and improve their services according to the valuable feedback from such reviews. There are too many websites where a person can look for reviews of places. But, it is equally important nowadays to get the feel of how a place is perceived on social media. This report is about our effort to do exactly the same by finding reviews about a particular location from Twitter and as an extended effort, we also recommend places surrounding the searched place having the most positive reviews on Google.

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
The project was tested on 3 different NLP algorithms and in the end the simplest one was used. The three different algorithms used were:< br />
1) Named Entity Recognition (N.E.R)< br />
2) Triword Indexing< br />
3) Regex Matching < br />

