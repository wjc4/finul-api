from flask import request, jsonify

from inu import application as app
from inu import db

import pyotp

@app.route('/register', methods=['POST'])
def register():        
    data = request.form
    user_id = data.get('user_id')
    if db.check_exist(user_id):
        return jsonify({'error': 'user_id already registered in database.'})
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    random_secret = pyotp.random_base32()
    user_data = {}
    user_data['secret'] = random_secret
    user_data['balance'] = 10000
    user_data['transactions'] = []
    user_data['state'] = 0
    user_data['name'] = name
    user_data['email'] = email
    user_data['phone'] = phone
    user_data['pending'] = None

    db.insert(user_id, user_data)
    return jsonify({'secret':random_secret})