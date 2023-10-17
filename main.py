import signal, time, json, re, requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from public.ipinyou import predictor, bidder
from public import utils, api, db_main

# Handler function for when the program is terminated
def terminate_handler(signal, frame):
    print('Terminating server...')
    stop_server()
    db_main.shutdown()
    exit(0)
    
def run_server():
    app.run(debug=True)

def stop_server():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is not None:
        shutdown_func()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "https://portfolio-a40fe.web.app", "https://portfolio-a40fe.firebaseapp.com"]}})

@app.route('/')
def hello_world():
    return render_template('index.html')

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
    pass

@app.route('/ad_request')
def ad_request():
    start = time.time()
    data = request.args
    user_tags = data['user_tags'].split(',')
    floor_price = data['floor_price']
    number = data['number']

    advertiserResult = predictor.get_advertiser_for(user_tags, floor_price, int(number))
    result = []
    for advertiser in advertiserResult:
        advertiser['bid'] = bidder.get_bid(user_tags, floor_price, advertiser['advertiserID'], advertiser['ctr'])['bid']
        db_main.update_ad_impression(advertiser['adID'])
        result.append({
            'advertiserID': advertiser['advertiserID'],
            'advertiser': advertiser['advertiser'],
            'campaignID': advertiser['campaignID'],
            'campaign': advertiser['campaign'],
            'adID': advertiser['adID'],
            'adText': advertiser['adText'],
            'bid': '{:.2f}$'.format(utils.convert_cost(advertiser['bid'])),
            'ctr': '{:.2f}%'.format(advertiser['ctr']),
            'time': '{:.2f}ms'.format((time.time() - start)*1000),
        })
        
    return jsonify(result)

    # return (utils.ad_html(advertiserResult['advertiser'], advertiserResult['campaign'], advertiserResult['adText']))

if __name__ == '__main__':
    # Run Flask server
    run_server()

    # Register handler for termination
    signal.signal(signal.SIGINT, terminate_handler)