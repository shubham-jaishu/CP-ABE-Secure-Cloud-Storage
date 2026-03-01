# Deployment Guide - CP-ABE Secure Cloud Storage

## Table of Contents
1. [Local Development Deployment](#local-development-deployment)
2. [AWS EC2 Deployment](#aws-ec2-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Production Considerations](#production-considerations)

---

## 1. Local Development Deployment

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Steps

```bash
# Navigate to project
cd /Users/avaamo/Desktop/swinnyyy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Access
- Server: `http://localhost:5000`
- Logs: `cpabe_system.log`

---

## 2. AWS EC2 Deployment

### 2.1 Launch EC2 Instance

1. **Go to AWS Console → EC2 → Launch Instance**

2. **Configure Instance:**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.small (minimum), t2.medium (recommended)
   - Key Pair: Create/select existing key
   
3. **Configure Security Group:**
   ```
   Type            Protocol    Port    Source
   SSH             TCP         22      Your IP
   HTTP            TCP         80      0.0.0.0/0
   Custom TCP      TCP         5000    0.0.0.0/0
   HTTPS           TCP         443     0.0.0.0/0
   ```

4. **Storage:** 20 GB minimum

5. **Launch Instance**

### 2.2 Connect to Instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

### 2.3 Setup Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Install AWS CLI (for S3 access)
sudo apt install awscli -y

# Configure AWS credentials
aws configure
```

### 2.4 Upload Application

**Option A: SCP Upload**
```bash
# From your local machine
scp -i your-key.pem -r /Users/avaamo/Desktop/swinnyyy ubuntu@<EC2-IP>:~/
```

**Option B: Git Clone**
```bash
# On EC2 instance
cd ~
git clone <your-repo-url> swinnyyy
cd swinnyyy
```

### 2.5 Install and Run

```bash
cd ~/swinnyyy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables for S3
export STORAGE_MODE=s3
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>
export S3_BUCKET_NAME=cpabe-encrypted-files

# Run with nohup (background)
nohup python app.py > output.log 2>&1 &

# Check if running
ps aux | grep app.py
```

### 2.6 Configure Nginx Reverse Proxy (Production)

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/cpabe
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name <your-domain-or-ip>;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cpabe /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2.7 Setup Systemd Service (Auto-start)

```bash
sudo nano /etc/systemd/system/cpabe.service
```

Add:
```ini
[Unit]
Description=CP-ABE Secure Cloud Storage
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/swinnyyy
Environment="PATH=/home/ubuntu/swinnyyy/venv/bin"
Environment="STORAGE_MODE=s3"
Environment="AWS_ACCESS_KEY_ID=<your-key>"
Environment="AWS_SECRET_ACCESS_KEY=<your-secret>"
Environment="S3_BUCKET_NAME=cpabe-encrypted-files"
ExecStart=/home/ubuntu/swinnyyy/venv/bin/python /home/ubuntu/swinnyyy/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable cpabe
sudo systemctl start cpabe
sudo systemctl status cpabe
```

### 2.8 Setup CloudWatch Monitoring

```bash
# Download CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb

# Create configuration
sudo nano /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

Add configuration:
```json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/home/ubuntu/swinnyyy/cpabe_system.log",
            "log_group_name": "/cpabe/application",
            "log_stream_name": "{instance_id}",
            "timezone": "UTC"
          }
        ]
      }
    }
  },
  "metrics": {
    "namespace": "CPABESystem",
    "metrics_collected": {
      "cpu": {
        "measurement": [
          {"name": "cpu_usage_idle"},
          {"name": "cpu_usage_iowait"}
        ],
        "metrics_collection_interval": 60
      },
      "disk": {
        "measurement": [
          {"name": "used_percent"}
        ],
        "metrics_collection_interval": 60
      },
      "mem": {
        "measurement": [
          {"name": "mem_used_percent"}
        ],
        "metrics_collection_interval": 60
      }
    }
  }
}
```

```bash
# Start CloudWatch Agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

---

## 3. Docker Deployment

### 3.1 Create Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 3.2 Create docker-compose.yml

```yaml
version: '3.8'

services:
  cpabe-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - STORAGE_MODE=local
      # For S3 mode:
      # - STORAGE_MODE=s3
      # - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      # - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      # - S3_BUCKET_NAME=cpabe-encrypted-files
    volumes:
      - ./encrypted_files:/app/encrypted_files
      - ./metadata:/app/metadata
      - ./cpabe_system.log:/app/cpabe_system.log
    restart: unless-stopped
```

### 3.3 Build and Run

```bash
# Build image
docker build -t cpabe-storage .

# Run container
docker run -d -p 5000:5000 --name cpabe-app cpabe-storage

# OR use docker-compose
docker-compose up -d

# View logs
docker logs -f cpabe-app
```

---

## 4. Production Considerations

### 4.1 Security Hardening

```bash
# 1. Use HTTPS (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# 2. Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# 3. Disable Flask debug mode
# Edit config.py:
DEBUG_MODE = False
```

### 4.2 Environment Variables

Create `.env` file:
```bash
STORAGE_MODE=s3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=cpabe-encrypted-files
FLASK_PORT=5000
LOG_LEVEL=INFO
```

Load with:
```bash
export $(cat .env | xargs)
```

### 4.3 Backup Strategy

```bash
# Backup metadata
aws s3 sync metadata/ s3://cpabe-backups/metadata/

# Backup encryption key (SECURE LOCATION!)
aws s3 cp encryption.key s3://cpabe-secure-keys/ --sse AES256

# Automated backup script
crontab -e
# Add: 0 2 * * * /home/ubuntu/swinnyyy/backup.sh
```

### 4.4 Monitoring Setup

```bash
# Install monitoring tools
pip install prometheus-flask-exporter

# Add to app.py:
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)

# Access metrics at /metrics endpoint
```

### 4.5 Load Balancing (High Availability)

```bash
# Use AWS Application Load Balancer
# 1. Create Target Group (port 5000)
# 2. Register EC2 instances
# 3. Create ALB
# 4. Configure health checks: /
```

### 4.6 Performance Optimization

```python
# config.py additions:
FLASK_WORKERS = 4  # Gunicorn workers
FLASK_THREADS = 2  # Threads per worker

# Run with Gunicorn:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Testing Deployment

### Verify Endpoints

```bash
# Health check
curl http://your-server:5000/

# Encrypt test
curl -X POST http://your-server:5000/encrypt \
  -F "file=@test.txt" \
  -F "policy=Role=Admin"

# Metrics
curl http://your-server:5000/metrics

# List files
curl http://your-server:5000/list
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | `sudo lsof -ti:5000 \| xargs kill -9` |
| Permission denied | `chmod +x app.py` or run with sudo |
| AWS credentials error | Run `aws configure` |
| S3 bucket access denied | Check IAM policy and bucket policy |
| Nginx not forwarding | Check `/var/log/nginx/error.log` |
| Service won't start | Check `sudo journalctl -u cpabe -n 50` |

---

## Maintenance Commands

```bash
# View application logs
tail -f ~/swinnyyy/cpabe_system.log

# Restart service
sudo systemctl restart cpabe

# Update application
cd ~/swinnyyy
git pull
sudo systemctl restart cpabe

# Check disk space
df -h

# Monitor system resources
htop
```

---

**Deployment Checklist:**

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] AWS credentials configured (if using S3)
- [ ] S3 bucket created and accessible
- [ ] Security group properly configured
- [ ] Nginx configured (production)
- [ ] SSL certificate installed (production)
- [ ] Systemd service configured
- [ ] CloudWatch agent installed
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Load testing completed
- [ ] Documentation updated

---

**Support**: For deployment issues, check logs at `cpabe_system.log`
