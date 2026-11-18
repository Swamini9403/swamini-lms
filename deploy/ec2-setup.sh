#!/usr/bin/env bash
# Idempotent EC2 bootstrap: installs Docker Engine, Buildx + Compose plugins, git and swap.
# Works on Amazon Linux 2023 and Ubuntu. Also run by the GitHub Actions deploy job.
set -euo pipefail

ARCH=$(uname -m)                                   # x86_64 / aarch64
case "$ARCH" in x86_64) BX_ARCH=amd64 ;; aarch64) BX_ARCH=arm64 ;; *) BX_ARCH=$ARCH ;; esac
PLUGINS=/usr/local/lib/docker/cli-plugins

if ! command -v docker >/dev/null 2>&1; then
  echo ">> Installing Docker Engine"
  if grep -qi "amazon linux" /etc/os-release; then
    sudo dnf install -y docker git
  else
    curl -fsSL https://get.docker.com | sudo sh
    sudo apt-get install -y git
  fi
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER"
fi

sudo mkdir -p "$PLUGINS"
if ! sudo docker compose version >/dev/null 2>&1; then
  echo ">> Installing Docker Compose plugin"
  sudo curl -fsSL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${ARCH}" -o "$PLUGINS/docker-compose"
  sudo chmod +x "$PLUGINS/docker-compose"
fi
if ! sudo docker buildx version >/dev/null 2>&1; then
  echo ">> Installing Docker Buildx plugin"
  BX_VER=$(curl -fsSL https://api.github.com/repos/docker/buildx/releases/latest | grep -m1 '"tag_name"' | cut -d'"' -f4)
  sudo curl -fsSL "https://github.com/docker/buildx/releases/download/${BX_VER}/buildx-${BX_VER}.linux-${BX_ARCH}" -o "$PLUGINS/docker-buildx"
  sudo chmod +x "$PLUGINS/docker-buildx"
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
sudo docker buildx version
