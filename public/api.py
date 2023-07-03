from flask import Flask, request, jsonify
import json
from public import db_main

def user_response(user):
    return {
            'name': user[1],
            'age': user[2],
            'gender': user[3],
            'interests': json.loads(user[4]),
        }