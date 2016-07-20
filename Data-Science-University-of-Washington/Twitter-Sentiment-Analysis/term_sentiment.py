import sys
import json
from collections import defaultdict
import re

scores = {} # initialize an empty dictionary
statuses = []

texts = []
verdict = []
new_scores = defaultdict(list)
output_scores = {}

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
    
        if (u'text' in dict.keys()):
            texts.append(dict['text'])
    
    for item in texts:
        words = []
        words = item.split()
        sum = 0
        tweet = []
        
        for string in words:
            
            tweet.append(re.sub("[^a-zA-Z]+", "", string).lower())

        
        for word in tweet:
            
            if (word.encode('utf8') in scores.keys()):
                sum = scores[word] + sum

        verdict.append(sum)
            
        for word in tweet:

                new_scores[word.encode('utf8')].append(sum)



    for key in new_scores:
        value = new_scores[key]
        sum = 0;
        for ints in value:
            sum = sum + ints
        ave = sum / len(value)
        output_scores[key] = ave




def main():
    sent_file = open("AFINN-111.txt")
    tweet_file = open("output.txt")
    
    get_sent(sent_file, tweet_file)
    print output_scores

if __name__ == '__main__':
    main()


