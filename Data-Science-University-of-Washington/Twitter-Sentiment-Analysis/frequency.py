import sys
import json
from collections import defaultdict
import re


scores = {} # initialize an empty dictionary
statuses = []

texts = []
freq = defaultdict(float)
termsums = [0]



def get_sent(tweet_file):
    for line in tweet_file:
        try:
            statuses.append(json.loads(line))
        except:
            pass

    for dict in statuses:
        
        if (u"text" in dict.keys()):
            texts.append(dict['text'])

    for item in texts:
        words = []
        words = item.split()
        tweet = []
        
        for string in words:
        	
			tweet.append(re.sub("[^a-zA-Z]+", "", string).lower())

        for string in tweet:

                termsums[0] += 1
                freq[string] += 1

	for item in freq:
		freq[item] = freq[item]/float(termsums[0])

	print freq



def main():
    tweet_file = open("test.txt")
    get_sent(tweet_file)
    print termsums[0]

if __name__ == '__main__':
    main()
