#!/usr/bin/env python3

# https://stevenloria.com/tf-idf/

import json, math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


reparations_file = open("data/wp_reparations_article", "r")
rblob = tb(reparations_file.read())
reparations_file.close()

blobs = [];
articles_file = open("data/wp_articles.json", "r")
articles = json.JSONDecoder().decode(articles_file.read())
articles_file.close()

for t in articles:
    blobs.append(tb(t))

scores = {word: tfidf(word, rblob, blobs) for word in rblob.words}
sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

rep_words_file = open("data/rep_words_file.json", "w")
rep_words_file.write(json.JSONEncoder().encode(sorted_words))
rep_words_file.close()
