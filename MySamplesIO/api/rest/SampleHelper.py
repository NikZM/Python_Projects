#!/usr/bin/env python

import random
import datetime
import uuid

import SampleAccessLayer


def generate_and_store(user_id):
    """A wrapper for the generate function that will also store the result in the mongo database,
    useful for compiling data to test. The UUID will be replaced with an auto-generated Objectid from mongo"""
    # TODO Delete when a proper test harness has been developed
    sample = generate()
    sequence = sample['sequence']
    locus = sample['locus']
    date = sample['date']
    generated_id = SampleAccessLayer.store_sample_data(
        user_id, sequence, locus, date)

    return {"sequence": sequence, "locus": locus, "date": date, "_id": str(generated_id)}


def process_and_store(object_id, user_id, store=True):
    """A wrapper for the process function that will fetch and store the result in the mongo database,
    useful for compiling data to test. The UUID will be replaced with an auto-generated Objectid from mongo"""
    # TODO Delete when a proper test harness has been developed
    sample = SampleAccessLayer.get_sample_data(object_id)

    processed_sample = process(sample['sequence'],
                               sample['locus'],
                               sample['date'])

    if store:
        generated_id = SampleAccessLayer.store_sample_data(user_id,
                                                        processed_sample['sequence'],
                                                        processed_sample['locus'],
                                                        processed_sample['date'])

        processed_sample['_id'] = generated_id

    return processed_sample


def generate():
    """Generate a random amino-acid sequence of length between 1 and 100 and a random locus upto 9999999.
    The function also returns the current date time and a UUID."""
    aa_list = ["A", "C", "T", "G"]
    aa_string = ""

    loop_count = random.randint(1, 100)

    for x in range(1, loop_count):
        aa_letter = aa_list[random.randint(0, 3)]
        aa_string += aa_letter

    locus = random.randint(0, 9999999)
    uu_id = str(uuid.uuid4())
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"sequence": aa_string, "locus": locus, "date": date, "_id": uu_id}


def process(sequence, locus, date):
    """Returns the sequence with the amino-acids inverted, i.e. A<>T, G<>C"""
    aa_conversion = {"A": "T", "T": "A", "C": "G", "G": "C"}
    inverse_sequence = ""

    for s in sequence:
        inverse_sequence += aa_conversion[s]

    uu_id = str(uuid.uuid4())

    return {"sequence": inverse_sequence, "locus": locus, "date": date, "_id": uu_id}
