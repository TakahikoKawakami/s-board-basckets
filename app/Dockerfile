# See here for image contents: https://github.com/microsoft/vscode-dev-containers/blob/v0.163.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
# FROM python:3.9

# add software-properties-common to install "add-apt-repository" command for installing neovim
RUN apt-get update && apt-get -y upgrade && apt-get install -y software-properties-common

# for git
ARG GIT_USER_NAME
ARG GIT_USER_EMAIL
RUN apt-get update && apt-get -y upgrade && apt-get install -y git \
    &&git config --global user.name ${GIT_USER_NAME} && git config --global user.name ${GIT_USER_NAME}

RUN apt-get update && apt-get -y upgrade && apt-get install -y --fix-missing\
    default-mysql-client \
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
ARG USE_ULTRAHOOK
ARG ULTRAHOOK_KEY
ARG ULTRAHOOK_URL
RUN if [ "${USE_ULTRAHOOK}" = true ]; then \
        gem install ultrahook \
        echo "api_key: ${ULTRAHOOK_KEY}" > ~/.ultrahook \
        ultrahook ${ULTRAHOOK_URL} http://0.0.0.0:${ULTRAHOOK_PORT}; \
    fi

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
COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# RUN expect -c " \
#     pip3 install -r app/requirements.txt; \
#     expect name ; send ${GIT_USER_NAME}  ; \
#     expect password ; send ${GIT_PASSWORD} ; \
#     expect $ ; exit"
# RUN rm requirements.txt
