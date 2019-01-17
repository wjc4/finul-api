from flask import request, jsonify, render_template
import datetime

from inu import application as app
from inu import db

@app.route('/transaction', methods=['GET'])
def transaction():
    return render_template('index.html')

# @app.route('/loading', methods=['GET'])
# def loading():
#     return render_template('loading.html')

@app.route('/verification', methods=['GET'])
def verification():
    return render_template('verification.html', fail=False)

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

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
        return jsonify({'error': 'sender_id does not exist.', 'sender_id': transaction['sender_id']})

    if not db.check_exist(transaction['receiver_id']):
        return jsonify({'error': 'receiver_id does not exist.', 'receiver_id': transaction['receiver_id']})

    sender_data = db.get(transaction['sender_id'])
    sender_data['pending'] = transaction
    sender_data['state'] = 1
    db.update(transaction['sender_id'], sender_data)
    receiver_data = db.get(transaction['receiver_id'])
    receiver_data['pending'] = transaction
    db.update(transaction['receiver_id'], receiver_data)

    # return jsonify({'state': 1, 'user_id': transaction['sender_id']})
    return render_template('loading.html')

from inu import email_tx

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

    if amount >= 1000:
        email_tx(sender_data['email'], amount)
        # send sms
    return render_template('success.html', amount=pending['amount'], name=receiver_data['name'], receiver_id=pending['receiver_id'], description=pending['description'])

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

@app.route('/get_transactions/<user_id>', methods=['GET'])
def get_transactions(user_id):
    if not db.check_exist(user_id):
        return jsonify({'error': 'user_id does not exist.', 'user_id': user_id})
    data = db.get(user_id)
    transactions = data['transactions']
    all_transactions = []
    for i in range(len(transactions)-1, -1):
        packaged = {}
        t = transactions[i]
        if t['sender_id'] == user_id:
            receiver_data = db.get(t['receiver_id'])
            receiver_name = receiver_data['name']
            packaged['message'] = 'SENT TO {}'.format(receiver_name)
            packaged['dt'] = 'on {} at {}'.format(t['date'], t['time'])
            packaged['amount'] = '-MYR{}'.format(t['amount'])
            packaged['color'] = 'red'
        elif t['receiver_id'] == user_id:
            packaged['message'] = 'RECEIVED'
            packaged['dt'] = 'on {} at {}'.format(t['date'], t['time'])
            packaged['amount'] = 'MYR{}'.format(t['amount'])
            packaged['color'] = 'green'
        else:
            return jsonify({'error': 'user_id not found in transaction'})
        all_transactions.append(packaged)

    return jsonify({'all_transactions': all_transactions})