#!/usr/bin/env python3

# https://stevenloria.com/tf-idf/

import sqlite3, math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

con = sqlite3.connect("db.sqlite")
cur = con.cursor()


cur.execute("SELECT * from wikipedia_pages WHERE is_rep = ?", ( int(True), ))
rep = cur.fetchone()
rblob = tb(rep[2])

blobs = [];
for t in cur.execute("SELECT * from wikipedia_pages WHERE is_rep=?", ( int(False), )):
    blobs.append(tb(t[2]))

scores = {word: tfidf(word, rblob, blobs) for word in rblob.words}
sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
for word, score in sorted_words:
    cur.execute("INSERT INTO wp_words (word, score) VALUES (?, ?)", (word, score))

con.commit()
cur.close()
con.close()

