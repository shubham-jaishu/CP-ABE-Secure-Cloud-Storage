#!/bin/bash

# Backup script for CP-ABE Secure Cloud Storage System

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "================================================"
echo "CP-ABE System Backup"
echo "Timestamp: $TIMESTAMP"
echo "================================================"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup metadata
if [ -d "metadata" ]; then
    echo "📋 Backing up metadata..."
    cp -r metadata "$BACKUP_DIR/"
    echo "✅ Metadata backed up"
fi

# Backup encrypted files (if local storage)
if [ -d "encrypted_files" ]; then
    echo "🔒 Backing up encrypted files..."
    cp -r encrypted_files "$BACKUP_DIR/"
    echo "✅ Encrypted files backed up"
fi

# Backup encryption key (SECURE THIS!)
if [ -f "encryption.key" ]; then
    echo "🔑 Backing up encryption key..."
    cp encryption.key "$BACKUP_DIR/"
    chmod 600 "$BACKUP_DIR/encryption.key"
    echo "⚠️  IMPORTANT: Encryption key backed up - Keep this secure!"
fi

# Backup logs
if [ -f "cpabe_system.log" ]; then
    echo "📝 Backing up logs..."
    cp cpabe_system.log "$BACKUP_DIR/"
    echo "✅ Logs backed up"
fi

# Create backup info file
cat > "$BACKUP_DIR/backup_info.txt" << EOF
CP-ABE System Backup
====================
Timestamp: $TIMESTAMP
Hostname: $(hostname)
User: $(whoami)
Storage Mode: ${STORAGE_MODE:-local}

Contents:
- Metadata files
- Encrypted files (if local storage)
- Encryption key
- System logs

To restore:
1. Copy metadata/ folder back to application directory
2. Copy encrypted_files/ folder back (if using local storage)
3. Copy encryption.key back (REQUIRED for decryption)
4. Restart application

SECURITY WARNING:
The encryption.key file is critical and sensitive.
Store this backup in a secure location.
EOF

# Compress backup
echo "📦 Compressing backup..."
tar -czf "$BACKUP_DIR.tar.gz" -C backups "$(basename $BACKUP_DIR)"
rm -rf "$BACKUP_DIR"

echo "✅ Backup complete: $BACKUP_DIR.tar.gz"
echo ""
echo "Backup size: $(du -h $BACKUP_DIR.tar.gz | cut -f1)"
echo ""
echo "⚠️  Remember to store this backup securely!"

# Optional: Upload to S3
if [ "$STORAGE_MODE" = "s3" ] && [ -n "$S3_BUCKET_NAME" ]; then
    echo ""
    echo "📤 Uploading backup to S3..."
    aws s3 cp "$BACKUP_DIR.tar.gz" "s3://$S3_BUCKET_NAME/backups/" && echo "✅ Uploaded to S3"
fi
