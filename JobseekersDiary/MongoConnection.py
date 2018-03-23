from pymongo import MongoClient
from bson.json_util import dumps
from flask import json

import datetime
import pprint
import dbconfig


def __get_database_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.jsa

def add_new_user(name):
    db = __get_database_client()
    users = db.users
    users.insert_one({name})

def add_activity(name, company, position, date, description):
    db = __get_database_client()
    activities = db.activities
    result = activities.insert_one(
        {
            "user": name,
            "company": company,
            "position": position,
            "date": date,
            "description": description
        })
    return result.acknowledged

def add_job(name, company, position, date):
    db = __get_database_client()
    users = db.users
    posts.update_one(
        {"user":name},
        {
            "$set": {
                "companies":company,
                "position":position,
                "date":date
            }
        }
    )
    return posts.find_one({"name":name})

def _write_nik():
    add_new_user("Nik Medgyesy")

def _write_job():
    return add_activity("Nik Medgyesy", "Cancer Genomics", "Junior Software Developer", "2018-03-21", "Technical Assessment")



def retrive_job_activity(name):
    db = __get_database_client()
    activities = db.activities
    users_activities = activities.find({"user":name})
    result = dumps(users_activities)
    return result

# for x in all_users_posts:
#     pprint.pprint(x)


# collection = db.test_collection
# posts = db.posts
# # post = {"author": "Mike",
# #         "text": "My second blog post!",
# #         "tags": ["mongodb", "python", "pymongo"],
# #         "date": datetime.datetime.utcnow()
# #        }

# # post_id = posts.insert_one(post).inserted_id
# # post2 = posts.find_one({"text": "My second blog post!"})
# pprint.pprint(posts)