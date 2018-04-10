from flask import Flask, render_template, request, json, redirect
from bson import json_util
from rest import ActivitiesDAL, UsersDAL, MongoConnection
app = Flask(__name__)

user_id = "5acb611ca313fc8a809fea7a"  # My userid

# ----------------------------------------------------------------------


@app.route('/')
def index():
    return redirect('/dashboard', code=302, Response=None)

# ----------------------------------------------------------------------


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

# ----------------------------------------------------------------------


@app.route('/api/rest/activities', methods=['GET'])
def get_all_job_activities():
    activities = ActivitiesDAL.retrieve_job_activities(user_id)
    return json.jsonify(activities), 200, {'ContentType': 'application/json'}

# ----------------------------------------------------------------------


@app.route('/api/rest/activities', methods=['POST'])
def add_job_activity():
    # user_id = request.form['user_id']
    company = request.form['company']
    position = request.form['position']
    date = request.form['date']
    description = request.form['description']

    activity = ActivitiesDAL.add_activity(
        user_id, company, position, date, description)

    if activity is not None:
        return json.dumps(activity), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({}), 500, {'ContentType': 'application/json'}

# ----------------------------------------------------------------------


@app.route('/api/rest/activities/<activity_id>', methods=['GET'])
def get_job_activity(activity_id):
    activity = ActivitiesDAL.retrieve_job_activity(activity_id)
    if activity is not None:
        return json.jsonify(activity), 200, {'ContentType': 'application/json'}
    else:
        return json.jsonify({'success': False}), 404, {'ContentType': 'application/json'}

# ----------------------------------------------------------------------


@app.route('/api/rest/activities/<activity_id>', methods=['PUT'])
def update_job_activity(activity_id):
    company = request.form['company']
    position = request.form['position']
    updated_count = ActivitiesDAL.update_job_activity(
        activity_id, company, position)
    if updated_count > 0:
        return json.dumps({"success": True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({"success": False}), 400, {'ContentType': 'application/json'}

# ----------------------------------------------------------------------


@app.route('/api/rest/activities/<activity_id>', methods=['DELETE'])
def delete_job_activity(activity_id):
    deleted = ActivitiesDAL.delete_job(user_id, activity_id)

    if deleted:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

# ----------------------------------------------------------------------


@app.route('/api/rest/users', methods=['POST'])
def add_new_user():
    email = request.form['email']
    password = request.form['password']
    inserted_id = UsersDAL.add_new_user(email, password)
    return json.dumps({"_id": inserted_id}), 200, {'ContentType': 'application/json'}


# ----------------------------------------------------------------------

@app.route('/api/rest/all', methods=['GET'])
def get_all():
    """Temporary method for debug and testing"""
    activities_client = MongoConnection.get_activities_client()
    users_client = MongoConnection.get_users_client()

    activities = activities_client.find()
    users = users_client.find()

    activity_arr = []
    users_arr = []

    for activity in activities:
        activity["_id"] = str(activity["_id"])
        activity_arr.append(activity)

    for user in users:
        user["_id"] = str(user["_id"])
        users_arr.append(user)

    return json.dumps({'activity': activity_arr, 'users': users_arr}), 200, {'ContentType': 'application/json'}

# ----------------------------------------------------------------------


if __name__ == '__main__':
    app.run()
