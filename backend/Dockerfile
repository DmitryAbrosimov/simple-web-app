FROM python:3.11.15-slim

ARG EXPOSE_BACKEND_PORT=8080
ENV EXPOSE_BACKEND_PORT=${EXPOSE_BACKEND_PORT}

ARG BACKEND_WORKDIR=/app_dir
ENV BACKEND_WORKDIR=${BACKEND_WORKDIR}

RUN groupadd -r app_grp && \
    useradd -r -g app_grp app_usr && \
    mkdir -p ${BACKEND_WORKDIR} && \
    chown app_usr:app_grp ${BACKEND_WORKDIR}

COPY --chown=app_usr:app_grp --chmod=755 app.py ${BACKEND_WORKDIR}/app.py

WORKDIR ${BACKEND_WORKDIR}

EXPOSE ${EXPOSE_BACKEND_PORT}

USER app_usr

ENTRYPOINT python ${BACKEND_WORKDIR}/app.py --port ${EXPOSE_BACKEND_PORT}
