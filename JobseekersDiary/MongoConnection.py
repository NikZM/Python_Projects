from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

import dbconfig


def __get_jsa_database():
    client = MongoClient(dbconfig.get_connection_string())
    return client.jsa


def add_new_user(user_name):
    users = __get_jsa_database().users
    inserted_id = users.insert_one({"user_name": user_name}).inserted_id
    return inserted_id


def retrieve_user_id(user_name):
    users = __get_jsa_database().users
    user_id = users.find_one({"user_name": user_name})
    return user_id['_id']


def add_activity(user_id, company, position, date, description):
    activities = __get_jsa_database().activities
    result = activities.update_one(
        {"user_id": user_id,
         "company": company,
         "position": position
         },
        {"$push": {
            "activity": {
                "date": date,
                "description": description
            }
        }
        }, upsert=True).acknowledged
    return result


def retrieve_job_activities(user_id):
    activities = __get_jsa_database().activities
    users_activities = activities.find({"user_id": user_id})
    result = dumps(users_activities)
    return result


def retrieve_job_activity(object_id):
    activities = __get_jsa_database()
    activity = activities.find_one({"_id": ObjectId(object_id)})
    result = dumps(activity)
    return result

# print retrieve_job_activities("5ab55684a313fc8a5226da9f")
