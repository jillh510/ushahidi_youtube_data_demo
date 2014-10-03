"""
Copyright (C) 2014, Jill Huchital
"""

USHAHIDI_API_KEY = '5435a4f76d18ed0f54deba52'
USHAHIDI_QUERY_URL = 'http://api.crisis.net/item/?sources=youtube'

import requests

def ushahidi_data():
    videos = []
    headers = {'Authorization': 'Bearer ' + USHAHIDI_API_KEY}
    try:
        r = requests.get(USHAHIDI_QUERY_URL, headers=headers)
        json_data = r.json();
        for d in json_data['data']:
            if 'source' in d and d['source'] == 'youtube' and 'remoteID' in d and 'contentEnglish' in d:
                videos.append(d['remoteID'])
    except:
        print 'something bad'
    return videos


def get_all_playlists():
    retval = []
    ushahidi_playlist = ushahidi_data()
    new_playlist = dict(playlist_name = "SYRIA", 
                playlist_videos = ushahidi_playlist)
    print new_playlist
    retval.append(new_playlist)
    print retval
    return retval

