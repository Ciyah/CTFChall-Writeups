#!/bin/bash
echo "[+] Waiting for SSO service..."
until [ "$(curl -s -o /dev/null -w "%{http_code}" http://sso.edulearn.htb:1337/login)" -eq 200 ]; do 
    echo "SSO service is not ready yet, waiting..."
    sleep 5
done
echo "[+] Starting bot..."
exec npm start