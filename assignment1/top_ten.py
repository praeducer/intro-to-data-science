import sys
import json
import re
import pprint

def twitterStreamToList(file_name):
    def addTweetDictToList(tweet_list, tweet_line):
        tweet_list.append(json.loads(tweet_line))
        return tweet_list
    return reduce(addTweetDictToList, open(file_name).readlines(), [])

def createHashtagCountsDict(tweet_list):
    def countHashtags(hashtag_counts, tweet_json):
        hashtags_entities = tweet_json.get("entities") or json.loads('{}')
        hashtag_list = hashtags_entities.get("hashtags") or [json.loads('{}')]
        for hashtag in hashtag_list:
            text = hashtag.get("text") or ''
            text = text.encode('utf-8')
            text = cleanString(text)
            if hashtag_counts.get(text):
                hashtag_counts[text] += 1
            else:
                hashtag_counts[text] = 1
        return hashtag_counts
    return reduce(countHashtags, tweet_list, {})

def printTopHashtags(hashtag_counts_dict, max_to_print):
    hashtag_counts_dict.pop('', None)
    sorted_hashtags = sorted(hashtag_counts_dict, key=hashtag_counts_dict.__getitem__, reverse=True)
    if len(sorted_hashtags) < 10:
        max_to_print = len(sorted_hashtags)
    for x in range(0, max_to_print):
        print str(sorted_hashtags[x]) + ' ' + str(hashtag_counts_dict[sorted_hashtags[x]])

def cleanString(dirty_string):
    clean_string = ""
    # replace all whitespace with a space character
    clean_string = re.sub(r'[ \t\r\n\f]', ' ', dirty_string)
    # Allow only alpha-numeric chars and whitespace char
    clean_string = re.sub(r'[^A-Za-z0-9 ]', '', clean_string)
    clean_string = clean_string.lower()
    return clean_string.strip()

def main():
    tweet_file_name = sys.argv[1]
    tweet_list = twitterStreamToList(tweet_file_name)
    test_tweet_list = ([
                       {
                           "text": "asshole",
                           "user": {
                               "location": "Charlotte, North Carolina"
                               },
                           "entities": {
                               "hashtags": [{
                                   "text": "tag1",
                                   "indices": [11, 21]
                               }]
                           }
                       },
                       {
                           "text": "attacking benefits",
                           "user": {
                               "location": "Augusta, Georgia"
                               },
                           "entities": {
                               "hashtags": [
                                   {
                                       "text": "tag1",
                                       "indices": [11, 21]
                                   },
                                   {
                                       "text": "tag1",
                                       "indices": [11, 21]
                                   }]
                           }
                       },
                       {
                           "text": "What a vibrant, wonderful, beautiful, couple of kittens.",
                           "user": {
                               "location": "Charlotte, NC"
                               },
                           "entities": {
                               "hashtags": [{
                                   "text": "tag2",
                                   "indices": [11, 21]
                               }]
                           }
                       },
                       {
                           "text": "What a vibrant, wonderful, beautiful, couple of kittens.",
                           "user": {
                               "location": "Augusta, GA"
                               },
                           "entities": {
                               "hashtags": [{
                                   "text": "tag3",
                                   "indices": [11, 21]
                               }]
                           }
                       },
                       {
                           "text": "What a vibrant, wonderful, beautiful, couple of kittens.",
                           "user": {
                               "location": "Augusta, GA"
                               },
                           "entities": {
                               "hashtags": []
                           }
                       }
                       ])

    hashtag_counts_dict = createHashtagCountsDict(tweet_list)
    printTopHashtags(hashtag_counts_dict, 10)

if __name__ == '__main__':
    main()
