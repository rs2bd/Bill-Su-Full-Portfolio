import sys
import json
from collections import defaultdict
import re

scores = {} # initialize an empty dictionary
statuses = []

texts = []
verdict = []





def get_sent(sent_file, tweet_file):
    
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        try:
            statuses.append(json.loads(line))
        except:
            pass

    for dict in statuses:
        
        if (u"text" in dict.keys()):
            texts.append(dict['text'])

    for item in texts:
        tweet = []
        words = []
        words = item.split()
        sum = 0
    
        for string in words:
            
            tweet.append(re.sub("[^a-zA-Z]+", "", string).lower())

        print tweet
        for word in tweet:
        
            if (word.encode('utf8') in scores.keys()):
                sum = scores[word] + sum
        
        verdict.append(sum)
    print verdict




def main():
    sent_file = open("AFINN-111.txt")
    tweet_file = open("test.txt")
    get_sent(sent_file, tweet_file)



if __name__ == '__main__':
    main()
