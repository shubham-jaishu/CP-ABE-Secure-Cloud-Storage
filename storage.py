"""
Storage module for handling local and S3 file storage
"""

import os
import json
import boto3
from botocore.exceptions import ClientError
import config


class StorageManager:
    """Manages file storage operations (local or S3)"""
    
    def __init__(self):
        self.storage_mode = config.STORAGE_MODE
        
        if self.storage_mode == "s3":
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION
            )
            self.bucket_name = config.S3_BUCKET_NAME
            self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                if config.AWS_REGION == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                else:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': config.AWS_REGION}
                    )
                print(f"Created S3 bucket: {self.bucket_name}")
            except ClientError as e:
                print(f"Warning: Could not create bucket - {str(e)}")
    
    def save_encrypted_file(self, filename, encrypted_data):
        """
        Save encrypted file to storage
        
        Args:
            filename (str): Name of the file
            encrypted_data (bytes): Encrypted file content
            
        Returns:
            str: Storage path or S3 key
        """
        if self.storage_mode == "s3":
            return self._save_to_s3(filename, encrypted_data)
        else:
            return self._save_to_local(filename, encrypted_data)
    
    def _save_to_local(self, filename, encrypted_data):
        """Save file to local storage"""
        file_path = os.path.join(config.LOCAL_STORAGE_PATH, filename)
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        return file_path
    
    def _save_to_s3(self, filename, encrypted_data):
        """Upload file to S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=encrypted_data
            )
            return f"s3://{self.bucket_name}/{filename}"
        except ClientError as e:
            raise Exception(f"S3 upload failed: {str(e)}")
    
    def load_encrypted_file(self, filename):
        """
        Load encrypted file from storage
        
        Args:
            filename (str): Name of the file
            
        Returns:
            bytes: Encrypted file content
        """
        if self.storage_mode == "s3":
            return self._load_from_s3(filename)
        else:
            return self._load_from_local(filename)
    
    def _load_from_local(self, filename):
        """Load file from local storage"""
        file_path = os.path.join(config.LOCAL_STORAGE_PATH, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {filename}")
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def _load_from_s3(self, filename):
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"S3 download failed: {str(e)}")
    
    def save_metadata(self, filename, metadata):
        """
        Save file metadata (including policy)
        
        Args:
            filename (str): Original filename
            metadata (dict): Metadata dictionary
        """
        metadata_file = os.path.join(config.METADATA_PATH, f"{filename}.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def load_metadata(self, filename):
        """
        Load file metadata
        
        Args:
            filename (str): Original filename
            
        Returns:
            dict: Metadata dictionary
        """
        metadata_file = os.path.join(config.METADATA_PATH, f"{filename}.json")
        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata not found for: {filename}")
        
        with open(metadata_file, 'r') as f:
            return json.load(f)
