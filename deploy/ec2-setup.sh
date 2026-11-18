#!/usr/bin/env bash
# Idempotent EC2 bootstrap: installs Docker Engine + Compose plugin and adds swap.
# Works on Ubuntu and Amazon Linux 2023. Run by the GitHub Actions deploy job.
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo ">> Installing Docker"
  if [ -f /etc/os-release ] && grep -qi "amazon linux" /etc/os-release; then
    sudo dnf install -y docker
  else
    curl -fsSL https://get.docker.com | sudo sh
  fi
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER"
fi

if ! sudo docker compose version >/dev/null 2>&1; then
  echo ">> Installing Docker Compose plugin"
  ARCH=$(uname -m)
  sudo mkdir -p /usr/local/lib/docker/cli-plugins
  sudo curl -fsSL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${ARCH}" \
    -o /usr/local/lib/docker/cli-plugins/docker-compose
  sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
fi

# Small instances (t2/t3.micro) need swap to run MySQL + Django comfortably
if [ "$(swapon --show | wc -l)" -eq 0 ]; then
  echo ">> Adding 2G swap"
  sudo fallocate -l 2G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
  sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi

sudo docker --version
sudo docker compose version
