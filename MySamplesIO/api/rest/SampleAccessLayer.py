#!/usr/bin/env python
from bson.json_util import dumps
from bson.objectid import ObjectId

import MongoConnection
import UserAccessLayer


def get_sample_count(user_id):
    samples = MongoConnection.get_samples_client()
    number_of_samples = samples.find({"user_id": user_id}).count()

    return number_of_samples


def store_sample_data(user_id, sequence, locus, date):
    samples = MongoConnection.get_samples_client()
    inserted_id = samples.insert_one(
        {"user_id": user_id,
         "sequence": sequence,
         "locus": locus,
         "date": date}
    ).inserted_id

    return inserted_id


def get_sample_data(object_id):
    samples = MongoConnection.get_samples_client()
    sample = samples.find_one({"_id": ObjectId(object_id)},
                              {"sequence": 1, "locus": 1, "date": 1})

    return {"sequence": sample['sequence'], "locus": sample['locus'], "date": sample['date']}


def get_patients_and_samples_by_doctor_id(doctor_id):
    patients = UserAccessLayer.get_patients_list(doctor_id)
    samples = MongoConnection.get_samples_client()

    patients_list = []

    for patient in patients:
        patient_samples = samples.find({"user_id": patient['user_id']})
        patients_list.append(patient_samples)

    return patients_list


def get_patients_samples(user_id):
    samples = MongoConnection.get_samples_client()
    patients_samples = samples.find({"user_id": user_id})

    return dumps(patients_samples)
