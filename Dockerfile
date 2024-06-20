FROM ubuntu:24.10

ARG DOCKER_HOME="/opt/yijun"
ARG DOCKER_CODE="/opt/yijun/code"
ARG DOCKER_USER="yijun"
ARG DOCKER_UID=5000
ARG PYTHON_VER=3.10.12

ARG BUILD_DEPS="wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev"

RUN apt-get upgrade -y && apt-get install -y $BUILD_DEPS && apt-get install -y libpq-dev libbz2-dev openssh-client git sudo

# Install Python
RUN wget https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz && \
    tar xzf Python-$PYTHON_VER.tgz && cd Python-$PYTHON_VER && \
    ./configure --enable-optimizations && \
    make altinstall && \
    ln -sf /usr/local/bin/python3.10 /usr/local/bin/python && \
    rm -rf /Python-$PYTHON_VER.tgz /Python-$PYTHON_VER
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && rm get-pip.py

RUN useradd -d ${DOCKER_HOME} -m -U -u ${DOCKER_UID} ${DOCKER_USER}

RUN sudo -H pip install poetry

RUN --mount=type=ssh,id=private_key \
    mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    poetry config virtualenvs.create false && \
    poetry config installer.max-workers 6 && \
    poetry install --without dev --no-interaction && \
    rm poetry.lock pyproject.toml

RUN apt-get purge -y $BUILD_DEPS

USER ${DOCKER_USER}

WORKDIR ${DOCKER_CODE}

ENV PYTHONPATH=.
ENV PORT=8000
ENV HOST=0.0.0.0
ENV WORKER_NUM=3

COPY --chown=${DOCKER_USER} . .
# gunicorn 'app.main:create_app()'  -w 1 -b 0.0.0.0:8000  # --worker-class gevent
CMD gunicorn 'app.main:create_app()'  -w 1 -b 0.0.0.0:8000