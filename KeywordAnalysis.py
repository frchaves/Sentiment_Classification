#!/usr/bin/env python
#Keyword-based Association Analysis
#run python3

from bs4 import BeautifulSoup
from textblob import TextBlob
import requests
import csv
import pandas as pd

url_test= "https://www.metacritic.com/game/playstation-4/star-wars-jedi-fallen-order/user-reviews"


######## Constructs of D&M IS Success Model #################

#Information Quality
items_IQ =[' graphics ', " controls ", " design ", " visual ", " colorful ", " beautiful ", " pretty ", " effect ", " slowdown ", " 4k ", " color ", " vibrant ", " detail ",
                                      " realism ", " hdr ", " ultra ", " high ", " medium ", " light ", " attention "]

#System Quality
items_SQ = [" lag ", " delay " ,  " performance " ,  " broken " ,  " wonky " ,  " 30 fps " ,  " 60 fps " ,  " framerate " ,  " frame " ,
                                    " stable " ,   " slow " ,  " animation " ,  " peak " ,  " impossible " ,   " amazing " ,  " sheer " ]
#Service Quality
items_SERVQ =[" customer support ",  " developer " ,  " studio " ,  " polish " ,  " figure out " ,  " fan " ,  " dedicated server " ,  " server " ,  " opponent " ,
                                     " free content " ,  " exclusive content " ,  " game pass " ,  " gamepass " ,  " psn " ,  " whole " ,  " system " ]
#Use
items_USE = [ " hours per week " ,  " game hours " , "  h  " ,  " longevity " ,  " hour " ,  " minute " ,  " addictive " ,  " repetitive " ,  " time " ,
                                   " bed " ,  " mins " ,  " quick " ,  " pun " ,  " week " ,  " day " ,  " hr " ,  " routine " ,  " addict "]
#User Satisfaction
items_USAT= [ " like " ,  " hate " ,  " bad " ,  " good " ,  " solid " ,  " fun " ,  " enjoyable " ,  " quality " ,  " inexcusable " ,  " awful " ,  " horrible " ,  " dated " ,  " perfect " ,
                                   " disappoint " ,  " outrageous " ,   " unapologetically " ,  " best " ,  " trash " ,  " mediocre " ,  " great " ,  " awesome " ,  " nonsense " ,  " cool " ,  " disaster " ,
                                   " okay " ,  " excellent " ,  " poor " ,  " entertain " ,  " flaw " ,  " forget " ,  " masterpiece " ,  " unfortunately " ,  " mess " ,  " mixed " ,  " tedium " ,
                                   " frustation " ,  " damn " ,  " problem " ,  " tedious " ,  " lazy " ,  " weak " ,  " slight " ,  " mindless " ,  " dull " ,  " tragic " ,  " emphasis " ,  " headache " ,
                                   " suck " ,  " crap " ,  " mind " ,  " hell " ,  " troll " ,  " * " ,   " attractive " ,  " bizarre " ]
# Net Benefits
items_NETB = [ " successful " , " solid game " ,  " improvement " ,  " minimum " ,  " standards " , " functional " ,  " success " ,  " all " ,  " bare " ,
                                   " good game " ,  " worst game " ,  " memorable " ,  " rating " ,  " above " ,  " dull " ,  " taste "]


#All Constructs
constructs_DM = {
    "items_IQ": items_IQ,
    "items_SQ": items_SQ,
    "items_SERVQ": items_SERVQ,
    "items_USE": items_USE,
    "items_USAT": items_USAT,
    "items_NETB": items_NETB,
}


# Counters for all constructs
constructs_dict_count = {
    "items_IQ": 0,
    "items_SQ": 0,
    "items_SERVQ": 0,
    "items_USE": 0,
    "items_USAT": 0,
    "items_NETB": 0,
}


# Influence from constructs
constructs_influence = {
    "items_IQ": 0,
    "items_SQ": 0,
    "items_SERVQ": 0,
    "items_USE": 0,
    "items_USAT": 0,
    "items_NETB": 0,
}


#Webscraper
#A webscraper to retrieve Metacritic's comments

def scraper (url):
    session = requests.Session()
    res = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, "html.parser")
    comments = soup.select(".review_body")
    comments_text = [comment.text for comment in comments]
    comments_text = (comments_text[1:])
    return comments_text

#Checks how many times words appear on a sentence
def check(sentence, words):
    res = []
    for word in words:
        if (word in sentence):
            res.append(True)

    return res


#Finds the most important Construct (where words of items appear the most)
def construct_analysis(comment):

    for items in constructs_DM:
        check_obj = check(comment,constructs_DM[items])
        constructs_dict_count[items] += len(check_obj)

    return constructs_dict_count

#Sentiment analysis function - Construct with most influence
def sentiment_classif (sentence):

    target_sentence = TextBlob(sentence)

    for items in constructs_DM:
        check_obj = check(sentence,constructs_DM[items])
        if(len(check_obj) == 0):
            sentiment = target_sentence.sentiment.polarity
            constructs_influence[items] += sentiment

    return constructs_influence


#Main

sentences = []
all_sentences =[]
most_constructs = {}
overall_influence_constructs = {}

#All comments
comments = scraper(url_test)

for comment in comments:
    comment_text = TextBlob(comment)
    sentences = comment_text.sentences
    #Turn sentences into string type
    for phrase in sentences:
        all_sentences.append(str(phrase))

for sentence in all_sentences:
    most_constructs = construct_analysis(sentence)
    overall_influence_constructs = sentiment_classif(sentence)

print(most_constructs)
print(overall_influence_constructs)

data = most_constructs, overall_influence_constructs

df = pd.DataFrame(data)

print(df)

#write to a CSV
df.to_csv("keyword_sentiment_analysis.csv")

