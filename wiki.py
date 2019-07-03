#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import json

def clean_wikipedia(text):
    soup = BeautifulSoup(text, 'html.parser')
    article = soup.find(id="mw-content-text")

    content = article.find_all('p')
    save = ""

    for p in content:
        save = save + ' ' + p.get_text()

    return save

result = requests.get("https://en.wikipedia.org/wiki/Reparations_for_slavery")
wp_article_file = open("data/wp_reparations_article", "w")
wp_article_file.write(clean_wikipedia(result.text))
wp_article_file.close()

articles = []
for x in range(1000):
    result = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    articles.append(clean_wikipedia(result.text))

articles_file = open("data/wp_articles.json", "w")
articles_file.write(json.JSONEncoder().encode(articles))
articles_file.close()
