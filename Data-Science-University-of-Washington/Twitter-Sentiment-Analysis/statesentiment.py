import sys
import json
from collections import defaultdict
import re

scores = {} # initialize an empty dictionary
states = {
    'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

tweet_by_state = defaultdict(list)
state_verdict = {}

def get_state(tweet_file): 

    statuses = []
    
    for line in tweet_file:

        try:
            statuses.append(json.loads(line))
        except:
            pass

    for dict in statuses:
        if ('place' in dict.keys()):
            if (dict['place']['place_type'] == "admin"):
                state_name = dict['place']['name']
    
            elif (dict['place']['place_type'] == "city"):
                full = dict['place']['full_name']
                abb = full[len(full)-2: len(full)]
                if (abb in states.keys()):
                    state_name = states[abb]
                else:
                    state_name = ""
        
            else:
                        state_name = ""

            if (u"text" in dict.keys()):
                tweet_by_state[state_name].append(dict['text'])




def get_sent(sent_file, tweet_by_state):
    verdict = []
    
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for keys in tweet_by_state:
        verdict = defaultdict (list)
        tweet = []
        words = []
        for item in tweet_by_state[keys]:
        
            words = item.split()
            sum = 0
        
            for char in words:
            
                tweet.append(re.sub("[^a-zA-Z]+", "", char).lower())


            for word in tweet:
        
                if (word.encode('utf8') in scores.keys()):
                    sum = scores[word] + sum

            verdict[keys].append(sum)

        total = 0
        for keys in verdict:
            for ints in verdict[keys]:
                total = total + ints
                ave = total / len(verdict[keys])
                state_verdict[keys] = ave







def main():
    sent_file = open("AFINN-111.txt")
    tweet_file = open("q5.txt")
    get_state(tweet_file)
    get_sent(sent_file, tweet_by_state)
    sorted_list = sorted(state_verdict, key = state_verdict.get, reverse = True)[:10]
    counter = 0
    for item in sorted_list:
        counter += 1;
        print ("Ranking: " + str(counter) + " State: " + item + " Sentiment: " + str(state_verdict[item]))


if __name__ == '__main__':
    main()


