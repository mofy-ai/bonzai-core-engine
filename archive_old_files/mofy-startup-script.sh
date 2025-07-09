#!/bin/bash
# MOFY Instant VM Startup Script
# Created: July 5, 2025
# Purpose: Rapid Docker + Python environment setup

echo "=== MOFY INSTANT VM STARTUP INITIATED ==="
echo "Timestamp: $(date)"

# Update system
apt-get update -y

# Install essential packages
apt-get install -y \
    docker.io \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    python3-venv \
    htop \
    nano \
    unzip

# Start and enable Docker
systemctl start docker
systemctl enable docker

# Add default user to docker group
usermod -aG docker $USER

# Create working directory
mkdir -p /opt/mofy
cd /opt/mofy

# Log completion
echo "MOFY VM READY - $(date)" > /var/log/mofy-ready.log
echo "CHALLENGE VM ONLINE!" >> /var/log/mofy-ready.log
echo "Docker status: $(systemctl is-active docker)" >> /var/log/mofy-ready.log

# Create success marker
touch /opt/mofy/vm-ready.marker

echo "=== MOFY INSTANT VM STARTUP COMPLETE ==="
echo "VM Ready at: $(date)"
