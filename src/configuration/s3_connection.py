import boto3
from src.constant.env_variables import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

class S3Client:
    def __init__(self) -> None:
        try:
            self.client = boto3.client(
                service_name = 's3',
                region_name = 'ap-south-1',
                aws_access_key_id = AWS_ACCESS_KEY_ID,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                )
        except Exception as e:
            raise e