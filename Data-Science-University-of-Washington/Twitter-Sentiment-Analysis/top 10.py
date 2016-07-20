__author__ = 'billsu'

import sys
import json


phrase = {}

def get_top (tweet_file):
    statuses = []

    for line in tweet_file:
        try:
            statuses.append(json.loads(line))
        except:
            pass

    for dict in statuses:

        if (u'entities' in dict.keys()):
            if (dict['entities']['hashtags'] != ""):
                for dict2 in dict['entities']['hashtags']:
                    if (dict2["text"] in phrase.keys()):
                        phrase[dict2["text"]] += 1
                    else:
                        phrase[dict2["text"]] = 1
    print phrase

def main():
    tweet_file = open("output.txt")
    get_top(tweet_file)
    sorted_list = sorted(phrase, key = phrase.get, reverse = True)[:10]
    counter = 0
    for item in sorted_list:
        counter += 1;
        print ("Ranking: " + str(counter) + " Hashtag: " + item + " Count: " + str(phrase[item]))


if __name__ == '__main__':
    main()

