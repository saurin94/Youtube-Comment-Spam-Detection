import random
import os.path
import sys
import urllib2
import webbrowser
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from training_data_set.training_data_provider import TrainingDataProvider
from naive_bayes.naive_bayes_impl import NaiveBayes
from data_fetching.data_fetcher import YoutubeCommentsDataFetcher
from bs4 import BeautifulSoup
from nltk.corpus import wordnet


def run_spam_detection(url):
    print "[run_spam_detection] Running spam detection on : " + url
    bae = NaiveBayes()
    provider = TrainingDataProvider()
    fetcher = YoutubeCommentsDataFetcher(url)
    all_comments = []
    spam_comments = provider.get_spam_comments()
    ham_comments = provider.get_ham_comments()
    all_comments = [(comment, "spam") for comment in spam_comments]
    all_comments += [(comment, "ham") for comment in ham_comments]
    all_comments = all_comments[:len(all_comments) / 80]
    random.shuffle(all_comments)  # 6433427
    print "Corpus size: " + str(len(all_comments))

    # extract the features
    all_features = [(bae.get_features(comment, ''), label) for (comment, label) in all_comments]
    print('Collected ' + str(len(all_features)) + ' feature sets')

    # train the classifier
    train_set, test_set, classifier = bae.train(all_features, 0.75)

    # evaluate its performance
    bae.evaluate(train_set, test_set, classifier)
    comments_from_youtube = fetcher.get_comments()
    create_and_open_result_html_file(comments_from_youtube, classifier, bae, url)


def create_and_open_result_html_file(comments_from_youtube, classifier, bae, video_url):
    soup = BeautifulSoup(urllib2.urlopen(video_url), "lxml")
    get_title = soup.find('span', attrs={'id': 'eow-title', 'class': 'watch-title'})
    get_tags = soup.find('meta', attrs={'name': 'keywords', 'content': True})
    get_description = soup.find('p', attrs={'id': 'eow-description'})
    get_category = soup.find('ul', attrs={'class': 'content watch-info-tag-list'})
    category = get_category.getText().encode('utf-8')
    category = category.split(" ")
    category = category[0]
    relevance_sentence = ""
    relevance_sentence += get_description.getText().encode('utf-8') + " "
    relevance_sentence += get_title['title'].encode('utf-8') + " "
    relevance_sentence += str(get_tags['content'].encode('utf-8'))
    for syn in wordnet.synsets(category):
        for lema in syn.lemmas():
            relevance_sentence += str(lema.name())
            relevance_sentence += " "

    for syn in wordnet.synsets(category):
        for sentence in syn.examples():
            relevance_sentence += str(sentence)
            relevance_sentence += " "
    with open("result.html", "w") as result_file:
        htmlstart = "<!DOCTYPE html><html><head><style>"
        htmlmain = "body{padding: 5px 15px;} table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}"
        htmlcss = "td, th {border: 1px solid #e7e7e7; text-align: left; padding: 8px;} tr:nth-child(even) " \
                  "{background-color: #f4f4f4;} .label-ham{color: green;} .label-spam{color: red;}</style></head><body><table>" \
                  "<tr><th>Comments</th><th>Category</th></tr>"

        result_file.write(htmlstart)
        result_file.write(htmlmain)
        result_file.write(htmlcss)
        title = relevance_sentence

        for cid in comments_from_youtube:
            comment = comments_from_youtube[cid]
            text = comment['text']
            start = text.find("\u")
            text = text[:start]
            text = text.encode("utf-8")
            print "values:",process.extract(text,title)
            ratio = fuzz.ratio(title, text)
            label = classifier.classify(bae.get_features(text, "bow"))
            if label == "spam" and ratio >= 5:
                label = "ham"
            tr = "<tr> " + \
                 "<td>" + text + "</td>" + \
                 "<td class='label-" + label + "'>" + label + "</td>" + \
                 "</tr>"
            result_file.write(tr)
        htmlend = "</table></body></html>"
        result_file.write(htmlend)
        result_file.close()
        result_file_path = 'file://' + os.path.realpath('result.html')
        webbrowser.open(result_file_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Please provide a Youtube video URL."
    else:
        url = sys.argv[1]
        run_spam_detection(url)
