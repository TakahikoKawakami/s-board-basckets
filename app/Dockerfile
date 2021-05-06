# See here for image contents: https://github.com/microsoft/vscode-dev-containers/blob/v0.163.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# ENV PYTHON_VERSION 3.9.3
ENV HOME /root
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
# ENV PYENV_ROOT $HOME/.pyenv
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
        vim \
        gcc \
        git \
        make
RUN apt-get install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    wget \
    ruby
# RUN apt-get install -y \
#     wget \
#     llvm \
#     libncurses5-dev \
#     libncursesw5-dev \
#     xz-utils \
#     tk-dev
RUN apt-get install -y \
    libffi-dev \
    liblzma-dev
#  && git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
#  && $PYENV_ROOT/plugins/python-build/install.sh
# RUN /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT
# RUN rm -rf $PYENV_ROOT

# COPY requirements.txt /opt/app/

RUN pip install --upgrade pip setuptools wheel

# for nodejs
RUN apt-get install -y nodejs npm

# for ultrahook
# RUN echo "api_key: {{your api key}}" > ~/.ultrahook
RUN gem install ultrahook
#&& ultrahook look-into-baskets http://0.0.0.0:5500

WORKDIR /root
