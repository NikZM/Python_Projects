from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

import MongoConnection


def add_activity(user_id, company, position, date, description):
    activities = MongoConnection.get_activities_database()
    d = datetime.date(*(int(s) for s in date.split('-')))
    result = activities.update_one(
        {"user_id": user_id,
         "company": company,
         "position": position
         },
        {"$push": {
            "activity": {
                "date": d,
                "description": description
            }
        }
        }, upsert=True).acknowledged
    return result


def retrieve_job_activities(user_id):
    activities = MongoConnection.get_activities_database()
    users_activities = activities.find({"user_id": user_id})
    result = dumps(users_activities)
    return result


def retrieve_job_activity(object_id):
    activities = MongoConnection.get_activities_database()
    activity = activities.find_one({"_id": ObjectId(object_id)})
    result = dumps(activity)
    return result


def delete_job(object_id):
    activities = MongoConnection.get_activities_database()
    result = activities.delete_one({"_id": ObjectId(object_id)}).acknowledged
    return result


def delete_job_activity(object_id, date, description):
    activities = MongoConnection.get_activities_database()
    d = datetime.date(*(int(s) for s in date.split('-')))
    result = activities.update_one(
        {"_id": ObjectId(object_id)},
        {"$pull": {
            "activity": {
                "date": d,
                "description": description
            }
        }}
    ).acknowledged
    return result


def update_job_activity(object_id, company, position):
    return None
