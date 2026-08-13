#!/bin/bash

# Generate random passwords for teacher and student accounts
export TEACHER_PASSWORD=$(openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 16)
export STUDENT_PASSWORD=$(openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 16)

echo "[+] Generated random passwords for teacher and student accounts"

# Set up environment variables
export CHROME_PATH=/usr/bin/google-chrome
export CLIENT_SECRET=$(openssl rand -base64 32)
export JWT_SECRET=$(openssl rand -base64 32)
export SESSION_SECRET=$(openssl rand -base64 32)
export CGO_ENABLED=1
export FLAG="HTB{f4k3_fl4g_f0r_t3st1ng}"

echo "127.0.0.1 edulearn.htb sso.edulearn.htb" >> /etc/hosts

# Start Supervisor
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf