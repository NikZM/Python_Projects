from pymongo import MongoClient
from . import dbconfig


def get_activities_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.get_database().activities


def get_users_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.get_database().users