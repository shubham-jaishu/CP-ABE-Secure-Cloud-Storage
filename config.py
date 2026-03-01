"""
Configuration file for CP-ABE Cloud Storage System
"""

import os

# Storage Configuration
STORAGE_MODE = os.getenv("STORAGE_MODE", "local")  # "local" or "s3"

# Local Storage
LOCAL_STORAGE_PATH = os.path.join(os.path.dirname(__file__), "encrypted_files")
METADATA_PATH = os.path.join(os.path.dirname(__file__), "metadata")

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "cpabe-encrypted-files")

# Encryption Configuration
ENCRYPTION_KEY_PATH = os.path.join(os.path.dirname(__file__), "encryption.key")

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8080  # Changed to 8080 to avoid port conflicts
DEBUG_MODE = True

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "cpabe_system.log"

# Create necessary directories
os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)
os.makedirs(METADATA_PATH, exist_ok=True)
