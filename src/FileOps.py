'''
Created on Sep 13, 2013

@author: rajath
'''

import xlrd

abbr_dict = {}
stopwords_list = []

# Read tweets and sentiments from excel file. Based on training data or test data excel file,
# accordingly columns are selected
def readExcelFile(filename, candidate, category):
    # Open excel workbook
    try:
        wb = xlrd.open_workbook(filename)
    except:
        print 'FILE NOT FOUND!!'
    
    original_tweets = []

    # Select worksheet by candidate name    
    sheet = wb.sheet_by_name(candidate)
    no_of_rows = sheet.nrows

    # The excel file containing training tweets and the one containing test tweets is
    # slightly different from each other. Hence we need separate for loops.
    if category == 'train':
        for rownum in range(2, no_of_rows):
            try:
                tweet = ''.join(sheet.cell(rownum, 3).value).encode('utf-8').strip()
                sentiment = sheet.cell(rownum, 6).value
            except:
                print "Some error occurred. RowNum: ", ''.join(sheet.cell(rownum, 3).value)
            
            if sentiment not in (1.0, -1.0, 2.0, 0.0):
                sentiment = 0.0
            
            # Capture the tweet and sentiment as a tuple and store it in a list
            tweet_tuple = tweet, sentiment
            original_tweets.append(tweet_tuple)
    else:
        if candidate == 'Obama':
            for rownum in range(no_of_rows):
                tweet = ''.join(sheet.cell(rownum, 0).value).encode('utf-8').strip()
                sentiment = sheet.cell(rownum, 4).value
                
                tweet_tuple = tweet, sentiment
                original_tweets.append(tweet_tuple)
        else:
            for rownum in range(2, no_of_rows):
                tweet = ''.join(sheet.cell(rownum, 3).value).encode('utf-8').strip()
                sentiment = sheet.cell(rownum, 7).value
                
                tweet_tuple = tweet, sentiment
                original_tweets.append(tweet_tuple)
    
    return original_tweets

# Read a flat file containing some abbreviations and their expansions in pipe separated format
# Use these abbreviations to replace text in the tweets as part of Preprocessing
def readAbbrFile(abbrFile):
    global abbr_dict
    
    f = open(abbrFile)
    lines = f.readlines()
    f.close()
    for i in lines:
        tmp = i.split('|')
        abbr_dict[tmp[0]] = tmp[1]

    return abbr_dict

# Read stopwords file to get the list of stopwords to remove them from tweets
def readStopwordsFile(stopwordsFile):
    global stopword_list
    
    with open(stopwordsFile) as f:
        lines = f.readlines()
    
    for word in lines:
        stopwords_list.append(word.strip())
    
    return list(set(stopwords_list))
