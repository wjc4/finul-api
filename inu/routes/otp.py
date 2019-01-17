
from flask import request, jsonify

from inu import application as app
from inu import db

import pyotp

@app.route('/otptest', methods=['GET'])
def evaluate():
    random_secret = pyotp.random_base32()
    totp = pyotp.TOTP(random_secret)
    generated_otp = totp.now() # => '492039'

    # OTP verified for current time
    totp.verify(generated_otp) # => True
    return jsonify(
        {
            'status':totp.verify(generated_otp),
            'secret':random_secret,
            'otp':generated_otp
        }
    )

