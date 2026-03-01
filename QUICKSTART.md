# CP-ABE Secure Cloud Storage System - Quick Reference

## 🚀 Quick Start (3 Simple Steps)

### Step 1: Install Dependencies
```bash
cd /Users/avaamo/Desktop/swinnyyy
pip3 install -r requirements.txt
```

### Step 2: Start Server
```bash
python3 app.py
```
Server will run at: `http://localhost:5000`

### Step 3: Test the System
Open another terminal:
```bash
cd /Users/avaamo/Desktop/swinnyyy
python3 test_system.py
```

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend with API endpoints |
| `policy_engine.py` | Policy evaluation (AND/OR logic) |
| `encryption.py` | AES encryption/decryption |
| `storage.py` | Local and S3 storage manager |
| `config.py` | Configuration settings |
| `requirements.txt` | Python dependencies |
| `test_system.py` | Automated test suite |
| `examples.py` | Usage examples and demonstrations |
| `start.sh` | Quick start script |
| `README.md` | Complete documentation |

---

## 🔌 API Endpoints Reference

### 1. Encrypt File
```bash
curl -X POST http://localhost:5000/encrypt \
  -F "file=@yourfile.pdf" \
  -F "policy=Role=Doctor AND Department=CSE"
```

### 2. Decrypt File
```bash
curl -X POST http://localhost:5000/decrypt \
  -H "Content-Type: application/json" \
  -d '{
    "encrypted_filename": "encrypted_yourfile.pdf",
    "user_attributes": {"Role": "Doctor", "Department": "CSE"}
  }' \
  --output decrypted.pdf
```

### 3. List All Files
```bash
curl http://localhost:5000/list
```

### 4. Get Metrics
```bash
curl http://localhost:5000/metrics
```

---

## 📋 Policy Examples

| Policy | Meaning |
|--------|---------|
| `Role=Doctor` | User must be a Doctor |
| `Role=Doctor AND Department=CSE` | User must be Doctor AND in CSE dept |
| `Role=Doctor OR Role=Admin` | User can be either Doctor OR Admin |
| `Department=IT AND Role=Manager` | User must be IT Manager |

---

## 🧪 Testing Scenarios

### Test 1: Valid Access
```python
# Encrypt with policy
policy = "Role=Doctor AND Department=CSE"

# Decrypt with matching attributes
user_attributes = {
    "Role": "Doctor",
    "Department": "CSE"
}
# ✅ Result: Access Granted
```

### Test 2: Invalid Access
```python
# Same policy
policy = "Role=Doctor AND Department=CSE"

# Try with non-matching attributes
user_attributes = {
    "Role": "Nurse",
    "Department": "CSE"
}
# ❌ Result: Access Denied
```

---

## ☁️ AWS S3 Configuration

### Enable S3 Mode
```bash
export STORAGE_MODE=s3
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export S3_BUCKET_NAME=your-bucket-name
python3 app.py
```

---

## 📊 Monitoring

### View Logs
```bash
tail -f cpabe_system.log
```

### Check System Metrics
```bash
curl http://localhost:5000/metrics
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Edit `config.py` and change `FLASK_PORT` |
| Dependencies error | Run `pip3 install -r requirements.txt` |
| AWS credentials | Run `aws configure` or set env variables |
| Connection refused | Make sure Flask app is running |

---

## 📞 Support Commands

### Test Policy Engine
```bash
python3 policy_engine.py
```

### Run Example Demonstrations
```bash
python3 examples.py
```

### Full Test Suite
```bash
python3 test_system.py
```

---

## 🎯 Key Features

✅ **AES Encryption** - Fast, secure file encryption  
✅ **Policy-Based Access** - AND/OR attribute matching  
✅ **Local & S3 Storage** - Flexible storage options  
✅ **Resource Monitoring** - CPU, memory, disk tracking  
✅ **RESTful API** - Easy integration  
✅ **Comprehensive Logging** - Audit trail and debugging  
✅ **CloudWatch Ready** - AWS monitoring compatible  

---

## 📚 Documentation

Full documentation: See `README.md`

For more examples: Run `python3 examples.py`

---

**Created**: March 2026  
**Version**: 1.0.0  
**Status**: Production-Ready Prototype
