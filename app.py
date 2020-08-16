

# Importing the Libraries
import numpy as np
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
import os
import flask
import requests
from Levenshtein import *
# Loading Flask and assigning the model variable
app = Flask(__name__)
CORS(app)
app = flask.Flask(__name__, template_folder='templates')


def news_call_classifier(fact_check):

    url = "https://bing-news-search1.p.rapidapi.com/news/search"
    querystring = {"count": "50", "setLang": "EN", "freshness": "Day","textFormat": "Raw", "safeSearch": "Off", "q": fact_check}

    headers = {
        'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
        'x-rapidapi-key': "1daa73315amsha25dced63e1e976p16fe0djsn4b6547ffa9e5",
        'x-bingapis-sdk': "true"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    response = response.json()

    news_headline = []
    for i in range(len(response['value'])):
        news_headline.append(response['value'][i]['name'])

    print(news_headline)
    prob_list = []
    for news_art in news_headline:
        prob_list.append(ratio(fact_check, news_art))
    # ratio1 = sum(prob_list)/len(prob_list)
    ratio1 = max(prob_list)
    print(ratio1)
    return ratio1*100


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    query_parameters = request.args
    url = query_parameters.get('news')
    url = url.split(sep="%20")
    url = " ".join(url)
    # Passing the news article to the model and returing whether it is Fake or Real
    pred = news_call_classifier(url)
    print(pred)
    temp={}
    temp["result"]=pred

    return jsonify(temp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True, use_reloader=False)
