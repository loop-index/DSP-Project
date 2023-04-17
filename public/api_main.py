from flask import Flask, request, jsonify
import db_main, cluster, grouping, json, api

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users')
def get_users():
    users = db_main.get_all_users()
    response = {}
    for user in users:
        response[user[0]] = api.user_response(user)
    return jsonify(response)

@app.route('/user/<id>')
def get_user(id):
    return jsonify(api.user_response(db_main.get_by_id(id)))

@app.route('/groups')
def get_groups():
    return str(grouping.get_categories())

def run_server():
    app.run()

def stop_server():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is not None:
        shutdown_func()