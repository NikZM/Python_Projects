#!/usr/bin/env python
import sys
sys.path.append('./api/rest/')
from flask import Flask, request, json, Session
from flask_httpauth import HTTPBasicAuth

import UserAccessLayer
import SampleAccessLayer
import SampleHelper

app = Flask(__name__)
session = Session()
auth = HTTPBasicAuth()


@app.route('/users', methods=['POST'])
def create_new_user():
    """Creates a new user"""
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    is_doctor = request.form['is_doctor']
    doctor_id = request.form['doctor_id']
    success = UserAccessLayer.create_new_user(
        username, password, email, is_doctor, doctor_id)
    if sucess:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


@app.route('/tokens', methods=['POST'])
def sign_in():
    """Returns crediential token"""
    username = request.form['username']
    password = request.form['password']
    user = UserAccessLayer.generate_token(username, password)
    session['token'] = user['token']
    session['user_id'] = user['user_id']
    session['is_doctor'] = user['is_doctor']

    return json.dumps({'success': True, 'token': session['token']}), 200, {'ContentType': 'application/json'}


@app.route('/patients', methods=['GET'])
@auth.login_required
def get_patients_list():
    "Returns a list of patients"
    # TODO Add validation to ensure this is only called by users with is_doctor set to true
    resp = UserAccessLayer.get_patients_list(user_id)

    return json.dumps(resp)


@app.route('/samples', methods=['POST'])
def add_sample():
    """Returns a random sample object for patient. If this route is called by a doctor 404 is returned"""
    if 'is_doctor' in session.keys and session['is_doctor']:
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}
    elif 'user_id' in session.keys():
        sample = SampleHelper.generate_and_store(session['user_id'])

        return json.dumps(sample)
    else:

        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}



@app.route('/samples', methods=['GET'])
def get_samples():
    """Returns a list of sample objects for a patient.
    If called by a doctor a list is given for each patient under that doctor"""
    if 'is_doctor' in session.keys and session['is_doctor']:
        resp = SampleAccessLayer.get_patients_and_samples_by_doctor_id(session['user_id'])

        return json.dumps(resp)
    else:
        resp = SampleAccessLayer.get_patients_samples(session['user_id'])

        return json.dumps(resp)
    


@app.route('/patients/<id>', methods=['GET'])
def get_patient(id):
    """Returns patient information (can only be accessed by his patient and its doctor)"""

    return json.dumps(UserAccessLayer.get_patient_information(id))


@app.route('/samples/<id>/process', methods=['GET'])
def process_sample(id):
    """Returns inverted genome sequence for given sample. Can only be called by doctor in charge of this patient"""
    if 'user_id' in session.keys():
        return json.dumps(SampleHelper.process_and_store(id, session['user_id'], False))
    else:
        return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
