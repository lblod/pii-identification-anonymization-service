FROM semtech/mu-python-template:feature-upgrade-python-with-gunicorn
LABEL maintainer="info@redpencil.io"

RUN python -m spacy download en_core_web_lg