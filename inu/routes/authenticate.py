from flask import request, jsonify, render_template

from inu import application as app
from inu import db

import pyotp

# STATES IN DB: 1 (transaction pending 2FA confirmation), 2 (2FA passed), 0 (no transaction pending)

@app.route('/auth_code/<user_id>/<code>', methods=['GET']) # either phone or browser can call this.
def authenticate_code(user_id, code):
    if not db.check_exist(user_id):
        return jsonify({'error': 'user_id does not exist.'})
    data = db.get(user_id)
    secret = data['secret']
    totp = pyotp.TOTP(secret)

    # OTP verified for current time
    status = totp.verify(code)
    if status:
        data['state'] = 2
        db.update(user_id, data)
        trans = confirm_transaction(user_id)
        return render_template('success.html', amount=trans['amount'], name=trans['receiver_name'], receiver_id=trans['receiver_id'], description=trans['description'])
    # return jsonify({'status': status, 'user_id': user_id})

def confirm_transaction(sender_id):
    sender_data = db.get(sender_id)

    pending = sender_data['pending']
    amount = pending['amount']
    if float(amount) > sender_data['balance']:
        return jsonify({'error': 'Account has insufficient balance for this transaction.'})

    receiver_id = pending['receiver_id']
    receiver_data = db.get(receiver_id)
    sender_data = confirm_pending(sender_data, sender_id)
    receiver_data = confirm_pending(receiver_data, receiver_id)
    db.update(sender_id, sender_data)
    db.update(receiver_id, receiver_data)
    return pending
    # return jsonify({'status': True, 'transaction': pending})

def confirm_pending(data, id):
    pending = data['pending']
    amount = pending['amount']
    if id == pending['sender_id']:
        data['balance'] -= float(amount)
    elif id == pending['receiver_id']:
        data['balance'] += float(amount)
    data['pending'] = None
    data['state'] = 0 # reset to 0 (no transaction pending) after confirming transfer
    data['transactions'].append(pending)
    return data
    
# @app.route('/auth_start/<user_id>', methods=['GET']) # browser will call this when a transaction is requested.
# def start(user_id):
#     if not db.check_exist(user_id):
#         return jsonify({'error': 'user_id does not exist.'})
#     data = db.get(user_id)
#     data['state'] = 1
#     db.update(user_id, data)
#     return jsonify({'state': 1})

@app.route('/auth_status/<user_id>', methods=['GET']) # browser will be polling this.
def status(user_id):
    if not db.check_exist(user_id):
        return jsonify({'error': 'user_id does not exist.'})
    data = db.get(user_id)
    return jsonify({'state': data['state'], 'user_id': user_id})

@app.route('/auth_poll/<user_id>', methods=['GET']) # phone will be polling this.
def poll(user_id):
    if not db.check_exist(user_id):
        return jsonify({'error': 'user_id does not exist.'})
    data = db.get(user_id)
    if data['pending']:
        return jsonify({'transaction': data['pending']})
    else:
        return jsonify({'transaction': None})
