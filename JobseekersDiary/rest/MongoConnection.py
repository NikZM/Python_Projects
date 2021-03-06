from pymongo import MongoClient

import dbconfig


def get_activities_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.jsa.activity


def get_users_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.jsa.users
