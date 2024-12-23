## SSH login with portforward

```bash
export REMOTEHOST=(ip address)
```

```bash
ssh ubuntu@$REMOTEHOST -i $LAMBDA_PRIVATE_KEY -L 6080:localhost:6080
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

Then, logout once and log back in.

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

## GPU

```bash
cd ~/dev-border/docker_amd64
sh build_gpu.sh
```

```bash
sh run_gpu.sh
```

## Copy mlrun in the remote host

```bash
scp -r -i $LAMBDA_PRIVATE_KEY ubuntu@$REMOTEHOST:/home/ubuntu/border/mlruns $HOME/data/border
```