from flask import Flask, request
import db_main, cluster, grouping

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<id>')
def get_user(id):
    interests = db_main.query('SELECT interests FROM users WHERE user_id = ' + id)
    groups = [grouping.insert_category(interest) for interest in interests]
    return str(groups)

def run_server():
    app.run()

def stop_server():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is not None:
        shutdown_func()