import sys
import json
import re

# FUNCTIONS FOR BUILDING DATA STRUCTURES #

# TODO: Update to take into account scores of closest words
# TODO: Account for terms that already exist. Especially if it occurred more than twice. Average for evey occurence?
# TODO: Should really use the results from the full multi-phrase dict analysis
def simpleFindandPrintNewTerms(tweet_file, original_dict):
    text = ""
    result_text = ""
    sentiment = 0
    for line in tweet_file:
        tweet = json.loads(line)
        if 'text' in tweet:
            unicode_string = tweet['text']
            text = unicode_string.encode('utf-8')
        else:
            text = ""
        text = cleanString(text)
        if text != "":
            result_tuple = simpleAnalyzeText(text, original_dict)
            result_text = result_tuple[0]
            sentiment = result_tuple[1]
        else:
            result_text = ""
            sentiment = 0
        new_terms_arr = result_text.split()
        for new_term in new_terms_arr:
            print new_term + " " + str(sentiment)

# Turn sentiment word to score mapping file into a dictionary.
def createScoresDict(scores_file):
    scores_file.seek(0)
    complete_dict = {}
    for line in scores_file:
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

def createTweetList(tweet_file):
    tweet_file.seek(0)
    tweets = []
    for line in tweet_file:
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

# returns tuple of the (<sentiment-of-orig-text>, <text-with-matched-phrase-replaced>)
def simpleAnalyzeText(text, scores_dict):
    sentiment = 0
    updated_text = text
    for scored_phrase in scores_dict.keys():
        if scored_phrase in updated_text:
            sentiment += int(scores_dict[scored_phrase])
        updated_text = updated_text.replace(scored_phrase, "")
    result = updated_text, sentiment
    return result

def analyzeTextList(texts, scores_dict_list):
    results = []
    # loop through the list of the text parsed from json Tweet objects
    for text in texts:
        sentiment = 0
        # loop through the dicts for single words, 2 word phrases, 3 word phrases etc.
        # analyze largest phrases first and remove them from set to prevent subsets of the phrases counting again. maybe do string.replace(phrase, old_text, new_text)
        for scores_dict in scores_dict_list:
            result_tuple = analyzeText(text, scores_dict)
            # updated text with matched phrases replaced with "_____"
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
            # TODO: This is a little too aggressive. replaces phrases and words that are inside other words and phrases.
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

def computeAndPrintTermFrequency(tweet_file):
    text = ""
    term_occurence_dict = {}
    occurence_of_all = 0
    for line in tweet_file:
        tweet = json.loads(line)
        if 'text' in tweet:
            unicode_string = tweet['text']
            text = unicode_string.encode('utf-8')
        else:
            text = ""
        text = cleanString(text)
        text_arr = text.split()
        for term in text_arr:
            occurence_of_all += 1
            if term in term_occurence_dict:
                term_occurence_dict[term] = term_occurence_dict[term] + 1
            else:
                term_occurence_dict[term] = 1
    for term in term_occurence_dict.keys():
        term_frequency = float(term_occurence_dict[term]) / float(occurence_of_all)
        print term + " " + str(term_frequency)


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
        print term + " " + str(scores_dict[term])

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
    tweet_file_name = sys.argv[1]
    tweet_file = open(tweet_file_name)

    computeAndPrintTermFrequency(tweet_file)

if __name__ == '__main__':
    main()
