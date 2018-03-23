from flask import Flask, render_template, request, json, redirect
import MongoConnection
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def signUpUser():
    company =  request.form['company'];
    position = request.form['position'];
    date = request.form['date'];
    return json.dumps({'status':'OK','company':company,'position':position, 'date':date});


@app.route('/api/rest/activities', methods=['GET'])
def get_all_job_activities():
    resp = MongoConnection.retrive_job_activity("Nik Medgyesy")
    return json.jsonify(resp);

@app.route('/api/rest/activities', methods=['POST'])
def create_job_activity():
    request.form['company'];
    return 0;

@app.route('/api/rest/activities/<int:activity_id>', methods=['GET'])
def get_job_activity(activity_id):
    return 0;

@app.route('/api/rest/activities/<int:activity_id>', methods=['PUT'])
def update_job_activity(activity_id):
    return 0;

@app.route('/api/rest/activities/<int:activity_id>', methods=['DELETE'])
def delete_job_activity(activity_id):
    return 0;

if __name__ == '__main__':
    app.run()
