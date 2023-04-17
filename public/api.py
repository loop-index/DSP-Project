from flask import Flask, request, jsonify
import db_main, cluster, grouping, json

def user_response(user):
    return {
            'name': user[1],
            'age': user[2],
            'gender': user[3],
            'interests': json.loads(user[4]),
        }