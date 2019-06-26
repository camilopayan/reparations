#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sqlite3
import requests

def clean_wikipedia(text):
    soup = BeautifulSoup(text, 'html.parser')
    article = soup.find(id="mw-content-text")

    content = article.find_all('p')
    save = ""

    for p in content:
        save = save + ' ' + p.get_text()

    return save

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

result = requests.get("https://en.wikipedia.org/wiki/Reparations_for_slavery")
cur.execute("INSERT INTO wikipedia_pages (is_rep, article) VALUES (?, ?)", (True, clean_wikipedia(result.text)))

for x in range(1000):
    result = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    cur.execute(
        "INSERT INTO wikipedia_pages (is_rep, article) VALUES (?, ?)",
        (False, clean_wikipedia(result.text))
    )

con.commit()
cur.close()
con.close()
