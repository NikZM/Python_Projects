import MongoConnection
from flask_hashing import Hashing
from flask import Flask
from bson.objectid import ObjectId

app = Flask(__name__)
hashing = Hashing(app)


def make_email_unique():
    """Only needed to run once after collection has been created"""
    # TODO Remove method and write directly to MongoDB console
    MongoConnection.get_users_client().create_index("email", unique=True)


def add_new_user(email, password):
    users = MongoConnection.get_users_client()
    salted_password = __salt_password(password)
    inserted_id = users.insert_one(
        {"email": email.lower(),
         "password": salted_password,
         "jobs": []}).inserted_id
    return inserted_id


def add_activity_to_user(user_id, activity_id):
    users = MongoConnection.get_users_client()
    result = users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"jobs": activity_id}})
    return result


def get_users_activity_ids(user_id):
    users = MongoConnection.get_users_client()
    job_ids = []
    result = users.find_one(
        {"_id": ObjectId(user_id)},
        {"jobs": 1, "_id": 0})["jobs"]
    for j_id in result:
        job_ids.append(str(j_id))

    return job_ids


def __salt_password(password):
    salted_pass = hashing.hash_value(password, 'NikZM')
    return salted_pass
