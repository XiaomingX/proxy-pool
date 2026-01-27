#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Updating system..."
apt update && apt upgrade -y

echo "Installing Squid and Apache2-utils..."
apt install squid apache2-utils -y

# Configuration variables
SQUID_CONF="/etc/squid/squid.conf"
PASSWD_FILE="/etc/squid/passwd"
PORT=3128

# Ask for username and password
echo "Please enter the username for the proxy:"
read -r USERNAME
echo "Please enter the password for the proxy:"
read -s DEFAULT_PASSWORD

# Create password file
htpasswd -bc "$PASSWD_FILE" "$USERNAME" "$DEFAULT_PASSWORD"

# Backup original config
cp "$SQUID_CONF" "$SQUID_CONF.bak"

echo "Configuring Squid..."
cat <<EOF > "$SQUID_CONF"
# Basic Auth
auth_param basic program /usr/lib/squid/basic_ncsa_auth $PASSWD_FILE
auth_param basic children 5
auth_param basic realm Squid Proxy-Caching Web Server
auth_param basic credentialsttl 2 hours
acl authenticated proxy_auth REQUIRED

# Allow authenticated users
http_access allow authenticated

# Port
http_port $PORT

# Disable cache (optional, for anonymity)
cache deny all

# Hide client IP (High Anonymity)
forwarded_for off
request_header_access Via deny all
request_header_access X-Forwarded-For deny all

# Deny everything else
http_access deny all
EOF

# Restart Squid
systemctl restart squid

# Get Public IP (for display)
PUBLIC_IP=$(curl -s ifconfig.me)

echo "--------------------------------------------"
echo "Proxy Server Installed Successfully!"
echo "IP: $PUBLIC_IP"
echo "Port: $PORT"
echo "Username: $USERNAME"
echo "Password: $DEFAULT_PASSWORD"
echo "--------------------------------------------"
echo "Usage string: http://$USERNAME:$DEFAULT_PASSWORD@$PUBLIC_IP:$PORT"
echo "--------------------------------------------"
