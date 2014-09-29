"""
Copyright (C) 2014, Jill Huchital
"""

from apiclient.discovery import build
from apiclient.errors import HttpError
from utils import clean_db_object

""" see https://console.developers.google.com/project/apps~videocategoryarcs/apiui/credential """
YOUTUBE_V3_API_KEY = 'API_KEY_HERE'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_MAX_RESULTS = 25

import operator

def youtube_search(query_string):
    videos = []
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_V3_API_KEY)
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(
            q=query_string,
            type='video',
            part="id,snippet",
            maxResults=YOUTUBE_MAX_RESULTS
        ).execute()

        """ Just look for videos, not channels or playlists """
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(dict(video_id = search_result["id"]["videoId"],
                    title = search_result["snippet"]["title"]))

    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

    return videos


def get_all_playlists(dbs):
    retval = []
    """
    for topic in dbs['topics'].find():
        if 'playlist' not in topic or len(topic['playlist']) < 1:
            continue
        print topic
        new_playlist = dict(playlist_name = topic['topic_name'],
                playlist_videos = topic['playlist'])
        print new_playlist
        retval.append(new_playlist)
    """
    retval = []
    for category in dbs['categories'].find():
        if 'topic_data' not in category:
            continue
        for topic in category['topic_data']:
            print topic
            if 'playlist' in category['topic_data'][topic]:
                new_playlist = dict(playlist_name = category['topic_data'][topic]['topic_name'],
                        playlist_videos = category['topic_data'][topic]['playlist'])
                print new_playlist
                retval.append(new_playlist)
    print retval
    return retval

def add_new_category(params, dbs):
    retval = "success"
    try:
        category_name = params.get('category_name')
        category_arc = params.get('category_arc')
    except:
        return "params missing"
    return retval

def compute_playlist(category, topic):
    print 'looking for topic ' + topic['topic_name']
    playlist = []
    for arcpos in category['arc']:
        video_choices = {}
        for c_search_term in arcpos['search_terms']:
            for t_search_term in topic['search_terms']:
                search_term = '\"' + c_search_term + ' ' + t_search_term + '\"'
                videos = youtube_search(search_term)
                for v in videos:
                    if v['video_id'] not in video_choices:
                        video_choices[v['video_id']] = 1
                    else:
                        video_choices[v['video_id']] += 1
        sorted_choices = sorted(video_choices.iteritems(), key = operator.itemgetter(1), reverse=True)
        if len(sorted_choices) < 1 and arcpos['required'] is True:
            print 'arcpos ' + arcpos['arcpos'] + ' empty; cannot complete playlist for ' + topic['topic_name'] + ' in category ' + category['category_name']
            break
        else:
            i = 0
            while i < len(sorted_choices) and sorted_choices[i][0] in playlist:
                i += 1
                continue
            if i < len(sorted_choices):
                playlist.append(sorted_choices[i][0])
    print 'final playlist for ' + topic['topic_name']
    print playlist
    return playlist

def add_new_topic(params, dbs):
    retval = "success"
    try:
        category_name = params.get('category_name')
        topic_name = params.get('topic_name')
        search_terms = params.get('search_terms')
        print params
        category = dbs['categories'].find_one({'category_name': category_name})
        if category is None:
            print 'no such category'
            retval = "no such category"
        elif 'topic_data' in category and topic_name in category['topic_data']:
            print 'topic exists'
            retval = "topic already exists"
        else:
            new_topic = dict(topic_name = topic_name, topic_display_name = topic_name,
                    search_terms = search_terms)
            print new_topic
            playlist = compute_playlist(category, new_topic)
            new_topic['playlist'] = playlist
            if 'topic_data' not in category:
                category['topic_data'] = {}
            category['topic_data'][topic_name] = new_topic
            print category
            dbs['categories'].save(category)
            new_category = dbs['categories'].find({'category_name': category_name})
            print new_category
    except:
        retval = "params missing"
    return retval

def get_all_categories(dbs):
    retval = []
    for category in dbs['categories'].find():
        retval.append(clean_db_object(category))
    return retval

def get_all_topics(dbs):
    retval = []
    for category in dbs['categories'].find():
        for t in category['topic_data']:
            retval.append(clean_db_object(category['topic_data'][t]))
    return retval

def create_playlists(dbs):
    video_lists = {}
    for category in dbs['categories'].find():
        print 'starting with category ' + category['category_name']
        for t in category['topic_data']:
            topic = category['topic_data'][t]
            playlist = compute_playlist(category, topic)
            topic['playlist'] = playlist
            category['topic_data'][topic['topic_name']] = topic
            dbs['categories'].save(category)
