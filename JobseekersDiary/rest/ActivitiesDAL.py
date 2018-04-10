from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument
import datetime
import UsersDAL
import MongoConnection
import json

# ----------------------------------------------------------------------


def add_activity(user_id, company, position, date, description):
    """"Adds an activity to an already present post (company and position).
    If none exist a new one is upserted and the users job list is updated 
    with the new object_id key.

    Returns the updated post"""
    activities = MongoConnection.get_activities_client()
    d = datetime.datetime(*(int(s) for s in date.split('-')))

    activity = activities.find_one_and_update(
        {
            "user_id": user_id,
            "company": company,
            "position": position
        },
        {
            "$addToSet": {
                "activity": {
                    "date": d,
                    "description": description
                }
            }
        }, upsert=True, return_document=ReturnDocument.AFTER)

    if activity is None:
        return None
    else:
        UsersDAL.add_activity_to_user(user_id, str(activity["_id"]))
        activity["_id"] = str(activity["_id"])
        return activity

# ----------------------------------------------------------------------


def retrieve_job_activities(user_id, reverse_date_order=True):
    """Retrieves the job activities list for a user as an array of 
    dictionaries. By default the activities are sorted in reverse 
    chronological order"""
    activities = MongoConnection.get_activities_client()
    job_ids = UsersDAL.get_users_activity_ids(user_id)
    job_activities = []

    for j_id in job_ids:
        job_activity = activities.find_one({"_id": ObjectId(j_id)},{"user_id":0})
        if job_activity is None:
            break

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

# ----------------------------------------------------------------------


def retrieve_job_activity(object_id):
    """Returns a single job post or none if not found"""
    activities = MongoConnection.get_activities_client()
    if not ObjectId.is_valid(object_id):
        return None
    activity = activities.find_one({"_id": ObjectId(object_id)})
    if activity is not None:
        activity["_id"] = str(activity["_id"])
    return activity

# ----------------------------------------------------------------------


def delete_job(user_id, job_id):
    """Returns a boolean if both the activities and user collection were 
    updated precisely once each"""
    activities = MongoConnection.get_activities_client()
    deleted_job_count = activities.delete_one(
        {"_id": ObjectId(job_id)}).deleted_count
    deleted_job_count += UsersDAL.remove_activity_from_user(user_id, job_id)
    # TODO Return some enums for various states i.e. deleted from user not jobs, jobs not user, neither
    return True if deleted_job_count == 2 else False

# ----------------------------------------------------------------------


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
    ).matched_count

    return True if matched_count == 1 else False

# ----------------------------------------------------------------------


def update_job_activity(object_id, company, position):
    activities = MongoConnection.get_activities_client()
    activity = activities.update_one(
        {"_id": ObjectId(object_id)},
        {"$set": {
            "company": company,
            "position": position
        }
        }
    )

    return activity.modified_count

# ----------------------------------------------------------------------


def delete_all_user_activity(user_id):
    """Deletes all job activities under a given user. 
    Returns a bool indicating if the operation was successful"""
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
# ----------------------------------------------------------------------
