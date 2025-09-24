#!/bin/bash

# Digital Signage Installation Script for Raspberry Pi
# Sicoob Credisete - Sistema de Sinalização Digital

set -e

echo "=== Digital Signage Installation Script ==="
echo "Installing Digital Signage Player for Raspberry Pi"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as a regular user, not root"
    exit 1
fi

# Update package list
echo "Updating package list..."
sudo apt update

# Install required packages
echo "Installing required packages..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    chromium-browser \
    vlc \
    feh \
    cec-utils \
    git \
    curl \
    wget \
    htop \
    vim \
    tmux

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install requests psutil

# Create digital signage directory
echo "Creating digital signage directory..."
mkdir -p ~/digital_signage
cd ~/digital_signage

# Clone or copy the player script
echo "Setting up player script..."
# Assuming the script is copied to this location
# You can also clone from a repository:
# git clone https://github.com/your-repo/digital-signage.git .

# Make script executable
chmod +x digital_signage_player.py

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/digital-signage.service > /dev/null <<EOF
[Unit]
Description=Digital Signage Player
After=network.target
Wants=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/digital_signage
ExecStart=/usr/bin/python3 $HOME/digital_signage/digital_signage_player.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable digital-signage.service
sudo systemctl start digital-signage.service

# Configure Chromium for kiosk mode
echo "Configuring Chromium for kiosk mode..."
mkdir -p ~/.config/chromium/Default
echo '{"first_run":false,"optimize_webui_for_touch":true}' > ~/.config/chromium/Default/Preferences

# Configure screen rotation (optional)
echo "Setting up screen rotation configuration..."
# This will be configured based on agency settings

# Configure auto-start
echo "Configuring auto-start..."
mkdir -p ~/.config/autostart
tee ~/.config/autostart/digital-signage.desktop > /dev/null <<EOF
[Desktop Entry]
Type=Application
Name=Digital Signage Player
Exec=$HOME/digital_signage/digital_signage_player.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

# Set up log rotation
echo "Setting up log rotation..."
sudo tee /etc/logrotate.d/digital-signage > /dev/null <<EOF
$HOME/digital_signage/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF

# Create configuration file template
echo "Creating configuration template..."
tee digital_signage_config.json > /dev/null <<EOF
{
    "agency_id": 1,
    "device_id": "raspberry_pi_$(hostname)",
    "api_url": "http://your-api-server:8000/api/v1",
    "orientation": "horizontal",
    "hibernation_enabled": true,
    "hibernation_start": "18:00",
    "hibernation_end": "08:00",
    "check_interval": 30,
    "status_interval": 300
}
EOF

# Make configuration file writable
chmod 644 digital_signage_config.json

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit digital_signage_config.json with your API server details"
echo "2. Reboot the Raspberry Pi: sudo reboot"
echo "3. Check service status: sudo systemctl status digital-signage"
echo "4. View logs: sudo journalctl -u digital-signage -f"
echo ""
echo "The digital signage player will start automatically after reboot."
