# Reddit-Flair-Detector
A Reddit Flair Detector web application that predicts flair of posts from Subreddit r/india. The app is live at https://reddit-flair-detector-sid.herokuapp.com/
#Codebase
This code has been written in python by it's easy to use yet powerful text processing and machine learning modules.
The web app is developed by Flask+HTML+CSS and is hosted on Heroku web server
# Project Execution
1)Open the terminal
2)Clone the repository by entering 
3)Ensure that Python3 and pip are installed
4)Create a virtual environment in the cloned folder by executing
```bash
py -m venv env
```
5)Activate the env virtual environment by the following command:
```bash
.\env\Scripts\activate
```
6)Install dependencies in requirements.txt and execute the following command
```bash
pip install -r requirements.txt
```
7)Enter python shell and execute the following commands:
```bash
import nltk
```
nltk.download('stopwords)
8)Start the application
```bash
py app.py
```
9)Go to your local host server mentioned in the terminal and start predicting!
# Idea and process
## Data extraction
I used the PRAW api to extract data from www.reddit.com/r/india/  and the data is then stored on MongoDB Atlas.
I extracted data from 100 posts for 12 flairs which are Coronavirus,Non-Political,Politics,Science/Technology,
Policy/Economy,Photography,AskIndia,Scheduled,Sports,Food,Business/Finanace,[R]eddiquette.
Initially I extracted data by searching the flair through the api but realised that there were lots of 
post with titles that included names of other flairs thus rigging the search and ruining my data. 
Hence making my extract the data again but now by checking the flair of each and every post individually.
Lastly, I ended with extracting data for 125 posts for each flair and top 30 comments for each post.
My approach can be found in Data_Scrapping.ipynb
##Exploratory Data Analysis
Qualitative analysis of my data included examining the text data particularly for comments,title,url and body.
After examining I found that data quality was poor as it contained bad symbols such as (,[,],/,:,;,),} etc. and had no uniformity 
in words.Apart from this, my data had lots of stopwords (a,the,is,in,of etc.) which could have impacted the accuracy of my 
machine learning models. I also observed that body of many posts only contained NaN which could again reduce the accuracy of 
my model.
Qualitative analysis included plotting mean values of scores and number of comments for a particular flair. This told us that these two features could be used for accurately predicting some particular flairs 
more effectively than the others thus making me consider then as a feature for my model.
##Creating ML models
The dataset is split into 90% train and 10% test data using train-test-split of scikit-learn.
The data is then passed into CountVectorizer and TF-IDF form.
I tested my data on 5 models namely Multinomial Naive Bayes, Logistic Regression, Random Forest, MLP and SVM .
I also tested various combinations of features both individually and combinedsome of which are as follows:
Title
Body
SCore
Author
Number of comments
Comments
Url
Comments+title+url+body
Comments+title+body
Comments+title+url
Comments+title+url+score
#Result
Best accuracy was found for comments+title+url+body for Linear SVM Algorithm
Accuracy:67.33%

**Algorithm** | **Accuracy**
------------ | -------------
Multinomial Naive Bayes | 40.00
Logistic Regression | 64.00
Random Forest | 53.33
Linear SVM | **67.33**
MLP | 54
#Heroku app
https://reddit-flair-detector-sid.herokuapp.com/
Automated Testing can be done at /automated_testing route.

##Resources
