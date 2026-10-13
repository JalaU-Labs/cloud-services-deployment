# Docker Installation

This document explains how to install Docker Engine and Docker Compose on the
three systems used during the lab: Arch Linux (local development), Ubuntu
(common in cloud images), and Amazon Linux 2023 (the EC2 instance).

Always install Docker from the official distribution repositories or the
official Docker repository. Avoid third-party scripts unless they come from
`get.docker.com`, which is maintained by Docker itself.

## 1. Arch Linux

Docker is available in the `extra` repository.

```bash
sudo pacman -Syu
sudo pacman -S docker docker-compose docker-buildx
```

Enable and start the daemon:

```bash
sudo systemctl enable --now docker.service
```

By default, only `root` can talk to the Docker socket. Add your user to the
`docker` group to avoid prefixing every command with `sudo`:

```bash
sudo usermod -aG docker $USER
```

Log out and back in for the group change to take effect, or run:

```bash
newgrp docker
```

Verify:

```bash
docker --version
docker compose version
docker run --rm hello-world
```

If `docker run` fails with a permission error, the group change did not take
effect. Log out of the session completely and log back in.

## 2. Ubuntu 22.04 / 24.04

Use the official Docker repository to get an up-to-date version.

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
```

Enable and start:

```bash
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
```

Verify with the same commands as in the Arch section.

## 3. Amazon Linux 2023

Amazon Linux 2023 ships with a recent Docker version in its own repositories.

```bash
sudo dnf update -y
sudo dnf install -y docker
```

Enable and start:

```bash
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user
```

Log out of the SSH session and back in for the group change to apply.

Docker Compose v2 is distributed as a plugin. Install it from the Docker
GitHub releases:

```bash
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL \
    https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
    -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

Verify:

```bash
docker --version
docker compose version
```

## 4. Verifying the Installation

On any of the three systems, the following commands must work without `sudo`:

```bash
docker ps
docker images
docker compose version
```

If `docker ps` returns `permission denied while trying to connect to the Docker
daemon socket`, the user is not in the `docker` group or the session needs to be
restarted.

## 5. Disk Usage Management

Docker accumulates images, containers, and volumes over time. To reclaim space:

```bash
# Remove all stopped containers, unused networks, dangling images, and build cache
docker system prune -a

# Remove unused volumes as well (careful: this deletes data)
docker system prune -a --volumes
```

Run `docker system df` to see how much space is currently used.

## 6. Security Notes

- The `docker` group is effectively equivalent to `root` on the host. Anyone in
  it can mount the host filesystem into a container. Do not add users you do
  not trust.
- Never expose the Docker daemon socket (`/var/run/docker.sock`) over TCP
  without TLS. Doing so is equivalent to handing out root access.
- On the EC2 instance, restrict the inbound rules of the Security Group as
  described in `02-aws-ec2-setup.md`. The Docker daemon does not need any
  inbound port other than the ones you explicitly publish.