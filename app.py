"""
Flask Backend for CP-ABE Secure Cloud Storage System
"""

import os
import time
import logging
import psutil
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import io

from encryption import EncryptionManager
from policy_engine import PolicyEngine
from storage import StorageManager
import config

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

# Initialize components
encryption_manager = EncryptionManager()
policy_engine = PolicyEngine()
storage_manager = StorageManager()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_system_metrics():
    """Get current CPU and memory usage"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "service": "CP-ABE Secure Cloud Storage",
        "storage_mode": config.STORAGE_MODE,
        "system_metrics": get_system_metrics()
    })


@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    """
    Encrypt file with access policy
    
    Expected form data:
    - file: File to encrypt
    - policy: Access policy string (e.g., "Role=Doctor AND Department=CSE")
    
    Returns:
    - JSON with encrypted filename and metadata
    """
    start_time = time.time()
    start_metrics = get_system_metrics()
    
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        if 'policy' not in request.form:
            return jsonify({"error": "No policy provided"}), 400
        
        file = request.files['file']
        policy = request.form['policy']
        
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        
        # Secure the filename
        original_filename = secure_filename(file.filename)
        encrypted_filename = f"encrypted_{original_filename}"
        
        # Read file data
        file_data = file.read()
        
        # Encrypt the file
        logger.info(f"Encrypting file: {original_filename}")
        encrypted_data = encryption_manager.encrypt_file(file_data)
        
        # Save encrypted file
        storage_path = storage_manager.save_encrypted_file(encrypted_filename, encrypted_data)
        
        # Save metadata
        metadata = {
            "original_filename": original_filename,
            "encrypted_filename": encrypted_filename,
            "policy": policy,
            "file_size": len(file_data),
            "encrypted_size": len(encrypted_data),
            "storage_path": storage_path,
            "timestamp": time.time()
        }
        storage_manager.save_metadata(encrypted_filename, metadata)
        
        # Calculate metrics
        end_time = time.time()
        end_metrics = get_system_metrics()
        encryption_time = end_time - start_time
        
        logger.info(f"File encrypted successfully: {encrypted_filename}")
        logger.info(f"Encryption time: {encryption_time:.4f}s")
        logger.info(f"CPU usage: {end_metrics['cpu_percent']}%")
        
        return jsonify({
            "success": True,
            "message": "File encrypted successfully",
            "encrypted_filename": encrypted_filename,
            "original_filename": original_filename,
            "policy": policy,
            "storage_mode": config.STORAGE_MODE,
            "metrics": {
                "encryption_time": f"{encryption_time:.4f}s",
                "cpu_percent": end_metrics['cpu_percent'],
                "memory_percent": end_metrics['memory_percent']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        return jsonify({"error": f"Encryption failed: {str(e)}"}), 500


@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    """
    Decrypt file if user attributes satisfy policy
    
    Expected JSON body:
    - encrypted_filename: Name of encrypted file
    - user_attributes: Dict of user attributes (e.g., {"Role": "Doctor", "Department": "CSE"})
    
    Returns:
    - Decrypted file if access granted
    - Error message if access denied
    """
    start_time = time.time()
    start_metrics = get_system_metrics()
    
    try:
        # Parse request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        encrypted_filename = data.get('encrypted_filename')
        user_attributes = data.get('user_attributes')
        
        if not encrypted_filename or not user_attributes:
            return jsonify({"error": "Missing encrypted_filename or user_attributes"}), 400
        
        logger.info(f"Decryption request for: {encrypted_filename}")
        logger.info(f"User attributes: {user_attributes}")
        
        # Load metadata
        metadata = storage_manager.load_metadata(encrypted_filename)
        policy = metadata['policy']
        
        logger.info(f"Policy: {policy}")
        
        # Check policy
        access_granted, message = policy_engine.check_policy(policy, user_attributes)
        
        if not access_granted:
            logger.warning(f"Access denied for {encrypted_filename}: {message}")
            return jsonify({
                "success": False,
                "message": "Access Denied",
                "reason": message,
                "policy": policy
            }), 403
        
        # Load encrypted file
        encrypted_data = storage_manager.load_encrypted_file(encrypted_filename)
        
        # Decrypt file
        logger.info(f"Decrypting file: {encrypted_filename}")
        decrypted_data = encryption_manager.decrypt_file(encrypted_data)
        
        # Calculate metrics
        end_time = time.time()
        end_metrics = get_system_metrics()
        decryption_time = end_time - start_time
        
        logger.info(f"File decrypted successfully: {encrypted_filename}")
        logger.info(f"Decryption time: {decryption_time:.4f}s")
        logger.info(f"CPU usage: {end_metrics['cpu_percent']}%")
        
        # Return decrypted file
        return send_file(
            io.BytesIO(decrypted_data),
            as_attachment=True,
            download_name=metadata['original_filename'],
            mimetype='application/octet-stream'
        )
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500


@app.route('/list', methods=['GET'])
def list_files():
    """List all encrypted files with their policies"""
    try:
        metadata_files = os.listdir(config.METADATA_PATH)
        files_info = []
        
        for metadata_file in metadata_files:
            if metadata_file.endswith('.json'):
                metadata_path = os.path.join(config.METADATA_PATH, metadata_file)
                with open(metadata_path, 'r') as f:
                    import json
                    metadata = json.load(f)
                    files_info.append({
                        "original_filename": metadata.get('original_filename'),
                        "encrypted_filename": metadata.get('encrypted_filename'),
                        "policy": metadata.get('policy'),
                        "storage_mode": config.STORAGE_MODE
                    })
        
        return jsonify({
            "success": True,
            "count": len(files_info),
            "files": files_info
        }), 200
        
    except Exception as e:
        logger.error(f"List files error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get current system metrics"""
    try:
        metrics = get_system_metrics()
        return jsonify({
            "success": True,
            "metrics": metrics,
            "storage_mode": config.STORAGE_MODE
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting CP-ABE Secure Cloud Storage System")
    logger.info(f"Storage mode: {config.STORAGE_MODE}")
    logger.info(f"Host: {config.FLASK_HOST}:{config.FLASK_PORT}")
    
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.DEBUG_MODE
    )
