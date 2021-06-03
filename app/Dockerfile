# See here for image contents: https://github.com/microsoft/vscode-dev-containers/blob/v0.163.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
# FROM python:3.9

# add software-properties-common to install "add-apt-repository" command for installing neovim
RUN apt-get update && apt-get -y upgrade && apt-get install -y software-properties-common

# ubuntu18以降でtzdataとgitを同時に入れると止まってしまうので、gitだけ外だし+ nointeractiveを追加
RUN apt-get update && apt-get -y upgrade && apt-get install -y git
RUN apt-get update && apt-get -y upgrade && apt-get install -y --fix-missing\
    locales-all \
    apt-utils \
    gawk \
    wget \
    curl \
    unzip \
    libtool-bin \
    libtool \
    libncurses5-dev \
    libzip-dev \
    libicu-dev \
    libonig-dev \
    sudo \
    zsh \
    sed \
    make \
    cmake \
    automake \
    gcc \
    g++ \
    gettext \
    gpg \
    musl-dev \
    ncurses-dev \
    tzdata \
    nginx \
    python \
    python-dev \
    python3 \
    python3-dev \
    python3-pip \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    wget \
    ruby \
  && mkdir /home/ubuntu \
  && rm -f /etc/nginx/sites-enabled/default \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y \
    libffi-dev \
    liblzma-dev
#  && git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
#  && $PYENV_ROOT/plugins/python-build/install.sh
# RUN /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT
# RUN rm -rf $PYENV_ROOT

# COPY requirements.txt /opt/app/

RUN pip3 install --upgrade pip setuptools wheel

# for ultrahook
# RUN echo "api_key: {{your api key}}" > ~/.ultrahook
RUN gem install ultrahook
#&& ultrahook look-into-baskets http://0.0.0.0:5500

# neovim
RUN pip3 install --upgrade pip
RUN pip3 install neovim
RUN pip3 install pynvim
RUN pip3 uninstall -y msgpack && pip3 install msgpack

# upgrade latest node and npm, and install yarn
# RUN npm install n -g && n stable \
#     && apt purge -y nodejs npm \
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update && apt-get upgrade -y && apt-get install -y nodejs \
    && curl -qL https://www.npmjs.com/install.sh | sh \
    && npm install -g --force yarn

# create docker user instead of root
# ARG USER_NAME
# ARG UID
# ARG GID
# RUN groupadd -g ${GID} ${USER_NAME}
# ENV HOME=/home/${USER_NAME}
# RUN useradd -u ${UID} -g ${GID} -s /bin/bash -m ${USER_NAME} \
#   && echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/${USER_NAME} &&\
#   chown -R ${USER_NAME} ${HOME}
USER vscode

# dotfilees
ENV TERMINFO=/usr/lib/terminfo
ENV TERM=xterm
ENV LC_ALL en_US.UTF-8
RUN cd ${HOME} \
    && git clone https://github.com/shabaraba/dotfiles.git \
    && cd dotfiles \
    && sudo make install \
    && make deploy


# ENV PYTHON_VERSION 3.9.3
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
# ENV PYENV_ROOT $HOME/.pyenv

WORKDIR /var/www/html
#CMD cd ${HOME}/dotfiles && systemctl start snapd && make install
