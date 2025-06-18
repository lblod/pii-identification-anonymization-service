FROM semtech/mu-python-template:2.0.0-beta.3
LABEL maintainer="info@redpencil.io"

RUN python -m spacy download en_core_web_lg