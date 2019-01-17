from flask import request, jsonify

from inu import application as app
from inu import db

import pyotp

@app.route('/authenticate', methods=['POST'])
def evaluate():
    code = request.form['code'] # 6 digit code
    user_id = request.form['user_id']

    data = db.get(user_id)
    secret = data['secret']
    totp = pyotp.TOTP(secret)

    # OTP verified for current time
    status = totp.verify(code)
    return jsonify({'status': status})