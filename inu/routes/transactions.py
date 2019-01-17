from flask import request, jsonify

from inu import application as app
from inu import db

@app.route('/transactions', methods=['POST'])
def record_transaction():
    data = request.form
    transaction = {}
    transaction['sender_id'] = data.get('sender_id')
    transaction['receiver_id'] = data.get('receiver_id')
    transaction['sender_name'] = data.get('sender_name')
    transaction['receiver_name'] = data.get('receiver_name')
    transaction['description'] = data.get('description')
    transaction['amount'] = data.get('amount')
    transaction['date'] = data.get('date')
    transaction['time'] = data.get('time')

    # if not db.check_exist(transaction['sender_id']): # assume they exist.

    sender_data = db.get(transaction['sender_id'])
    sender_data['transactions'].append(transaction)
    db.update(transaction['sender_id'], sender_data)

    receiver_data = db.get(transaction['receiver_id'])
    receiver_data['transactions'].append(transaction)
    db.update(transaction['receiver_id'], receiver_data)

    return jsonify(transaction)
