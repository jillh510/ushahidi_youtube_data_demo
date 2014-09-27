"""
Copyright (C) 2014, Jill Huchital
"""

""" Clean _id out of objects returned from the DB, so that they'll JSONify nicely """
def clean_db_object(obj):
    for key in ["_id"]:
        obj.pop(key, None)
    return obj
