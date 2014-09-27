"""
Copyright (C) 2014, Jill Huchital
"""
from pymongo import MongoClient

app_db = None

def connect_to_db():
    try:
        client = MongoClient()
        app_db = client.db_data
        all_dbs = dict(categories = app_db.category,
                topics = app_db.topic)
    except:
        print 'uh oh connecting'
        return None
    if app_db is None:
        print 'uh oh db'
        return None
    print app_db.collection_names()
    return all_dbs
