from collections import Counter
from nltk import NaiveBayesClassifier, classify
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
import configurations


class NaiveBayes(object):
    def __init__(self):
        print "Using Naive Bayer classifier."
        self.ALL_SPAM_COMMENTS_FILE = configurations.PROJECT_ROOT + "/data_set/spam.txt"
        self.ALL_HAM_COMMENTS_FILE = configurations.PROJECT_ROOT + "/data_set/ham.txt"
        self.STOP_WORDS_LIST = stopwords.words('english')

    def train(self, features, samples_proportion):
        train_size = int(len(features) * samples_proportion)
        train_set, test_set = features[:train_size], features[train_size:]
        print('Training corpus: ' + str(len(train_set)) + ' comments')
        print('Test corpus: ' + str(len(test_set)) + ' comments')
        # now train the classifier
        classifier = NaiveBayesClassifier.train(train_set)
        return train_set, test_set, classifier

    def evaluate(self, train_set, test_set, classifier):
        print('Correctness on the training set = ' + str(classify.accuracy(classifier, train_set) * 100) + "%")
        print('Correctness on the test set = ' + str(classify.accuracy(classifier, test_set) * 100) + "%")
        classifier.show_most_informative_features(20)

    def get_features(self, text, algorithm):
        # bag of words algorithm
        if algorithm == "bow":
            return self.bag_of_words(text)
        else:
            return {word: True for word in self.preprocess(text) if not word in self.STOP_WORDS_LIST}

    def bag_of_words(self, text):
        words_dict = Counter(self.preprocess(text)).items()
        return {word: word_count for word, word_count in words_dict if not word in self.STOP_WORDS_LIST}

    def preprocess(self, sentence):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(unicode(sentence, errors='ignore'))]