#!/usr/bin/env python3

from bs4 import BeautifulSoup
import sqlite3
import requests
import billboard
import pprint
import time

HIP_HOP_CHART = 'r-b-hip-hop-songs'

songs = {}
chart = False

while True:
    if chart == False:
        chart = billboard.ChartData(HIP_HOP_CHART)
    else:
        previous = chart.previousDate
        chart = billboard.ChartData(HIP_HOP_CHART, previous)

    for s in chart:
        songs[s.title] = s.artist

    print(len(songs))
    if len(songs) > 1000:
        break

pprint.pprint(songs)

song_t = []

for key in songs:
    song_t.append((key, songs[key]))

con = sqlite3.connect("db.sqlite")
cur = con.cursor()
cur.executemany('INSERT INTO hip_hop_corpus (name, artist) VALUES (?, ?)', song_t)
con.commit()
cur.close()
con.close()

