## SSH login with portforward

```bash
ssh ubuntu@$REMOTEHOST -i ~/.ssh/20240817_lambda -L 6080:localhost:6080
```

## Install Docker

```bash
sudo apt-get remove containerd.io && \
sudo apt -y update && sudo apt -y install docker.io \
     nvidia-container-toolkit && \
sudo systemctl daemon-reload && \
sudo systemctl restart docker
```

## Add the user to the docker group

```bash
sudo adduser "$(id -un)" docker
```

Then, login to the host. Check if GPU is working.

```bash
docker run --gpus all border_headless nvidia-smi
```

## Clone repositories

```bash
cd $HOME
git clone https://github.com/taku-y/dev-border.git
git clone https://github.com/taku-y/border.git
```

## Build Docker image

```bash
cd ~/dev-border/docker_amd64
sh build.sh
```

## Run Docker container

```bash
sh run.sh
```
