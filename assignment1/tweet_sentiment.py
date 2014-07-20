import sys
import json
import re

# FUNCTIONS FOR BUILDING DATA SCTRUCTURES #

# Turn sentiment word to score mapping file into a dictionary.
def createScoresDict(file):
    file.seek(0)
    complete_dict = {}
    for line in file:
        term, score = line.split("\t")
        complete_dict[term] = int(score)
    return complete_dict

def createPhraseScoresDict(complete_dict, phrase_word_count):
    phrase_scores ={}
    for terms in complete_dict.keys():
        phrase_arr = terms.split(" ")
        phrase_str =""
        if len(phrase_arr) == phrase_word_count:
            phrase_str = ' '.join(phrase_arr)
            phrase_scores[phrase_str] = complete_dict[terms]
    return phrase_scores

def createScoresDictList(complete_dict):
    max_phrase_length = countLongestPhrase(complete_dict)
    dict_list = []
    for x in range(0, max_phrase_length):
        phrase_word_count = ( max_phrase_length - x )
        phrase_scores_dict = createPhraseScoresDict(complete_dict, phrase_word_count)
        dict_list.append(phrase_scores_dict)
    return dict_list

def createTweetList(file):
    file.seek(0)
    tweets = []
    for line in file:
        tweet = {}
        tweet = json.loads(line)
        tweets.append(tweet)
    return tweets

def createTextList(tweets):
    texts = []
    for tweet in tweets:
        if 'text' in tweet:
            unicode_string = tweet['text']
            text = unicode_string.encode('utf-8')
            texts.append(text)
        else:
            texts.append("")
    return texts

# FUNCTIONS FOR PROCESSING DATA #

def cleanScoresDict(dirty_dict):
    clean_dict = {}
    for dirty_term in dirty_dict.keys():
        clean_term = cleanString(dirty_term)
        clean_dict[clean_term] = dirty_dict[dirty_term]
    return clean_dict

def cleanTextList(dirty_list):
    clean_list = []
    for dirty_text in dirty_list:
        clean_text = cleanString(dirty_text)
        clean_list.append(clean_text)
    return clean_list

def cleanString(dirty_string):
    clean_string = ""
    # replace all whitespace with a space character
    clean_string = re.sub(r'[ \t\r\n\f]', ' ', dirty_string)
    # Allow only alpha-numeric chars and whitespace char
    clean_string = re.sub(r'[^A-Za-z0-9 ]', '', clean_string)
    clean_string = clean_string.lower()
    return clean_string

# FUNCTIONS FOR ANALYZING DATA #

def simpleAnalyzeTextList(texts, scores):
    results = []
    for text in texts:
        sentiment = 0
        for term in scores.keys():
            if term in text:
                sentiment += int(scores[term])
        results.append(sentiment)
    return results

def analyzeTextList(texts, scores_dict_list):
    results = []
    # loop through the list of the text parsed from json Tweet objects
    for text in texts:
        sentiment = 0
        # loop through the dicts for single words, 2 word phrases, 3 word phrases etc.
        # analyze largest phrases first and remove them from set to prevent subsets of the phrases counting again. maybe do string.replace(phrase, old_text, new_text)
        for scores_dict in scores_dict_list:
            result_tuple = analyzeText(text, scores_dict)
            # updated text with matched phrases replaced with "____"
            text = result_tuple[0]
            sentiment += result_tuple[1]
        results.append(sentiment)
    return results

# returns tuple of the (<sentiment-of-orig-text>, <text-with-matched-phrase-replaced>)
def analyzeText(text, scores_dict):
    sentiment = 0
    updated_text = text
    for scored_phrase in scores_dict.keys():
        score = int(scores_dict[scored_phrase])
        phrase_count = countPhraseInText(scored_phrase, text)
        # sentiment is incremented by the score of the phrase multipled by how many times it occurred
        sentiment += ( score * phrase_count )
        if phrase_count > 0:
            updated_text = updated_text.replace(scored_phrase, "_____")
    result = updated_text, sentiment
    return result

# Check to see if phrase exists in Tweet text. Return how many times.
def countPhraseInText(scored_phrase, text):
    phrase_count = 0
    # split on all whitespace to handle multiple word phrases
    scored_phrase_arr = scored_phrase.split()
    text_arr = text.split()
    for text_arr_index in range(0, ( (len(text_arr) - len(scored_phrase_arr)) + 1 ) ):
        # assume a match at first
        match = True
        for scored_phrase_index in range(0, len(scored_phrase_arr)):
            if match and ( scored_phrase_arr[scored_phrase_index] == text_arr[text_arr_index + scored_phrase_index] ):
                match = True
            else: # This will break the loop since we do not need to continue checking
                match = False
        if match == True: # If it stayed True the entire time then we found a match
            phrase_count += 1
    return phrase_count

def countLongestPhrase(complete_dict):
    longest_phrase_count = 0
    for phrase in complete_dict:
        phrase_arr = phrase.split(" ")
        if len(phrase_arr) > longest_phrase_count:
            longest_phrase_count = len(phrase_arr)
    return longest_phrase_count

# FUNCTIONS FOR DISPLAYING DATA #

def printTweet(tweet):
    print json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ': '))

def printTextList(texts):
    count = 0
    for text in texts:
        count += 1
        print "---\n" + str(count) + "\n---\n\t" + text + "\n\n"

def printResults(results):
    for result in results:
        print result

def printPhraseScoreFile(file):
    file.seek(0)
    num = 0
    for line in file:
        if " " in line:       # if the line contains a space
           print line
           num+=1
    print str(num) + " in total\n"

def printScoresDict(scores_dict):
    for term in scores_dict.keys():
        print term + "\t" + str(scores_dict[term])
    print "\t" + str(len(scores_dict)) + " in total\n"

def printScoresDictList(dict_list):
    for scores_dict in dict_list:
        print "---\nDict of phrases with length " + str(countLongestPhrase(scores_dict)) + "\n---"
        printScoresDict(scores_dict)

def printTextScore(texts, results):
    count = 0
    for text in texts:
            result = results[count]
            count += 1
            print "\n---\n " + str(count) + "\n---\n\t" + '"' + text + '"' + "\n"
            print "\t* score = " + str(result)


def main():
    #"""
    sent_file_name = sys.argv[1]
    tweet_file_name = sys.argv[2]
    sent_file = open(sent_file_name)
    tweet_file = open(tweet_file_name)

    scores_dict = cleanScoresDict(createScoresDict(sent_file))
    scores_dict_list = createScoresDictList(scores_dict)
    tweet_list = createTweetList(tweet_file)
    dirty_text_list = createTextList(tweet_list)
    text_list = cleanTextList(dirty_text_list)

    #simple_result_list = simpleAnalyzeTextList(text_list, scores_dict)
    result_list = analyzeTextList(text_list, scores_dict_list)

    printResults(result_list)

    """
    print '\n' + '-' * 55 + '\n\nHello, Science!\n'

    print '-' * 55 + '\n'
    print 'DATA:\n'

    #word_scores_dict = createPhraseScoresDict(scores_dict, 1)
    #phrase_scores_dict = createPhraseScoresDict(scores_dict, 2)
    #three_phrase_scores_dict = createPhraseScoresDict(scores_dict, 3)

    print "First Tweet's full contents:"
    printTweet(tweet_list[0])
    print "\nText from all Tweets:"
    printTextList(text_list)
    printPhraseScoreFile(sent_file)
    printScoresDict(word_scores_dict)
    printScoresDict(phrase_scores_dict)
    printScoresDictList(scores_dict_list)
    printTextScore(text_list, result_list)


    print '-' * 55 + '\n'
    print 'STATS:\n'

    sent_file.seek(0)
    tweet_file.seek(0)
    print ("Input 1, " + str(sent_file_name) + ", is the sentiment mapping and has\n\t" +
           str(len(sent_file.readlines())) + " lines")
    print( "\ta longest phrase of " +
           str(countLongestPhrase(scores_dict)) + " words")
    print ("Input 2, " + str(tweet_file_name) + ", is the stream of Tweets and has\n\t" +
           str(len(tweet_file.readlines())) + " lines")
    print ("The dict of scores has\n\t" +
           str(len(scores_dict)) + " keys")
    print ("The list of Tweets has\n\t" +
           str(len(tweet_list)) + " items")
    print ("The list of texts has\n\t" +
           str(len(text_list)) + " items")
    print ("The list of results has\n\t" +
           str(len(results_list)) + " items")

    print '-' * 55 + '\n'
    print 'RESULTS OF ANALYSIS:\n'

    printTextScore(text_list, result_list)

    # TESTING
    phrase1 = ("messing up")
    phrase2 = ("fed up")
    phrase3 = ("right direction")
    word1 = ("expands")
    word2 = ("abhor")
    word3 = ("bereaved")
    text = word1 + " " + phrase1 + " " + word1 + " XXXXX YYYYY " + phrase2 + " " + word2 + " XXXXX YYYYY ZZZZZ " + phrase3 + " " + word3 + " X Y Z X Y Z " + phrase1 + " " + word1
    phrase1_count = countPhraseInText(phrase1, text)
    word1_count = countPhraseInText(word1, text)
    #sentiment = analyzeText(text, scores_dict)
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

    test_text_list.append(text)
    test_text_list = cleanTextList(test_text_list)
    test_result_list = analyzeTextList(test_text_list, scores_dict_list)

    print 'phrase1 = "' + phrase1 + '"' + " with a score of " + str(int(scores_dict[phrase1]))
    print 'phrase2 = "' + phrase2 + '"' + " with a score of " + str(int(scores_dict[phrase2]))
    print 'phrase3 = "' + phrase3 + '"' + " with a score of " + str(int(scores_dict[phrase3]))
    print 'word1 = "' + word1 + '"' + " with a score of " + str(int(scores_dict[word1]))
    print 'word2 = "' + word2 + '"' + " with a score of " + str(int(scores_dict[word2]))
    print 'word3 = "' + word3 + '"' + " with a score of " + str(int(scores_dict[word3]))
    print 'text = "' + text + '"'
    print 'phrase1 in text count = "' + str(phrase1_count) + '"'
    print 'word1 in text count = "' + str(word1_count) + '"'
    #print 'sentiment of text = "' + str(sentiment) + '"'

    printTextScore(test_text_list, test_result_list)

    print '\n' + '-' * 55 + '\n'

    #"""

if __name__ == '__main__':
    main()
