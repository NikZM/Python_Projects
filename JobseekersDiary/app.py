import sys
sys.path.append('/rest/')
from flask import Flask, render_template, request, json, redirect
from rest import MongoConnection
from bson import json_util

from rest import ActivitiesDAL, UsersDAL
app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard', code=302, Response=None)


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/api/rest/activities', methods=['GET'])
def get_all_job_activities():
    user_id = "5acb611ca313fc8a809fea7a"
    resp = ActivitiesDAL.retrieve_job_activities(user_id)
    return json.jsonify(resp)


@app.route('/api/rest/activities', methods=['POST'])
def create_job_activity():
    user_id = request.form['user_id']
    company = request.form['company']
    position = request.form['position']
    date = request.form['date']
    description = request.form['description']

    success = ActivitiesDAL.add_activity(
        user_id, company, position, date, description)
        
    if success:
        return json.dumps({'status': 'OK'})
    else:
        return json.dumps({'status': 'bad'})


@app.route('/api/rest/activities/<activity_id>', methods=['GET'])
def get_job_activity(activity_id):
    resp = ActivitiesDAL.retrieve_job_activity(activity_id)
    return json.jsonify(resp)


@app.route('/api/rest/activities/<activity_id>', methods=['PUT'])
def update_job_activity(activity_id):
    return 0


@app.route('/api/rest/activities/<activity_id>', methods=['DELETE'])
def delete_job_activity(activity_id):
    return 0


@app.route('/api/rest/users', methods=['POST'])
def add_new_user():
    email = request.form['email']
    password = request.form['password']
    resp = UsersDAL.add_new_user(email, password)
    return json.jsonify(resp)



if __name__ == '__main__':
    app.run()
