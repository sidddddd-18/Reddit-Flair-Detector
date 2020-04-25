import praw
import pandas as pd
import pickle
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import lxml
from flask import Flask, render_template,request,flash
import json

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
STOPWORDS=set(stopwords.words('english'))
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

def string_form(value):
    return str(value)

def clean_text(text):
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

app=Flask(__name__)
app.secret_key='yippi k yay'

@app.route("/", methods=['GET', 'POST'])
def home():
	reddit=praw.Reddit(client_id='Qq1MxtQ9YVNXgA', \
                     client_secret='hg00d83IEYWEAAT0RdFzm50zm5E', \
                     user_agent='testing', \
                     username='mic_testing123', \
                     password='Cookies')

	if request.method == "POST":
		link=request.form["URL"]
		try:
				sub=reddit.submission(url=str(link))
		except:
			flash("Url not valid")
			return render_template("index.html")
		if str(sub.subreddit)!="india":
			flash("Post does not belong to r/india")
			return render_template("index.html")
		result=predict(sub)	

		flash(result)
		return render_template("index.html")
	return render_template("index.html")

@app.route('/automated_testing',methods=['POST'])
def automated_testing():
	reddit=praw.Reddit(client_id='Qq1MxtQ9YVNXgA', \
                     client_secret='hg00d83IEYWEAAT0RdFzm50zm5E', \
                     user_agent='testing', \
                     username='mic_testing123', \
                     password='Cookies')
	file=request.files['upload_file']
	links=file.read().decode('utf-8').split('\n')
	results={}
	for i in links:
		sub=reddit.submission(url=str(i))
		result=predict(sub)
		results[i]=result
	return json.dumps(results)



def predict(sub):
	posts=[]
	title=sub.title
	url=sub.url
	body=sub.selftext
	sub.comments.replace_more(limit=0)
	st=''
	for c in sub.comments.list():
		count=0
		if count<=30:
			st=st+c.body+' '
			count=+1
		else:
			break
	comments=st
	posts.append([title,url,body,comments])
	data=pd.DataFrame(posts,columns=['title','url','body','comments'])
	title=sub.title
	url=sub.url
	body=sub.selftext
	sub.comments.replace_more(limit=0)
	st=''
	for c in sub.comments.list():
		count=0
		if count<=30:
			st=st+c.body+' '
			count=+1
		else:
			break
	comments=st
	posts.append([title,url,body,comments])
	data=pd.DataFrame(posts,columns=['title','url','body','comments'])
	data["title"]=data["title"].apply(string_form)
	data["body"]=data["body"].apply(string_form)
	data["comments"]=data["comments"].apply(string_form)
	data["title"]=data["title"].apply(clean_text)
	data["body"]=data["body"].apply(clean_text)
	data["comments"]=data["comments"].apply(clean_text)

	combination=data["comments"]+data["title"]+data["url"]+data["body"]


	loaded_model=pickle.load(open("model/SVM_ctbu.sav",'rb'))
	predicted_flair=loaded_model.predict(combination)
	result=str(predicted_flair)	
	return result[2:(len(result)//2)-1]




if __name__ == '__main__':
	app.run()    