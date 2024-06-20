FROM ubuntu:22.04

ARG DOCKER_HOME="/opt/yijun"
ARG DOCKER_CODE="/opt/yijun/code"
ARG DOCKER_GROUP="yijun"
ARG DOCKER_USER="yijun"
ARG DOCKER_UID=5000

WORKDIR ${DOCKER_CODE}

RUN groupadd -g ${DOCKER_UID} ${DOCKER_GROUP} \
    && useradd -r -u ${DOCKER_UID} -g ${DOCKER_GROUP} -d ${DOCKER_HOME} ${DOCKER_USER} \
    && chown -R ${DOCKER_USER}:${DOCKER_GROUP} ${DOCKER_HOME}

RUN echo ${DOCKER_USER} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${DOCKER_USER} && \
    chmod 0440 /etc/sudoers.d/${DOCKER_USER}

# Install git if there are stuff needs to install from git
RUN mkdir ${DOCKER_HOME}/.ssh && \
    chown -R ${DOCKER_USER} ${DOCKER_HOME}/.ssh && \
    apt-get update && apt-get install -y --fix-missing curl openssh-client git sudo && \
    ssh-keyscan bitbucket.org >> ${DOCKER_HOME}/.ssh/known_hosts && \
    echo "alias docker='sudo docker'" > ${DOCKER_HOME}/.bashrc

COPY poetry.lock pyproject.toml ./

RUN --mount=type=ssh,id=private_key \
    mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    poetry config virtualenvs.create false && \
    poetry config installer.max-workers 6 && \
    poetry install --without dev --no-interaction && \
    rm poetry.lock pyproject.toml

ENV PATH "$PATH:/opt/yijun/.local/bin"

USER ${DOCKER_USER}

ENV PYTHONPATH=.
ENV PORT=8000
ENV HOST=0.0.0.0
ENV WORKER_NUM=1

COPY --chown=${DOCKER_USER} . .

CMD gunicorn -w $WORKER_NUM -k gevent -b $HOST:$PORT --log-level info app.patched:app