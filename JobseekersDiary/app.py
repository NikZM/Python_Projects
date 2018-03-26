from flask import Flask, render_template, request, json, redirect
import MongoConnection
app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/dashboard', code=302, Response=None)


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/api/rest/activities', methods=['GET'])
def get_all_job_activities():
    resp = ActivitiesDAL.retrive_job_activities("Nik Medgyesy")
    return json.jsonify(resp)


@app.route('/api/rest/activities', methods=['POST'])
def create_job_activity():
    company = request.form['company']
    position = request.form['position']
    date = request.form['date']
    description = request.form['description']

    success = ActivitiesDAL.add_activity(
        "5ab55684a313fc8a5226da9f", company, position, date, description)
    if success:
        return json.dumps({'status': 'OK'})
    else:
        return json.dumps({'status': 'bad'})


@app.route('/api/rest/activities/<activity_id>', methods=['GET'])
def get_job_activity(activity_id):
    resp = ActivitiesDAL.retreive_job_activity(activity_id)
    return json.jsonify(resp)


@app.route('/api/rest/activities/<activity_id>', methods=['PUT'])
def update_job_activity(activity_id):
    return 0


@app.route('/api/rest/activities/<activity_id>', methods=['DELETE'])
def delete_job_activity(activity_id):
    return 0


if __name__ == '__main__':
    app.run()
