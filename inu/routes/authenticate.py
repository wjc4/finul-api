from flask import request, jsonify

from inu import application as app
from inu import db

import pyotp

# STATES IN DB: 1 (transaction pending 2FA confirmation), 2 (2FA passed), 0 (no transaction pending)

@app.route('/auth_code/<user_id>/<code>', methods=['GET']) # either phone or browser can call this.
def authenticate_code(user_id, code):
    data = db.get(user_id)
    secret = data['secret']
    totp = pyotp.TOTP(secret)

    # OTP verified for current time
    status = totp.verify(code)
    if status:
        data['state'] = 2
        db.update(user_id, data)
    return jsonify({'status': status})

@app.route('/auth_start/<user_id>', methods=['GET']) # browser will call this when a transaction is requested.
def start(user_id):
    data = db.get(user_id)
    data['state'] = 1
    db.update(user_id, data)
    return jsonify({'state': 1})

@app.route('/auth_status/<user_id>', methods=['GET']) # browser will be polling this.
def poll(user_id):
    data = db.get(user_id)
    return jsonify({'state': data['state']})