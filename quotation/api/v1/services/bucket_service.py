import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
import os

from quotation.models import LogoImage

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_image(self, image, customer_id):
        try:
            file_name = f"{customer_id}/{image.name}"
            res = self.s3_client.upload_fileobj(
                image,
                self.bucket_name,
                file_name,
                ExtraArgs={'ACL': 'public-read'}
            )
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
        except Exception as e:
            return None
        
    def save_to_database(self, image_url, customer_id):
        LogoImage.objects.create(image=image_url, customer_id=customer_id)
