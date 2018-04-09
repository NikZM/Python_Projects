from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument
import datetime
import UsersDAL
import MongoConnection
import json


def add_activity(user_id, company, position, date, description):
    """"Actually working, I'm happy. Will add an activity to an already present post (company and position).
    If none exist a new one is upserted and the users job list is updated with the new object_id key.

    Returns the object_id for the post"""
    activities = MongoConnection.get_activities_client()
    d = datetime.datetime(*(int(s) for s in date.split('-')))

    activity = activities.find_one_and_update(
        {
            "user_id": user_id,
            "company": company,
            "position": position
        },
        {
            "$push": {
                "activity": {
                    "date": d,
                    "description": description
                }
            }
        }, upsert=True, return_document=ReturnDocument.AFTER)
    UsersDAL.add_activity_to_user(user_id, str(activity["_id"]))

    return str(activity["_id"])


def retrieve_job_activities(user_id, reverse_date_order=True):
    """This one works to? I'm on a role. Retrieves the job activities list for a user as an array of dictionaries.
    By default the activities are sorted in reverse chronological order"""
    activities = MongoConnection.get_activities_client()
    job_ids = UsersDAL.get_users_activity_ids(user_id)
    job_activities = []

    for j_id in job_ids:
        job_activity = activities.find_one({"_id": ObjectId(j_id)})
        # Unnest object id from id
        job_activity["_id"] = str(job_activity["_id"])

        # Reverse chronological date
        job_activity["activity"].sort(
            key=lambda activity: activity["date"],
            reverse=reverse_date_order)

        # Format date to YYYY-mm-dd
        for activity in sorted(job_activity["activity"], key=lambda activity: activity["date"], reverse=True):
            activity["date"] = activity["date"].strftime("%Y-%m-%d")

        job_activities.append(job_activity)

    return job_activities


def retrieve_job_activity(object_id):
    activities = MongoConnection.get_activities_client()
    activity = activities.find_one({"_id": ObjectId(object_id)})
    result = dumps(activity)
    return result


def delete_job(object_id):
    activities = MongoConnection.get_activities_client()
    result = activities.delete_one({"_id": ObjectId(object_id)}).acknowledged
    return result


def delete_job_activity(object_id, date, description):
    activities = MongoConnection.get_activities_client()
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


def delete_all_user_activity(user_id):
    """Deletes all job activities under a given user. Returns a bool indicating if the operation was successful"""
    activities = MongoConnection.get_activities_client()
    activities.delete_many({})
    user_client = MongoConnection.get_users_client()
    user_client.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set":
            {
                "jobs": []
            }
         })

