from os import getenv

import boto3


def upload_image():
    s3 = boto3.client(
        's3',
        aws_access_key_id=getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=getenv('AWS_SECRET_KEY')
    )
