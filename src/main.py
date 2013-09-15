'''
Created on Sep 13, 2013

@author: rajath
'''

import logging
from FileOps import readExcelFile
import Classifier

TRAINING_DATA_FILE = '../data/training-Obama-Romney-tweets.xlsx'
TEST_DATA_FILE = '../data/testing-Obama-Romney-tweets-spring-2013.xlsx'

def word_feats(words):
    return dict([(word, True) for word in words])

if __name__ == '__main__':
    
    # Create an instance of NaiveBayesClassifier
    nbClassifier = Classifier.NBClassifier()
    # TODO: add logging everywhere
    # TODO: add function decorators to capture the time taken  
    # TODO: add multi-threading
    # TODO: add more classifiers (ex. SVM-lite)

    # call file ops to read input file
    training_tweets = readExcelFile(TRAINING_DATA_FILE, 'Obama', 'train') + readExcelFile(TRAINING_DATA_FILE, 'Romney', 'train')
    training_feats = nbClassifier.get_feats(word_feats, training_tweets)
    
    # call get_feats for test tweets
    test_tweets = readExcelFile(TEST_DATA_FILE, 'Obama', 'test') + readExcelFile(TEST_DATA_FILE, 'Romney', 'test')
    test_feats = nbClassifier.get_feats(word_feats, test_tweets)

    # Train the feature sets using Naive Bayes Classifier
    nbClassifier.train(training_feats, test_feats)
    
    # Calculate the accuracy
    nbClassifier.accuracy()

    # Calculate precision, recall and F-score of positive, negative, neutral and mixed sentiment tweets
    nbClassifier.stats()

    # Print the confusion matrix
    nbClassifier.confusion_matrix()
#end