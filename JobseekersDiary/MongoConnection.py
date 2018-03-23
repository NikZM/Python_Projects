from pymongo import MongoClient
from bson.json_util import dumps
from flask import json
from bson.objectid import ObjectId

import dbconfig


def __get_activities_database():
    client = MongoClient(dbconfig.get_connection_string())
    return client.jsa.activities


def add_activity(name, company, position, date, description):
    activities = __get_activities_database()
    result = activities.insert_one(
        {
            "user": name,
            "company": company,
            "position": position,
            "date": date,
            "description": description
        })
    return result.acknowledged


def retrive_job_activities(name):
    activities = __get_activities_database()
    users_activities = activities.find({"user": name})
    result = dumps(users_activities)
    return result


def retrive_job_activity(object_id):
    activities = __get_activities_database()
    activity = activities.find_one({"_id": ObjectId(object_id)})
    result = dumps(activity)
    return result
