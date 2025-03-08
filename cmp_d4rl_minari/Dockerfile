ARG BASE_IMAGE=ubuntu:22.04
FROM --platform=linux/amd64 ${BASE_IMAGE}

ARG TORCH_URL=https://download.pytorch.org/whl/cpu

# Adapted from https://qiita.com/takahashiakari/items/f096e5bcdfecf3d5ba90
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install --no-install-recommends --fix-missing -y xfce4 xfce4-goodies tigervnc-standalone-server novnc websockify sudo xterm init systemd snapd vim net-tools curl wget git tzdata
RUN apt update -y && apt install -y dbus-x11 x11-utils x11-xserver-utils x11-apps
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:mozillateam/ppa -y
RUN echo 'Package: *' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Pin: release o=LP-PPA-mozillateam' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Pin-Priority: 1001' >> /etc/apt/preferences.d/mozilla-firefox
RUN echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:jammy";' | tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
RUN apt update -y && apt install -y firefox
RUN apt update -y && apt install -y xubuntu-icon-theme
RUN touch /root/.Xauthority
EXPOSE 5901
EXPOSE 6080

ENV DEBIAN_FRONTEND noninteractive
RUN echo "Set disable_coredump false" >> /etc/sudo.conf
RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4EB27DB2A3B88B8B
RUN apt-get update -q && \
    apt-get upgrade -yq && \
    apt-get install -yq wget curl git build-essential vim sudo libssl-dev

# clang
RUN apt install -y -q libclang-dev

# sdl
RUN apt update -y && \
    apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive && \
    apt install -y -q --no-install-recommends \
        libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-net-dev libsdl2-ttf-dev \
        libsdl-image1.2-dev

# zip
RUN apt install -y zip

# swig
RUN apt install -y swig

# python
RUN apt install -y python3.10 python3.10-dev python3.10-distutils python3.10-venv python3-pip

# cmake
RUN apt install -y cmake

# headers required for building libtorch
RUN apt install -y libgoogle-glog-dev libgflags-dev

# llvm, mesa for robosuite
RUN apt install -y llvm libosmesa6-dev

# Used for Mujoco
RUN apt install -y patchelf libglfw3 libglfw3-dev

# Used for minari
RUN apt-get update && \
    apt install -y libhdf5-serial-dev --fix-missing

# Cleanup
RUN rm -rf /var/lib/apt/lists/*

# Use bash
RUN mv /bin/sh /bin/sh_tmp && ln -s /bin/bash /bin/sh

# rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# python
RUN cd /root && python3 -m venv venv
RUN source /root/venv/bin/activate && pip3 install --upgrade pip
RUN source /root/venv/bin/activate && pip3 install torch==1.11.0+cu113 --extra-index-url ${TORCH_URL}
RUN source /root/venv/bin/activate && pip3 install mujoco==2.1.2
RUN source /root/venv/bin/activate && pip3 install gym[mujoco_py,classic_control]==0.23.0
RUN source /root/venv/bin/activate && pip3 install "Cython<3"
RUN source /root/venv/bin/activate && pip3 install git+https://github.com/tinkoff-ai/d4rl@master#egg=d4rl
RUN source /root/venv/bin/activate && pip3 install tqdm==4.64.0
RUN source /root/venv/bin/activate && pip3 install wandb==0.12.21
RUN source /root/venv/bin/activate && pip3 install pyrallis==0.3.1
RUN source /root/venv/bin/activate && pip3 uninstall scipy -y
RUN source /root/venv/bin/activate && pip3 install numpy==1.21.3

RUN mkdir -p /root/.mujoco \
    && wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz \
    && tar -xf mujoco.tar.gz -C /root/.mujoco \
    && rm mujoco.tar.gz

# SSH, enabling VScode remote development
RUN apt update && apt install -y openssh-server
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Japanese
RUN apt install -y fonts-noto-cjk language-pack-ja

# .bashrc
RUN echo 'export LIBTORCH=$HOME/venv/lib/python3.10/site-packages/torch' >> ~/.bashrc
RUN echo 'export LD_LIBRARY_PATH=$LIBTORCH/lib' >> ~/.bashrc
RUN echo 'export LD_LIBRARY_PATH=/root/.mujoco/mujoco210/bin:$LD_LIBRARY_PATH' >> ~/.bashrc
RUN echo 'export LIBTORCH_CXX11_ABI=0' >> ~/.bashrc
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
RUN echo 'export PYTHONPATH=$HOME/border/border-py-gym-env/examples:$PYTHONPATH' >> ~/.bashrc
RUN echo 'export CARGO_TARGET_DIR=$HOME/target' >> ~/.bashrc
RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.mujoco/mujoco210/bin' >> ~/.bashrc
RUN echo 'export MUJOCO_GL=glfw' >> ~/.bashrc
RUN echo 'source $HOME/venv/bin/activate' >> ~/.bashrc
# RUN echo 'export RUSTFLAGS="-C target-feature=+fp16"' >> ~/.bashrc

# Aliases
RUN echo "alias gs='git status'" >> ~/.bashrc
RUN echo "alias gb='git branch'" >> ~/.bashrc
RUN echo "alias gd='git diff'" >> ~/.bashrc
RUN echo "alias gd1='git diff HEAD^'" >> ~/.bashrc
RUN echo "alias gd2='git diff HEAD^^ HEAD^'" >> ~/.bashrc
RUN echo "alias gd3='git diff HEAD^^^ HEAD^^'" >> ~/.bashrc
RUN echo "alias gd4='git diff HEAD^^^^ HEAD^^^'" >> ~/.bashrc
RUN echo "alias gl='git lg -5'" >> ~/.bashrc
RUN echo "alias gll='git lg -10'" >> ~/.bashrc
RUN echo "alias glll='git lg'" >> ~/.bashrc
RUN echo "alias gpo='git push origin'" >> ~/.bashrc
RUN echo "alias gfo='git fetch origin'" >> ~/.bashrc
RUN echo "alias hl='highlight -O rtf --style=molokai'" >> ~/.bashrc
RUN echo "alias cl='clear'" >> ~/.bashrc
RUN echo "alias hg='history | grep '" >> ~/.bashrc
RUN echo "alias dps='docker ps'" >> ~/.bashrc
RUN echo "alias dpa='docker ps -a'" >> ~/.bashrc
RUN echo "alias tml='tmux list-sessions'" >> ~/.bashrc
RUN echo "alias tma='tmux a -t'" >> ~/.bashrc
RUN echo "alias tms='tmux new -s'" >> ~/.bashrc
RUN echo "alias tr2='tree -L 2'" >> ~/.bashrc
RUN echo "alias tr3='tree -L 3'" >> ~/.bashrc
RUN echo "alias tr4='tree -L 4'" >> ~/.bashrc

RUN rm /bin/sh && mv /bin/sh_tmp /bin/sh

CMD bash -c "vncserver -localhost no -SecurityTypes None -geometry 1024x768 --I-KNOW-THIS-IS-INSECURE && openssl req -new -subj "/C=JP" -x509 -days 365 -nodes -out self.pem -keyout self.pem && websockify -D --web=/usr/share/novnc/ --cert=self.pem 6080 localhost:5901 && service ssh start && tail -f /dev/null"
