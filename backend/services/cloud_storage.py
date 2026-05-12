import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from core.config import settings

class CloudStorageService:
    def __init__(self):
        # Initialize the S3 client for DigitalOcean Spaces
        self.session = boto3.session.Session()
        self.client = self.session.client(
            's3',
            region_name=settings.DO_SPACES_ENDPOINT.split('.')[0].replace('https://', ''),
            endpoint_url=settings.DO_SPACES_ENDPOINT,
            aws_access_key_id=settings.DO_SPACES_KEY,
            aws_secret_access_key=settings.DO_SPACES_SECRET
        )

    async def upload_file(self, file: UploadFile, user_id: str) -> str:
        """
        Uploads a file to DO Spaces and returns the object key.
        The path is structured as: user_id/filename
        """
        file_path = f"{user_id}/{file.filename}"
        
        try:
            # Read file content
            content = await file.read()
            
            self.client.put_object(
                Bucket=settings.DO_SPACES_BUCKET,
                Key=file_path,
                Body=content,
                ACL='private', # Keep files private by default
                ContentType=file.content_type
            )
            
            return file_path # This is the unique reference we save in SQL
            
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Cloud upload failed: {str(e)}")

    def delete_file(self, file_path: str):
        """
        Deletes a file from DO Spaces using its object key.
        """
        try:
            self.client.delete_object(
                Bucket=settings.DO_SPACES_BUCKET,
                Key=file_path
            )
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Cloud deletion failed: {str(e)}")

    def generate_presigned_url(self, file_path: str, expiration=3600):
        """
        Generates a temporary URL so the user can view/download the file securely.
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.DO_SPACES_BUCKET, 'Key': file_path},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            return None

# Instantiate the service
cloud_storage = CloudStorageService()