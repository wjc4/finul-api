from flask import request, jsonify
import datetime

from inu import application as app
from inu import db

@app.route('/pending_transaction', methods=['POST'])
def pending_transaction():
    data = request.form
    transaction = {}
    transaction['sender_id'] = data.get('sender_id')
    transaction['receiver_id'] = data.get('receiver_id')
    transaction['description'] = data.get('description')
    transaction['amount'] = data.get('amount')

    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d %H:%M")
    date = dt.split()[0]
    time = dt.split()[1]
    transaction['date'] = date
    transaction['time'] = time

    if not db.check_exist(transaction['sender_id']):
        return jsonify({'error': 'sender_id does not exist.', 'user_id': transaction['sender_id']})

    sender_data = db.get(transaction['sender_id'])
    sender_data['pending'] = transaction
    sender_data['state'] = 1
    db.update(transaction['sender_id'], sender_data)
    receiver_data = db.get(transaction['receiver_id'])
    receiver_data['pending'] = transaction
    db.update(transaction['receiver_id'], receiver_data)

    return jsonify({'state': 1, 'user_id': transaction['sender_id']})

@app.route('/confirm_transaction/<sender_id>', methods=['GET'])
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

    return jsonify({'status': True, 'transaction': pending})

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