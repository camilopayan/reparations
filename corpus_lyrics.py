#!/usr/bin/env python3

import sqlite3
import requests
import os

con = sqlite3.connect("db.sqlite")
con.row_factory = sqlite3.Row
cur = con.cursor()

apikey = os.environ['MUSIXMATCH_API_KEY']

data = []

for row in cur.execute("SELECT * from hip_hop_corpus"):
    payload = {
            'apikey': apikey,
            'q_track': row['name'],
            'q_artist': row['artist'],
            's_track_rating': 'desc',
            's_artist_rating': 'desc',
            'page_size': 1,
            'f_has_lyrics': 'true',
            }
    mmr = requests.get("http://api.musixmatch.com/ws/1.1/track.search", params=payload)
    track_id = ''
    if mmr.json()['message']['body']['track_list']:
        track_id = mmr.json()['message']['body']['track_list'][0]['track']['track_id']
    else:
        continue

    lyrics_pl = {
            'apikey': apikey,
            'track_id': track_id,
            }
    mml = requests.get("https://api.musixmatch.com/ws/1.1/track.lyrics.get", lyrics_pl)
    lyrics = mml.json()['message']['body']['lyrics']['lyrics_body'].replace('\n', ' ')
    data.append((lyrics, row['id']))

cur.executemany('UPDATE hip_hop_corpus SET lyrics = ? WHERE id = ?', data)
con.commit()
cur.close()
con.close()
