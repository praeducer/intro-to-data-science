import sys
import json
import re
import pprint

# populate data structures

def twitterStreamToList(file_name):
    def addTweetDictToList(tweet_list, tweet_line):
        tweet_list.append(json.loads(tweet_line))
        return tweet_list
    return reduce(addTweetDictToList, open(file_name).readlines(), [])

def sentFileToDict(file_name):
    def addSentValToDict(sent_dict, file_line):
        term, score = file_line.split("\t")
        term = cleanString(term)
        score = int(score)
        sent_dict[term] = score
        return sent_dict
    return reduce(addSentValToDict, open(file_name).readlines(), {})

# helper functions

def cleanString(dirty_string):
    clean_string = ""
    # replace all whitespace with a space character
    clean_string = re.sub(r'[ \t\r\n\f]', ' ', dirty_string)
    # Allow only alpha-numeric chars and whitespace char
    clean_string = re.sub(r'[^A-Za-z0-9 ]', '', clean_string)
    clean_string = clean_string.lower()
    return clean_string.strip()

# anlaysis

def analyzeTweets(tweet_list, sent_dict):
    return map(lambda tweet: analyzeText(cleanString(tweet.get('text') or ''), sent_dict), tweet_list)

# Note: Does not handle multi-term phrases from sent_dict (which includes not counting sub-terms twice)
def analyzeText(text, sent_dict):
    def accumSent(sent, term):
        if sent_dict.get(term):
            sent += sent_dict[term]
        return sent
    return reduce(accumSent, text.split(), 0)

# geo-location
# could user user->geo_enabled plus coordinates or just location property of tweet
# making strong assumption on format of user defined location e.g. "<city>, <state> [, <country>]"
def getAllTweetLocations(tweet_list, states_dict):

    def getLocation(tweet):
        user = tweet.get('user') or json.loads('{}')

        def getState(loc):
            loc_split = loc.split(',')
            state = ''
            if len(loc_split) >= 2:
                maybe_state = cleanString(loc_split[1])
                # TODO: Consider using two state_dicts to exploit indexing
                for state_abbr, state_full in states_dict.iteritems():
                    if maybe_state == state_full.lower() or maybe_state == state_abbr.lower():
                        state = state_abbr
            return state
        return getState(user.get('location') or '')
    return map(lambda tweet: getLocation(tweet), tweet_list)

def mapAvgSentToState(tweet_list, sent_dict, states_dict):
    state_sents = zip(getAllTweetLocations(tweet_list, states_dict), analyzeTweets(tweet_list, sent_dict))
    def countStateSent(aggr_state_sents, state_sent):
        state, sent = state_sent
        total, count = aggr_state_sents.get(state) or (0, 0)
        aggr_state_sents[state] = (total + sent, count + 1)
        return aggr_state_sents
    aggr_state_sents = reduce(countStateSent, state_sents, {})
    return map(lambda (state, (total, count)): (state, (float(total) / float(count))), aggr_state_sents.iteritems())

def printHappiestState(state_avg_sents):
    print max(state_avg_sents, key=lambda (state, sent): sent)[0]

if __name__ == '__main__':
    sent_file_name = sys.argv[1]
    tweet_file_name = sys.argv[2]
    sent_dict = sentFileToDict(sent_file_name)
    tweet_list = twitterStreamToList(tweet_file_name)
    test_text_list = ([
                      "",
                      "Le escribi, espero que me entienda..",
                      "asshole",
                      "attacking benefits",
                      "can't stand",
                      "What a dickhead!",
                      "This shit does not work!",
                      "short-sighted",
                      "That son-of-a-bitch! That's some kind of prblm!",
                      "What a vibrant, wonderful, beautiful, couple of kittens."
                      ])

    test_tweet_list = ([
                       {
                           "text": "asshole",
                           "user": {
                               "location": "Charlotte, North Carolina"
                               }
                       },
                       {
                           "text": "attacking benefits",
                           "user": {
                               "location": "Augusta, Georgia"
                               }
                       },
                       {
                           "text": "What a vibrant, wonderful, beautiful, couple of kittens.",
                           "user": {
                               "location": "Charlotte, NC"
                               }
                       },
                       {
                           "text": "What a vibrant, wonderful, beautiful, couple of kittens.",
                           "user": {
                               "location": "Augusta, GA"
                               }
                       }
                       ])

    states_dict = {
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

    #test_state_avg_sents = mapAvgSentToState(test_tweet_list, sent_dict, states_dict)
    state_avg_sents = mapAvgSentToState(tweet_list, sent_dict, states_dict)

    #print pprint.pprint(twitterStreamToList(tweet_file_name))
    #print pprint.pprint(map(lambda text: analyzeText(cleanString(text), sent_dict), test_text_list))
    #print pprint.pprint(analyzeTweets(tweet_list, sent_dict))
    #print pprint.pprint(getAllTweetLocations(tweet_list, states_dict))
    #print pprint.pprint(analyzeTweets(test_tweet_list, sent_dict))
    #print pprint.pprint(getAllTweetLocations(test_tweet_list, states_dict))
    #printHappiestState(test_state_avg_sents)
    printHappiestState(state_avg_sents)
