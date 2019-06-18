#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sqlite3
import requests

con = sqlite3.connect("./db.sqlite")
cur = con.cursor()

result = requests.get("https://en.wikipedia.org/wiki/Reparations_for_slavery")

soup = BeautifulSoup(result.text, 'html.parser')

article = soup.find(id="mw-content-text")

content = article.find_all('p')
save = ""

for p in content:
    print(p.get_text())
    save = save + ' ' + p.get_text()

cur.execute('insert into wikipedia_pages (is_rep, article) VALUES (?, ?)', (True, save))
