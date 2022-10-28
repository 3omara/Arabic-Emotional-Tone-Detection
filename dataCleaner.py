from ast import pattern
import sys
sys.path.append('./Scripts')
sys.path.append('./Files')
sys.path.append('./Datasets')
import os
os.system('pip install nltk')
os.system('pip install openpyxl')
os.system('pip install emot')
from bs4 import BeautifulSoup
import re
import emot
from nltk.corpus import stopwords
import nltk
import json
import requests
import emoji
nltk.download('punkt')
import ArStemmerLib as lib
import pyarabic.araby as araby
from farasa.stemmer import FarasaStemmer
import qalsadi.lemmatizer
from snowballstemmer import stemmer

def remove_diacritics(tweet):
    tweet = araby.strip_diacritics(tweet.strip())
    return tweet

def clean_arabic_text(tweet):
    pattern = '[^ \u0620-\u064A]'
    tweet = re.sub(pattern, "", tweet)
    return tweet.strip()

def remove_eng_and_nums(tweet):
    pattern = '[a-zA-Z0-9\u0660-\u0669]'
    tweet = re.sub(pattern, "", tweet)
    return tweet

def remove_links(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = re.sub(r"http\S+", "", tweet)
    return tweet

def remove_stop_words(tweet):
    f = open("Files/arabicStops.txt", "r", encoding="utf-8")
    ar_stop_words = f.read()
    ar_stop_words = ar_stop_words.split('\n')
    ar_stop_words = set(ar_stop_words)
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    curr = ""
    for word in  re.split("\W+",tweet):
        if word not in ar_stop_words: 
            curr = curr + word +" "
    curr = curr.strip()
    return curr

def stripChar(list_chars):
    strippedList = []
    for character in list_chars:
        strippedList.append(character.strip())
    return(strippedList)

def replace_emojies(tweet):
    f1 = open(u'Files/PositiveEmoji.txt','r',encoding='utf-8-sig')
    PositiveEmoji = list(f1.read().split('\n'))
    f2 = open(u'Files/NegativeEmoji.txt','r',encoding='utf-8-sig')
    NegativeEmoji = list(f2.read().split('\n'))
    emojies = emoji.emoji_list(tweet)
    for emo in emojies:
        if emo["emoji"] in PositiveEmoji:
            tweet = re.sub(emo["emoji"], "ايموشنموجب ", tweet)
        elif emo["emoji"] in NegativeEmoji:
            tweet = re.sub(emo["emoji"], "ايموشنسالب ", tweet)
    
    return tweet

def replace_emoticons(tweet_with_emo):
    f1 = open(u'Files/PositiveEmoji.txt','r',encoding='utf-8-sig')
    PositiveEmoji = list(f1.read().split('\n'))
    f2 = open(u'Files/NegativeEmoji.txt','r',encoding='utf-8-sig')
    NegativeEmoji = list(f2.read().split('\n'))

    PositiveEmojistr = stripChar(PositiveEmoji)
    NegativeEmojistr = stripChar(NegativeEmoji)

    extracted_emot = emot.emot.emoticons(u'%s' %tweet_with_emo)
    extracted_emoji = emot.emot.emoji(u'%s' %tweet_with_emo)
    for emots in extracted_emot:
        if emots['value'] in PositiveEmojistr:
            tweet_with_emo = tweet_with_emo.replace( emots['value'], "ايموشنموجب" )
        elif emots['value'] in NegativeEmojistr:
            tweet_with_emo = tweet_with_emo.replace( emots['value'], "ايموشنسالب" )
            
    for emojis in extracted_emoji:
        if emojis['value'] in PositiveEmojistr:
            tweet_with_emo = tweet_with_emo.replace( emojis['value'], " ايموشنموجب" )
        elif emojis['value'] in NegativeEmojistr:
            tweet_with_emo = tweet_with_emo.replace( emojis['value'], " ايموشنسالب" )
    return(tweet_with_emo)

def remove_amp(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = BeautifulSoup(tweet , "html.parser").get_text()
    return tweet
    
#removing hash without removing the hashtag
def remove_hash(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = re.sub(r"#", "", tweet)
    return tweet
    
#remove under score    
def remove_under_score(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = lambda tweet : re.sub(r"_", " ", tweet)
    return tweet

def remove_longation(tweet):
    for char in ['و', 'ي', 'ا']:
        tweet = re.sub(f"{char}+", char, tweet)
    return tweet

#remove longation
# def remove_longation(text):
#     text = text.strip()
#     text = u"%s" %text
#     p_longation = re.compile(r'(.)\1+')
#     subst = r"\1\1"
#     text = re.sub(p_longation, subst, text)
#     text = text.replace('وو', 'و')
#     text = text.replace('يي', 'ي')
#     text = text.replace('اا', 'ا')
#     return(text)

def replace_punctuation(tweet):
    tweet = re.sub("[?؟]", " استفهام ", tweet)
    tweet = re.sub("!", " استعجاب ", tweet)
    return tweet.strip()

#cleaning the string
def clean_str(text):
    text = text.strip()
    text = u"%s" %text
    search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
    replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']
    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])
    #trim    
    text = text.strip()
    return text
    
#clean seperately
def remove_prt(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = re.sub(r"#prt", " ", tweet)
    return tweet
    
def remove_extrass(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = re.sub(r"\\", " ", tweet)
    return tweet
    
def remove_tag_persons(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = re.sub(r"@\S+", "", tweet)
    return tweet
    
def remove_dots(tweet):
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    tweet = tweet.replace(".", "")
    return tweet

def farasa_stemmer(tweet):                          ##### https://farasa-api.qcri.org/
    stemmer = FarasaStemmer()
    result = stemmer.stem(tweet)
    return result

def qalsadi_lemmatizer(tweet):                      ##### https://pypi.org/project/qalsadi/
    lemmer = qalsadi.lemmatizer.Lemmatizer()
    result = lemmer.lemmatize_text(tweet)
    return " ".join(result)

def snow_ball_stemmer(tweet):                       ##### 
    ar_stemmer = stemmer("arabic")
    result = ar_stemmer.stemWords(tweet.split())
    return " ".join(result)

def stem_docs(tweet):
    stemmer = lib.ArStemmer()
    tweet = tweet.strip()
    tweet = u"%s" %tweet
    curr = ""
    for word in tweet.split():  
        curr = curr + stemmer.stem(word) +" "
    curr = curr.strip()
    return  curr


# def preProcess(df): 
#     df['tweet'] = df.tweet.map(lambda tweet : stem_docs(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_longation(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_stop_words(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_links(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_amp(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_hash(tweet))
#     df["tweet"]= df.tweet.map(lambda tweet : re.sub(r"_", " ", tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : clean_str(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_prt(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_extrass(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_tag_persons(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_dots(tweet))
#     df['tweet'] = df.tweet.map(lambda tweet : remove_eng_and_nums(tweet))