'''
Created on Sep 15, 2013

@author: rajath
'''

from PreprocessData import clean_data
from nltk.classify import NaiveBayesClassifier
from nltk.metrics.confusionmatrix import ConfusionMatrix
import nltk.classify.util
import nltk.metrics
import collections

class NBClassifier:
    actual = None
    classified = None
    ref_list = []
    test_list = []
    classifier = None
    training_feats = None
    test_feats = None

    # Create feature sets of all the tweets
    def get_feats(self, featx, orig_tweets):
        
        posTweets, negTweets, neuTweets, mixTweets = clean_data(orig_tweets,)
        
        posfeats = [(featx(tweets),'pos') for tweets, sent in posTweets]
        negfeats = [(featx(tweets),'neg') for tweets, sent in negTweets]
        neufeats = [(featx(tweets),'neu') for tweets, sent in neuTweets]
        mixfeats = [(featx(tweets),'mix') for tweets, sent in mixTweets]
        
        total_feats = posfeats + negfeats + neufeats + mixfeats

        return total_feats

    # Train the feature sets to produce reference and actual lists
    def train(self, training_feats, test_feats):
        self.classifier = NaiveBayesClassifier.train(training_feats)
        self.training_feats = training_feats
        self.test_feats = test_feats
        
        self.actual = collections.defaultdict(set)
        self.classified = collections.defaultdict(set)
        
        self.ref_list = list()
        self.test_list = list()
        for i, (feats, label) in enumerate(test_feats):
            self.actual[label].add(i)
            self.ref_list.append(label)
            observed = self.classifier.classify(feats)
            self.classified[observed].add(i)
            self.test_list.append(observed)

    # Compute Accuracy
    def accuracy(self):
        print 'ACCURACY:', nltk.classify.util.accuracy(self.classifier, self.test_feats)

    # Compute Precision, Recall and F-score of positive, negative, neutral and mixed sentiment tweets
    def stats(self):
        
        print 'POSITIVE CLASS'
        print 'precision:', nltk.metrics.precision(self.actual['pos'], self.classified['pos'])
        print 'recall:', nltk.metrics.recall(self.actual['pos'], self.classified['pos'])
        print 'F-score:', nltk.metrics.f_measure(self.actual['pos'], self.classified['pos'])
        print
        print 'NEGATIVE CLASS'
        print 'precision:', nltk.metrics.precision(self.actual['neg'], self.classified['neg'])
        print 'recall:', nltk.metrics.recall(self.actual['neg'], self.classified['neg'])
        print 'F-score:', nltk.metrics.f_measure(self.actual['neg'], self.classified['neg'])
        print
        print 'NEUTRAL CLASS'
        print 'precision:', nltk.metrics.precision(self.actual['neu'], self.classified['neu'])
        print 'recall:', nltk.metrics.recall(self.actual['neu'], self.classified['neu'])
        print 'F-score:', nltk.metrics.f_measure(self.actual['neu'], self.classified['neu'])
        print
        print 'MIXED CLASS'
        print 'precision:', nltk.metrics.precision(self.actual['mix'], self.classified['mix'])
        print 'recall:', nltk.metrics.recall(self.actual['mix'], self.classified['mix'])
        print 'F-score:', nltk.metrics.f_measure(self.actual['mix'], self.classified['mix'])

    # Build and print the Confusion Matrix
    def confusion_matrix(self):
        cm = ConfusionMatrix(self.ref_list, self.test_list)
        print cm.pp(sort_by_count=True, show_percents=False, truncate=9)
        print
