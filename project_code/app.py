from flask import Flask, render_template, redirect, url_for, session, request, flash, logging, send_from_directory
import tweepy
import json
import os
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from tkinter import *
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EmotionOptions
app = Flask(__name__)

consumer_key = "08LUUM5dzmMboZLWUBSuacq0h"
consumer_secret = "p32ioyxLBWIlVbYVoGptG8IpgSYKjIDe67A3XavhqdGCYOZWY6"
access_key = "745987644748763139-oTRYAPlxe6z2zDZSvydVtu5zClCHHMn"
access_secret = "IPexUopP4rKuxvkcygoBM3zsOv4vLor0P3lgZoRCwEBfx"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/searchTweets', methods = ['GET', 'POST'])
def searchTweets():
    if request.method == "POST" :
        username = request.form['username']
        session['username'] = username
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        number_of_tweets=5
        tweets = api.user_timeline(screen_name=username)
        tmp=[]
        tmp1=[]
        tweets_for_csv = [tweet.text for tweet in tweets]
        for j in tweets_for_csv:
            tmp.append(j)
        session['tweets'] = tmp
        natural_language_understanding = NaturalLanguageUnderstandingV1(
          username='1ae30c3f-9586-41a7-a104-97a57422662e',
          password='l7WmYMFXSewn',
          version='2018-03-16')

        response = natural_language_understanding.analyze(
            text= str(tmp),
            features=Features(
            emotion=EmotionOptions())).get_result()
        m = response["emotion"]
        n = m["document"]
        r = n["emotion"]
        emotns = list()
        d = dict()
        session['analysis'] = response
        emotns.append(r["sadness"])
        emotns.append(r["joy"])
        emotns.append(r["fear"])
        emotns.append(r["disgust"])
        emotns.append(r["anger"])
        d[0] = 'Sadness'
        d[1] = 'Joy'
        d[2] = 'Fear'
        d[3] = 'Disgust'
        d[4] = 'Anger'
        maxm = max(emotns)
        pos = (emotns.index(maxm))
        return render_template('tweets.html', username = username, persistent = d[pos])
    return redirect('/')

@app.route('/showTweets', methods = ['GET', 'POST'])
def showTweets():
    return render_template('showTweets.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)
