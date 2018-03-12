import difflib
#search is the search term
search = "Empire State Building"
#text is the tweet
text = "Empire Building is an excellent Place to be!!!"    
#splitting ans finding the size of tweet and search word
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
	print("Yes")
else: 
	print("No")
print("------------------")
#three = [' '.join([i,j,k]) for i,j,k in zip(words, words[1:], words[2:])]
#print(three)
#print(difflib.get_close_matches('no information available', three, cutoff=0.9))
#Oyutput:
#['n0 inf0rmation available']