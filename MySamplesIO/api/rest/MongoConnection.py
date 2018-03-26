#!/usr/bin/env python
from pymongo import MongoClient

import dbconfig


def get_samples_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.mysamplesio.samples


def get_users_client():
    client = MongoClient(dbconfig.get_connection_string())
    return client.mysamplesio.users
