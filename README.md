# youtube-comment-spam-detector

##Setup:
1) Download the training data set csv file from this URL: http://mlg.ucd.ie/yt/

2) Save the downloaded csv file in `youtube-spam-detector/data_set` directory as `huge.csv`

3) Now go to project root `youtube-spam-detector/` and execute the `main.py` script with URL of any YouTube video
   `python main.py "https://www.youtube.com/watch?v=sHvB5VPokg8"`
   
4) Project will execute Naive Bayes algorithm and open the result HTML file in default browser
   
###Output:
The output is a HTML file which classifies each comment into `spam` or `ham` category. 


----------------------------------------------------------------------
###Classes

####YoutubeCommentsDataFetcher
takes a url and creates a json file of comments on that url.

####TrainingDataProvider
reads data set .csv files and creates separate .txt files for ham and spam

####NaiveBayes
implementation of Naive Bayes algorithm using nltk

####main.py
starting point
