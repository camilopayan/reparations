#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import requests
import billboard
import pprint
import time

HIP_HOP_CHART = 'r-b-hip-hop-songs'
RAP_CHART = 'rap-song'

def get_songs(songs, chart_name):
    chart = billboard.ChartData(chart_name)

    while chart.previousDate and not chart.date.startswith('1979'):
        for s in chart:
            songs[s.title] = s.artist

        try:
            chart = billboard.ChartData(chart_name, chart.previousDate)
        except requests.exceptions.RequestException:
            time.sleep(10)
            continue

        print(chart)
        time.sleep(10)

songs = {}
get_songs(songs, HIP_HOP_CHART)
get_songs(songs, RAP_CHART)

song_t = []

for key in songs:
    song_t.append((key, songs[key]))

file_obj = open("data/song_list.json", "w")
file_obj.write(json.JSONEncoder().encode(song_t))
file_obj.close()
