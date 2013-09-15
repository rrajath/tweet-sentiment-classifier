'''
Created on Sep 13, 2013

@author: rajath
'''
import re
from FileOps import readAbbrFile, readStopwordsFile
from nltk.stem import WordNetLemmatizer as wnl
from nltk.tokenize import word_tokenize
import string

exclude = set(string.punctuation)
stopwordsFile = '../data/stopwords.txt'
abbrFile = '../data/abbr.txt'

stopwords = readStopwordsFile(stopwordsFile)
abbr_dict = readAbbrFile(abbrFile)

def clean_data(original_tweets):
    pos_tweets = []
    neg_tweets = []
    neu_tweets = []
    mix_tweets = []

    for tweet,sentiment in original_tweets:
        if sentiment == 0.0:
            neu_tweets.append((process_tweet(tweet),sentiment))
        elif sentiment == 2.0:
            mix_tweets.append((process_tweet(tweet),sentiment))
        elif sentiment == 1.0:
            pos_tweets.append((process_tweet(tweet),sentiment))
        elif sentiment == -1.0:
            neg_tweets.append((process_tweet(tweet),sentiment))
    return pos_tweets, neg_tweets, neu_tweets, mix_tweets
#end
    
def process_tweet(tweet):
    #Removing URls
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',tweet)
    
    #Replace 2 or more repetitions of a character
    tweet = replaceTwoOrMore(tweet)

    #Removing usernames
    tweet = re.sub('@[^\s]+','',tweet)

    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    #Replace the hex code "\xe2\x80\x99" with single quote
    tweet = re.sub(r'\\xe2\\x80\\x99', "'", tweet)
    
    #Removing <e> and <a> tags
    tweet = re.sub(r'(<e>|</e>|<a>|</a>|\n)', '', tweet)
    
    #Removing apostrophe
#     tweet = tweet.replace("\'s",'')
    
    #Expanding contractions. For example, "can't" will be replaced with "cannot"
#    tweet = RegexReplacer().replace(tweet)

    #Removing punctuation
    tweet = ''.join(ch for ch in tweet if ch not in exclude)
    
    #Removing words that end with digits
    tweet = re.sub(r'\d+','',tweet)
    
    #Removing words that start with a number or a special character
    tweet = re.sub(r"^[^a-zA-Z]+", ' ', tweet)

    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)

    #Replace all words that don't start with a letter, number or an underscore with an empty string
    tweet = re.sub(r'\\[xa-z0-9.*]+', '', tweet)
    
    #Remove trailing spaces and full stops
    tweet = tweet.strip(' .')
    
    #Convert CamelCaseWords to space delimited words
    tweet = convertCamelCase(tweet)
    
    #Convert everything to lower characters
    tweet = tweet.lower()

    #Tokenize the tweet
    tweet = tokenize_tweet(tweet)

    #Replace abbreviations with their corresponding meanings
    tweet = replaceAbbr(tweet)
    
    #Lemmatize the words in tweets
    tweet = wordLemmatizer(tweet)
    
    #Remove stopwords from the tweet
    tweet = removeStopWords(tweet, stopwords)
    
    #Removing duplicates
    tweet = list(set(tweet))

    return tweet
#end

# Removing stopwords
def removeStopWords(tweet, stopwords):
    tmp = []
    for i in tweet:
        if i not in stopwords:
            tmp.append(i)

    return tmp
#end


# This method replaces two or more consecutive letters with the same character to
# something shorter. For example, gooooooood becomes good.
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)
#end

# This method converts camel cased words into space delimited words.
# For example: ThisIsASentence will be changed to This Is A Sentence
def convertCamelCase(word):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",word)
#end

def is_ascii(self, word):
    return all(ord(c) < 128 for c in word)
#end

# This function checks the dictionary containing abbreviations and their meanings as (key,value) pairs
# and replaces the key with the corresponding value
def replaceAbbr(s):
    for word in s:
        if word.lower() in abbr_dict.keys():
            s = [abbr_dict[word.lower()] if word.lower() in abbr_dict.keys() else word for word in s]
    return s
#end

# Tokenize the tweet and split the words
def tokenize_tweet(tweet):
    return word_tokenize(tweet)
#end

# This method lemmatizes each word in a tweet. The method accepts a list, lemmatizes each word
# and returns back the list
def wordLemmatizer(tweet_words):
    return [wnl().lemmatize(word) for word in tweet_words]
#end