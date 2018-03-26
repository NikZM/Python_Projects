#!/usr/bin/env python
from flask import Flask
from flask_hashing import Hashing
from bson.json_util import dumps
from bson.objectid import ObjectId

import MongoConnection
import SampleAccessLayer

app = Flask(__name__)
hashing = Hashing(app)


def make_email_unique():
    """Only needed to run once after collection has been created"""
    # TODO Remove method and write directly to MongoDB console
    MongoConnection.get_users_client().create_index("email", unique=True)
    MongoConnection.get_users_client().create_index("user_name", unique=True)


def create_new_user(username, password, email, is_doctor, doctor_id):
    """Create a new user entry in the mongoDB. 'Username' & 'Email' must both be unique"""
    users = MongoConnection.get_users_client()
    hashed_password = hashing.hash_value(password)
    result = users.insert_one(
        {
            "user_name": username,
            "password": hashed_password,
            "email": email,
            "is_doctor": is_doctor,
            "doctor_id": doctor_id
        }
    ).acknowledged
    return result


def generate_token(username, password):
    """Generates the authentication token for future calls to the API"""
    users = MongoConnection.get_users_client()
    user = users.find_one({"user_name": username}, {
                          "password": 1, "is_doctor": 1})
    user_id = str(user["_id"])
    is_doctor = bool(user['is_doctor'])
    hashed_password = user["password"]

    if hashing.check_value(hashed_password, password):
        # TODO Generate token
        return {"user_id": user_id, "token": "temp", "is_doctor": is_doctor}
    else:
        # TODO Include bad credentials exception
        return None


def get_patients_list(user_id):
    """Returns a list of patients with the doctor_id matching the user_id"""
    # TODO Add validation to ensure this method is only called by users with is_doctor True
    users = MongoConnection.get_users_client()
    result = users.find({"doctor_id": user_id}, {"user_name": 1})
    return result


def get_patient_information(user_id):
    """Returns the username, email address and sample count for a patient"""
    users = MongoConnection.get_users_client()
    user = users.find_one({"_id": user_id}, {"user_name": 1, "email": 1})
    number_of_samples = SampleAccessLayer.get_sample_count(user_id)
    return {"user": user['user_name'],
            "email": user['email'],
            "number_of_samples": number_of_samples}
