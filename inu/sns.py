import boto3
# from .password import get_aws_access_key_id, get_aws_secret_access_key, get_number, get_region

import datetime
import os

class SNSConnection:
    def __init__(self):
        # Create an SNS client
        print("connecting to aws sns")
        self.client = boto3.client(
            "sns",
            # aws_access_key_id=os.environ['aws_access_key_id'],
            # aws_secret_access_key=os.environ['aws_secret_access_key'],
            # region_name=os.environ['region']
            aws_access_key_id='AKIAII3WXXP4Q6D2ZBHA',
            aws_secret_access_key='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',
            region_name='ap-southeast-1'
        )
        # self.client = boto3.client(
        #     "sns",
        #     aws_access_key_id=get_aws_access_key_id(),
        #     aws_secret_access_key=get_aws_secret_access_key(),
        #     region_name=get_region()
        # )

        self.client.set_sms_attributes(
            attributes={
                'DefaultSenderID': 'CIMBBank',
                'DefaultSMSType': 'Transactional'
            }
        )
        print("connected to aws sns")

    def insert(self, sms_number, target_name, amount=0.00):
        today = datetime.date.today().strftime('%d/%m %H:%M')
        message = "Your transfer to " + target_name + " for RM" + str(amount) + " on " + today + " was successful. If unauthorised, call +603 6204 7788"
        # Send your sms message.
        self.client.publish(
            PhoneNumber=sms_number,
            Message=message
        )