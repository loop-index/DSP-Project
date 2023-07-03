import signal, time, json, re, requests
from flask import Flask, request, jsonify
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
cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

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
    pass

@app.route('/ad_request')
def ad_request():
    start = time.time()
    data = request.args
    user_tags = data['user_tags'].split(',')
    floor_price = data['floor_price']

    advertiserResult = predictor.get_advertiser_for(user_tags, floor_price)
    bidResult = bidder.get_bid(user_tags, floor_price, advertiserResult['advertiserID'], advertiserResult['ctr'])

    db_main.update_ad_impression(advertiserResult['adID'])
    return jsonify({
        'advertiserID': advertiserResult['advertiserID'],
        'advertiser': advertiserResult['advertiser'],
        'campaignID': advertiserResult['campaignID'],
        'campaign': advertiserResult['campaign'],
        'adID': advertiserResult['adID'],
        'adText': advertiserResult['adText'],
        'bid': '{:.2f}$'.format(utils.convert_cost(bidResult['bid'])),
        'ctr': '{:.2f}%'.format(advertiserResult['ctr']),
        'time': '{:.2f}ms'.format((time.time() - start)*1000),
    })

    # return (utils.ad_html(advertiserResult['advertiser'], advertiserResult['campaign'], advertiserResult['adText']))

if __name__ == '__main__':
    # Run Flask server
    run_server()

    # Register handler for termination
    signal.signal(signal.SIGINT, terminate_handler)