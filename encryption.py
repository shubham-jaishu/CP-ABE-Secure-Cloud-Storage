"""
Encryption module using AES (Fernet) for file encryption/decryption
"""

import os
from cryptography.fernet import Fernet
import config


class EncryptionManager:
    """Manages file encryption and decryption operations"""
    
    def __init__(self):
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_generate_key(self):
        """Load existing encryption key or generate a new one"""
        if os.path.exists(config.ENCRYPTION_KEY_PATH):
            with open(config.ENCRYPTION_KEY_PATH, 'rb') as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(config.ENCRYPTION_KEY_PATH, 'wb') as key_file:
                key_file.write(key)
            return key
    
    def encrypt_file(self, file_data):
        """
        Encrypt file data using AES (Fernet)
        
        Args:
            file_data (bytes): Raw file data to encrypt
            
        Returns:
            bytes: Encrypted file data
        """
        try:
            encrypted_data = self.cipher.encrypt(file_data)
            return encrypted_data
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_file(self, encrypted_data):
        """
        Decrypt file data using AES (Fernet)
        
        Args:
            encrypted_data (bytes): Encrypted file data
            
        Returns:
            bytes: Decrypted file data
        """
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return decrypted_data
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
