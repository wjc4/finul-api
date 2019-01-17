from flask import request, jsonify

from inu import application as app
from inu import db

import pyotp

@app.route('/register/<user_id>', methods=['GET'])
def evaluate():
    random_secret = pyotp.random_base32()
    user_data = {}
    user_data['secret'] = random_secret
    user_data['balance'] = 10000
    user_data['transactions'] = []
    db.insert(user_id, user_data)
    return jsonify({'secret':random_secret})
